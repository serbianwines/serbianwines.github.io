#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка целостности таблиц рейтингов.

Скрипт только читает. Он говорит, что в данных не сходится, — правится
сырьё (`vivino-zapisi.jsonl`, `kritiki-zapisi.jsonl`, `raion-hozyaistv.json`)
и таблицы пересобираются `sobrat-tablicy.py`.

    python3 _rabota/rejtingi/proverit-dannye.py

Код возврата 0 — чисто, 1 — есть замечания.
"""

import json
import os
import sys

RYADOM = os.path.dirname(os.path.abspath(__file__))

SHKALY = {
    "vivino": (5, 1.0, 5.0),
    "falstaff": (100, 50, 100),
    "wine-searcher": (100, 50, 100),
    "vino.rs": (100, 50, 100),
    "tastings": (100, 50, 100),
    "decanter": (100, 50, 100),
}


def chitat(imya):
    return [json.loads(s) for s in
            open(os.path.join(RYADOM, imya), encoding="utf-8") if s.strip()]


def main():
    hozyaistva = chitat("hozyaistva.jsonl")
    vina = chitat("vina.jsonl")
    ocenki = chitat("ocenki.jsonl")
    nagrady = chitat("nagrady.jsonl")

    zamechaniya = []

    def proverka(imya, plohie, kak_pokazat):
        if plohie:
            zamechaniya.append((imya, [kak_pokazat(p) for p in plohie]))
            print("✗ %s — %d" % (imya, len(plohie)))
        else:
            print("✓ %s" % imya)

    # Ссылочная целостность
    klyuchi_vin = {v["klyuch"] for v in vina}
    proverka("оценки без своего вина",
             [o for o in ocenki if o["klyuch_vina"] not in klyuchi_vin],
             lambda o: "%s · %s" % (o["hozyaistvo"], o["vino"]))

    proverka("награды без своего вина",
             [n for n in nagrady if n["klyuch_vina"] and n["klyuch_vina"] not in klyuchi_vin],
             lambda n: "%s · %s" % (n["hozyaistvo"], n["vino"]))

    imena_hozyaistv = {h["hozyaistvo"] for h in hozyaistva}
    proverka("вина без своего хозяйства",
             [v for v in vina if v["hozyaistvo"] not in imena_hozyaistv],
             lambda v: "%s · %s" % (v["hozyaistvo"], v["vino"]))

    proverka("награды без своего хозяйства",
             [n for n in nagrady if n["hozyaistvo"] not in imena_hozyaistv],
             lambda n: n["hozyaistvo"])

    # Дубли ключей
    vidano = {}
    dubli = []
    for v in vina:
        if v["klyuch"] in vidano:
            dubli.append(v)
        vidano[v["klyuch"]] = v
    proverka("дубли ключей вин", dubli, lambda v: v["klyuch"])

    # Одно измерение на источник, вино и урожай
    pary, povtory = set(), []
    for o in ocenki:
        para = (o["klyuch_vina"], o["istochnik"], o["god"])
        if para in pary:
            povtory.append(o)
        pary.add(para)
    proverka("повтор измерения (источник + вино + урожай)", povtory,
             lambda o: "%s · %s [%s %s]" % (o["hozyaistvo"], o["vino"],
                                            o["istochnik"], o["god"] or "все"))

    # Шкалы и диапазоны
    ne_v_shkale = []
    for o in ocenki:
        shkala = SHKALY.get(o["istochnik"])
        if not shkala:
            ne_v_shkale.append(o)
            continue
        nazvanie, nizhe, vyshe = shkala
        if o["shkala"] != nazvanie or not (nizhe <= o["ball"] <= vyshe):
            ne_v_shkale.append(o)
    proverka("балл вне шкалы источника", ne_v_shkale,
             lambda o: "%s · %s = %s [%s]" % (o["hozyaistvo"], o["vino"],
                                              o["ball"], o["istochnik"]))

    # Выборка есть только там, где она осмысленна
    chuzhaya_vyborka = [o for o in ocenki
                        if o["istochnik"] != "vivino" and o["vyborka"]]
    proverka("число отзывов у оценки критика", chuzhaya_vyborka,
             lambda o: "%s · %s" % (o["hozyaistvo"], o["vino"]))

    otricatelnaya = [o for o in ocenki if o["vyborka"] is not None and o["vyborka"] < 1]
    proverka("выборка меньше одного", otricatelnaya,
             lambda o: "%s · %s" % (o["hozyaistvo"], o["vino"]))

    # Полнота, о которой надо знать, но это не поломка
    print()
    bez_raiona = [h for h in hozyaistva if not h["raion_knigi"]]
    bez_vyborki = [o for o in ocenki if o["istochnik"] == "vivino" and not o["vyborka"]]
    print("не поломка, но знать стоит:")
    print("   хозяйств без района книги: %d — %s"
          % (len(bez_raiona), ", ".join(h["hozyaistvo"] for h in bez_raiona) or "нет"))
    print("   оценок Vivino без числа отзывов: %d из %d"
          % (len(bez_vyborki),
             sum(1 for o in ocenki if o["istochnik"] == "vivino")))
    print("   вин без идентификатора Vivino: %d из %d"
          % (sum(1 for v in vina if not v["vivino_id"]), len(vina)))
    print("   наград: %d, из них хозяйству целиком: %d"
          % (len(nagrady), sum(1 for n in nagrady if not n["vino"])))

    if zamechaniya:
        print("\nЗамечания:")
        for imya, spisok in zamechaniya:
            print(" %s:" % imya)
            for s in spisok[:12]:
                print("   ", s)
            if len(spisok) > 12:
                print("    … и ещё %d" % (len(spisok) - 12))
        return 1
    print("\nЧисто. Проверка механическая — она не говорит, что данные верны,")
    print("только что они согласованы между собой.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
