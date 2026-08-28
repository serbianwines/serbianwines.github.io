#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Свести собранное по настоящим рејонима, а не по главам книги.

Отдельно — сверка: какая глава книги какому рејону отвечает. Она нужна
не для укора книге, а для решения. Книга делит Сербию на десять глав,
рејонизација — на двадцать два рејона, и это разные сетки: одна глава
может покрывать три рејона, а целые рејоны в книгу не попасть вовсе.

    python3 _rabota/rejtingi/svesti-rejony.py --otchet
"""

import collections
import json
import os
import sys

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
FAJL = os.path.join(RYADOM, "po-rejonima.md")

GLAVY = {
    "fruska": "Фрушка гора", "subotica": "Суботичко-Хоргошская пешчара",
    "banat": "Банат", "sumadija": "Шумадия", "morave": "Три Моравы и Жупа",
    "negotin": "Неготинска Крайина", "toplica": "Топлица",
    "jugoistok": "Юго-восток", "podunavlje": "Подунавье и Белградский район",
    "metohija": "Косово и Метохия",
}


def put(imya):
    return os.path.join(RYADOM, imya)


def chitat(imya):
    return [json.loads(s) for s in open(put(imya), encoding="utf-8") if s.strip()]


def sobrat():
    hoz = chitat("hozyaistva.jsonl")
    oc = chitat("ocenki.jsonl")
    ng = chitat("nagrady.jsonl")
    spr = json.load(open(put("rejony-vinogorja.json"), encoding="utf-8"))

    po_klyuchu = {h["klyuch"]: h for h in hoz}
    # Ключ хозяйства в оценках не лежит — сводим по имени, как в таблицах.
    imya_klyuch = {h["hozyaistvo"]: h["klyuch"] for h in hoz}

    viv = collections.Counter()
    kri = collections.Counter()
    nag = collections.Counter()
    for o in oc:
        k = imya_klyuch.get(o["hozyaistvo"])
        if k:
            (viv if o["istochnik"] == "vivino" else kri)[k] += 1
    for z in ng:
        k = imya_klyuch.get(z["hozyaistvo"])
        if k:
            nag[k] += 1
    return hoz, po_klyuchu, spr, viv, kri, nag


def stroki():
    hoz, po_klyuchu, spr, viv, kri, nag = sobrat()
    poryadok = [r["rejon"] for r in spr["rejony"]]
    region = {r["rejon"]: r["region"] for r in spr["rejony"]}
    po_rejonu = collections.defaultdict(list)
    for h in hoz:
        po_rejonu[h["rejon"]].append(h)

    out = []
    out.append("## Что собралось по рејонима\n")
    out.append("Хозяйства разложены по действующей рејонизацији: "
               "3 региона, 22 рејона, 77 виногорја. Глава книги — "
               "отдельный столбец, она не обязана совпадать.\n")
    out.append("| Регион | Рејон | Хозяйств | Оценок Vivino | Оценок критиков | Наград |")
    out.append("|---|---|---|---|---|---|")
    for rejon in poryadok:
        spisok = po_rejonu.get(rejon, [])
        if not spisok:
            continue
        out.append("| %s | %s | %d | %d | %d | %d |"
                   % (region[rejon], rejon, len(spisok),
                      sum(viv[h["klyuch"]] for h in spisok),
                      sum(kri[h["klyuch"]] for h in spisok),
                      sum(nag[h["klyuch"]] for h in spisok)))
    pusto = [r for r in poryadok if not po_rejonu.get(r)]
    bez = po_rejonu.get(None, [])
    out.append("| — | **рејон не установлен** | %d | %d | %d | %d |"
               % (len(bez), sum(viv[h["klyuch"]] for h in bez),
                  sum(kri[h["klyuch"]] for h in bez),
                  sum(nag[h["klyuch"]] for h in bez)))
    if pusto:
        out.append("\n**Рејоны, из которых не собралось ни одного хозяйства:** "
                   + ", ".join(pusto) + ".\n")

    # --------------------------------------------- сверка с главами книги
    out.append("\n## Главы книги и рејоны\n")
    out.append("Столбец слева — глава книги, справа — в какие рејоны "
               "попадают её хозяйства по действующей рејонизацији.\n")
    out.append("| Глава книги | Рејоны её хозяйств |")
    out.append("|---|---|")
    po_glave = collections.defaultdict(collections.Counter)
    for h in hoz:
        if h["raion_knigi"]:
            po_glave[h["raion_knigi"]][h["rejon"]] += 1
    for kod, imya in GLAVY.items():
        c = po_glave.get(kod)
        if not c:
            out.append("| %s | нет хозяйств с установленным рејоном |" % imya)
            continue
        chasti = ["%s — %d" % (r or "не установлен", n)
                  for r, n in c.most_common()]
        out.append("| %s | %s |" % (imya, "; ".join(chasti)))

    v_knige = {h["rejon"] for h in hoz if h["raion_knigi"] and h["rejon"]}
    mimo = [r for r in poryadok if po_rejonu.get(r) and r not in v_knige]
    if mimo:
        out.append("\n**Рејоны, где хозяйства есть, а в книге их нет:**\n")
        for r in mimo:
            spisok = sorted(po_rejonu[r], key=lambda h: h["hozyaistvo"])
            out.append("- **%s** (%s) — %s"
                       % (r, region[r],
                          ", ".join(h["hozyaistvo"] for h in spisok[:12])
                          + (" и ещё %d" % (len(spisok) - 12) if len(spisok) > 12 else "")))

    # --------------------------------------------- виногорја внутри рејона
    # Книга строится от виноградарских областей, поэтому важно не только
    # сколько хозяйств в рејоне, но и как они разложены по его виногорјима
    # и какие виногорја пусты. Округ здесь не участвует вовсе: он
    # административный и к виноградарству отношения не имеет.
    vinogorja_rejona = {r["rejon"]: [v["vinogorje"] for v in r["vinogorja"]]
                        for r in spr["rejony"]}
    out.append("\n## Виногорја внутри рејонов\n")
    out.append("Официальных виногорја 77. Пустое виногорје — не ошибка: "
               "хозяйство может быть, но без установленного места.\n")
    out.append("| Рејон | Виногорје | Хозяйств |")
    out.append("|---|---|---|")
    for rejon in poryadok:
        spisok = po_rejonu.get(rejon, [])
        if not spisok:
            continue
        po_vg = collections.Counter(h["vinogorje"] for h in spisok)
        for vg in vinogorja_rejona.get(rejon, []):
            out.append("| %s | %s | %s |"
                       % (rejon, vg, po_vg.get(vg) or "—"))
        if po_vg.get(None):
            out.append("| %s | *виногорје не установлено* | %d |"
                       % (rejon, po_vg[None]))

    # --------------------------------------------- хозяйства по рејонима
    out.append("\n## Хозяйства по рејонима\n")
    out.append("Город — куда ехать. Это населённый пункт хозяйства, "
               "а не округ: округ единица государственного управления, "
               "к виноградарству отношения не имеет.\n")
    for rejon in poryadok:
        spisok = sorted(po_rejonu.get(rejon, []), key=lambda h: h["hozyaistvo"])
        if not spisok:
            continue
        out.append("\n### %s — %s\n" % (rejon, region[rejon]))
        out.append("| Хозяйство | Виногорје | Город | Откуда рејон | В книге |")
        out.append("|---|---|---|---|---|")
        for h in spisok:
            out.append("| %s | %s | %s | %s | %s |"
                       % (h["hozyaistvo"], h["vinogorje"] or "—",
                          h.get("gorod") or "—",
                          h["rejon_istochnik"],
                          GLAVY.get(h["raion_knigi"], "—")))
    return out


def main():
    out = stroki()
    if "--otchet" in sys.argv:
        vstuplenie = put("rejony-vstuplenie.md")
        nachalo = (open(vstuplenie, encoding="utf-8").read()
                   if os.path.exists(vstuplenie) else "# Рејоны и виногорја\n")
        with open(FAJL, "w", encoding="utf-8") as f:
            f.write(nachalo.rstrip() + "\n\n")
            f.write("<!-- Собрано скриптом svesti-rejony.py. Руками не править. -->\n\n")
            f.write("\n".join(out) + "\n")
        print("собран %s" % os.path.basename(FAJL))
    else:
        print("\n".join(out))


if __name__ == "__main__":
    main()
