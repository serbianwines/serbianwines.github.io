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
CVETA = [("красное", "Красные"), ("белое", "Белые"), ("розе", "Розе")]


def chitat():
    jl = lambda imya: [json.loads(s) for s in
                       (ZDES / imya).read_text(encoding="utf-8").splitlines() if s.strip()]
    cena = {}
    put = ZDES / "ceny-vin.json"
    if put.exists():
        cena = json.loads(put.read_text(encoding="utf-8"))["ceny"]
    return jl("hozyaistva.jsonl"), jl("vina.jsonl"), jl("ocenki.jsonl"), \
        jl("nagrady.jsonl"), cena


def razobrat():
    hozyaistva, vina, ocenki, nagrady, cena = chitat()
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

    ochki = lambda k: sum(STROGOST.get(z["istochnik"], 1) * STUPEN.get(z["mesto"], 1)
                          for z in medali[k])
    # Рејон вина — свой, если конкурс объявил происхождение винограда;
    # иначе рејон дома. Книга о терруаре, и место у вина от лозы.
    rejon = lambda v: v.get("rejon") or (dom.get(v["hozyaistvo"]) or {}).get("rejon")
    po_rejonu = collections.defaultdict(list)
    for v in vina:
        r = rejon(v)
        if r:
            po_rejonu[r].append(v)
    return dict(vina=vina, dom=dom, vivino=vivino, kritiki=kritiki, medali=medali,
                ochki=ochki, cena=cena, cvet=cvet, po_rejonu=po_rejonu)


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


def procentili(znacheniya):
    poryadok = sorted(znacheniya.values())
    n = len(poryadok) or 1
    return {k: sum(1 for x in poryadok if x <= v) / n for k, v in znacheniya.items()}


def svodnaya(d, vina, skolko=SKAMEJKA):
    """Согласие трёх дорожек: оценка вина — худший из трёх процентилей."""
    est = [v for v in vina if d["medali"][v["klyuch"]] and d["kritiki"][v["klyuch"]]
           and est_vivino(d, v["klyuch"])]
    if len(est) < 3:
        return []
    m = procentili({v["klyuch"]: d["ochki"](v["klyuch"]) for v in est})
    k = procentili({v["klyuch"]: max(d["kritiki"][v["klyuch"]]) for v in est})
    p = procentili({v["klyuch"]: d["vivino"][v["klyuch"]]["ball"] for v in est})
    ocenka = {v["klyuch"]: min(m[v["klyuch"]], k[v["klyuch"]], p[v["klyuch"]])
              for v in est}
    return spisok(d, est, ocenka.get, lambda kl: kl in ocenka, skolko=skolko)


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
        pech("\n## %s\n" % imya)
        dorozhki = [
            ("Олимпиадный зачёт", spisok(d, vina, d["ochki"], lambda k: bool(d["medali"][k]))),
            ("Мнение экспертов", spisok(d, vina, lambda k: max(d["kritiki"][k]),
                                        lambda k: bool(d["kritiki"][k]))),
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
        pech("| Вино | Сверх ожидания | Критик | Vivino | Медали | Динаров |")
        pech("|---|---|---|---|---|---|")
        s_ostatkom = lambda v: "| %s | %+.1f | %s" % (
            "%s · %s" % (v["hozyaistvo"], v["vino"]), ostatok[v["klyuch"]],
            stroka_vina(d, v, cena=True).split(" | ", 1)[1])
        for v in spisok(d, [v for v in s_cenoj if v["klyuch"] in ostatok],
                        ostatok.get, lambda k: k in ostatok, skolko=10):
            pech(s_ostatkom(v))
        pech("\nХвост того же ряда — вино, которое просит больше, чем даёт:\n")
        pech("| Вино | Сверх ожидания | Критик | Vivino | Медали | Динаров |")
        pech("|---|---|---|---|---|---|")
        for k in sorted(ostatok, key=ostatok.get)[:5]:
            pech(s_ostatkom(next(x for x in s_cenoj if x["klyuch"] == k)))

    dostupnye = [v for v in s_cenoj if d["cena"][v["klyuch"]] <= potolok]
    pech("\n## Если в кармане %d динаров\n" % potolok)
    pech("Другой вопрос и другой ответ: не «что выгодно», а «что взять "
         "сегодня». Цена известна у %d отобранных вин, медиана %.0f динаров.\n"
         % (len(s_cenoj), statistics.median(ceny)))
    pech(shapka(cena=True))
    for v in spisok(d, dostupnye, lambda k: kachestvo(d, k), lambda k: True, skolko=10):
        pech(stroka_vina(d, v, cena=True))

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
    kljuchi = razbor.parse_args()
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
        (ZDES / "rejtingi.md").write_text("\n".join(stroki) + "\n", encoding="utf-8")
        print("собран rejtingi.md")


if __name__ == "__main__":
    main()
