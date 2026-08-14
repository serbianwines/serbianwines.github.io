#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Переезд подсказок с радиокнопок на popover — по одному термину за раз.

Это то самое согласованное исключение из правила «править руками»:
замена механическая, видимый текст обязан остаться побайтно тем же.
После каждого запуска:

    python3 _rabota/check.py index.html --text-same-as <файл до правки>

Использование:

    python3 _rabota/pereezd-podskazki.py index.html pesak les cernozem
    python3 _rabota/pereezd-podskazki.py index.html --next 8
    python3 _rabota/pereezd-podskazki.py index.html --list

Скрипт отказывается работать, если хоть одна из связок термина выглядит
не так, как ожидалось: лучше остановиться, чем испортить книгу наполовину.
"""

import argparse
import re
import sys


def ostavshiesya(html):
    """Ключи подсказок, ещё сидящих на радиокнопках, в порядке появления."""
    return [m.group(1) for m in re.finditer(
        r'<input type="radio" name="gloss" id="gl-([a-z0-9-]+)" class="gr-in">', html)]


def perevesti(html, key):
    """Переводит один термин. Возвращает новый html или падает с объяснением."""
    gl, gp = "gl-" + key, "gp-" + key

    # 1. Радиокнопка уходит.
    radio = '<input type="radio" name="gloss" id="%s" class="gr-in">' % gl
    if html.count(radio) != 1:
        sys.exit("%s: радиокнопка не найдена или не одна" % key)
    html = html.replace(radio, "")

    # 2. Три правила CSS, которые её обслуживали.
    pravilo = "#%s:checked ~ .%s{transform:none}\n" % (gl, gp)
    if html.count(pravilo) != 1:
        sys.exit("%s: правила transform нет" % key)
    html = html.replace(pravilo, "")

    ctl = "#%s:checked ~ .ctl{opacity:0;pointer-events:none}\n" % gl
    if html.count(ctl) != 1:
        sys.exit("%s: правила ctl нет" % key)
    html = html.replace(ctl, "")

    scrim = "#%s:checked ~ .gscrim" % gl
    if html.count(scrim) != 1:
        sys.exit("%s: правила gscrim нет" % key)
    html = html.replace(scrim + ",", "", 1) if scrim + "," in html \
        else html.replace("," + scrim, "", 1)

    # 3. Панель получает id и атрибут popover. У панелей под знаком «?»
    #    к «gpanel» добавлен ещё один класс, поэтому ищем по концу списка.
    m = re.search(r'<div class="((?:gpanel|gpanel-unv| )+)%s" role="dialog"' % gp, html)
    if not m or len(re.findall(r'"[^"]*\b%s" role="dialog"' % gp, html)) != 1:
        sys.exit("%s: панель не найдена или не одна" % key)
    panel_start = m.group(0)
    html = html.replace(
        panel_start,
        '<div class="%s%s" id="%s" popover role="dialog"' % (m.group(1), gp, gp))

    # 4. Крестик внутри этой панели закрывает её же.
    nachalo = html.index('%s" id="%s"' % (gp, gp))
    sled = html.find('<div class="gpanel ', nachalo + 1)
    konec = sled if sled != -1 else len(html)
    telo = html[nachalo:konec]
    krest = '<label class="gp-x" tabindex="0" for="gl-none">✕</label>'
    if telo.count(krest) != 1:
        sys.exit("%s: крестик в панели не найден или не один" % key)
    telo = telo.replace(krest, '<button class="gp-x" type="button" '
                               'popovertarget="%s" popovertargetaction="hide">✕</button>' % gp)
    html = html[:nachalo] + telo + html[konec:]

    # 5. Термины в тексте становятся кнопками. Внутри метки только текст,
    #    поэтому замена целиком безопасна.
    vsego = 0
    for klass in ("t", "unv"):
        obrazec = re.compile(
            r'<label class="%s" tabindex="0" for="%s">([^<]*)</label>' % (klass, gl))
        html, n = obrazec.subn(
            lambda m: '<button class="%s" type="button" popovertarget="%s">%s</button>'
                      % (klass, gp, m.group(1)), html)
        vsego += n
    if vsego == 0:
        sys.exit("%s: ни одной метки — ни термина, ни знака «?»" % key)

    if 'for="%s"' % gl in html:
        sys.exit("%s: остались ссылки на радиокнопку" % key)
    return html


def main():
    ap = argparse.ArgumentParser(description="Переезд подсказок на popover")
    ap.add_argument("file")
    ap.add_argument("keys", nargs="*", help="ключи подсказок без приставки gl-")
    ap.add_argument("--next", type=int, metavar="N", help="взять первые N оставшихся")
    ap.add_argument("--list", action="store_true", help="показать, что не переехало")
    args = ap.parse_args()

    html = open(args.file, encoding="utf-8").read()
    ostalos = ostavshiesya(html)

    if args.list:
        print("не переехало: %d" % len(ostalos))
        print(" ".join(ostalos))
        return

    keys = args.keys or (ostalos[:args.next] if args.next else [])
    if not keys:
        ap.error("нечего делать: укажите ключи или --next N")

    for key in keys:
        html = perevesti(html, key)
        print("переехал: " + key)

    open(args.file, "w", encoding="utf-8").write(html)
    print("осталось: %d" % len(ostavshiesya(html)))


if __name__ == "__main__":
    main()
