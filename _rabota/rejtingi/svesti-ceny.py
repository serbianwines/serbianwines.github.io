# -*- coding: utf-8 -*-
"""Свести цены магазина с нашей таблицей вин.

Цены лежат в `vinoteka-ceny.json` сырьём, как их печатает магазин. Свод
вынесен отдельно нарочно: он неточен, и его неточность надо видеть,
а не прятать внутри сборщика.

Магазин зовёт вина короче нас: «Erdevik Bella Novela» — это наша «Bella
Novela Sauvignon Blanc», «Janko Mesečina» — «Mesečina Penušavo Belo».
Поэтому после точного ключа пробуется совпадение по началу имени, но
**только когда в доме подходит ровно одно вино**. Если подходит несколько
— «Chardonnay» годится и «Chardonnay barrique», и «Classic Chardonnay», —
цена не ставится: это разные вина, и выбирать между ними наугад нельзя.

Пишет `ceny-vin.json`: ключ вина → цена, и отдельно список несведённого.
"""
import importlib.util, json, pathlib, re, sys, collections

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
OBEM = re.compile(r"\b(\d(?:[.,]\d)?)\s*L\b", re.I)


def chistoe_imya(imya):
    return re.sub(r"\s+", " ", AKCIYA.sub("", imya or "")).strip()


def ne_ta_butylka(imya):
    """Магнум — другой товар и другая цена, а имя вина то же.

    Снимать объём из имени нельзя: цена полуторалитровой бутылки встанет
    обычной. «Rodoslov Grand Reserve» стоит 5025 динаров, а он же 1,5 л —
    13 990. Поэтому нестандартный объём просто пропускается.
    """
    sovpalo = OBEM.search(imya or "")
    return bool(sovpalo) and sovpalo.group(1).replace(",", ".") != "0.75"


def slova(st, imya):
    return [c for c in st.klyuch(st.latinicej(imya or "")).split("-") if c]


def main():
    st = tablicy()
    syroe = json.loads((ZDES / "vinoteka-ceny.json").read_text(encoding="utf-8"))
    vina = [json.loads(s) for s in (ZDES / "vina.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]

    # Наши вина, разложенные по дому: имя в словах → ключ.
    po_domu = collections.defaultdict(list)
    for v in vina:
        po_domu[st.klyuch_hozyaistva(v["hozyaistvo"])].append(
            (slova(st, v["vino"]), v["klyuch"]))
    nashi = {v["klyuch"] for v in vina}

    def dom_iz_imeni(imya):
        """Хозяйство по началу имени вина.

        У сотни с лишним позиций магазин оставил поле производителя
        пустым, а имя дома при этом стоит первым словом самого вина:
        «Aleksandrović Trijumf», «Kovačević Aurelius». Берётся самое
        длинное начало, которое оказывается известным нам домом:
        «Zvonko Bogdan» длиннее и точнее, чем «Zvonko».
        """
        chasti = (imya or "").split()
        for skolko in range(min(4, len(chasti) - 1), 0, -1):
            nachalo = " ".join(chasti[:skolko])
            if st.klyuch_hozyaistva(nachalo) in po_domu:
                return nachalo
        return ""

    cena, spor, netu = {}, [], []
    schet = collections.Counter()
    iz_imeni = 0          # считается отдельно: это не исход, а способ
    for z in syroe["vina"]:
        if not z.get("cena_rsd"):
            continue
        imya = chistoe_imya(z["vino"])
        if ne_ta_butylka(imya):
            schet["не та бутылка (не 0,75)"] += 1
            continue
        if not z["hozyaistvo"].strip():
            z = {**z, "hozyaistvo": dom_iz_imeni(imya)}
            if z["hozyaistvo"]:
                iz_imeni += 1
        klyuch = st.klyuch_vina(z["hozyaistvo"], imya)
        if klyuch in nashi:
            schet["ключ сошёлся точно"] += 1
            cena.setdefault(klyuch, z["cena_rsd"])
            continue
        hoz = st.klyuch_hozyaistva(z["hozyaistvo"])
        if hoz not in po_domu:
            netu.append({**z, "pochemu": "хозяйства нет в наших таблицах"})
            schet["хозяйства нет вовсе"] += 1
            continue
        # Имя магазина без имени дома впереди — с ним и сравниваем.
        moi = slova(st, imya)
        bez_doma = st.klyuch_vina(z["hozyaistvo"], imya).split("-")
        bez_doma = bez_doma[len(hoz.split("-")):]
        podoshli = [k for nash, k in po_domu[hoz]
                    if nash[:len(bez_doma)] == bez_doma or bez_doma[:len(nash)] == nash]
        if len(podoshli) == 1:
            schet["сошлось по началу имени"] += 1
            cena.setdefault(podoshli[0], z["cena_rsd"])
        elif podoshli:
            schet["подходит несколько — не ставим"] += 1
            spor.append({**z, "kandidaty": podoshli})
        else:
            schet["такого вина у нас нет"] += 1
            netu.append({**z, "pochemu": "дом есть, вина нет"})

    (ZDES / "ceny-vin.json").write_text(json.dumps({
        "chto_eto": "Ключ вина → розничная цена в динарах. Свод имён магазина "
                    "с нашими; неточности перечислены рядом.",
        "istochnik": syroe["istochnik"],
        "sobrano": syroe["sobrano"],
        "ceny": cena,
        "podhodit_neskolko": spor,
        "ne_nashlos": netu,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print("позиций магазина с ценой: %d" % sum(schet.values()))
    for k, n in schet.most_common():
        print("   %-30s %4d" % (k, n))
    print("   (из них дом взят из имени вина: %d)" % iz_imeni)
    print("\nцена проставлена %d нашим винам из %d → ceny-vin.json"
          % (len(cena), len(vina)))


if __name__ == "__main__":
    main()
