#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавить записи в nagrady-zapisi.jsonl — награды и места в категориях.

Строки вида

    Источник | год | категория | место | Хозяйство | Вино | урожай | адрес

Награда — не балл. «Лучшее белое из местных сортов 2025 года» и «92 балла
Falstaff» устроены по-разному: у первого нет шкалы, зато есть категория и
год, у второго наоборот. Поэтому награды лежат отдельно от оценок, а не
переводятся в числа.

Поле «место»: `1` — победитель категории, `2`, `3` — если названы; `zlato`,
`srebro`, `bronza`, `platina`, `best-in-show` — для конкурсных медалей.
"""
import json
import os
import sys

FAJL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nagrady-zapisi.jsonl")


def main():
    bylo = {}
    if os.path.exists(FAJL):
        for stroka in open(FAJL, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[(z["istochnik"], z["god"], z["kategoriya"],
                      z["hozyaistvo"], z["vino"])] = z

    for stroka in sys.stdin:
        stroka = stroka.strip()
        if not stroka or stroka.startswith("#"):
            continue
        ch = [c.strip() for c in stroka.split("|")]
        if len(ch) < 6:
            sys.exit("не разобрано: %s" % stroka)
        z = {
            "istochnik": ch[0],
            "god": int(ch[1]) if ch[1] else None,
            "kategoriya": ch[2],
            "mesto": ch[3],
            "hozyaistvo": ch[4],
            "vino": ch[5],
            "urozhaj": int(ch[6]) if len(ch) > 6 and ch[6] else None,
            "stranica": ch[7] if len(ch) > 7 else "",
        }
        bylo[(z["istochnik"], z["god"], z["kategoriya"],
              z["hozyaistvo"], z["vino"])] = z

    with open(FAJL, "w", encoding="utf-8") as f:
        for z in bylo.values():
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    po_istochnikam = {}
    for z in bylo.values():
        po_istochnikam[z["istochnik"]] = po_istochnikam.get(z["istochnik"], 0) + 1
    sys.stderr.write("всего %d: %s\n" % (len(bylo), ", ".join(
        "%s %d" % (k, v) for k, v in sorted(po_istochnikam.items()))))


if __name__ == "__main__":
    main()
