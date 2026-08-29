# -*- coding: utf-8 -*-
"""Balkans International Wine Competition: сербские вина.

Софийский конкурс, с 2013 года, судят вслепую. Для Сербии это самый
близкий крупный конкурс, и по охвату он сопоставим с Decanter: около сотни
сербских вин в год.

Отдаёт и балл, и медаль. Таблица результатов — восемь колонок: цвет,
страна, сорта, хозяйство, имя вина, урожай, балл по стобалльной шкале,
медаль. Поэтому каждая строка даёт две записи: оценку в дорожку критиков
и медаль в дорожку наград.

Страницы лежат по адресу `balkanswine.eu/competition/results-<год>/`
обычной разметкой, без сценариев.

    python3 _rabota/rejtingi/vzjat-biwc.py

Пишет `biwc-zapisi.json`, страницы кладёт в `kesh-biwc/`.
"""
import json, os, re, html, time, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-biwc")
STRANICA = "https://balkanswine.eu/competition/results-%d/"
GODY = range(2013, 2027)
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
STRANA = "serbia"


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
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


MEDALI = ("platinum", "double gold", "grand gold", "gold", "silver",
          "bronze")
# Цвет и стиль стоят отдельной колонкой и мешают найти имя вина.
# Пишут их по-разному: «semi dry», «semi-dry», «Special / Organic».
CVETA = ("white", "red", "rose", "rosé", "sparkling", "dessert", "orange",
         "special", "sweet", "semi dry", "semi-dry", "semidry", "semi sweet",
         "semi-sweet", "semisweet", "fortified", "organic", "natural",
         "biodynamic", "still", "special / organic")
# «NV» — вино без урожая, а не имя. Такие ячейки надо снять, иначе они
# сдвигают всю строку и хозяйством становится название вина.
BEZ_UROZHAYA = ("nv", "n/v", "n.v.", "/", "-", "—")
# Заголовок раздела: «GOLD MEDALS» в одних годах, просто «Gold» в других.
ZAGOLOVOK_MEDALI = re.compile(
    r"^(platinum|double\s+gold|grand\s+gold|gold|silver|bronze)"
    r"(\s+medals?)?$", re.I)
# Строки таблиц и заголовки — в порядке появления: медаль в старых годах
# стоит заголовком <h3> над своей таблицей, а не колонкой в строке.
KUSOK = re.compile(r"<tr[^>]*>(?P<ryad>.*?)</tr>"
                   r"|<h[1-4][^>]*>(?P<zagolovok>.*?)</h[1-4]>", re.S)
YACHEJKA = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)


def chisto(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def snyat(yachejki, podhodit, ostavit=2):
    """Снять первую подходящую ячейку, если после этого хватит остальных."""
    for i, y in enumerate(yachejki):
        if podhodit(y) and len(yachejki) > ostavit:
            return yachejki.pop(i)
    return None


def razobrat(stranica, god):
    """Сербские строки таблиц результатов.

    Раскладка год от года разная: колонок от пяти до восьми, цвет стоит
    то до страны, то после имени вина, а балл и медаль местами меняются
    друг с другом. До 2021 года балла в таблице не было вовсе, а медаль
    стояла заголовком раздела — то строкой таблицы («GOLD MEDALS»),
    то <h3> над отдельной таблицей.

    Поэтому ячейки разбираются не по месту, а по виду: сначала из строки
    вынимаются медаль, балл, урожай и цвет — каждый узнаётся по себе, —
    а то, что осталось, читается по порядку: сорта, хозяйство, вино.
    """
    zapisi = []
    medal_razdela, razdel = None, ""
    for kusok in KUSOK.finditer(stranica):
        if kusok.group("zagolovok") is not None:
            imya = chisto(kusok.group("zagolovok"))
            if ZAGOLOVOK_MEDALI.match(imya):
                medal_razdela = re.sub(r"\s+medals?$", "", imya,
                                       flags=re.I).lower().strip()
            elif imya:
                medal_razdela = None      # «Best Winery», «Trophy» и прочее
                razdel = imya
            continue

        yachejki = [chisto(y) for y in YACHEJKA.findall(kusok.group("ryad"))]
        zapolneno = [y for y in yachejki if y]
        if len(zapolneno) == 1 and ZAGOLOVOK_MEDALI.match(zapolneno[0]):
            medal_razdela = re.sub(r"\s+medals?$", "", zapolneno[0],
                                   flags=re.I).lower().strip()
            razdel = zapolneno[0]
            continue
        if len(zapolneno) == 1:
            razdel = zapolneno[0]
        nomer = next((i for i, y in enumerate(yachejki)
                      if y.lower().strip() == STRANA), None)
        if nomer is None:
            continue

        cvet = ""
        if nomer and yachejki[nomer - 1].lower().strip() in CVETA:
            cvet = yachejki[nomer - 1].lower().strip()
        ostalos = [y for y in yachejki[nomer + 1:] if y]

        medal = snyat(ostalos, lambda y: y.lower().strip() in MEDALI)
        ball = snyat(ostalos, lambda y: re.match(r"^\d{2,3}([.,]\d+)?$", y.strip())
                     and 50 <= float(y.strip().replace(",", ".")) <= 100)
        # Год пишут и «2019», и «2019.»; вино без урожая — «NV» или «/».
        urozhaj = snyat(ostalos, lambda y: re.match(r"^(19|20)\d{2}\.?$", y.strip()))
        snyat(ostalos, lambda y: y.lower().strip() in BEZ_UROZHAYA)
        cvet_v_stroke = snyat(ostalos, lambda y: y.lower().strip() in CVETA)

        vino = ostalos.pop().strip() if ostalos else ""
        hozyaistvo = ostalos.pop().strip() if ostalos else ""
        if not hozyaistvo or not vino:
            continue
        zapisi.append({
            "god": god,
            "cvet": cvet or (cvet_v_stroke or "").lower().strip(),
            "sorta": " ".join(ostalos).strip(),
            "hozyaistvo": hozyaistvo,
            "vino": vino,
            "urozhaj": int(urozhaj.strip().rstrip(".")) if urozhaj else None,
            "ball": int(float(ball.replace(",", "."))) if ball else None,
            "medal": (medal or medal_razdela or "").lower().strip() or None,
            # Трофеи медали не имеют, зато имеют название: «Best of Show
            # Serbia», «White Wine Trophy». Это тоже награда, просто другая.
            "kategoriya": razdel if not (medal or medal_razdela) else "",
            "stranica": "balkanswine.eu/competition/results-%d/" % god,
        })
    # Одно и то же вино в таблице встречается дважды: в общем списке
    # и ещё раз в блоке трофеев. Написание при этом гуляет («MV Tamjanika
    # Hope» и «MV Tamjanika HOPE»), поэтому сводим по ключу без регистра.
    # Изредка два таких вхождения расходятся в балле — у Радловића
    # каберне 2020 года стоит и 92, и 89. Такое не выбрасывается молча:
    # запись остаётся одна, а расхождение записывается отдельно.
    po_klyuchu, poryadok, raznoglasiya = {}, [], []
    for z in zapisi:
        klyuch = (z["hozyaistvo"].lower(), z["vino"].lower(), z["urozhaj"])
        bylo = po_klyuchu.get(klyuch)
        if bylo is None:
            po_klyuchu[klyuch] = z
            poryadok.append(klyuch)
            continue
        if bylo["ball"] != z["ball"] and None not in (bylo["ball"], z["ball"]):
            raznoglasiya.append({
                "god": z["god"], "hozyaistvo": z["hozyaistvo"],
                "vino": z["vino"], "urozhaj": z["urozhaj"],
                "bally": sorted({bylo["ball"], z["ball"]}),
                "vzyato": max(bylo["ball"], z["ball"]),
            })
            if z["ball"] > bylo["ball"]:
                po_klyuchu[klyuch] = z
        elif z["ball"] is not None and bylo["ball"] is None:
            po_klyuchu[klyuch] = z
        elif z["medal"] and not bylo["medal"]:
            bylo["medal"] = z["medal"]
    return [po_klyuchu[k] for k in poryadok], raznoglasiya


def main():
    vse, po_godam, raznoglasiya = [], {}, []
    for god in GODY:
        try:
            stranica = vzjat(STRANICA % god, "biwc-%d.html" % god)
        except urllib.error.HTTPError as beda:
            print("  %d: HTTP %s" % (god, beda.code))
            continue
        najdeno, spory = razobrat(stranica, god)
        raznoglasiya += spory
        if najdeno:
            po_godam[god] = len(najdeno)
            print("  BIWC %d: %d" % (god, len(najdeno)))
        vse += najdeno
    s_ballom = [z for z in vse if z["ball"] is not None]
    s_medalyu = [z for z in vse if z["medal"]]
    json.dump({
        "chto_eto": "Сербские вина на Balkans International Wine Competition. "
                    "У конкурса есть и балл по стобалльной шкале, и медаль, "
                    "поэтому строка даёт и оценку, и награду.",
        "istochnik": "balkanswine.eu",
        "po_godam": po_godam,
        "vsego": len(vse),
        "s_ballom": len(s_ballom),
        "s_medalyu": len(s_medalyu),
        "raznoglasiya": raznoglasiya,
        "zapisi": vse,
    }, open(put("biwc-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего %d, с баллом %d, с медалью %d → biwc-zapisi.json"
          % (len(vse), len(s_ballom), len(s_medalyu)))


if __name__ == "__main__":
    main()
