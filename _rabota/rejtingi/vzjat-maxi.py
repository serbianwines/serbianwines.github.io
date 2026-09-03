#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Разобрать сохранённую страницу винного раздела Maxi Online.

Супермаркетная полка — единственный срез, которого не хватало: в винотеке
нет ни Жупы, ни Врањца за девятьсот динаров, а именно там живёт вино,
о котором читатель спрашивает «что взять в супермаркете».

Машиной Maxi не берётся: каталог виден картой сайта, но цену страница
подгружает сценарием, и адрес их товарного API в разметке не назван.
Зато страница, открытую человеком, можно сохранить (Ctrl+S) — в ней уже
всё нарисовано. Тот же приём, что с Falstaff.

    py -3 _rabota/rejtingi/vzjat-maxi.py "Vino.html"

Сохранять надо **прокрученную до конца** страницу: список подгружается
частями. Сколько всего вин в разделе, страница пишет сама — «Prikaži N
proizvoda».

Пишет `maxi-ceny.json`.
"""
import html
import json
import pathlib
import re
import sys
import time

ZDES = pathlib.Path(__file__).resolve().parent

# Карточка товара: марка, имя, цена. Цена разбита на три узла —
# «69», «99», «RSD», — потому что копейки нарисованы надстрочными.
# Страница режется по метке карточки, а не сопоставляется одним
# выражением с окном: расстояние между карточками у Maxi доходит до
# десятка тысяч знаков, и окно на четыре тысячи пропускало почти всё —
# из двухсот шести карточек находились три.
METKA = 'data-testid="product-block-name-link"'
ZAGOLOVOK = re.compile(r'title="([^"]*)"')
ADRES = re.compile(r'href="([^"]*)"')
MARKA = re.compile(r'data-testid="product-brand">([^<]*)<')
IMYA = re.compile(r'data-testid="product-name">([^<]*)<')
# Целая часть бывает с разделителем разрядов: «1.019». Первая редакция
# читала только `\d+` и находила цену у 98 карточек из 203 — все, что
# дороже тысячи динаров, выпадали, то есть как раз вино, а не спрайсер.
CENA = re.compile(
    r'data-testid="product-block-price"[^>]*>\s*'
    r'<div[^>]*>([\d.]+)</div>\s*<sup[^>]*>(\d+)</sup>', re.S)
STARAYA = re.compile(r'data-testid="product-block-old-price"[^>]*'
                     r'aria-label="[^:]*:\s*([\d.,]+)')
OBEM = re.compile(r'(\d+(?:[.,]\d+)?)\s*(l|ml)\b', re.I)
# «Ovaj proizvod više nije dostupan»: у снятой с продажи позиции цены нет
# вовсе. Это не сбой разбора, а состояние полки, и его надо сохранить.
NET_V_PRODAZHE = 'data-testid="product-block-unavailable-text"' 


def obem_litrov(imya):
    """Объём из имени: «0.75l», «200 ml», «1.5 l»."""
    sovpalo = OBEM.search(imya or "")
    if not sovpalo:
        return None
    chislo = float(sovpalo.group(1).replace(",", "."))
    return chislo / 1000 if sovpalo.group(2).lower() == "ml" else chislo


def razobrat(stranica):
    vina = []
    for hvost in stranica.split(METKA)[1:]:
        cena = CENA.search(hvost)
        marka = MARKA.search(hvost)
        imya = IMYA.search(hvost)
        staraya = STARAYA.search(hvost)
        zagolovok = ZAGOLOVOK.search(hvost[:400])
        adres = ADRES.search(hvost[:600])
        polnoe = html.unescape(imya.group(1) if imya
                               else zagolovok.group(1) if zagolovok else "")
        if not polnoe:
            continue
        vina.append({
            "vino": polnoe.strip(),
            "hozyaistvo": html.unescape(marka.group(1)).strip() if marka else "",
            "cena_rsd": (float("%s.%s" % (cena.group(1).replace(".", ""),
                                          cena.group(2))) if cena else None),
            "cena_bez_skidki": (float(staraya.group(1).replace(",", "."))
                                if staraya else None),
            "litrov": obem_litrov(polnoe),
            "v_prodazhe": NET_V_PRODAZHE not in hvost[:3000],
            "stranica": adres.group(1) if adres else "",
        })
    return vina


def main():
    fajly = [pathlib.Path(a) for a in sys.argv[1:]]
    if not fajly:
        raise SystemExit("нужен путь к сохранённой странице раздела «Vino»")
    vina, vidano = [], set()
    vsego = None
    for fajl in fajly:
        stranica = fajl.read_text(encoding="utf-8", errors="replace")
        schet = re.search(r'Prikaži\s+(\d+)\s+proizvoda', stranica)
        if schet:
            vsego = int(schet.group(1))
        for z in razobrat(stranica):
            klyuch = (z["hozyaistvo"], z["vino"])
            if klyuch in vidano:
                continue
            vidano.add(klyuch)
            vina.append(z)
        print("%s: разобрано %d" % (fajl.name, len(vina)))
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    snyato = sum(1 for z in vina if not z["v_prodazhe"])
    (ZDES / "maxi-ceny.json").write_text(json.dumps({
        "chto_eto": "Винный раздел Maxi Online: цена в динарах, марка, объём. "
                    "Супермаркетная полка — то, чего нет в винотеках.",
        "istochnik": "maxi.rs, раздел «Пиће, кафа и чај → Вино», "
                     "сохранённая страница",
        "sobrano": time.strftime("%Y-%m-%d"),
        "vsego_v_razdele": vsego,
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nв разделе %s позиций; собрано %d, с ценой %d, снято с продажи %d"
          " → maxi-ceny.json" % (vsego if vsego else "?", len(vina),
                                 s_cenoj, snyato))


if __name__ == "__main__":
    main()
