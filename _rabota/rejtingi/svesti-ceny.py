# -*- coding: utf-8 -*-
"""Свести цены магазинов с нашей таблицей вин.

Цены лежат сырьём, как их печатает каждый магазин: `vinoteka-ceny.json`,
`winestars-ceny.json`. Одного магазина мало — это его ассортимент, а не
сербская полка, — поэтому источников несколько, а у вина остаётся
и средняя цена, и разброс между магазинами. Свод
вынесен отдельно нарочно: он неточен, и его неточность надо видеть,
а не прятать внутри сборщика.

Магазин зовёт вина короче нас: «Erdevik Bella Novela» — это наша «Bella
Novela Sauvignon Blanc», «Janko Mesečina» — «Mesečina Penušavo Belo».
Поэтому после точного ключа пробуется совпадение по началу имени, но
**только когда в доме подходит ровно одно вино**. Если подходит несколько
— «Chardonnay» годится и «Chardonnay barrique», и «Classic Chardonnay», —
цена не ставится: это разные вина, и выбирать между ними наугад нельзя.

Совпадение по началу имени — единственное место, где решение принимается
похожестью, и на нём же держатся два предохранителя. Первый: цвет,
названный магазином в имени товара, обязан не противоречить нашему —
иначе цена красного встаёт белому. Второй: чистить магазинное имя можно
только от слов, которые вина не называют; цвет и сахар из имени не
снимаются. Пары, сведённые похожестью, печатаются по `SVESTI_CENY_POKAZAT=1`
— их надо перечитывать глазами, механической проверки тут нет.

Пишет `ceny-vin.json`: ключ вина → цена, и отдельно список несведённого.
"""
import importlib.util, json, os, pathlib, re, statistics, sys, collections

ZDES = pathlib.Path(__file__).resolve().parent


def tablicy():
    """Ключи вин строит `sobrat-tablicy.py`; берём их оттуда, не повторяя."""
    spec = importlib.util.spec_from_file_location("st", ZDES / "sobrat-tablicy.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


# Магазин дописывает к имени условия акции и объём бутылки. Ни то, ни
# другое к вину не относится: «AKCIJA 2+1 Malča Anonymus» — та же
# «Anonymus», а «Grand Trianon 1,5L» — тот же «Grand Trianon».
AKCIYA = re.compile(r"^\s*AKCIJA\b[^A-Za-zČĆŠĐŽčćšđž]*", re.I)
# Урожай в конце имени — свойство бутылки, а не имя вина: «Aleksić
# Bonaca 2023» это наша «Bonaca». Ни одно наше имя годом не кончается,
# так что снимать его безопасно.
UROZHAJ = re.compile(r"[\s,]*\b(19[5-9]\d|20[0-2]\d)\s*$")
# Супермаркет зовёт товар по ярлыку полки: «Vino belo Chardonnay
# Kovacevic 0,75l». Слова «вино», цвет и «стоно» имени вина не называют,
# а начало имени у нас — как раз то, по чему идёт сведение. Без их снятия
# из ста шестидесяти шести позиций Maxi сходились три.
# «Crno» в списке не было, и «Vino crno Petit Verdot Grumen» не сходилось
# ни с чем: слово оставалось впереди имени вина. У Maxi красное зовётся
# и «crveno», и «crno», у обоих есть женский и мужской род.
YARLYK = re.compile(r"^\s*(?:vino|stono|kvalitetno|vrhunsko|belo|beli|bela|"
                    r"crveno|crveni|crvena|crno|crni|crna|bijelo|roze|rose|"
                    r"ruzicasto|penusavo|blago\s+penusavo|"
                    r"suvo|polusuvo|poluslatko)\b[\s,-]*", re.I)
# Дробная часть бывает любой длины: 1,5 л, 0,5 л, 0,375 л. Первая
# редакция читала только один знак после запятой и полубутылку Маканы
# («Makana 0.375L», 2970 динаров) приняла за обычную.
OBEM = re.compile(r"\b(\d(?:[.,]\d+)?)\s*L\b", re.I)
# Ярлык полки стоит не только в начале имени. Idea пишет его после имени
# дома — «Aleksić vinarija vino belo bonaca 0,75l», — а объём в конце
# мешает сведению по началу имени: «erdevik-bella-novela-0-75l» не
# сходится с нашей «Bella Novela Sauvignon Blanc», потому что «0» и
# «75l» встают посреди сравнения. Поэтому есть второй, вычищенный вид
# имени; он пробуется, только когда обычный не дал пары.
# Снимаются только слова, которые вина не называют и вин не различают.
# Цвет и сахар («belo», «crveno», «roze», «suvo», «poluslatko») сюда не
# входят нарочно: они стоят в именах самих вин и различают соседние
# бутылки одного дома. Первая редакция снимала и их — и приписала
# «Cilić Onyx Crveno» цену белого «Onyx Belo», а три разных «Tri Koze»
# Ердевика свела в одно вино. Указатель с так же вычищенными нашими
# именами от этого не спас: когда в доме есть только белый, красный
# сходится с ним однозначно и молча.
YARLYK_SLOVO = re.compile(r"\b(?:vino|vina|stono|kvalitetno|vrhunsko)\b", re.I)
LYUBOJ_OBEM = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:l|ml)\b", re.I)


def bez_yarlykov(imya):
    """Имя без слов полки и без объёма. Пустое имя не возвращается:
    у вина, названного одним «Roze», чистить нечего."""
    korotko = LYUBOJ_OBEM.sub(" ", imya or "")
    korotko = YARLYK_SLOVO.sub(" ", korotko)
    korotko = re.sub(r"[\s,\-]+", " ", korotko).strip()
    return korotko or (imya or "").strip()


def chistoe_imya(imya, yarlyk=False):
    """`yarlyk` — снимать ли ярлык полки. Только у супермаркета: в винотеке
    «Rose» в начале имени бывает частью имени, а не цветом на ценнике."""
    imya = UROZHAJ.sub("", AKCIYA.sub("", imya or ""))
    # Ярлык снимается по слову: у «Vino blago penusavo belo Una» их четыре
    # подряд, а у «Vinarija Coka» первое слово — имя дома, не ярлык.
    while yarlyk:
        korotko = YARLYK.sub("", imya, count=1)
        if korotko == imya or not korotko.strip():
            break
        imya = korotko
    return re.sub(r"\s+", " ", imya).strip()


def nacenka(po_magazinu, supermarkety):
    """Насколько супермаркет дороже винотеки на одном и том же вине."""
    otnosheniya = []
    for magaziny in po_magazinu.values():
        polka = [c for m, c in magaziny.items() if m in supermarkety]
        lavka = [c for m, c in magaziny.items() if m not in supermarkety]
        if polka and lavka:
            otnosheniya.append(statistics.median(polka) / statistics.median(lavka))
    if not otnosheniya:
        return {}
    return {"vin_v_oboih": len(otnosheniya),
            "nacenka_supermarketa": round(statistics.median(otnosheniya), 3),
            "deshevle_v_supermarkete": sum(1 for x in otnosheniya if x < 1)}


def sladost_zapisi_(zapis):
    """«suvo» у одного магазина и «Suvo» у другого — одно и то же.
    Без приведения в таблице стоят обе записи, и счёт по сахару врёт."""
    zapis = re.sub(r"\s+", " ", (zapis or "").strip())
    return zapis[:1].upper() + zapis[1:].lower() if zapis else ""


def ne_ta_butylka(imya):
    """Магнум — другой товар и другая цена, а имя вина то же.

    Снимать объём из имени нельзя: цена полуторалитровой бутылки встанет
    обычной. «Rodoslov Grand Reserve» стоит 5025 динаров, а он же 1,5 л —
    13 990. Поэтому нестандартный объём просто пропускается.
    """
    sovpalo = OBEM.search(imya or "")
    return bool(sovpalo) and sovpalo.group(1).replace(",", ".") != "0.75"


# Цвет, названный магазином прямо в имени товара. Ищется только в хвосте,
# после снятого имени дома: «Belo Brdo» — хозяйство, а не белое вино.
CVET_V_IMENI = [
    ("белое", {"belo", "beli", "bela", "bele", "bijelo", "blanc", "white"}),
    ("красное", {"crveno", "crveni", "crvena", "crno", "crna", "crni", "red"}),
    ("розе", {"roze", "rose", "ruzicasto", "rosé"}),
]


# Цвет, названный магазином отдельным полем. Это надёжнее, чем слово
# в имени: «Prodaja vina» пишет его значком товара, а не ярлыком полки.
CVET_POLYA = {"belo vino": "белое", "crveno vino": "красное",
              "rose vino": "розе", "roze vino": "розе"}


def cvet_iz_imeni(slova_hvosta):
    najdeno = {c for c, nabor in CVET_V_IMENI if nabor & set(slova_hvosta)}
    return najdeno.pop() if len(najdeno) == 1 else None


def slova(st, imya):
    return [c for c in st.klyuch(st.latinicej(imya or "")).split("-") if c]


def main():
    st = tablicy()
    MAGAZINY = [("vinoteka", "vinoteka-ceny.json"),
                ("winestars", "winestars-ceny.json"),
                ("cerpromet", "cerpromet-ceny.json"),
                ("wineart", "wineart-ceny.json"),
                ("prodajavina", "prodajavina-ceny.json"),
                ("maxi", "maxi-ceny.json"),
                # Обязательный ценовник той же сети — другой срез, не
                # витрина интернет-магазина, а полка гипермаркета.
                # Держится отдельным источником: у него своя цена
                # и свой набор товаров.
                ("maxi-cenovnik", "maxi-cenovnik-ceny.json"),
                ("idea", "idea-ceny.json"),
                # Цены, снятые автором с экрана там, где машиной не
                # берётся. В супермаркетный срез не идут: строки Wolt
                # приходят и из Maxi, и из делекатесной GUSTO, а мерить
                # полку сети по делекатесной нельзя.
                ("vruchnuyu", "ceny-vruchnuyu.json")]
    # Супермаркет — не винотека: у него другая полка и другие цены.
    # Разделение нужно, чтобы можно было спросить отдельно «что взять
    # в супермаркете», а не усреднять две разные торговли в одну.
    SUPERMARKET = {"maxi", "maxi-cenovnik", "idea"}
    syroe = {"vina": [], "istochnik": [], "sobrano": ""}
    for imya, fajl in MAGAZINY:
        put = ZDES / fajl
        if not put.exists():
            continue
        d = json.loads(put.read_text(encoding="utf-8"))
        for z in d["vina"]:
            # У Церпромета в каталоге весь мир; чужие вина нам не нужны,
            # а поле страны у него есть — им и отсекаем.
            strana = (z.get("strana") or "").lower()
            if strana and not strana.startswith("srbij"):
                continue
            # В винный раздел супермаркета попадает и ракия, и спрайцер,
            # и снятые с продажи позиции без цены.
            if not z.get("cena_rsd") or z.get("v_prodazhe") is False:
                continue
            if re.match(r"\s*(rakija|spricer|viljamovka)\b", z["vino"], re.I):
                continue
            syroe["vina"].append({**z, "magazin": imya})
        syroe["istochnik"].append(d["istochnik"])
        syroe["sobrano"] = max(syroe["sobrano"], d["sobrano"])
    vina = [json.loads(s) for s in (ZDES / "vina.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]

    # Полка супермаркета сама по себе — величина, на которую в тексте
    # ссылаются («медиана бутылки столько-то»). Считается здесь, чтобы
    # число в книге не расходилось с тем, что лежит в файлах.
    polka = [z for z in syroe["vina"]
             if z["magazin"] in SUPERMARKET and z.get("cena_rsd")]
    obychnye = [z["cena_rsd"] for z in polka
                if (z.get("litrov") or 0.75) == 0.75]
    polka_svodka = {
        "magaziny": sorted({z["magazin"] for z in polka}),
        "pozicij_s_cenoj": len(polka),
        "iz_nih_0_75": len(obychnye),
        "mediana_0_75": round(statistics.median(obychnye)) if obychnye else None,
    }
    vinoteki = [z["cena_rsd"] for z in syroe["vina"]
                if z["magazin"] not in SUPERMARKET and z.get("cena_rsd")
                and (z.get("litrov") or 0.75) == 0.75]
    polka_svodka["mediana_vinoteki"] = (round(statistics.median(vinoteki))
                                        if vinoteki else None)

    # Наши вина, разложенные по дому: имя в словах → ключ.
    po_domu = collections.defaultdict(list)
    # То же, но именами без слов полки и без объёма. Второй указатель
    # нужен, чтобы вычищенное имя магазина сравнивалось с так же
    # вычищенным нашим: «Aurelius Belo» и «Aurelius Crveni» без цвета
    # обе становятся «Aurelius», подходят обе — и цена не ставится
    # ни одной. Чистить только магазинное имя было бы опасно: цена
    # белого встала бы красному, будь красный в доме единственным.
    po_domu_bez = collections.defaultdict(list)
    for v in vina:
        po_domu[st.klyuch_hozyaistva(v["hozyaistvo"])].append(
            (slova(st, v["vino"]), v["klyuch"]))
        po_domu_bez[st.klyuch_hozyaistva(v["hozyaistvo"])].append(
            (slova(st, bez_yarlykov(v["vino"])), v["klyuch"]))
    nashi = {v["klyuch"] for v in vina}
    nash_cvet = {v["klyuch"]: v.get("cvet") for v in vina}

    # Сорт узнаётся по ключу, а не по написанию: у «vino prokupac»
    # служебное слово ключом снимается, и остаётся «prokupac» — тот самый
    # призрак из поля производителя Decanter. Без сравнения по ключу
    # «Ukusi moga kraja vino prokupac» доставался ему.
    KLYUCHI_SORTOV = {st.klyuch_hozyaistva(x) for x in st.SORT_NE_DOM}

    def dom_iz_imeni(imya):
        """Хозяйство по началу имени вина.

        У сотни с лишним позиций магазин оставил поле производителя
        пустым, а имя дома при этом стоит первым словом самого вина:
        «Aleksandrović Trijumf», «Kovačević Aurelius». Берётся самое
        длинное начало, которое оказывается известным нам домом:
        «Zvonko Bogdan» длиннее и точнее, чем «Zvonko».
        """
        chasti = [c for c in (imya or "").split()
                  if not re.fullmatch(r"\d+(?:[.,]\d+)?\s*(?:l|ml)?", c, re.I)]
        # Имя дома стоит и в конце: Maxi пишет «Vino belo Sauvignon Blanc
        # Djurdjic 0.75l». Хвост пробуется первым — он вернее начала:
        # в начале обычно сорт.
        for skolko in range(min(4, len(chasti) - 1), 0, -1):
            konec = " ".join(chasti[-skolko:])
            klyuch = st.klyuch_hozyaistva(konec)
            if klyuch in KLYUCHI_SORTOV:
                continue
            if klyuch in po_domu:
                return konec
        for skolko in range(min(4, len(chasti) - 1), 0, -1):
            nachalo = " ".join(chasti[:skolko])
            # Сорт хозяйством не считается: список общий, в
            # `sobrat-tablicy.py`, чтобы не расходился по скриптам.
            klyuch = st.klyuch_hozyaistva(nachalo)
            if klyuch in KLYUCHI_SORTOV:
                continue
            if klyuch in po_domu:
                return nachalo
        return ""

    # Ключ вина → магазин → все его цены на это вино. Список, а не одно
    # число: магазин различает вина тоньше нас — «Tri Morave crveno»,
    # «…belo», «…rose» и «…Rezerva» у нас одна строка «Tri Morave», —
    # и брать первую попавшуюся цену нельзя.
    po_magazinam = collections.defaultdict(lambda: collections.defaultdict(list))
    sladost = {}                                  # ключ вина → «Suvo», «Poluslatko»…
    spor, netu = [], []
    schet = collections.Counter()
    iz_imeni = 0          # считается отдельно: это не исход, а способ
    for z in syroe["vina"]:
        if not z.get("cena_rsd"):
            continue
        imya = chistoe_imya(z["vino"], yarlyk=z["magazin"] in SUPERMARKET)
        # Объём магазин пишет то в имени, то отдельным полем. Поле
        # надёжнее: в имени его может не быть вовсе.
        litrov = z.get("litrov")
        if litrov is not None and abs(litrov - 0.75) > 0.001:
            schet["не та бутылка (не 0,75)"] += 1
            continue
        if ne_ta_butylka(imya):
            schet["не та бутылка (не 0,75)"] += 1
            continue
        # Поле марки не всегда называет хозяйство. У Maxi под маркой
        # «Crasto» — дистрибьютор — идут «Poligraf Cuvee Molovin»,
        # «Trianon Erdevik» и «Tamjanika Bellucci», то есть вина трёх
        # разных домов. Поэтому имя дома берётся из имени товара не
        # только когда поле пусто, но и когда в нём стоит незнакомое нам
        # имя: своё оно вернёт, чужое — нет, а хуже не станет.
        #
        # Хуже того, марка бывает знакомой и всё равно чужой: под маркой
        # «Vinarija Grumen» у Maxi лежат «Sauvignon Blanc Djurdjic»,
        # «Simonida Djurdjic» и македонский «Alexandar Bovin». Грумен
        # им поставщик, а не винодел. Поэтому если имя товара называет
        # другой известный нам дом — верить имени, а не марке: имя
        # о вине, марка о поставке.
        # Условие у подмены одно и узкое: марка перебивается только
        # тогда, когда её имени в имени товара нет вовсе. «Vino belo
        # Sauvignon Blanc Djurdjic» под маркой «Vinarija Grumen» —
        # Грумена в имени нет, значит он поставщик, и верить надо имени.
        # А «Deurić Probus 276» под маркой «Vinarija Deurić» — Деурић
        # в имени стоит, и «Probus» в конце это сорт в имени вина,
        # а не другое хозяйство. Без этой оговорки терялось тринадцать
        # цен: «Breg Sila», «Milanović Probus», «Milićević Vladavina».
        iz_tovara = dom_iz_imeni(imya)
        svoya = st.klyuch_hozyaistva(z["hozyaistvo"]) if z["hozyaistvo"].strip() else ""
        marka_v_imeni = bool(svoya) and bool(
            set(svoya.split("-")) & set(slova(st, imya)))
        if iz_tovara and not marka_v_imeni and (
                not svoya or svoya not in po_domu
                or st.klyuch_hozyaistva(iz_tovara) != svoya):
            z = {**z, "hozyaistvo": iz_tovara}
            iz_imeni += 1
        klyuch = st.klyuch_vina(z["hozyaistvo"], imya)
        if klyuch in nashi:
            schet["ключ сошёлся точно"] += 1
            po_magazinam[klyuch][z["magazin"]].append(z["cena_rsd"])
            if sladost_zapisi_(z.get("tip_vina")):
                sladost.setdefault(klyuch, sladost_zapisi_(z.get("tip_vina")))
            continue
        hoz = st.klyuch_hozyaistva(z["hozyaistvo"])
        if hoz not in po_domu:
            netu.append({**z, "pochemu": "хозяйства нет в наших таблицах"})
            schet["хозяйства нет вовсе"] += 1
            continue
        # Имя магазина без имени дома впереди — с ним и сравниваем.
        def hvost(imya_magazina):
            """Имя магазина без имени дома впереди, в словах.

            Отрезать по числу слов дома нельзя: `klyuch_vina` снимает имя
            дома не всегда целиком. У товара «Vino rose Zvonko Bogdan»
            ключ выходит `zvonko-bogdan-zvonko`, и хвост «zvonko» сошёлся
            с нашим «Zvonko 4 Bogdan Konja Debela» — розе получило цену
            совсем другого вина. Поэтому слова дома снимаются, пока они
            идут: у этого товара хвост пустеет, и цена не ставится вовсе.
            Так и надо: имя вина здесь съел ярлык полки, а «rose» —
            и есть имя вина.
            """
            polnyj = [c for c in
                      st.klyuch_vina(z["hozyaistvo"], imya_magazina).split("-") if c]
            slova_doma = set(hoz.split("-"))
            while polnyj and polnyj[0] in slova_doma:
                polnyj.pop(0)
            return polnyj

        def podobrat(bez_doma, indeks):
            """Пустой хвост — не совпадение, а его отсутствие: «Kovačević
            crveno vino» после чистки не называет вина вовсе, и подошли бы
            все вина дома, а в доме с единственным вином — оно одно."""
            if not bez_doma:
                return []
            # Совпадение слово в слово сильнее совпадения по началу.
            # «Trijumf Gold» подходит и нашему «Trijumf Gold», и нашему
            # «Trijumf» — но второе годится лишь потому, что оно короче.
            # Без этого предпочтения обе кандидатуры считались спорными
            # и цена не ставилась ни одной, хотя имя названо полностью.
            tochno = [k for nash, k in indeks[hoz] if nash == bez_doma]
            if len(tochno) == 1:
                return tochno
            return [k for nash, k in indeks[hoz]
                    if nash[:len(bez_doma)] == bez_doma
                    or bez_doma[:len(nash)] == nash]

        podoshli = podobrat(hvost(imya), po_domu)
        kak = "по началу имени"
        # Обычное имя пары не дало — пробуем вычищенное. Магазин пишет
        # на ценнике то, чего в имени вина нет: объём («Erdevik vino
        # bella novela 0,75l») и слова полки посреди имени («Aleksić
        # vinarija vino belo bonaca»). Второй заход идёт по указателю,
        # где так же вычищены и наши имена, — иначе чистка сама
        # порождала бы ложные совпадения.
        chistoe = bez_yarlykov(imya)
        if not podoshli and chistoe != imya:
            podoshli = podobrat(hvost(chistoe), po_domu_bez)
            kak = "по вычищенному имени"
        # Магазин различает вина тоньше нас: «Tri Morave» у него отдельно
        # белое, красное и розе, у нас — одна строка. Пока цвета сходятся
        # или неизвестны, это просто разброс; когда магазин прямо назвал
        # цвет, а у нашего вина стоит другой, — это разные вина, и цена
        # красного встала бы белому. Сравнивается только явный цвет
        # и только с нашими тремя: «десертное» и «игристое» цвету
        # магазина не противоречат.
        # Цвет ищется во всех словах имени товара, кроме слов имени
        # дома: супермаркет пишет его ярлыком впереди («Vino crveno
        # Kadarka Tonkovic»), а «Belo Brdo» — хозяйство, и его «belo»
        # цветом считать нельзя.
        nazvan = (CVET_POLYA.get((z.get("cvet_magazina") or "").lower())
                  or cvet_iz_imeni(set(slova(st, z["vino"])) - set(hoz.split("-"))))
        if nazvan:
            podoshli = [k for k in podoshli
                        if nash_cvet.get(k) in ("", None, nazvan)
                        or nash_cvet.get(k) not in ("белое", "красное", "розе")]
        if len(podoshli) == 1:
            # Сведение по началу имени — единственное место, где решение
            # принимается не точным ключом, а похожестью. Пары печатаются
            # по `SVESTI_CENY_POKAZAT=1`: их надо перечитывать глазами,
            # механическая проверка тут не поможет.
            if os.environ.get("SVESTI_CENY_POKAZAT"):
                print("   %-14s %-52s → %s" % (kak, z["vino"][:52], podoshli[0]))
            schet["сошлось по началу имени"] += 1
            po_magazinam[podoshli[0]][z["magazin"]].append(z["cena_rsd"])
            if sladost_zapisi_(z.get("tip_vina")):
                sladost.setdefault(podoshli[0], sladost_zapisi_(z.get("tip_vina")))
        elif podoshli:
            schet["подходит несколько — не ставим"] += 1
            spor.append({**z, "kandidaty": podoshli})
        else:
            schet["такого вина у нас нет"] += 1
            netu.append({**z, "pochemu": "дом есть, вина нет"})

    # Цена вина — середина по магазинам. Разброс сохраняется рядом:
    # одна и та же бутылка стоит в двух лавках по-разному, и делать вид,
    # что цена одна, нельзя.
    # Если у одного магазина на одно наше вино несколько цен и они
    # расходятся больше чем на четверть — это разные вина, а не разброс.
    # «Temet Tri Morave» так стоил 1755 у одного и 11 900 у другого: там
    # была «Rezerva Crveno» в деревянной шкатулке. Такую цену не ставим,
    # а записываем в спорные.
    PREDEL = 1.25
    cena, razbros, po_magazinu = {}, {}, {}
    for k, magaziny in po_magazinam.items():
        chistye = {}
        for magazin, spisok in magaziny.items():
            if max(spisok) / min(spisok) > PREDEL:
                spor.append({"klyuch_vina": k, "magazin": magazin,
                             "ceny": sorted(spisok),
                             "pochemu": "у магазина несколько разных вин "
                                        "на одну нашу строку"})
                continue
            chistye[magazin] = statistics.median(spisok)
        if not chistye:
            continue
        # Разные магазины расходятся в цене на проценты — измерено:
        # медиана отношения 0,93, крайние 0,72 и 1,11. Расхождение
        # в разы означает не рынок, а разные вина: «Temet Tri Morave»
        # у одного 1795, у другого 11 900, потому что там «Rezerva».
        # Такому вину цену не ставим вовсе.
        if len(chistye) > 1 and max(chistye.values()) / min(chistye.values()) > 2:
            spor.append({"klyuch_vina": k,
                         "ceny": {m: round(c) for m, c in chistye.items()},
                         "pochemu": "магазины расходятся в разы — похоже, "
                                    "это разные вина"})
            continue
        cena[k] = round(statistics.median(chistye.values()))
        po_magazinu[k] = {m: round(c) for m, c in chistye.items()}
        if len(chistye) > 1:
            razbros[k] = po_magazinu[k]
    # Сладость приходит только от Церпромета — «Tip vina» в карточке.
    # Больше её взять неоткуда: у Vivino есть лишь пометка «десертное»,
    # у конкурсов — колонка цвета, куда сладость попадает изредка.
    sahar = {k: v for k, v in sladost.items() if v and k in cena}
    (ZDES / "ceny-vin.json").write_text(json.dumps({
        "chto_eto": "Ключ вина → розничная цена в динарах, середина по "
                    "магазинам. Свод имён магазинов с нашими; неточности "
                    "и разброс цен перечислены рядом.",
        "istochnik": syroe["istochnik"],
        "sobrano": syroe["sobrano"],
        "magazinov_u_vina": {k: len(v) for k, v in po_magazinu.items()},
        "polka_supermarketa": {
            **polka_svodka,
            # Сколько вин полки в винотеку не попадают вовсе: это и есть
            # довод, зачем супермаркет собирать отдельно.
            "tolko_v_supermarkete": sum(
                1 for k, v in po_magazinu.items()
                if any(m in SUPERMARKET for m in v)
                and not any(m not in SUPERMARKET for m in v)),
            # Одна и та же бутылка в супермаркете и в винотеке. Полка
            # супермаркета дешевле в целом — но не потому, что там
            # дешевле то же вино, а потому, что там другое вино.
            **nacenka(po_magazinu, SUPERMARKET),
        },
        "ceny": cena,
        # Супермаркетов несколько, и цена у них не одна: берётся
        # середина по тем из них, где вино нашлось. Первая редакция
        # писала цену последнего по списку — то есть какую придётся.
        "supermarket": {k: round(statistics.median(
                            [c for m, c in v.items() if m in SUPERMARKET]))
                        for k, v in po_magazinu.items()
                        if any(m in SUPERMARKET for m in v)},
        "sahar": sahar,
        "po_magazinam": razbros,
        "podhodit_neskolko": spor,
        "ne_nashlos": netu,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print("позиций магазина с ценой: %d" % sum(schet.values()))
    for k, n in schet.most_common():
        print("   %-30s %4d" % (k, n))
    print("   (из них дом взят из имени вина: %d)" % iz_imeni)
    print("\nцена проставлена %d нашим винам из %d → ceny-vin.json"
          % (len(cena), len(vina)))
    if sahar:
        print("тип вина (суво/полуслатко) известен у %d вин" % len(sahar))
    if razbros:
        raznica = [max(v.values()) / min(v.values()) for v in razbros.values()]
        print("в двух магазинах сразу: %d вин, крайняя разница цен %.0f%%"
              % (len(razbros), (max(raznica) - 1) * 100))


if __name__ == "__main__":
    main()
