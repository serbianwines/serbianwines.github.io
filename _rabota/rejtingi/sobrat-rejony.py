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
    (None, None): (None, None),
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
    for a, b in (("š", "s"), ("đ", "d"), ("č", "c"), ("ć", "c"), ("ž", "z")):
        s = s.lower().replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9а-я]+", "-", s).strip("-")


def klyuch_mesta(*chasti):
    """Ключ места — с переводом кириллицы в латиницу."""
    return prostoj_klyuch(latinicej(" ".join(c for c in chasti if c)))


SLUZHEBNYE = ("vinarija", "podrum", "podrumi", "vinogradi", "vinska-kuca",
              "vinarska-kuca", "gazdinstvo", "winery", "estate", "manastir",
              "monastery")


def bez_skobok(imya):
    """«Винарија Тришић (Vinarija Trišić)» — это «Vinarija Trišić».

    То же правило, что в `sobrat-tablicy.py`: латинская расшифровка в
    скобках заменяет кириллическое имя. Скобки с кириллицей внутри
    («Aglaya (Аглая)») наоборот отбрасываются.
    """
    sovpalo = re.search(r"^(.+?)\s*\(([^()]+)\)\s*$", imya)
    if not sovpalo:
        return imya
    v_skobkah = sovpalo.group(2)
    if any("\u0400" <= z <= "\u04ff" for z in v_skobkah):
        return sovpalo.group(1)
    return v_skobkah


def klyuch_hozyaistva(imya):
    """Ключ хозяйства — ровно тот же, что в `sobrat-tablicy.py`.

    Кириллица сама по себе в латиницу здесь не переводится — только
    через скобки: ключи обязаны совпадать с остальными таблицами, иначе
    рејон не с чем будет связать.
    """
    k = prostoj_klyuch(bez_skobok(imya))
    chasti = [c for c in k.split("-") if c and c not in SLUZHEBNYE]
    return "-".join(chasti) or k


# ---------------------------------------------------------------- справочник
def spravochnik():
    d = json.load(open(put("rejony-vinogorja.json"), encoding="utf-8"))
    po_rejonu = {r["rejon"]: r for r in d["rejony"]}
    IMYA_REJONA.update({r["kod"]: r["rejon"] for r in d["rejony"]})
    # город → рејон и город → виногорје, для показаний по месту
    gorod_rejon, gorod_vinogorje = {}, {}
    for r in d["rejony"]:
        for o in r["opstine"]:
            gorod_rejon.setdefault(klyuch_mesta(o), set()).add(r["rejon"])
        for v in r["vinogorja"]:
            for o in v["katastarske_opstine"]:
                gorod_vinogorje.setdefault(klyuch_mesta(o), set()).add(
                    (r["rejon"], v["vinogorje"]))
    # Справочник vinarijesrbije знает ещё сотню мест, которых нет в списке
    # общин: сёла и части городов. Рејон по ним ставится так же.
    if os.path.exists(put("vinarijesrbije-mesta.json")):
        vs = json.load(open(put("vinarijesrbije-mesta.json"), encoding="utf-8"))
        for g in vs["goroda"]:
            kod = SLUG_REJONA.get(g["rejon_slug"], g["rejon_slug"])
            if IMYA_REJONA.get(kod):
                gorod_rejon.setdefault(klyuch_mesta(g["gorod"]), set()).add(
                    IMYA_REJONA[kod])
    return d, po_rejonu, gorod_rejon, gorod_vinogorje


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
            para = (bez_pustogo(w.get("region")), bez_pustogo(w.get("subRegion")))
            if para not in DECANTER_PARA:
                para = (para[0], None)
            rejon, vinogorje = DECANTER_PARA.get(para, (None, None))
            p[klyuch_hozyaistva(w["producer"])].append({
                "istochnik": "decanter", "syroe": " · ".join(x for x in para if x),
                "rejon": rejon, "vinogorje": vinogorje})

    if os.path.exists(put("vivino-syrye.json")):
        for w in json.load(open(put("vivino-syrye.json"), encoding="utf-8"))["vina"]:
            syroe = w.get("region_vivino") or w.get("region")
            if not w.get("hozyaistvo") or not syroe:
                continue
            p[klyuch_hozyaistva(w["hozyaistvo"])].append({
                "istochnik": "vivino", "syroe": syroe,
                "rejon": VIVINO_REJON.get(syroe), "vinogorje": None})

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


def po_mestu(gde, gorod_rejon, gorod_vinogorje):
    """Рејон и виногорје по городу хозяйства, если он назван однозначно.

    В карте книги в этом поле не только город: «Вршац. Внимание: …»,
    «Земун; фрушкогорские этикетки, но…». Берём то, что стоит до первого
    знака препинания, — дальше идёт замечание, а не место.
    """
    if not gde:
        return None, None, ""
    gde = re.split(r"[,;.(]", gde)[0].strip()
    if not gde:
        return None, None, ""
    # В поле не только место: «Гроцка под Белградом», «Малча под Нишем».
    # Пробуем целиком, потом отбрасываем по слову с конца — так «Нови
    # Сланкамен» находится целиком, а «Гроцка под Белградом» находится
    # как «Гроцка», не превращаясь по дороге в «Нови».
    slova = gde.split()
    for skolko in range(len(slova), 0, -1):
        chast = " ".join(slova[:skolko])
        k = klyuch_mesta(chast)
        r = gorod_rejon.get(k, set())
        v = gorod_vinogorje.get(k, set())
        # Сперва рејон по списку общин, и только потом виногорје внутри
        # него. Имена мест по стране повторяются: «Topola» — и община
        # Шумадијског рејона, и кадастровое село Јагодинског виногорја.
        # Если искать сразу виногорје, Александровић уезжает из Шумадије.
        if len(r) == 1:
            rejon = next(iter(r))
            svoi = {vg for rj, vg in v if rj == rejon}
            return rejon, (next(iter(svoi)) if len(svoi) == 1 else None), chast
        if len(v) == 1:
            # Общины рејон не назвали, но виногорје на всю страну одно —
            # так находится Крњево, которое общиной не является.
            rejon, vinogorje = next(iter(v))
            return rejon, vinogorje, chast
    return None, None, ""


def main():
    d, po_rejonu, gorod_rejon, gorod_vinogorje = spravochnik()
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
        # Город: сперва из книги, иначе из справочника винарий. Он нужен
        # не только ради рејона — по нему же находится и виногорје.
        gde = gde_po_klyuchu.get(k, "") or next(
            (x["gorod"] for x in pok if x.get("gorod")), "")
        m_rejon, m_vinogorje, m_gde = po_mestu(gde, gorod_rejon, gorod_vinogorje)

        raznoglasie = ""
        # Место — старше всего. Справочник винарий пишет Vino Budimir
        # в Сремски рејон, а адресом даёт Александровац, то есть Жупу:
        # ярлык у них ошибочный, адрес — нет. Поэтому если город найден
        # однозначно, он и решает, даже когда источник один.
        if m_rejon:
            rejon, istochnik = m_rejon, "mesto"
            if rejony and set(rejony) != {m_rejon}:
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
            raznoglasie = "; ".join("%s ×%d" % (r, n) for r, n in rejony.most_common())
            spor.append((k, dict(rejony), m_rejon, rejon))

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

        itog[k] = {
            "hozyaistvo": imya_po_klyuchu.get(k, k),
            "region": po_rejonu.get(rejon, {}).get("region"),
            "rejon": rejon,
            "vinogorje": vinogorje,
            "istochnik": istochnik if rejon else "ne_ustanovlen",
            "raznoglasie": raznoglasie,
            "gde": gde,
            "pokazaniya": sorted({"%s: %s" % (x["istochnik"], x["syroe"])
                                  for x in pok}),
        }

    json.dump({"chto_eto": "Настоящий рејон и виногорје каждого хозяйства — "
                           "по действующей рејонизацији, не по главам книги.",
               "spravochnik": "rejony-vinogorja.json",
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


if __name__ == "__main__":
    main()
