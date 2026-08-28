#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавить записи в kritiki-zapisi.jsonl — стобалльные оценки критиков.

Строки вида

    Источник | Хозяйство | Вино | урожай | балл | адрес

Источник: falstaff, wine-searcher, tastings, decanter, suckling.
Это не Vivino: у Vivino пятибалльная оценка толпы, здесь стобалльная
оценка экспертов. Смешивать их в одном числе нельзя, и книга не должна.

Строки берутся со стандартного входа или из файла, если он назван первым
доводом, — на Windows это единственный удобный способ:

    py -3 dobavit-kritiki.py dobavka.txt
"""
import json
import os
import sys

# На русской Windows консоль по умолчанию не UTF-8, и первая же кириллица
# в выводе роняет скрипт с UnicodeEncodeError. Просим UTF-8 явно.
for _potok in (sys.stdout, sys.stderr, sys.stdin):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

FAJL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kritiki-zapisi.jsonl")


def otkryt_vhod():
    """Строки со входа: из файла, если он назван, иначе из stdin.

    В PowerShell и cmd нет heredoc, и подать строки на stdin неудобно.
    Поэтому на Windows проще положить их в файл и передать его именем:

        py -3 dobavit-kritiki.py dobavka.txt
    """
    if len(sys.argv) > 1:
        return open(sys.argv[1], encoding="utf-8").read().splitlines()
    return sys.stdin


def main():
    bylo = {}
    if os.path.exists(FAJL):
        for stroka in open(FAJL, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[(z["istochnik"], z["hozyaistvo"], z["vino"], z["god"])] = z

    for stroka in otkryt_vhod():
        stroka = stroka.strip()
        if not stroka or stroka.startswith("#"):
            continue
        ch = [c.strip() for c in stroka.split("|")]
        if len(ch) < 5:
            sys.exit("не разобрано: %s" % stroka)
        z = {
            "istochnik": ch[0],
            "hozyaistvo": ch[1],
            "vino": ch[2],
            "god": ch[3] or None,
            "ball": int(ch[4]) if ch[4] and ch[4] != "-" else None,
            "stranica": ch[5] if len(ch) > 5 else "",
        }
        bylo[(z["istochnik"], z["hozyaistvo"], z["vino"], z["god"])] = z

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
