# -*- coding: utf-8 -*-
"""Годовой выбор `vino.rs` — «Najbolja vina Srbije» — из сохранённых страниц.

Единственная сербская экспертная дорожка в наших таблицах. Портал сам
пишет, что это «nikada nije bio ocenjivanje u klasičnom smislu»: не
дегустация вслепую, а годовой обзор редакции плюс большой опрос среди
винных профессионалов, и в счёт идут только вина, вышедшие на рынок за
последние двенадцать месяцев. Поэтому запись идёт наградой с местом
в категории, а не баллом: шкалы здесь нет.

Машиной сайт не берётся — стоит за капчей SiteGround: на запрос приходит
код 202 и переход на `/.well-known/sgcaptcha/`. Страницы сохранил автор
браузером (Ctrl+S), как с Falstaff и Maxi.

    py -3 _rabota/rejtingi/vzjat-vino-rs.py kesh-vino-rs/*.html

Сами страницы лежат в `kesh-vino-rs/` и держатся в истории нарочно, в
отличие от кешей магазинов: те пересобираются запуском, а эту капчу
машиной не пройти, и без сохранённых страниц разбор не повторить.

Год берётся из имени файла. Разметка от года к году разная, и это не
прихоть — менялся сам формат выбора:

    2019        <h3>категория</h3>, победитель в <strong><em>…</em></strong>,
                дальше «U najužoj konkurenciji» и места со второго по
                десятое списком «1) …» — нумерация там своя, от первого
                догоняющего, поэтому к ней прибавляется единица.
    2020–2023   <h4>категория</h4>, дальше готовая десятка «1. … 2. …».
    2024–2025   <h2>раздел</h2> / <h3>подкатегория</h3> / <h4>победитель</h4>;
                десяток больше нет, только победители, зато по два на
                категорию — обычный и органический.

Строка вина устроена одинаково все годы: «имя урожай хозяйство», где
урожай — четыре цифры (иногда через дробь: «PK Zero 2017/18 Sagmeister»).
По ним она и делится. Если года в строке нет, это категория не о вине —
винодельня, человек, событие, — и имя пишется в поле хозяйства.

Пишет `vino-rs-zapisi.json`; строки для `nagrady-zapisi.jsonl` печатает
ключ `--stroki`.
"""
import argparse
import html
import importlib.util
import json
import pathlib
import re
import sys
import time
import unicodedata

ZDES = pathlib.Path(__file__).resolve().parent

TELO = re.compile(r'<div[^>]*class="[^"]*itemFullText[^"]*"[^>]*>(.*)', re.S)
KONEC = ("Srodni tekstovi", "itemLinks", 'class="itemBackToTop')
UZEL = re.compile(r"<(h[234])[^>]*>(.*?)</\1>", re.S)
POBEDITEL_2019 = re.compile(r"<strong>\s*<em>(.*?)</em>", re.S)
DOGONYAYUSHIE_2019 = re.compile(r"\d\)\s*<em>(.*?)</em>", re.S)
ABZAC = re.compile(r"<p[^>]*>(.*?)</p>", re.S)
UROZHAJ = re.compile(r"\b(19\d\d|20\d\d)(\s*/\s*(?:\d{4}|\d{2}))?\b")
# У игристого урожай бывает не назван вовсе: «Mesečina NV Janko», где
# NV — non-vintage. Строка устроена так же, и делить её надо там же.
BEZ_UROZHAYA = re.compile(r"\bNV\b")
ORGANIKA = re.compile(r"\((?:organsko|organski|prirodno)\)\s*$", re.I)

# Цвет по категории — для ключа награды: у хозяйства с одним именем вина
# бывает и красное, и белое, и без цвета они схлопываются в одну запись.
CVET = {"красное": "red", "белое": "white", "розе": "rose"}


def prosto(imya):
    """Имя категории без регистра, диакритики и уточнений в скобках."""
    imya = re.sub(r"\([^)]*\)", " ", imya or "")
    # Год выпуска в имени категории («…uspon u 2021. godini») к делу
    # не относится: категория одна и та же из года в год.
    imya = re.sub(r"\b20\d\d\.?\s*", " ", imya)
    imya = "".join(z for z in unicodedata.normalize("NFD", imya.lower())
                   if unicodedata.category(z) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", imya)).strip()


# Сербское имя категории → наше. Переведено руками: имена у портала
# гуляют от года к году («od autohtone ili novostvorene sorte» в 2019-м
# и «od lokalne sorte» в 2022-м — одно и то же), и сводить их по
# похожести нельзя.
KATEGORII = {
    "najbolje crveno vino srbije": "лучшее красное",
    "najbolje belo vino srbije": "лучшее белое",
    "najbolje roze vino srbije": "лучшее розе",
    "najbolje roze vino": "лучшее розе",
    "najbolje penusavo vino srbije": "лучшее игристое",
    "najbolje penusavo vino": "лучшее игристое",
    "najbolje oranz vino srbije": "лучшее оранж",
    "najbolje oranz vino": "лучшее оранж",
    "najbolje poluslatko ili slatko vino srbije": "лучшее сладкое или полусладкое",
    "najbolje slatko ili poluslatko vino srbije": "лучшее сладкое или полусладкое",
    "najbolje slatko ili poluslatko vino": "лучшее сладкое или полусладкое",
    "najbolje prirodno slatko ili poluslatko vino srbije":
        "лучшее сладкое или полусладкое",
    "slatka ili poluslatka vina": "лучшее сладкое или полусладкое",
    "najbolje pojacano vino srbije": "лучшее креплёное",
    "najbolje pojacano vino": "лучшее креплёное",
    "pojacana vina": "лучшее креплёное",
    "najbolje crveno vino srbije od autohtone ili novostvorene sorte":
        "лучшее красное, местные сорта",
    "najbolje belo vino srbije od autohtone ili novostvorene sorte":
        "лучшее белое, местные сорта",
    "najbolje crveno vino srbije od lokalne sorte": "лучшее красное, местные сорта",
    "najbolje belo vino srbije od lokalne sorte": "лучшее белое, местные сорта",
    "najbolje crveno vino od lokalnih sorti": "лучшее красное, местные сорта",
    "najbolje belo vino od lokalnih sorti": "лучшее белое, местные сорта",
    "najbolje crveno vino od internacionalnih sorti":
        "лучшее красное, международные сорта",
    "najbolje belo vina od internacionalnih sorti":
        "лучшее белое, международные сорта",
    "najbolje crveno organsko ili prirodno vino srbije": "лучшее красное, органика",
    "najbolje belo organsko ili prirodno vino srbije": "лучшее белое, органика",
    "najbolje organsko ili prirodno vino srbije": "лучшее органическое",
    "tradicionalna i sarmat metoda": "лучшее игристое, классический метод",
    "methode ancestrale i petillant naturel": "лучшее игристое, предковый метод",
    "serbian best buy": "за свои деньги",
    "crveno vino s najboljim odnosom cene i kvaliteta": "за свои деньги, красное",
    "belo vino s najboljim odnosom cene i kvaliteta": "за свои деньги, белое",
    "roze vino s najboljim odnosom cene i kvaliteta": "за свои деньги, розе",
    "roze vina s najboljim odnosom cene i kvaliteta": "за свои деньги, розе",
    "crveno vino srbije s najboljim odnosom cene i kvaliteta":
        "за свои деньги, красное",
    "belo vino srbije s najboljim odnosom cene i kvaliteta": "за свои деньги, белое",
    "roze vino srbije s najboljim odnosom cene i kvaliteta": "за свои деньги, розе",
    "crveno vino od internacionalnih sorti s najboljim odnosom cene i kvaliteta":
        "за свои деньги, красное, международные сорта",
    "crveno vino od lokalnih sorti s najboljim odnosom cene i kvaliteta":
        "за свои деньги, красное, местные сорта",
    "belo vino od internacionalnih sorti s najboljim odnosom cene i kvaliteta":
        "за свои деньги, белое, международные сорта",
    "belo vino od lokalnih sorti s najboljim odnosom cene i kvaliteta":
        "за свои деньги, белое, местные сорта",
    "najbolja vinarija": "винодельня года",
    "najbolja vinarija srbije": "винодельня года",
    "najbolja mala vinarija": "лучшая малая винодельня",
    "najbolja mala vinarija srbije": "лучшая малая винодельня",
    "najbolja mlada vinarija": "лучшая молодая винодельня",
    "najbolja mlada vinarija srbije": "лучшая молодая винодельня",
    "priznanje za poseban doprinos srpskom vinarstvu":
        "особый вклад в сербское виноделие",
    "najveci doprinos vinskom turizmu": "вклад в винный туризм",
    "najveci doprinos vinskom turizmu srbije": "вклад в винный туризм",
    "vinska licnost godine": "винная личность года",
    "vinska licnost godine u srbiji": "винная личность года",
    "najbolji vinski brend": "лучший винный бренд",
    "najbolji vinski brend srbije": "лучший винный бренд",
    "najbolji marketing": "лучший маркетинг",
    "najbolji dizajn etiketa": "лучший дизайн этикетки",
    "najbolji dizajn etikete": "лучший дизайн этикетки",
    "najbolja vinska manifestacija": "лучшее винное событие",
    "najbolja vinska manifestacija u srbiji": "лучшее винное событие",
    "najprijatnije iznena enje": "самый приятный сюрприз",
    # «Vinarija od koje se očekuje najveći uspon u 2021. godini»: год
    # в имени свой у каждого выпуска, поэтому ключ без него.
    "vinarija od koje se ocekuje najveci uspon u godini":
        "винодельня, от которой ждут взлёта",
}
# Подкатегории 2025 года названы одним словом и держатся на разделе.
KATEGORII_RAZDELA = {
    ("crvena vina", "internacionalne sorte"): "лучшее красное, международные сорта",
    ("crvena vina", "lokalne sorte"): "лучшее красное, местные сорта",
    ("bela vina", "internacionalne sorte"): "лучшее белое, международные сорта",
    ("bela vina", "lokalne sorte"): "лучшее белое, местные сорта",
    ("roze vina", ""): "лучшее розе",
    ("oranz vina", ""): "лучшее оранж",
}
# Разделы, в которых голая подкатегория относится к вину этого цвета.
RAZDEL_CVET = {"crvena vina": "красное", "bela vina": "белое",
               "roze vina": "розе", "oranz vina": "оранж",
               "penusava vina": "игристое", "desertna vina": "десертное"}


def tekst(kus):
    return re.sub(r"\s+", " ",
                  html.unescape(re.sub(r"<[^>]+>", " ", kus))).replace("\xa0", " ").strip()


def telo_stati(stranica):
    sovpalo = TELO.search(stranica)
    t = sovpalo.group(1) if sovpalo else stranica
    for konec in KONEC:
        k = t.find(konec)
        if k > 0:
            t = t[:k]
    return re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)


def desyatka(kus):
    """Десятка из категории: один абзац, строки разделены `<br>`.

    Резать по одному номеру нельзя: после десятой строки без всякого
    разделителя начинается описание, и «10. Prokupac 2017 Kostić»
    прирастало целым абзацем прозы. Поэтому список берётся абзацем,
    а строки — по `<br>`; номера при этом обязаны идти подряд.
    """
    for abzac in ABZAC.findall(kus):
        najdeno, zhdem = [], 1
        for stroka in re.split(r"<br\s*/?>", abzac, flags=re.I):
            sovpalo = re.match(r"(10|[1-9])[.)]\s*(.+)", tekst(stroka))
            if not sovpalo or int(sovpalo.group(1)) != zhdem:
                continue
            najdeno.append((zhdem, sovpalo.group(2)))
            zhdem += 1
        if najdeno:
            return najdeno
    return []


def po_chelovecheski(imya):
    """Заголовки 2024 и 2025 годов набраны капслоком, и «AURUM 2020
    RALEVIĆ» пошло бы в книгу криком. Сплошная заглавная строка
    приводится к обычному виду; строки, где регистр смешан, не трогаются.
    Точное написание внутри слова так не восстановить («SoviNoa» станет
    «Sovinoa»), но ключ вина от регистра не зависит, а увидеть имя
    набранным капслоком хуже.
    """
    if not imya or any(z.islower() for z in imya):
        return imya
    return re.sub(r"[A-Za-zČĆŠĐŽčćšđžÁÉÍÓÚáéíóú’'\u00c0-\u024f]+",
                  lambda m: m.group(0)[:1] + m.group(0)[1:].lower(), imya)


def otdelit_dom(hvost, st, doma):
    """Из хвоста строки вынуть имя дома, а остальное вернуть вину.

    Портал ставит год не всегда после имени вина: «Furmint 2017 Kew
    Sagmeister» — это «Furmint Kew» Сагмајстера, а не вино «Furmint»
    хозяйства «Kew Sagmeister». То же с «Brut 2016 Blanc de Blancs
    Lastar» и «LH Zero 2016 Lipolist Sagmeister». Поэтому от хвоста
    отрезается самый длинный конец, который мы знаем как хозяйство;
    что осталось впереди — часть имени вина. Не узнали ни одного конца —
    хвост целиком считается домом, как и раньше.
    """
    slova = hvost.split()
    for skolko in range(len(slova)):
        dom = " ".join(slova[skolko:])
        if st and st.klyuch_hozyaistva(dom) in doma:
            return " ".join(slova[:skolko]), dom
    return "", hvost


def razobrat_stroku(stroka, st=None, doma=frozenset()):
    """«Bukovski Cuvee 2021 Matalj» → вино, урожай, хозяйство."""
    stroka = re.sub(r"\s+", " ", stroka).strip(" .,;:")
    organika = bool(ORGANIKA.search(stroka))
    stroka = ORGANIKA.sub("", stroka).strip()
    posledniy = None
    for sovpalo in UROZHAJ.finditer(stroka):
        posledniy = sovpalo
    if not posledniy:
        bez_goda = BEZ_UROZHAYA.search(stroka)
        if bez_goda:
            return {"vino": po_chelovecheski(
                        stroka[:bez_goda.start()].strip(" .,-")),
                    "urozhaj": None, "bez_urozhaya": True,
                    "hozyaistvo": po_chelovecheski(
                        stroka[bez_goda.end():].strip(" .,-")),
                    "organika": organika}
        return {"hozyaistvo": po_chelovecheski(stroka), "vino": "",
                "urozhaj": None, "organika": organika}
    hvost_vina, dom = otdelit_dom(stroka[posledniy.end():].strip(" .,-"), st, doma)
    imya_vina = (stroka[:posledniy.start()].strip(" .,-")
                 + (" " + hvost_vina if hvost_vina else "")).strip()
    return {
        "vino": po_chelovecheski(imya_vina),
        "urozhaj": int(posledniy.group(1)),
        "hozyaistvo": po_chelovecheski(dom),
        "organika": organika,
    }


def nashi_doma():
    """Ключи наших хозяйств — чтобы отличить награду хозяйству от награды
    человеку или событию. «Vinska ličnost godine» — это люди, «Najbolja
    vinska manifestacija» — сборища; ни то, ни другое хозяйством не
    является, и в таблицу наград им нельзя. Признак — не имя категории:
    у «лучшего дизайна этикетки» в 2024 году названо вино, а в 2023-м
    хозяйство. Признак простой: назвали урожай — речь о вине; не назвали
    и имя узнаётся хозяйством — о хозяйстве; иначе ни о том, ни о другом.
    """
    spec = importlib.util.spec_from_file_location("st", ZDES / "sobrat-tablicy.py")
    st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st)
    doma = set()
    put = ZDES / "hozyaistva.jsonl"
    if put.exists():
        for stroka in put.read_text(encoding="utf-8").splitlines():
            if not stroka.strip():
                continue
            h = json.loads(stroka)
            for imya in h.get("imena") or [h["hozyaistvo"]]:
                doma.add(st.klyuch_hozyaistva(imya))
    return st, doma


def razobrat_stranicu(stranica, god, st=None, doma=frozenset()):
    t = telo_stati(stranica)
    uzly = [(m.group(1), tekst(m.group(2)), m.end()) for m in UZEL.finditer(t)]
    uzly = [(tip, imya, konec) for tip, imya, konec in uzly if imya]
    zapisi, ne_uznano = [], []
    razdel = ""
    for nomer, (tip, imya, konec) in enumerate(uzly):
        sledom = uzly[nomer + 1][2] - len(uzly[nomer + 1][1]) if nomer + 1 < len(uzly) \
            else len(t)
        kus = t[konec:sledom]
        if god >= 2024 and tip == "h2":
            razdel = prosto(imya)
            # У «ROZE VINA» и «ORANŽ VINA» в 2025-м подкатегории нет
            # вовсе: победители стоят прямо под разделом. Раздел тогда
            # и есть категория.
            if not (nomer + 1 < len(uzly) and uzly[nomer + 1][0] == "h4"):
                continue
        if god >= 2024 and tip == "h4":
            continue                       # победители берутся при своей категории
        kategoriya = KATEGORII.get(prosto(imya))
        if not kategoriya and god >= 2024:
            podkategoriya = "" if tip == "h2" else prosto(imya)
            kategoriya = KATEGORII_RAZDELA.get((razdel, podkategoriya))
        if not kategoriya:
            ne_uznano.append({"god": god, "zagolovok": imya})
            continue
        if god >= 2024:
            # Победители — заголовки <h4> до следующей категории.
            svoi = [(1, i) for _, i, _ in
                    [u for u in uzly[nomer + 1:] if u[0] == "h4"]
                    [:kolichestvo_h4(uzly, nomer)]]
        elif god == 2019:
            pobeditel = POBEDITEL_2019.search(kus)
            svoi = [(1, tekst(pobeditel.group(1)))] if pobeditel else []
            svoi += [(n + 2, tekst(x))
                     for n, x in enumerate(DOGONYAYUSHIE_2019.findall(kus))]
        else:
            svoi = desyatka(kus)
        for mesto, stroka in svoi:
            razobrano = razobrat_stroku(stroka, st, doma)
            if not razobrano["hozyaistvo"]:
                continue
            kat = kategoriya
            if razobrano.pop("organika") and "органика" not in kat:
                kat += ", органика"
            komu = "vino" if (razobrano["urozhaj"]
                              or razobrano.get("bez_urozhaya")) else (
                "hozyaistvo" if st and st.klyuch_hozyaistva(
                    razobrano["hozyaistvo"]) in doma else "ne_vino")
            zapisi.append({
                "istochnik": "vino.rs", "god": god, "kategoriya": kat,
                "mesto": str(mesto), "cvet": cvet_kategorii(kat),
                "komu": komu,
                "stranica": "vino.rs, годовой тест %d" % god, **razobrano})
    return zapisi, ne_uznano


def kolichestvo_h4(uzly, nomer):
    """Сколько заголовков-победителей относится к этой категории:
    все, что стоят до следующей категории (h2 или h3)."""
    skolko = 0
    for tip, _, _ in uzly[nomer + 1:]:
        if tip == "h4":
            skolko += 1
        else:
            break
    return skolko


def cvet_kategorii(kat):
    for slovo, cvet in CVET.items():
        if kat.startswith("лучшее " + slovo) or kat.startswith("за свои деньги, " + slovo):
            return cvet
    return ""


def main():
    razbor = argparse.ArgumentParser()
    razbor.add_argument("fajly", nargs="+", help="сохранённые страницы vino.rs")
    razbor.add_argument("--stroki", action="store_true",
                        help="печатать строки для dobavit-nagrady.py")
    kljuchi = razbor.parse_args()

    st, doma = nashi_doma()
    vse, ne_uznano = [], []
    for imya in kljuchi.fajly:
        put = pathlib.Path(imya)
        sovpalo = re.search(r"(20\d\d)", put.name)
        if not sovpalo:
            print("год не назван в имени файла: %s" % put.name, file=sys.stderr)
            continue
        god = int(sovpalo.group(1))
        zapisi, ne = razobrat_stranicu(
            put.read_text(encoding="utf-8", errors="replace"), god, st, doma)
        vse += zapisi
        ne_uznano += ne
        print("  %d: записей %3d, категорий %2d, заголовков не узнано %d"
              % (god, len(zapisi), len({z["kategoriya"] for z in zapisi}), len(ne)))

    (ZDES / "vino-rs-zapisi.json").write_text(json.dumps({
        "chto_eto": "Годовой выбор vino.rs «Najbolja vina Srbije»: место "
                    "в категории, а не балл. Единственная сербская "
                    "экспертная дорожка в наших данных.",
        "istochnik": "vino.rs, раздел «Veliki test», сохранённые страницы",
        "sobrano": time.strftime("%Y-%m-%d"),
        "komu_chto": {k: sum(1 for z in vse if z["komu"] == k)
                      for k in ("vino", "hozyaistvo", "ne_vino")},
        "zapisi": vse,
        "zagolovki_ne_uznany": ne_uznano,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nвсего %d записей за %d лет → vino-rs-zapisi.json"
          % (len(vse), len({z["god"] for z in vse})))
    if ne_uznano:
        print("заголовков без перевода: %d — %s"
              % (len(ne_uznano),
                 "; ".join(sorted({z["zagolovok"][:40] for z in ne_uznano}))))
    if kljuchi.stroki:
        # В таблицу наград идут только записи о вине и о хозяйстве:
        # человек и событие хозяйством не являются.
        for z in [x for x in vse if x["komu"] != "ne_vino"]:
            print(" | ".join(["vino.rs", str(z["god"]), z["kategoriya"],
                              z["mesto"], z["hozyaistvo"], z["vino"],
                              str(z["urozhaj"] or ""), z["stranica"], z["cvet"]]))


if __name__ == "__main__":
    main()
