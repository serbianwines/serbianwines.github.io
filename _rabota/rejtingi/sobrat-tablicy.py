#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Собрать из сырых выписок три нормализованные таблицы.

Сырьё — `vivino-zapisi.jsonl`, `kritiki-zapisi.jsonl`, `raion-hozyaistv.json`,
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


def put(imya):
    return os.path.join(RYADOM, imya)


def chitat_jsonl(imya):
    if not os.path.exists(put(imya)):
        return []
    return [json.loads(s) for s in open(put(imya), encoding="utf-8") if s.strip()]


def klyuch(*chasti):
    """Устойчивый ключ: без регистра, диакритики и лишних пробелов."""
    s = " ".join(c for c in chasti if c).lower()
    s = s.replace("š", "s").replace("đ", "d").replace("č", "c")
    s = s.replace("ć", "c").replace("ž", "z")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    s = re.sub(r"[^a-z0-9а-я]+", "-", s)
    return s.strip("-")


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
    vivino = chitat_jsonl("vivino-zapisi.jsonl")
    kritiki = chitat_jsonl("kritiki-zapisi.jsonl")
    nagrady_syrye = chitat_jsonl("nagrady-zapisi.jsonl")
    karta = json.load(open(put("raion-hozyaistv.json"), encoding="utf-8"))["hozyaistva"]
    zvezdy = {z["hozyaistvo"]: z for z in
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
    imena = ({z["hozyaistvo"] for z in vivino} | {z["hozyaistvo"] for z in kritiki}
             | {z["hozyaistvo"] for z in nagrady_syrye})
    hozyaistva = []
    for imya in sorted(imena):
        svedeniya = karta.get(imya, {})
        slugi = {razobrat_stranicu(z.get("stranica"))[1] for z in vivino
                 if z["hozyaistvo"] == imya}
        slug = ""
        for adres in slugi:
            sovpalo = re.search(r"/wineries/([a-z0-9-]+)", adres or "")
            if sovpalo:
                slug = sovpalo.group(1)
                break
        hozyaistva.append({
            "hozyaistvo": imya,
            "klyuch": klyuch(imya),
            "raion_knigi": svedeniya.get("raion"),
            "raion_istochnik": svedeniya.get("istochnik", "ne_ustanovlen"),
            "gde": svedeniya.get("gde", ""),
            "v_knige": v_knige_hoz(imya),
            "vivino_slug": slug,
            "falstaff_zvezd": zvezdy.get(imya, {}).get("zvezd"),
            "vin_v_dannyh": sum(1 for z in vivino if z["hozyaistvo"] == imya),
        })

    # ---------------- вина ----------------
    vina, vidano = [], {}
    for z in vivino:
        k = klyuch(z["hozyaistvo"], z["vino"])
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
                "vivino_status": "ocenka_est" if z.get("ocenka") else "malo_ocenok",
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
        elif vivino_id and not vidano[k]["vivino_id"]:
            vidano[k]["vivino_id"] = vivino_id
            vidano[k]["vivino_adres"] = adres
    for z in nagrady_syrye:
        if not z["vino"]:
            continue          # награда хозяйству, а не вину
        k = klyuch(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": z["vino"],
                "vivino_id": None,
                "vivino_adres": "",
                "vivino_status": "net_na_vivino",
                "v_knige": v_knige_vino(z["vino"]),
                "est_u_kritikov": False,
            }
    for z in kritiki:
        k = klyuch(z["hozyaistvo"], z["vino"])
        if k not in vidano:
            vidano[k] = {
                "klyuch": k,
                "hozyaistvo": z["hozyaistvo"],
                "vino": z["vino"],
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
        if z.get("ocenka") is None:
            continue
        _, adres, ogovorka = razobrat_stranicu(z.get("stranica"))
        ocenki.append({
            "klyuch_vina": klyuch(z["hozyaistvo"], z["vino"]),
            "hozyaistvo": z["hozyaistvo"],
            "vino": z["vino"],
            "istochnik": "vivino",
            "shkala": 5,
            "ball": z["ocenka"],
            "vyborka": z.get("chislo_ocenok"),
            "vyborka_nizhnyaya_granica": nizhnyaya_granica(ogovorka),
            "god": None,
            "ogovorka": ogovorka,
            "stranica": adres,
            "sobrano": SOBRANO,
        })
    for z in kritiki:
        if z.get("ball") is None:
            continue
        ocenki.append({
            "klyuch_vina": klyuch(z["hozyaistvo"], z["vino"]),
            "hozyaistvo": z["hozyaistvo"],
            "vino": z["vino"],
            "istochnik": z["istochnik"],
            "shkala": 100,
            "ball": z["ball"],
            "vyborka": None,
            "vyborka_nizhnyaya_granica": False,
            "god": int(z["god"]) if z.get("god") else None,
            "ogovorka": "",
            "stranica": z.get("stranica", ""),
            "sobrano": SOBRANO,
        })

    # ---------------- награды ----------------
    nagrady = [{
        "klyuch_vina": klyuch(z["hozyaistvo"], z["vino"]) if z["vino"] else "",
        "hozyaistvo": z["hozyaistvo"],
        "vino": z["vino"],
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


if __name__ == "__main__":
    main()
