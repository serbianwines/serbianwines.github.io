#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собрать из index.html перечень того, чему нужны рейтинги.

Только чтение. Книгу не трогает.

    python3 _rabota/rejtingi/sobrat-celi.py index.html > _rabota/rejtingi/celi-spisok.json

Что выдаёт: по каждому из десяти регионов — хозяйства из карточек и названия
вин, встреченные в тексте главы. Названия вин берутся из <em> внутри главы;
курсив в книге держит именно их, но заодно ловит сербские слова и термины,
поэтому очевидный мусор отсеивается списком stop-слов, а остальное остаётся
на глаз человека: лучше лишнее имя в списке, чем потерянное.
"""
import html
import json
import re
import sys

# На русской Windows консоль по умолчанию не UTF-8, и первая же кириллица
# в выводе роняет скрипт с UnicodeEncodeError. Просим UTF-8 явно.
for _potok in (sys.stdout, sys.stderr, sys.stdin):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

REGIONY = [
    ("fruska",     "Фрушка гора"),
    ("subotica",   "Суботичско-Хоргошская пешчара"),
    ("banat",      "Банат"),
    ("sumadija",   "Шумадия"),
    ("morave",     "Три Моравы и Жупа"),
    ("negotin",    "Неготинска Крайина"),
    ("toplica",    "Топлица"),
    ("jugoistok",  "Юго-восток"),
    ("podunavlje", "Подунавье и Белградский район"),
    ("metohija",   "Косово и Метохия"),
]

# Курсивом в книге набраны не только вина: сербские слова, латинские цитаты,
# народные имена сортов. Всё это в список целей не идёт.
STOP = {
    "ruster ausbruch", "сушково вино", "суварак", "самоток", "грашак",
    "banatski rizling", "жупска резидба", "ружица", "мирисавка", "тамьяниоза",
    "горняк", "пивница", "прокупачко црно", "метох", "почему", "koş", "hava",
    "инверсии", "полусуварка", "црвена динка", "воловско око", "овчи репак",
    "врапчије грожђе", "першун грожђе", "шљива грожђе", "чавчица", "чађавица",
    "златава", "багрина", "креаца", "прокупац", "зачинак", "региональным",
    "кремен",
    # Курсивом в книге стоит не только вино. Эти три попадали в список
    # вин и потом искались среди рейтингов как ненайденные бутылки:
    # Gaggan — ресторан в Бангкоке, где стояла кадарка Маурера;
    # Aureus Mons — римское имя местности у Смедерева; UN1244 —
    # номер резолюции в таможенной маркировке косовского вина.
    "gaggan", "aureus mons", "un1244",
}


def bez_tegov(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


def glavy(kniga):
    """Нарезать книгу на главы регионов.

    Граница главы — не начало следующей: за последней главой сразу идут
    приложения, и по такой границе в Метохию затягивало половину книги.
    Режем по закрытию блока главы, `</details></section>`.
    """
    out = []
    for kod, imya in REGIONY:
        i = kniga.find('<section class="place" id="%s"' % kod)
        if i < 0:
            sys.exit("глава %s в книге не найдена" % kod)
        j = kniga.find("</details></section>", i)
        if j < 0:
            sys.exit("конец главы %s в книге не найден" % kod)
        out.append((kod, imya, kniga[i:j]))
    return out


def hozyaistva(glava):
    """Карточки виноделен: имя и подпись под ним."""
    out = []
    for kusok in re.findall(r'<div class="win">(.*?)</div>', glava, re.S):
        imya = re.search(r'<p class="win-n">(.*?)</p>', kusok, re.S)
        podpis = re.search(r'<p class="win-r">(.*?)</p>', kusok, re.S)
        if not imya:
            continue
        polnoe = bez_tegov(imya.group(1))
        # Знак ◈ помечает винный туризм, к имени хозяйства он не относится.
        polnoe = polnoe.replace("◈", "").strip()
        # В одной карточке бывает несколько хозяйств через среднюю точку.
        for odno in [c.strip() for c in polnoe.split("·")]:
            if odno:
                out.append({
                    "hozyaistvo": odno,
                    "podpis": bez_tegov(podpis.group(1)) if podpis else "",
                })
    return out


def vina(glava):
    out = []
    for kusok in re.findall(r"<em>(.*?)</em>", glava, re.S):
        # Курсив нередко захватывает точку в конце предложения:
        # «La Rem Chardonnay 2023.» — к имени вина она не относится.
        nazvanie = bez_tegov(kusok).rstrip(".,;:")
        if not nazvanie or nazvanie.lower() in STOP:
            continue
        if nazvanie not in out:
            out.append(nazvanie)
    return out


def prilozhenie_g(kniga):
    """Приложение «Кто на вершине»: платины, золото, шпаргалка по деньгам.

    Там названы бутылки, а не только хозяйства, и часть из них в главах
    регионов не повторяется. Для сверки с рейтингами нужны и они.
    """
    i = kniga.find('<section class="part" id="vinarije"')
    if i < 0:
        return None
    j = kniga.find('<section class="part" id="vybor"', i)
    kusok = kniga[i:j if j > i else len(kniga)]
    return {
        "kod": "vinarije",
        "imya": "Приложение Г. Кто на вершине",
        "yakor": "#vinarije",
        "hozyaistva": hozyaistva(kusok),
        "vina_v_tekste": vina(kusok),
    }


def main():
    put = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    kniga = open(put, encoding="utf-8").read()
    razdely = [
        {
            "kod": kod,
            "imya": imya,
            "yakor": "#" + kod,
            "hozyaistva": hozyaistva(glava),
            "vina_v_tekste": vina(glava),
        }
        for kod, imya, glava in glavy(kniga)
    ]
    prilozhenie = prilozhenie_g(kniga)
    if prilozhenie:
        razdely.append(prilozhenie)
    print(json.dumps({"istochnik": put, "regiony": razdely},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
