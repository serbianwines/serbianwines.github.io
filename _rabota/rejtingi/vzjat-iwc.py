# -*- coding: utf-8 -*-
"""International Wine Challenge: сербские медали.

IWC — лондонский конкурс, судят вслепую, результаты открыты и отдаются
обычными запросами. Сербия у него есть с 2009 по 2022 год; в 2011 и 2023–2026
сербских вин не заявлено.

Балла IWC не ставит — только медали (Trophy, Gold, Silver, Bronze,
Commended) и дегустационную заметку. Поэтому записи идут в дорожку наград,
а не оценок: у медали нет шкалы, складывать её с баллами нельзя.

    python3 _rabota/rejtingi/vzjat-iwc.py

Пишет `iwc-zapisi.json`. Страницы кладёт в `kesh-iwc/`.
"""
import json, os, re, html, sys, time, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-iwc")
SPISOK = ("https://www.internationalwinechallenge.com/canopy/search_results"
          "?wpcat=WineTab.S&Challenge_Year=%s_993276&Country=170&page=%d")
STRANA_SRBIJA = "170"          # номер Сербии в справочнике IWC
# Годы перечислялись поимённо, и 2011-й в списке пропущен — а у него
# три сербские медали. Поэтому здесь сплошной ряд: пустой год отвечает
# «Displaying 0 results», и это видно, а не молчит. Сербских вин у IWC
# нет до 2009 года и после 2022-го — проверено запросом.
GODY = range(2008, 2027)
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Карточка результата. Одним выражением её не взять: медаль лежит
# в отдельном <li> после сорта, и необязательные группы в длинном
# шаблоне молча остаются пустыми — так вышло в первом заходе, где
# у всех 63 записей медаль оказалась None. Поэтому страница режется
# на карточки, и каждая разбирается по частям.
NACHALO = re.compile(r'<a class="result" href="beverage_details\?wid=(\d+)"')
MEDAL = re.compile(r'images/medals/IWC/\d+/([A-Za-z_]+?)_thumb\.png')


def kuski(stranica):
    """Страница → куски по карточке на каждый."""
    mesta = [(m.start(), m.group(1)) for m in NACHALO.finditer(stranica)]
    for i, (nachalo, nomer) in enumerate(mesta):
        konec = mesta[i + 1][0] if i + 1 < len(mesta) else len(stranica)
        yield nomer, stranica[nachalo:konec]


def vzjat(adres, imya):
    fajl = os.path.join(KESH, imya)
    if os.path.exists(fajl):
        return open(fajl, encoding="utf-8").read()
    zapros = urllib.request.Request(adres, headers={
        "User-Agent": BRAUZER, "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(zapros, timeout=60) as otvet:
        tekst = otvet.read().decode("utf-8", "replace")
    os.makedirs(KESH, exist_ok=True)
    open(fajl, "w", encoding="utf-8").write(tekst)
    time.sleep(1.2)
    return tekst


def chisto(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def razobrat(stranica, god):
    zapisi = []
    for nomer, kusok in kuski(stranica):
        zagolovok = re.search(r"<h2>(.*?)</h2>", kusok, re.S)
        hozyaistvo = re.search(r"<p>Produced by (.*?)</p>", kusok, re.S)
        mesto = re.search(r"<p>From (.*?)</p>", kusok, re.S)
        sort = re.search(r"<p>Made with (.*?)</p>", kusok, re.S)
        medal = MEDAL.search(kusok)
        imya = chisto(zagolovok.group(1)) if zagolovok else ""
        urozhaj = None
        sovpalo = re.search(r",\s*(\d{4})\s*$", imya)
        if sovpalo:
            urozhaj = int(sovpalo.group(1))
            imya = imya[:sovpalo.start()].strip()
        gde = chisto(mesto.group(1)) if mesto else ""
        zapisi.append({
            "god": god,
            "nomer": nomer,
            "hozyaistvo": chisto(hozyaistvo.group(1)) if hozyaistvo else "",
            "vino": imya,
            "urozhaj": urozhaj,
            "medal": medal.group(1).replace("_", " ") if medal else None,
            "sort": chisto(sort.group(1)) if sort else "",
            "oblast_iwc": gde.rsplit(",", 1)[0].strip() if "," in gde else "",
            "stranica": "internationalwinechallenge.com, IWC %d, вино %s"
                        % (god, nomer),
        })
    return zapisi


def main():
    vse, po_godam = [], {}
    for god in GODY:
        stranica_nomer, za_god = 1, []
        while True:
            tekst = vzjat(SPISOK % (god, stranica_nomer),
                          "iwc-%d-%02d.html" % (god, stranica_nomer))
            najdeno = razobrat(tekst, god)
            za_god += najdeno
            skolko = re.search(r"Displaying\s+(\d+)\s+results", tekst)
            vsego = int(skolko.group(1)) if skolko else len(za_god)
            if len(za_god) >= vsego or not najdeno:
                break
            stranica_nomer += 1
        po_godam[god] = (len(za_god), vsego)
        print("  IWC %d: разобрано %d из %d" % (god, len(za_god), vsego))
        vse += za_god

    bez_medali = [z for z in vse if not z["medal"]]
    json.dump({
        "chto_eto": "Сербские вина, отмеченные на International Wine Challenge. "
                    "IWC ставит медали, а не баллы — это награды, не оценки.",
        "istochnik": "internationalwinechallenge.com/canopy/search_results",
        "strana_v_spravochnike": STRANA_SRBIJA,
        "gody": sorted(GODY),
        "vsego": len(vse),
        "bez_medali": len(bez_medali),
        "zapisi": vse,
    }, open(put("iwc-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего записей: %d, без медали: %d → iwc-zapisi.json"
          % (len(vse), len(bez_medali)))


if __name__ == "__main__":
    main()
