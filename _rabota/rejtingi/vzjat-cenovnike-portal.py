#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полка остальных сетей: обязательные ценовники с портала открытых данных.

Что это. С 2025 года крупная сербская розница обязана публиковать цены,
и каждый торговец выкладывает их у себя. Мы брали два таких ценовника
поштучно — Maxi с `maxi.rs` и группу IDEA — Roda — Mercator с
`backend.roda.rs`, — каждый своим способом и своим разбором.

Оказалось, есть место, где лежат все: национальный портал открытых
данных `data.gov.rs`. У него открытый API,

    data.gov.rs/api/1/datasets/?q=<запрос>&page_size=50

и по запросу «Ценовници производа» он отдаёт сорок наборов данных —
по одному на торговца. У каждого набора ресурс-CSV с прямым адресом.
Формат у всех **один и тот же**, государственный:

    KATEGORIJA; NAZIV KATEGORIJE; Naziv proizvoda; Robna marka;
    Barkod proizvoda; Jedinica mere; Naziv trgovca - formata;
    Datum cenovnika; Redovna cena; Cena po jedinici mere;
    Snižena cena; Datum početka sniženja; Datum kraja sniženja;
    Stopa PDV; VRSTA_CENOVNIKA

Поэтому и разбор один на всех, а не по сети.

Что берётся. Сети, которых у нас ещё не было: Univerexport, Aman, DIS,
Gomex, Veropoulos, Cash & Carry Plus и региональные. Delhaize и IDEA
лежат на портале тоже, и одним файлом на всю сеть — у Delhaize это
Maxi, Tempo и Shop&Go вместе, чего у нас нет, — но их ценовники уже
берутся своими сборщиками, и подменять их на ходу значило бы менять
измеренные числа полки. Записано на будущее.

Две ловушки.

1. **Кодировка у сетей разная.** Univerexport и Delhaize пишут UTF-8
   с меткой, Lidl — cp1250 (у него, впрочем, свой адрес, не портальный).
   Определяется по первым байтам: если «Naziv» читается — угадали.
2. **Ценовник на формат, а не на магазин.** В колонке «Naziv trgovca -
   formata» стоит не адрес лавки, а формат сети: «UNIVEREXPORT - C3-MC3».
   Цена в разных форматах разная, поэтому берётся середина, а число
   форматов сохраняется рядом.

Пишет `portal-cenovnik-ceny.json`. Кеш — в `kesh-cenovniki-portal/`.
"""
import argparse
import collections
import csv
import io
import json
import pathlib
import re
import statistics
import time
import urllib.parse
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-cenovniki-portal"
API = "https://data.gov.rs/api/1/datasets/"
ZAPROSY = ("Ценовници производа", "cenovnici proizvoda")
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
SROK = 300

# Сети, чьи ценовники у нас уже есть своими сборщиками. С портала
# не берутся, чтобы одна и та же полка не считалась дважды.
UZHE_EST = re.compile(r"delhaize|idea marketi", re.I)
# Торговцы не с едой: на портале лежат и книжные, и ветеринарные,
# и автосалоны. Вина у них нет, а файл качать незачем.
NE_EDA = re.compile(r"books|hemij|veterinar|moto|dexy|metalac|kids|"
                    r"drogerie|conditors|lupus", re.I)

VINO = re.compile(r"\bvin[oa]\b", re.I)
NE_VINO = re.compile(r"sir[cć]e|sirce|vinjak|rakij|pivo|spricer|špricer|"
                     r"kobasic|sos\b|[cč]okolad|bombon|paste", re.I)


def vzjat(imya, adres, dvoichnoe=False):
    """Кеш на диске: файлы по двадцать мегабайт, качать дважды незачем."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya
    if fajl.exists():
        return fajl.read_bytes() if dvoichnoe else fajl.read_text(
            encoding="utf-8", errors="replace")
    for popytka in range(3):
        try:
            zapros = urllib.request.Request(
                adres, headers={"User-Agent": BRAUZER,
                                "Accept": "application/json, text/csv, */*"})
            with urllib.request.urlopen(zapros, timeout=SROK) as otvet:
                syroe = otvet.read()
            break
        except Exception:
            if popytka == 2:
                return b"" if dvoichnoe else ""
            time.sleep(2 ** (popytka + 1))
    fajl.write_bytes(syroe)
    time.sleep(0.5)
    return syroe if dvoichnoe else syroe.decode("utf-8", "replace")


def nabory():
    """Торговец → адрес его CSV. Из каталога портала, страницами."""
    najdeno = {}
    for zapros in ZAPROSY:
        for stranica in range(1, 4):
            adres = API + "?q=%s&page_size=50&page=%d" % (
                urllib.parse.quote(zapros), stranica)
            tekst = vzjat("katalog-%s-%d.json"
                          % (re.sub(r"\W+", "-", zapros)[:20], stranica), adres)
            try:
                otvet = json.loads(tekst)
            except ValueError:
                break
            for zapis in otvet.get("data") or []:
                imya = ((zapis.get("organization") or {}).get("name") or "").strip()
                if not imya:
                    continue
                for resurs in zapis.get("resources") or []:
                    if (resurs.get("format") or "").lower() != "csv":
                        continue
                    najdeno.setdefault(imya, resurs.get("url"))
            if not otvet.get("next_page"):
                break
    return najdeno


def prochitat(dvoichnoe):
    """Текст файла: кодировку сети объявляют по-разному, и не всегда верно."""
    for kodirovka in ("utf-8-sig", "cp1250", "utf-16"):
        try:
            tekst = dvoichnoe.decode(kodirovka)
        except (UnicodeDecodeError, UnicodeError):
            continue
        if "aziv proizvoda" in tekst[:2000] or "AZIV PROIZVODA" in tekst[:2000]:
            return tekst
    return dvoichnoe.decode("utf-8", "replace")


def chislo(zapis):
    zapis = (zapis or "").strip().replace(" ", "").replace(",", ".")
    try:
        return float(zapis)
    except ValueError:
        return None


def polya(stroka):
    """Имена колонок у сетей в разном регистре; сводим к одному виду."""
    return {re.sub(r"\s+", " ", (k or "").strip().lower()): v
            for k, v in stroka.items()}


def vinnye_stroki(tekst, torgovec):
    najdeno = []
    for syraya in csv.DictReader(io.StringIO(tekst), delimiter=";"):
        z = polya(syraya)
        imya = (z.get("naziv proizvoda") or "").strip()
        if not imya or not VINO.search(imya) or NE_VINO.search(imya):
            continue
        najdeno.append({
            "vino": imya,
            "hozyaistvo": (z.get("robna marka") or "").strip(),
            "shtrihkod": (z.get("barkod proizvoda") or "").strip(),
            "cena_rsd": chislo(z.get("redovna cena")),
            "cena_akcii": chislo(z.get("snižena cena") or z.get("snizena cena")),
            "litrov": chislo(z.get("jedinica mere")),
            "format": (z.get("naziv trgovca - formata") or "").strip(),
            "torgovec": torgovec,
        })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--vse", action="store_true",
                        help="брать всех торговцев портала, а не только "
                             "продуктовые сети")
    kljuchi = razbor.parse_args()

    vse = nabory()
    print("наборов на портале: %d" % len(vse))
    berjom = {imya: adres for imya, adres in vse.items()
              if adres and not UZHE_EST.search(imya)
              and (kljuchi.vse or not NE_EDA.search(imya))}
    print("берём %d" % len(berjom))

    stroki = []
    for nomer, (imya, adres) in enumerate(sorted(berjom.items()), 1):
        fajl = "cenovnik-%s.csv" % re.sub(r"\W+", "-", imya.lower())[:48]
        dvoichnoe = vzjat(fajl, adres, dvoichnoe=True)
        if not dvoichnoe:
            print("  %2d/%d %-44s не отдался" % (nomer, len(berjom), imya[:44]))
            continue
        nashli = vinnye_stroki(prochitat(dvoichnoe), imya)
        stroki += nashli
        print("  %2d/%d %-44s %6.1f МБ, винных строк %5d"
              % (nomer, len(berjom), imya[:44], len(dvoichnoe) / 1e6, len(nashli)))

    # Один товар лежит в нескольких форматах сети и стоит там по-разному.
    # Ключ — штрихкод: имя сокращают по-разному от строки к строке.
    po_kodu = collections.defaultdict(list)
    for s in stroki:
        po_kodu[s["shtrihkod"] or s["vino"]].append(s)
    vina = []
    for _, spisok in po_kodu.items():
        ceny = [s["cena_rsd"] for s in spisok if s["cena_rsd"]]
        obrazec = spisok[0]
        vina.append({
            "vino": obrazec["vino"],
            "hozyaistvo": obrazec["hozyaistvo"],
            "shtrihkod": obrazec["shtrihkod"],
            "cena_rsd": round(statistics.median(ceny), 2) if ceny else None,
            "litrov": obrazec["litrov"],
            "setej": len({s["torgovec"] for s in spisok}),
            "formatov": len({s["format"] for s in spisok}),
            "torgovcy": sorted({s["torgovec"] for s in spisok})[:6],
            "v_prodazhe": True,
        })
    vina.sort(key=lambda z: z["vino"])
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "portal-cenovnik-ceny.json").write_text(json.dumps({
        "chto_eto": "Винные строки обязательных ценовников сербских сетей "
                    "с национального портала открытых данных. Формат у всех "
                    "торговцев один, поэтому и разбор один.",
        "istochnik": "data.gov.rs, наборы «Ценовници производа»",
        "sobrano": time.strftime("%Y-%m-%d"),
        "torgovcev": len(berjom),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nстрок %d, разных товаров %d, с ценой %d → portal-cenovnik-ceny.json"
          % (len(stroki), len(vina), s_cenoj))


if __name__ == "__main__":
    main()
