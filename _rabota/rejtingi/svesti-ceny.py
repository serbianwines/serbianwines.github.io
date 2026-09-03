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

Пишет `ceny-vin.json`: ключ вина → цена, и отдельно список несведённого.
"""
import importlib.util, json, pathlib, re, statistics, sys, collections

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
# Дробная часть бывает любой длины: 1,5 л, 0,5 л, 0,375 л. Первая
# редакция читала только один знак после запятой и полубутылку Маканы
# («Makana 0.375L», 2970 динаров) приняла за обычную.
OBEM = re.compile(r"\b(\d(?:[.,]\d+)?)\s*L\b", re.I)


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
    MAGAZINY = [("vinoteka", "vinoteka-ceny.json"),
                ("winestars", "winestars-ceny.json"),
                ("cerpromet", "cerpromet-ceny.json")]
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
            syroe["vina"].append({**z, "magazin": imya})
        syroe["istochnik"].append(d["istochnik"])
        syroe["sobrano"] = max(syroe["sobrano"], d["sobrano"])
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
            po_magazinam[klyuch][z["magazin"]].append(z["cena_rsd"])
            if z.get("tip_vina"):
                sladost.setdefault(klyuch, z["tip_vina"])
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
            po_magazinam[podoshli[0]][z["magazin"]].append(z["cena_rsd"])
            if z.get("tip_vina"):
                sladost.setdefault(podoshli[0], z["tip_vina"])
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
        "ceny": cena,
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
