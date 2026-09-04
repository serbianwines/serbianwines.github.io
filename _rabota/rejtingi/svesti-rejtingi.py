# -*- coding: utf-8 -*-
"""Рейтинги вин: по главам и по стране целиком.

Четыре дорожки, и они говорят разное — проверено: в сильных главах
пятнадцать мест трёх пятёрок занимают 13–15 разных вин.

* **олимпиадный зачёт** — очки медалей: строгость конкурса × ступень;
* **мнение экспертов** — лучший балл по стобалльной шкале;
* **vox populi** — оценка Vivino при выборке от 25 отзывов;
* **сводная** — худший из трёх процентилей главы. Именно худший:
  «и жюри, и критик, и покупатель» — утверждение о согласии, а среднее
  согласие прячет. В сводную идут только вина со всеми тремя сигналами.

Веса конкурсов взяты из измеренной строгости — доли золота и выше среди
их наград: Decanter 4%, AWC 17%, BIWC 31%, Wine Trophy 86%.

Главы — по действующей рејонизацији, слабые рејоны под географическим
зонтиком; приём взят у самой книги, где «Банат» и «Юго-восток» уже так
устроены. Разбор — в `perestrojka-glav.md`.

Печатает пятёрку и скамейку: фактчек выбивает вино, следующее поднимается.

    python3 _rabota/rejtingi/svesti-rejtingi.py [--otchet]
"""
import argparse, collections, json, math, pathlib, statistics, sys

ZDES = pathlib.Path(__file__).resolve().parent
SKAMEJKA = 10          # столько печатается: пятёрка плюс запас на фактчек
POROG_VYBORKI = 25     # ниже средняя Vivino ничего не значит

# Строгость конкурса. Меряется долей золота и выше среди его же наград:
# у Decanter 4%, у AWC 17%, у софийского BIWC 31%, у Wine Trophy 86%.
STROGOST = {"decanter": 3, "awc-vienna": 2, "iwc": 2, "cmb": 2,
            "biwc": 1, "wine-trophy": 1, "vino.rs": 1}
STUPEN = {"best-in-show": 6, "platina": 5, "dvojno-zlato": 5, "grand-gold": 5,
          "veliko-zlato": 5, "trofej": 5, "zlato": 4, "srebro": 2,
          "bronza": 1, "commended": 0.5}
# Годовой выбор vino.rs даёт не медаль, а место в десятке, и вес ему
# поставлен измерением, а не на глаз. Мерка одна для всех отличий: какую
# долю их обладателей другие судьи оценили в 92 балла и выше. «Другие» —
# обязательно: у медали Decanter балл ставил сам Decanter, и без этой
# оговорки конкурс мерил бы сам себя.
#
#     decanter zlato      74%      место 1–5 у vino.rs   55%
#     biwc dvojno-zlato   57%      место 6–10            37%
#     decanter srebro     49%      decanter bronza       38%
#     biwc zlato          36%      awc zlato             38%
#
# Место в первой пятёрке годового выбора предсказывает качество как
# серебро Decanter (6 очков) или двойное золото BIWC (5); место с шестого
# по десятое — как бронза Decanter (3) или золото BIWC (4). Отсюда 5,5
# и 3,5. Дробить пятёрку дальше данные не дают: второе место меряется
# хуже пятого (36% против 53%), разброс на выборках по полтора десятка
# вин больше самой разницы.
MESTO_V_PYATERKE = 5.5
MESTO_V_DESYATKE = 3.5

# Что из годового выбора вообще считается наградой вину. Дизайн этикетки,
# маркетинг и «винный бренд» о вине не говорят ничего. «За свои деньги»
# говорит, но о другом: эти вина дешевле (медиана 1500 динаров против
# 1834) и по баллу слабее (медиана 90 против 92), зато стоят своих денег
# — их место в таблицах «за свои деньги», не в олимпиадном зачёте.
VINO_RS_KACHESTVO = "лучшее"
VINO_RS_ZA_DENGI = "за свои деньги"
# Насколько отличие «за свои деньги» двигает вино в наших рядах о цене.
# Мерка та же — остаток над ожиданием по цене: у всех вин с ценой и
# баллом медиана остатка 0,0; у отмеченных vino.rs «за свои деньги» —
# +1,0; у первой тройки таких — +1,7. Столько и прибавляем. Это
# соглашение, но с числами за спиной; поменять — одна строка.
BONUS_ZA_DENGI = {"tri": 2.0, "desyat": 1.0}


def stupen(mesto):
    """Вес отличия: медаль по имени, место в десятке — по номеру."""
    if mesto in STUPEN:
        return STUPEN[mesto]
    if (mesto or "").isdigit():
        nomer = int(mesto)
        return MESTO_V_PYATERKE if nomer <= 5 else MESTO_V_DESYATKE
    return 1


def ochki_vino_rs(nagrady):
    """Очки годового выбора: одно вино за один год — одно отличие.

    Общая категория и её дольки — «лучшее красное», «лучшее красное,
    местные сорта», «лучшее красное, органика» — это один и тот же
    выбор одного и того же года, нарезанный трижды. Складывать их значит
    утроить вес ровно тем винам, что попали в узкую дольку: органическому
    красному из местного сорта. Поэтому за год берётся лучшее место,
    а не сумма мест.
    """
    luchshee = {}
    for z in nagrady:
        if not z["kategoriya"].startswith(VINO_RS_KACHESTVO):
            continue
        luchshee[z["god"]] = max(luchshee.get(z["god"], 0), stupen(z["mesto"]))
    return sum(luchshee.values())

# Главы: имя → рејоны действующей рејонизације. Чачанско-краљевачки стоит
# в Трем Моравама: Западна Морава — одна из трёх Морава, и Трстеник
# с Краљевом лежат на ней же. Отдельной главы он не унесёт — одно
# хозяйство, — а другого сборного соседа у него нет.
GLAVY = [
    ("Фрушка гора (Срем)", ["Sremski rejon"]),
    ("Суботичко-хоргошка пешчара", ["Subotički rejon"]),
    ("Банат", ["Južnobanatski rejon", "Banatski rejon", "Potiski rejon"]),
    ("Бачка", ["Rejon Bačka", "Rejon Telečka"]),
    ("Три Мораве и Жупа", ["Rejon Tri Morave", "Čačansko–kraljevački rejon"]),
    ("Шумадија", ["Šumadijski rejon"]),
    ("Неготинска Крајина", ["Rejon Negotinska Krajina"]),
    ("Подунавље и Београд", ["Beogradski rejon", "Mlavski rejon"]),
    ("Подриње и Колубара", ["Pocersko Valjevski Rejon"]),
    ("Топлица", ["Toplički rejon"]),
    ("Југоисток", ["Knjaževački rejon", "Niški rejon", "Nišavski rejon",
                   "Leskovački rejon", "Vranjski rejon"]),
    ("Косово и Метохија", ["Južnometohijski rejon", "Severnometohijski rejon"]),
]
# Главы, которые забирают ещё и хозяйства без рејона, но с известным
# регионом. Пока такая одна: Лакићевић стоит в Лепосавићу, а Лепосавић
# в рејонизацију не входит — ни в Севернометохијски рејон, ни в
# Јужнометохијски. Косово он от этого быть не перестаёт.
REGION_GLAVY = {"Косово и Метохија": "Kosovo i Metohija"}
CVETA = [("красное", "Красные"), ("белое", "Белые"), ("розе", "Розе")]


def chitat():
    jl = lambda imya: [json.loads(s) for s in
                       (ZDES / imya).read_text(encoding="utf-8").splitlines() if s.strip()]
    cena, supermarket, polka_svodka, u_hozyaistva = {}, {}, {}, {}
    dostavka = {}
    put = ZDES / "ceny-vin.json"
    if put.exists():
        d = json.loads(put.read_text(encoding="utf-8"))
        cena = d["ceny"]
        supermarket = d.get("supermarket", {})
        # Числа о самой полке — сколько позиций и какая медиана —
        # считает `svesti-ceny.py`. Здесь они только печатаются:
        # руками вписанное число в тексте устаревает молча.
        polka_svodka = d.get("polka_supermarketa", {})
        # То же о третьем канале — магазине самого хозяйства.
        u_hozyaistva = dict(d.get("u_hozyaistva") or {},
                            hozyaistv=d.get("hozyaistv_s_magazinom"))
        # И о четвёртом — витрине доставки.
        dostavka = d.get("dostavka") or {}
    return jl("hozyaistva.jsonl"), jl("vina.jsonl"), jl("ocenki.jsonl"), \
        jl("nagrady.jsonl"), cena, supermarket, polka_svodka, \
        u_hozyaistva, dostavka


def razobrat():
    (hozyaistva, vina, ocenki, nagrady, cena, supermarket,
     polka_svodka, u_hozyaistva, dostavka) = chitat()
    # Цвет вина стоит в самой таблице — его сводит `sobrat-tablicy.py`.
    cvet = {v["klyuch"]: v.get("cvet") for v in vina}
    dom = {h["hozyaistvo"]: h for h in hozyaistva}
    vivino = {z["klyuch_vina"]: z for z in ocenki
              if z["istochnik"] == "vivino" and z.get("ball")}
    kritiki = collections.defaultdict(list)
    for z in ocenki:
        if z["istochnik"] != "vivino" and z.get("ball"):
            kritiki[z["klyuch_vina"]].append(z["ball"])
    medali = collections.defaultdict(list)
    for z in nagrady:
        medali[z["klyuch_vina"]].append(z)

    def ochki(k):
        svoi = medali[k]
        chuzhie = sum(STROGOST.get(z["istochnik"], 1) * stupen(z["mesto"])
                      for z in svoi if z["istochnik"] != "vino.rs")
        if EKSPERT_S_VINO_RS:
            # Выбор ушёл к экспертам — в олимпиадном зачёте его больше нет.
            return chuzhie
        return chuzhie + STROGOST.get("vino.rs", 1) * ochki_vino_rs(
            [z for z in svoi if z["istochnik"] == "vino.rs"])

    # Ранг вина внутри дорожки годового выбора — нужен «согласию трёх»,
    # чтобы поставить в ряд вино без балла критика.
    vybor = {v["klyuch"]: ochki_vino_rs(
                 [z for z in medali[v["klyuch"]] if z["istochnik"] == "vino.rs"])
             for v in vina}
    vybor = {k: v for k, v in vybor.items() if v > 0}
    rang_vino_rs = procentili(vybor)
    # Рејон вина — свой, если конкурс объявил происхождение винограда;
    # иначе рејон дома. Книга о терруаре, и место у вина от лозы.
    rejon = lambda v: v.get("rejon") or (dom.get(v["hozyaistvo"]) or {}).get("rejon")
    po_rejonu = collections.defaultdict(list)
    # Хозяйство бывает в известном месте, но вне рејонизације: Лакићевић
    # стоит в Лепосавићу, а Лепосавић не входит ни в один из двух
    # метохијских рејона. Глава о крае от этого не должна его терять,
    # поэтому вина такого дома собираются по региону.
    po_regionu = collections.defaultdict(list)
    for v in vina:
        r = rejon(v)
        if r:
            po_rejonu[r].append(v)
            continue
        region = (dom.get(v["hozyaistvo"]) or {}).get("region")
        if region:
            po_regionu[region].append(v)
    return dict(vina=vina, dom=dom, vivino=vivino, kritiki=kritiki, medali=medali,
                ochki=ochki, cena=cena, supermarket=supermarket,
                polka_supermarketa=polka_svodka,
                u_hozyaistva=u_hozyaistva,
                dostavka=dostavka,
                cvet=cvet, po_rejonu=po_rejonu, po_regionu=po_regionu,
                rang_vino_rs=rang_vino_rs)


def dinarov(skolko):
    """«1150 динаров», «1801 динар», «1802 динара». Число здесь считается,
    а не вписывается, и падеж вместе с ним."""
    if skolko is None:
        return "?"
    sto = skolko % 100
    poslednyaya = skolko % 10
    if 11 <= sto <= 14 or poslednyaya == 0 or poslednyaya >= 5:
        return "%d динаров" % skolko
    return "%d динар%s" % (skolko, "" if poslednyaya == 1 else "а")


def perechislit(slova):
    """«Idea, Roda и Maxi»: запятые между всеми, «и» перед последним.
    Без этого выходило «Idea и Roda и Mercator и Maxi»."""
    slova = list(slova)
    if len(slova) < 2:
        return "".join(slova)
    return ", ".join(slova[:-1]) + " и " + slova[-1]


def vin_shtuk(skolko):
    """«63 вин», «81 вина», «22 вина». Падеж считается, а не вписывается:
    в отчёте число берётся из данных и меняется от прогона к прогону."""
    sto, poslednyaya = skolko % 100, skolko % 10
    if 11 <= sto <= 14 or poslednyaya == 0 or poslednyaya >= 5:
        return "%d вин" % skolko
    return "%d вина" % skolko


def mesta_za_dengi(d, k):
    """Места этого вина в категории «за свои деньги» годового выбора."""
    return [z for z in d["medali"][k] if z["istochnik"] == "vino.rs"
            and VINO_RS_ZA_DENGI in z["kategoriya"] and z["mesto"].isdigit()]


def bonus_za_dengi(d, k):
    mesta = [int(z["mesto"]) for z in mesta_za_dengi(d, k)]
    if not mesta:
        return 0.0
    return BONUS_ZA_DENGI["tri" if min(mesta) <= 3 else "desyat"]


def za_dengi_pometka(d, k):
    """Как показать отметку в таблице: лучшее место и его год."""
    mesta = mesta_za_dengi(d, k)
    if not mesta:
        return "—"
    luchshee = min(mesta, key=lambda z: int(z["mesto"]))
    return "%s-е, %d" % (luchshee["mesto"], luchshee["god"])


def est_vivino(d, k):
    z = d["vivino"].get(k)
    return bool(z and (z.get("vyborka") or 0) >= POROG_VYBORKI)


def spisok(d, vina, klyuch, godno, cap=2, skolko=SKAMEJKA):
    """Ранжированный список с потолком на хозяйство.

    Потолок нужен, иначе пятёрка района становится витриной одного дома:
    у Александровића хватит вин на всю Шумадију.
    """
    schet, itog = collections.Counter(), []
    for v in sorted((x for x in vina if godno(x["klyuch"])),
                    key=lambda x: klyuch(x["klyuch"]), reverse=True):
        if schet[v["hozyaistvo"]] >= cap:
            continue
        schet[v["hozyaistvo"]] += 1
        itog.append(v)
        if len(itog) == skolko:
            break
    return itog


def ocenka_eksperta(d, k):
    """Мнение экспертов одним числом — для «согласия трёх».

    Пока выбор `vino.rs` лежит в олимпиадном зачёте, это балл критика.
    С ключом `--ekspert-s-vino-rs` вино без балла, но с местом в выборе,
    тоже встаёт в ряд: не пересчётом шкал — так делать нельзя, — а своим
    рангом внутри дорожки выбора. Число служебное, в таблицы не идёт
    и нужно только чтобы упорядочить.
    """
    if d["kritiki"][k]:
        return max(d["kritiki"][k])
    return 80 + 20 * d["rang_vino_rs"].get(k, 0)


def procentili(znacheniya):
    poryadok = sorted(znacheniya.values())
    n = len(poryadok) or 1
    return {k: sum(1 for x in poryadok if x <= v) / n for k, v in znacheniya.items()}


def svodnaya(d, vina, skolko=SKAMEJKA):
    """Согласие трёх дорожек: оценка вина — худший из трёх процентилей."""
    est = [v for v in vina
           if d["ochki"](v["klyuch"]) > 0 and est_ekspert(d, v["klyuch"])
           and est_vivino(d, v["klyuch"])]
    if len(est) < 3:
        return []
    m = procentili({v["klyuch"]: d["ochki"](v["klyuch"]) for v in est})
    k = procentili({v["klyuch"]: ocenka_eksperta(d, v["klyuch"]) for v in est})
    p = procentili({v["klyuch"]: d["vivino"][v["klyuch"]]["ball"] for v in est})
    ocenka = {v["klyuch"]: min(m[v["klyuch"]], k[v["klyuch"]], p[v["klyuch"]])
              for v in est}
    return spisok(d, est, ocenka.get, lambda kl: kl in ocenka, skolko=skolko)


# Куда отнести годовой выбор `vino.rs`. Решено автором: к экспертам —
# жюри из сотни профессионалов стоит рядом с баллом критика, а не рядом
# с медалью. Измерено, что от переноса меняется: наполняемость пятёрок
# не трогается вовсе, а дорожки перестают повторять друг друга —
# пересечение пятёрки зачёта с пятёркой экспертов падает с 40% до 20%
# по медиане глав. Разбор в `vesa-otlichij.md`. Ключ
# `--ekspert-v-zachjot` возвращает старое устройство.
#
# Сложить место и балл прямо нельзя: шкалы разные, и это первое правило
# `slovar-polej.md`. Складываются процентили — так же, как в «согласии
# трёх», где три несравнимые дорожки уже сведены этим способом. У вина
# берётся среднее из тех процентилей, которые для него есть: у 220 вин
# есть место vino.rs и нет балла критика, у 954 наоборот, и требовать
# оба голоса значило бы выкинуть и тех, и других.
EKSPERT_S_VINO_RS = True


def ochki_kachestva(d, k):
    """Очки годового выбора — только по категориям о качестве."""
    return ochki_vino_rs([z for z in d["medali"][k] if z["istochnik"] == "vino.rs"])


def est_ekspert(d, k):
    if d["kritiki"][k]:
        return True
    return EKSPERT_S_VINO_RS and ochki_kachestva(d, k) > 0


def mnenie_ekspertov(d, vina, skolko=SKAMEJKA):
    """Дорожка «мнение экспертов»: балл критика, а с ключом — и место
    в годовом выборе."""
    if not EKSPERT_S_VINO_RS:
        return spisok(d, vina, lambda k: max(d["kritiki"][k]),
                      lambda k: bool(d["kritiki"][k]), skolko=skolko)
    est = [v for v in vina if est_ekspert(d, v["klyuch"])]
    s_ballom = {v["klyuch"]: max(d["kritiki"][v["klyuch"]])
                for v in est if d["kritiki"][v["klyuch"]]}
    s_mestom = {v["klyuch"]: ochki_kachestva(d, v["klyuch"])
                for v in est if ochki_kachestva(d, v["klyuch"]) > 0}
    pk, pm = procentili(s_ballom), procentili(s_mestom)
    ocenka = {}
    for v in est:
        k = v["klyuch"]
        golosa = [x for x in (pk.get(k), pm.get(k)) if x is not None]
        if golosa:
            ocenka[k] = sum(golosa) / len(golosa)
    return spisok(d, est, ocenka.get, lambda k: k in ocenka, skolko=skolko)


def kachestvo(d, k):
    """Качество вина для сводных таблиц страны — балл критика.

    Первая редакция подставляла сюда оценку Vivino, пересчитанную
    в стобалльную шкалу, когда балла критика не было. Это была ошибка:
    пересчёт ставил вино, которого не судил никто, выше вина с золотом
    Decanter. Шкалы Vivino и критиков не переводятся одна в другую — это
    записано в `slovar-polej.md` первым же правилом, — и складывать их
    в одно число нельзя. Вино без балла критика в этот ряд не идёт; для
    покупательской оценки есть своя таблица.
    """
    return max(d["kritiki"][k]) if d["kritiki"][k] else 0


def modelirovat_cenu(d, ocenka, godno):
    """Сколько баллов обещает цена — и насколько вино это обещание бьёт.

    «За свои деньги» — не «дёшево и хорошо», а «лучше, чем за него
    просят». Поэтому строится ожидание: балл как функция логарифма цены,
    и вино оценивается остатком, превышением над ожиданием.

    Ожидание получается плоским — удвоение цены прибавляет около балла,
    связь слабая. Это не изъян счёта, а свойство сербской полки, и оно
    само по себе стоит того, чтобы сказать его вслух: цена здесь плохо
    предсказывает качество.
    """
    pary = [(d["cena"][k], ocenka(k)) for k in d["cena"] if godno(k)]
    if len(pary) < 30:
        return None
    x = [math.log(c) for c, _ in pary]
    y = [b for _, b in pary]
    sx, sy = statistics.mean(x), statistics.mean(y)
    naklon = (sum((a - sx) * (b - sy) for a, b in zip(x, y))
              / sum((a - sx) ** 2 for a in x))
    svobodnyj = sy - naklon * sx
    razbros = statistics.pstdev([b - (svobodnyj + naklon * a) for a, b in zip(x, y)])
    svyaz = (sum((a - sx) * (b - sy) for a, b in zip(x, y))
             / math.sqrt(sum((a - sx) ** 2 for a in x)
                         * sum((b - sy) ** 2 for b in y)))
    return dict(ozhidanie=lambda c: svobodnyj + naklon * math.log(c),
                naklon=naklon, razbros=razbros, svyaz=svyaz, vin=len(pary))


def stroka_vina(d, v, cena=False):
    k = v["klyuch"]
    b = max(d["kritiki"][k]) if d["kritiki"][k] else None
    z = d["vivino"].get(k)
    kuski = ["%s · %s" % (v["hozyaistvo"], v["vino"]),
             str(b) if b else "—",
             ("%.1f" % z["ball"]) if z and z.get("ball") else "—",
             "%.0f" % d["ochki"](k) if d["medali"][k] else "—"]
    if cena:
        kuski.append("%d" % d["cena"][k] if k in d["cena"] else "—")
    return "| " + " | ".join(kuski) + " |"


def shapka(cena=False):
    stolbcy = ["Вино", "Критик", "Vivino", "Медали"] + (["Динаров"] if cena else [])
    return ("| " + " | ".join(stolbcy) + " |\n|"
            + "|".join("---" for _ in stolbcy) + "|")


def po_glavam(d, pech):
    for imya, rejony in GLAVY:
        vina = [v for r in rejony for v in d["po_rejonu"].get(r, [])]
        if imya in REGION_GLAVY:
            vina += d["po_regionu"].get(REGION_GLAVY[imya], [])
        pech("\n## %s\n" % imya)
        dorozhki = [
            ("Олимпиадный зачёт", spisok(d, vina, d["ochki"], lambda k: bool(d["medali"][k]))),
            ("Мнение экспертов", mnenie_ekspertov(d, vina)),
            ("Vox populi", spisok(d, vina, lambda k: d["vivino"][k]["ball"],
                                  lambda k: est_vivino(d, k))),
            ("Согласие трёх", svodnaya(d, vina)),
        ]
        for zagolovok, spis in dorozhki:
            if len(spis) < 3:
                pech("**%s** — не набирается: подходящих вин %d.\n"
                     % (zagolovok, len(spis)))
                continue
            pech("**%s**%s\n" % (zagolovok,
                 "" if len(spis) >= 5 else " — только %d вина вместо пяти" % len(spis)))
            pech(shapka())
            for nomer, v in enumerate(spis, 1):
                pech(stroka_vina(d, v) + ("" if nomer != 5 or len(spis) == 5
                                          else ""))
            pech("")
        for kod, zagolovok in CVETA:
            svoi = [v for v in vina if d["cvet"].get(v["klyuch"]) == kod]
            trojka = spisok(d, svoi, lambda k: kachestvo(d, k),
                            lambda k: kachestvo(d, k) > 0, skolko=5)
            if len(trojka) < 3:
                continue      # розе есть не везде, и выдумывать его незачем
            pech("**%s: тройка и запас**\n" % zagolovok)
            pech(shapka())
            for v in trojka:
                pech(stroka_vina(d, v))
            pech("")


def po_strane(d, pech):
    vse = [v for v in d["vina"] if kachestvo(d, v["klyuch"]) > 0]
    pech("\n# По стране целиком\n")
    pech("Здесь районы соревнуются друг с другом, а не каждый сам с собой.\n")

    pech("\n## Супервина: десятка лучших без оглядки на цену\n")
    pech(shapka(cena=True))
    for v in spisok(d, vse, lambda k: kachestvo(d, k), lambda k: True, skolko=10):
        pech(stroka_vina(d, v, cena=True))

    for kod, zagolovok in CVETA:
        svoi = [v for v in vse if d["cvet"].get(v["klyuch"]) == kod]
        pyat = spisok(d, svoi, lambda k: kachestvo(d, k), lambda k: True, skolko=5)
        if len(pyat) < 3:
            continue
        pech("\n## %s: пятёрка страны\n" % zagolovok)
        pech(shapka(cena=True))
        for v in pyat:
            pech(stroka_vina(d, v, cena=True))

    narodnye = spisok(d, d["vina"], lambda k: d["vivino"][k]["ball"],
                      lambda k: est_vivino(d, k), skolko=10)
    pech("\n## Vox populi: десятка по оценке покупателей\n")
    pech("Шкала Vivino своя и в стобалльную не переводится, поэтому "
         "покупательский ряд стоит отдельно, а не подмешан к баллам критиков.\n")
    pech(shapka(cena=True))
    for v in narodnye:
        pech(stroka_vina(d, v, cena=True))

    s_cenoj = [v for v in vse if v["klyuch"] in d["cena"]]
    if not s_cenoj:
        return
    ceny = sorted(d["cena"][v["klyuch"]] for v in s_cenoj)
    potolok = 2000

    # Две разные таблицы на два разных вопроса. Первая редакция знала
    # только вторую и звала её «за свои деньги» — а это был всего лишь
    # список лучших из дешёвых, что не одно и то же.
    est_ball = lambda k: bool(d["kritiki"][k])
    m = modelirovat_cenu(d, lambda k: max(d["kritiki"][k]), est_ball)
    if m:
        ostatok = {v["klyuch"]: max(d["kritiki"][v["klyuch"]])
                   - m["ozhidanie"](d["cena"][v["klyuch"]])
                   for v in s_cenoj if est_ball(v["klyuch"])}
        pech("\n## Лучше, чем за них просят\n")
        pech("Здесь не «дёшево и хорошо», а «дороже своей цены». Цена "
             "переводится в ожидаемый балл, и вино оценивается превышением "
             "над ожиданием. Ожидание плоское: удвоение цены обещает всего "
             "%.1f балла, связь слабая (коэффициент %.2f по %d винам, "
             "разброс остатка %.1f балла). Это и есть главный вывод: "
             "**в Сербии цена почти не предсказывает качество**, и покупать "
             "по ценнику здесь бессмысленнее, чем где-либо.\n"
             % (m["naklon"] * math.log(2), m["svyaz"], m["vin"], m["razbros"]))
        pech("Второй голос здесь — сам `vino.rs`: у него есть своя "
             "категория «за свои деньги», и её отметка вино в ряду "
             "поднимает. Столбец «vino.rs» показывает лучшее место "
             "и год; в порядке ряда отметка стоит %+.1f балла остатка "
             "за первую тройку и %+.1f за прочие места десятки — ровно "
             "столько, на сколько такие вина в среднем и превышают "
             "ожидание по цене. Столбец «сверх ожидания» при этом "
             "остаётся чистым измерением, без надбавки.\n"
             % (BONUS_ZA_DENGI["tri"], BONUS_ZA_DENGI["desyat"]))
        pech("| Вино | Сверх ожидания | vino.rs | Критик | Vivino | Медали | Динаров |")
        pech("|---|---|---|---|---|---|---|")
        s_ostatkom = lambda v: "| %s | %+.1f | %s | %s" % (
            "%s · %s" % (v["hozyaistvo"], v["vino"]), ostatok[v["klyuch"]],
            za_dengi_pometka(d, v["klyuch"]),
            stroka_vina(d, v, cena=True).split(" | ", 1)[1])
        poryadok = {k: v + bonus_za_dengi(d, k) for k, v in ostatok.items()}
        for v in spisok(d, [v for v in s_cenoj if v["klyuch"] in ostatok],
                        poryadok.get, lambda k: k in ostatok, skolko=10):
            pech(s_ostatkom(v))
        pech("\nХвост того же ряда — вино, которое просит больше, чем даёт:\n")
        pech("| Вино | Сверх ожидания | vino.rs | Критик | Vivino | Медали | Динаров |")
        pech("|---|---|---|---|---|---|---|")
        for k in sorted(poryadok, key=poryadok.get)[:5]:
            pech(s_ostatkom(next(x for x in s_cenoj if x["klyuch"] == k)))

    dostupnye = [v for v in s_cenoj if d["cena"][v["klyuch"]] <= potolok]
    pech("\n## Если в кармане %d динаров\n" % potolok)
    pech("Другой вопрос и другой ответ: не «что выгодно», а «что взять "
         "сегодня». Цена известна у %d отобранных вин, медиана %s.\n"
         % (len(s_cenoj), dinarov(round(statistics.median(ceny)))))
    pech(shapka(cena=True))
    for v in spisok(d, dostupnye, lambda k: kachestvo(d, k), lambda k: True, skolko=10):
        pech(stroka_vina(d, v, cena=True))

    if d["supermarket"]:
        polka = [v for v in d["vina"] if v["klyuch"] in d["supermarket"]]
        s_ocenkoj = [v for v in polka if kachestvo(d, v["klyuch"]) > 0
                     or est_vivino(d, v["klyuch"])]
        svodka = d.get("polka_supermarketa") or {}
        # Один источник бывает сразу несколькими сетями: обязательный
        # ценовник группы покрывает и Roda, и Mercator, и IDEA.
        MAGAZIN = {"maxi": ["Maxi"], "maxi-cenovnik": ["Maxi"],
                   "idea": ["Idea"], "idea-cenovnik": ["Roda", "Mercator"]}
        pech("\n## Что взять в супермаркете\n")
        # Одна сеть попадает в список дважды — витриной интернет-магазина
        # и обязательным ценовником, — а зовётся одинаково. Имена
        # склеиваются, иначе выходит «Maxi и Maxi».
        seti = list(dict.fromkeys(
            imya for m in svodka.get("magaziny", [])
            for imya in MAGAZIN.get(m, [m])))
        pech("Полка супермаркета — не полка винотеки. Медиана бутылки 0,75 "
             "на полках %s — %s против %s у винотек. Из %d обычных бутылок "
             "с нашими таблицами сошлись %d, и %d из этих %d в винотеке нет "
             "вовсе. Вот те, о которых есть что сказать.\n" % (
                 perechislit(seti),
                 dinarov(svodka.get("mediana_0_75")),
                 svodka.get("mediana_vinoteki"),
                 svodka.get("iz_nih_0_75", 0), len(d["supermarket"]),
                 svodka.get("tolko_v_supermarkete", 0), len(d["supermarket"])))
        # Полка супермаркета дешевле в целом — и дороже на каждой
        # отдельной бутылке. Это не противоречие, а разный вопрос:
        # ассортимент против одного и того же вина.
        if svodka.get("vin_v_oboih"):
            pech("Дешевле там, однако, не то же вино, а другое. Из %d вин, "
                 "которые продаются и в супермаркете, и в винотеке, дешевле "
                 "в супермаркете %d: одна и та же бутылка на полке стоит "
                 "в среднем на %.0f%% дороже. В супермаркет идут не за "
                 "скидкой на знакомое вино, а за тем, чего в винотеке нет.\n"
                 % (svodka["vin_v_oboih"], svodka["deshevle_v_supermarkete"],
                    (svodka["nacenka_supermarketa"] - 1) * 100))
        pech("| Вино | Критик | Vivino | Медали | Динаров |")
        pech("|---|---|---|---|---|")
        for v in sorted(s_ocenkoj,
                        key=lambda v: (-(kachestvo(d, v["klyuch"]) or 0),
                                       d["supermarket"][v["klyuch"]]))[:12]:
            k = v["klyuch"]
            z = d["vivino"].get(k)
            pech("| %s · %s | %s | %s | %s | %d |" % (
                v["hozyaistvo"], v["vino"],
                max(d["kritiki"][k]) if d["kritiki"][k] else "—",
                ("%.1f" % z["ball"]) if z and z.get("ball") else "—",
                "%.0f" % d["ochki"](k) if d["medali"][k] else "—",
                d["supermarket"][k]))
        # Третий канал — магазин самого хозяйства. Он идёт в другую
        # сторону, чем два первых, и стоит после ряда: ряд о полке,
        # а это уже о том, где ту же бутылку взять дешевле.
        uh = d.get("u_hozyaistva") or {}
        if uh.get("vin_i_tam_i_tam"):
            pech("")
            pech("Есть и третья полка — у самого хозяйства, и на ней то же "
                 "вино обычно дешевле: в среднем на %.0f%%. Цена известна "
                 "и в винотеке, и в магазине винодельни у %s; у винодельни "
                 "дешевле %d из них. Собственные магазины нашлись у %s "
                 "хозяйств, и там же стоят флагманы, которых в винотеках "
                 "нет вовсе.\n"
                 % ((1 - uh["cena_hozyaistva_k_lavke"]) * 100,
                    vin_shtuk(uh["vin_i_tam_i_tam"]),
                    uh["deshevle_u_hozyaistva"],
                    uh.get("hozyaistv") or "нескольких"))

        # Четвёртая полка — витрина доставки. Она дороже всех, и потому
        # идёт в счёт последней; но лавок в ней больше, чем во всех
        # остальных источниках вместе, и цену трёхсот вин знаем только
        # оттуда.
        dost = d.get("dostavka") or {}
        if dost.get("nacenka_dostavki"):
            pech("Четвёртая — витрина доставки: %s винотек в Wolt. Она "
                 "дороже полки, и насколько, теперь измерено на %s, "
                 "а не на четырёх бутылках: середина отношения %.2f, "
                 "то есть примерно %.0f%% сверху. Строка доставки идёт "
                 "в счёт только там, где полочной цены нет вовсе, — "
                 "а таких %s.\n"
                 % (dost.get("lavok") or "нескольких",
                    vin_shtuk(dost["vin_i_tam_i_tam"]),
                    dost["nacenka_dostavki"],
                    (dost["nacenka_dostavki"] - 1) * 100,
                    vin_shtuk(dost["vin_tolko_iz_dostavki"])))

    # Доступное вино редко ездит на конкурс, и ряд выше молчит как раз
    # о самых ходовых бутылках: у «Sfera» Бикицког 308 отзывов и ни
    # одного балла. Поэтому у покупателей здесь свой ряд, а не примечание.
    narodnye_deshevye = [v for v in d["vina"]
                         if v["klyuch"] in d["cena"]
                         and d["cena"][v["klyuch"]] <= potolok
                         and est_vivino(d, v["klyuch"])]
    pech("\n## То же, по мнению покупателей\n")
    pech("Тот же потолок, но ряд строит выборка Vivino. Ряд нужен отдельно: "
         "дешёвое вино на конкурс возят редко, и таблица выше молчит "
         "как раз о самых ходовых бутылках.\n")
    pech(shapka(cena=True))
    for v in spisok(d, narodnye_deshevye, lambda k: d["vivino"][k]["ball"],
                    lambda k: True, skolko=10):
        pech(stroka_vina(d, v, cena=True))


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("--otchet", action="store_true",
                        help="собрать rejtingi.md, а не печатать на экран")
    razbor.add_argument("--ekspert-v-zachjot", action="store_true",
                        help="вернуть годовой выбор vino.rs в олимпиадный "
                             "зачёт, как было до решения автора")
    razbor.add_argument("--v-fajl", default="rejtingi.md",
                        help="куда писать отчёт (для сравнения вариантов)")
    kljuchi = razbor.parse_args()
    global EKSPERT_S_VINO_RS
    EKSPERT_S_VINO_RS = not kljuchi.ekspert_v_zachjot
    d = razobrat()
    stroki = []
    pech = stroki.append if kljuchi.otchet else print
    if kljuchi.otchet:
        vstuplenie = ZDES / "rejtingi-vstuplenie.md"
        if vstuplenie.exists():
            pech(vstuplenie.read_text(encoding="utf-8").rstrip())
            pech("\n<!-- Собрано скриптом svesti-rejtingi.py. Руками не править. -->")
    po_strane(d, pech)
    pech("\n# По главам\n")
    po_glavam(d, pech)
    if kljuchi.otchet:
        (ZDES / kljuchi.v_fajl).write_text("\n".join(stroki) + "\n",
                                           encoding="utf-8")
        print("собран %s%s" % (kljuchi.v_fajl,
                               "" if EKSPERT_S_VINO_RS
                               else " (выбор vino.rs — в олимпиадном зачёте)"))


if __name__ == "__main__":
    main()
