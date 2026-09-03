# -*- coding: utf-8 -*-
"""Цены и свойства вин из каталога «Cerpromet».

Третий ценовой источник и самый подробный: у карточки товара лежит
`schema.org/Product` с ценой в динарах, а рядом — таблица свойств, какой
нет ни у Винотеке Београд, ни у Wine Stars:

    Zemlja : Srbija   Sorta : Cabernet - Merlot   Tip vina : Suvo
    Alkohol : 14.5    Brend : Podrum Erdevik      Berba : 2019

«Tip vina» закрывает ту дыру, ради которой затевался поиск сладости:
отличить сухое от полусладкого по нашим источникам было нечем. «Zemlja»
отсекает чужие вина, «Brend» даёт хозяйство, «Berba» — урожай.

Берётся в два шага: список категории даёт адреса карточек, карточка —
цену и свойства. Цены в списке нет, поэтому по карточкам ходить
приходится, и это около пятисот запросов.

Пишет `cerpromet-ceny.json`. Кеш — в `kesh-cerpromet/`.
"""
import argparse, html, json, pathlib, re, time, urllib.parse, urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-cerpromet"
SAJT = "https://cerpromet.com"
RAZDEL = SAJT + "/kategorija/vino"
PAUZA = 1.2
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
TOVAR = re.compile(r'href="(/proizvod/[^"#?]+)"')


def vzjat(adres, imya):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    # В адресах карточек попадаются сербские буквы («…_kovačevic»),
    # и без обычного кодирования пути запрос падает на ascii.
    razobrano = urllib.parse.urlsplit(adres)
    adres = urllib.parse.urlunsplit(razobrano._replace(
        path=urllib.parse.quote(razobrano.path)))
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    with urllib.request.urlopen(zapros, timeout=90) as otvet:
        tekst = otvet.read().decode("utf-8", "replace")
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def tovar_iz_kartochki(stranica, put):
    """Цена — из `ld+json`, свойства — из таблицы под описанием."""
    tovar = {}
    for kus in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>',
                           stranica, re.S):
        try:
            d = json.loads(kus.group(1))
        except ValueError:
            continue
        if isinstance(d, dict) and d.get("@type") == "Product":
            predlozhenie = d.get("offers") or {}
            if isinstance(predlozhenie, list):
                predlozhenie = predlozhenie[0] if predlozhenie else {}
            tovar = {"vino": html.unescape(d.get("name") or ""),
                     "cena_rsd": predlozhenie.get("price"),
                     "valyuta": predlozhenie.get("priceCurrency"),
                     "opisanie": d.get("description") or ""}
            break
    if not tovar:
        return None
    # Свойства стоят таблицей, где каждое слово — свой узел разметки.
    # Поэтому теги заменяются разделителем, и значение читается как
    # «Поле | : | … | значение |»: без разделителя «Severna Makedonija»
    # обрезалась до «Severna», а сорт и урожай не находились вовсе.
    tekst = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", stranica))
    for pole, imya in (("Zemlja", "strana"), ("Sorta", "sorta"),
                       ("Tip vina", "tip_vina"), ("Alkohol", "alkohol"),
                       ("Brend", "hozyaistvo"), ("Berba", "urozhaj")):
        sovpalo = re.search(re.escape(pole) + r"\s*\|\s*:\s*(?:\|\s*)+([^|]{1,60}?)\s*\|",
                            tekst)
        tovar[imya] = html.unescape(sovpalo.group(1).strip()) if sovpalo else ""
    tovar["stranica"] = SAJT + put
    return tovar


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--stranic", type=int, default=60)
    kljuchi = razbor.parse_args()

    adresa = []
    for nomer in range(1, kljuchi.stranic + 1):
        adres = RAZDEL if nomer == 1 else "%s?page=%d" % (RAZDEL, nomer)
        stranica = vzjat(adres, "spisok-%d.html" % nomer)
        svoi = [p for p in dict.fromkeys(TOVAR.findall(stranica))]
        novyh = [p for p in svoi if p not in adresa]
        adresa.extend(novyh)
        print("  список %2d: карточек %2d, новых %2d" % (nomer, len(svoi), len(novyh)))
        if not novyh:
            break
    print("всего карточек: %d\n" % len(adresa))

    vina, bez_ceny = [], 0
    for nomer, put in enumerate(adresa, 1):
        imya = "tovar-" + re.sub(r"[^a-z0-9]+", "-", put.lower()).strip("-") + ".html"
        try:
            tovar = tovar_iz_kartochki(vzjat(SAJT + put, imya), put)
        except Exception as oshibka:
            print("   %s — не взялось: %s" % (put, str(oshibka)[:50]))
            continue
        if not tovar:
            continue
        if not tovar.get("cena_rsd"):
            bez_ceny += 1
        vina.append(tovar)
        if nomer % 50 == 0:
            print("   карточек разобрано %d из %d" % (nomer, len(adresa)))

    serbskie = sum(1 for z in vina if (z.get("strana") or "").lower().startswith("srbij"))
    (ZDES / "cerpromet-ceny.json").write_text(json.dumps({
        "chto_eto": "Вина у «Cerpromet»: цена в динарах, страна, сорт, тип вина "
                    "(суво/полусуво/слатко), крепость, хозяйство, урожай.",
        "istochnik": RAZDEL,
        "sobrano": time.strftime("%Y-%m-%d"),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d вин, без цены %d, сербских %d → cerpromet-ceny.json"
          % (len(vina), bez_ceny, serbskie))


if __name__ == "__main__":
    main()
