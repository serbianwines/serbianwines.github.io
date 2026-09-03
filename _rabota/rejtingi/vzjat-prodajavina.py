# -*- coding: utf-8 -*-
"""Цены и свойства сербских вин у «Prodaja vina» (prodajavina.com).

Пятая винотека. Взята ради того же, ради чего «Wine Art Shop»: у неё
раздел сербских вин разложен **по рејонима** — `/vina/srpska-vina/
tri-morave-rejon.html`, `/vina/srpska-vina/vranjski-rejon.html`, — и
рејон стоит у каждого вина в карточке списка. Это второе независимое
показание торговли о происхождении вина, а не о месте подвала.

Магазин на Magento, и всё нужное лежит прямо в списке: имя с урожаем,
сорт, рејон (или виногорје — магазин мешает уровни), хозяйство, цвет,
крепость и цена. За карточками ходить не нужно вовсе.

**Ловушка цены.** У товара три цены: за бутылку, за ящик шести и за ящик
двенадцати. Ящик дешевле, и если брать первую попавшуюся `<span
class="price">`, в таблицу попадёт цена оптовой упаковки. Берётся только
та, что стоит внутри `cena_1_proizvod` — «1 x 750ml».

Пишет `prodajavina-ceny.json`. Кеш страниц — в `kesh-prodajavina/`.
"""
import argparse
import html
import json
import pathlib
import re
import time
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-prodajavina"
SAJT = "https://prodajavina.com"
RAZDEL = SAJT + "/vina/srpska-vina.html"
PAUZA = 1.5
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def vzjat(adres, imya_kesha):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    # Туннель здешнего прокси рвётся на середине обмена без всякой
    # закономерности; это не отказ сайта. Повтор с растущей паузой.
    for popytka in range(4):
        try:
            with urllib.request.urlopen(zapros, timeout=90) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            break
        except Exception:
            if popytka == 3:
                raise
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def chislo(stroka):
    """«1.290,00 din.» → 1290.0."""
    stroka = re.sub(r"[^\d.,]", "", stroka or "").replace(".", "").replace(",", ".")
    try:
        return float(stroka)
    except ValueError:
        return None


# У первой и последней карточки на странице класс с приписком —
# «product first», «product last», — и метка по точному классу теряла
# по две карточки со страницы из пятнадцати.
KARTOCHKA = re.compile(r'<li class="product(?:\s+\w+)?">')
# Адрес товара бывает и в корне сайта, и внутри раздела:
# `/aleksic-bonaca-2023.html`, но `/vina/srpska-vina/aleksandrovic-
# prokupac-2022.html`. Требование корня теряло по вину со страницы.
ADRES = re.compile(r'href="(https://prodajavina\.com/[a-z0-9/-]+\.html)" title')
IMYA = re.compile(r'class="product-name"><a[^>]*title="([^"]*)"')
# Сорт и рејон стоят в одном блоке «izregije», и искать их надо только
# в нём: у части вин адрес самой карточки лежит внутри `/vina/srpska-
# vina/`, и поиск рејона по всей карточке принимал за рејон имя вина.
IZREGIJE = re.compile(r'class="desc std izregije[^"]*">(.*?)</div>', re.S)
SORT = re.compile(r'href="[^"]*\?sorta=\d+" title="([^"]*)"')
REJON = re.compile(r'href="[^"]*/vina/srpska-vina/[a-z0-9-]+\.html" title="([^"]*)"')
HOZYAISTVO = re.compile(r'href="[^"]*\?vinarija=\d+" title="([^"]*)"')
CVET = re.compile(r'class="tip_vina_slicica[^"]*"[^>]*>|title="([^"]*vino[^"]*)" class="tip_vina_slicica')
CVET_IZ_SSYLKI = re.compile(r'tip_vina\.html" title="([^"]*)"')
KREPOST = re.compile(r'Alk\.\s*([\d,\.]+)\s*%')
TOVAR = re.compile(r'/product/(\d+)/')
NET_V_PRODAZHE = 'availability out-of-stock'
# Цена одной бутылки: только внутри «1 x 750ml». Ниже в карточке стоят
# цены за ящик шести и двенадцати, и они дешевле.
CENA_BUTYLKI = re.compile(
    r"cena_1_proizvod[^>]*>\s*(?P<obem>[^<]*)"          # «1 x 750ml»
    r"(?:.(?!tier-price))*?class='price'>([^<]*)<", re.S)
CENA_ZAPASNAYA = re.compile(
    r'cena_1_proizvod[^>]*>(?P<obem>[^<]*)</span>'
    r'(?:.(?!tier-price))*?class="price">([^<]*)<', re.S)
OBEM = re.compile(r'(\d+)\s*x\s*(\d+(?:[.,]\d+)?)\s*(ml|l)\b', re.I)


def litrov(zapis):
    """«1 x 750ml» → 0.75. Число бутылок в упаковке здесь всегда одна:
    цена ящика берётся отдельным узлом и нам не нужна."""
    sovpalo = OBEM.search(zapis or "")
    if not sovpalo:
        return None
    skolko = float(sovpalo.group(2).replace(",", "."))
    return skolko / 1000 if sovpalo.group(3).lower() == "ml" else skolko


# В мегаменю лежит закомментированный промо-блок с товарной карточкой —
# «Nino Franco Prosecco», итальянское, без рејона. Браузер его не рисует,
# а разбор находил и считал шестнадцатым вином на странице из пятнадцати.
KOMMENTARIJ = re.compile(r"<!--.*?-->", re.S)


def razobrat_spisok(stranica):
    najdeno = []
    for kus in KARTOCHKA.split(KOMMENTARIJ.sub(" ", stranica))[1:]:
        imya = IMYA.search(kus)
        adres = ADRES.search(kus)
        if not imya or not adres:
            continue
        cena = CENA_BUTYLKI.search(kus) or CENA_ZAPASNAYA.search(kus)
        izregije = IZREGIJE.search(kus)
        otkuda = izregije.group(1) if izregije else ""
        rejon = REJON.search(otkuda)
        sort = SORT.search(otkuda)
        hozyaistvo = HOZYAISTVO.search(kus)
        cvet = CVET_IZ_SSYLKI.search(kus)
        krepost = KREPOST.search(kus)
        tovar = TOVAR.search(kus)
        najdeno.append({
            "nomer": tovar.group(1) if tovar else "",
            "vino": html.unescape(imya.group(1)).strip(),
            "hozyaistvo": (html.unescape(hozyaistvo.group(1)).strip()
                           if hozyaistvo else ""),
            "sorta": html.unescape(sort.group(1)).strip() if sort else "",
            # Магазин мешает уровни: у одних вин здесь рејон, у других
            # виногорје. Пишем как есть, разбирается при сведении.
            "rejon_magazina": (html.unescape(rejon.group(1)).strip()
                               if rejon else ""),
            "cvet_magazina": html.unescape(cvet.group(1)).strip() if cvet else "",
            "krepost": krepost.group(1) if krepost else "",
            "cena_rsd": chislo(cena.group(2)) if cena else None,
            "litrov": litrov(cena.group("obem")) if cena else None,
            "v_prodazhe": NET_V_PRODAZHE not in kus,
            "stranica": adres.group(1),
        })
    return najdeno


def vsego_pozicij(stranica):
    sovpalo = re.search(r'class="amount">\s*Artikli\s+\d+\s+do\s+\d+\s+od\s+(\d+)',
                        stranica)
    return int(sovpalo.group(1)) if sovpalo else 0


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--stranic", type=int, default=0,
                        help="сколько страниц взять (0 — весь раздел)")
    kljuchi = razbor.parse_args()

    pervaya = vzjat(RAZDEL, "spisok-1.html")
    vsego = vsego_pozicij(pervaya)
    na_stranice = len(razobrat_spisok(pervaya)) or 15
    stranic = kljuchi.stranic or (vsego + na_stranice - 1) // na_stranice
    print("в разделе «Српска вина» %d позиций, по %d на страницу, страниц %d"
          % (vsego, na_stranice, stranic))

    vina, vidano = [], set()
    for nomer in range(1, stranic + 1):
        adres = RAZDEL if nomer == 1 else "%s?p=%d" % (RAZDEL, nomer)
        stranica = pervaya if nomer == 1 else vzjat(adres, "spisok-%d.html" % nomer)
        svoi = razobrat_spisok(stranica)
        novyh = 0
        for z in svoi:
            klyuch = z["nomer"] or z["stranica"]
            if klyuch in vidano:
                continue
            vidano.add(klyuch)
            vina.append(z)
            novyh += 1
        print("  страница %2d: карточек %2d, новых %2d" % (nomer, len(svoi), novyh))
        if not svoi:
            break

    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    s_rejonom = sum(1 for z in vina if z["rejon_magazina"])
    (ZDES / "prodajavina-ceny.json").write_text(json.dumps({
        "chto_eto": "Сербские вина у «Prodaja vina»: цена за бутылку в динарах, "
                    "сорт, цвет, крепость, объём и рејон, как его называет "
                    "сам магазин.",
        "istochnik": RAZDEL,
        "sobrano": time.strftime("%Y-%m-%d"),
        "vsego_v_razdele": vsego,
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d вин, с ценой %d, с рејоном %d → prodajavina-ceny.json"
          % (len(vina), s_cenoj, s_rejonom))


if __name__ == "__main__":
    main()
