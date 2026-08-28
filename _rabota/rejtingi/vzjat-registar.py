# -*- coding: utf-8 -*-
"""Винарски регистар — официальный перечень производителей вина.

Министарство пољопривреде публикует «Преглед произвођача вина» таблицей
XLSX: регистрационный номер, вид лица, матичный номер, полное название,
округ и населённое место с почтовым индексом. Населённое место — то, чего
не хватало, чтобы поставить рејон хозяйствам, о которых молчат каталоги.

Страница реестра: https://www.minpolj.gov.rs/vinarski-registar/
Файл там называется «Pregled-proizvodjaca-vina-na-dan-<дата>.xlsx» и
меняет имя при каждом обновлении, поэтому адрес берётся со страницы.
"""
import json, re, sys, pathlib, zipfile, io, urllib.request
import xml.etree.ElementTree as ET

ZDES = pathlib.Path(__file__).resolve().parent
STRANICA = "https://www.minpolj.gov.rs/vinarski-registar/"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
PROSTRANSTVO = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def skachat(adres):
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    with urllib.request.urlopen(zapros, timeout=90) as otvet:
        return otvet.read()


def najti_fajl():
    stranica = skachat(STRANICA).decode("utf-8", "replace")
    ssylki = re.findall(r'href="([^"]*Pregled-proizvodjaca-vina[^"]*\.xlsx)"', stranica)
    if not ssylki:
        raise SystemExit("на странице реестра нет ссылки на «Pregled proizvodjaca vina»")
    return ssylki[0]


def razobrat(dvoichnoe):
    kniga = zipfile.ZipFile(io.BytesIO(dvoichnoe))
    obshie = ["".join(t.text or "" for t in si.iter(PROSTRANSTVO + "t"))
              for si in ET.fromstring(kniga.read("xl/sharedStrings.xml"))]
    list_ = ET.fromstring(kniga.read("xl/worksheets/sheet1.xml"))
    stroki = []
    for ryad in list_.iter(PROSTRANSTVO + "row"):
        yachejki = {}
        for yach in ryad.iter(PROSTRANSTVO + "c"):
            stolbec = re.match(r"[A-Z]+", yach.get("r")).group()
            znach = yach.find(PROSTRANSTVO + "v")
            if znach is None:
                vstroennoe = yach.find(PROSTRANSTVO + "is")
                tekst = ("".join(t.text or "" for t in vstroennoe.iter(PROSTRANSTVO + "t"))
                         if vstroennoe is not None else "")
            elif yach.get("t") == "s":
                tekst = obshie[int(znach.text)]
            else:
                tekst = znach.text or ""
            yachejki[stolbec] = tekst.strip()
        stroki.append(yachejki)
    return stroki


def bez_koda(znachenie):
    """«(19) Rasinski» → «Rasinski»; «(37230) Velja Glava» → индекс и место."""
    sovpalo = re.match(r"\((\d+)\)\s*(.*)", znachenie or "")
    if sovpalo:
        return sovpalo.group(1), sovpalo.group(2).strip()
    return "", (znachenie or "").strip()


def main():
    adres = najti_fajl()
    print("файл реестра:", adres)
    stroki = razobrat(skachat(adres))
    zapisi = []
    for ryad in stroki[1:]:
        nomer_okruga, okrug = bez_koda(ryad.get("E"))
        indeks, naselje = bez_koda(ryad.get("F"))
        nazvanie = ryad.get("D", "")
        if not nazvanie:
            continue
        zapisi.append({
            "reg_nomer": ryad.get("A", ""),
            "vid": ryad.get("B", ""),
            "maticnyj_nomer": ryad.get("C", ""),
            "nazvanie": nazvanie,
            "okrug": okrug,
            "okrug_nomer": nomer_okruga,
            "naselje": naselje,
            "indeks": indeks,
        })
    itog = {
        "chto_eto": "Винарски регистар Министарства пољопривреде: производители вина, "
                    "внесённые в реестр. Округ — управни, не виноградарский; место — насеље.",
        "istochnik": adres,
        "stranica": STRANICA,
        "vsego": len(zapisi),
        "zapisi": zapisi,
    }
    put = ZDES / "vinarski-registar.json"
    put.write_text(json.dumps(itog, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"записей: {len(zapisi)} → {put.name}")


if __name__ == "__main__":
    main()
