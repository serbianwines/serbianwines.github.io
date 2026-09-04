#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Цены винного раздела «eDiskont» — дисконта напитков.

Зачем. Дисконт напитков — не винотека и не супермаркет: у него полка
уже, чем у винотеки, но дешевле, и в неё попадает то, чего в сети нет.
Из специализированных дисконтов машине открыт один — `ediskont.rs`.

Как берётся. Каталога по API у него нет: сайт не на WooCommerce и не
на Shopify, а на своей вёрстке (в разметке попадаются следы Magento,
но ни `/graphql`, ни `/rest/` не отвечают — оба ведут на страницу
«Nema strane»). Зато раздел отдаётся целиком одним запросом:

    ediskont.rs/sr/proizvodi/vino?limit=500

Без `limit` страница показывает двадцать четыре товара и никакой
разбивки на страницы в разметке нет: остальное подгружается сценарием.
С `limit` приходит весь раздел — двести тридцать шесть позиций.

Разметка простая и держится трёх зацепок: ссылка `/sr/proizvod/<слаг>`,
имя в `product-name`, цена в `price-block`, где дробная часть вынесена
в отдельный `price_decimal`. Цена без разделителя тысяч не приходит
никогда, так что «1.323,90» разбирается как есть.

Берутся четыре цветных раздела, а не общий: цвет со страницы — это
единственное, что тут есть сверх имени и цены, и терять его жалко.

Пишет `ediskont-ceny.json`. Кеш — в `kesh-ediskont/`.
"""
import argparse
import html
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-ediskont"
KORNI = "https://www.ediskont.rs/sr/proizvodi/%s?limit=500"
RAZDELY = [("belo-vino", "белое"), ("crveno-vino", "красное"),
           ("rose-vino", "розе"), ("penusavo-vino", "игристое"),
           ("vino", None)]
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Товар в сетке — блок `product-preview-item`. Имя и адрес карточки
# лежат в ссылке `p-title`, марка — в `text-block-brand` (бывает
# пустой), цена — в `price-block`, дробная часть отдельным `span`.
# В боковом блоке страницы есть другая разметка, `product-name`:
# это «акционные товары», их десять и они те же на всех страницах.
# Первая редакция разбирала как раз её и приносила десять позиций
# вместо сотни.
BLOK = re.compile(r'<div class="product-preview-item"')
IMYA = re.compile(r'<a class="p-title"\s+href="([^"]+)">(.*?)</a>', re.S)
MARKA = re.compile(r'<p class="text-block-brand">(.*?)</p>', re.S)
CENA = re.compile(r'<span class="price">\s*([\d.]+),'
                  r'<span class="price_decimal">(\d+)</span>', re.S)
NE_VINO = re.compile(r"rakij|viski|whisk|vodka|d[zž]in\b|\bgin\b|konjak|rum\b|"
                     r"liker|vermut|pivo|\bsok\b|dispenzer|[cč]a[sš]e|otvara|"
                     r"poklon|gift|kutij", re.I)


def vzjat(imya, adres):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    tekst = ""
    for popytka in range(3):
        try:
            zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
            with urllib.request.urlopen(zapros, timeout=90) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError:
            break
        except Exception:
            if popytka == 2:
                break
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(1.0)
    return tekst


def chistoe(syroe):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", syroe or ""))).strip()


def tovary_razdela(slag):
    """Имя, адрес и цена каждого товара раздела.

    Цена ищется в куске разметки после имени и до имени следующего
    товара: в блоке рядом с ценой лежат ещё «Šifra» и «Brend», тоже
    в `<span class="price">`, но без цифр с запятой, и по образцу они
    не сходятся.
    """
    tekst = vzjat("razdel-%s.html" % slag, KORNI % slag)
    najdeno = []
    for kusok in BLOK.split(tekst)[1:]:
        imya = IMYA.search(kusok)
        if not imya:
            continue
        cena = CENA.search(kusok)
        marka = MARKA.search(kusok)
        najdeno.append({
            "vino": chistoe(imya.group(2)),
            "hozyaistvo": chistoe(marka.group(1)) if marka else "",
            "stranica": imya.group(1),
            "cena_rsd": (float(cena.group(1).replace(".", "") + "." + cena.group(2))
                         if cena else None),
        })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.parse_args()

    po_adresu = {}
    for slag, cvet in RAZDELY:
        najdeno = tovary_razdela(slag)
        novyh = 0
        for z in najdeno:
            if NE_VINO.search(z["vino"]):
                continue
            est = po_adresu.get(z["stranica"])
            if est:
                est.setdefault("cvet_magazina", cvet)
                continue
            po_adresu[z["stranica"]] = {**z, "cvet_magazina": cvet,
                                        "magazin": "eDiskont",
                                        "v_prodazhe": True}
            novyh += 1
        print("  %-16s товаров %4d, новых %4d" % (slag, len(najdeno), novyh))

    vina = sorted(po_adresu.values(), key=lambda z: z["vino"])
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "ediskont-ceny.json").write_text(json.dumps({
        "chto_eto": "Винный раздел дисконта напитков «eDiskont»: имя, цена "
                    "в динарах, цвет со страницы раздела.",
        "istochnik": "ediskont.rs/sr/proizvodi/vino?limit=500",
        "sobrano": time.strftime("%Y-%m-%d"),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nразных вин %d, с ценой %d → ediskont-ceny.json" % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
