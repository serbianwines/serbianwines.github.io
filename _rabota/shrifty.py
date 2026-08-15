#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Забрать гарнитуры, которые просит книга, и урезать их до её знаков.

Книга — законченный текст, набор знаков в ней известен наперёд, поэтому
шрифты можно урезать до нужного: файлы выходят в разы легче полных.
Запускать заново, только если в книге появились незнакомые знаки —
скрипт сам скажет, если такое случится.

    python3 _rabota/shrifty.py index.html

Читателю скрипт не нужен: в книгу попадают готовые файлы из каталога fonts.
"""

import hashlib
import html as H
import os
import re
import sys
import urllib.parse
import urllib.request

BRAUZER = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# что именно просит вёрстка книги
GARNITURY = [
    ("Literata",      "ital,wght@0,400;0,700;1,400", "literata"),
    ("Alegreya",      "ital,wght@0,700;0,800;1,800", "alegreya"),
    ("IBM Plex Mono", "wght@400;600",                "plexmono"),
]

# запас сверх встреченного: полная кириллица, латиница, цифры и типографика,
# чтобы новая буква в тексте не осталась без шрифта
ZAPAS = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
         "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
         "ĆćČčĐđŠšŽžĂăÂâÎîȘșȚț"
         " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
         "«»„“”‘’–—…·•№°²³×÷≈≤≥←↑→↓↔✕◈›‹§¶†‡")


def znaki_knigi(fajl):
    s = open(fajl, encoding="utf-8").read()
    telo = s[s.index("<body"):]
    telo = re.sub(r"<script.*?</script>", "", telo, flags=re.S)
    tekst = H.unescape(re.sub(r"<[^>]+>", " ", telo))
    return set(tekst) - set("\n\r\t")


def skachat(url, imja=None):
    zapros = urllib.request.Request(url, headers={"User-Agent": BRAUZER})
    with urllib.request.urlopen(zapros, timeout=60) as otvet:
        dannye = otvet.read()
    if imja:
        open(imja, "wb").write(dannye)
    return dannye


def main():
    fajl = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    znaki = znaki_knigi(fajl)
    nabor = "".join(sorted(znaki | set(ZAPAS)))
    print("знаков в книге: %d, в наборе для шрифтов: %d" % (len(znaki), len(nabor)))

    os.makedirs("fonts", exist_ok=True)
    pravila = []
    for imja, osi, kljuch in GARNITURY:
        url = ("https://fonts.googleapis.com/css2?family="
               + urllib.parse.quote(imja) + ":" + urllib.parse.quote(osi, safe="@,;.")
               + "&text=" + urllib.parse.quote(nabor)
               + "&display=swap")
        css = skachat(url).decode("utf-8")
        bloki = re.findall(r"@font-face\s*\{(.*?)\}", css, re.S)
        if not bloki:
            sys.exit("%s: сервис не отдал ни одного начертания" % imja)
        # Literata и Alegreya отдаются переменными: одним файлом покрыты оба
        # начертания, которые просит вёрстка. Отличаем их по совпадению
        # содержимого и кладём один файл вместо двух.
        vidano = {}
        for blok in bloki:
            stil = (re.search(r"font-style:\s*(\w+)", blok) or [None, "normal"])[1]
            ves = (re.search(r"font-weight:\s*(\d+)", blok) or [None, "400"])[1]
            adres = re.search(r"url\((https://[^)]+)\)", blok).group(1)
            dannye = skachat(adres)
            otpechatok = hashlib.md5(dannye).hexdigest()
            if otpechatok in vidano:
                fajl_shrifta = vidano[otpechatok]
                pravila.append((imja, stil, ves, fajl_shrifta, True))
                continue
            hvost = "-italic" if stil == "italic" else ""
            fajl_shrifta = "fonts/%s%s.woff2" % (kljuch, hvost)
            if os.path.exists(fajl_shrifta) and fajl_shrifta in vidano.values():
                fajl_shrifta = "fonts/%s-%s%s.woff2" % (kljuch, ves, hvost)
            if kljuch == "plexmono":
                fajl_shrifta = "fonts/%s-%s.woff2" % (kljuch, ves)
            open(fajl_shrifta, "wb").write(dannye)
            vidano[otpechatok] = fajl_shrifta
            print("  %-30s %6.1f КБ" % (fajl_shrifta, len(dannye) / 1024))
            pravila.append((imja, stil, ves, fajl_shrifta, False))

    print("\nЧто получилось (правила в книге собраны из этого вручную,"
          "\nу переменных гарнитур вес задан промежутком):\n")
    for imja, stil, ves, f, povtor in pravila:
        print("  %-14s %-8s %-4s %s%s" % (imja, stil, ves, f,
              "  (тот же файл)" if povtor else ""))


if __name__ == "__main__":
    main()
