# -*- coding: utf-8 -*-
"""Цены и свойства сербских вин у «Wine Art Shop» (wineartshop.rs).

Четвёртая винотека к трём собранным. Взята не ради ещё одной цены:
в карточке товара у неё стоит поле **«Region»**, и стоит оно рејоном —
«Pocersko valjevski rejon», «Nišavski rejon». Это единственный найденный
источник, который приписывает вино рејону сам, не через место подвала.
Показание торговли, не закона, но независимое, и сверить с ним нашу
привязку хозяйств стоит.

Кроме рејона карточка отдаёт сорт, объём, крепость, стиль (суво,
полусуво, слатко) и страну. Сладость до сих пор давал один Церпромет.

Берётся в два шага, как у «Vinoteka Beograd»:

1. **Список** `/vina?page=N`, по 27 позиций. В карточке списка уже есть
   имя, хозяйство, цена и строка «SRBIJA, VINO, SUVO» — по ней и
   отбираются сербские, чтобы не ходить за карточками чужих вин.
2. **Карточки** только сербских: `ld+json` с ценой и артикулом плюс
   таблица «Спецификације» с рејоном и сортом.

Пишет `wineart-ceny.json`. Кеш страниц — в `kesh-wineart/`.
"""
import argparse
import html
import json
import pathlib
import re
import time
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-wineart"
SAJT = "https://wineartshop.rs"
RAZDEL = SAJT + "/vina"
PAUZA = 1.5          # чужой сайт, спешить некуда
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def vzjat(adres, imya_kesha):
    """Скачать страницу, положив её в кеш; повторно — из кеша."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    # Туннель здешнего прокси иногда рвётся на середине обмена — это не
    # отказ сайта и не повод бросать сбор. Повтор с растущей паузой;
    # страницы кешируются, так что повторный запуск продолжает с места.
    for popytka in range(4):
        try:
            with urllib.request.urlopen(zapros, timeout=90) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            break
        except Exception:
            if popytka == 3:
                raise
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def chislo(stroka):
    """«1.122,00» → 1122.0. Точка — разряды, запятая — дробь."""
    stroka = (stroka or "").strip().replace(".", "").replace(",", ".")
    try:
        return float(stroka)
    except ValueError:
        return None


# Карточка списка. Магазин кладёт её одним `<article>`, и всё нужное —
# внутри: адрес, хозяйство, имя, строка «SRBIJA, VINO, SUVO» и цена.
# Режется по метке начала карточки, а не сопоставляется окном: длина
# карточки гуляет от товара к товару из-за значков и лент акций.
KARTOCHKA = 'class="product-list_item catalog-product-card'
ADRES = re.compile(r'href="(/p/[^"]+)"')
HOZYAISTVO = re.compile(r'catalog-product-card__manufacturer">([^<]*)<')
IMYA = re.compile(r'catalog-product-card__title">\s*<a[^>]*>([^<]*)</a>', re.S)
# «SRBIJA, VINO, SUVO»: страна, вид товара, стиль. Разделены запятыми,
# число полей непостоянно — у ракии стиля нет.
METKA = re.compile(r'catalog-product-card__meta">.*?<span>([^<]*)</span>', re.S)
CENA = re.compile(r'catalog-product-card__price-current">([\d.,]+)')

# Карточка товара: schema.org в `ld+json` и таблица свойств.
# Тип скрипта в разметке записан с мнемоникой: «application/ld&#x2B;json».
# Требование буквального «ld+json» не находило ничего, и цена с артикулом
# из карточки терялись молча — списочная цена их прикрывала.
TOVAR_JSON = re.compile(
    r'<script type="application/ld(?:\+|&#x2B;)json">\s*(\{.*?\})\s*</script>',
    re.S | re.I)
SVOJSTVO = re.compile(r'<dt>([^<]+)</dt><dd>([^<]*)</dd>')


def razobrat_spisok(stranica):
    najdeno = []
    for kus in stranica.split(KARTOCHKA)[1:]:
        adres = ADRES.search(kus)
        imya = IMYA.search(kus)
        if not adres or not imya:
            continue
        metka = METKA.search(kus)
        polya = [c.strip() for c in html.unescape(metka.group(1)).split(",")] \
            if metka else []
        hozyaistvo = HOZYAISTVO.search(kus)
        cena = CENA.search(kus)
        najdeno.append({
            "put": adres.group(1),
            "vino": html.unescape(imya.group(1)).strip(),
            "hozyaistvo": (html.unescape(hozyaistvo.group(1)).strip()
                           if hozyaistvo else ""),
            "strana": polya[0] if polya else "",
            "stil": polya[2] if len(polya) > 2 else "",
            "cena_rsd": chislo(cena.group(1)) if cena else None,
        })
    return najdeno


def razobrat_kartochku(stranica):
    """Свойства из таблицы «Спецификације» и артикул из `ld+json`."""
    svojstva = {html.unescape(k).strip(): html.unescape(v).strip()
                for k, v in SVOJSTVO.findall(stranica)}
    tovar = {}
    for kus in TOVAR_JSON.finditer(stranica):
        try:
            d = json.loads(html.unescape(kus.group(1)))
        except ValueError:
            continue
        if d.get("@type") == "Product":
            tovar = d
            break
    return svojstva, tovar


def litrov(zapis):
    """«0.75» — так магазин пишет объём, без единицы."""
    sovpalo = re.search(r"(\d+(?:[.,]\d+)?)", zapis or "")
    return float(sovpalo.group(1).replace(",", ".")) if sovpalo else None


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--stranic", type=int, default=40,
                        help="предел числа страниц списка")
    razbor.add_argument("--bez-kartochek", action="store_true",
                        help="только список, не ходить за карточками")
    kljuchi = razbor.parse_args()

    vina, vidano = [], set()
    for nomer in range(1, kljuchi.stranic + 1):
        adres = RAZDEL if nomer == 1 else "%s?page=%d" % (RAZDEL, nomer)
        stranica = vzjat(adres, "spisok-%d.html" % nomer)
        svoi = razobrat_spisok(stranica)
        if not svoi:
            print("  страница %2d пуста — конец раздела" % nomer)
            break
        novyh = 0
        for z in svoi:
            if z["put"] in vidano:
                continue
            vidano.add(z["put"])
            vina.append(z)
            novyh += 1
        print("  страница %2d: карточек %2d, новых %2d" % (nomer, len(svoi), novyh))
        if not novyh:
            break

    serbskie = [z for z in vina if z["strana"].upper().startswith("SRBIJ")]
    print("\nв разделе %d вин, сербских %d" % (len(vina), len(serbskie)))

    if not kljuchi.bez_kartochek:
        for nomer, z in enumerate(serbskie, 1):
            imya_kesha = "tovar-%s.html" % z["put"].rsplit("/", 1)[-1]
            try:
                stranica = vzjat(SAJT + z["put"], imya_kesha)
            except Exception as beda:            # сеть, а не разбор
                z["pochemu_net_kartochki"] = str(beda)
                continue
            svojstva, tovar = razobrat_kartochku(stranica)
            z["rejon_magazina"] = svojstva.get("Region", "")
            z["sorta"] = svojstva.get("Sorta", "")
            z["krepost"] = svojstva.get("Procenat alkohola", "")
            z["litrov"] = litrov(svojstva.get("Zapremina"))
            z["tip_vina"] = svojstva.get("Stil vina", "") or z["stil"]
            z["artikul"] = svojstva.get("SKU", "") or str(tovar.get("sku", ""))
            iz_json = ((tovar.get("offers") or {}).get("price"))
            if iz_json:
                z["cena_rsd"] = float(iz_json)
            if nomer % 25 == 0:
                print("  карточек: %d из %d" % (nomer, len(serbskie)))

    s_cenoj = sum(1 for z in serbskie if z["cena_rsd"])
    s_rejonom = sum(1 for z in serbskie if z.get("rejon_magazina"))
    (ZDES / "wineart-ceny.json").write_text(json.dumps({
        "chto_eto": "Сербские вина у «Wine Art Shop»: цена в динарах, стиль "
                    "(суво/полусуво/слатко), сорт, объём, крепость и рејон, "
                    "как его называет сам магазин.",
        "istochnik": RAZDEL,
        "sobrano": time.strftime("%Y-%m-%d"),
        "vsego_v_razdele": len(vina),
        "vina": serbskie,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d сербских вин, с ценой %d, с рејоном %d → wineart-ceny.json"
          % (len(serbskie), s_cenoj, s_rejonom))


if __name__ == "__main__":
    main()
