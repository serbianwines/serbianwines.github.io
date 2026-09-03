# -*- coding: utf-8 -*-
"""Цены сербских вин из каталога «Wine Stars».

Второй ценовой источник после `vzjat-vinoteku.py`. Нужен затем, что одна
винотека — это её ассортимент, а не сербская полка: по одному магазину
нельзя говорить ни о среднем уровне цен, ни о том, дорого ли вино.

Магазин из того же теста, что и Винотека Београд: всё нужное лежит
атрибутами `data-*` на узле товара — имя, хозяйство (`data-brand`), цена
и категория, из которой читается цвет. Браузер не нужен.

Пишет `winestars-ceny.json`. Кеш страниц — в `kesh-winestars/`.
"""
import argparse, json, pathlib, re, time, urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-winestars"
RAZDEL = "https://winestars.rs/category/vina/56/%d/srbija"
PAUZA = 1.5
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Номер товара берётся самой скобкой: искать его потом в `polya` нельзя —
# окно начинается уже после него, и `data-product=` там не встретится,
# зато встретится `data-product-name`. Первая редакция на этом и споткнулась:
# у всех товаров номер выходил пустым, и вторая страница целиком считалась
# уже виденной.
TOVAR = re.compile(r'data-product="(?P<nomer>\d+)"(?P<polya>.{0,1400})', re.S)
POLE = lambda imya, kus: (re.search(r'data-%s="([^"]*)"' % imya, kus, re.I)
                          or [None, ""])[1]
ADRES = re.compile(r'href="(https://winestars\.rs/product/[^"]+)"')


def vzjat(nomer):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / ("spisok-%d.html" % nomer)
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    zapros = urllib.request.Request(RAZDEL % nomer, headers={"User-Agent": BRAUZER})
    with urllib.request.urlopen(zapros, timeout=90) as otvet:
        tekst = otvet.read().decode("utf-8", "replace")
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def razobrat(stranica):
    najdeno = []
    for kus in TOVAR.finditer(stranica):
        polya = kus.group("polya")
        imya = POLE("product-name", polya)
        if not imya:
            continue
        hvost = stranica[kus.end():kus.end() + 900]
        adres = ADRES.search(hvost)
        # Категория у магазина читается цветом: «Belo vino», «Crveno vino».
        kategorii = POLE("categories", polya).replace("&quot;", '"')
        try:
            kategorii = json.loads(kategorii) if kategorii else []
        except ValueError:
            kategorii = []
        cena = POLE("price", polya)
        najdeno.append({
            "nomer": kus.group("nomer"),
            "vino": imya.strip(),
            "hozyaistvo": POLE("brand", polya).strip(),
            "artikul": POLE("sku", polya).strip(),
            "kategorii": kategorii,
            "cena_rsd": float(cena) if re.fullmatch(r"\d+(\.\d+)?", cena or "") else None,
            "stranica": adres.group(1) if adres else "",
        })
    return najdeno


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--stranic", type=int, default=40,
                        help="предел страниц; обход всё равно встанет на пустой")
    kljuchi = razbor.parse_args()
    vina, vidano = [], set()
    for nomer in range(1, kljuchi.stranic + 1):
        svoi = razobrat(vzjat(nomer))
        novyh = [z for z in svoi if z["nomer"] not in vidano]
        for z in novyh:
            vidano.add(z["nomer"])
            vina.append(z)
        print("  страница %2d: разобрано %2d, новых %2d" % (nomer, len(svoi), len(novyh)))
        # Магазин на страницах за последней отдаёт ту же последнюю, поэтому
        # признак конца — не пустая страница, а отсутствие новых товаров.
        if not novyh:
            break
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "winestars-ceny.json").write_text(json.dumps({
        "chto_eto": "Цены сербских вин у «Wine Stars». Розничная, в динарах, "
                    "на день сбора. Второй ценовой источник рядом с Винотекой Београд.",
        "istochnik": RAZDEL % 1,
        "sobrano": time.strftime("%Y-%m-%d"),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d вин, из них с ценой %d → winestars-ceny.json"
          % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
