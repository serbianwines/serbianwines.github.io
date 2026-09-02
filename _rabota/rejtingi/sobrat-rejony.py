#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проставить хозяйствам настоящий рејон и виногорје.

Не главу книги, а действующее сербское деление: 3 региона, 22 рејона,
77 виногорја (`rejony-vinogorja.json`). Главы книги — отдельная величина,
они могут не совпадать с рејонима и, возможно, будут править́ся; поэтому
здесь они не участвуют вовсе.

Показания берутся из того, что отдали сами источники:

    Decanter          region + subRegion — самое подробное, есть и виногорје
    Vivino            region — плоский список, до виногорја не доходит
    Falstaff          область в примечании к записи
    vinarijesrbije    справочник винарий с рејоном и городом
    книга             город хозяйства (`gde` в raion-hozyaistv.json)

Каждое показание переводится в официальное имя таблицей ниже. Таблица
явная: сокращать её догадками нельзя, потому что часть имён у источников
осталась от старой рејонизације, где рејонов было девять, и одно старое
имя покрывает несколько нынешних. Такие случаи помечаются как
неоднозначные и рејон по ним не ставится.

    python3 _rabota/rejtingi/sobrat-rejony.py
"""

import collections
import glob
import json
import os
import re
import sys
import unicodedata

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))


def put(imya):
    return os.path.join(RYADOM, imya)


# ---------------------------------------------------------------- перевод
# Слева — как пишет источник, справа — официальное имя рејона.
# `None` значит «имя есть, но рејон по нему не определяется»: либо это
# уровень региона, либо имя из старой рејонизације, покрывающее несколько
# нынешних рејонов. Пустая строка в таблице — ошибка, все случаи названы.
VIVINO_REJON = {
    "Srem": "Sremski rejon",
    "Fruška Gora": "Sremski rejon",
    "Subotica-Horgos": "Subotički rejon",
    "Bačka": "Rejon Bačka",
    "Potisje": "Potiski rejon",
    "Tri Morave": "Rejon Tri Morave",
    "Negotinska Krajina": "Rejon Negotinska Krajina",
    "Toplica": "Toplički rejon",
    "Knjaževac": "Knjaževački rejon",
    "Niš": "Niški rejon",
    "Leskovac": "Leskovački rejon",
    "Vranje": "Vranjski rejon",
    "Pirot": "Nišavski rejon",
    "Pocerina": "Pocersko Valjevski Rejon",
    "Čačak-Kraljevo": "Čačansko–kraljevački rejon",
    # Ниже — имена, по которым рејон не ставится.
    "Banat": None,               # у Vivino один Банат на Банатски и Јужнобанатски
    "Timočka Krajina": None,     # Неготинска Крајина плюс Књажевачки
    "Nisava-South Morava": None, # старый большой рејон: Нишки, Нишавски, Лесковачки, Врањски, Топлички
    "Šumadija-Great Morava": None,  # старый: Шумадијски, Београдски, Млавски, Три Мораве
    "West Morava": None,         # Чачанско-краљевачки или Три Мораве
    "Morava": None,
    "Central Serbia": None,      # уровень региона
    "Vojvodina": None,           # уровень региона
    "Metohija": None,            # два метохијска рејона
    "Wine of Serbia": None,      # свалка
}

# У Decanter два поля, и пара «рејон + подрејон» часто указывает точнее,
# чем каждое поле по отдельности. Ключ — пара, значение — рејон и
# виногорје (виногорје может отсутствовать).
DECANTER_PARA = {
    ("Srem", "Fruška Gora"): ("Sremski rejon", "Fruškogorsko vinogorje"),
    ("Srem", None): ("Sremski rejon", None),
    ("Subotica-Horgoš", "Riđičko-Vinogorje"): ("Subotički rejon", "Riđičko vinogorje"),
    ("Subotica-Horgoš", None): ("Subotički rejon", None),
    ("Subotica-Horgoš", "Fruška Gora"): (None, None),  # у них же ошибка ввода
    ("Vojvodina", "Subotica"): ("Subotički rejon", None),
    ("Vojvodina", None): (None, None),
    ("Banat", "North Banat"): ("Banatski rejon", None),
    ("Banat", "South Banat"): ("Južnobanatski rejon", None),
    ("Šumadija-Great Morava", "Oplenac"): ("Šumadijski rejon", "Oplenačko vinogorje"),
    ("Šumadija-Great Morava", "Jagodina"): ("Rejon Tri Morave", "Jagodinsko vinogorje"),
    ("Šumadija-Great Morava", "Mlava"): ("Mlavski rejon", None),
    ("Šumadija-Great Morava", "Belgrade"): ("Beogradski rejon", None),
    ("Šumadija-Great Morava", None): (None, None),
    ("West Morava", "Kruševac"): ("Rejon Tri Morave", "Kruševačko vinogorje"),
    ("West Morava", None): (None, None),
    ("Nišava-South Morava", "Toplica"): ("Toplički rejon", None),
    ("Nišava-South Morava", "Vranje"): ("Vranjski rejon", None),
    ("Nišava-South Morava", "Niš"): ("Niški rejon", None),
    ("Negotinska Krajina", None): ("Rejon Negotinska Krajina", None),
    ("Timok", "Knjaževac"): ("Knjaževački rejon", None),
    ("Timok", "Krajina"): ("Rejon Negotinska Krajina", None),
    ("Pocerina", None): ("Pocersko Valjevski Rejon", None),
    ("Centralna Srbija", "Tri Morave"): ("Rejon Tri Morave", None),
    ("Centralna Srbija", None): (None, None),
    ("Tri Morave", None): ("Rejon Tri Morave", None),
    ("Oplenac", None): ("Šumadijski rejon", "Oplenačko vinogorje"),
    # Тимок — это Књажевачки рејон и Неготинска Крајина сразу, Ниш —
    # четыре рејона, Банат — два. Одним регионом рејон не назван, и
    # ставить его наугад нельзя: пусто здесь стоит нарочно.
    ("Timok", None): (None, None),
    ("Nišava-South Morava", None): (None, None),
    ("Banat", None): (None, None),
    (None, None): (None, None),
}

# Одно и то же место DWWA пишет и по-английски, и по-сербски, и
# в испорченной кодировке: «Šumadija-Great Morava», «Šumadijsko-
# Velikomoravski», «Å Umadijsko-Velikomoravski». Разные написания —
# не разные места, но таблица выше про это не знает и молча отвечала
# «не знаю» на каждое второе.
DECANTER_IMENA = {
    "sumadijsko-velikomoravski": "Šumadija-Great Morava",
    "sumadijsko velikomoravski": "Šumadija-Great Morava",
    "sumadija-great morava": "Šumadija-Great Morava",
    "subotica-horgos": "Subotica-Horgoš",
    "negotinska krajina": "Negotinska Krajina",
}


# IWC и Wine Trophy тоже называют область хозяйства — теми же именами
# старой рејонизације, что и DWWA, только со своими опечатками. Оба
# источника были собраны и не читались вовсе: место у них лежало в
# записи и никуда не шло.
OBLAST_KONKURSA = {
    "negotinska krajina": ("Rejon Negotinska Krajina", None),
    "subotica": ("Subotički rejon", None),
    "subotica-horgos": ("Subotički rejon", None),
    "belgrade viticultural region": ("Beogradski rejon", None),
    "fruska gora": ("Sremski rejon", "Fruškogorsko vinogorje"),
    "srem": ("Sremski rejon", None),
    "pocerina": ("Pocersko Valjevski Rejon", None),
    # Тимок — это Књажевачки рејон и Неготинска Крајина сразу, Шумадијско-
    # великоморавски — четыре рејона, Западна Морава и Нишава — по
    # нескольку. Одним именем рејон здесь не назван: пусто стоит нарочно.
    "timok": (None, None),
    "timocki rajon": (None, None),
    "sumadijsko velikomoravski": (None, None),
    "sumdijsko-velikomoravski rajon": (None, None),
    "sumadija-great morava": (None, None),
    "west morava": (None, None),
    "nisava-south morava": (None, None),
    "banat": (None, None),
    "vojvodina": (None, None),
    "centralna srbija": (None, None),
}


def oblast_konkursa(syroe):
    """Рејон по имени области, как его пишут конкурсы. Или ничего."""
    s = chinit_kodirovku(bez_pustogo(syroe))
    if not s:
        return None, None, ""
    s = re.sub(r",\s*serbia\s*$", "", s.strip(), flags=re.I)
    prosto = "".join(z for z in unicodedata.normalize("NFD", s.lower())
                     if unicodedata.category(z) != "Mn")
    prosto = re.sub(r"\s+", " ", prosto).strip()
    rejon, vinogorje = OBLAST_KONKURSA.get(prosto, (None, None))
    return rejon, vinogorje, s


def oblast_vina(syroe):
    """Рејон и виногорје по области, заявленной у самого вина.

    Строка приходит в двух видах: «Srem · Fruška Gora» — так её пишет
    Decanter, склеивая region и subRegion, — и вольная, «Timocki Rajon,
    Serbia», у IWC и Wine Trophy.

    Это происхождение винограда, а не адрес хозяйства, и для справочника
    о терруаре оно старше: у Карића одни вина заявлены в Поцерини, другие
    в Срему, и это два разных виноградника, а не ошибка.
    """
    s = chinit_kodirovku(bez_pustogo(syroe))
    if not s:
        return None, None
    if " · " in s:
        chasti = [imya_decantera(x) for x in s.split(" · ")]
        para = (chasti[0], chasti[1] if len(chasti) > 1 else None)
        if para not in DECANTER_PARA:
            para = (para[0], None)
        if para in DECANTER_PARA:
            return DECANTER_PARA[para]
    para = (imya_decantera(s), None)
    if para in DECANTER_PARA:
        return DECANTER_PARA[para]
    rejon, vinogorje, _ = oblast_konkursa(s)
    return rejon, vinogorje


def chinit_kodirovku(s):
    """Вернуть строку, дважды закодированную в UTF-8, к читаемому виду.

    «Subotica-HorgoÅ¡» — это «Subotica-Horgoš», прочитанное как latin-1.
    """
    if not s or not re.search(r"[ÂÃÅ]", s):
        return s
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def imya_decantera(s):
    """Написание места у DWWA — к тому, которое знает таблица пар."""
    s = chinit_kodirovku(bez_pustogo(s))
    if not s:
        return None
    prosto = re.sub(r"\s+", " ", s).strip()
    bez_znakov = "".join(
        z for z in unicodedata.normalize("NFD", prosto.lower())
        if unicodedata.category(z) != "Mn")
    return DECANTER_IMENA.get(bez_znakov, prosto)

# Имя старой рејонизације рејона не даёт, но регион даёт, а иногда и
# короткий список, в котором рејон точно есть. Это не «не знаем ничего»:
# «Šumadija-Great Morava» — четыре рејона из двадцати двух, и записать
# их в поле расхождения полезнее, чем оставить пустоту.
#
# «Central Serbia» и «Wine of Serbia» сюда не входят: у первого слаг
# `serbia`, то есть это вся страна, а не регион Централна Србија.
VIVINO_REGION = {
    "Srem": "Vojvodina", "Fruška Gora": "Vojvodina", "Bačka": "Vojvodina",
    "Potisje": "Vojvodina", "Banat": "Vojvodina", "Vojvodina": "Vojvodina",
    "Subotica-Horgos": "Vojvodina",
    "Šumadija-Great Morava": "Centralna Srbija", "Tri Morave": "Centralna Srbija",
    "West Morava": "Centralna Srbija", "Morava": "Centralna Srbija",
    "Negotinska Krajina": "Centralna Srbija", "Timočka Krajina": "Centralna Srbija",
    "Toplica": "Centralna Srbija", "Knjaževac": "Centralna Srbija",
    "Niš": "Centralna Srbija", "Nisava-South Morava": "Centralna Srbija",
    "Leskovac": "Centralna Srbija", "Vranje": "Centralna Srbija",
    "Pirot": "Centralna Srbija", "Pocerina": "Centralna Srbija",
    "Čačak-Kraljevo": "Centralna Srbija",
    "Metohija": "Kosovo i Metohija",
}

KANDIDATY_REJONA = {
    "Banat": ["Banatski rejon", "Južnobanatski rejon"],
    "Timočka Krajina": ["Rejon Negotinska Krajina", "Knjaževački rejon"],
    "Nisava-South Morava": ["Niški rejon", "Nišavski rejon", "Leskovački rejon",
                            "Vranjski rejon", "Toplički rejon"],
    "Šumadija-Great Morava": ["Šumadijski rejon", "Beogradski rejon",
                              "Mlavski rejon", "Rejon Tri Morave"],
    "West Morava": ["Čačansko–kraljevački rejon", "Rejon Tri Morave"],
    "Metohija": ["Severnometohijski rejon", "Južnometohijski rejon"],
}

FALSTAFF_REJON = {
    "Суботица-Хоргош": "Subotički rejon",
    "Шумадия-Велика Морава": None,   # тот же старый большой рејон
    "поиск по Сербии": None,
    "список красных": None,
    "список белых": None,
    "список розе": None,
    "Tasting Serbien 2023": None,
}

# Справочник vinarijesrbije.rs делит Сербию на те же 22 рејона, но зовёт
# два из них иначе. Сводим по слагу: слаг у них устойчивее имени.
SLUG_REJONA = {
    "negotinska-krajina": "rejon-negotinska-krajina",
    "sumadija": "sumadijski-rejon",
}

# Код рејона в справочнике → его официальное имя. Заполняется при чтении
# справочника: держать два списка имён руками — верный способ разойтись.
IMYA_REJONA = {}

PUSTO = {"Not Applicable", "Not applicable", "None", "", None}


def bez_pustogo(z):
    return None if (z in PUSTO) else z


# Города в карте книги записаны кириллицей («Сремски Карловци»), а в
# справочнике рејонов — латиницей («Sremski Karlovci»). Сербская
# кириллица и латиница переводятся одна в другую однозначно, поэтому
# сводить их можно без догадок. Двубуквенные идут первыми: иначе «њ»
# распадётся на «n» и «j» по одному, а «џ» — на «d» и «z».
KIRILLICA = [("Њ", "Nj"), ("Љ", "Lj"), ("Џ", "Dž"), ("њ", "nj"), ("љ", "lj"),
             ("џ", "dž"), ("а", "a"), ("б", "b"), ("в", "v"), ("г", "g"),
             ("д", "d"), ("ђ", "đ"), ("е", "e"), ("ж", "ž"), ("з", "z"),
             ("и", "i"), ("ј", "j"), ("к", "k"), ("л", "l"), ("м", "m"),
             ("н", "n"), ("о", "o"), ("п", "p"), ("р", "r"), ("с", "s"),
             ("т", "t"), ("ћ", "ć"), ("у", "u"), ("ф", "f"), ("х", "h"),
             ("ц", "c"), ("ч", "č"), ("ш", "š"), ("й", "j"), ("щ", "š"),
             ("ы", "i"), ("э", "e"), ("ю", "ju"), ("я", "ja"), ("ъ", ""),
             ("ь", "")]


def latinicej(s):
    for a, b in KIRILLICA:
        s = s.replace(a, b).replace(a.upper(), b.upper() if len(b) == 1
                                    else b.capitalize())
    return s


def prostoj_klyuch(s):
    # «dj» — тот же «đ» без диакритики, см. `sobrat-tablicy.py`.
    s = s.lower().replace("dj", "đ")
    for a, b in (("š", "s"), ("đ", "d"), ("č", "c"), ("ć", "c"), ("ž", "z")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9а-я]+", "-", s).strip("-")


def klyuch_mesta(*chasti):
    """Ключ места — с переводом кириллицы в латиницу."""
    return prostoj_klyuch(latinicej(" ".join(c for c in chasti if c)))


# Тот же список, что в `sobrat-tablicy.py`, — ключи обязаны совпадать.
SLUZHEBNYE = ("vinarija", "podrum", "podrumi", "vinogradi", "vinska-kuca",
              "vinarska-kuca", "gazdinstvo", "winery", "estate", "manastir",
              "monastery", "vino", "vina", "doo", "ad", "pr", "vinery",
              "vineyards", "wine", "wines")


# Имена, сведённые руками и с доказательством, — `sinonimy-hozyaistv.json`.
# Похожесть имён доказательством не считается: Jovanović и Jovanov,
# Madžić и Adžić, Stojković и Stojanović — разные хозяйства.
def _sinonimy():
    """Варианты имени → каноническое. Сводится по ключу, а не по строке.

    По строке не годится: у источников есть и «Šapat», и «Sapat» без
    диакритики, и перечислять оба в списке синонимов — заведомо не
    перечислить все. Ключ их и так уравнивает, поэтому свожу ключи.
    """
    put_f = os.path.join(RYADOM, "sinonimy-hozyaistv.json")
    if not os.path.exists(put_f):
        return {}
    d = json.load(open(put_f, encoding="utf-8"))["hozyaistva"]
    return {_bazovyj_klyuch(v): _bazovyj_klyuch(imya)
            for imya, z in d.items() for v in z["varianty"]}


def bez_skobok(imya):
    """«Винарија Тришић (Vinarija Trišić)» — это «Vinarija Trišić».

    То же правило, что в `sobrat-tablicy.py`: латинская расшифровка в
    скобках заменяет кириллическое имя. Скобки с кириллицей внутри
    («Aglaya (Аглая)») наоборот отбрасываются.
    """
    sovpalo = re.search(r"^(.+?)\s*\(([^()]+)\)\s*$", imya)
    if not sovpalo:
        # То же самое, но через тире: «Орлић Породична Винарија -
        # Orlić Family Winery», «Трилогия Винария - Vinarija Trilogija».
        sovpalo = re.search(r"^(.+?)\s+[-–]\s+(.+?)\s*$", imya)
    if not sovpalo:
        return imya
    levo, pravo = sovpalo.group(1), sovpalo.group(2)
    kirillica = lambda s: any("\u0400" <= z <= "\u04ff" for z in s)
    if kirillica(pravo) and not kirillica(levo):
        return levo
    if kirillica(levo) and not kirillica(pravo):
        return pravo
    return imya


SINONIMY = {}


def klyuch_hozyaistva(imya):
    """Ключ хозяйства — ровно тот же, что в `sobrat-tablicy.py`.

    Кириллица сама по себе в латиницу здесь не переводится — только
    через скобки: ключи обязаны совпадать с остальными таблицами, иначе
    рејон не с чем будет связать.
    """
    return SINONIMY.get(_bazovyj_klyuch(imya), _bazovyj_klyuch(imya))


def _bazovyj_klyuch(imya):
    k = prostoj_klyuch(bez_skobok(imya))
    chasti = [c for c in k.split("-") if c and c not in SLUZHEBNYE]
    return "-".join(chasti) or k


# ------------------------------------------------- кадастровые имена
# В официальном тексте рејонизације кадастровые общины перечислены не
# списком, а прозой: «Северни део: делови катастарских општина Речка,
# Мокрање, …, Рајац. Јужни део: делови катастарских општина Браћевац, …».
# При разборе по запятым такая фраза целиком попадает в одно имя, и место
# теряется: из-за этого Рајац — то самое село роглевачко-рајачких пивниц —
# в карте отсутствовал, а Vinarija Raj уезжала в Чачанско-краљевачки рејон.
# Слипшихся строк 58 из 2162; здесь они разбираются обратно на имена.
POYASNENIE = re.compile(
    r"(?:^|\s)(?:severni|južni|istočni|zapadni|centralni|severoistočni"
    r"|severozapadni|jugoistočni|jugozapadni|ljiški)\s+deo(?:\s*\([^)]*\))?\s*:\s*"
    r"|(?:^|\s)(?:i\s+)?(?:kao\s+i\s+)?(?:cel\w+\s+)?(?:delovi?e?\s+)?"
    r"katastarsk\w+\s+opštin\w*\s+"
    r"|(?:^|\s)oaza\s+.*?\s+(?:obuhvata|nalazi\s+se\s+na)\s+", re.I)
HVOST_MESTA = re.compile(r"\s*[–-]?\s*(van\s+)?(varošica|varoš|grad|selo)$", re.I)
NAPRAVLENIE = re.compile(r"^(severni|južni|istočni|zapadni|centralni|severoistočni"
                         r"|severozapadni|jugoistočni|jugozapadni|ljiški)\s+deo$", re.I)


def imena_kadastra(stroka):
    """Имена кадастровых общин из строки официального текста."""
    kuski = re.split(r"\.\s+", stroka)
    while True:                       # пояснения бывают вложены друг в друга
        novye = [c for k in kuski for c in POYASNENIE.split(k)]
        if novye == kuski:
            break
        kuski = novye
    imena = []
    for kus in kuski:
        kus = (kus or "").strip().strip(".,:;")
        kus = re.sub(r"\s*\([^)]*\)\s*$", "", kus).strip()
        kus = HVOST_MESTA.sub("", kus).strip()
        if kus and not NAPRAVLENIE.match(kus):
            imena.append(kus)
    return imena


# ---------------------------------------------------------------- справочник
def spravochnik():
    """Справочник и четыре карты мест, по убыванию достоверности.

    Уровни разделены нарочно. «Aleksandrovac» — это и община Рејона Три
    Мораве, и кадастровое село ещё в четырёх виногорјима по всей стране.
    Пока обе карты были свалены в одну, девять жупских винарий оставались
    без рејона: имя выглядело неоднозначным. Община — административная
    единица, и когда справочник пишет город, он имеет в виду её.
    """
    d = json.load(open(put("rejony-vinogorja.json"), encoding="utf-8"))
    po_rejonu = {r["rejon"]: r for r in d["rejony"]}
    IMYA_REJONA.update({r["kod"]: r["rejon"] for r in d["rejony"]})

    karty = {"vinogorje": {}, "opstina": {}, "selo": {}, "okrug": {},
             "spravochnik": {}, "okrug_vse": {}}
    for r in d["rejony"]:
        for o in r["opstine"]:
            karty["opstina"].setdefault(klyuch_mesta(o), set()).add(
                (r["rejon"], None))
        for v in r["vinogorja"]:
            karty["vinogorje"].setdefault(klyuch_mesta(v["vinogorje"]),
                                          set()).add((r["rejon"], v["vinogorje"]))
            for o in v["katastarske_opstine"]:
                for imya in imena_kadastra(o):
                    karty["selo"].setdefault(klyuch_mesta(imya), set()).add(
                        (r["rejon"], v["vinogorje"]))
    # Округ — самый крупный уровень. Он выводится не по выборке, а по
    # официальным спискам: община → округ, община → рејон, значит округ →
    # рејоны. Годится только тот округ, который целиком лежит в одном
    # рејоне: Зајечарски, например, делится между Књажевачким и Нишким,
    # и по нему ставить нечего.
    if os.path.exists(put("opstina-okrug.json")):
        pары = json.load(open(put("opstina-okrug.json"), encoding="utf-8"))["opstiny"]
        okrug_opstiny = {klyuch_mesta(o): ok for o, ok in pары.items()}
        okrug_rejony = {}
        for r in d["rejony"]:
            for o in r["opstine"]:
                ok = okrug_opstiny.get(klyuch_mesta(o))
                if ok:
                    okrug_rejony.setdefault(ok, set()).add(r["rejon"])
        for ok, rejony in okrug_rejony.items():
            karty["okrug_vse"][klyuch_mesta(ok + " okrug")] = set(rejony)
            if len(rejony) == 1:
                karty["okrug"].setdefault(klyuch_mesta(ok + " okrug"),
                                          set()).add((next(iter(rejony)), None))

    if os.path.exists(put("vinarijesrbije-mesta.json")):
        vs = json.load(open(put("vinarijesrbije-mesta.json"), encoding="utf-8"))
        for g in vs["goroda"]:
            kod = SLUG_REJONA.get(g["rejon_slug"], g["rejon_slug"])
            if IMYA_REJONA.get(kod):
                karty["spravochnik"].setdefault(klyuch_mesta(g["gorod"]),
                                                set()).add((IMYA_REJONA[kod], None))
    return d, po_rejonu, karty


# ---------------------------------------------------------------- показания
def pokazaniya():
    """Собрать по хозяйствам всё, что источники говорят о месте."""
    p = collections.defaultdict(list)

    for f in glob.glob(put("kesh-decanter/*")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        for w in (d if isinstance(d, list) else d.get("data", [])):
            if not isinstance(w, dict) or not w.get("producer"):
                continue
            para = (imya_decantera(w.get("region")),
                    imya_decantera(w.get("subRegion")))
            if para not in DECANTER_PARA:
                para = (para[0], None)
            rejon, vinogorje = DECANTER_PARA.get(para, (None, None))
            p[klyuch_hozyaistva(w["producer"])].append({
                "istochnik": "decanter", "syroe": " · ".join(x for x in para if x),
                "rejon": rejon, "vinogorje": vinogorje})

    # IWC называет область у каждой медали, Wine Trophy — тоже, своими
    # словами: «Timocki Rajon, Serbia», «Fruška gora, Serbia».
    for fajl, pole, imya in (("iwc-zapisi.json", "oblast_iwc", "iwc"),
                             ("wine-trophy-zapisi.json", "mesto", "wine-trophy")):
        if not os.path.exists(put(fajl)):
            continue
        for z in json.load(open(put(fajl), encoding="utf-8"))["zapisi"]:
            rejon, vinogorje, syroe = oblast_konkursa(z.get(pole))
            if not syroe:
                continue
            p[klyuch_hozyaistva(z["hozyaistvo"])].append({
                "istochnik": imya, "syroe": syroe,
                "rejon": rejon, "vinogorje": vinogorje})

    if os.path.exists(put("vivino-syrye.json")):
        for w in json.load(open(put("vivino-syrye.json"), encoding="utf-8"))["vina"]:
            syroe = w.get("region_vivino") or w.get("region")
            if not w.get("hozyaistvo") or not syroe:
                continue
            p[klyuch_hozyaistva(w["hozyaistvo"])].append({
                "istochnik": "vivino", "syroe": syroe,
                "rejon": VIVINO_REJON.get(syroe), "vinogorje": None,
                "region": VIVINO_REGION.get(syroe),
                "kandidaty": KANDIDATY_REJONA.get(syroe)})

    for s in open(put("kritiki-zapisi.jsonl"), encoding="utf-8"):
        if not s.strip():
            continue
        z = json.loads(s)
        if z["istochnik"] != "falstaff":
            continue
        oblast = z.get("stranica", "").split(" · ")[0].replace("falstaff, ", "")
        p[klyuch_hozyaistva(z["hozyaistvo"])].append({
            "istochnik": "falstaff", "syroe": oblast,
            "rejon": FALSTAFF_REJON.get(oblast), "vinogorje": None})

    # ivv.rs рејона не называет вовсе — только место. Зато место у него
    # есть у всех 142 хозяйств, и часто с округом: «Aleksandrovac,
    # Rasinski okrug». Рејон из него выводится картой мест.
    if os.path.exists(put("ivv-mesta.json")):
        for v in json.load(open(put("ivv-mesta.json"), encoding="utf-8"))["vinarii"]:
            if not v.get("mesto"):
                continue
            p[klyuch_hozyaistva(v["imya"])].append({
                "istochnik": "ivv", "syroe": v["mesto"],
                "rejon": None, "vinogorje": None, "gorod": v["mesto"]})

    # Винарски регистар Министарства пољопривреде: место — насеље, где
    # производитель зарегистрирован. Оно точнее любого каталога, но это
    # адрес юридического лица: у трёх десятков винарий он городской,
    # столичный, и виноградника там нет. Такие в `svesti-registar.py`
    # оставлены без места нарочно.
    if os.path.exists(put("registar-hozyaistv.json")):
        d = json.load(open(put("registar-hozyaistv.json"), encoding="utf-8"))
        for k, v in d["hozyaistva"].items():
            if not v.get("mesto"):
                continue
            p[k].append({
                "istochnik": "registar", "syroe": v["mesto"],
                "rejon": None, "vinogorje": None, "gorod": v["mesto"]})

    # Страница хозяйства на Vivino отдаёт адрес: улица, город, индекс.
    # В листинге его нет, поэтому берётся отдельно — `vzjat-adresa-vivino.py`.
    for f in glob.glob(put("kesh-vivino-adresa/*.json")):
        try:
            v = json.load(open(f, encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not v.get("gorod") or v.get("strana") not in (None, "rs"):
            continue
        p[klyuch_hozyaistva(v.get("imya_listinga") or v["imya"])].append({
            "istochnik": "vivino-adres", "syroe": v["gorod"],
            "rejon": None, "vinogorje": None, "gorod": v["gorod"]})

    if os.path.exists(put("vinarijesrbije-mesta.json")):
        d = json.load(open(put("vinarijesrbije-mesta.json"), encoding="utf-8"))
        po_slugu = {r["slug"]: r["imya"] for r in d["rejony"]}
        for v in d["vinarii"]:
            if not v.get("rejon_slug"):
                continue
            p[klyuch_hozyaistva(v["imya"])].append({
                "istochnik": "vinarijesrbije",
                "syroe": "%s%s" % (po_slugu.get(v["rejon_slug"], v["rejon_slug"]),
                                   ", " + v["gorod"] if v.get("gorod") else ""),
                "rejon": IMYA_REJONA.get(SLUG_REJONA.get(v["rejon_slug"],
                                                         v["rejon_slug"])),
                "vinogorje": None,
                "gorod": v.get("gorod") or ""})

    return p


UROVNI = ("vinogorje", "opstina", "selo", "okrug", "spravochnik")


def kandidaty(gde):
    """Куски поля места, от целого к частям.

    В поле пишут по-разному: «Vinča, Topola - Oplenac», «Grošnica,
    Kragujevac», «Гроцка под Белградом», «Вршац. Внимание: …». Поэтому
    сначала отсекается замечание после точки с запятой, потом поле
    делится по запятым и тире, и каждая часть ещё укорачивается с конца
    по слову — так «Гроцка под Белградом» находится как «Гроцка».
    """
    gde = re.split(r"[;(]", gde)[0]
    gde = re.sub(r"\.\s+[А-ЯA-Z].*$", "", gde)      # «Вршац. Внимание: …»
    chasti = [c.strip(" .-") for c in re.split(r"[,–—]|\s-\s", gde)]
    out = []
    for c in chasti:
        if not c:
            continue
        slova = c.split()
        for skolko in range(len(slova), 0, -1):
            out.append(" ".join(slova[:skolko]))
    return out


# Справочник винарий кое-где пишет в графе города область, а не место.
# Ехать «во Фрушку гору» нельзя — это гряда, а «в Жупу» — это край.
NE_GOROD = {"fruska-gora", "zupa"}


def imya_goroda(gde, karty):
    """Место, куда ехать: населённый пункт, а не округ.

    Округ в этой работе — только машинерия: он помогает найти рејон и
    отсечь чужие, но читателю он не нужен. Нужен город или село:
    «Vinča, Topola - Oplenac, Šumadijski okrug» — ехать в Винчу.

    Берётся самый точный кусок поля, который справочник узнаёт как место.
    Пояснения вроде «Vivino относит к „Zapadna Morava“» местом не
    становятся: там узнавать нечего.
    """
    if not gde:
        return ""
    for kus in kandidaty(gde):
        klyuch = klyuch_mesta(kus)
        if klyuch.endswith("-okrug") or klyuch in NE_GOROD:
            continue
        # Виногорје — не место назначения: «Фрушка гора» и «Левачко
        # виногорје» это область, а не адрес, куда ехать.
        for uroven in ("opstina", "selo", "spravochnik"):
            if klyuch in karty[uroven]:
                return re.sub(r"^(selo|village|село)\s+", "", kus,
                              flags=re.I).strip()
    return ""


def po_mestu(gde, karty):
    """Рејон и виногорје по месту хозяйства.

    Сначала собираются все попадания, потом берётся самое достоверное:
    названное виногорје старше общины, община старше кадастрового села,
    село старше чужого справочника. Если на одном уровне два разных
    ответа — место считается неразобранным: угадывать тут нельзя.
    """
    if not gde:
        return None, None, ""
    kusky = kandidaty(gde)


    # Названный округ не столько указывает рејон, сколько отсекает чужие.
    # «Rajac, Borski okrug»: Рајац есть и в Јеличком виногорју под Чачком,
    # но Борски округ — это Неготинска Крајина, и чачанский Рајац отпадает.
    # Округ, которого нет в списках, ничего не отсекает.
    okrug_rejony = set()
    for kus in kusky:
        okrug_rejony |= karty["okrug_vse"].get(klyuch_mesta(kus), set())

    def popadaniya(uroven):
        out = []
        for kus in kusky:
            for para in karty[uroven].get(klyuch_mesta(kus), ()):
                if okrug_rejony and para[0] not in okrug_rejony:
                    continue
                out.append((para, kus))
        return out

    for uroven in UROVNI:
        nashlos = popadaniya(uroven)
        rejony = {p[0] for p, _ in nashlos}
        if not rejony:
            continue                      # на этом уровне место не названо
        if len(rejony) > 1:
            # Уровень ответил, но двумя ответами сразу: община Сомбор
            # лежит и в Телечком, и в Суботичком, и в Рејону Бачка.
            # Спускаться ниже тут нельзя — нижний уровень слабее, и его
            # единственный ответ будет не решением, а догадкой.
            return None, None, ""
        rejon = rejony.pop()
        # Рејон найден. Виногорје ищется отдельно и уже внутри него:
        # уровень общины виногорја не знает вовсе, а село знает — так
        # «Vinča, Topola - Oplenac» даёт и Шумадијски, и Опленачко.
        vinogorja = {vg for u in ("vinogorje", "selo")
                     for (rj, vg), _ in popadaniya(u) if rj == rejon and vg}
        return (rejon,
                vinogorja.pop() if len(vinogorja) == 1 else None,
                nashlos[0][1])

    # Последняя попытка: место названо не селом, а областью. У Бојана Баше
    # книга пишет просто «Срем» — списки мест такого не знают, они
    # о населённых пунктах, зато таблица областей знает. Только после
    # всех уровней: село точнее области, и перебивать его нельзя.
    # Кириллицу перед этим надо перевести, таблица латинская.
    for kus in kusky:
        rejon, vinogorje, _ = oblast_konkursa(latinicej(kus))
        if rejon:
            return rejon, vinogorje, kus
    return None, None, ""


def rejony_mesta(gde, karty):
    """Рејоны, между которыми место не решает.

    Рејонизација делит иные общины между рејонима: Кањижа лежит и в
    Потиском, и в Суботичком, Зрењанин — в Банатском и Потиском, Сомбор
    сразу в трёх. Ставить один из них наугад нельзя, но и молчать не
    стоит: короткий список — это знание.
    """
    if not gde:
        return []
    kusky = kandidaty(gde)
    for uroven in UROVNI:
        rejony = {para[0] for kus in kusky
                  for para in karty[uroven].get(klyuch_mesta(kus), ())}
        if rejony:
            return sorted(rejony)
    return []


def main():
    d, po_rejonu, karty = spravochnik()
    karta = json.load(open(put("raion-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]
    gde_po_klyuchu = {klyuch_hozyaistva(k): v.get("gde", "")
                      for k, v in karta.items()}
    imya_po_klyuchu = {}
    for s in open(put("hozyaistva.jsonl"), encoding="utf-8"):
        if s.strip():
            z = json.loads(s)
            imya_po_klyuchu[z["klyuch"]] = z["hozyaistvo"]

    p = pokazaniya()
    itog, spor = {}, []
    for k in sorted(set(p) | set(imya_po_klyuchu) | set(gde_po_klyuchu)):
        pok = p.get(k, [])
        rejony = collections.Counter(x["rejon"] for x in pok if x["rejon"])
        vinogorja = collections.Counter(x["vinogorje"] for x in pok if x["vinogorje"])

        rejon = vinogorje = None
        istochnik = "ne_ustanovlen"
        # Города, названные хоть кем-то. Он нужен не только ради рејона —
        # по нему же находится и виногорје. Источники разного веса, и вес
        # тут не вкусовой: каталоги пишут, где хозяйство стоит, а регистр —
        # где оно зарегистрировано, и это разные вещи. У Амбелоса ivv.rs
        # даёт Велику Плану, а регистр — Пожаревац: контора в городе,
        # виноградник за ним. Поэтому места разбираются по старшинству,
        # и слабый источник не спорит с сильным, а молчит при нём.
        VES = {"ivv": 1, "vinarijesrbije": 1, "registar": 2, "vivino-adres": 3}
        # Источники, у которых область — заявленное происхождение вина,
        # а не адрес хозяйства.
        KONKURSY = {"decanter", "iwc", "wine-trophy"}
        po_vesu = collections.defaultdict(list)
        if gde_po_klyuchu.get(k):
            po_vesu[0].append(gde_po_klyuchu[k])          # город из книги
        for x in pok:
            if x.get("gorod"):
                po_vesu[VES.get(x["istochnik"], 2)].append(x["gorod"])

        raznoglasie = ""
        gde, m_rejon, m_vinogorje = "", None, None
        razobrano_vsego = []
        for ves in (0, 1, 2):
            razobrano = [(g,) + po_mestu(g, karty)[:2] for g in po_vesu.get(ves, [])]
            razobrano = [(g, r, v) for g, r, v in razobrano if r]
            razobrano_vsego += razobrano
            raznye = {r for _, r, _ in razobrano}
            if len(raznye) > 1:
                # Спор внутри одного веса место не решает: у Urošević
                # ivv.rs пишет Баноштор на Фрушкој гори, а vinarijesrbije —
                # Књажевац, это разные концы страны.
                raznoglasie = "города спорят: " + "; ".join(
                    "%s → %s" % (g, r) for g, r, _ in razobrano)
                spor.append((k, {}, None, None))
                break
            if raznye:
                gde, m_rejon, m_vinogorje = razobrano[0]
                break
        if not gde:
            gde = gde_po_klyuchu.get(k, "") or next(
                (x["gorod"] for x in pok if x.get("gorod")), "")
        # Место — старше всего. Справочник винарий пишет Vino Budimir
        # в Сремски рејон, а адресом даёт Александровац, то есть Жупу:
        # ярлык у них ошибочный, адрес — нет. Поэтому если город найден
        # однозначно, он и решает, даже когда источник один.
        # Ярлык конкурса — о винограде, город — о доме. Подавая вино,
        # производитель заявляет происхождение винограда, и конкурс
        # печатает именно его; город берётся из каталога или регистра
        # и говорит, где стоит подвал или контора. Справочник о терруаре
        # относит вино к месту виноградника, поэтому единодушный ярлык
        # конкурсов старше города. Единодушный и не единичный: одна
        # строка против места — это чаще опечатка или чужая запись,
        # приставшая при сведении имён.
        konkursnye = collections.Counter(
            x["rejon"] for x in pok
            if x["rejon"] and x["istochnik"] in KONKURSY)
        if m_rejon:
            rejon, istochnik = m_rejon, "mesto"
            if (len(konkursnye) == 1 and sum(konkursnye.values()) >= 2
                    and next(iter(konkursnye)) != m_rejon):
                rejon = next(iter(konkursnye))
                istochnik = "konkurs"
                raznoglasie = ("виноградник по конкурсам %s ×%d, "
                               "дом по месту %s" % (rejon, konkursnye[rejon],
                                                    m_rejon))
                spor.append((k, dict(rejony), m_rejon, rejon))
            elif rejony and set(rejony) != {m_rejon}:
                raznoglasie = "по месту %s, у источников %s" % (
                    m_rejon, "; ".join("%s ×%d" % (r, n)
                                       for r, n in rejony.most_common()))
                spor.append((k, dict(rejony), m_rejon, rejon))
        elif len(rejony) == 1:
            rejon = next(iter(rejony))
            istochnik = "+".join(sorted({x["istochnik"] for x in pok if x["rejon"]}))
        elif len(rejony) > 1:
            (pervyj, n1), (vtoroj, n2) = rejony.most_common(2)
            if n1 >= 4 * n2:
                # Одиночная запись против восьмидесяти — это опечатка
                # у источника, а не второе место работы хозяйства.
                rejon, istochnik = pervyj, "bolshinstvo"
            raznoglasie = "; ".join(x for x in (raznoglasie,
                "; ".join("%s ×%d" % (r, n) for r, n in rejony.most_common())) if x)
            spor.append((k, dict(rejony), m_rejon, rejon))

        # Адрес со страницы Vivino — последним, уже после ярлыков.
        # Его вписывает тот, кто занял страницу хозяйства, и это часто
        # контора: у Fleur d'Oranger там Нови Сад, а Decanter относит вина
        # к северу Баната. Ярлык конкурса тут вернее адреса.
        if not rejon:
            for g in po_vesu.get(3, []):
                v_rejon, v_vinogorje, _ = po_mestu(g, karty)
                if v_rejon:
                    rejon, vinogorje = v_rejon, v_vinogorje
                    istochnik, gde = "vivino-adres", g
                    break

        # Виногорје — тем же порядком: место старше ярлыка источника.
        # У Radovanović адрес Крњево, то есть Крњевачко виногорје, а
        # Decanter пишет «Oplenac» — их подрејон крупнее и здесь неверен.
        svoi_rejona = {v["vinogorje"] for v in
                       po_rejonu.get(rejon, {}).get("vinogorja", [])}
        if m_vinogorje and (not rejon or m_vinogorje in svoi_rejona):
            vinogorje = m_vinogorje
        elif len(vinogorja) == 1:
            vinogorje = next(iter(vinogorja))
        # Единственное виногорје рејона — это и есть его виногорје.
        if rejon and not vinogorje:
            vs = po_rejonu.get(rejon, {}).get("vinogorja", [])
            if len(vs) == 1:
                vinogorje = vs[0]["vinogorje"]
        # Виногорје и рејон могли прийти от разных источников и не сойтись:
        # у Savić рејон вышел Нишавски по четырём записям, а виногорје —
        # Опленачко по одной. Виногорје из чужого рејона — не виногорје.
        if vinogorje and rejon:
            svoi = {v["vinogorje"] for v in po_rejonu.get(rejon, {}).get("vinogorja", [])}
            if vinogorje not in svoi:
                raznoglasie = "; ".join(x for x in (raznoglasie,
                                        "виногорје %s — не из этого рејона" % vinogorje) if x)
                vinogorje = None
        elif vinogorje and not rejon:
            vinogorje = None

        # Рејона может не быть, а регион при этом известен: «Banat» —
        # это точно Војводина, пусть и неясно, Банатски или Јужнобанатски.
        # Тогда же записываются кандидаты — короткий список, в котором
        # рејон точно есть. Пустое поле и «один из четырёх» — не одно и то же.
        region = po_rejonu.get(rejon, {}).get("region")
        if not rejon:
            regiony = {x["region"] for x in pok if x.get("region")}
            if len(regiony) == 1:
                region = regiony.pop()
            kand = sorted({r for x in pok for r in (x.get("kandidaty") or [])})
            # Место названо, но само по себе рејона не решает — община
            # поделена между рејонима. Тогда кандидаты берутся от него.
            if not kand:
                kand = [r for r in rejony_mesta(gde, karty)]
                if len(kand) < 2:
                    kand = []
            if kand and not raznoglasie:
                raznoglasie = "рејон один из: " + "; ".join(kand)
                if not region:
                    regiony = {po_rejonu.get(r, {}).get("region") for r in kand}
                    if len(regiony) == 1:
                        region = regiony.pop()

        itog[k] = {
            "hozyaistvo": imya_po_klyuchu.get(k, k),
            "region": region,
            "rejon": rejon,
            "vinogorje": vinogorje,
            "gorod": imya_goroda(gde, karty),
            "istochnik": istochnik if rejon else "ne_ustanovlen",
            "raznoglasie": raznoglasie,
            "gde": gde,
            "pokazaniya": sorted({"%s: %s" % (x["istochnik"], x["syroe"])
                                  for x in pok}),
        }

    # Области, заявленные у самих вин, — со всеми, кто их печатает.
    # Таблица нужна `sobrat-tablicy.py`: там у вина ставится свой рејон,
    # а держать перевод областей в двух местах нельзя.
    oblasti = {}
    for imya in ("nagrady-zapisi.jsonl", "kritiki-zapisi.jsonl"):
        if not os.path.exists(put(imya)):
            continue
        for stroka in open(put(imya), encoding="utf-8"):
            if not stroka.strip():
                continue
            syroe = json.loads(stroka).get("oblast")
            if syroe and syroe not in oblasti:
                r, vg = oblast_vina(syroe)
                oblasti[syroe] = {"rejon": r, "vinogorje": vg}
    ne_uznano = sorted(k for k, v in oblasti.items() if not v["rejon"])
    if ne_uznano:
        print("области вин, не узнанные справочником (%d): %s"
              % (len(ne_uznano), "; ".join(ne_uznano[:12])))

    json.dump({"chto_eto": "Настоящий рејон и виногорје каждого хозяйства — "
                           "по действующей рејонизацији, не по главам книги.",
               "spravochnik": "rejony-vinogorja.json",
               "oblasti_vin": oblasti,
               "hozyaistva": itog},
              open(put("rejony-hozyaistv.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    s_rejonom = [z for z in itog.values() if z["rejon"]]
    s_vinogorjem = [z for z in itog.values() if z["vinogorje"]]
    print("хозяйств: %d, с рејоном: %d, с виногорјем: %d, спорных: %d"
          % (len(itog), len(s_rejonom), len(s_vinogorjem), len(spor)))
    po_ist = collections.Counter(z["istochnik"] for z in s_rejonom)
    for i, n in po_ist.most_common():
        print("   %-22s %d" % (i, n))
    print()
    for rejon, n in collections.Counter(z["rejon"] for z in s_rejonom).most_common():
        print("   %-30s %d" % (rejon, n))
    if spor:
        print("\nразошлись показания (рејон не поставлен, если место не решило):")
        for k, r, m, vzyato in spor:
            print("   %-24s %-46s место: %-16s взято: %s"
                  % (k, r, m or "—", vzyato or "— (не поставлен)"))


SINONIMY.update(_sinonimy())


if __name__ == "__main__":
    main()
