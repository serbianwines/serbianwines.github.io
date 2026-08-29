# -*- coding: utf-8 -*-
"""Balkans International Wine Competition: сербские вина.

Софийский конкурс, судят вслепую; результаты на сайте выложены с 2014
года. Для Сербии это самый близкий крупный конкурс, и по охвату он
сопоставим с Decanter: около сотни сербских вин в год.

Отдаёт и балл, и медаль. Таблица результатов — до восьми колонок: цвет,
страна, сорта, хозяйство, имя вина, урожай, балл по стобалльной шкале,
медаль. Поэтому каждая строка даёт две записи: оценку в дорожку критиков
и медаль в дорожку наград.

Сверх медалей есть трофеи: «Grand Trophy», «Best of Show Serbia», «Trophy
Dry White Wine». Трофей стоит выше медали, шкалы у него нет, и одно вино
берёт трофей и медаль сразу — поэтому трофей живёт отдельной записью,
а не полем при медали. Собирает их `trofei()`, отдельно от таблиц.

Страницы лежат обычной разметкой, без сценариев, по двум адресам сразу:
болгарскому `резултати-<год>` и английскому `results-<год>`. Английский
заведён не на все года, и там, где его нет, отдаётся пустая страница
без всякой ошибки, — поэтому адрес выбирается по наличию таблиц.

    python3 _rabota/rejtingi/vzjat-biwc.py

Пишет `biwc-zapisi.json`, страницы кладёт в `kesh-biwc/`.
"""
import json, os, re, html, time, unicodedata, urllib.error, urllib.request
from urllib.parse import quote

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-biwc")
STRANICA = "https://balkanswine.eu/competition/results-%d/"
# Сайт болгарский, и основной адрес результатов тоже: «резултати-<год>».
# Английский слуг заведён не на все года — 2015 и 2016 по нему отдают
# страницу с одним меню, без единой таблицы, и молча давали ноль вин.
# Поэтому адреса пробуются по очереди: годится тот, где таблицы есть.
# Адрес собирается сложением, а не подстановкой: в percent-кодировке
# кириллицы полно знаков «%», и форматирование на них спотыкается.
ZAPASNAYA = lambda god: ("https://balkanswine.eu/"
                         + quote("резултати") + "-%d/" % god)
# Результаты на сайте выложены с 2014 года: за 2013-й страницы нет
# ни по одному из двух адресов, и в меню сайта её тоже нет.
GODY = range(2014, 2027)
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
STRANA = "serbia"


def stranica_goda(god):
    """Страница результатов года — по тому адресу, где есть таблицы."""
    poslednyaya = ""
    for nomer, adres in enumerate((STRANICA % god, ZAPASNAYA(god))):
        imya = "biwc-%d%s.html" % (god, "" if not nomer else "-bg")
        try:
            tekst = vzjat(adres, imya)
        except urllib.error.HTTPError as beda:
            print("  %d: HTTP %s" % (god, beda.code))
            continue
        if "<tr" in tekst:
            return tekst
        poslednyaya = tekst
    return poslednyaya


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
# Трофей — высшая награда конкурса, отдельная от медали: «Grand Trophy»,
# «Best of Show Serbia», «Trophy Dry White Wine». Одно и то же вино берёт
# и медаль, и трофей, поэтому трофей — не поле при медали, а своя запись.
TROFEJ = re.compile(r"(^|\s)(trophy|best of show|best winery)", re.I)
# Хозяйство в свободной строке узнаётся по слову при имени.
SLOVO_HOZYAISTVA = re.compile(
    r"\b(winery|wineries|vinarija|vinarijа|cellar|podrum|estate|wines|"
    r"chateau|salaš|salas|doo|d\.o\.o|atelje|vinarium)\b", re.I)
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


SLUZHEBNOE = re.compile(r"\b(vinarija|winery|wineries|podrum|wines|doo|"
                        r"d o o|ad|pik|pr)\b")


def gladko(s):
    """Имя без диакритики, регистра и служебных слов — только для сравнения.

    В самих записях остаётся то написание, какое дал конкурс: сглаженное
    имя нужно, чтобы узнать одно вино в двух написаниях, а не заменить их.
    """
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(z for z in s if unicodedata.category(z) != "Mn")
    s = SLUZHEBNOE.sub(" ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def imya_vina(hozyaistvo, vino):
    """Имя вина без имени хозяйства внутри него.

    BIWC 2026 печатает один и тот же каберне Радловића дважды: «Radlovic ·
    Cabernet Sauvignon» с баллом 92 и «Vinarija Radlović doo · Radlovic
    Cabernet Sauvignon» с баллом 89. Это одно вино, названное по-разному,
    и без такого сглаживания оно расходится на две записи с разным баллом.
    """
    h, v = gladko(hozyaistvo), gladko(vino)
    if h:
        v = re.sub(r"\b%s\b" % re.escape(h), " ", v).strip() or v
    return re.sub(r"\s+", " ", v)


def razobrat_ryad(yachejki, nomer, god):
    """Одна строка таблицы: ячейки читаются по виду, а не по месту.

    Раскладка год от года разная — колонок от пяти до восьми, цвет стоит
    то до страны, то после имени вина, балл и медаль местами меняются.
    Поэтому сначала из строки вынимается всё, что узнаётся само собой:
    медаль, балл, урожай, цвет. Оставшееся читается по порядку: сорта,
    хозяйство, вино. Строку победителя трофея разбирает та же функция —
    таблица там та же самая.
    """
    cvet = ""
    if nomer and yachejki[nomer - 1].lower().strip() in CVETA:
        cvet = yachejki[nomer - 1].lower().strip()
    ostalos = [y for y in yachejki[nomer + 1:] if y]
    # Где в строке стоит цвет — тем и различаются две раскладки. В 2015-м
    # порядок «страна, хозяйство, цвет, сорта, вино»: хозяйство сразу за
    # страной, а сорта — после цвета. В остальных годах сорта стоят перед
    # хозяйством, и тогда хозяйство берётся с конца, предпоследним.
    # Без этого различения хозяйством у всего 2015 года становился сорт:
    # «Cabernet Sauvignon 100%» вместо «Matalj winery».
    hozyaistvo_vperedi = next(
        (i for i, y in enumerate(ostalos) if y.lower().strip() in CVETA),
        None) == 1

    medal = snyat(ostalos, lambda y: y.lower().strip() in MEDALI)
    ball = snyat(ostalos, lambda y: re.match(r"^\d{2,3}([.,]\d+)?$", y.strip())
                 and 50 <= float(y.strip().replace(",", ".")) <= 100)
    # Год пишут и «2019», и «2019.»; вино без урожая — «NV» или «/».
    urozhaj = snyat(ostalos, lambda y: re.match(r"^(19|20)\d{2}\.?$", y.strip()))
    snyat(ostalos, lambda y: y.lower().strip() in BEZ_UROZHAYA)
    cvet_v_stroke = snyat(ostalos, lambda y: y.lower().strip() in CVETA)

    hozyaistvo = ostalos.pop(0).strip() if hozyaistvo_vperedi and ostalos else ""
    vino = ostalos.pop().strip() if ostalos else ""
    if not hozyaistvo:
        hozyaistvo = ostalos.pop().strip() if ostalos else ""
    if not hozyaistvo or not vino:
        return None
    return {
        "god": god,
        "cvet": cvet or (cvet_v_stroke or "").lower().strip(),
        "sorta": " ".join(ostalos).strip(),
        "hozyaistvo": hozyaistvo,
        "vino": vino,
        "urozhaj": int(urozhaj.strip().rstrip(".")) if urozhaj else None,
        "ball": int(float(ball.replace(",", "."))) if ball else None,
        "medal": (medal or "").lower().strip() or None,
        "stranica": "balkanswine.eu/competition/results-%d/" % god,
    }


def razobrat(stranica, god):
    """Сербские строки таблиц результатов.

    До 2021 года балла в таблице не было вовсе, а медаль стояла
    заголовком раздела — то строкой таблицы («GOLD MEDALS»), то <h3> над
    отдельной таблицей. Поэтому раздел приходится вести отдельно от строк.
    Сами ячейки разбирает razobrat_ryad: не по месту, а по виду.
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

        zapis = razobrat_ryad(yachejki, nomer, god)
        if zapis is None:
            continue
        zapisi.append(dict(zapis, **{
            "medal": (zapis["medal"] or medal_razdela or "").lower().strip()
                     or None,
            # Имя трофея здесь не хранится. Раньше хранилось — и терялось:
            # строка под заголовком «Grand Trophy» несёт и медаль, поэтому
            # условие «если нет медали» стирало трофей у всех, кто взял
            # обе награды сразу, а сведение по вину оставляло из двух
            # трофеев один. Трофеи собираются отдельно, функцией trofei().
            "kategoriya": "",
        }))
    # Одно и то же вино в таблице встречается дважды: в общем списке
    # и ещё раз в блоке трофеев. Написание при этом гуляет («MV Tamjanika
    # Hope» и «MV Tamjanika HOPE»), поэтому сводим по ключу без регистра.
    # Изредка два таких вхождения расходятся в балле — у Радловића
    # каберне 2020 года стоит и 92, и 89. Такое не выбрасывается молча:
    # запись остаётся одна, а расхождение записывается отдельно.
    po_klyuchu, poryadok, raznoglasiya = {}, [], []
    for z in zapisi:
        klyuch = (gladko(z["hozyaistvo"]), imya_vina(z["hozyaistvo"], z["vino"]),
                  z["urozhaj"])
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


def razobrat_svobodnuyu(stroka, god, imya_trofeya):
    """Строку-трофей, написанную прозой, а не колонками.

    В 2021 и 2022 годах победителей трофеев печатали одной ячейкой:

        Pinoranž, 2019, Vinarium winery, Serbia
        Vincic White Reserve 2012, Vinarija Vincic
        Serbia – Vinarija Ralevic, Virgo Sauvignon Blanc 2021

    Страна стоит то последней частью, то первой через тире, то не стоит
    вовсе — тогда её называет сам заголовок («Best of Show Serbia»).
    Хозяйство узнаётся по слову при имени, урожай — по четырём цифрам.
    Разбор возвращает и исходную строку: если он ошибся в разделении
    хозяйства и вина, это видно, а не спрятано.
    """
    tekst = stroka.replace("—", "–").strip()
    serbskaya = imya_trofeya.lower().rstrip(".").endswith("serbia")
    chasti = [c.strip(" .") for c in re.split(r"[,–]", tekst) if c.strip(" .")]
    ostalos = []
    for c in chasti:
        if c.lower() == "serbia":
            serbskaya = True
        else:
            ostalos.append(c)
    if not serbskaya or not ostalos:
        return None
    hozyaistvo = next((c for c in ostalos if SLOVO_HOZYAISTVA.search(c)), None)
    if hozyaistvo is None:
        hozyaistvo = ostalos[-1]
    ostalos = [c for c in ostalos if c is not hozyaistvo]
    urozhaj = None
    for i, c in enumerate(ostalos):
        god_v_chasti = re.search(r"\b(19|20)\d{2}\b", c)
        if god_v_chasti:
            urozhaj = int(god_v_chasti.group(0))
            ostalos[i] = c[:god_v_chasti.start()] + c[god_v_chasti.end():]
            break
    vino = " ".join(c.strip(" ,.") for c in ostalos if c.strip(" ,."))
    return {
        "god": god,
        "kategoriya": imya_trofeya,
        "hozyaistvo": hozyaistvo.strip(),
        "vino": vino.strip(),
        "urozhaj": urozhaj,
        "cvet": "",
        "ball": None,
        "stroka": stroka,
        "stranica": "balkanswine.eu/competition/results-%d/" % god,
    }


def trofei(stranica, god):
    """Трофеи конкурса: заголовок трофея и строка победителя под ним.

    Трофей стоит выше медали: «Grand Trophy Best Wine in the Balkans»,
    «Best of Show Serbia», «Trophy Dry White Wine». Раньше эти строки
    в сбор не попадали: в одни годы у них нет колонки страны, и разбор
    медальных таблиц отбрасывал их молча — вместе с двумя сербскими
    гран-при, 2020 и 2024 годов.

    Заголовок — короткая строка в одну-две ячейки; победитель — первая
    непустая строка после него. Победитель бывает и колонками, как в
    медальной таблице, и прозой в одну ячейку.
    """
    # Заголовок трофея бывает и строкой таблицы, и <h3> над ней: до 2020
    # года — только <h3>. Поэтому идём по документу, а не по таблицам.
    ryady = []
    for kusok in KUSOK.finditer(stranica):
        if kusok.group("zagolovok") is not None:
            imya = chisto(kusok.group("zagolovok"))
            ryady.append([imya] if imya else [])
        else:
            ya = [chisto(y) for y in YACHEJKA.findall(kusok.group("ryad"))]
            ryady.append([y for y in ya if y])

    najdeno = []
    for i, ryad in enumerate(ryady):
        if not ryad or len(ryad) > 2:
            continue
        imya = " ".join(ryad).strip()
        if not TROFEJ.search(imya) or len(imya) > 70:
            continue
        pobeditel = next((r for j, r in enumerate(ryady[i + 1:i + 4])
                          if r and not (len(r) <= 2
                                        and TROFEJ.search(" ".join(r)))), None)
        if not pobeditel:
            continue
        if len(pobeditel) >= 4:
            nomer = next((k for k, y in enumerate(pobeditel)
                          if y.lower().strip() == STRANA), None)
            if nomer is None:
                continue
            zapis = razobrat_ryad(pobeditel, nomer, god)
            if zapis is None:
                continue
            zapis["kategoriya"] = imya
            zapis["stroka"] = " | ".join(pobeditel)
            zapis.pop("sorta", None)
            zapis.pop("medal", None)
            najdeno.append(zapis)
        else:
            zapis = razobrat_svobodnuyu(" ".join(pobeditel), god, imya)
            if zapis:
                najdeno.append(zapis)

    # Один и тот же трофей печатают дважды — в сводке наверху и в разделе.
    po_klyuchu = {}
    for z in najdeno:
        po_klyuchu.setdefault(
            (z["kategoriya"].lower(), z["hozyaistvo"].lower(),
             z["vino"].lower(), z["urozhaj"]), z)
    return list(po_klyuchu.values())


def main():
    vse, po_godam, raznoglasiya, vse_trofei = [], {}, [], []
    for god in GODY:
        stranica = stranica_goda(god)
        if not stranica:
            continue
        najdeno, spory = razobrat(stranica, god)
        raznoglasiya += spory
        vzyato = trofei(stranica, god)
        if najdeno or vzyato:
            po_godam[god] = len(najdeno)
            print("  BIWC %d: %d вин, трофеев %d" % (god, len(najdeno),
                                                     len(vzyato)))
        vse += najdeno
        vse_trofei += vzyato
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
        "trofeev": len(vse_trofei),
        "raznoglasiya": raznoglasiya,
        "trofei": vse_trofei,
        "zapisi": vse,
    }, open(put("biwc-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего %d, с баллом %d, с медалью %d, трофеев %d → biwc-zapisi.json"
          % (len(vse), len(s_ballom), len(s_medalyu), len(vse_trofei)))
    for z in vse_trofei:
        print("   %s  %-38s %s · %s %s" % (
            z["god"], z["kategoriya"][:38], z["hozyaistvo"], z["vino"],
            z["urozhaj"] or ""))


if __name__ == "__main__":
    main()
