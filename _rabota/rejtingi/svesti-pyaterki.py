#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Свести собранное вручную в пятёрки по районам книги.

Читает `vivino-zapisi.jsonl` (что удалось выписать из выдачи) и
`raion-hozyaistv.json` (какое хозяйство к какому району книги относится),
применяет то же правило отбора, что и `sobrat-rejtingi.py`, и печатает
результат. Ничего не скачивает.

    python3 _rabota/rejtingi/svesti-pyaterki.py
    python3 _rabota/rejtingi/svesti-pyaterki.py --markdown > po-regionam.md

Вина без известного числа отзывов в пятёрки не идут — в этом весь смысл
правила. Они перечисляются отдельно, как очередь на уточнение.
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

# Правило отбора живёт в одном месте — в sobrat-rejtingi.py. Имя файла с
# дефисом обычным import не берётся, поэтому константы вычитываются из текста.
_ishodnik = open(os.path.join(RYADOM, "sobrat-rejtingi.py"), encoding="utf-8").read()
_prostranstvo = {}
for _stroka in _ishodnik.splitlines():
    if _stroka.startswith(("MIN_OCENOK", "VES_NEDOVERIYA", "MAX_OT_HOZYAISTVA", "V_SPISKE")):
        exec(_stroka.split("#")[0], {}, _prostranstvo)          # noqa: S102
MIN_OCENOK = _prostranstvo["MIN_OCENOK"]
VES_NEDOVERIYA = _prostranstvo["VES_NEDOVERIYA"]
MAX_OT_HOZYAISTVA = _prostranstvo["MAX_OT_HOZYAISTVA"]
V_SPISKE = _prostranstvo["V_SPISKE"]

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


def chitat():
    """Читаем сведённые таблицы, а не сырьё.

    Раньше здесь лежал разбор ручных выписок. После сплошного сбора это
    неверно: район и канонические имена хозяйств живут в `hozyaistva`,
    а оценки — в `ocenki`. Сырьё остаётся входом для `sobrat-tablicy.py`,
    а отчёты строятся по таблицам.
    """
    def tablica(imya):
        return [json.loads(s) for s in
                open(os.path.join(RYADOM, imya), encoding="utf-8") if s.strip()]

    zapisi = [{"hozyaistvo": o["hozyaistvo"], "vino": o["vino"],
               "ocenka": o["ball"], "chislo_ocenok": o["vyborka"]}
              for o in tablica("ocenki.jsonl") if o["istochnik"] == "vivino"]
    karta = {h["hozyaistvo"]: {"raion": h["raion_knigi"],
                               "istochnik": h["raion_istochnik"]}
             for h in tablica("hozyaistva.jsonl")}
    return zapisi, karta


def sdvinutaya(ocenka, chislo, srednee):
    return (chislo * ocenka + VES_NEDOVERIYA * srednee) / (chislo + VES_NEDOVERIYA)


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--markdown", action="store_true")
    razbor.add_argument("--otchet", action="store_true",
                        help="собрать po-regionam.md целиком: вступление плюс таблицы")
    dovody = razbor.parse_args()
    if dovody.otchet:
        dovody.markdown = True

    zapisi, karta = chitat()

    # Средняя считается по тем, кто сам прошёл порог: иначе её тянут вниз
    # бутылки с парой отзывов, и поправка перестаёт означать «как обычно».
    opora = [z for z in zapisi
             if z.get("ocenka") and (z.get("chislo_ocenok") or 0) >= MIN_OCENOK]
    srednee = sum(z["ocenka"] for z in opora) / len(opora)

    po_raionam = {kod: [] for kod, _ in IMENA}
    bez_raiona, bez_chisla = [], []
    for z in zapisi:
        svedeniya = karta.get(z["hozyaistvo"])
        raion = svedeniya["raion"] if svedeniya else None
        if z.get("ocenka") is None:
            continue
        if not z.get("chislo_ocenok"):
            bez_chisla.append((raion, z))
            continue
        if raion is None:
            bez_raiona.append(z)
        else:
            po_raionam[raion].append(z)

    vyvod = []
    for kod, imya in IMENA:
        godnye = [z for z in po_raionam[kod] if z["chislo_ocenok"] >= MIN_OCENOK]
        for z in godnye:
            z["itogovaya"] = round(sdvinutaya(z["ocenka"], z["chislo_ocenok"], srednee), 3)
        godnye.sort(key=lambda z: z["itogovaya"], reverse=True)
        pyat, skolko = [], {}
        for z in godnye:
            if skolko.get(z["hozyaistvo"], 0) >= MAX_OT_HOZYAISTVA:
                continue
            skolko[z["hozyaistvo"]] = skolko.get(z["hozyaistvo"], 0) + 1
            pyat.append(z)
            if len(pyat) == V_SPISKE:
                break
        ochered = sorted([z for r, z in bez_chisla if r == kod],
                         key=lambda z: -z["ocenka"])
        vyvod.append((kod, imya, pyat, len(godnye), len(po_raionam[kod]), ochered))

    if dovody.markdown:
        print("<!-- Собрано скриптом svesti-pyaterki.py. Руками не править: -->")
        print("<!-- правьте vivino-zapisi.jsonl и перегенерируйте.          -->")
        print()
        print("Порог %d отзывов · вес недоверия %d · потолок %d вина на хозяйство."
              % (MIN_OCENOK, VES_NEDOVERIYA, MAX_OT_HOZYAISTVA))
        print("Средняя, к которой идёт сдвиг, — **%.2f** по %d винам, прошедшим порог.\n"
              % (srednee, len(opora)))
        for kod, imya, pyat, godnyh, vsego, ochered in vyvod:
            print("## %s\n" % imya)
            if pyat:
                print("| # | Вино | Vivino | Отзывов | После сдвига |")
                print("|---|---|---|---|---|")
                for n, z in enumerate(pyat, 1):
                    print("| %d | %s · %s | %.1f | %d | %.2f |"
                          % (n, z["hozyaistvo"], z["vino"],
                             z["ocenka"], z["chislo_ocenok"], z["itogovaya"]))
            else:
                print("Пятёрка не собирается: ни одного вина с известным числом отзывов.")
            print()
            if len(pyat) < V_SPISKE and pyat:
                print("В списке %d вина из пяти: у остальных района число отзывов"
                      " не установлено.\n" % len(pyat))
            if ochered:
                print("Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:\n")
                print(", ".join("%s · %s %.1f" % (z["hozyaistvo"], z["vino"], z["ocenka"])
                                for z in ochered[:14])
                      + ("." if len(ochered) <= 14 else " — и ещё %d." % (len(ochered) - 14)))
                print()
        if bez_raiona:
            print("## Хозяйства без района\n")
            print("Вина есть, к какой главе книги отнести — не установлено:\n")
            for z in sorted(bez_raiona, key=lambda z: -z["ocenka"]):
                print("- %s · %s — %.1f (%d)"
                      % (z["hozyaistvo"], z["vino"], z["ocenka"], z["chislo_ocenok"]))
            print()
        return vyvod, srednee, bez_raiona, bez_chisla

    if not dovody.markdown:
        print("средняя по прошедшим порог: %.3f (вин в опоре: %d)" % (srednee, len(opora)))
        print("порог %d отзывов, вес недоверия %d, потолок на хозяйство %d\n"
              % (MIN_OCENOK, VES_NEDOVERIYA, MAX_OT_HOZYAISTVA))
        for kod, imya, pyat, godnyh, vsego, ochered in vyvod:
            print("%s — с числом отзывов %d, прошло порог %d, ждут уточнения %d"
                  % (imya, vsego, godnyh, len(ochered)))
            for n, z in enumerate(pyat, 1):
                print("   %d. %-46s %.1f (%d) → %.3f"
                      % (n, (z["hozyaistvo"] + " · " + z["vino"])[:46],
                         z["ocenka"], z["chislo_ocenok"], z["itogovaya"]))
            if not pyat:
                print("   пятёрка не собирается")
            print()
        print("вина хозяйств без района: %d" % len(bez_raiona))
        print("вина без числа отзывов вообще: %d" % len(bez_chisla))
    return vyvod, srednee, bez_raiona, bez_chisla


def sobrat_otchet():
    """Записать готовый отчёт: вступление плюс таблицы.

    Склейкой в оболочке этого лучше не делать: в PowerShell перенаправление
    пишет не в UTF-8, и файл выходит в кракозябрах. Проще собрать самим.
    """
    vstuplenie = open(os.path.join(RYADOM, "po-regionam-vstuplenie.md"), encoding="utf-8").read()
    bufer = io.StringIO()
    nastojashchij, sys.stdout = sys.stdout, bufer
    try:
        main()
    finally:
        sys.stdout = nastojashchij
    with open(os.path.join(RYADOM, "po-regionam.md"), "w", encoding="utf-8") as f:
        f.write(vstuplenie + bufer.getvalue())
    print("собран po-regionam.md")


if __name__ == "__main__":
    if "--otchet" in sys.argv:
        sobrat_otchet()
    else:
        main()
