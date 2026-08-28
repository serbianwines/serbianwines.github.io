#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собрать из сырых выписок три нормализованные таблицы.

Сырьё — `vivino-zapisi.jsonl` и `vivino-syrye.json` (сплошной сбор по API,
если он сделан; при совпадении он старше), `kritiki-zapisi.jsonl`,
`nagrady-zapisi.jsonl`, `raion-hozyaistv.json`,
`falstaff-zvezdy.json`, `celi-spisok.json`. Всё это писалось по ходу сбора и
для анализа неудобно: идентификатор вина спрятан внутри строки-примечания,
две дорожки лежат порознь, шкалы разные.

На выходе — три таблицы в JSONL и CSV:

    hozyaistva.*   хозяйства: район, звёзды, есть ли в книге
    vina.*         вина: ключ, идентификатор Vivino, адрес
    ocenki.*       оценки в длинном виде: строка на измерение
    nagrady.*      награды и места в категориях: у них нет шкалы

Длинный вид у оценок выбран нарочно. Оценка Vivino и балл Falstaff — разные
величины в разных шкалах, и складывать их нельзя. Зато в длинной таблице
они спокойно лежат рядом: у каждой строки написано, чья шкала, каков балл
и на какой выборке он держится. Свести их в широкий вид — одна сводная
таблица; обратно из широкого вида в длинный уже не разложишь.

    python3 _rabota/rejtingi/sobrat-tablicy.py
"""

import csv
import json
import os
import sys
import re
import unicodedata

# На русской Windows консоль по умолчанию не UTF-8, и первая же кириллица
# в выводе роняет скрипт с UnicodeEncodeError. Просим UTF-8 явно.
for _potok in (sys.stdout, sys.stderr, sys.stdin):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
SOBRANO = "2026-08-28"


# Районы Vivino → главы книги. Взяты только однозначные: «Central Serbia»
# и «Wine of Serbia» у них свалка на полторы тысячи вин, по ним судить нельзя.
# «Šumadija-Great Morava» — официальный крупный регион, он покрывает и
# Шумадию, и часть Поморавья, поэтому тоже не годится.
RAION_PO_VIVINO = {
    "Srem": "fruska",
    "Fruška Gora": "fruska",
    "Subotica-Horgos": "subotica",
    "Banat": "banat",
    "Tri Morave": "morave",
    "Negotinska Krajina": "negotin",
    "Toplica": "toplica",
    "Knjaževac": "jugoistok",
    "Niš": "jugoistok",
    "Nisava-South Morava": "jugoistok",
    "Leskovac": "jugoistok",
    "Vranje": "jugoistok",
    "Pirot": "jugoistok",
}


def put(imya):
    return os.path.join(RYADOM, imya)


def chitat_jsonl(imya):
    if not os.path.exists(put(imya)):
        return []
    return [json.loads(s) for s in open(put(imya), encoding="utf-8") if s.strip()]


def vivino_iz_api():
    """Сплошной сбор по API, если он уже сделан.

    `sobrat-rejtingi.py` складывает результат в `vivino-syrye.json`. Эти
    данные точнее ручных выписок: там оценка и число отзывов приходят
    полями, а не пересказом выдачи. Поэтому при совпадении они старше.
    """
    if not os.path.exists(put("vivino-syrye.json")):
        return []
    d = json.load(open(put("vivino-syrye.json"), encoding="utf-8"))
    iz_api = []
    for z in d.get("vina", []):
        if not z.get("hozyaistvo") or not z.get("vino"):
            continue
        iz_api.append({
            "hozyaistvo": z["hozyaistvo"],
            "vino": z["vino"],
            "ocenka": z.get("ocenka"),
            "chislo_ocenok": z.get("chislo_ocenok"),
            "stranica": ("w/%s" % z["id_vina"]) if z.get("id_vina") else "",
            "id_vina": z.get("id_vina"),
            "iz_api": True,
        })
    return iz_api


def svesti_vivino(ruchnoe, iz_api):
    """Слить ручные выписки и сбор по API. При совпадении API старше.

    Ручное не выбрасывается: в нём могут оказаться вина, которых сплошной
    обход не вернул (снятые с продажи, переименованные). Но там, где есть
    и то и другое, берётся API.
    """
    def klyuch_zapisi(z):
        """Одно вино надёжнее всего опознаётся по идентификатору Vivino.

        Имя ненадёжно: одно и то же вино у меня записано как
        «Zupa Aleksandrovac · Srpski Vranac», а у API — как
        «Zupa · Aleksandrovac Srpski Vranac». Идентификатор один.
        """
        vivino_id, _, _ = razobrat_stranicu(z.get("stranica"))
        if z.get("id_vina"):
            return ("id", z["id_vina"])
        if vivino_id:
            return ("id", vivino_id)
        return ("imya", klyuch_hozyaistva(z["hozyaistvo"]), klyuch(z["vino"]))

    svedeno = {}
    for z in ruchnoe:
        svedeno[klyuch_zapisi(z)] = z
    poverh_ruchnyh = 0
    for z in iz_api:
        k = klyuch_zapisi(z)
        if k in svedeno:
            poverh_ruchnyh += 1
        svedeno[k] = z

    # Второй проход, по имени. Идентификатор разводит записи, у которых
    # имя разбито по-разному, а ключ вина в таблицах всё равно строится
    # из имени — иначе оценку критика не с чем было бы связать. Поэтому
    # то, что сходится по имени, тоже сводим: старше запись из API.
    po_imeni = {}
    for z in svedeno.values():
        k = (klyuch_hozyaistva(z["hozyaistvo"]), klyuch(z["vino"]))
        if k in po_imeni and not z.get("iz_api"):
            continue
        po_imeni[k] = z
    svedeno = po_imeni

    if iz_api:
        print("Vivino: ручных %d, из API %d, из них поверх ручных %d"
              % (len(ruchnoe), len(iz_api), poverh_ruchnyh))
    return list(svedeno.values())


# Одно и то же хозяйство зовётся по-разному: в книге «Deurić», у Vivino
# «Vinarija Deurić», у Decanter «Vinarija Deuric». Слова «винария»,
# «подрум», «виногради» в имени ничего не различают — при сведении их
# отбрасываем, а для показа берём то имя, которое встретилось первым.
# Слова, которые в имени хозяйства ничего не различают: род занятий
# («винарија», «подрум»), форма собственности («д.о.о.», «пр») и
# английские кальки. «Vino Budimir» и «Budimir», «Krstašica Doo» и
# «Krstašica», «Podrum Vina Žarković» и «Žarković» — одни и те же дома.
SLUZHEBNYE = ("vinarija", "vinarija-", "podrum", "podrumi", "vinogradi",
              "vinska-kuca", "vinarska-kuca", "gazdinstvo", "winery",
              "vinarija-vinarija", "estate", "manastir", "monastery",
              "vino", "vina", "doo", "pr", "vinery", "vineyards",
              "wine", "wines")


# Имена, сведённые руками и с доказательством, — `sinonimy-hozyaistv.json`.
# Похожесть имён доказательством не считается: Jovanović и Jovanov,
# Madžić и Adžić, Stojković и Stojanović — разные хозяйства.
def _sinonimy():
    """Варианты имени → каноническое. Сводится по ключу, а не по строке.

    По строке не годится: у источников есть и «Šapat», и «Sapat» без
    диакритики, и перечислять оба в списке синонимов — заведомо не
    перечислить все. Ключ их и так уравнивает, поэтому свожу ключи.
    """
    put_f = os.path.join(RYADOM, "sinonimy-hozyaistv.json")
    if not os.path.exists(put_f):
        return {}
    d = json.load(open(put_f, encoding="utf-8"))["hozyaistva"]
    return {_bazovyj_klyuch(v): _bazovyj_klyuch(imya)
            for imya, z in d.items() for v in z["varianty"]}


def bez_skobok(imya):
    """«Винарија Тришић (Vinarija Trišić)» — это «Vinarija Trišić».

    Часть сербских хозяйств Vivino держит кириллицей, дописывая латинскую
    расшифровку в скобках, а Decanter и Falstaff знают только латинское
    имя. Без этого одно хозяйство стоит в таблице дважды, и рејон
    достаётся только латинской записи.

    Скобки берутся, только если внутри латиница: у «Aglaya (Аглая)»
    и «Vinarija Novak (Новак)» в скобках, наоборот, кириллица, и там
    основное имя как раз перед скобками.
    """
    sovpalo = re.search(r"^(.+?)\s*\(([^()]+)\)\s*$", imya)
    if not sovpalo:
        # То же самое, но через тире: «Орлић Породична Винарија -
        # Orlić Family Winery», «Трилогия Винария - Vinarija Trilogija».
        sovpalo = re.search(r"^(.+?)\s+[-–]\s+(.+?)\s*$", imya)
    if not sovpalo:
        return imya
    levo, pravo = sovpalo.group(1), sovpalo.group(2)
    kirillica = lambda s: any("\u0400" <= z <= "\u04ff" for z in s)
    if kirillica(pravo) and not kirillica(levo):
        return levo
    if kirillica(levo) and not kirillica(pravo):
        return pravo
    return imya


def _bazovyj_klyuch(imya):
    k = klyuch(bez_skobok(imya))
    chasti = [c for c in k.split("-") if c and c not in SLUZHEBNYE]
    return "-".join(chasti) or k


SINONIMY = {}
# Имена, объявленные в файле синонимов главными: они и показываются.
KANON_IMYA = set()


def klyuch_hozyaistva(imya):
    """Ключ хозяйства: без служебных слов, регистра и диакритики."""
    k = _bazovyj_klyuch(imya)
    return SINONIMY.get(k, k)


def klyuch_vina(hozyaistvo, vino, snimat_povtor=True):
    """Ключ вина: хозяйство плюс имя, без повтора хозяйства в имени.

    Falstaff печатает имя хозяйства внутри названия вина — «Zvonko Bogdan
    Cuvée No 1», «Manastir Bukovo Filigran Gamay», — а Decanter и Vivino
    зовут те же вина «Cuvée No.1» и «Filigran Gamay». Без снятия повтора
    одно вино попадает в таблицу дважды и в отчёте стоит двумя строками.

    Для записей Vivino повтор не снимается: у них есть собственный
    идентификатор, и он говорит, что «Tarpos Merlot» и «Merlot» у Tarpoš —
    две разные позиции каталога. Свести их по имени значило бы решить за
    Vivino, что это одно вино, и потерять одну из двух выборок отзывов.
    """
    hoz = klyuch_hozyaistva(hozyaistvo)
    chasti = klyuch(vino).split("-")
    if snimat_povtor:
        for skolko in range(len(chasti) - 1, 0, -1):
            nachalo = [c for c in chasti[:skolko] if c not in SLUZHEBNYE]
            if "-".join(nachalo) == hoz:
                chasti = chasti[skolko:]
                break
    return hoz + "-" + "-".join(chasti)


def imya_vina(hozyaistvo, vino, snimat_povtor=True):
    """Имя вина для таблиц — без имени хозяйства в начале.

    Ключ повтор уже снимает; здесь то же самое делается с показываемым
    именем, иначе в отчёте стоит «Zvonko Bogdan · Zvonko Bogdan Cuvée
    No 1». В сырых записях имя остаётся ровно таким, как его печатает
    источник, — таблицы производные, сырьё правится только руками.
    """
    if not snimat_povtor:
        return vino
    slova = vino.split()
    hoz = klyuch_hozyaistva(hozyaistvo)
    for skolko in range(len(slova) - 1, 0, -1):
        if klyuch_hozyaistva(" ".join(slova[:skolko])) == hoz:
            return " ".join(slova[skolko:])
    return vino


def klyuch(*chasti):
    """Устойчивый ключ: без регистра, диакритики и лишних пробелов."""
    s = " ".join(c for c in chasti if c).lower()
    # «dj» — тот же «đ», записанный без диакритики: Decanter пишет
    # «Mrdjanin», «Djurdjic», «Medje» там, где у Vivino стоит «Mrđanin»,
    # «Đurđić», «Međe». Без этого одно хозяйство разъезжается на два.
    s = s.replace("dj", "đ")
    s = s.replace("š", "s").replace("đ", "d").replace("č", "c")
    s = s.replace("ć", "c").replace("ž", "z")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    # Апостроф и точка внутри слова разделителями не работают: «King's
    # Crown» и «Kings Crown», «Cuvée No.1» и «Cuvee No1» — одно вино,
    # записанное разными руками. Пробел и дефис разделителями остаются,
    # иначе «Cabernet-Merlot» разошлось бы с «Cabernet Merlot».
    s = re.sub(r"[.'\u2019]", "", s)
    s = re.sub(r"[^a-z0-9а-я]+", "-", s)
    return s.strip("-")


def chislo_ili_nichego(znachenie):
    """Ноль у Vivino значит «нечего показать», а не «оценка ноль».

    Отдаётся он и в поле оценки, и в поле числа отзывов, и если принять
    его за значение, в таблицу попадут полторы тысячи вин с баллом 0.
    """
    if isinstance(znachenie, (int, float)) and znachenie > 0:
        return znachenie
    return None


def razobrat_stranicu(stranica):
    """Из строки-примечания вынуть идентификатор вина, адрес и оговорку.

    Писалось это руками и по-разному: «w/5027454», «wineries/erdevik»,
    «w/2115277 · профиль вкуса, нижняя граница». Разбирается здесь один раз,
    чтобы дальше в таблицах лежали чистые поля.
    """
    stranica = stranica or ""
    ogovorka = ""
    if "·" in stranica:
        stranica, ogovorka = [c.strip() for c in stranica.split("·", 1)]
    sovpalo = re.search(r"\bw/(\d+)\b", stranica)
    vivino_id = int(sovpalo.group(1)) if sovpalo else None
    adres = ""
    if stranica:
        adres = "https://www.vivino.com/" + stranica.lstrip("/")
    return vivino_id, adres, ogovorka


def nizhnyaya_granica(ogovorka):
    """Число отзывов, взятое из профиля вкуса или из отдельного урожая, —
    это не всё число оценок, а его нижняя оценка. Отмечаем явно."""
    return bool(re.search(r"нижняя граница|профиль вкуса", ogovorka or ""))


def main():
    vivino = svesti_vivino(chitat_jsonl("vivino-zapisi.jsonl"), vivino_iz_api())
    kritiki = chitat_jsonl("kritiki-zapisi.jsonl")
    nagrady_syrye = chitat_jsonl("nagrady-zapisi.jsonl")
    karta = json.load(open(put("raion-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]
    zvezdy = {klyuch_hozyaistva(z["hozyaistvo"]): z for z in
              json.load(open(put("falstaff-zvezdy.json"), encoding="utf-8"))["hozyaistva"]}

    celi = json.load(open(put("celi-spisok.json"), encoding="utf-8"))

    # Что названо в книге: хозяйства и отдельные бутылки.
    hoz_v_knige, vina_v_knige = set(), set()
    for razdel in celi["regiony"]:
        for h in razdel["hozyaistva"]:
            hoz_v_knige.add(klyuch(h["hozyaistvo"].replace("◈", "")))
        for v in razdel["vina_v_tekste"]:
            vina_v_knige.add(klyuch(v))

    def v_knige_hoz(imya):
        k = klyuch(imya)
        return any(k in kn or kn in k for kn in hoz_v_knige if kn)

    def v_knige_vino(imya):
        k = klyuch(imya)
        return any(k == kn or kn in k for kn in vina_v_knige if kn)

    # ---------------- хозяйства ----------------
    # Одно хозяйство приходит под разными именами: «Deurić», «Vinarija
    # Deurić», «Vinarija Deuric». Сводим по ключу, а показываем то имя,
    # которое знает книга; если книга его не знает — самое длинное,
    # оно обычно полнее.
    imena_knigi = {klyuch_hozyaistva(k) for k in karta}
    karta_po_klyuchu = {klyuch_hozyaistva(k): v for k, v in karta.items()}
    varianty = {}
    for z in vivino + kritiki + nagrady_syrye:
        k = klyuch_hozyaistva(z["hozyaistvo"])
        varianty.setdefault(k, set()).add(z["hozyaistvo"])
    imena = []
    for k, nabor in varianty.items():
        knizhnye = [i for i in nabor if klyuch_hozyaistva(i) in imena_knigi
                    and i in karta]
        # Ровно равные по длине варианты («Todorović» и «Todorovic»)
        # иначе выбирались как попало — от запуска к запуску имя в
        # таблицах менялось. Порядок задан явно: длиннее, с диакритикой,
        # затем по алфавиту.
        # Имя, названное в `sinonimy-hozyaistv.json`, старше длины: там
        # оно выбрано с доказательством. Иначе побеждала бы опечатка —
        # «Vista Hills Plus» длиннее, чем «Vista Hill».
        svedennoe = [i for i in nabor if i in KANON_IMYA]
        imena.append(knizhnye[0] if knizhnye else
                     svedennoe[0] if svedennoe else
                     sorted(nabor, key=lambda i: (-len(i),
                                                  -sum(z > "\x7f" for z in i),
                                                  i))[0])
    # Канонические имена выбраны; теперь всюду пишем именно их, иначе
    # в таблице вин хозяйство будет зваться иначе, чем в таблице хозяйств.
    kanon = {}
    for imya in imena:
        for variant in varianty[klyuch_hozyaistva(imya)]:
            kanon[variant] = imya

    def imya_hozyaistva(syroe):
        return kanon.get(syroe, syroe)

    for spisok in (vivino, kritiki, nagrady_syrye):
        for z in spisok:
            z["hozyaistvo"] = imya_hozyaistva(z["hozyaistvo"])

    nastoyashchee_mesto = {}
    if os.path.exists(put("rejony-hozyaistv.json")):
        nastoyashchee_mesto = json.load(
            open(put("rejony-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]

    hozyaistva = []
    for imya in sorted(imena):
        svedeniya = dict(karta_po_klyuchu.get(klyuch_hozyaistva(imya), {}))
        if not svedeniya.get("raion"):
            # Района в книге нет — попробуем по району Vivino, но только
            # если все его сербские вина указывают на одну главу.
            predlozheno = {RAION_PO_VIVINO.get(z.get("region_vivino"))
                           for z in vivino
                           if klyuch_hozyaistva(z["hozyaistvo"])
                           == klyuch_hozyaistva(imya)}
            predlozheno.discard(None)
            if len(predlozheno) == 1:
                svedeniya["raion"] = predlozheno.pop()
                svedeniya["istochnik"] = "vivino"
        slugi = {razobrat_stranicu(z.get("stranica"))[1] for z in vivino
                 if z["hozyaistvo"] == imya}
        slug = ""
        for adres in slugi:
            sovpalo = re.search(r"/wineries/([a-z0-9-]+)", adres or "")
            if sovpalo:
                slug = sovpalo.group(1)
                break
        # Настоящее место — рејон и виногорје по действующей рејонизацији.
        # Считает `sobrat-rejony.py`; здесь только подставляется. Глава
        # книги (`raion_knigi`) остаётся рядом отдельной величиной: она
        # не обязана совпадать с рејоном, и автор её ещё может менять.
        mesto = nastoyashchee_mesto.get(klyuch_hozyaistva(imya), {})
        hozyaistva.append({
            "hozyaistvo": imya,
            "klyuch": klyuch_hozyaistva(imya),
            "region": mesto.get("region"),
            "rejon": mesto.get("rejon"),
            "vinogorje": mesto.get("vinogorje"),
            "rejon_istochnik": mesto.get("istochnik", "ne_ustanovlen"),
            "rejon_raznoglasie": mesto.get("raznoglasie", ""),
            "raion_knigi": svedeniya.get("raion"),
            "raion_istochnik": svedeniya.get("istochnik", "ne_ustanovlen"),
            "gde": svedeniya.get("gde", "") or mesto.get("gde", ""),
            "v_knige": v_knige_hoz(imya),
            "vivino_slug": slug,
            "falstaff_zvezd": zvezdy.get(klyuch_hozyaistva(imya), {}).get("zvezd"),
            "vin_v_dannyh": sum(1 for z in vivino
                                if klyuch_hozyaistva(z["hozyaistvo"])
                                == klyuch_hozyaistva(imya)),
        })

    # ---------------- вина ----------------
    vina, vidano = [], {}
    for z in vivino:
        k = klyuch_vina(z["hozyaistvo"], z["vino"], snimat_povtor=False)
        vivino_id, adres, _ = razobrat_stranicu(z.get("stranica"))
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": z["vino"],
                "vivino_id": vivino_id,
                "vivino_adres": adres if vivino_id else "",
                # «Мало оценок» — тоже сведение: Vivino прячет оценку, пока
                # отзывов слишком мало. Пустое поле и такой ответ — разное.
                "vivino_status": ("ocenka_est"
                                  if chislo_ili_nichego(z.get("ocenka"))
                                  else "malo_ocenok"),
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
        elif vivino_id and not vidano[k]["vivino_id"]:
            vidano[k]["vivino_id"] = vivino_id
            vidano[k]["vivino_adres"] = adres
    for z in nagrady_syrye:
        if not z["vino"]:
            continue          # награда хозяйству, а не вину
        k = klyuch_vina(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": imya_vina(z["hozyaistvo"], z["vino"]),
                "vivino_id": None,
                "vivino_adres": "",
                "vivino_status": "net_na_vivino",
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
    for z in kritiki:
        k = klyuch_vina(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": imya_vina(z["hozyaistvo"], z["vino"]),
                "vivino_id": None,
                "vivino_adres": "",
                "vivino_status": "net_na_vivino",
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": True,
            }
        else:
            vidano[k]["est_u_kritikov"] = True
    vina = sorted(vidano.values(), key=lambda z: (z["hozyaistvo"], z["vino"]))

    # ---------------- оценки, длинный вид ----------------
    ocenki = []
    for z in vivino:
        if chislo_ili_nichego(z.get("ocenka")) is None:
            continue
        _, adres, ogovorka = razobrat_stranicu(z.get("stranica"))
        ocenki.append({
            "klyuch_vina": klyuch_vina(z["hozyaistvo"], z["vino"],
                                       snimat_povtor=False),
            "hozyaistvo": z["hozyaistvo"],
            "vino": z["vino"],
            "istochnik": "vivino",
            "shkala": 5,
            "ball": z["ocenka"],
            "vyborka": chislo_ili_nichego(z.get("chislo_ocenok")),
            "vyborka_nizhnyaya_granica": nizhnyaya_granica(ogovorka),
            "god": None,
            "konkurs_god": None,
            "ogovorka": ogovorka,
            "stranica": adres,
            "sobrano": SOBRANO,
        })
    for z in kritiki:
        if z.get("ball") is None:
            continue
        ocenki.append({
            "klyuch_vina": klyuch_vina(z["hozyaistvo"], z["vino"]),
            "hozyaistvo": z["hozyaistvo"],
            "vino": imya_vina(z["hozyaistvo"], z["vino"]),
            "istochnik": z["istochnik"],
            "shkala": 100,
            "ball": z["ball"],
            "vyborka": None,
            "vyborka_nizhnyaya_granica": False,
            "god": int(z["god"]) if z.get("god") else None,
            "konkurs_god": z.get("konkurs_god"),
            "ogovorka": "",
            "stranica": z.get("stranica", ""),
            "sobrano": SOBRANO,
        })

    # ---------------- награды ----------------
    nagrady = [{
        "klyuch_vina": (klyuch_vina(z["hozyaistvo"], z["vino"])
                        if z["vino"] else ""),
        "hozyaistvo": z["hozyaistvo"],
        "vino": imya_vina(z["hozyaistvo"], z["vino"]),
        "istochnik": z["istochnik"],
        "god": z["god"],
        "kategoriya": z["kategoriya"],
        "mesto": z["mesto"],
        "urozhaj": z["urozhaj"],
        "stranica": z["stranica"],
        "sobrano": SOBRANO,
    } for z in nagrady_syrye]

    for imya, tablica in (("hozyaistva", hozyaistva), ("vina", vina),
                          ("ocenki", ocenki), ("nagrady", nagrady)):
        with open(put(imya + ".jsonl"), "w", encoding="utf-8") as f:
            for s in tablica:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        with open(put(imya + ".csv"), "w", encoding="utf-8", newline="") as f:
            pero = csv.DictWriter(f, fieldnames=list(tablica[0].keys()))
            pero.writeheader()
            pero.writerows(tablica)
        print("%-12s %4d строк → %s.jsonl, %s.csv" % (imya, len(tablica), imya, imya))


SINONIMY.update(_sinonimy())
KANON_IMYA.update(
    json.load(open(os.path.join(RYADOM, "sinonimy-hozyaistv.json"),
                   encoding="utf-8"))["hozyaistva"]
    if os.path.exists(os.path.join(RYADOM, "sinonimy-hozyaistv.json")) else {})


if __name__ == "__main__":
    main()
