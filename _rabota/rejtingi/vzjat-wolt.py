#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Цены винотек в доставке Wolt.

Начать надо с признания. В `ceny-vruchnuyu.json` записано: «Wolt отвечает
429 на всё подряд», — и потому четырнадцать цен автор снимал со снимков
экрана вручную. Это была моя ошибка, а не отказ Wolt. Ассортимент лежит
открыто, и путь к нему такой:

    https://consumer-api.wolt.com/consumer-api/consumer-assortment/v1
        /venues/slug/<площадка>/assortment
        /venues/slug/<площадка>/assortment/categories/slug/<раздел>

Первый адрес отдаёт разделы, второй — товары раздела, страницами по
пятьдесят; следующая страница берётся по `metadata.next_page_token`.
Ключевое — **удвоенный `consumer-api` в пути**. Без него, то есть по
`consumer-api.wolt.com/consumer-assortment/v1/...`, тот же адрес отвечает
`404 page not found`, и я принял это за то, что раздел закрыли. Ни
заголовков, ни ключа не нужно; ограничения по частоте на этом пути тоже
нет — 429 приходит с других, поисковых.

Что берётся.

Список площадок — из карты сайта: `wolt.com/sitemap/venues/srb-1.xml`,
две тысячи шестьдесят шесть сербских заведений. Из них отбираются
винотеки — по имени слага (`vinoteka`, `vino`, `wine`) плюс те, что
названы иначе и вписаны руками (`ours`). Супермаркеты Wolt сюда нарочно
не идут: полка сети берётся обязательными ценовниками (`vzjat-cenovnike.py`,
`vzjat-cenovnike-idea.py`), а это цена без наценки доставки.

Вино отделяется от ракије не по разделу, а по метке товара:
`product_hierarchy_tags` содержит `WINE`. У OURS так отделились
четыреста шестьдесят пять вин от двадцати ракија, девяти жестин и семи
джинов, и ни одна чаша не попала.

Цена приходит в мелких единицах: `price` 200200 — это 2002,00 динара.
Проверено по сохранённой автором странице: «Janko Zapis Crveni 0.75l»
показан там как «RSD 2,002.00».

Три ловушки.

1. **Набор вместо бутылки.** «Fantinel Friulano akcija 3x0,75l». Цена
   набора, поставленная вину, завысила бы её втрое.
2. **Витрина в браузере — не весь раздел.** Сохранённая страница держит
   девятнадцать карточек из ста восьмидесяти трёх: список подгружается
   по мере прокрутки. Разбирать сохранённую вёрстку тут бессмысленно,
   и потому берётся API.
3. **Пустая площадка — не пустая полка.** У делекатесной GUSTO раздел
   «Vino» отвечает нулём товаров, хотя автор нашёл там вина Грумена.
   Поэтому счёт по каждой площадке печатается: ноль виден, а не молчит.

Одно и то же вино стоит в разных винотеках по-разному. Как и у Maxi,
берётся середина, а число лавок сохраняется рядом — цена одной лавки
не выдаётся за цену рынка.

Каждая строка помечена `kanal: "dostavka"`: в приложении цена бывает
с наценкой — измерено на Легате, восемнадцать процентов, — и в сведении
такая строка идёт в счёт только там, где полочной нет вовсе.

Пишет `wolt-ceny.json`. Кеш — в `kesh-wolt/`.
"""
import argparse
import collections
import json
import pathlib
import re
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-wolt"
KARTA = "https://wolt.com/sitemap/venues/srb-1.xml"
API = ("https://consumer-api.wolt.com/consumer-api/consumer-assortment/v1"
       "/venues/slug/%s/assortment")
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
PAUZA = 0.3
SROK = 60
# Ярлык страницы заведения читается из `schema.org/Store`; он лежит
# в середине вёрстки, около четырёхсот тридцати килобайт от начала.
# Читать страницу целиком (полтора мегабайта на заведение) незачем.
GOLOVA = 700_000

# Винотека по имени слага. «podrum» и «vinarija» тоже сюда: под ними
# сидят лавки при хозяйствах.
VINNAYA = re.compile(r"vinotek|vino-|-vino|^vino|wine|vinarij|podrum", re.I)
# Названы иначе, а торгуют вином. Список ведётся руками и с проверкой.
IMENEM_NE_VIDNO = ("ours",)
# Набор бутылок, а не бутылка.
NABOR = re.compile(r"\bpaket|\bboc[ae]\b|\bbo[cč]a\b|\bset\b|\bkutij|"
                   r"\d\s*[x×]\s*0[.,]\d+", re.I)
OBEM = re.compile(r"(\d+(?:[.,]\d+)?)\s*(l|ml)\b", re.I)


def vzjat(imya, adres, golova=None):
    """Скачать с кешем на диске. Отказ тоже кешируется — пустой строкой."""
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya
    if fajl.exists():
        return fajl.read_text(encoding="utf-8")
    tekst = ""
    for popytka in range(3):
        try:
            zapros = urllib.request.Request(
                adres, headers={"User-Agent": BRAUZER, "Accept-Language": "en"})
            with urllib.request.urlopen(zapros, timeout=SROK) as otvet:
                syroe = otvet.read(golova) if golova else otvet.read()
            tekst = syroe.decode("utf-8", "replace")
            break
        except urllib.error.HTTPError as oshibka:
            if oshibka.code == 429 and popytka < 2:
                time.sleep(5 * (popytka + 1))
                continue
            break
        except Exception:
            if popytka == 2:
                break
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def ploshchadki():
    """Слаг → адрес страницы. Из карты сайта, город в адресе уже есть."""
    tekst = vzjat("karta-zavedenij.xml", KARTA)
    adresa = {}
    for syroe in re.findall(r"<loc>(.*?)</loc>", tekst, re.S):
        adres = re.sub(r"\s+", "", syroe)
        sovpalo = re.search(r"/venue/([^/]+)/?$", adres)
        if sovpalo:
            adresa.setdefault(sovpalo.group(1), adres)
    return adresa


def yarlyk(slag, adres):
    """Имя и город лавки — из `schema.org/Store` на её странице."""
    tekst = vzjat("zavedenie-%s.html" % slag, adres, golova=GOLOVA)
    for kus in re.findall(
            r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', tekst, re.S):
        try:
            zapis = json.loads(kus)
        except ValueError:
            continue
        if zapis.get("@type") == "Store":
            adres_lavki = zapis.get("address") or {}
            return {"magazin": zapis.get("name") or slag,
                    "gorod": adres_lavki.get("addressLocality"),
                    "ulica": adres_lavki.get("streetAddress")}
    return {"magazin": slag, "gorod": None, "ulica": None}


def razdely(slag):
    tekst = vzjat("razdely-%s.json" % slag, API % slag)
    try:
        return json.loads(tekst).get("categories") or []
    except ValueError:
        return []


def tovary(slag, razdel):
    """Все товары раздела: страницами, курсор — `next_page_token`."""
    najdeno, token, stranica = [], None, 1
    while True:
        adres = (API % slag) + "/categories/slug/" + urllib.parse.quote(razdel)
        if token:
            adres += "?page_token=" + urllib.parse.quote(token)
        tekst = vzjat("tovary-%s-%s-%d.json" % (slag, razdel, stranica),
                      adres)
        try:
            otvet = json.loads(tekst)
        except ValueError:
            return najdeno
        najdeno += otvet.get("items") or []
        token = (otvet.get("metadata") or {}).get("next_page_token")
        stranica += 1
        if not token or stranica > 60:
            return najdeno


def litrov(imya):
    """Объём из имени: «0.75l», «1L», «500 ml». Нет — значит нет."""
    sovpalo = OBEM.search(imya or "")
    if not sovpalo:
        return None
    chislo = float(sovpalo.group(1).replace(",", "."))
    return chislo / 1000 if sovpalo.group(2).lower() == "ml" else chislo


def vina_ploshchadki(slag, lavka):
    najdeno = []
    for razdel in razdely(slag):
        for tovar in tovary(slag, razdel.get("slug") or ""):
            if "WINE" not in (tovar.get("product_hierarchy_tags") or []):
                continue
            imya = (tovar.get("name") or "").strip()
            if not imya or NABOR.search(imya):
                continue
            cena = tovar.get("price")
            najdeno.append({
                "vino": imya,
                "cena_rsd": round(cena / 100, 2) if cena else None,
                "litrov": litrov(imya),
                "razdel": razdel.get("name"),
                # Описание пишет само хозяйство, и оно бывает
                # подробнее нашего: сорт, год, иногда виноградник.
                "opisanie": (tovar.get("description") or "").strip() or None,
                **lavka,
            })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--ploshchadok", type=int, default=0,
                        help="взять только первые N (для пробы)")
    kljuchi = razbor.parse_args()

    adresa = ploshchadki()
    otbor = sorted(s for s in adresa
                   if VINNAYA.search(s) or s in IMENEM_NE_VIDNO)
    if kljuchi.ploshchadok:
        otbor = otbor[:kljuchi.ploshchadok]
    print("заведений в Сербии %d, винотек %d" % (len(adresa), len(otbor)))

    stroki, pusto = [], []
    for nomer, slag in enumerate(otbor, 1):
        lavka = yarlyk(slag, adresa[slag])
        nashli = vina_ploshchadki(slag, lavka)
        stroki += nashli
        if not nashli:
            pusto.append(slag)
        print("  %2d/%d %-42s %-22s вин %4d" %
              (nomer, len(otbor), slag[:42], (lavka["gorod"] or "—")[:22],
               len(nashli)))

    # Одно вино в нескольких лавках стоит по-разному. Ключ — имя товара:
    # штрихкод у винотек заполнен через раз (у одной из ста девяти, у
    # другой у ста девяноста восьми из трёхсот пятидесяти трёх), и
    # ключом служить не может.
    po_imeni = collections.defaultdict(list)
    for zapis in stroki:
        po_imeni[zapis["vino"]].append(zapis)
    vina = []
    for imya, spisok in po_imeni.items():
        ceny = [z["cena_rsd"] for z in spisok if z["cena_rsd"]]
        obrazec = spisok[0]
        vina.append({
            "vino": imya,
            "cena_rsd": round(statistics.median(ceny), 2) if ceny else None,
            "litrov": obrazec["litrov"],
            "magazin": obrazec["magazin"],
            "gorod": obrazec["gorod"],
            "magazinov": len({z["magazin"] for z in spisok}),
            "opisanie": next((z["opisanie"] for z in spisok if z["opisanie"]),
                             None),
            "kanal": "dostavka",
            "v_prodazhe": True,
        })
    vina.sort(key=lambda z: z["vino"])
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])

    (ZDES / "wolt-ceny.json").write_text(json.dumps({
        "chto_eto": "Вина сербских винотек в доставке Wolt: имя товара, "
                    "цена в динарах, лавка и город. Цена в приложении "
                    "бывает с наценкой, поэтому у каждой строки "
                    "`kanal: \"dostavka\"`.",
        "istochnik": "consumer-api.wolt.com, ассортимент площадок из "
                     "wolt.com/sitemap/venues/srb-1.xml",
        "sobrano": time.strftime("%Y-%m-%d"),
        "ploshchadok": len(otbor),
        "ploshchadok_bez_vina": pusto,
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nстрок %d, разных вин %d, с ценой %d → wolt-ceny.json"
          % (len(stroki), len(vina), s_cenoj))
    if pusto:
        print("без вина: %s" % ", ".join(pusto))


if __name__ == "__main__":
    main()
