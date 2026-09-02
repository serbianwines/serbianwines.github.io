# -*- coding: utf-8 -*-
"""Цены сербских вин из каталога «Vinoteka Beograd».

Цена нужна ради пятёрки «лучшее за свои деньги»: у медалей и баллов
критиков есть перекос в дорогое, и без цены его не видно. У Vivino цен
сербских вин нет вовсе (см. `istochniki-dostup.md`), агрегаторы
(cenoteka, eponuda) стоят за Cloudflare, а этот магазин отдаёт всё
обычной разметкой.

Берётся в два шага, чтобы не ходить лишний раз к чужому сайту:

1. **Список.** Раздел «Вина из Сербии», по 48 позиций на страницу.
   В разметке списка уже стоит и цена, и хозяйство (`data-productbrand`),
   и адрес карточки. Четырнадцать запросов на весь каталог.
2. **Карточки** — отдельно и только для тех вин, что дошли до отбора:
   там лежит `schema.org/Product` с ценой и, в тексте, «Tip vina: Suvo».
   Это `--kartochki` со списком ключей на входе.

Пишет `vinoteka-ceny.json`. Кеш страниц — в `kesh-vinoteka/`.
"""
import argparse, json, pathlib, re, sys, time, urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-vinoteka"
SAJT = "https://www.vinotekabeograd.com"
RAZDEL = SAJT + "/vina-iz-srbije"
NA_STRANICE = 24   # столько магазин кладёт на страницу по умолчанию
PAUZA = 1.5          # секунда с лишним между запросами: чужой сайт, спешить некуда
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def vzjat(adres, imya_kesha):
    """Скачать страницу, положив её в кеш; повторно — из кеша."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    with urllib.request.urlopen(zapros, timeout=90) as otvet:
        tekst = otvet.read().decode("utf-8", "replace")
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def chislo(stroka):
    """«4.090,00» → 4090.0. У магазина точка — разряды, запятая — дробь."""
    stroka = (stroka or "").strip().replace(".", "").replace(",", ".")
    try:
        return float(stroka)
    except ValueError:
        return None


# Блок товара в списке. Всё нужное магазин выкладывает атрибутами
# `data-*` на одном узле — имя, хозяйство, цена, артикул с урожаем, — и
# читать их надёжнее, чем вёрстку вокруг: она от раздела к разделу гуляет.
# Закрывающий «>» узла границей не работает: он же стоит внутри
# `data-productCatBread="Proizvodi > Vina > Srbija"`. Берётся окно
# фиксированной длины — атрибуты товара укладываются в тысячу знаков.
TOVAR = re.compile(r'data-productposition="\d+"(?P<polya>.{0,1200})', re.S)
POLE = lambda imya, kus: (re.search(r'data-%s="([^"]*)"' % imya, kus, re.I) or [None, ""])[1]
ADRES = re.compile(r'href="(https://www\.vinotekabeograd\.com/[^"]+)"')


def razobrat_spisok(stranica):
    """Из разметки списка вынуть имя, хозяйство, цену, артикул и адрес."""
    najdeno = []
    for kus in TOVAR.finditer(stranica):
        polya = kus.group("polya")
        nomer = POLE("productid", polya)
        if not nomer:
            continue
        # Адрес карточки лежит уже за атрибутами, в первой ссылке товара.
        hvost = stranica[kus.end():kus.end() + 1500]
        adres = ADRES.search(hvost)
        najdeno.append({
            "nomer": nomer,
            "vino": POLE("productName", polya).strip(),
            "hozyaistvo": POLE("productbrand", polya).strip(),
            "artikul": POLE("product-item-id", polya).strip(),
            "cena_rsd": chislo(POLE("productPrice", polya)),
            "stranica": adres.group(1) if adres else "",
        })
    return najdeno


def vsego_pozicij(stranica):
    sovpalo = re.search(r'products-found-number">(\d+)<', stranica)
    return int(sovpalo.group(1)) if sovpalo else 0


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--stranic", type=int, default=0,
                        help="сколько страниц списка взять (0 — весь раздел)")
    kljuchi = razbor.parse_args()

    pervaya = vzjat(RAZDEL, "spisok-1.html")
    vsego = vsego_pozicij(pervaya)
    stranic = kljuchi.stranic or (vsego + NA_STRANICE - 1) // NA_STRANICE
    print("в разделе «Вина из Сербии» %d позиций, страниц %d" % (vsego, stranic))

    vina, vidano = [], set()
    for nomer in range(1, stranic + 1):
        # Страницы у магазина — отрезок пути, а не параметр запроса.
        adres = RAZDEL if nomer == 1 else "%s/page-%d" % (RAZDEL, nomer)
        stranica = pervaya if nomer == 1 else vzjat(adres, "spisok-%d.html" % nomer)
        svoi = razobrat_spisok(stranica)
        novyh = 0
        for z in svoi:
            if z["nomer"] in vidano:
                continue
            vidano.add(z["nomer"])
            vina.append(z)
            novyh += 1
        print("  страница %2d: разобрано %2d, новых %2d" % (nomer, len(svoi), novyh))
        if not svoi:
            break

    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    put = ZDES / "vinoteka-ceny.json"
    put.write_text(json.dumps({
        "chto_eto": "Цены сербских вин у «Vinoteka Beograd», раздел «Вина из Сербии». "
                    "Цена розничная, в динарах, на день сбора.",
        "istochnik": RAZDEL,
        "sobrano": time.strftime("%Y-%m-%d"),
        "vsego_v_razdele": vsego,
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d вин, из них с ценой %d → vinoteka-ceny.json"
          % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
