#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сбор рейтингов Vivino по хозяйствам из книги «Терруары Сербии».

Скрипт только читает и складывает данные в свой каталог. Книгу он не трогает
и не должен научиться её трогать: правки в index.html вносятся руками.

Зачем. У вина на Vivino есть две величины — средняя оценка и число оценок.
Порознь они бесполезны: 4,8 по трём отзывам не значит ничего, 3,4 по тысяче
значит много. Скрипт берёт обе и сводит их в одно число, по которому вина
внутри региона можно выстроить (как — сказано ниже, в «Правиле отбора»).

    # 1. перечень целей — что вообще искать (делается по книге)
    python3 _rabota/rejtingi/sobrat-celi.py index.html > _rabota/rejtingi/celi-spisok.json

    # 2. сбор (нужен доступ к vivino.com, см. README.md)
    python3 _rabota/rejtingi/sobrat-rejtingi.py

    # 3. пересчёт из уже собранного, без сети
    python3 _rabota/rejtingi/sobrat-rejtingi.py --tolko-schitat

Итог — два файла рядом со скриптом:
    vivino-syrye.json   всё, что отдал сайт, как отдал
    vivino-itog.json    по регионам книги, отсортировано по правилу отбора

Сеть. Из среды, где книга собиралась в августе 2026-го, vivino.com закрыт
политикой исходящего трафика, поэтому скрипт писался «вслепую» и на живом
сайте не проверялся. Первый запуск — на машине автора; если разметка ответа
разошлась, править надо разбор в `razobrat_vino`, остальное от него не зависит.
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

RYADOM = os.path.dirname(os.path.abspath(__file__))
CELI = os.path.join(RYADOM, "celi-spisok.json")
SYRYE = os.path.join(RYADOM, "vivino-syrye.json")
ITOG = os.path.join(RYADOM, "vivino-itog.json")

API = "https://www.vivino.com/api/explore/explore"
STRANA = "RS"          # код Сербии в разметке Vivino
NA_STRANICE = 50       # сколько вин просить за один запрос

ZAGOLOVKI = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "application/json",
    "Accept-Language": "en,sr;q=0.8,ru;q=0.6",
}


# --------------------------------------------------------------------------
# правило отбора
# --------------------------------------------------------------------------
#
# Задача: не пустить в список вино, у которого высокая оценка держится на
# двух отзывах, и не выкинуть хорошее вино только за то, что его пили реже
# соседа. Обе крайности решаются одним приёмом — сдвигом к среднему.
#
#     итог = (n * ocenka + m * srednee) / (n + m)
#
# n — сколько оценок у вина, m — вес «недоверия». Пока оценок мало, итог
# тянется к средней по стране; чем их больше, тем меньше поправка значит.
# При n = m поправка ровно вполовину.
#
# Дополнительно — жёсткий порог MIN_OCENOK: ниже него вино в список не
# попадает вовсе, каким бы ни был пересчёт. Сама Vivino считает вино
# «популярным» от тысячи оценок, но для Сербии эта планка бессмысленна:
# тысячу набирают единицы, и по ней в списке не осталось бы никого.
#
# Оба числа подобраны по тому, что реально видно у сербских вин: у заметных
# бутылок 30–900 оценок, у большинства малых хозяйств — меньше тридцати.

MIN_OCENOK = 25    # меньше — вино не рассматривается
VES_NEDOVERIYA = 50
MAX_OT_HOZYAISTVA = 2   # сколько вин одного хозяйства пускать в пятёрку
V_SPISKE = 5


def sdvinutaya(ocenka, chislo, srednee):
    """Оценка, сдвинутая к средней тем сильнее, чем меньше отзывов."""
    return (chislo * ocenka + VES_NEDOVERIYA * srednee) / (chislo + VES_NEDOVERIYA)


# --------------------------------------------------------------------------
# сеть
# --------------------------------------------------------------------------

def zapros(adres, params):
    url = adres + "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers=ZAGOLOVKI)
    with urllib.request.urlopen(req, timeout=40) as otvet:
        return json.loads(otvet.read().decode("utf-8"))


def peredyshka():
    """Пауза между запросами. Сайт чужой, торопиться некуда."""
    time.sleep(1.5 + random.random())


def vse_vina_strany(predel_stranic=60):
    """Пройти постранично весь список сербских вин."""
    sobrano, stranica = [], 1
    while stranica <= predel_stranic:
        params = {
            "country_code": STRANA,
            "country_codes[]": STRANA.lower(),
            "currency_code": "RSD",
            "min_rating": 1,
            "order_by": "ratings_count",
            "order": "desc",
            "page": stranica,
            "per_page": NA_STRANICE,
        }
        try:
            otvet = zapros(API, params)
        except urllib.error.HTTPError as e:
            sys.stderr.write("страница %d: HTTP %s\n" % (stranica, e.code))
            break
        except Exception as e:                      # noqa: BLE001
            sys.stderr.write("страница %d: %s\n" % (stranica, e))
            break

        kusok = (otvet.get("explore_vintage") or {}).get("matches") or []
        if not kusok:
            break
        sobrano.extend(kusok)
        sys.stderr.write("страница %d: +%d, всего %d\n"
                         % (stranica, len(kusok), len(sobrano)))
        stranica += 1
        peredyshka()
    return sobrano


def razobrat_vino(zapis):
    """Вытащить из ответа то немногое, что нужно: имя, оценку, число оценок.

    Ответ Vivino вложенный и со временем меняется. Всё, что зависит от его
    устройства, собрано здесь — если сайт перестроит разметку, править нужно
    только эту функцию.
    """
    vintage = zapis.get("vintage") or {}
    vino = vintage.get("wine") or {}
    hozyaistvo = (vino.get("winery") or {}).get("name") or ""
    region = ((vino.get("region") or {}).get("name")) or ""

    # У Vivino две статистики: по конкретному урожаю и по вину вообще.
    # Для книги нужна вторая: она устойчивее и не устаревает со сменой года
    # на этикетке.
    st_vina = vino.get("statistics") or {}
    st_urozhaya = vintage.get("statistics") or {}

    def chislo(d, klyuch):
        v = d.get(klyuch)
        return v if isinstance(v, (int, float)) else None

    return {
        "id_vina": vino.get("id"),
        "id_urozhaya": vintage.get("id"),
        "hozyaistvo": hozyaistvo,
        "vino": vino.get("name") or "",
        "polnoe_imya": vintage.get("name") or "",
        "god": vintage.get("year"),
        "region_vivino": region,
        "ocenka": chislo(st_vina, "ratings_average") or chislo(st_urozhaya, "ratings_average"),
        "chislo_ocenok": chislo(st_vina, "ratings_count") or chislo(st_urozhaya, "ratings_count"),
        "ocenka_urozhaya": chislo(st_urozhaya, "ratings_average"),
        "chislo_ocenok_urozhaya": chislo(st_urozhaya, "ratings_count"),
        "adres": ("https://www.vivino.com/w/%s" % vino["id"]) if vino.get("id") else "",
    }


# --------------------------------------------------------------------------
# сведение с книгой
# --------------------------------------------------------------------------

def klyuch(s):
    """Имя хозяйства к сравнимому виду: без регистра, диакритики и слова «винарија»."""
    s = (s or "").lower()
    for a, b in (("š", "s"), ("đ", "d"), ("dž", "dz"), ("č", "c"), ("ć", "c"),
                 ("ž", "z"), ("ń", "n"), ("ö", "o"), ("ü", "u")):
        s = s.replace(a, b)
    for lishnee in ("vinarija", "vinarija -", "podrum", "winery", "vinogradi",
                    "vinska kuca", "estate"):
        s = s.replace(lishnee, " ")
    return " ".join(s.split())


def sovpalo(imya_knigi, imya_vivino):
    a, b = klyuch(imya_knigi), klyuch(imya_vivino)
    if not a or not b:
        return False
    return a == b or a in b or b in a


def po_regionam(vina, celi):
    """Разложить вина по регионам книги — по хозяйству, а не по региону Vivino.

    Районы Vivino с районами книги не совпадают: там своя сетка, и Жупа,
    например, растворена в «Tri Morave». Единственная надёжная привязка —
    хозяйство: где книга поместила винодельню, там её вина и учитываются.
    """
    razlozheno = {r["kod"]: [] for r in celi["regiony"]}
    bez_regiona = []
    for v in vina:
        kuda = None
        for region in celi["regiony"]:
            if region["kod"] == "vinarije":
                continue        # приложение, не район
            for h in region["hozyaistva"]:
                if sovpalo(h["hozyaistvo"], v["hozyaistvo"]):
                    kuda = region["kod"]
                    break
            if kuda:
                break
        (razlozheno[kuda] if kuda else bez_regiona).append(v)
    return razlozheno, bez_regiona


def pyaterka(vina_regiona, srednee):
    """Отобрать пятёрку: порог по числу отзывов, сдвиг к среднему, потолок на хозяйство."""
    godnye = [v for v in vina_regiona
              if v.get("ocenka") and (v.get("chislo_ocenok") or 0) >= MIN_OCENOK]
    for v in godnye:
        v["itogovaya"] = round(sdvinutaya(v["ocenka"], v["chislo_ocenok"], srednee), 3)
    godnye.sort(key=lambda v: v["itogovaya"], reverse=True)

    otobrano, skolko = [], {}
    for v in godnye:
        k = klyuch(v["hozyaistvo"])
        if skolko.get(k, 0) >= MAX_OT_HOZYAISTVA:
            continue
        skolko[k] = skolko.get(k, 0) + 1
        otobrano.append(v)
        if len(otobrano) == V_SPISKE:
            break
    return otobrano, len(godnye)


# --------------------------------------------------------------------------

def main():
    razbor = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    razbor.add_argument("--tolko-schitat", action="store_true",
                        help="не ходить в сеть, пересчитать из vivino-syrye.json")
    razbor.add_argument("--stranic", type=int, default=60,
                        help="сколько страниц выдачи пройти (по 50 вин)")
    dovody = razbor.parse_args()

    if not os.path.exists(CELI):
        sys.exit("нет %s — сначала запустите sobrat-celi.py" % CELI)
    celi = json.load(open(CELI, encoding="utf-8"))

    if dovody.tolko_schitat:
        if not os.path.exists(SYRYE):
            sys.exit("нет %s — сначала запустите сбор без --tolko-schitat" % SYRYE)
        vina = json.load(open(SYRYE, encoding="utf-8"))["vina"]
    else:
        syrye = vse_vina_strany(dovody.stranic)
        if not syrye:
            sys.exit("сайт не отдал ни одной страницы; см. README.md, раздел о доступе")
        vina = [razobrat_vino(z) for z in syrye]
        # Одно вино приходит несколькими урожаями — оставляем по одному на вино.
        po_id = {}
        for v in vina:
            if v["id_vina"] and v["id_vina"] not in po_id:
                po_id[v["id_vina"]] = v
        vina = list(po_id.values())
        json.dump({"sobrano": time.strftime("%Y-%m-%d"), "vina": vina},
                  open(SYRYE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        sys.stderr.write("записано %s: %d вин\n" % (SYRYE, len(vina)))

    # Средняя, к которой сдвигаются малоизвестные вина, считается только по
    # тем, кто сам прошёл порог. Иначе её тянут вниз сотни бутылок с двумя
    # отзывами, и поправка перестаёт означать «как обычно бывает в Сербии».
    opora = [v for v in vina
             if v.get("ocenka") and (v.get("chislo_ocenok") or 0) >= MIN_OCENOK]
    if not opora:
        sys.exit("в собранном нет ни одного вина с %d оценками — проверьте razobrat_vino"
                 % MIN_OCENOK)
    srednee = sum(v["ocenka"] for v in opora) / len(opora)

    razlozheno, bez_regiona = po_regionam(vina, celi)
    itog = {
        "sobrano": time.strftime("%Y-%m-%d"),
        "pravilo": {
            "min_ocenok": MIN_OCENOK,
            "ves_nedoveriya": VES_NEDOVERIYA,
            "max_ot_hozyaistva": MAX_OT_HOZYAISTVA,
            "srednyaya_po_vyborke": round(srednee, 3),
            "vsego_vin_v_vyborke": len(vina),
            "vin_proshlo_porog": len(opora),
        },
        "regiony": [],
        "hozyaistva_vne_knigi": sorted({v["hozyaistvo"] for v in bez_regiona}),
    }
    for region in celi["regiony"]:
        if region["kod"] == "vinarije":
            continue
        pyat, godnyh = pyaterka(razlozheno[region["kod"]], srednee)
        itog["regiony"].append({
            "kod": region["kod"],
            "imya": region["imya"],
            "yakor": region["yakor"],
            "naideno_vin": len(razlozheno[region["kod"]]),
            "proshlo_porog": godnyh,
            "pyaterka": pyat,
        })

    json.dump(itog, open(ITOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for r in itog["regiony"]:
        print("%-32s найдено %3d, прошло порог %3d, в пятёрке %d"
              % (r["imya"], r["naideno_vin"], r["proshlo_porog"], len(r["pyaterka"])))
        for v in r["pyaterka"]:
            print("    %-44s %.1f (%d) → %.2f"
                  % ((v["hozyaistvo"] + " " + v["vino"])[:44],
                     v["ocenka"], v["chislo_ocenok"], v["itogovaya"]))
    print("\nзаписано %s" % ITOG)


if __name__ == "__main__":
    main()
