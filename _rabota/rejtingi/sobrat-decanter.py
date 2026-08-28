#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Медали Decanter World Wine Awards по Сербии, все годы.

Поиск наград на сайте конкурса — сценарий поверх собственного API, и через
поисковую выдачу оттуда не видно ничего. Само API открыто и отдаёт по каждому
вину сразу всё: хозяйство, имя, урожай, цвет, стиль, медаль и **балл**.

    https://decanterresultsapi.decanter.com/api/DWWA/<год>/wines/search?country=Serbia

Балл здесь — не оценка одного критика, а результат слепой дегустации жюри,
и шкала у него стобалльная. Поэтому медали идут в `nagrady-zapisi.jsonl`,
а баллы — в `kritiki-zapisi.jsonl`: это два разных высказывания об одном вине.

    python3 _rabota/rejtingi/sobrat-decanter.py
    python3 _rabota/rejtingi/sobrat-decanter.py --gody 2024 2025 2026
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
KESH = os.path.join(RYADOM, "kesh-decanter")
API = ("https://decanterresultsapi.decanter.com/api/DWWA/%d"
       "/wines/search?country=Serbia")

ZAGOLOVKI = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "application/json",
    "Origin": "https://awards.decanter.com",
    "Referer": "https://awards.decanter.com/",
}

# Числовой код награды. Сверено по данным 2026 года: платина ровно 97,
# золото 95, серебро 90–93, бронза 86–89.
MEDALI = {
    1: ("best-in-show", "Best in Show"),
    2: ("best-in-show", "Best in Show"),
    3: ("platina", "платина"),
    4: ("platina", "платина"),
    5: ("zlato", "золото"),
    6: ("srebro", "серебро"),
    7: ("bronza", "бронза"),
}


def vzyat(god):
    os.makedirs(KESH, exist_ok=True)
    put = os.path.join(KESH, "dwwa-%d.json" % god)
    if os.path.exists(put):
        return json.load(open(put, encoding="utf-8"))
    zapros = urllib.request.Request(API % god, headers=ZAGOLOVKI)
    try:
        with urllib.request.urlopen(zapros, timeout=60) as otvet:
            telo = otvet.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        sys.stderr.write("DWWA %d: HTTP %s\n" % (god, e.code))
        return []
    with open(put, "w", encoding="utf-8") as f:
        f.write(telo)
    time.sleep(1.0)
    return json.loads(telo)


def dopisat(imya, zapisi, klyuchi):
    put = os.path.join(RYADOM, imya)
    bylo = {}
    if os.path.exists(put):
        for stroka in open(put, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[tuple(z.get(k) for k in klyuchi)] = z
    novyh = 0
    for z in zapisi:
        k = tuple(z.get(x) for x in klyuchi)
        if k not in bylo:
            novyh += 1
        bylo[k] = z
    with open(put, "w", encoding="utf-8") as f:
        for z in bylo.values():
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    print("%s: всего %d, новых %d" % (imya, len(bylo), novyh))


def main():
    razbor = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    razbor.add_argument("--gody", type=int, nargs="+",
                        default=list(range(2015, 2027)))
    dovody = razbor.parse_args()

    nagrady, ocenki, po_godam = [], [], {}
    for god in dovody.gody:
        stroki = vzyat(god)
        if not stroki:
            continue
        po_godam[god] = len(stroki)
        print("DWWA %d: %d медалей" % (god, len(stroki)))
        for z in stroki:
            kod, imya_medali = MEDALI.get(z.get("award"), ("", ""))
            if not kod:
                continue
            hozyaistvo = (z.get("producer") or "").strip()
            vino = (z.get("name") or "").strip()
            if not (hozyaistvo and vino):
                continue
            urozhaj = z.get("vintage")
            urozhaj = int(urozhaj) if str(urozhaj).isdigit() else None
            adres = "awards.decanter.com, DWWA %d, вино %s" % (god, z.get("id"))

            nagrady.append({
                "istochnik": "decanter",
                "god": god,
                "kategoriya": imya_medali,
                "mesto": kod,
                "hozyaistvo": hozyaistvo,
                "vino": vino,
                "urozhaj": urozhaj,
                "stranica": adres,
            })
            ball = z.get("score")
            if isinstance(ball, (int, float)) and 50 <= ball <= 100:
                ocenki.append({
                    "istochnik": "decanter",
                    "hozyaistvo": hozyaistvo,
                    "vino": vino,
                    "god": str(urozhaj) if urozhaj else None,
                    "konkurs_god": god,
                    "ball": int(ball),
                    "stranica": adres,
                })

    if not nagrady:
        sys.exit("ничего не получено")

    dopisat("nagrady-zapisi.jsonl", nagrady,
            ["istochnik", "god", "kategoriya", "hozyaistvo", "vino"])
    dopisat("kritiki-zapisi.jsonl", ocenki,
            ["istochnik", "hozyaistvo", "vino", "god", "konkurs_god"])

    print("\nпо годам: %s" % ", ".join(
        "%d — %d" % (g, n) for g, n in sorted(po_godam.items())))
    print("всего медалей %d, из них с баллом %d" % (len(nagrady), len(ocenki)))


if __name__ == "__main__":
    main()
