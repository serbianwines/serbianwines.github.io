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
import io
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


def pokazat_nagrady(spisok, markdown):
    """Награды печатаются отдельным блоком: у них нет шкалы, и в одну
    таблицу с баллами их ставить нельзя."""
    if not spisok:
        if markdown:
            print("_Наград не найдено._\n")
        return
    spisok = sorted(spisok, key=lambda n: (-(n["god"] or 0), n["kategoriya"]))
    if markdown:
        print("**Награды**\n")
        print("| Год | Категория | Место | Кому |")
        print("|---|---|---|---|")
        for n in spisok:
            komu = n["hozyaistvo"] + (" · " + n["vino"] if n["vino"] else "")
            if n["urozhaj"]:
                komu += " %d" % n["urozhaj"]
            print("| %s | %s | %s | %s | " % (n["god"], n["kategoriya"],
                                              n["mesto"], komu))
        print()
    else:
        for n in spisok:
            komu = n["hozyaistvo"] + (" · " + n["vino"] if n["vino"] else "")
            print("   %s %s — %s [%s]"
                  % (n["god"], n["kategoriya"], komu, n["istochnik"]))


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--markdown", action="store_true")
    razbor.add_argument("--otchet", action="store_true",
                        help="собрать kritiki-po-regionam.md целиком: вступление плюс таблицы")
    dovody = razbor.parse_args()
    if dovody.otchet:
        dovody.markdown = True

    def tablica(imya):
        return [json.loads(s) for s in
                open(os.path.join(RYADOM, imya), encoding="utf-8") if s.strip()]

    # Из таблиц, а не из сырья: там канонические имена хозяйств и район.
    zapisi = [dict(o, ball=o["ball"], god=o["god"])
              for o in tablica("ocenki.jsonl") if o["istochnik"] != "vivino"]
    nagrady = tablica("nagrady.jsonl")
    karta = {h["hozyaistvo"]: {"raion": h["raion_knigi"],
                               "istochnik": h["raion_istochnik"]}
             for h in tablica("hozyaistva.jsonl")}

    po_raionam = {kod: [] for kod, _ in IMENA}
    nagrady_raionov = {kod: [] for kod, _ in IMENA}
    bez_raiona, nagrady_bez_raiona = [], []
    for z in zapisi:
        svedeniya = karta.get(z["hozyaistvo"])
        raion = svedeniya["raion"] if svedeniya else None
        (po_raionam[raion] if raion else bez_raiona).append(z)
    for n in nagrady:
        svedeniya = karta.get(n["hozyaistvo"])
        raion = svedeniya["raion"] if svedeniya else None
        (nagrady_raionov[raion] if raion else nagrady_bez_raiona).append(n)

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
            pokazat_nagrady(nagrady_raionov[kod], True)
        else:
            print("%s — оценок %d, наград %d"
                  % (imya, len(spisok), len(nagrady_raionov[kod])))
            for z in spisok:
                print("   %3s  %s · %s %s [%s]"
                      % (z["ball"], z["hozyaistvo"], z["vino"], z["god"] or "",
                         z["istochnik"]))
            pokazat_nagrady(nagrady_raionov[kod], False)
    if bez_raiona:
        zagolovok = "## Хозяйства без района\n" if dovody.markdown else "без района:"
        print(zagolovok)
        for z in sorted(bez_raiona, key=lambda z: -(z["ball"] or 0)):
            print(("- " if dovody.markdown else "   ")
                  + "%s · %s %s — %s [%s]"
                  % (z["hozyaistvo"], z["vino"], z["god"] or "", z["ball"],
                     IMYA_ISTOCHNIKA.get(z["istochnik"], z["istochnik"])))


def sobrat_otchet():
    """Записать готовый отчёт: вступление плюс таблицы.

    Склейкой в оболочке этого лучше не делать: в PowerShell перенаправление
    пишет не в UTF-8, и файл выходит в кракозябрах. Проще собрать самим.
    """
    vstuplenie = open(os.path.join(RYADOM, "kritiki-vstuplenie.md"), encoding="utf-8").read()
    bufer = io.StringIO()
    nastojashchij, sys.stdout = sys.stdout, bufer
    try:
        main()
    finally:
        sys.stdout = nastojashchij
    with open(os.path.join(RYADOM, "kritiki-po-regionam.md"), "w", encoding="utf-8") as f:
        f.write(vstuplenie + bufer.getvalue())
    print("собран kritiki-po-regionam.md")


if __name__ == "__main__":
    if "--otchet" in sys.argv:
        sobrat_otchet()
    else:
        main()
