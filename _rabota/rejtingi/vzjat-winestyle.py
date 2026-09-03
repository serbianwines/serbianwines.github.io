# -*- coding: utf-8 -*-
"""Годовые списки сербских вин журнала «Wine Style».

Единственный найденный сербский голос, который говорит о вине сам, а не
пересказывает иностранное жюри. В конце года журнал печатает список
сербских вин, «которые привлекли особое внимание».

**Это не оценка качества, и журнал говорит это сам:** «Ovo nije lista
najboljih» (2019), «Lista koja sledi ne predstavlja odabir najboljih,
već vina koja su po raznim kriterijumima bila u fokusu vinske javnosti»
(2021). В список попадают за стиль, за редкий сорт, за удачную кампанию,
за этикетку. Поэтому собранное **не заводится ни в одну дорожку
рейтингов** и лежит отдельным файлом: это показание о заметности, а не
о качестве, и решать, нужно ли оно книге, — автору.

Разметка у каждого года своя, и порядок «вино/хозяйство» меняется:

    2019  <h2><strong>ВИНО</strong> ХОЗЯЙСТВО</h2>
    2020  <p>ХОЗЯЙСТВО<em> ВИНО</em></p>
    2021  <h3>ВИНО / ХОЗЯЙСТВО</h3>
    2023  <h3>ХОЗЯЙСТВО / ВИНО</h3>

Где стороны разделены косой чертой, порядок не угадывается, а решается:
половина, чей ключ известен нам как хозяйство, и есть хозяйство. Если
не узнаётся ни одна или узнаются обе — пара остаётся неразобранной
и попадает в `ne_razobrano`, а не выдумывается.

Пишет `winestyle-spiski.json`. Кеш — в `kesh-winestyle/`.
"""
import html
import importlib.util
import json
import pathlib
import re
import time
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-winestyle"
PAUZA = 1.5
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Год списка и адрес. Адреса найдены по карте сайта: журнал зовёт список
# то «najatraktivnija srpska vina», то «top lista srpskih vina».
SPISKI = [
    (2019, "https://winestyle.rs/2020/najatraktivnija-srpska-vina-u-2019/"),
    (2020, "https://winestyle.rs/2020/najatraktivnija-srpska-vina-u-2020/"),
    (2021, "https://winestyle.rs/2022/top-lista-srpskih-vina-u-2021/"),
    (2023, "https://winestyle.rs/2024/najatraktivnija-srpska-vina-u-2023/"),
]

TELO = re.compile(r'<div[^>]*class="[^"]*entry-content[^"]*"[^>]*>(.*)', re.S)
ZAGOLOVOK = re.compile(r"<h([23])[^>]*>(.*?)</h\1>", re.S)
ABZAC = re.compile(r"<p[^>]*>(.*?)</p>", re.S)
SILNO = re.compile(r"<strong[^>]*>(.*?)</strong>", re.S)
KURSIV = re.compile(r"<em[^>]*>(.*?)</em>", re.S)
# Поля, которые журнал печатает под именем вина. Есть не у всех лет.
POLE = {
    "sorta": re.compile(r"Sortni sastav:\s*([^\n]{2,80})|Sorta:\s*([^\n]{2,80})", re.I),
    "urozhaj": re.compile(r"Berba:\s*(\d{4})", re.I),
    "krepost": re.compile(r"Alkohol:\s*([\d,\.]+)\s*%", re.I),
    "cena_rsd": re.compile(r"maloprodajna cena:\s*([\d\.]+)", re.I),
}


def tablicy():
    spec = importlib.util.spec_from_file_location("st", ZDES / "sobrat-tablicy.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def vzjat(adres, imya_kesha):
    KESH.mkdir(exist_ok=True)
    fajl = KESH / imya_kesha
    if fajl.exists():
        return fajl.read_text(encoding="utf-8", errors="replace")
    zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
    for popytka in range(4):
        try:
            with urllib.request.urlopen(zapros, timeout=90) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            break
        except Exception:
            if popytka == 3:
                raise
            time.sleep(2 ** (popytka + 1))
    fajl.write_text(tekst, encoding="utf-8")
    time.sleep(PAUZA)
    return tekst


def prosto(kus):
    """Разметка прочь, неразрывный пробел — обычным."""
    return re.sub(r"\s+", " ",
                  html.unescape(re.sub(r"<[^>]+>", " ", kus))).replace("\xa0", " ").strip()


def pary_goda(telo, god):
    """Пары «одно, другое» так, как их печатает этот год."""
    if god == 2020:
        # <p>ХОЗЯЙСТВО<em> ВИНО</em></p>: хозяйство прямым, вино курсивом.
        pary = []
        for kus in ABZAC.findall(telo):
            kursiv = KURSIV.search(kus)
            if not kursiv:
                continue
            dom = prosto(KURSIV.sub(" ", kus))
            vino = prosto(kursiv.group(1))
            # Отсекаем вступление: там курсивом набрано имя журнала.
            if dom and vino and len(dom) < 40 and "Wine Style" not in vino:
                pary.append((dom, vino))
        return pary
    if god == 2019:
        # <h2><strong>ВИНО</strong> ХОЗЯЙСТВО</h2>
        pary = []
        for _, kus in ZAGOLOVOK.findall(telo):
            silno = SILNO.search(kus)
            if not silno:
                continue
            vino = prosto(silno.group(1))
            dom = prosto(SILNO.sub(" ", kus))
            if vino and dom:
                pary.append((vino, dom))
        return pary
    # 2021 и 2023: «ОДНО / ДРУГОЕ» в заголовке.
    pary = []
    for _, kus in ZAGOLOVOK.findall(telo):
        stroka = prosto(kus)
        if "/" not in stroka or len(stroka) > 90:
            continue
        levo, pravo = [c.strip() for c in stroka.split("/", 1)]
        if levo and pravo:
            pary.append((levo, pravo))
    return pary


def razobrat_pole(hvost):
    """Сорт, урожай, крепость, цена — из абзаца под именем вина."""
    najdeno = {}
    tekst = prosto(hvost)
    for imya, vyrazhenie in POLE.items():
        sovpalo = vyrazhenie.search(tekst)
        if not sovpalo:
            continue
        znachenie = next((g for g in sovpalo.groups() if g), "")
        if imya == "cena_rsd":
            znachenie = znachenie.replace(".", "")
        najdeno[imya] = znachenie.strip(" .,")
    return najdeno


def main():
    st = tablicy()
    nashi_doma = set()
    for stroka in (ZDES / "hozyaistva.jsonl").read_text(encoding="utf-8").splitlines():
        if stroka.strip():
            h = json.loads(stroka)
            for imya in h.get("imena") or [h["hozyaistvo"]]:
                nashi_doma.add(st.klyuch_hozyaistva(imya))

    # Имена вин по дому — для развязки, когда домом выглядят обе
    # половины: «Doja / Breg» — у Дојe есть «Breg Prokupac» и «Breg
    # Cabernet Sauvignon», а «Breg» отдельным домом тоже числится.
    vina_doma = {}
    for stroka in (ZDES / "vina.jsonl").read_text(encoding="utf-8").splitlines():
        if not stroka.strip():
            continue
        v = json.loads(stroka)
        vina_doma.setdefault(st.klyuch_hozyaistva(v["hozyaistvo"]), set()).add(
            st.klyuch(st.latinicej(v["vino"])))

    def nazyvaet_vino(dom, vino):
        """Есть ли у этого дома вино, чьё имя начинается так."""
        k = st.klyuch(st.latinicej(vino))
        return any(x == k or x.startswith(k + "-")
                   for x in vina_doma.get(st.klyuch_hozyaistva(dom), ()))

    nashi_vina = {json.loads(x)["klyuch"] for x in
                  (ZDES / "vina.jsonl").read_text(encoding="utf-8").splitlines()
                  if x.strip()}

    vina, ne_razobrano = [], []
    for god, adres in SPISKI:
        stranica = vzjat(adres, "spisok-%d.html" % god)
        telo = TELO.search(stranica)
        telo = telo.group(1) if telo else stranica
        telo = re.sub(r"<script.*?</script>|<style.*?</style>", " ", telo, flags=re.S)
        pary = pary_goda(telo, god)
        vzyato = 0
        for levo, pravo in pary:
            # Какая половина — хозяйство, решает наш список домов,
            # а не порядок: у 2021 года он один, у 2023 обратный.
            # Сорт хозяйством не считается: у Decanter в поле
            # производителя завелись «Prokupac» и «Marselan», и без
            # этого «Prokupac / Virtus» выглядит парой двух хозяйств.
            levo_dom = (not st.sort_a_ne_dom(levo)
                        and st.klyuch_hozyaistva(levo) in nashi_doma)
            pravo_dom = (not st.sort_a_ne_dom(pravo)
                         and st.klyuch_hozyaistva(pravo) in nashi_doma)
            if levo_dom and pravo_dom:
                # Обе половины — дома. Решает наш же каталог: чьё вино
                # так называется, тот и хозяйство.
                levo_dom = nazyvaet_vino(levo, pravo)
                pravo_dom = nazyvaet_vino(pravo, levo)
            if levo_dom == pravo_dom:
                ne_razobrano.append({"god": god, "stroka": "%s / %s" % (levo, pravo),
                                     "pochemu": "хозяйством выглядят обе половины"
                                     if levo_dom else "хозяйством не выглядит ни одна"})
                continue
            dom, vino = (levo, pravo) if levo_dom else (pravo, levo)
            # Абзац под именем: там сорт, урожай, крепость и цена.
            mesto = telo.find(html.escape(vino[:20])) if vino else -1
            # Ключ считается тем же способом, что в наших таблицах, и
            # рядом стоит, нашлось ли такое вино у нас: список журнала
            # зовёт вина короче («Omnibus Lector» вместо «Omnibus Lector
            # Chardonnay»), и без этой пометки не видно, что сошлось.
            klyuch = st.klyuch_vina(dom, vino)
            zapis = {"god": god, "hozyaistvo": dom, "vino": vino,
                     "klyuch_vina": klyuch, "est_u_nas": klyuch in nashi_vina,
                     "stranica": adres}
            if mesto > 0:
                zapis.update(razobrat_pole(telo[mesto:mesto + 1200]))
            vina.append(zapis)
            vzyato += 1
        print("  %d: пар %2d, разобрано %2d" % (god, len(pary), vzyato))

    (ZDES / "winestyle-spiski.json").write_text(json.dumps({
        "chto_eto": "Годовые списки сербских вин журнала «Wine Style». "
                    "НЕ оценка качества: журнал прямо пишет, что это не "
                    "список лучших, а список вин, привлёкших внимание. "
                    "В дорожки рейтингов не заводится.",
        "istochnik": "winestyle.rs, рубрика «Виноскоп»",
        "sobrano": time.strftime("%Y-%m-%d"),
        "vin_est_u_nas": sum(1 for z in vina if z["est_u_nas"]),
        "vina": vina,
        "ne_razobrano": ne_razobrano,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d вин за %d года, не разобрано %d → winestyle-spiski.json"
          % (len(vina), len(SPISKI), len(ne_razobrano)))


if __name__ == "__main__":
    main()
