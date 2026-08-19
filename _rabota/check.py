#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обязательные проверки книги «Терруары Сербии».

Скрипт только читает. Он ничего не правит и не должен научиться править:
правки вносятся руками, скрипт лишь говорит, что сломалось.

Использование:

    python3 check.py index.html
    python3 check.py index.html --text-same-as эталон.html

Второй режим сверяет видимый текст двух файлов побайтно. Он нужен, когда
разметка меняется механически (например, метки становятся кнопками):
если хоть один знак текста разошёлся, трансформация отклоняется целиком.

Код возврата 0 — всё чисто, 1 — есть замечания.
"""

import argparse
import os
import re
import sys
from html.parser import HTMLParser

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


# --------------------------------------------------------------------------
# разбор
# --------------------------------------------------------------------------

class Doc(HTMLParser):
    """Собирает дерево тегов и видимый текст."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []            # открытые теги: (имя, классы, строка)
        self.unclosed = []         # теги, оставшиеся открытыми к концу файла
        self.nested_places = []    # главы внутри глав
        self.text = []             # видимый текст
        self._skip = 0             # внутри <script>/<style> текст не считаем
        self._in_body = False      # текст head — это метаданные, не книга

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self._in_body = True
        if tag in ("script", "style"):
            self._skip += 1
        if tag in VOID:
            return
        cls = dict(attrs).get("class", "")
        classes = set(cls.split())
        if tag == "section" and "place" in classes:
            outer = [f for f in self.stack if f[0] == "section" and "place" in f[1]]
            if outer:
                self.nested_places.append((self.getpos()[0], outer[-1][2]))
        self.stack.append((tag, classes, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return
        # закрывающий тег без открывающего — тоже дефект структуры
        self.unclosed.append(("</%s> без пары" % tag, self.getpos()[0]))

    def handle_data(self, data):
        if not self._skip and self._in_body:
            self.text.append(data)

    def close(self):
        super().close()
        for tag, _, line in self.stack:
            if tag not in ("html", "body", "head"):
                self.unclosed.append(("<%s> не закрыт" % tag, line))


def parse(html):
    d = Doc()
    d.feed(html)
    d.close()
    return d


def visible_text(html):
    return "".join(parse(html).text)


# --------------------------------------------------------------------------
# проверки
# --------------------------------------------------------------------------

def check_ids(html):
    ids = re.findall(r'\bid="([^"]+)"', html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    return ["дубль id: " + i for i in dupes]


def check_labels(html):
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    bad = sorted({f for f in re.findall(r'\bfor="([^"]+)"', html) if f not in ids})
    return ['label for="%s" — такого id нет' % f for f in bad]


def check_anchors(html):
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    bad = sorted({
        a for a in re.findall(r'href="#([^"]*)"', html)
        if a and a not in ids
    })
    return ['ссылка href="#%s" — такого id нет' % a for a in bad]


def check_tooltips(html):
    """Полнота проводки подсказок.

    Пока подсказки держатся на радиокнопках, у каждой должно быть пять
    связок: input, панель, transform, gscrim, ctl. После переезда на
    popover проверяется другое: у каждой кнопки есть панель с атрибутом
    popover, и у каждой панели есть хотя бы одна кнопка.
    """
    out = []

    radios = sorted({
        i for i in re.findall(r'\bid="(gl-[a-z0-9-]+)"', html) if i != "gl-none"
    })
    for gid in radios:
        key = gid[3:]
        missing = []
        if 'id="%s"' % gid not in html:
            missing.append("input")
        if "gp-%s" % key not in html:
            missing.append("панель")
        if "#%s:checked ~ .gp-%s{transform:none" % (gid, key) not in html:
            missing.append("transform")
        if "#%s:checked ~ .gscrim" % gid not in html:
            missing.append("gscrim")
        if "#%s:checked ~ .ctl" % gid not in html:
            missing.append("ctl")
        if missing:
            out.append("подсказка %s — нет: %s" % (gid, ", ".join(missing)))

    targets = sorted(set(re.findall(r'popovertarget="([^"]+)"', html)))
    if targets:
        panels = set(re.findall(r'\bid="([^"]+)"[^>]*\bpopover\b', html))
        panels |= set(re.findall(r'\bpopover\b[^>]*\bid="([^"]+)"', html))
        for t in targets:
            if t not in panels:
                out.append('popovertarget="%s" — панели с таким id и атрибутом popover нет' % t)
        for p in sorted(panels):
            if p not in targets:
                out.append("панель %s — на неё ничто не ссылается" % p)

    return out


def check_fonts(html, doc):
    """Знаки книги против того, на что урезаны шрифты.

    Шрифты лежат рядом с книгой урезанными до её знаков. Стоит появиться в
    тексте букве, которой в них нет, — она нарисуется чужой гарнитурой
    посреди слова, и заметить это глазом трудно. Набор, на котором собраны
    шрифты, записан в fonts/nabor.txt скриптом shrifty.py.
    """
    put = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "nabor.txt")
    if not os.path.exists(put):
        return []
    nabor = set(open(put, encoding="utf-8").read())
    # знаки, которых в шрифтах нет вовсе: их и не просили
    net_v_garniturah = set("◈✕↔")
    chuzhie = sorted(set("".join(doc.text)) - nabor - net_v_garniturah - set(" \n\r\t"))
    if not chuzhie:
        return []
    return ["в книге есть знак, которого нет в шрифтах: %s (перезапустите "
            "_rabota/shrifty.py)" % " ".join(repr(z) for z in chuzhie)]


def check_structure(doc):
    out = ["структура: %s, строка %d" % (what, line) for what, line in doc.unclosed]
    out += [
        "глава внутри главы: строка %d вложена в главу со строки %d" % (inner, outer)
        for inner, outer in doc.nested_places
    ]
    return out


def check_torn_words(html):
    """Слово, разорванное пополам открывающим тегом.

    Знак «?» — законное исключение: он вплотную примыкает к слову,
    к которому относится, и разрывом не является.
    """
    out = []
    for m in re.finditer(r'[а-яё](<(?:label|button)\b[^>]*>)', html, re.I):
        if 'class="unv"' in m.group(1):
            continue
        line = html.count("\n", 0, m.start()) + 1
        out.append("разорванное слово, строка %d: …%s" % (line, html[m.start() - 25:m.start() + 60]))
    return out


# --------------------------------------------------------------------------
# запуск
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Проверки книги «Терруары Сербии»")
    ap.add_argument("file", help="проверяемый файл")
    ap.add_argument("--text-same-as", metavar="ЭТАЛОН",
                    help="сверить видимый текст с эталонным файлом побайтно")
    args = ap.parse_args()

    html = open(args.file, encoding="utf-8").read()
    doc = parse(html)

    blocks = [
        ("дубли id", check_ids(html)),
        ("битые label for", check_labels(html)),
        ("битые внутренние ссылки", check_anchors(html)),
        ("проводка подсказок", check_tooltips(html)),
        ("знаки и шрифты", check_fonts(html, doc)),
        ("структура и изоляция глав", check_structure(doc)),
        ("разорванные слова", check_torn_words(html)),
    ]

    if args.text_same_as:
        etalon = open(args.text_same_as, encoding="utf-8").read()
        a, b = visible_text(etalon), visible_text(html)
        if a == b:
            blocks.append(("сверка текста с эталоном", []))
        else:
            n = min(len(a), len(b))
            i = next((k for k in range(n) if a[k] != b[k]), n)
            blocks.append(("сверка текста с эталоном", [
                "текст разошёлся на знаке %d (было %d знаков, стало %d)" % (i, len(a), len(b)),
                "  эталон: …%s…" % a[max(0, i - 40):i + 40].replace("\n", "⏎"),
                "  стало:  …%s…" % b[max(0, i - 40):i + 40].replace("\n", "⏎"),
            ]))

    total = 0
    for name, problems in blocks:
        if problems:
            total += len(problems)
            print("✗ %s — %d" % (name, len(problems)))
            for p in problems[:20]:
                print("    " + p)
            if len(problems) > 20:
                print("    …и ещё %d" % (len(problems) - 20))
        else:
            print("✓ %s" % name)

    print()
    if total:
        print("Замечаний: %d. Не коммитить, пока не разобрано." % total)
    else:
        print("Чисто. Механические проверки пройдены — они не заменяют чтения.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
