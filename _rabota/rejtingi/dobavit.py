#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Добавить записи в vivino-zapisi.jsonl.

На вход — строки вида

    Хозяйство | Вино | оценка | число_отзывов | источник

Число отзывов может быть пустым: значит, выдача его не показала. Такие
записи в отбор не идут, но в файле остаются — по ним видно, что искать дальше.
"""
import json
import os
import sys

FAJL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vivino-zapisi.jsonl")


def main():
    bylo = {}
    if os.path.exists(FAJL):
        for stroka in open(FAJL, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[(z["hozyaistvo"], z["vino"])] = z

    dobavleno = obnovleno = 0
    for stroka in sys.stdin:
        stroka = stroka.strip()
        if not stroka or stroka.startswith("#"):
            continue
        chasti = [c.strip() for c in stroka.split("|")]
        if len(chasti) < 3:
            sys.exit("не разобрано: %s" % stroka)
        hoz, vino, ocenka = chasti[0], chasti[1], chasti[2]
        chislo = chasti[3] if len(chasti) > 3 and chasti[3] else ""
        istochnik = chasti[4] if len(chasti) > 4 else ""
        zapis = {
            "hozyaistvo": hoz,
            "vino": vino,
            "ocenka": float(ocenka.replace(",", ".")) if ocenka and ocenka != "-" else None,
            "chislo_ocenok": int(chislo) if chislo else None,
            "stranica": istochnik,
        }
        klyuch = (hoz, vino)
        if klyuch in bylo:
            # Не затираем известное число отзывов пустым.
            if zapis["chislo_ocenok"] is None:
                zapis["chislo_ocenok"] = bylo[klyuch].get("chislo_ocenok")
            if not zapis["stranica"]:
                zapis["stranica"] = bylo[klyuch].get("stranica", "")
            obnovleno += 1
        else:
            dobavleno += 1
        bylo[klyuch] = zapis

    with open(FAJL, "w", encoding="utf-8") as f:
        for z in bylo.values():
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    s_chislom = sum(1 for z in bylo.values() if z.get("chislo_ocenok"))
    sys.stderr.write("всего %d, из них с числом отзывов %d (+%d новых, %d обновлено)\n"
                     % (len(bylo), s_chislom, dobavleno, obnovleno))


if __name__ == "__main__":
    main()
