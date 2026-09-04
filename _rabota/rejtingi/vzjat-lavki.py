#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Цены специализированных винных лавок с их собственных сайтов.

Зачем. Винотека держит то, чего нет ни в супермаркете, ни у хозяйства:
привозные линейки, малые партии, старые урожаи. Часть таких лавок мы
уже берём поимённо — «Vinoteka Beograd», «Wine Stars», «Wine Art»,
«Cerpromet», «Prodaja vina», — но каждую своим разбором вёрстки.
Здесь берутся остальные, и одним способом: у сербских лавок почти
поголовно WooCommerce, а у него открыт Store API.

    https://<сайт>/wp-json/wc/store/products?per_page=100&page=N

Тот же приём, что у магазинов хозяйств (`vzjat-vinarije.py`), и те же
ловушки: разметка в поле имени, наборы бутылок вместо бутылки, ракије
и подарочные коробки в одном каталоге с вином.

Откуда список сайтов. Из карточек площадок Wolt: у заведения в
`schema.org/Store` стоит поле `sameAs` — адрес его собственного сайта.
Пятьдесят четыре из шестидесяти восьми винотек его указали, и это
готовый перечень специализированных лавок Сербии, собранный не на глаз.
Часть из них указывает вместо сайта страницу в Instagram или сам Wolt —
такие сюда не идут. Остальные перечислены в `LAVKI` руками, с пометкой,
что это за лавка: список короткий, ведётся глазами и требует проверки.

Цена приходит в мелких единицах: `price` 285000 при `currency_minor_unit`
2 — это 2850,00 динара.

Пишет `lavki-ceny.json`. Кеш — в `kesh-lavki/`.
"""
import argparse
import concurrent.futures
import html
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-lavki"
SROK = 25
POTOKOV = 5
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
PUTI = ("/wp-json/wc/store/products?per_page=100&page=%d",
        "/wp-json/wc/store/v1/products?per_page=100&page=%d")
PUT_SHOPIFY = "/products.json?limit=250&page=%d"

# Набор бутылок, а не бутылка.
NABOR = re.compile(r"\bpaket|\bboc[ae]\b|\bbo[cč]a\b|\bset\b|\bkutij|"
                   r"\d\s*[x×]\s*0[.,]\d+|\bgift\s*box", re.I)
# Не вино. Лавка держит и ракију, и джин, и бокалы, и подарки.
NE_VINO = re.compile(r"rakij|lozova[cč]|liker|viski|whisk|vodka|votka|"
                     r"d[zž]in\b|\bgin\b|konjak|cognac|rum\b|tekil|"
                     r"vermut|bermut|pivo|\bsok\b|voda\b|"
                     r"poklon|suvenir|[cč]a[sš]e|[cč]ep\b|otvara|dekanter|"
                     r"maslin|\bmed\b|[cč]aj\b|kozmetik|knjig|majic|"
                     r"gift|souvenir|glass|sir\b|[dž]em\b|prsut|"
                     r"tartuf|[cč]okolad", re.I)


def imya_tovara(syroe):
    """WooCommerce кладёт в поле имени разметку и экранированные знаки."""
    syroe = re.sub(r"<[^>]+>", " ", html.unescape(syroe or ""))
    return re.sub(r"\s+", " ", syroe).strip()


def vzjat(imya_kesha, adres):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    tekst = ""
    for popytka in range(2):
        try:
            zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
            with urllib.request.urlopen(zapros, timeout=SROK) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError:
            break
        except Exception:
            if popytka:
                break
            time.sleep(2)
    fajl.write_text(tekst, encoding="utf-8")
    return tekst


def cena_iz(zapis, minor=2):
    """Цена WooCommerce — строка в мелких единицах."""
    syroe = zapis.get("prices") or {}
    znak = syroe.get("price")
    edinic = syroe.get("currency_minor_unit")
    if znak is None:
        return None
    try:
        chislo = float(znak) / (10 ** int(edinic if edinic is not None else minor))
    except (TypeError, ValueError):
        return None
    return round(chislo, 2) or None


def stranicy_woo(adres, klyuch):
    """Все страницы каталога WooCommerce; пустая страница — конец."""
    for put in PUTI:
        vse, stranica = [], 1
        while stranica <= 40:
            tekst = vzjat("%s-woo-%d.json" % (klyuch, stranica),
                          adres + (put % stranica))
            try:
                kus = json.loads(tekst)
            except ValueError:
                break
            if not isinstance(kus, list) or not kus:
                break
            vse += kus
            stranica += 1
        if vse:
            return vse, "woocommerce"
    return [], ""


def stranicy_shopify(adres, klyuch):
    vse, stranica = [], 1
    while stranica <= 20:
        tekst = vzjat("%s-shop-%d.json" % (klyuch, stranica),
                      adres + (PUT_SHOPIFY % stranica))
        try:
            kus = (json.loads(tekst) or {}).get("products") or []
        except ValueError:
            break
        if not kus:
            break
        vse += kus
        stranica += 1
    return vse, ("shopify" if vse else "")


def tovary_lavki(imya, adres):
    klyuch = re.sub(r"\W+", "-", adres.split("//")[-1])[:40]
    syroe, rod = stranicy_woo(adres, klyuch)
    if not syroe:
        syroe, rod = stranicy_shopify(adres, klyuch)
    najdeno = []
    for t in syroe:
        nazvanie = imya_tovara(t.get("name") or t.get("title"))
        if not nazvanie or NABOR.search(nazvanie) or NE_VINO.search(nazvanie):
            continue
        if rod == "woocommerce":
            cena = cena_iz(t)
            v_prodazhe = t.get("is_in_stock")
        else:
            varianty = t.get("variants") or [{}]
            try:
                cena = round(float(varianty[0].get("price")), 2)
            except (TypeError, ValueError):
                cena = None
            v_prodazhe = varianty[0].get("available")
        najdeno.append({
            "vino": nazvanie,
            "cena_rsd": cena,
            "v_prodazhe": True if v_prodazhe is None else bool(v_prodazhe),
            "magazin": imya,
            "stranica": t.get("permalink") or adres,
        })
    return najdeno, rod, len(syroe)


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--lavka", help="взять одну лавку по имени домена")
    kljuchi = razbor.parse_args()

    spisok = json.loads((ZDES / "lavki-spisok.json").read_text(encoding="utf-8"))
    lavki = [z for z in spisok["lavki"]
             if not kljuchi.lavka or kljuchi.lavka in z["adres"]]
    print("лавок в списке: %d" % len(lavki))

    vse, svodka = [], []
    with concurrent.futures.ThreadPoolExecutor(POTOKOV) as bassejn:
        zadachi = {bassejn.submit(tovary_lavki, z["imya"], z["adres"]): z
                   for z in lavki}
        for zadacha in concurrent.futures.as_completed(zadachi):
            z = zadachi[zadacha]
            try:
                najdeno, rod, vsego = zadacha.result()
            except Exception as oshibka:
                print("  %-30s ошибка: %s" % (z["imya"][:30], str(oshibka)[:50]))
                continue
            vse += najdeno
            svodka.append((z["imya"], rod, vsego, len(najdeno)))
    for imya, rod, vsego, vin in sorted(svodka):
        print("  %-30s %-13s товаров %4d, вин %4d" % (imya[:30], rod or "—", vsego, vin))

    s_cenoj = sum(1 for z in vse if z["cena_rsd"])
    (ZDES / "lavki-ceny.json").write_text(json.dumps({
        "chto_eto": "Цены специализированных винных лавок с их собственных "
                    "сайтов: Store API WooCommerce и Shopify.",
        "istochnik": "сайты лавок, перечень — в lavki-spisok.json",
        "sobrano": time.strftime("%Y-%m-%d"),
        "lavok": len({z["magazin"] for z in vse}),
        "vina": vse,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nпозиций %d, с ценой %d, лавок с товаром %d → lavki-ceny.json"
          % (len(vse), s_cenoj, len({z["magazin"] for z in vse})))


if __name__ == "__main__":
    main()
