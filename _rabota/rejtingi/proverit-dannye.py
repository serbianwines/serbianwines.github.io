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

# На русской Windows консоль по умолчанию не UTF-8, и первая же кириллица
# в выводе роняет скрипт с UnicodeEncodeError. Просим UTF-8 явно.
for _potok in (sys.stdout, sys.stderr, sys.stdin):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))

SHKALY = {
    "vivino": (5, 1.0, 5.0),
    "falstaff": (100, 50, 100),
    "wine-searcher": (100, 50, 100),
    "vino.rs": (100, 50, 100),
    "tastings": (100, 50, 100),
    "decanter": (100, 50, 100),
    "gilbert-gaillard": (100, 50, 100),
    "biwc": (100, 50, 100),
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
        # Одно вино может брать медаль в разные годы конкурса — это
        # разные события, а не повтор измерения.
        para = (o["klyuch_vina"], o["istochnik"], o["god"], o.get("konkurs_god"))
        if para in pary:
            povtory.append(o)
        pary.add(para)
    proverka("повтор измерения (источник + вино + урожай + год конкурса)", povtory,
             lambda o: "%s · %s [%s %s]" % (o["hozyaistvo"], o["vino"],
                                            o["istochnik"], o["god"] or "все"))

    vidano_hoz, dubli_hoz = set(), []
    for h in hozyaistva:
        if h["klyuch"] in vidano_hoz:
            dubli_hoz.append(h)
        vidano_hoz.add(h["klyuch"])
    proverka("дубли ключей хозяйств", dubli_hoz, lambda h: h["hozyaistvo"])

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

    # Рејон и виногорје — только из справочника, и виногорје обязано
    # принадлежать своему рејону. Опечатка в имени рејона иначе тихо
    # заводит двадцать третий рејон, которого в Сербии нет.
    put_spr = os.path.join(RYADOM, "rejony-vinogorja.json")
    if os.path.exists(put_spr):
        spr = json.load(open(put_spr, encoding="utf-8"))["rejony"]
        imena_rejonov = {r["rejon"] for r in spr}
        region_rejona = {r["rejon"]: r["region"] for r in spr}
        vinogorja_rejona = {r["rejon"]: {v["vinogorje"] for v in r["vinogorja"]}
                            for r in spr}
        proverka("рејон не из справочника",
                 [h for h in hozyaistva
                  if h.get("rejon") and h["rejon"] not in imena_rejonov],
                 lambda h: "%s → %s" % (h["hozyaistvo"], h["rejon"]))
        proverka("виногорје не из своего рејона",
                 [h for h in hozyaistva
                  if h.get("vinogorje") and h.get("rejon")
                  and h["vinogorje"] not in vinogorja_rejona.get(h["rejon"], set())],
                 lambda h: "%s → %s / %s" % (h["hozyaistvo"], h["rejon"],
                                             h["vinogorje"]))
        proverka("виногорје без рејона",
                 [h for h in hozyaistva if h.get("vinogorje") and not h.get("rejon")],
                 lambda h: "%s → %s" % (h["hozyaistvo"], h["vinogorje"]))
        proverka("регион не тот, что у рејона",
                 [h for h in hozyaistva
                  if h.get("rejon") and h.get("region")
                  and region_rejona.get(h["rejon"]) != h["region"]],
                 lambda h: "%s → %s / %s" % (h["hozyaistvo"], h["rejon"], h["region"]))

    # Полнота, о которой надо знать, но это не поломка
    print()
    bez_raiona = [h for h in hozyaistva if not h["raion_knigi"]]
    bez_rejona = [h for h in hozyaistva if not h.get("rejon")]
    bez_vyborki = [o for o in ocenki if o["istochnik"] == "vivino" and not o["vyborka"]]
    print("не поломка, но знать стоит:")
    primery = ", ".join(h["hozyaistvo"] for h in bez_raiona[:8])
    print("   хозяйств без района книги: %d из %d%s"
          % (len(bez_raiona), len(hozyaistva),
             (" — например: " + primery) if primery else ""))
    print("   хозяйств с настоящим рејоном: %d из %d, с виногорјем: %d"
          % (len(hozyaistva) - len(bez_rejona), len(hozyaistva),
             sum(1 for h in hozyaistva if h.get("vinogorje"))))
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
