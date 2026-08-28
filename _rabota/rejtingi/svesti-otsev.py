# -*- coding: utf-8 -*-
"""Отсев: о ком в справочнике рейтингов есть что сказать, а о ком нет.

В таблице 437 хозяйств. Это не значит, что все они заслуживают строки
в книге: у части нет ни одной оценки, у части оценка есть, но ниже
сербской нормы, а две строки — вовсе не хозяйства.

Отсев идёт по тому, что у нас есть, и только по нему. Отсутствие оценки —
это отсутствие данных, а не доказательство плохого вина: маленькое
хозяйство может делать прекрасное вино, которое просто никто не оценил.
Поэтому ступени названы по признаку, а не по приговору.

    python3 _rabota/rejtingi/svesti-otsev.py --otchet

Ключ `--otchet` собирает `otsev.md` — вступление плюс таблицы.
"""
import json, os, sys, collections

RYADOM = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(RYADOM, *ch)

MIN_OCENOK = 25          # тот же порог, что у пятёрок
NIZKAYA = 3.4            # нижняя десятая часть сербских оценок Vivino


def zagruzit():
    hoz = [json.loads(s) for s in open(put("hozyaistva.jsonl"), encoding="utf-8")
           if s.strip()]
    vina = collections.defaultdict(list)
    for s in open(put("vina.jsonl"), encoding="utf-8"):
        if s.strip():
            z = json.loads(s)
            vina[z["hozyaistvo"]].append(z)
    ocenki = collections.defaultdict(list)
    for s in open(put("ocenki.jsonl"), encoding="utf-8"):
        if s.strip():
            z = json.loads(s)
            ocenki[z["hozyaistvo"]].append(z)
    nagrady = collections.defaultdict(list)
    for s in open(put("nagrady.jsonl"), encoding="utf-8"):
        if s.strip():
            z = json.loads(s)
            nagrady[z["hozyaistvo"]].append(z)
    registr = {}
    if os.path.exists(put("registar-hozyaistv.json")):
        registr = json.load(open(put("registar-hozyaistv.json"),
                                 encoding="utf-8"))["hozyaistva"]
    return hoz, vina, ocenki, nagrady, registr


def svodka(h, vina, ocenki, nagrady, registr):
    imya = h["hozyaistvo"]
    viv = [o for o in ocenki[imya] if o["shkala"] == 5]
    kritiki = [o for o in ocenki[imya] if o["shkala"] == 100]
    vesomye = [o for o in viv if (o["vyborka"] or 0) >= MIN_OCENOK]
    medali = nagrady[imya]
    gody = [x["god"] for x in medali if x.get("god")] + \
           [o["konkurs_god"] or o["god"] for o in kritiki
            if o.get("konkurs_god") or o.get("god")]
    return {
        "hozyaistvo": imya,
        "klyuch": h["klyuch"],
        "rejon": h["rejon"],
        "v_knige": h["v_knige"],
        "vin": len(vina[imya]),
        "vin_vesomyh": len(vesomye),
        "otzyvov": sum(o["vyborka"] or 0 for o in viv),
        "luchshij_vivino": max((o["ball"] for o in vesomye), default=None),
        "kritikov": len(kritiki),
        "luchshij_kritik": max((o["ball"] for o in kritiki), default=None),
        "medalej": len(medali),
        "poslednij_god": max(gody) if gody else None,
        "v_registre": h["klyuch"] in registr,
    }


def ne_hozyaistva():
    """Строки, о которых уже известно, что это не хозяйства."""
    if not os.path.exists(put("sinonimy-hozyaistv.json")):
        return {}
    d = json.load(open(put("sinonimy-hozyaistv.json"), encoding="utf-8"))
    return dict(d.get("ne_privyazano", {}))


def stupen(s):
    """Одна ступень на хозяйство, от «сказать есть что» к «сказать нечего»."""
    if s["kritikov"] or s["medalej"]:
        return "оценка критика или медаль"
    if s["vin_vesomyh"]:
        return "только Vivino, выборка набрана"
    if s["vin"]:
        return "вина есть, оценок нет"
    return "ни вин, ни оценок"


def main():
    hoz, vina, ocenki, nagrady, registr = zagruzit()
    # В `ne_privyazano` лежат и разборы, ключ которых не имя строки;
    # отсеиваются только те, что и правда стоят в таблице.
    imena = {h["hozyaistvo"] for h in hoz}
    lozhnye = {k: v for k, v in ne_hozyaistva().items() if k in imena}
    svodki = [svodka(h, vina, ocenki, nagrady, registr) for h in hoz
              if h["hozyaistvo"] not in lozhnye]
    for s in svodki:
        s["stupen"] = stupen(s)

    stroki = []
    d = stroki.append
    d("## Что получилось")
    d("")
    d("| Ступень | Всего | Из них без рејона | Из них в книге |")
    d("|---|---|---|---|")
    poryadok = ["оценка критика или медаль", "только Vivino, выборка набрана",
                "вина есть, оценок нет", "ни вин, ни оценок"]
    for st in poryadok:
        gruppa = [s for s in svodki if s["stupen"] == st]
        if not gruppa:
            continue
        d("| %s | %d | %d | %d |" % (
            st, len(gruppa),
            sum(1 for s in gruppa if not s["rejon"]),
            sum(1 for s in gruppa if s["v_knige"])))
    d("| **всего** | **%d** | **%d** | **%d** |" % (
        len(svodki), sum(1 for s in svodki if not s["rejon"]),
        sum(1 for s in svodki if s["v_knige"])))
    d("")

    # ---- о ком сказать есть что, но неизвестно где
    est = sorted([s for s in svodki
                  if not s["rejon"] and s["stupen"] in poryadok[:2]],
                 key=lambda s: (-(s["luchshij_kritik"] or 0), -s["medalej"],
                                -(s["luchshij_vivino"] or 0), -s["otzyvov"]))
    d("## Сказать есть что, а где стоит — неизвестно")
    d("")
    d("Именно эти и стоят руки. У остальных без рејона нет ни одной оценки, "
      "и место им ничего не добавит.")
    d("")
    d("| Хозяйство | Лучший балл критика | Медалей | Лучшая Vivino | Вин с выборкой | Отзывов | Последний год |")
    d("|---|---|---|---|---|---|---|")
    for s in est:
        d("| %s | %s | %s | %s | %s | %d | %s |" % (
            s["hozyaistvo"],
            s["luchshij_kritik"] or "—", s["medalej"] or "—",
            s["luchshij_vivino"] or "—", s["vin_vesomyh"] or "—",
            s["otzyvov"], s["poslednij_god"] or "—"))
    d("")

    # ---- оценка ниже сербской нормы
    nizkie = []
    for s in svodki:
        if s["kritikov"] or s["medalej"] or not s["vin_vesomyh"]:
            continue
        if s["luchshij_vivino"] is not None and s["luchshij_vivino"] <= NIZKAYA:
            nizkie.append(s)
    nizkie.sort(key=lambda s: (s["luchshij_vivino"], -s["otzyvov"]))
    d("## Оценка набрана, но ниже сербской нормы")
    d("")
    d("Лучшее вино хозяйства держится на %s и ниже при выборке от %d отзывов — "
      "это нижняя десятая часть всех сербских оценок Vivino (средняя 3,85, "
      "медиана 3,90). Ни медалей, ни оценок критиков у этих хозяйств нет."
      % (str(NIZKAYA).replace(".", ","), MIN_OCENOK))
    d("")
    d("| Хозяйство | Лучшая Vivino | Вин с выборкой | Отзывов | Рејон |")
    d("|---|---|---|---|---|")
    for s in nizkie:
        d("| %s | %s | %d | %d | %s |" % (
            s["hozyaistvo"], s["luchshij_vivino"], s["vin_vesomyh"],
            s["otzyvov"], s["rejon"] or "—"))
    d("")

    # ---- нет ни одной оценки
    nemye = sorted([s for s in svodki if s["stupen"] in poryadok[2:]],
                   key=lambda s: (-s["vin"], s["hozyaistvo"]))
    d("## Ни одной оценки и ни одной награды")
    d("")
    d("%d хозяйств. Вина у них в сборе есть, но Vivino не показывает оценку — "
      "отзывов слишком мало, — и ни на один конкурс они не выходили. "
      "Справочнику рейтингов сказать о них нечего: не потому, что вино плохое, "
      "а потому, что его никто не оценил." % len(nemye))
    d("")
    d("| Хозяйство | Вин в сборе | В Винарском регистру | Рејон |")
    d("|---|---|---|---|")
    for s in nemye:
        d("| %s | %d | %s | %s |" % (
            s["hozyaistvo"], s["vin"], "да" if s["v_registre"] else "не нашлось",
            s["rejon"] or "—"))
    d("")

    if lozhnye:
        d("## Строки, которые не хозяйства")
        d("")
        d("Ошибки ввода у Decanter: в поле производителя стоит название сорта. "
          "В отсчёт выше они не входят.")
        d("")
        for imya, pochemu in sorted(lozhnye.items()):
            d("- **%s** — %s" % (imya, pochemu))
        d("")

    otchet = "\n".join(stroki)
    if "--otchet" in sys.argv:
        vstuplenie = ""
        if os.path.exists(put("otsev-vstuplenie.md")):
            vstuplenie = open(put("otsev-vstuplenie.md"), encoding="utf-8").read()
            if not vstuplenie.endswith("\n\n"):
                vstuplenie += "\n\n"
        open(put("otsev.md"), "w", encoding="utf-8").write(vstuplenie + otchet + "\n")
        print("собран otsev.md")
    else:
        print(otchet)


if __name__ == "__main__":
    main()
