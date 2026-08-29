#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сплошной сбор Vivino по сербским хозяйствам.

Как это устроено. У Vivino есть два входа, и годится только второй.

Первый — `api/explore/explore`, «витрина». Он фильтрует по рынку, а рынок
определяется по адресу запроса, не параметром. С европейского адреса
сербских вин видно десяток: остальные в этом магазине не продаются.
Для нашей задачи он бесполезен.

Второй — листинг хозяйств страны плюс `api/wineries/{id}/wines`. Рынок
там ни при чём: отдаётся всё, что у хозяйства есть, с оценкой и числом
отзывов полями. Этим и берём.

    python3 _rabota/rejtingi/sobrat-vivino.py
    python3 _rabota/rejtingi/sobrat-vivino.py --iz-kesha    # без сети

Складывает `vivino-syrye.json` — его подхватывает `sobrat-tablicy.py`.
Ответы сохраняются в `kesh-vivino/`, поэтому повторный запуск не бьёт
по сайту заново.
"""

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

RYADOM = os.path.dirname(os.path.abspath(__file__))
KESH = os.path.join(RYADOM, "kesh-vivino")
ITOG = os.path.join(RYADOM, "vivino-syrye.json")

LISTING = "https://www.vivino.com/en/wineries/countries/republic-of-serbia?page=%d"
PREDEL_VIN = 100
VINA_HOZYAISTVA = ("https://www.vivino.com/api/wineries/%s/wines"
                   "?per_page=" + str(PREDEL_VIN))

ZAGOLOVKI = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
}

# Числовые коды видов вина у Vivino.
VIDY = {1: "красное", 2: "белое", 3: "игристое", 4: "розе",
        7: "десертное", 24: "креплёное"}


def peredyshka():
    """Пауза между запросами. Сайт чужой, торопиться некуда."""
    time.sleep(1.0 + random.random())


def vzyat(adres, kak_json, imya_v_keshe):
    """Скачать с оглядкой на кеш: то, что уже брали, второй раз не берём."""
    os.makedirs(KESH, exist_ok=True)
    put = os.path.join(KESH, imya_v_keshe)
    if os.path.exists(put):
        soderzhimoe = open(put, encoding="utf-8").read()
        return json.loads(soderzhimoe) if kak_json else soderzhimoe

    zapros = urllib.request.Request(adres, headers=dict(
        ZAGOLOVKI, **({"Accept": "application/json"} if kak_json else {})))
    # Сеть иногда рвётся посреди ответа. Это не повод терять час сбора:
    # пробуем ещё, с нарастающей паузой.
    posledn = None
    for popytka in range(4):
        try:
            with urllib.request.urlopen(zapros, timeout=60) as otvet:
                soderzhimoe = otvet.read().decode("utf-8", "replace")
            break
        except urllib.error.HTTPError:
            raise
        except Exception as e:                              # noqa: BLE001
            posledn = e
            time.sleep(2 ** popytka)
    else:
        raise posledn
    with open(put, "w", encoding="utf-8") as f:
        f.write(soderzhimoe)
    peredyshka()
    return json.loads(soderzhimoe) if kak_json else soderzhimoe


# --------------------------------------------------------------------------
# хозяйства
# --------------------------------------------------------------------------

# В карточке хозяйства нужное лежит в служебных атрибутах разметки:
# идентификатор, имя и ссылка со слагом. Это устойчивее, чем ловить
# имя по классам, которые у них меняются от сборки к сборке.
KARTOCHKA = re.compile(
    r'href="/en/wineries/(?P<slug>[a-z0-9\-]+)"[^>]*'
    r'data-mp-entity-id="(?P<id>\d+)"[^>]*'
    r'data-mp-entity-name="(?P<imya>[^"]*)"', re.S)


def vse_hozyaistva(predel_stranic=40):
    najdeno, stranica = {}, 1
    while stranica <= predel_stranic:
        try:
            html = vzyat(LISTING % stranica, False, "listing-%02d.html" % stranica)
        except urllib.error.HTTPError as e:
            sys.stderr.write("страница %d: HTTP %s\n" % (stranica, e.code))
            break
        bylo = len(najdeno)
        for m in KARTOCHKA.finditer(html):
            najdeno[m.group("id")] = {
                "id": m.group("id"),
                "imya": m.group("imya"),
                "slug": m.group("slug"),
            }
        novyh = len(najdeno) - bylo
        print("листинг, страница %d: +%d, всего %d" % (stranica, novyh, len(najdeno)))
        if novyh == 0:
            break
        stranica += 1
    return list(najdeno.values())


# --------------------------------------------------------------------------
# вина
# --------------------------------------------------------------------------

def vina_hozyaistva(hozyaistvo):
    try:
        otvet = vzyat(VINA_HOZYAISTVA % hozyaistvo["id"], True,
                      "vina-%s.json" % hozyaistvo["id"])
    except urllib.error.HTTPError as e:
        sys.stderr.write("  %s: HTTP %s\n" % (hozyaistvo["imya"], e.code))
        return []
    # Ответ не говорит, сколько вин у хозяйства всего, поэтому обрезку
    # видно только по тому, что их ровно столько, сколько просили. Пока
    # такого не было — самое большое хозяйство отдаёт 75 из ста, — но
    # молча упереться в предел этот сбор не должен.
    if len(otvet.get("wines") or []) >= PREDEL_VIN:
        sys.stderr.write("  %s: вин ровно %d — вероятно, выдача обрезана\n"
                         % (hozyaistvo["imya"], PREDEL_VIN))
    out = []
    for v in otvet.get("wines") or []:
        st = v.get("statistics") or {}
        # У хозяйства могут числиться вина других его марок; страну
        # проверяем по региону самого вина, а не по листингу.
        region = v.get("region") or {}
        strana = ((region.get("country") or {}).get("code") or "").lower()
        out.append({
            "id_vina": v.get("id"),
            "hozyaistvo": (v.get("winery") or {}).get("name") or hozyaistvo["imya"],
            "vino": v.get("name") or "",
            "ocenka": st.get("ratings_average"),
            "chislo_ocenok": st.get("ratings_count"),
            # Сколько человек сфотографировали этикетку. Это не качество,
            # а охват: сколько людей вообще брали бутылку в руки. Величина
            # своя и полезная — у самых ходовых сербских вин она в двести
            # раз больше медианы, и с баллом почти не связана.
            "etiketok": st.get("labels_count"),
            "urozhaev": st.get("vintages_count"),
            "vid": VIDY.get(v.get("type_id"), ""),
            "region_vivino": region.get("name") or "",
            "strana": strana,
            "adres": "https://www.vivino.com/w/%s" % v["id"] if v.get("id") else "",
        })
    return out


def main():
    razbor = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    razbor.add_argument("--iz-kesha", action="store_true",
                        help="ничего не качать, собрать из уже скачанного")
    dovody = razbor.parse_args()

    if dovody.iz_kesha and not os.path.isdir(KESH):
        sys.exit("кеша нет: %s" % KESH)

    hozyaistva = vse_hozyaistva()
    print("\nхозяйств в Сербии: %d\n" % len(hozyaistva))

    vse_vina, pusto = [], 0
    for n, h in enumerate(hozyaistva, 1):
        vina = vina_hozyaistva(h)
        if not vina:
            pusto += 1
        vse_vina.extend(vina)
        print("%3d/%d  %-42s вин %3d  (всего %d)"
              % (n, len(hozyaistva), h["imya"][:42], len(vina), len(vse_vina)))

    # Одно вино приходит один раз, но хозяйства иногда пересекаются.
    po_id = {}
    for v in vse_vina:
        if v["id_vina"] and v["id_vina"] not in po_id:
            po_id[v["id_vina"]] = v
    vina = list(po_id.values())

    ne_serbskie = [v for v in vina if v["strana"] and v["strana"] != "rs"]
    s_ocenkoj = [v for v in vina if v.get("ocenka")]
    s_chislom = [v for v in vina if v.get("chislo_ocenok")]

    json.dump({
        "sobrano": time.strftime("%Y-%m-%d"),
        "hozyaistv": len(hozyaistva),
        "vina": vina,
    }, open(ITOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\nзаписано %s" % ITOG)
    print("   хозяйств %d, из них без вин %d" % (len(hozyaistva), pusto))
    print("   вин %d, с оценкой %d, с числом отзывов %d"
          % (len(vina), len(s_ocenkoj), len(s_chislom)))
    if ne_serbskie:
        print("   вин не из Сербии (другие марки тех же хозяйств): %d"
              % len(ne_serbskie))


if __name__ == "__main__":
    main()
