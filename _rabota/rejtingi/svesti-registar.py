# -*- coding: utf-8 -*-
"""Свести хозяйства с Винарским регистром.

Регистр называет производителей полным юридическим именем: «Мilan Aleksić
PR, proizvodnja vina i agro saveti “FITOMEDIK” Venčac». Vivino и Decanter
называют их маркой: «Fitomedik». Сводятся они по значимым словам: из имени
выбрасывается всё служебное — «винарија», «подрум», «д.о.о.», «пр»,
«производња вина» — и то, что осталось, ищется в имени записи регистра.

Совпадение принимается, только если все найденные записи сходятся на одном
насељу. Иначе пишутся кандидаты, но место не ставится: «Николић» в регистре
двенадцать, и выбирать между ними наугад нельзя.

**Столичный адрес местом не считается.** У регистра насеље — это адрес
юридического лица, и у трёх десятков винарий он городской: «Beograd —
Врачар», «Нови Београд», «Земун». Виноградника там нет, это квартира
владельца. Такие записи помечаются, но рејон по ним не ставится.

Пишет `registar-hozyaistv.json`. Регистр берётся `vzjat-registar.py`.
"""
import json, os, re, sys, collections, unicodedata

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)

# Городские општине Београда: у регистра это адрес конторы, не виноградник.
STOLICA = {
    "beograd - stari grad", "beograd - vračar", "beograd - voždovac",
    "beograd - palilula", "beograd - savski venac", "beograd - čukarica",
    "beograd - rakovica", "zvezdara - beograd", "novi beograd", "zemun",
}

# Слова, которые не различают хозяйства: правовая форма, род занятий,
# слово «винарија» на четырёх языках.
SLUZHEBNYE = set("""
vinarija vinarije vinariji vinarski vinarska vinarsko vinarije kuca kuce
vinska vinski vinsko podrum podrumi podruma vino vina vinu vinom doo dooel
ad pr preduzetnik preduzece privredno drustvo ogranicenom odgovornoscu
proizvodnja proizvodnju proizvodnje proizvodne proizvodna proizvodni
proizvodnju radnja radnje zanatska samostalna udruzenje vinogradara vinara
vinograd vinogradi vinogradarstvo grozda grozdja od sa the winery wine
wines vineyard vineyards weingut estate cellar cellars family porodicna
porodicno porodicni manufaktura imanje salas srl ltd gmbh company trgovinu
trgovina veliko malo usluge uslugu promet rakije rakija agro saveti agrar
poljoprivredna poljoprivredno gazdinstvo
""".split())

# Совпадения, отклонённые руками. Три случая, и каждый проверен:
# у одного адрес регистра — контора владельца, у двух совпало не имя
# хозяйства, а название села в имени чужой записи.
OTKLONENO = {
    "Dalia": "Регистр даёт Крушевац — это адрес общества. Сама винарија "
             "Кристине Лукић стоит в Рајцу-Смедовцу, Неготинска Крајина, и "
             "вина у Vivino подписаны Неготинском Крајином.",
    "Vinarija Vrbica": "Совпало не имя, а село: запись «VINARIJA VELES VELIKA "
             "VRBICA» — это Велес из Велике Врбице. Адрес самой Vinarija "
             "Vrbica на Vivino — Аранђеловац.",
    "Vinarija Venčac": "То же: «AGROZEBEC DOO Venčac» — это Агрозебец из "
             "жупског Венчца. Decanter относит вина Vinarija Venčac к "
             "Шумадији, а Венчац — ещё и гора под Аранђеловцем.",
}

# Совпадения, подтверждённые руками. Разбор ищет имя хозяйства целиком
# в имени записи регистра, а регистр пишет юридическое имя — и наше имя
# в нём иногда не помещается: «Monastery Visoki Dečani» против «Vinica
# Manastira Visoki Dečani», «Dukay-Sagmeister» против двух отдельных
# записей. Такие случаи разбираются глазами, по одному, с доказательством.
PODTVERZHDENO = {
    "Monastery Visoki Decani  (Манастирско Дечанско)": (
        ["3712"],
        "Запись № 3712 — «Vinica Manastira Visoki Dečaniˮ DOO», Велика "
        "Хоча, Призренски округ. Это винарија самог манастира Високи "
        "Дечани; другого производителя с этим именем в регистру нет. "
        "Разбор не свёл их сам: в имени регистра стоит «Manastira», "
        "а у нас английское «Monastery»."),
    "Jelena Munizaba PR Radnja za proizvodnju grozdja i vina, "
    "turizam i ugostiteljstvo.": (
        ["5326"],
        "Запись № 5326 — «JELENA MUNIŽABA PR RADNJA ZA PROIZVODNJU "
        "GROŽĐA I VINA…», Риђица, Западнобачки округ: то же имя и та же "
        "правовая форма. У нас оно пришло от AWC Vienna без диакритики, "
        "«Munizaba» вместо «Munižaba», и разбор его не узнал."),
}

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


def slova(imya):
    """Слова имени: кириллица в латиницу, диакритика снята, «dj» = «đ»."""
    s = latinicej(imya or "").lower().replace("dj", "đ")
    for a, b in (("š", "s"), ("đ", "d"), ("č", "c"), ("ć", "c"), ("ž", "z")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]+", " ", s).split()


def znachimye(imya):
    """Слова, по которым хозяйство вообще можно узнать."""
    return [w for w in slova(imya)
            if w not in SLUZHEBNYE and not w.isdigit() and len(w) > 2]


SKOBKI = re.compile(r"^(.*?)\s*[(\[]([^)\]]+)[)\]]\s*$")


def napisaniya(imya):
    """Написания одного имени. «Aglaya (Аглая)» — это одно слово дважды.

    Если складывать слова обоих написаний в одно требование, совпадения
    не будет никогда: в регистре имя записано один раз, а требований два.
    Поэтому половинки проверяются порознь.
    """
    varianty = [imya]
    sovpalo = SKOBKI.match(imya)
    if sovpalo:
        varianty += [sovpalo.group(1).strip(), sovpalo.group(2).strip()]
    elif " - " in imya:
        varianty += [c.strip() for c in imya.split(" - ", 1)]
    return [v for v in varianty if v]


def main():
    reg = json.load(open(put("vinarski-registar.json"), encoding="utf-8"))
    zapisi = reg["zapisi"]
    for z in zapisi:
        z["slova"] = set(slova(z["nazvanie"]))
        z["stolica"] = z["naselje"].lower() in STOLICA

    hozyaistva = [json.loads(s) for s in open(put("hozyaistva.jsonl"),
                                              encoding="utf-8") if s.strip()]

    itog, schet = {}, collections.Counter()
    for h in hozyaistva:
        trebovaniya = [znachimye(v) for v in napisaniya(h["hozyaistvo"])]
        trebovaniya = [t for t in trebovaniya if t]
        if not trebovaniya:
            schet["имя из одних служебных слов"] += 1
            continue
        podtverzhdeno = PODTVERZHDENO.get(h["hozyaistvo"])
        if podtverzhdeno:
            nomera = set(podtverzhdeno[0])
            nashlos = [z for z in zapisi if z["reg_nomer"] in nomera]
            if len(nashlos) != len(nomera):
                sys.exit("подтверждённой руками записи нет в регистре: %s"
                         % h["hozyaistvo"])
        else:
            nashlos = [z for z in zapisi
                       if any(all(w in z["slova"] for w in nuzhno)
                              for nuzhno in trebovaniya)]
        if not nashlos:
            schet["в регистре не нашлось"] += 1
            continue
        mesta = {z["naselje"] for z in nashlos}
        zapis = {
            "hozyaistvo": h["hozyaistvo"],
            "sovpalo": [{"reg_nomer": z["reg_nomer"], "nazvanie": z["nazvanie"],
                         "naselje": z["naselje"], "okrug": z["okrug"]}
                        for z in nashlos],
        }
        if podtverzhdeno:
            zapis["mesto"] = "%s, %s okrug" % (nashlos[0]["naselje"],
                                               nashlos[0]["okrug"])
            zapis["zamechanie"] = "подтверждено руками: " + podtverzhdeno[1]
            schet["подтверждено руками"] += 1
        elif h["hozyaistvo"] in OTKLONENO:
            zapis["mesto"] = ""
            zapis["zamechanie"] = "отклонено руками: " + OTKLONENO[h["hozyaistvo"]]
            schet["отклонено руками"] += 1
        elif len(mesta) > 1:
            zapis["mesto"] = ""
            zapis["zamechanie"] = "записей регистра несколько, и места разные"
            schet["несколько записей, места разные"] += 1
        elif nashlos[0]["stolica"]:
            zapis["mesto"] = ""
            zapis["zamechanie"] = ("адрес столичный (%s) — это контора, "
                                   "не виноградник" % nashlos[0]["naselje"])
            schet["столичный адрес"] += 1
        else:
            zapis["mesto"] = "%s, %s okrug" % (nashlos[0]["naselje"],
                                               nashlos[0]["okrug"])
            zapis["zamechanie"] = ""
            schet["место установлено"] += 1
        itog[h["klyuch"]] = zapis

    # Одна запись регистра — одно хозяйство. Если на неё притязают двое,
    # то либо это одно хозяйство под двумя именами — тогда его сводят
    # руками, с доказательством, в `sinonimy-hozyaistv.json`, — либо
    # совпадение ложное: «Manufaktura Spasić» садится на единственного
    # в регистре Спасића из Жупе, хотя делает сремску зеленику. Место
    # в обоих случаях не ставится.
    pretendenty = collections.defaultdict(list)
    for k, z in itog.items():
        if z["mesto"]:
            pretendenty[z["sovpalo"][0]["reg_nomer"]].append(k)
    for nomer, klyuchi in pretendenty.items():
        if len(klyuchi) < 2:
            continue
        for k in klyuchi:
            itog[k]["mesto"] = ""
            itog[k]["zamechanie"] = (
                "на запись регистра № %s притязают несколько хозяйств: %s"
                % (nomer, ", ".join(sorted(itog[x]["hozyaistvo"] for x in klyuchi))))
            schet["место установлено"] -= 1
            schet["на одну запись притязают несколько"] += 1

    json.dump({
        "chto_eto": "Хозяйства, найденные в Винарском регистру. Насеље регистра — "
                    "адрес юридического лица; столичные адреса местом не считаются.",
        "istochnik": reg["istochnik"],
        "vsego_v_registre": reg["vsego"],
        "hozyaistva": itog,
    }, open(put("registar-hozyaistv.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)

    print("хозяйств в таблице: %d, найдено в регистре: %d"
          % (len(hozyaistva), len(itog)))
    for chto, n in schet.most_common():
        print("   %-34s %d" % (chto, n))


if __name__ == "__main__":
    main()
