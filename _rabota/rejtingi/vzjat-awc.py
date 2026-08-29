# -*- coding: utf-8 -*-
"""AWC Vienna: сербские вина.

Австрийский конкурс, крупнейший из признанных OIV: около десяти тысяч вин
в год. База открыта и лежит отдельно от сайта конкурса — на
awc-online.awc-vienna.at; сайт `awc-vienna.at/en/results` отвечает 404,
и из-за этого источник был записан в закрытые.

Фильтра по стране у поиска нет, а каждый запрос обрезан сотней записей
(`max_wine_results` в настройках года). Поэтому обход идёт по категориям:
их около сорока в год, и в каждой берётся её сотня — то есть лучшие по
баллу. Сербские строки выбираются из выдачи по полю страны.

Обрезка честная и её надо помнить: в большой категории сербское вино
может не попасть в сотню лучших. Зато AWC и так публикует только вина
от 84 баллов, так что теряется низ, а не верх.

У AWC есть и балл (с десятой долей, «88,9»), и медаль, поэтому строка
даёт и оценку, и награду.

    python3 _rabota/rejtingi/vzjat-awc.py

Пишет `awc-zapisi.json`, ответы кладёт в `kesh-awc/`.
"""
import json, os, re, html, time, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-awc")
POISK = "https://awc-online.awc-vienna.at/search/wine"
ITOG = POISK + "/result?year=%d&categoryId=%s&page=%d"
STRANA = "Serbia"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


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
    time.sleep(1.0)
    return tekst


def svojstva(stranica):
    """Состояние страницы: приложение отдаёт его в атрибуте data-page."""
    sovpalo = re.search(r'data-page="([^"]+)"', stranica)
    if not sovpalo:
        return {}
    return json.loads(html.unescape(sovpalo.group(1))).get("props", {})


def ball(stroka):
    """«88,9» → 88.9. Запятая у них десятичная, а не разделитель."""
    if not stroka:
        return None
    try:
        return float(str(stroka).replace(",", "."))
    except ValueError:
        return None


def main():
    nachalo = svojstva(vzjat(POISK, "poisk.html"))
    gody = [g["year"] for g in nachalo.get("years", [])]
    print("годы:", gody)

    vse, po_godam, obrezano = [], {}, []
    for god in gody:
        # Список категорий у каждого года свой.
        svoi = svojstva(vzjat(POISK + "?year=%d" % god, "poisk-%d.html" % god))
        kategorii = svoi.get("categories") or nachalo.get("categories") or {}
        za_god = []
        # По категориям листается только текущий год: для прошлых лет
        # запрос с их номером возвращает пусто, а отдаётся лишь общий
        # список — полсотни-сотня лучших. Поэтому «все категории» берём
        # всегда, а разбивку — сколько дадут.
        for kod, imya_kategorii in kategorii.items():
            stranica_nomer, vsego = 1, None
            while True:
                svojstva_stranicy = svojstva(vzjat(
                    ITOG % (god, kod, stranica_nomer),
                    "awc-%d-%s-%d.html" % (god, kod, stranica_nomer)))
                spisok = (svojstva_stranicy.get("items") or {})
                zapisi = spisok.get("data") or []
                vsego = spisok.get("total")
                for z in zapisi:
                    if (z.get("c_name_en") or "") != STRANA:
                        continue
                    za_god.append({
                        "god": god,
                        "kategoriya": imya_kategorii,
                        "nomer": z.get("w_id"),
                        "hozyaistvo": (z.get("winery_company") or "").strip(),
                        "vino": (z.get("w_bezeichnung") or "").strip(),
                        # 9999 у них значит «без урожая».
                        "urozhaj": (z.get("w_jahrgang")
                                    if z.get("w_jahrgang") not in (None, 9999)
                                    else None),
                        "ball": ball(z.get("w_ergebnis")),
                        "medal": (z.get("medal") or "").strip() or None,
                        "trofej": bool(z.get("w_trophyWinner")),
                        "stranica": "awc-online.awc-vienna.at/wine/%s" % z.get("w_id"),
                    })
                if stranica_nomer >= (spisok.get("last_page") or 1):
                    break
                stranica_nomer += 1
            if vsego and vsego >= 100:
                obrezano.append({"god": god, "kategoriya": imya_kategorii})
            if kod == "0" and vsego:
                po_godam.setdefault("otdano_vsego", {})[god] = vsego
        po_godam[god] = len(za_god)   # уже с учётом «всех категорий»
        print("  AWC %d: %d сербских" % (god, len(za_god)))
        vse += za_god

    # Одно вино попадает и в свою категорию, и в общий список.
    vidano, bez_povtorov = set(), []
    for z in vse:
        if z["nomer"] in vidano:
            continue
        vidano.add(z["nomer"])
        bez_povtorov.append(z)

    # У AWC две дегустации в году, зимняя и летняя, и одно вино может
    # пройти обе — тогда номера разные, а вино то же и балл другой.
    # Оставляем один, больший, а расхождение записываем.
    po_klyuchu, poryadok, raznoglasiya = {}, [], []
    for z in bez_povtorov:
        klyuch = (z["hozyaistvo"].lower(), z["vino"].lower(), z["urozhaj"], z["god"])
        bylo = po_klyuchu.get(klyuch)
        if bylo is None:
            po_klyuchu[klyuch] = z
            poryadok.append(klyuch)
            continue
        if bylo["ball"] != z["ball"]:
            raznoglasiya.append({
                "god": z["god"], "hozyaistvo": z["hozyaistvo"], "vino": z["vino"],
                "urozhaj": z["urozhaj"],
                "bally": sorted({bylo["ball"], z["ball"]}),
                "vzyato": max(bylo["ball"], z["ball"])})
        if (z["ball"] or 0) > (bylo["ball"] or 0):
            po_klyuchu[klyuch] = z
    itog = [po_klyuchu[k] for k in poryadok]

    json.dump({
        "chto_eto": "Сербские вина AWC Vienna. У конкурса есть и балл, и медаль.",
        "istochnik": POISK,
        "kak_sobrano": "Фильтра по стране нет, выдача обрезана сотней записей "
                       "на категорию; обход идёт по категориям каждого года.",
        "obrezannyh_kategorij": len(obrezano),
        "raznoglasiya": raznoglasiya,
        "po_godam": po_godam,
        "vsego": len(itog),
        "zapisi": itog,
    }, open(put("awc-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего сербских вин: %d (категорий с обрезкой: %d) → awc-zapisi.json"
          % (len(itog), len(obrezano)))


if __name__ == "__main__":
    main()
