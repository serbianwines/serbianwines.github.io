#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Что прошло бы предложенное правило отбора, а что нет.

Правило к данным **не применено**: это отчёт для чтения, а не фильтр.
Решение о том, входит ли оно в работу, за автором.

Четыре двери, и вину довольно любой одной:

    три и более независимых источника высказались о нём;
    балл критика 90 и выше;
    строгая награда — золото Decanter либо двойное золото, платина
        или трофей у остальных конкурсов;
    оценка Vivino 4,0 и выше — кроме «громких немых» хозяйств.

«Громкое немое» — хозяйство из верхних десяти процентов по охвату
(сколько людей сфотографировали этикетку), о котором за все годы не
высказалось ни одно жюри и ни один критик. Таких пять, и на них
приходится четыреста тысяч сканов — самая ходовая полка Сербии,
которую конкурсы не судили ни разу.

    python3 _rabota/rejtingi/svesti-otbor.py            # на экран
    python3 _rabota/rejtingi/svesti-otbor.py --otchet   # собрать otbor.md
"""
import collections
import io
import json
import os
import statistics
import sys

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)

POROG_VIVINO = 4.0
POROG_KRITIKA = 90
# Награда, которую конкурс даёт скупо. У Decanter золото получают 4%
# награждённых, и все его золотые лауреаты стоят у покупателей выше 3,7.
# У остальных конкурсов золото раздаётся щедрее, поэтому от них берутся
# только ступени выше золота.
VYSHE_ZOLOTA = {"platina", "dvojno-zlato", "best-in-show", "trofej",
                "veliko-zlato"}


def chitat():
    def jl(imya):
        return [json.loads(s) for s in open(put(imya), encoding="utf-8")
                if s.strip()]
    return jl("hozyaistva.jsonl"), jl("vina.jsonl"), jl("ocenki.jsonl"), jl("nagrady.jsonl")


# Сколько сканов этикетки делают хозяйство маркой национального масштаба.
# Это единственное число в правиле, которое выбрано, а не измерено: спад
# охвата плавный, разрыва в нём нет. Пятнадцать тысяч — в шестьдесят семь
# раз выше медианного хозяйства (223), и на этой черте в «немые» попадают
# ровно пять домов, все с массовой полки. Ниже неё стоят хозяйства другого
# рода — например, «Francuska Vinarija» французской пары Бонжиро: о ней
# жюри тоже молчит, но это бутик, а не марка из супермаркета.
POROG_OHVATA = 15000


def gromkie_nemye(vina, ocenki, nagrady):
    """Хозяйства с огромным охватом, о которых жюри молчит."""
    ohvat = collections.Counter()
    for z in vina:
        ohvat[z["hozyaistvo"]] += z.get("etiketok") or 0
    skazano = ({z["hozyaistvo"] for z in nagrady}
               | {z["hozyaistvo"] for z in ocenki if z["shkala"] == 100})
    return {h for h, v in ohvat.items()
            if v >= POROG_OHVATA and h not in skazano}


def razobrat():
    hozyaistva, vina, ocenki, nagrady = chitat()
    vivino = {z["klyuch_vina"]: z["ball"] for z in ocenki
              if z["shkala"] == 5 and z["ball"] is not None}
    kritiki = collections.defaultdict(list)
    for z in ocenki:
        if z["shkala"] == 100:
            kritiki[z["klyuch_vina"]].append(z["ball"])
    nagrady_vina = collections.defaultdict(list)
    for z in nagrady:
        nagrady_vina[z["klyuch_vina"]].append(z)
    # Голос источника: и конкурс, и критик — независимые высказывания.
    golosa = collections.defaultdict(set)
    for z in nagrady:
        if z["klyuch_vina"]:
            golosa[z["klyuch_vina"]].add(z["istochnik"])
    for z in ocenki:
        if z["shkala"] == 100 and z["klyuch_vina"]:
            golosa[z["klyuch_vina"]].add(z["istochnik"])

    nemye = gromkie_nemye(vina, ocenki, nagrady)

    def strogaya_nagrada(k):
        for x in nagrady_vina[k]:
            if x["istochnik"] == "decanter" and x["mesto"] == "zlato":
                return True
            if x["mesto"] in VYSHE_ZOLOTA:
                return True
        return False

    proshli, dver = {}, collections.Counter()
    for z in vina:
        k = z["klyuch"]
        if len(golosa[k]) >= 3:
            prichina = "три источника и больше"
        elif max(kritiki[k], default=0) >= POROG_KRITIKA:
            prichina = "балл критика 90+"
        elif strogaya_nagrada(k):
            prichina = "строгая награда"
        elif vivino.get(k, 0) >= POROG_VIVINO and z["hozyaistvo"] not in nemye:
            prichina = "Vivino 4,0+"
        else:
            continue
        proshli[k] = prichina
        dver[prichina] += 1
    return dict(hozyaistva={z["hozyaistvo"]: z for z in hozyaistva},
                vina=vina, vivino=vivino, kritiki=kritiki,
                nagrady_vina=nagrady_vina, golosa=golosa, nemye=nemye,
                proshli=proshli, dver=dver)


def ohvat_hozyaistva(vina):
    o = collections.Counter()
    for z in vina:
        o[z["hozyaistvo"]] += z.get("etiketok") or 0
    return o


def pokazat(d):
    vina, proshli, vivino = d["vina"], d["proshli"], d["vivino"]
    hozyaistva, golosa = d["hozyaistva"], d["golosa"]
    po_klyuchu = {z["klyuch"]: z for z in vina}
    hoz_proshli = {po_klyuchu[k]["hozyaistvo"] for k in proshli}

    print("## Сколько проходит\n")
    print("| | Вин |")
    print("|---|---|")
    for prichina, skolko in d["dver"].most_common():
        print("| %s | %d |" % (prichina, skolko))
    print("| **всего** | **%d** у %d хозяйств |" % (len(proshli), len(hoz_proshli)))
    b = [vivino[k] for k in proshli if k in vivino]
    print("\nУ прошедших медиана Vivino %.2f; ниже 3,7 остаётся %d из %d.\n"
          % (statistics.median(b), sum(1 for x in b if x < 3.7), len(b)))

    print("## По рејонима — хватит ли на пятёрку\n")
    print("| Рејон | Прошло вин | Хозяйств |")
    print("|---|---|---|")
    po_rejonu = collections.defaultdict(set)
    for k in proshli:
        h = hozyaistva.get(po_klyuchu[k]["hozyaistvo"])
        po_rejonu[(h or {}).get("rejon") or "рејон не установлен"].add(k)
    for rejon, g in sorted(po_rejonu.items(), key=lambda x: -len(x[1])):
        hoz = {po_klyuchu[k]["hozyaistvo"] for k in g}
        print("| %s | %d | %d |" % (rejon, len(g), len(hoz)))

    print("\n## Верхушка: о вине высказались три источника и больше\n")
    print("| Хозяйство | Вино | Vivino | Балл критика | Источники |")
    print("|---|---|---|---|---|")
    verh = [k for k, p in proshli.items() if p == "три источника и больше"]
    for k in sorted(verh, key=lambda k: (-len(golosa[k]),
                                         -max(d["kritiki"][k], default=0))):
        z = po_klyuchu[k]
        print("| %s | %s | %s | %s | %s |"
              % (z["hozyaistvo"], z["vino"], vivino.get(k, "—"),
                 max(d["kritiki"][k], default="—"), ", ".join(sorted(golosa[k]))))

    print("\n## Громкие немые: полка, которую жюри не судило ни разу\n")
    print("Хозяйства, чьи этикетки сфотографированы больше %d раз и о ком "
          "при этом за все годы не высказалось ни одно жюри и ни один "
          "критик.\n" % POROG_OHVATA)
    ohvat = ohvat_hozyaistva(vina)
    print("| Хозяйство | Этикеток | Вин | Медиана Vivino |")
    print("|---|---|---|---|")
    for h in sorted(d["nemye"], key=lambda h: -ohvat[h]):
        b = [vivino[z["klyuch"]] for z in vina
             if z["hozyaistvo"] == h and z["klyuch"] in vivino]
        print("| %s | %d | %d | %s |"
              % (h, ohvat[h], sum(1 for z in vina if z["hozyaistvo"] == h),
                 ("%.2f" % statistics.median(b)) if b else "—"))

    print("\n## Отсеяно вопреки высокой оценке покупателей\n")
    otsev = [z for z in vina if z["klyuch"] not in proshli
             and vivino.get(z["klyuch"], 0) >= POROG_VIVINO]
    print("Вин с оценкой %.1f и выше, которые правило не пропускает, — %d.\n"
          % (POROG_VIVINO, len(otsev)))
    if otsev:
        print("| Хозяйство | Вино | Vivino | Этикеток |")
        print("|---|---|---|---|")
        for z in sorted(otsev, key=lambda z: -vivino[z["klyuch"]]):
            print("| %s | %s | %.1f | %s |" % (z["hozyaistvo"], z["vino"],
                  vivino[z["klyuch"]], z.get("etiketok") or "—"))

    print("\n## Отсеяно вопреки медали\n")
    s_medalyu = [z for z in vina if z["klyuch"] not in proshli
                 and d["nagrady_vina"][z["klyuch"]]]
    print("Вин с медалью, которые правило не пропускает, — %d. Это медали "
          "ниже золота либо золото щедрых конкурсов, и покупатели их не "
          "поддержали.\n" % len(s_medalyu))
    print("| Хозяйство | Вино | Vivino | Награды |")
    print("|---|---|---|---|")
    for z in sorted(s_medalyu, key=lambda z: -(vivino.get(z["klyuch"]) or 0))[:40]:
        med = collections.Counter(x["kategoriya"] for x in d["nagrady_vina"][z["klyuch"]])
        print("| %s | %s | %s | %s |"
              % (z["hozyaistvo"], z["vino"], vivino.get(z["klyuch"], "—"),
                 ", ".join("%s×%d" % (k, v) if v > 1 else k
                           for k, v in med.most_common()[:3])))
    if len(s_medalyu) > 40:
        print("\nПоказаны сорок из %d — остальные так же." % len(s_medalyu))

    print("\n## Хозяйства, которые правило вычёркивает целиком\n")
    est_chto_skazat = {z["hozyaistvo"] for z in vina
                       if z["klyuch"] in vivino or d["nagrady_vina"][z["klyuch"]]
                       or d["kritiki"][z["klyuch"]]}
    vycherknuty = sorted(est_chto_skazat - hoz_proshli)
    print("Хозяйств, о которых что-то известно, но ни одно вино не проходит, "
          "— %d.\n" % len(vycherknuty))
    print("| Хозяйство | Рејон | Лучшая Vivino | Медалей |")
    print("|---|---|---|---|")
    for h in vycherknuty:
        b = [vivino[z["klyuch"]] for z in vina
             if z["hozyaistvo"] == h and z["klyuch"] in vivino]
        med = sum(len(d["nagrady_vina"][z["klyuch"]]) for z in vina
                  if z["hozyaistvo"] == h)
        print("| %s | %s | %s | %d |"
              % (h, (hozyaistva.get(h) or {}).get("rejon") or "—",
                 ("%.1f" % max(b)) if b else "—", med))


def main():
    d = razobrat()
    if "--otchet" not in sys.argv:
        pokazat(d)
        return
    vstuplenie = ""
    if os.path.exists(put("otbor-vstuplenie.md")):
        vstuplenie = io.open(put("otbor-vstuplenie.md"), encoding="utf-8").read()
        if not vstuplenie.endswith("\n\n"):
            vstuplenie += "\n\n"
    bufer = io.StringIO()
    nastojashchij, sys.stdout = sys.stdout, bufer
    try:
        pokazat(d)
    finally:
        sys.stdout = nastojashchij
    io.open(put("otbor.md"), "w", encoding="utf-8").write(vstuplenie + bufer.getvalue())
    print("собран otbor.md")


if __name__ == "__main__":
    main()
