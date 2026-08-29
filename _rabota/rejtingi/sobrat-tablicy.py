#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собрать из сырых выписок три нормализованные таблицы.

Сырьё — `vivino-zapisi.jsonl` и `vivino-syrye.json` (сплошной сбор по API,
если он сделан; при совпадении он старше), `kritiki-zapisi.jsonl`,
`nagrady-zapisi.jsonl`, `raion-hozyaistv.json`,
`falstaff-zvezdy.json`, `celi-spisok.json`. Всё это писалось по ходу сбора и
для анализа неудобно: идентификатор вина спрятан внутри строки-примечания,
две дорожки лежат порознь, шкалы разные.

На выходе — три таблицы в JSONL и CSV:

    hozyaistva.*   хозяйства: район, звёзды, есть ли в книге
    vina.*         вина: ключ, идентификатор Vivino, адрес
    ocenki.*       оценки в длинном виде: строка на измерение
    nagrady.*      награды и места в категориях: у них нет шкалы

Длинный вид у оценок выбран нарочно. Оценка Vivino и балл Falstaff — разные
величины в разных шкалах, и складывать их нельзя. Зато в длинной таблице
они спокойно лежат рядом: у каждой строки написано, чья шкала, каков балл
и на какой выборке он держится. Свести их в широкий вид — одна сводная
таблица; обратно из широкого вида в длинный уже не разложишь.

    python3 _rabota/rejtingi/sobrat-tablicy.py
"""

import csv
import json
import os
import sys
import re
import unicodedata

# На русской Windows консоль по умолчанию не UTF-8, и первая же кириллица
# в выводе роняет скрипт с UnicodeEncodeError. Просим UTF-8 явно.
for _potok in (sys.stdout, sys.stderr, sys.stdin):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
SOBRANO = "2026-08-28"


# Районы Vivino → главы книги. Взяты только однозначные: «Central Serbia»
# и «Wine of Serbia» у них свалка на полторы тысячи вин, по ним судить нельзя.
# «Šumadija-Great Morava» — официальный крупный регион, он покрывает и
# Шумадию, и часть Поморавья, поэтому тоже не годится.
RAION_PO_VIVINO = {
    "Srem": "fruska",
    "Fruška Gora": "fruska",
    "Subotica-Horgos": "subotica",
    "Banat": "banat",
    "Tri Morave": "morave",
    "Negotinska Krajina": "negotin",
    "Toplica": "toplica",
    "Knjaževac": "jugoistok",
    "Niš": "jugoistok",
    "Nisava-South Morava": "jugoistok",
    "Leskovac": "jugoistok",
    "Vranje": "jugoistok",
    "Pirot": "jugoistok",
}


def put(imya):
    return os.path.join(RYADOM, imya)


def chitat_jsonl(imya):
    if not os.path.exists(put(imya)):
        return []
    return [json.loads(s) for s in open(put(imya), encoding="utf-8") if s.strip()]


def vivino_iz_api():
    """Сплошной сбор по API, если он уже сделан.

    `sobrat-rejtingi.py` складывает результат в `vivino-syrye.json`. Эти
    данные точнее ручных выписок: там оценка и число отзывов приходят
    полями, а не пересказом выдачи. Поэтому при совпадении они старше.
    """
    if not os.path.exists(put("vivino-syrye.json")):
        return []
    d = json.load(open(put("vivino-syrye.json"), encoding="utf-8"))
    iz_api = []
    for z in d.get("vina", []):
        if not z.get("hozyaistvo") or not z.get("vino"):
            continue
        iz_api.append({
            "hozyaistvo": z["hozyaistvo"],
            "vino": z["vino"],
            "ocenka": z.get("ocenka"),
            "chislo_ocenok": z.get("chislo_ocenok"),
            "etiketok": z.get("etiketok"),
            "stranica": ("w/%s" % z["id_vina"]) if z.get("id_vina") else "",
            "id_vina": z.get("id_vina"),
            "iz_api": True,
        })
    return iz_api


def svesti_vivino(ruchnoe, iz_api):
    """Слить ручные выписки и сбор по API. При совпадении API старше.

    Ручное не выбрасывается: в нём могут оказаться вина, которых сплошной
    обход не вернул (снятые с продажи, переименованные). Но там, где есть
    и то и другое, берётся API.
    """
    def klyuch_zapisi(z):
        """Одно вино надёжнее всего опознаётся по идентификатору Vivino.

        Имя ненадёжно: одно и то же вино у меня записано как
        «Zupa Aleksandrovac · Srpski Vranac», а у API — как
        «Zupa · Aleksandrovac Srpski Vranac». Идентификатор один.
        """
        vivino_id, _, _ = razobrat_stranicu(z.get("stranica"))
        if z.get("id_vina"):
            return ("id", z["id_vina"])
        if vivino_id:
            return ("id", vivino_id)
        return ("imya", klyuch_hozyaistva(z["hozyaistvo"]), klyuch(z["vino"]))

    svedeno = {}
    for z in ruchnoe:
        svedeno[klyuch_zapisi(z)] = z
    poverh_ruchnyh = 0
    for z in iz_api:
        k = klyuch_zapisi(z)
        if k in svedeno:
            poverh_ruchnyh += 1
        svedeno[k] = z

    # Второй проход, по имени. Идентификатор разводит записи, у которых
    # имя разбито по-разному, а ключ вина в таблицах всё равно строится
    # из имени — иначе оценку критика не с чем было бы связать. Поэтому
    # то, что сходится по имени, тоже сводим: старше запись из API.
    po_imeni = {}
    for z in svedeno.values():
        k = (klyuch_hozyaistva(z["hozyaistvo"]), klyuch(z["vino"]))
        if k in po_imeni and not z.get("iz_api"):
            continue
        po_imeni[k] = z
    svedeno = po_imeni

    if iz_api:
        print("Vivino: ручных %d, из API %d, из них поверх ручных %d"
              % (len(ruchnoe), len(iz_api), poverh_ruchnyh))
    return list(svedeno.values())


# Одно и то же хозяйство зовётся по-разному: в книге «Deurić», у Vivino
# «Vinarija Deurić», у Decanter «Vinarija Deuric». Слова «винария»,
# «подрум», «виногради» в имени ничего не различают — при сведении их
# отбрасываем, а для показа берём то имя, которое встретилось первым.
# Слова, которые в имени хозяйства ничего не различают: род занятий
# («винарија», «подрум»), форма собственности («д.о.о.», «пр») и
# английские кальки. «Vino Budimir» и «Budimir», «Krstašica Doo» и
# «Krstašica», «Podrum Vina Žarković» и «Žarković» — одни и те же дома.
SLUZHEBNYE = ("vinarija", "vinarija-", "podrum", "podrumi", "vinogradi",
              "vinska-kuca", "vinarska-kuca", "gazdinstvo", "winery",
              "vinarija-vinarija", "estate", "manastir", "monastery",
              "vino", "vina", "doo", "ad", "pr", "vinery", "vineyards",
              "wine", "wines")


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


def _sinonimy_vin():
    """Написания одного вина → то, которое остаётся. Ключ по хозяйству.

    Список ведётся руками, в `sinonimy-vin.json`, и каждая пара
    просмотрена глазами. Догадкой по похожести имён его наполнять
    нельзя: «Trijumf» и «Trijumf Selection» отличаются одним словом
    и при этом разные вина, а таких пар в данных две сотни.
    """
    put_f = os.path.join(RYADOM, "sinonimy-vin.json")
    if not os.path.exists(put_f):
        return {}
    d = json.load(open(put_f, encoding="utf-8"))["vina"]
    svod = {}
    for hozyaistvo, vina in d.items():
        hoz = klyuch_hozyaistva(hozyaistvo)
        for imya, z in vina.items():
            for v in z["varianty"]:
                svod[(hoz, klyuch(latinicej(v)).replace("-", " "))] = imya
    return svod


def _marki():
    """Варианты, которые именем хозяйства не являются.

    «Belina» у Матијашевића, «Amante» у Рубина, «Tri Sunca» у
    Фрушкогорског — марка или сорт, попавшие у источника в поле
    производителя. Хозяйство они называют верно, поэтому в списке
    синонимов стоят; но снимать их с начала имени вина нельзя:
    «Belina Oranž» без «Belina» становится другим вином.
    """
    put_f = os.path.join(RYADOM, "sinonimy-hozyaistv.json")
    if not os.path.exists(put_f):
        return set()
    d = json.load(open(put_f, encoding="utf-8"))["hozyaistva"]
    return {_bazovyj_klyuch(m) for z in d.values() for m in z.get("marki", ())}


def bez_skobok(imya):
    """«Винарија Тришић (Vinarija Trišić)» — это «Vinarija Trišić».

    Часть сербских хозяйств Vivino держит кириллицей, дописывая латинскую
    расшифровку в скобках, а Decanter и Falstaff знают только латинское
    имя. Без этого одно хозяйство стоит в таблице дважды, и рејон
    достаётся только латинской записи.

    Скобки берутся, только если внутри латиница: у «Aglaya (Аглая)»
    и «Vinarija Novak (Новак)» в скобках, наоборот, кириллица, и там
    основное имя как раз перед скобками.
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


# Сербская кириллица и латиница переводятся одна в другую однозначно,
# поэтому сводить их можно без догадок. Двубуквенные идут первыми: иначе
# «њ» распадётся на «n» и «j» по одному, а «џ» — на «d» и «z».
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


def est_kirillica(s):
    return any("\u0400" <= z <= "\u04ff" for z in s or "")


def odno_imya_dvumya_alfavitami(vino):
    """«Три Мораве (Tri Morave)» → «Tri Morave»: то же имя, другой алфавит.

    Vivino держит часть сербских вин кириллицей, дописывая латиницу
    в скобках, а конкурсы знают только латинское имя. Без сведения одно
    вино стоит двумя строками: оценка покупателей на одной, медаль
    на другой, и ни на одной нет обеих.

    Скобки снимаются, только если в них ровно перевод головы буква
    в букву. Этого мало для «Морава Глина (Morava Clay)» — там перевод
    смысла, а не письма, — и это нарочно: «Тома Здравковиђ Бело (Toma
    Zdravković Red)» и «... (Toma Zdravković White)» иначе слиплись бы
    в одно вино, а это две разные позиции каталога.
    """
    itog = (vino or "").strip()
    for sovpalo in list(re.finditer(r"\(([^()]+)\)", itog)):
        vnutri = sovpalo.group(1)
        mesto = itog.find(sovpalo.group(0))
        if est_kirillica(vnutri):
            # Обратный случай: имя латиницей, в скобках оно же кириллицей —
            # «Filigran Merlot (Филигран Мерлот)». Скобки просто снимаются.
            slova = itog[:mesto].rstrip().split()
            for skolko in range(1, min(len(slova), 8) + 1):
                hvost = " ".join(slova[-skolko:])
                if est_kirillica(hvost) or klyuch(hvost) != klyuch(latinicej(vnutri)):
                    continue
                itog = re.sub(r"\s+", " ", (itog[:mesto]
                              + itog[mesto + len(sovpalo.group(0)):])).strip()
                break
            continue
        if mesto < 0:
            continue
        slova = itog[:mesto].rstrip().split()
        for skolko in range(1, min(len(slova), 8) + 1):
            hvost = " ".join(slova[-skolko:])
            if not est_kirillica(hvost) or klyuch(latinicej(hvost)) != klyuch(vnutri):
                continue
            zamena = (" ".join(slova[:-skolko]) + " " + vnutri
                      + itog[mesto + len(sovpalo.group(0)):])
            zamena = re.sub(r"\s+", " ", zamena).strip()
            # Если кириллица осталась, скобки покрыли только часть имени:
            # «Гмитар Прокупац (Prokupac)» превратилось бы в «Гмитар
            # Prokupac» — смесь двух алфавитов вместо одного имени.
            if not est_kirillica(zamena):
                itog = zamena
            break
    return itog or vino


def _bazovyj_klyuch(imya):
    k = klyuch(bez_skobok(imya))
    chasti = [c for c in k.split("-") if c and c not in SLUZHEBNYE]
    return "-".join(chasti) or k


SINONIMY = {}
# Имена, объявленные в файле синонимов главными: они и показываются.
KANON_IMYA = set()
# Варианты, которые именем хозяйства не являются, — см. _marki().
MARKI = set()
# Написания одного вина, сведённые руками, — см. _sinonimy_vin().
SINONIMY_VIN = {}


def klyuch_hozyaistva(imya):
    """Ключ хозяйства: без служебных слов, регистра и диакритики."""
    k = _bazovyj_klyuch(imya)
    return SINONIMY.get(k, k)


# Год урожая в диапазоне живых урожаев. Раньше 1950-го — уже не урожай,
# а часть имени: «1804 Početak», «1903 Мир», «Kadarka 1880», «Bakator 1909».
GOD_UROZHAYA = re.compile(r"(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)")


def bez_goda_urozhaya(vino):
    """Убрать год урожая, попавший внутрь имени вина.

    Урожай — своё поле, и в имени ему делать нечего: «Arno 2015» и «Arno»
    у Алексића одно вино, «MERLOT 2020», «MERLOT 2021» и «Merlot»
    у Тодоровића — тоже. Источники печатают год в имени неровно, и без
    этого одно вино расходится на строку за каждый урожай.

    Число, которое годом быть не может, остаётся на месте: «Cuvée 21»,
    «Grašac 26a», «33 Premium», «Prokupac 1186», «Kadarka 1880».
    """
    ostalos = re.sub(r"\s+", " ", GOD_UROZHAYA.sub(" ", vino or "")).strip(" ,.-–—")
    return ostalos or vino


def snimaetsya(nachalo, hoz):
    """Снимать ли это начало имени вина как повтор имени хозяйства.

    Снимается, если начало называет то же хозяйство, — но не тогда,
    когда это марка или сорт, попавшие у источника в поле производителя:
    «Belina», «Amante», «Verus», «Tri Sunca». Хозяйство они называют
    верно, а из имени вина их убирать нельзя.
    """
    if _bazovyj_klyuch(nachalo) in MARKI:
        return False
    return klyuch_hozyaistva(nachalo) == hoz


def klyuch_vina(hozyaistvo, vino, snimat_povtor=True):
    """Ключ вина: хозяйство плюс имя, без повтора хозяйства в имени.

    Falstaff печатает имя хозяйства внутри названия вина — «Zvonko Bogdan
    Cuvée No 1», «Manastir Bukovo Filigran Gamay», — а Decanter и Vivino
    зовут те же вина «Cuvée No.1» и «Filigran Gamay». Без снятия повтора
    одно вино попадает в таблицу дважды и в отчёте стоит двумя строками.

    Для записей Vivino повтор не снимается: у них есть собственный
    идентификатор, и он говорит, что «Tarpos Merlot» и «Merlot» у Tarpoš —
    две разные позиции каталога. Свести их по имени значило бы решить за
    Vivino, что это одно вино, и потерять одну из двух выборок отзывов.
    """
    hoz = klyuch_hozyaistva(hozyaistvo)
    # Ключ строится по латинице: кириллическое имя вина и латинское —
    # одно вино, а не два. Перевод письма однозначен, догадок здесь нет.
    vino = bez_goda_urozhaya(odno_imya_dvumya_alfavitami(vino))
    chasti = klyuch(latinicej(vino)).split("-")
    if snimat_povtor:
        for skolko in range(len(chasti) - 1, 0, -1):
            nachalo = [c for c in chasti[:skolko] if c not in SLUZHEBNYE]
            # Через klyuch_hozyaistva, а не напрямую: в начале имени вина
            # стоит то написание хозяйства, какое дал источник, и оно
            # бывает синонимом — «Verus Chardonnay» у Киша, «Vimmid
            # Cabernet Sauvignon» у Фрунзе. Показываемое имя их снимало
            # (imya_vina сводит синонимы), а ключ — нет, и одно вино
            # расходилось на две строки с одинаковым именем.
            if snimaetsya("-".join(nachalo), hoz):
                chasti = chasti[skolko:]
                break
    # Свод написаний — последним: в списке они записаны без имени
    # хозяйства впереди, и до его снятия поиск не находил ничего.
    svedeno = SINONIMY_VIN.get((hoz, " ".join(chasti).replace("-", " ")))
    if svedeno:
        chasti = klyuch(latinicej(svedeno)).split("-")
    return hoz + "-" + "-".join(chasti)


def imya_vina(hozyaistvo, vino, snimat_povtor=True):
    """Имя вина для таблиц — без имени хозяйства в начале.

    Ключ повтор уже снимает; здесь то же самое делается с показываемым
    именем, иначе в отчёте стоит «Zvonko Bogdan · Zvonko Bogdan Cuvée
    No 1». В сырых записях имя остаётся ровно таким, как его печатает
    источник, — таблицы производные, сырьё правится только руками.
    """
    # «Три Мораве (Tri Morave)» показывается как «Tri Morave»: на этикетке
    # стоит латиница, и справочник зовёт вино так же. Сводится только
    # ровное повторение имени другим алфавитом — см. odno_imya_dvumya_alfavitami.
    vino = bez_goda_urozhaya(odno_imya_dvumya_alfavitami(vino))
    hoz = klyuch_hozyaistva(hozyaistvo)
    if snimat_povtor:
        slova = vino.split()
        for skolko in range(len(slova) - 1, 0, -1):
            if snimaetsya(" ".join(slova[:skolko]), hoz):
                vino = " ".join(slova[skolko:])
                break
    return SINONIMY_VIN.get((hoz, klyuch(latinicej(vino)).replace("-", " ")),
                            vino)


def klyuch(*chasti):
    """Устойчивый ключ: без регистра, диакритики и лишних пробелов."""
    s = " ".join(c for c in chasti if c).lower()
    # «dj» — тот же «đ», записанный без диакритики: Decanter пишет
    # «Mrdjanin», «Djurdjic», «Medje» там, где у Vivino стоит «Mrđanin»,
    # «Đurđić», «Međe». Без этого одно хозяйство разъезжается на два.
    s = s.replace("dj", "đ")
    s = s.replace("š", "s").replace("đ", "d").replace("č", "c")
    s = s.replace("ć", "c").replace("ž", "z")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    # Апостроф и точка внутри слова разделителями не работают: «King's
    # Crown» и «Kings Crown», «Cuvée No.1» и «Cuvee No1» — одно вино,
    # записанное разными руками. Пробел и дефис разделителями остаются,
    # иначе «Cabernet-Merlot» разошлось бы с «Cabernet Merlot».
    s = re.sub(r"[.'\u2019]", "", s)
    s = re.sub(r"[^a-z0-9а-я]+", "-", s)
    return s.strip("-")


def chislo_ili_nichego(znachenie):
    """Ноль у Vivino значит «нечего показать», а не «оценка ноль».

    Отдаётся он и в поле оценки, и в поле числа отзывов, и если принять
    его за значение, в таблицу попадут полторы тысячи вин с баллом 0.
    """
    if isinstance(znachenie, (int, float)) and znachenie > 0:
        return znachenie
    return None


def razobrat_stranicu(stranica):
    """Из строки-примечания вынуть идентификатор вина, адрес и оговорку.

    Писалось это руками и по-разному: «w/5027454», «wineries/erdevik»,
    «w/2115277 · профиль вкуса, нижняя граница». Разбирается здесь один раз,
    чтобы дальше в таблицах лежали чистые поля.
    """
    stranica = stranica or ""
    ogovorka = ""
    if "·" in stranica:
        stranica, ogovorka = [c.strip() for c in stranica.split("·", 1)]
    sovpalo = re.search(r"\bw/(\d+)\b", stranica)
    vivino_id = int(sovpalo.group(1)) if sovpalo else None
    adres = ""
    if stranica:
        adres = "https://www.vivino.com/" + stranica.lstrip("/")
    return vivino_id, adres, ogovorka


def nizhnyaya_granica(ogovorka):
    """Число отзывов, взятое из профиля вкуса или из отдельного урожая, —
    это не всё число оценок, а его нижняя оценка. Отмечаем явно."""
    return bool(re.search(r"нижняя граница|профиль вкуса", ogovorka or ""))


def main():
    vivino = svesti_vivino(chitat_jsonl("vivino-zapisi.jsonl"), vivino_iz_api())
    kritiki = chitat_jsonl("kritiki-zapisi.jsonl")
    nagrady_syrye = chitat_jsonl("nagrady-zapisi.jsonl")
    karta = json.load(open(put("raion-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]
    zvezdy = {klyuch_hozyaistva(z["hozyaistvo"]): z for z in
              json.load(open(put("falstaff-zvezdy.json"), encoding="utf-8"))["hozyaistva"]}

    celi = json.load(open(put("celi-spisok.json"), encoding="utf-8"))

    # Что названо в книге: хозяйства и отдельные бутылки.
    hoz_v_knige, vina_v_knige = set(), set()
    for razdel in celi["regiony"]:
        for h in razdel["hozyaistva"]:
            hoz_v_knige.add(klyuch(h["hozyaistvo"].replace("◈", "")))
        for v in razdel["vina_v_tekste"]:
            vina_v_knige.add(klyuch(v))

    def v_knige_hoz(imya):
        k = klyuch(imya)
        return any(k in kn or kn in k for kn in hoz_v_knige if kn)

    def v_knige_vino(imya):
        k = klyuch(imya)
        return any(k == kn or kn in k for kn in vina_v_knige if kn)

    # ---------------- хозяйства ----------------
    # Одно хозяйство приходит под разными именами: «Deurić», «Vinarija
    # Deurić», «Vinarija Deuric». Сводим по ключу, а показываем то имя,
    # которое знает книга; если книга его не знает — самое длинное,
    # оно обычно полнее.
    imena_knigi = {klyuch_hozyaistva(k) for k in karta}
    karta_po_klyuchu = {klyuch_hozyaistva(k): v for k, v in karta.items()}
    varianty = {}
    for z in vivino + kritiki + nagrady_syrye:
        k = klyuch_hozyaistva(z["hozyaistvo"])
        varianty.setdefault(k, set()).add(z["hozyaistvo"])
    imena = []
    for k, nabor in varianty.items():
        knizhnye = [i for i in nabor if klyuch_hozyaistva(i) in imena_knigi
                    and i in karta]
        # Ровно равные по длине варианты («Todorović» и «Todorovic»)
        # иначе выбирались как попало — от запуска к запуску имя в
        # таблицах менялось. Порядок задан явно: длиннее, с диакритикой,
        # затем по алфавиту.
        # Имя, названное в `sinonimy-hozyaistv.json`, старше длины: там
        # оно выбрано с доказательством. Иначе побеждала бы опечатка —
        # «Vista Hills Plus» длиннее, чем «Vista Hill».
        svedennoe = [i for i in nabor if i in KANON_IMYA]
        imena.append(knizhnye[0] if knizhnye else
                     svedennoe[0] if svedennoe else
                     sorted(nabor, key=lambda i: (-len(i),
                                                  -sum(z > "\x7f" for z in i),
                                                  i))[0])
    # Канонические имена выбраны; теперь всюду пишем именно их, иначе
    # в таблице вин хозяйство будет зваться иначе, чем в таблице хозяйств.
    kanon = {}
    for imya in imena:
        for variant in varianty[klyuch_hozyaistva(imya)]:
            kanon[variant] = imya

    def imya_hozyaistva(syroe):
        return kanon.get(syroe, syroe)

    for spisok in (vivino, kritiki, nagrady_syrye):
        for z in spisok:
            z["hozyaistvo"] = imya_hozyaistva(z["hozyaistvo"])

    nastoyashchee_mesto = {}
    if os.path.exists(put("rejony-hozyaistv.json")):
        nastoyashchee_mesto = json.load(
            open(put("rejony-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]

    hozyaistva = []
    for imya in sorted(imena):
        svedeniya = dict(karta_po_klyuchu.get(klyuch_hozyaistva(imya), {}))
        if not svedeniya.get("raion"):
            # Района в книге нет — попробуем по району Vivino, но только
            # если все его сербские вина указывают на одну главу.
            predlozheno = {RAION_PO_VIVINO.get(z.get("region_vivino"))
                           for z in vivino
                           if klyuch_hozyaistva(z["hozyaistvo"])
                           == klyuch_hozyaistva(imya)}
            predlozheno.discard(None)
            if len(predlozheno) == 1:
                svedeniya["raion"] = predlozheno.pop()
                svedeniya["istochnik"] = "vivino"
        slugi = {razobrat_stranicu(z.get("stranica"))[1] for z in vivino
                 if z["hozyaistvo"] == imya}
        slug = ""
        for adres in slugi:
            sovpalo = re.search(r"/wineries/([a-z0-9-]+)", adres or "")
            if sovpalo:
                slug = sovpalo.group(1)
                break
        # Настоящее место — рејон и виногорје по действующей рејонизацији.
        # Считает `sobrat-rejony.py`; здесь только подставляется. Глава
        # книги (`raion_knigi`) остаётся рядом отдельной величиной: она
        # не обязана совпадать с рејоном, и автор её ещё может менять.
        mesto = nastoyashchee_mesto.get(klyuch_hozyaistva(imya), {})
        hozyaistva.append({
            "hozyaistvo": imya,
            "klyuch": klyuch_hozyaistva(imya),
            "region": mesto.get("region"),
            "rejon": mesto.get("rejon"),
            "vinogorje": mesto.get("vinogorje"),
            # Место назначения: населённый пункт, куда ехать. Округ сюда
            # не попадает — он служебный, к виноградарству отношения
            # не имеет и в справочнике не нужен.
            "gorod": mesto.get("gorod", ""),
            "rejon_istochnik": mesto.get("istochnik", "ne_ustanovlen"),
            "rejon_raznoglasie": mesto.get("raznoglasie", ""),
            "raion_knigi": svedeniya.get("raion"),
            "raion_istochnik": svedeniya.get("istochnik", "ne_ustanovlen"),
            "gde": svedeniya.get("gde", "") or mesto.get("gde", ""),
            "v_knige": v_knige_hoz(imya),
            "vivino_slug": slug,
            "falstaff_zvezd": zvezdy.get(klyuch_hozyaistva(imya), {}).get("zvezd"),
            "vin_v_dannyh": sum(1 for z in vivino
                                if klyuch_hozyaistva(z["hozyaistvo"])
                                == klyuch_hozyaistva(imya)),
        })

    # ---------------- вина ----------------
    vina, vidano = [], {}
    for z in vivino:
        k = klyuch_vina(z["hozyaistvo"], z["vino"], snimat_povtor=False)
        vivino_id, adres, _ = razobrat_stranicu(z.get("stranica"))
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                # Повтор имени хозяйства у записей Vivino не снимается —
                # см. klyuch_vina, — но кириллическое написание с латинской
                # расшифровкой в скобках приводится к латинице: на этикетке
                # стоит она.
                "vino": imya_vina(z["hozyaistvo"], z["vino"],
                                  snimat_povtor=False),
                "vivino_id": vivino_id,
                "vivino_adres": adres if vivino_id else "",
                # «Мало оценок» — тоже сведение: Vivino прячет оценку, пока
                # отзывов слишком мало. Пустое поле и такой ответ — разное.
                "vivino_status": ("ocenka_est"
                                  if chislo_ili_nichego(z.get("ocenka"))
                                  else "malo_ocenok"),
                # Охват: сколько человек сфотографировали этикетку.
                "etiketok": chislo_ili_nichego(z.get("etiketok")),
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
        elif not vidano[k].get("etiketok") and z.get("etiketok"):
            vidano[k]["etiketok"] = chislo_ili_nichego(z.get("etiketok"))
        elif vivino_id and not vidano[k]["vivino_id"]:
            vidano[k]["vivino_id"] = vivino_id
            vidano[k]["vivino_adres"] = adres
    for z in nagrady_syrye:
        if not z["vino"]:
            continue          # награда хозяйству, а не вину
        k = klyuch_vina(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": imya_vina(z["hozyaistvo"], z["vino"]),
                "vivino_id": None,
                "vivino_adres": "",
                "vivino_status": "net_na_vivino",
                "etiketok": None,
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
    for z in kritiki:
        k = klyuch_vina(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": imya_vina(z["hozyaistvo"], z["vino"]),
                "vivino_id": None,
                "vivino_adres": "",
                "vivino_status": "net_na_vivino",
                "etiketok": None,
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": True,
            }
        else:
            vidano[k]["est_u_kritikov"] = True
    vina = sorted(vidano.values(), key=lambda z: (z["hozyaistvo"], z["vino"]))

    # ---------------- оценки, длинный вид ----------------
    ocenki = []
    for z in vivino:
        if chislo_ili_nichego(z.get("ocenka")) is None:
            continue
        _, adres, ogovorka = razobrat_stranicu(z.get("stranica"))
        ocenki.append({
            "klyuch_vina": klyuch_vina(z["hozyaistvo"], z["vino"],
                                       snimat_povtor=False),
            "hozyaistvo": z["hozyaistvo"],
            "vino": imya_vina(z["hozyaistvo"], z["vino"], snimat_povtor=False),
            "istochnik": "vivino",
            "shkala": 5,
            "ball": z["ocenka"],
            "vyborka": chislo_ili_nichego(z.get("chislo_ocenok")),
            "vyborka_nizhnyaya_granica": nizhnyaya_granica(ogovorka),
            "god": None,
            "konkurs_god": None,
            "cvet": "",
            "ogovorka": ogovorka,
            "stranica": adres,
            "sobrano": SOBRANO,
        })
    for z in kritiki:
        if z.get("ball") is None:
            continue
        ocenki.append({
            "klyuch_vina": klyuch_vina(z["hozyaistvo"], z["vino"]),
            "hozyaistvo": z["hozyaistvo"],
            "vino": imya_vina(z["hozyaistvo"], z["vino"]),
            "istochnik": z["istochnik"],
            "shkala": 100,
            "ball": z["ball"],
            "vyborka": None,
            "vyborka_nizhnyaya_granica": False,
            "god": int(z["god"]) if z.get("god") else None,
            "konkurs_god": z.get("konkurs_god"),
            # Цвет отличает одно измерение от другого: «Tri Morave»
            # у Темета — и красное, и розовое, и белое игристое, и на
            # одном конкурсе они получают разные баллы. Имя вина у них
            # общее, поэтому без цвета это выглядит повтором.
            "cvet": z.get("cvet") or "",
            "ogovorka": "",
            "stranica": z.get("stranica", ""),
            "sobrano": SOBRANO,
        })

    # Одно и то же измерение дважды. Такое выходит, когда источник
    # напечатал вино двумя написаниями — BIWC 2025 дал «Atila Chardonay»
    # и «Atila Chardonnay» с одним и тем же баллом, — а свод написаний
    # сделал из них одно вино. Балл при этом не меняется, и вторая
    # строка ничего не добавляет. Если бы баллы разошлись, обе строки
    # остались бы: это уже расхождение источника, и его видно в проверке.
    vidano_izmerenie, bez_povtorov, snyato = set(), [], 0
    for z in ocenki:
        k = (z["klyuch_vina"], z["istochnik"], z["god"], z.get("konkurs_god"),
             z.get("cvet") or "", z["ball"])
        if k in vidano_izmerenie:
            snyato += 1
            continue
        vidano_izmerenie.add(k)
        bez_povtorov.append(z)
    if snyato:
        print("оценок-повторов снято: %d (то же вино, источник, урожай и балл)"
              % snyato)
    ocenki = bez_povtorov

    # ---------------- награды ----------------
    nagrady = [{
        "klyuch_vina": (klyuch_vina(z["hozyaistvo"], z["vino"])
                        if z["vino"] else ""),
        "hozyaistvo": z["hozyaistvo"],
        "vino": imya_vina(z["hozyaistvo"], z["vino"]),
        "istochnik": z["istochnik"],
        "god": z["god"],
        "kategoriya": z["kategoriya"],
        "mesto": z["mesto"],
        "urozhaj": z["urozhaj"],
        "cvet": z.get("cvet") or "",
        "stranica": z["stranica"],
        "sobrano": SOBRANO,
    } for z in nagrady_syrye]

    for imya, tablica in (("hozyaistva", hozyaistva), ("vina", vina),
                          ("ocenki", ocenki), ("nagrady", nagrady)):
        with open(put(imya + ".jsonl"), "w", encoding="utf-8") as f:
            for s in tablica:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        with open(put(imya + ".csv"), "w", encoding="utf-8", newline="") as f:
            pero = csv.DictWriter(f, fieldnames=list(tablica[0].keys()))
            pero.writeheader()
            pero.writerows(tablica)
        print("%-12s %4d строк → %s.jsonl, %s.csv" % (imya, len(tablica), imya, imya))


SINONIMY.update(_sinonimy())
MARKI.update(_marki())
SINONIMY_VIN.update(_sinonimy_vin())
KANON_IMYA.update(
    json.load(open(os.path.join(RYADOM, "sinonimy-hozyaistv.json"),
                   encoding="utf-8"))["hozyaistva"]
    if os.path.exists(os.path.join(RYADOM, "sinonimy-hozyaistv.json")) else {})


if __name__ == "__main__":
    main()
