#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Приложение и его подглавы — на <details>. По одному разделу за раз.

Структурная правка, поэтому скрипт ничего не угадывает: он проверяет, что
раздел устроен ожидаемо, и отказывается работать иначе. Видимый текст при
этом меняться не должен — сверять браузером, innerText до и после.

    python3 _rabota/pereezd-prilozhenija.py index.html sorta
    python3 _rabota/pereezd-prilozhenija.py index.html --list
"""

import argparse
import re
import sys

PUSTYE = {"area","base","br","col","embed","hr","img","input",
          "link","meta","param","source","track","wbr"}


def granicy(html):
    """Начала разделов приложений в порядке следования."""
    i = html.index('id="prilozhenija"')
    return [(m.start(), re.search(r'id="([^"]+)"', m.group(0)).group(1))
            for m in re.finditer(r'<section class="part" id="[^"]+">', html[i:])
            for m in [m]] , i


def kusok(html, ide):
    """Начало и конец раздела: до следующего раздела или до конца приложений."""
    nach = html.index('<section class="part" id="%s">' % ide)
    sled = re.search(r'<section class="part" id="[^"]+">', html[nach + 10:])
    kon = nach + 10 + sled.start() if sled else html.index('</div>\n</body>') if '</div>\n</body>' in html else len(html)
    if not sled:
        # последний раздел: ищем закрытие тома приложений
        kon = html.index('</section>', html.rindex('<section class="part" id="%s">' % ide)) + len('</section>')
    return nach, kon


def glubina(fragment):
    """Баланс тегов: 0 — значит фрагмент самодостаточен."""
    g = 0
    for m in re.finditer(r'<(/?)([a-z0-9]+)([^>]*)>', fragment, re.I):
        zakr, teg, atr = m.group(1), m.group(2).lower(), m.group(3)
        if teg in PUSTYE or atr.endswith("/"):
            continue
        g += -1 if zakr else 1
    return g


def perevesti(html, ide):
    nach, kon = kusok(html, ide)
    kus = html[nach:kon]
    hvost = kus[kus.rindex('</section>'):]
    assert hvost.strip() == '</section>', "раздел %s кончается не так: %r" % (ide, hvost[:40])
    kus = kus[:kus.rindex('</section>')]

    if 'class="part-det"' in kus:
        sys.exit("%s: уже переехал" % ide)

    # заголовок
    m = re.match(r'(<section class="part" id="%s">)\s*<p class="part-num">(.*?)</p>\s*'
                 r'(<h2 class="part-h">.*?</h2>)' % ide, kus, re.S)
    if not m:
        sys.exit("%s: заголовок устроен не так, как ожидалось" % ide)
    golova = (m.group(1) + '<details class="part-det"><summary class="part-head">'
              + '<span class="part-num">' + m.group(2) + '</span>'
              + m.group(3) + '</summary><div class="part-body">')
    telo = kus[m.end():]

    # подглавы: каждая от своего h3 до следующего или до конца раздела
    zagolovki = [(mm.start(), mm.end()) for mm in
                 re.finditer(r'<h3 class="sub-h"[^>]*>.*?</h3>', telo, re.S)]
    if zagolovki:
        части, prev = [], 0
        for i, (a, b) in enumerate(zagolovki):
            konec = zagolovki[i + 1][0] if i + 1 < len(zagolovki) else len(telo)
            vnutr = telo[b:konec]
            if glubina(vnutr) != 0:
                sys.exit("%s: подглава со смещением %d не самодостаточна — заворачивать нельзя" % (ide, a))
            части.append(telo[prev:a])
            части.append('<details class="sub-det"><summary class="sub-head">'
                         + telo[a:b] + '</summary><div class="sub-body">'
                         + vnutr + '</div></details>')
            prev = konec
        части.append(telo[prev:])
        telo = "".join(части)

    novoe = golova + telo + '</div></details></section>'
    if glubina(novoe) != 0:
        sys.exit("%s: после сборки теги не сходятся" % ide)
    return html[:nach] + novoe + html[kon:]


def main():
    ap = argparse.ArgumentParser(description="Приложения на <details>")
    ap.add_argument("file")
    ap.add_argument("razdel", nargs="?")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    html = open(args.file, encoding="utf-8").read()

    if args.list or not args.razdel:
        i = html.index('id="prilozhenija"')
        for m in re.finditer(r'<section class="part" id="([^"]+)">', html[i:]):
            ide = m.group(1)
            nach, kon = kusok(html, ide)
            pod = len(re.findall(r'<h3 class="sub-h"', html[nach:kon]))
            print("%-12s %s | подглав: %d" % (
                ide, "переехал" if 'class="part-det"' in html[nach:kon] else "на месте", pod))
        return

    html = perevesti(html, args.razdel)
    open(args.file, "w", encoding="utf-8").write(html)
    print("переехал:", args.razdel)


if __name__ == "__main__":
    main()
