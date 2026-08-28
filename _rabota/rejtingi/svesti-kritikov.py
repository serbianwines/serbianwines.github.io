#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Свести оценки критиков по районам книги.

Читает `kritiki-zapisi.jsonl` и `raion-hozyaistv.json`, раскладывает по
десяти главам и печатает по убыванию балла.

    python3 _rabota/rejtingi/svesti-kritikov.py
    python3 _rabota/rejtingi/svesti-kritikov.py --markdown

Порога по числу отзывов здесь нет и быть не может: это оценка эксперта,
а не толпы. Одна дегустация Falstaff весит столько же, сколько тысяча
отметок в телефоне, — и это другая величина, а не та же в другой шкале.
Поэтому две дорожки, Vivino и критики, не складываются в одно число.
"""

import argparse
import json
import os

RYADOM = os.path.dirname(os.path.abspath(__file__))

IMENA = [
    ("fruska", "Фрушка гора"),
    ("subotica", "Суботичско-Хоргошская пешчара"),
    ("banat", "Банат"),
    ("sumadija", "Шумадия"),
    ("morave", "Три Моравы и Жупа"),
    ("negotin", "Неготинска Крайина"),
    ("toplica", "Топлица"),
    ("jugoistok", "Юго-восток"),
    ("podunavlje", "Подунавье и Белградский район"),
    ("metohija", "Косово и Метохия"),
]

IMYA_ISTOCHNIKA = {
    "falstaff": "Falstaff",
    "wine-searcher": "Wine-Searcher",
    "vino.rs": "vino.rs",
    "tastings": "Tastings.com",
}


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--markdown", action="store_true")
    dovody = razbor.parse_args()

    zapisi = [json.loads(s) for s in
              open(os.path.join(RYADOM, "kritiki-zapisi.jsonl"), encoding="utf-8")
              if s.strip()]
    karta = json.load(open(os.path.join(RYADOM, "raion-hozyaistv.json"),
                           encoding="utf-8"))["hozyaistva"]

    po_raionam = {kod: [] for kod, _ in IMENA}
    bez_raiona = []
    for z in zapisi:
        svedeniya = karta.get(z["hozyaistvo"])
        raion = svedeniya["raion"] if svedeniya else None
        (po_raionam[raion] if raion else bez_raiona).append(z)

    if dovody.markdown:
        print("<!-- Собрано скриптом svesti-kritikov.py. Руками не править. -->\n")
    for kod, imya in IMENA:
        spisok = sorted(po_raionam[kod], key=lambda z: -(z["ball"] or 0))
        if dovody.markdown:
            print("## %s\n" % imya)
            if not spisok:
                print("Оценок критиков не найдено.\n")
                continue
            print("| Вино | Урожай | Балл | Источник |")
            print("|---|---|---|---|")
            for z in spisok:
                print("| %s · %s | %s | %s | %s |"
                      % (z["hozyaistvo"], z["vino"], z["god"] or "—", z["ball"],
                         IMYA_ISTOCHNIKA.get(z["istochnik"], z["istochnik"])))
            print()
        else:
            print("%s — %d" % (imya, len(spisok)))
            for z in spisok:
                print("   %3s  %s · %s %s [%s]"
                      % (z["ball"], z["hozyaistvo"], z["vino"], z["god"] or "",
                         z["istochnik"]))
    if bez_raiona:
        zagolovok = "## Хозяйства без района\n" if dovody.markdown else "без района:"
        print(zagolovok)
        for z in sorted(bez_raiona, key=lambda z: -(z["ball"] or 0)):
            print(("- " if dovody.markdown else "   ")
                  + "%s · %s %s — %s [%s]"
                  % (z["hozyaistvo"], z["vino"], z["god"] or "", z["ball"],
                     IMYA_ISTOCHNIKA.get(z["istochnik"], z["istochnik"])))


if __name__ == "__main__":
    main()
