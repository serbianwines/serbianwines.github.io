# -*- coding: utf-8 -*-
"""AWC Vienna: сербские вина.

Австрийский конкурс, крупнейший из признанных OIV: около десяти тысяч вин
в год. База открыта и лежит отдельно от сайта конкурса — на
awc-online.awc-vienna.at; сайт `awc-vienna.at/en/results` отвечает 404,
и из-за этого источник был записан в закрытые.

Фильтра по стране у поиска нет. Первый обход шёл по категориям года, и это
оказалось почти впустую: разбивка по категориям отдаётся только для текущего
года, а для прошлых сервер возвращает общий список — полсотни-сотню лучших
вин года по баллу. Сербское вино туда не попадает почти никогда. Из-за этого
за двенадцать лет набралось пять записей, а за один текущий год — двадцать.

Обход идёт по свободному тексту. Поиск ищет по подстроке и не различает
диакритику: «Kovacevic» и «Kovačević» дают одно и то же, «ubi» находит Rubin.
Слова для поиска берутся из имён хозяйств — наших и регистра виноделов, — а
сверх того закидывается невод из сербских сортов, мест и фамильных окончаний:
он ловит хозяйства, которых нет ни в одном нашем списке. Так нашлись
Toplicki Vinogradi и Vinarija Lastar.

Год у поиска обязателен: без него сервер отвечает 500.

Обход по категориям оставлен: ответы уже в кеше, лишних запросов он не
делает, а текущий год отдаёт полностью. Оба обхода сливаются по номеру вина.

У AWC есть и балл (с десятой долей, «88,9»), и медаль, поэтому строка
даёт и оценку, и награду. Публикуются только вина от 84 баллов.

    python3 _rabota/rejtingi/vzjat-awc.py

Пишет `awc-zapisi.json`, ответы кладёт в `kesh-awc/`.
"""
import json, os, re, html, time, threading, unicodedata
import urllib.error, urllib.parse, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-awc")
POISK = "https://awc-online.awc-vienna.at/search/wine"
ITOG = POISK + "/result?"
STRANA = "Serbia"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NITEJ = 3          # в три потока: около трёх с половиной запросов в секунду
ZHDAT = 0.4

# Слова, которые в имени хозяйства не значат ничего: по ним искать бессмысленно.
OBSHCHIE = set("""vinarija vinarije podrum podrumi winery wine wines vino vina
vinogradi vinograd vineyard vineyards doo ltd estate cellar cellars kuca kuca
vinska vinski chateau family porodicna srbija serbia the and of de distillery
group company farm agro vinarstvo weingut vinarium imanje salas manastir
preduzetnik proizvodnja proizvodna radnja privredno drustvo trgovinu veliko
vocem povrcem promet usluge pravno lice vinogradarstvo rakije rakija saveti
export import poljoprivredno gazdinstvo ogranak sa ogranicenom odgovornoscu"""
                .split())

# Невод: сорта, места и фамильные окончания. Ловит хозяйства, которых нет
# ни у нас, ни в регистре, — например тех, кто участвовал и закрылся.
NEVOD = """prokupac tamjanika vranac krstac smederevka morava probus bagrina
grasac dinka slankamenka kadarka portugizer sedusa zacinak plovdina ruzica
negotin fruska vrsac subotic sremski banat sumadija zupa oplenac palic srem
knjazevac aleksandrovac topli ovic evic ijic njic adic anic inic uric""".split()


def ascii_(stroka):
    """Диакритику поиск не различает — снимаем её и мы, чтобы не плодить слова."""
    razobrano = unicodedata.normalize("NFD", stroka)
    bez = "".join(z for z in razobrano if unicodedata.category(z) != "Mn")
    return bez.replace("đ", "dj").replace("Đ", "Dj").replace("ł", "l")


def slovo_dlya_poiska(imya):
    """Самое длинное собственное слово имени: по нему и ищем."""
    slova = [s for s in re.split(r"[^0-9A-Za-z]+", ascii_(imya)) if s]
    svoi = [s for s in slova if s.lower() not in OBSHCHIE and len(s) >= 4]
    if not svoi:
        svoi = [s for s in slova if len(s) >= 3] or slova
    return max(svoi, key=len).lower() if svoi else None


def slova_dlya_poiska():
    """Слова обхода: наши хозяйства, регистр, невод.

    Поиск идёт по подстроке, поэтому длинное слово лишнее, если внутри него
    уже сидит короткое из списка: «kis» найдёт и «kiseljak».
    """
    nashi, ostalnye = [], []
    put_hoz = put("hozyaistva.jsonl")
    if os.path.exists(put_hoz):
        for stroka in open(put_hoz, encoding="utf-8"):
            s = slovo_dlya_poiska(json.loads(stroka)["hozyaistvo"])
            if s:
                nashi.append(s)
    put_reg = put("vinarski-registar.json")
    if os.path.exists(put_reg):
        for z in json.load(open(put_reg, encoding="utf-8"))["zapisi"]:
            s = slovo_dlya_poiska(z["nazvanie"])
            if s:
                ostalnye.append(s)
    # Невод первым: он самый широкий, и с него выгоднее начинать сокращение.
    poryadok, vidano = [], set()
    for s in NEVOD + sorted(set(nashi), key=len) + sorted(set(ostalnye), key=len):
        if s in vidano:
            continue
        vidano.add(s)
        poryadok.append(s)
    nuzhnye = []
    for s in poryadok:
        if not any(k in s for k in nuzhnye):
            nuzhnye.append(s)
    return nuzhnye


zamok = threading.Lock()


def skachat(adres, imya):
    """Ответ сайта. Возвращает пусто, если сайт не отдал."""
    for popytka in range(5):
        try:
            zapros = urllib.request.Request(adres, headers={
                "User-Agent": BRAUZER, "Accept": "text/html",
                "Accept-Language": "en-US,en;q=0.9"})
            with urllib.request.urlopen(zapros, timeout=60) as otvet:
                tekst = otvet.read().decode("utf-8", "replace")
            time.sleep(ZHDAT)
            return tekst
        except Exception as beda:
            if popytka == 4:
                print("   не отдал:", imya, beda)
                return ""
            time.sleep(2 ** popytka)


def vyzhimka(stranica):
    """Из страницы — только то, что сборщику нужно.

    Каждый ответ AWC — это тридцать килобайт оболочки приложения ради
    полутора килобайт данных, а запросов почти семь тысяч. Целиком такой
    кеш весит двести мегабайт, и держать его в хранилище книги нельзя.
    Поэтому в кеш кладётся выжимка: счётчики выдачи, список категорий
    года — и сербские строки целиком, со всеми полями. Чужие строки
    отбрасываются: сборщик их всё равно отсеивает по стране.
    """
    svoi = svojstva(stranica)
    spisok = svoi.get("items") or {}
    vyzhato = {
        "total": spisok.get("total"),
        "last_page": spisok.get("last_page"),
        "serbskie": [z for z in (spisok.get("data") or [])
                     if (z.get("c_name_en") or "") == STRANA],
    }
    # Список категорий и годов приходит с каждым ответом, а нужен только
    # со страниц формы: в выдаче он занял бы три килобайта из четырёх.
    if not spisok:
        for pole in ("categories", "years"):
            if svoi.get(pole):
                vyzhato[pole] = svoi[pole]
    return vyzhato


def vzjat(adres, imya):
    """Выжимка ответа: из кеша, а если её там нет — с сайта."""
    fajl = os.path.join(KESH, imya + ".json")
    if os.path.exists(fajl):
        return json.load(open(fajl, encoding="utf-8"))
    # Кеш первого захода лежал целыми страницами. Читаем и его,
    # переписывая выжимкой: лишних запросов это не делает.
    staryj = os.path.join(KESH, imya + ".html")
    if os.path.exists(staryj):
        vyzhato = vyzhimka(open(staryj, encoding="utf-8").read())
        with zamok:
            json.dump(vyzhato, open(fajl, "w", encoding="utf-8"),
                      ensure_ascii=False)
            os.remove(staryj)
        return vyzhato
    vyzhato = vyzhimka(skachat(adres, imya))
    with zamok:
        os.makedirs(KESH, exist_ok=True)
        json.dump(vyzhato, open(fajl, "w", encoding="utf-8"),
                  ensure_ascii=False)
    return vyzhato


def svojstva(stranica):
    """Состояние страницы: приложение отдаёт его в атрибуте data-page."""
    sovpalo = re.search(r'data-page="([^"]+)"', stranica or "")
    if not sovpalo:
        return {}
    try:
        return json.loads(html.unescape(sovpalo.group(1))).get("props", {})
    except ValueError:
        return {}


def ball(stroka):
    """«88,9» → 88.9. Запятая у них десятичная, а не разделитель."""
    if not stroka:
        return None
    try:
        return float(str(stroka).replace(",", "."))
    except ValueError:
        return None


def zapis(z, god, otkuda):
    return {
        "god": god,
        "kategoriya": (z.get("w_k_name_en") or z.get("w_k_name") or "").strip()
                      or None,
        "nomer": z.get("w_id"),
        "hozyaistvo": (z.get("winery_company") or "").strip(),
        "vino": (z.get("w_bezeichnung") or "").strip(),
        # 9999 у них значит «без урожая».
        "urozhaj": (z.get("w_jahrgang")
                    if z.get("w_jahrgang") not in (None, 9999) else None),
        "ball": ball(z.get("w_ergebnis")),
        "medal": (z.get("medal") or "").strip() or None,
        # Поле приходит строкой «Y» или «N»: bool() тут пометил бы трофеем всё.
        "trofej": str(z.get("w_trophyWinner") or "").strip().upper() == "Y",
        "otkuda": otkuda,
        "stranica": "awc-online.awc-vienna.at/wine/%s" % z.get("w_id"),
    }


def vydacha(god, imya_fajla, **parametry):
    """Все страницы одной выдачи. Возвращает сербские строки и общий счёт."""
    nomer, vsego, nashlos = 1, None, []
    while True:
        adres = ITOG + urllib.parse.urlencode(
            dict(year=god, page=nomer, **parametry))
        vyzhato = vzjat(adres, "%s-%d" % (imya_fajla, nomer))
        vsego = vyzhato.get("total") if vsego is None else vsego
        nashlos += vyzhato.get("serbskie") or []
        if nomer >= (vyzhato.get("last_page") or 1):
            break
        nomer += 1
    return nashlos, (vsego or 0)


def obhod_kategorij(gody, nachalo):
    """Первый обход, по категориям. Оставлен ради текущего года и кеша."""
    vse, po_godam, obrezano = [], {}, []
    for god in gody:
        svoi = vzjat(POISK + "?year=%d" % god, "poisk-%d" % god)
        kategorii = svoi.get("categories") or nachalo.get("categories") or {}
        za_god = []
        for kod, imya_kategorii in kategorii.items():
            nashlos, vsego = vydacha(god, "awc-%d-%s" % (god, kod),
                                     categoryId=kod)
            for z in nashlos:
                stroka = zapis(z, god, "kategoriya")
                stroka["kategoriya"] = stroka["kategoriya"] or imya_kategorii
                za_god.append(stroka)
            if vsego >= 100:
                obrezano.append({"god": god, "kategoriya": imya_kategorii})
            if kod == "0" and vsego:
                po_godam.setdefault("otdano_vsego", {})[god] = vsego
        po_godam[god] = len(za_god)
        print("  категории %d: %d сербских строк" % (god, len(za_god)))
        vse += za_god
    return vse, po_godam, obrezano


def obhod_teksta(gody, slova):
    """Второй обход, по свободному тексту. Он и даёт основную добычу."""
    vse, obrezano = [], []
    zadaniya = [(god, s) for god in gody for s in slova]
    sdelano = [0]

    def rabotnik(dolya):
        for nomer in range(dolya, len(zadaniya), NITEJ):
            god, slovo = zadaniya[nomer]
            imya = "tekst-%d-%s" % (god, re.sub(r"[^a-z0-9]+", "_", slovo))
            nashlos, vsego = vydacha(god, imya, categoryId=0, text=slovo)
            with zamok:
                vse.extend(zapis(z, god, "tekst:" + slovo) for z in nashlos)
                if vsego >= 100:
                    obrezano.append({"god": god, "slovo": slovo, "vsego": vsego})
                sdelano[0] += 1
                if sdelano[0] % 200 == 0:
                    print("   ...%d из %d запросов, сербских строк %d"
                          % (sdelano[0], len(zadaniya), len(vse)))

    niti = [threading.Thread(target=rabotnik, args=(i,)) for i in range(NITEJ)]
    for n in niti:
        n.start()
    for n in niti:
        n.join()
    return vse, obrezano


def main():
    nachalo = vzjat(POISK, "poisk")
    gody = [g["year"] for g in nachalo.get("years", [])]
    print("годы:", gody)
    slova = slova_dlya_poiska()
    print("слов для поиска: %d, запросов будет около %d"
          % (len(slova), len(slova) * len(gody)))

    po_kategoriyam, po_godam, obrezano = obhod_kategorij(gody, nachalo)
    po_tekstu, obrezano_tekst = obhod_teksta(gody, slova)
    print("категории дали %d строк, текст — %d"
          % (len(po_kategoriyam), len(po_tekstu)))

    # Одно вино попадает и в свою категорию, и в общий список, и в несколько
    # текстовых запросов сразу.
    vidano, bez_povtorov = set(), []
    for z in po_kategoriyam + po_tekstu:
        if z["nomer"] in vidano:
            continue
        vidano.add(z["nomer"])
        bez_povtorov.append(z)

    # У AWC две дегустации в году, зимняя и летняя, и одно вино может
    # пройти обе — тогда номера разные, а вино то же и балл другой.
    # Оставляем один, больший, а расхождение записываем.
    po_klyuchu, poryadok, raznoglasiya = {}, [], []
    for z in bez_povtorov:
        # Ключ без диакритики: у AWC одно и то же вино на двух дегустациях
        # года пишется то «Komsinice», то «Komšinice», и с диакритикой
        # в ключе обе записи оставались, а балл у них разный.
        klyuch = (ascii_(z["hozyaistvo"]).lower(), ascii_(z["vino"]).lower(),
                  z["urozhaj"], z["god"])
        bylo = po_klyuchu.get(klyuch)
        if bylo is None:
            po_klyuchu[klyuch] = z
            poryadok.append(klyuch)
            continue
        if bylo["ball"] != z["ball"]:
            raznoglasiya.append({
                "god": z["god"], "hozyaistvo": z["hozyaistvo"], "vino": z["vino"],
                "urozhaj": z["urozhaj"],
                "bally": sorted({bylo["ball"], z["ball"]}),
                "vzyato": max(bylo["ball"], z["ball"])})
        if (z["ball"] or 0) > (bylo["ball"] or 0):
            po_klyuchu[klyuch] = z
    itog = [po_klyuchu[k] for k in poryadok]

    fakt = {}
    for z in itog:
        fakt[z["god"]] = fakt.get(z["god"], 0) + 1

    json.dump({
        "chto_eto": "Сербские вина AWC Vienna. У конкурса есть и балл, и медаль.",
        "istochnik": POISK,
        "kak_sobrano": "Фильтра по стране нет. Обход идёт по свободному тексту: "
                       "имена хозяйств из наших списков и регистра плюс невод из "
                       "сербских сортов, мест и фамильных окончаний. Поиск ищет "
                       "по подстроке и не различает диакритику. Обход по "
                       "категориям оставлен ради текущего года.",
        "slov_poiska": len(slova),
        "obrezannyh_kategorij": len(obrezano),
        "obrezannyh_zaprosov_teksta": obrezano_tekst,
        "raznoglasiya": raznoglasiya,
        "po_godam": {**po_godam, "najdeno": fakt},
        "vsego": len(itog),
        "zapisi": itog,
    }, open(put("awc-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего сербских вин: %d → awc-zapisi.json" % len(itog))
    print("по годам:", " ".join("%s:%d" % (g, fakt[g]) for g in sorted(fakt)))


if __name__ == "__main__":
    main()
