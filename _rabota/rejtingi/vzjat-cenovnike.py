# -*- coding: utf-8 -*-
"""Полка супермаркета из обязательных ценовников Delhaize (Maxi).

С 2025 года крупная сербская розница обязана публиковать цены каждого
магазина отдельным файлом на каждый день. Maxi выкладывает их на
`maxi.rs/cenovnici`: по одному CSV на магазин, пятьсот пятьдесят два
магазина, полный ассортимент с ценой, штрихкодом и ценой по акции.

Это лучше, чем винный раздел их же интернет-магазина: там двести шесть
позиций, здесь в одном гипермаркете триста семнадцать винных строк, и
у каждой заполнена марка — «Matalj», «Rubin», «Vinoprodukt Coka», — по
которой вино и сводится с нашей таблицей.

Как берётся:

1. Список файлов на дату — запросом GraphQL к `maxi.rs/api/v1/`,
   `GetDigitalPriceListsByDate`. Дата в формате dd-MM-yyyy.
2. Сами файлы — с `static.maxi.rs`.

**Оба хоста отвечают только браузеру.** Без строки `User-Agent` браузера
API отдаёт 403, а CDN — страницу «Access Denied» вместо файла. Это не
защита от робота вообще, а проверка одной строки, но знать надо: ошибка
приходит содержимым файла, а не кодом ответа.

Берутся не все магазины, а одиннадцать гипермаркетов «Mega Maxi»: у них
ассортимент шире всего, и они разбросаны по стране — Београд, Нови Сад,
Ниш, Крагујевац, Краљево, Ужице, Шабац, Чачак, Врњачка Бања. Пятьсот
файлов ради того же ассортимента качать незачем.

Пишет `maxi-cenovnik-ceny.json`. Кеш — в `kesh-cenovniki/`.
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
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-cenovniki"
API = "https://www.maxi.rs/api/v1/"
CDN = "https://static.maxi.rs/"
PAUZA = 1.0
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
ZAPROS_SPISKA = (
    "query GetDigitalPriceListsByDate($date: String!, $after: String, "
    "$first: Int) { digitalPriceListsByDate(date: $date, after: $after, "
    "first: $first) { items { name path lastModified } nextMarker } }")

# Вино в имени товара. Ищутся слова, а не подстроки: «vinsko sirće» —
# уксус, «vinjak» — бренди, и оба содержат «vin».
VINO = re.compile(r"\b(vino|vina|vinu|vinom)\b", re.I)
NE_VINO = re.compile(r"\b(sirce|sirće|vinjak|rakija|pivo|spricer|špricer|"
                     r"cokolad|čokolad|bombon|kobasic|paste|sos)\b", re.I)
CENA = re.compile(r"([\d.,]+)")


def vzjat(imya_kesha, sdelat):
    """Кеш на диске: чужие файлы по мегабайту, качать дважды незачем."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    for popytka in range(4):
        try:
            tekst = sdelat()
            break
        except Exception:
            if popytka == 3:
                raise
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def spisok_fajlov(data):
    """Все ценовники на дату. Страницами по сто, курсор — `nextMarker`."""
    vse, posle = [], None
    while True:
        telo = json.dumps({
            "operationName": "GetDigitalPriceListsByDate",
            "variables": {"date": data, "first": 100, "after": posle},
            "query": ZAPROS_SPISKA}).encode()

        def poluchit(telo=telo):
            zapros = urllib.request.Request(
                API, data=telo,
                headers={"Content-Type": "application/json",
                         "User-Agent": BRAUZER})
            with urllib.request.urlopen(zapros, timeout=90) as otvet:
                return otvet.read().decode("utf-8", "replace")

        kus = json.loads(vzjat("spisok-%s-%d.json" % (data, len(vse)), poluchit))
        d = kus["data"]["digitalPriceListsByDate"]
        vse += d["items"]
        posle = d.get("nextMarker")
        if not posle:
            return vse


def skachat_cenovnik(put):
    def poluchit():
        zapros = urllib.request.Request(
            CDN + put, headers={"User-Agent": BRAUZER,
                                "Referer": "https://www.maxi.rs/cenovnici"})
        with urllib.request.urlopen(zapros, timeout=180) as otvet:
            return otvet.read().decode("utf-8-sig", "replace")
    return vzjat(put.rsplit("/", 1)[-1], poluchit)


def chislo(zapis):
    """«659.99 rsd» → 659.99. Пусто у товара без акции — это не ноль."""
    sovpalo = CENA.search(zapis or "")
    if not sovpalo:
        return None
    try:
        return float(sovpalo.group(1).replace(",", "."))
    except ValueError:
        return None


def litrov(zapis):
    """«JEDINICA MERE» — число без единицы: «.75» это 0,75 л, «3» — три
    литра, «.185» — сто восемьдесят пять граммов. У вина это литры."""
    try:
        return float((zapis or "").strip())
    except ValueError:
        return None


def vinnye_stroki(tekst, magazin):
    najdeno = []
    for r in csv.DictReader(io.StringIO(tekst), delimiter=";"):
        imya = (r.get("NAZIV PROIZVODA") or "").strip()
        if not VINO.search(imya) or NE_VINO.search(imya):
            continue
        najdeno.append({
            "vino": imya,
            "hozyaistvo": (r.get("ROBNA MARKA") or "").strip(),
            "shtrihkod": (r.get("BARKOD PROIZVODA") or "").strip(),
            "cena_rsd": chislo(r.get("PRODAJNA CENA")),
            "cena_akcii": chislo(r.get("SNIZENA CENA")),
            "litrov": litrov(r.get("JEDINICA MERE")),
            "magazin": magazin,
        })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--data", default=time.strftime("%d-%m-%Y",
                                                        time.gmtime(time.time() - 86400)),
                        help="дата ценовника, dd-MM-yyyy (по умолчанию вчера)")
    razbor.add_argument("--vse-magaziny", action="store_true",
                        help="брать все магазины, а не только гипермаркеты")
    kljuchi = razbor.parse_args()

    fajly = spisok_fajlov(kljuchi.data)
    print("ценовников на %s: %d" % (kljuchi.data, len(fajly)))
    nuzhnye = [z for z in fajly
               if kljuchi.vse_magaziny
               or "MEGA_MAXI" in z["path"].rsplit("/", 1)[-1]]
    print("берём %d" % len(nuzhnye))

    stroki = []
    for nomer, z in enumerate(nuzhnye, 1):
        imya = z["path"].rsplit("/", 1)[-1]
        magazin = re.sub(r"_\d{8}\.csv$", "", imya)
        stroki += vinnye_stroki(skachat_cenovnik(z["path"]), magazin)
        print("  %2d/%d %-46s винных строк всего %d"
              % (nomer, len(nuzhnye), magazin[:46], len(stroki)))

    # Один товар лежит в нескольких магазинах и стоит там по-разному.
    # Ключ — штрихкод: имя у Maxi сокращено по-разному от строки к строке
    # («Vino crv.Lederer», «Vino crveno Lederer»), а штрихкод один.
    po_kodu = collections.defaultdict(list)
    for s in stroki:
        po_kodu[s["shtrihkod"] or s["vino"]].append(s)
    vina = []
    for kod, spisok in po_kodu.items():
        ceny = [s["cena_rsd"] for s in spisok if s["cena_rsd"]]
        akcii = [s["cena_akcii"] for s in spisok if s["cena_akcii"]]
        obrazec = spisok[0]
        vina.append({
            "vino": obrazec["vino"],
            "hozyaistvo": obrazec["hozyaistvo"],
            "shtrihkod": obrazec["shtrihkod"],
            # Середина по магазинам: в Ужице и на Врачару цена разная,
            # и брать первую попавшуюся значило бы выдавать один магазин
            # за всю сеть.
            "cena_rsd": round(statistics.median(ceny), 2) if ceny else None,
            "cena_akcii": round(statistics.median(akcii), 2) if akcii else None,
            "litrov": obrazec["litrov"],
            "magazinov": len(spisok),
            "v_prodazhe": True,
        })
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "maxi-cenovnik-ceny.json").write_text(json.dumps({
        "chto_eto": "Винные строки обязательных ценовников Maxi: цена, цена "
                    "по акции, штрихкод, марка. Полка сети, а не витрина "
                    "интернет-магазина.",
        "istochnik": "maxi.rs/cenovnici, гипермаркеты «Mega Maxi», "
                     "ценовник за " + kljuchi.data,
        "sobrano": time.strftime("%Y-%m-%d"),
        "magazinov": len(nuzhnye),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nразных товаров %d, с ценой %d → maxi-cenovnik-ceny.json"
          % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
