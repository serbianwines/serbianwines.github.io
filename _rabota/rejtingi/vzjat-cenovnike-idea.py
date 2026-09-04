#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полка супермаркетов IDEA, Roda и Mercator из обязательных ценовников.

С 2025 года крупная сербская розница обязана публиковать цены каждого
магазина отдельным файлом на каждый день. Группа IDEA — Roda — Mercator
выкладывает их одним архивом на `roda.rs/cenovnici`: 289 магазинов,
по книге Excel на магазин, полный ассортимент с ценой, штрихкодом
и маркой.

Зачем отдельно от Maxi. Это другая сеть и другая полка: у Mercator'а
в белградском гипермаркете стоит «Kameničarka» Александровића за 2099,99
динара, а у Maxi её нет вовсе. Автор нашёл её в Wolt — и цена там та же
до копейки, то есть приложение показывает полку, а не наценку.

Три ловушки, все три стоили времени.

1. **Адрес скачивания не тот, что в ссылке.** На странице стоит
   `/api/shops-price-lists/<N>/download` — относительный путь, и по нему
   сам сайт отвечает своей же страницей «404». Файл лежит на отдельном
   хосте `backend.roda.rs`, и найти его можно только в сборках страницы:
   имя `https://backend.roda.rs` попадается в одном из чанков Next.js.
2. **Файлов на выбор несколько, и они разного охвата.** CSV за 26 августа
   весит 20 МБ, и в нём четыре магазина; архив за нужный день — 131 МБ,
   и в нём все 289. Размер тут не мера свежести, а мера полноты.
3. **Кодировка.** CSV — UTF-16 с BOM и точкой с запятой; книги Excel
   внутри архива — обычный xlsx. Разбираются здесь стандартной
   библиотекой: xlsx это zip с XML, и ради одного плоского листа тянуть
   стороннюю библиотеку незачем.

Берутся не все 289 магазинов, а крупные: два гипермаркета и шесть
«Roda Mega», плюс те «Super» и «VML», у которых ассортимент такой же
широкий. Остальные — мелкие магазины у дома с тем же товаром.

Пишет `idea-cenovnik-ceny.json`. Кеш — в `kesh-cenovniki-idea/`.
"""
import argparse
import collections
import json
import pathlib
import re
import statistics
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-cenovniki-idea"
STRANICA = "https://roda.rs/cenovnici"
BACKEND = "https://backend.roda.rs/api/shops-price-lists/%d/download"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Крупные магазины сети. Мелкие держат тот же товар, а файлов втрое
# больше, и ассортимент у них уже.
KRUPNYE = re.compile(r"HIPERMARKET|RODA MEGA|SUPER |VML", re.I)
# Вино в имени товара — те же правила, что у ценовников Maxi: ищутся
# слова, а не подстроки, потому что «vinsko sirće» это уксус,
# а «vinjak» — бренди.
VINO = re.compile(r"\b(vino|vina|vinu|vinom)\b", re.I)
NE_VINO = re.compile(r"\b(sirce|sirće|vinjak|rakija|pivo|spricer|špricer|"
                     r"cokolad|čokolad|bombon|kobasic|paste|sos)\b", re.I)
XSD = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def vzjat(adres, imya_kesha, dvoichnyj=False):
    """Скачать с кешем на диске; при обрыве — ещё три попытки."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_bytes() if dvoichnyj else fajl.read_text(
            encoding="utf-8", errors="replace")
    for popytka in range(4):
        try:
            zapros = urllib.request.Request(
                adres, headers={"User-Agent": BRAUZER, "Referer": STRANICA})
            with urllib.request.urlopen(zapros, timeout=600) as otvet:
                telo = otvet.read()
            break
        except Exception:
            if popytka == 3:
                raise
            time.sleep(2 ** (popytka + 1))
    fajl.write_bytes(telo)
    return telo if dvoichnyj else telo.decode("utf-8", "replace")


def spisok_cenovnikov():
    """Что выложено: id, имя файла, дата, размер. Список стоит прямо
    в разметке страницы, отдельным запросом его брать не надо."""
    stranica = vzjat(STRANICA, "stranica.html")
    najdeno = []
    for z in re.finditer(
            r'"id":(\d+),"name":"(cene[^"]+)"[^}]*?"dateOnly":"([^"]+)"'
            r'[^}]*?"blobContentLength":"(\d+)","blobContentType":"([^"]+)"',
            stranica):
        najdeno.append({"id": int(z.group(1)), "imya": z.group(2),
                        "data": z.group(3), "bajt": int(z.group(4)),
                        "tip": z.group(5)})
    return najdeno


def nomer_stolbca(adres):
    """«H12» → 7. Буквенная часть адреса ячейки — номер столбца."""
    bukvy = re.match(r"([A-Z]+)", adres or "")
    if not bukvy:
        return None
    nomer = 0
    for bukva in bukvy.group(1):
        nomer = nomer * 26 + (ord(bukva) - 64)
    return nomer - 1


def stroki_xlsx(dvoichnoe):
    """Плоский лист книги Excel — списками значений, стандартной
    библиотекой. Книга здесь простая: один лист, строки без формул,
    все тексты в общей таблице строк.

    Значение кладётся по адресу ячейки, а не подряд. Excel пустых ячеек
    не пишет вовсе, и первая же редакция, складывавшая значения подряд,
    съезжала на всех строках без акции: `StopaPDV` (20) вставала в
    `SnizenaCena`, и «акционная цена» выходила двадцать динаров у пятисот
    сорока семи товаров из семисот шестидесяти девяти. Цена уцелела
    случайно — `RedovnaCena` стоит до первой дыры; будь пустой
    `RobnaMarka`, съехала бы и она.
    """
    with zipfile.ZipFile(dvoichnoe) as kniga:
        obshchie = []
        if "xl/sharedStrings.xml" in kniga.namelist():
            koren = ET.fromstring(kniga.read("xl/sharedStrings.xml"))
            for si in koren:
                obshchie.append("".join(t.text or "" for t in si.iter(XSD + "t")))
        imya_lista = next(i for i in kniga.namelist()
                          if re.match(r"xl/worksheets/sheet\d+\.xml$", i))
        koren = ET.fromstring(kniga.read(imya_lista))
        for stroka in koren.iter(XSD + "row"):
            znacheniya = []
            for nomer, kletka in enumerate(stroka):
                v = kletka.find(XSD + "v")
                tekst = v.text if v is not None else None
                if kletka.get("t") == "s" and tekst is not None:
                    tekst = obshchie[int(tekst)]
                elif kletka.get("t") == "inlineStr":
                    tekst = "".join(t.text or "" for t in kletka.iter(XSD + "t"))
                stolbec = nomer_stolbca(kletka.get("r") or "")
                if stolbec is None:
                    stolbec = nomer
                while len(znacheniya) <= stolbec:
                    znacheniya.append(None)
                znacheniya[stolbec] = tekst
            yield znacheniya


def chislo(zapis):
    try:
        return float(str(zapis).replace(",", "."))
    except (TypeError, ValueError):
        return None


def vinnye_stroki(dvoichnoe, magazin):
    najdeno, shapka = [], None
    for znacheniya in stroki_xlsx(dvoichnoe):
        if shapka is None:
            shapka = [(z or "").strip() for z in znacheniya]
            continue
        z = dict(zip(shapka, znacheniya))
        imya = (z.get("NazivProizvoda") or "").strip()
        if not VINO.search(imya) or NE_VINO.search(imya):
            continue
        najdeno.append({
            "vino": imya,
            "hozyaistvo": (z.get("RobnaMarka") or "").strip(),
            "shtrihkod": (z.get("BarkodProizvoda") or "").strip(),
            "cena_rsd": chislo(z.get("RedovnaCena")),
            "cena_akcii": chislo(z.get("SnizenaCena")),
            "magazin": magazin,
        })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--vse-magaziny", action="store_true",
                        help="брать все 289 магазинов, а не только крупные")
    kljuchi = razbor.parse_args()

    vse = spisok_cenovnikov()
    arhivy = [z for z in vse if z["imya"].endswith(".zip")]
    if not arhivy:
        raise SystemExit("на странице нет ни одного архива с ценовниками")
    svezhij = max(arhivy, key=lambda z: z["data"])
    print("ценовник за %s, %.0f МБ" % (svezhij["data"], svezhij["bajt"] / 1e6))
    put = KESH / svezhij["imya"]
    if not put.exists():
        vzjat(BACKEND % svezhij["id"], svezhij["imya"], dvoichnyj=True)

    stroki = []
    with zipfile.ZipFile(put) as arhiv:
        vnutri = []
        for imya in arhiv.namelist():
            sovpalo = re.match(r"objekat_(.+?)_cene_proizvoda", imya)
            magazin = sovpalo.group(1) if sovpalo else imya
            if kljuchi.vse_magaziny or KRUPNYE.search(magazin):
                vnutri.append((imya, magazin))
        print("магазинов в архиве %d, берём %d" % (len(arhiv.namelist()), len(vnutri)))
        for nomer, (imya, magazin) in enumerate(sorted(vnutri, key=lambda p: p[1]), 1):
            import io
            svoi = vinnye_stroki(io.BytesIO(arhiv.read(imya)), magazin)
            stroki += svoi
            print("  %2d/%d %-40s винных строк %3d"
                  % (nomer, len(vnutri), magazin[:40], len(svoi)))

    # Один товар лежит в нескольких магазинах и стоит там по-разному.
    # Ключ — штрихкод: имя сокращено по-разному от строки к строке.
    po_kodu = collections.defaultdict(list)
    for s in stroki:
        po_kodu[s["shtrihkod"] or s["vino"]].append(s)
    vina = []
    for spisok in po_kodu.values():
        ceny = [s["cena_rsd"] for s in spisok if s["cena_rsd"]]
        akcii = [s["cena_akcii"] for s in spisok if s["cena_akcii"]]
        obrazec = spisok[0]
        vina.append({
            "vino": obrazec["vino"],
            "hozyaistvo": obrazec["hozyaistvo"],
            "shtrihkod": obrazec["shtrihkod"],
            "cena_rsd": round(statistics.median(ceny), 2) if ceny else None,
            "cena_akcii": round(statistics.median(akcii), 2) if akcii else None,
            "magazinov": len(spisok),
            "v_prodazhe": True,
        })
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "idea-cenovnik-ceny.json").write_text(json.dumps({
        "chto_eto": "Винные строки обязательных ценовников группы IDEA — Roda — "
                    "Mercator: цена, цена по акции, штрихкод, марка. Полка сети, "
                    "а не витрина интернет-магазина.",
        "istochnik": "roda.rs/cenovnici, файл за %s; крупные магазины сети"
                     % svezhij["data"],
        "sobrano": time.strftime("%Y-%m-%d"),
        "magazinov": len({s["magazin"] for s in stroki}),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nразных товаров %d, с ценой %d → idea-cenovnik-ceny.json"
          % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
