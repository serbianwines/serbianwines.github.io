#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Разобрать сохранённую страницу поиска Falstaff и добавить оценки.

Falstaff закрыт от автоматического чтения — отвечает страницей Cloudflare.
Но страницу, открытую человеком в браузере, можно сохранить (Ctrl+S) и
скормить сюда: в её разметке лежит состояние Livewire, а в нём — те же
данные, что рисует список, полями. Балл, хозяйство, урожай, район, тип
вина, имя дегустатора и название дегустации.

    py -3 _rabota/rejtingi/vzjat-falstaff.py "Weine__Falstaff.html"
    py -3 _rabota/rejtingi/vzjat-falstaff.py stranica1.html stranica2.html

Пишет в `kritiki-zapisi.jsonl`. Повторный запуск на той же странице ничего
не задваивает: ключ — источник, хозяйство, вино, урожай.

Сохранять надо **прокрученную до конца** страницу: список подгружается
частями, и в разметку попадает только то, что уже показано. Сколько всего
вин у Falstaff по Сербии, страница пишет сама — «N entries».
"""

import html
import json
import os
import re
import sys

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
FAJL = os.path.join(RYADOM, "kritiki-zapisi.jsonl")


def vytashchit_snimki(razmetka):
    """Состояния Livewire из атрибутов wire:snapshot."""
    for syroe in re.findall(r'wire:snapshot="([^"]+)"', razmetka):
        raw = html.unescape(syroe)
        if '"hits"' not in raw:
            continue
        try:
            yield json.loads(raw)
        except ValueError:
            continue


def sobrat_zapisi(uzel, najdeno):
    """Обойти вложенность и собрать всё, что похоже на карточку вина."""
    if isinstance(uzel, dict):
        if "uid" in uzel and "name" in uzel and "producer_name" in uzel:
            najdeno.append(uzel)
        for v in uzel.values():
            sobrat_zapisi(v, najdeno)
    elif isinstance(uzel, list):
        for v in uzel:
            sobrat_zapisi(v, najdeno)


def pervyj(znachenie):
    """У Falstaff почти всё завёрнуто в список с служебным довеском."""
    while isinstance(znachenie, list) and znachenie:
        znachenie = znachenie[0]
    return znachenie


def razobrat(z):
    ball = None
    rating = pervyj(z.get("rating"))
    if isinstance(rating, dict):
        ball = rating.get("points_total") or rating.get("points_list")
    if ball is None:
        ball = z.get("points")
    try:
        ball = int(ball)
    except (TypeError, ValueError):
        return None
    if not 50 <= ball <= 100:
        return None

    hozyaistvo = (z.get("producer_name") or "").strip()
    vino = (z.get("name") or "").replace(" ", " ").strip()
    if not (hozyaistvo and vino):
        return None

    degustator, degustaciya = "", ""
    ocenki = pervyj(z.get("ratings"))
    if isinstance(ocenki, dict):
        degustator = ocenki.get("tester") or ""
    tasting = pervyj(z.get("tastings"))
    if isinstance(tasting, str):
        degustaciya = tasting

    region = ""
    r = pervyj(z.get("region"))
    if isinstance(r, dict):
        region = (r.get("path") or "").replace(" Serbia", "").strip()

    vid = ""
    k = pervyj(z.get("category"))
    if isinstance(k, dict):
        vid = k.get("main") or ""

    god = z.get("year")
    slug = z.get("slug") or ""
    primechanie = " · ".join(x for x in (degustaciya, degustator) if x)

    return {
        "istochnik": "falstaff",
        "hozyaistvo": hozyaistvo,
        "vino": vino,
        "god": str(god) if god else None,
        "konkurs_god": None,
        "ball": ball,
        "vid": vid,
        "region_falstaff": region,
        "stranica": ("falstaff.com/en/wines/%s" % slug if slug else "falstaff.com")
                    + (" · " + primechanie if primechanie else ""),
    }


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)

    bylo = {}
    if os.path.exists(FAJL):
        for stroka in open(FAJL, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[(z["istochnik"], z["hozyaistvo"], z["vino"], z["god"],
                      z.get("konkurs_god"))] = z

    vsego, novyh = 0, 0
    for put in sys.argv[1:]:
        razmetka = open(put, encoding="utf-8", errors="replace").read()
        skolko = re.search(r"([\d\s]+)\s*entries", razmetka)
        kartochki = []
        for snimok in vytashchit_snimki(razmetka):
            sobrat_zapisi(snimok, kartochki)
        # Одно вино может встретиться в снимке дважды.
        po_uid = {}
        for k in kartochki:
            po_uid.setdefault(k.get("uid"), k)

        v_fajle = 0
        for k in po_uid.values():
            z = razobrat(k)
            if not z:
                continue
            v_fajle += 1
            klyuch = (z["istochnik"], z["hozyaistvo"], z["vino"], z["god"],
                      z["konkurs_god"])
            if klyuch not in bylo:
                novyh += 1
            bylo[klyuch] = z
        vsego += v_fajle
        print("%s: карточек %d, с баллом %d%s"
              % (os.path.basename(put), len(po_uid), v_fajle,
                 (", на странице заявлено %s" % skolko.group(1).strip())
                 if skolko else ""))

    with open(FAJL, "w", encoding="utf-8") as f:
        for z in bylo.values():
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    falstaff = sum(1 for z in bylo.values() if z["istochnik"] == "falstaff")
    print("\nразобрано %d, новых %d. Всего Falstaff в записях: %d"
          % (vsego, novyh, falstaff))


if __name__ == "__main__":
    main()
