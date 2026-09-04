#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сверить место хозяйства с адресом на его собственном сайте.

Зачем. Место у двух с лишним сотен хозяйств стоит по Винарском регистру,
а насеље регистра — это адрес юридического лица. Обычно он совпадает
с подвалом, но не всегда, и разница молча уводит вино в чужую главу:
Ђорђевић стоял в Лапову, в Шумадијском рејону, а винарија и шесть
гектаров у него в Горњем Ступњу под Александровцем, то есть в Жупи.
Нашлось это случайно. Проверка должна быть не случайной.

Как. У хозяйства берётся его сайт (адрес — из карточки Vivino), с него
главная и обычные страницы контактов, и из них вынимается сербский
почтовый адрес. Три способа, по убыванию надёжности:

    schema.org/PostalAddress   addressLocality + postalCode
    почтовый индекс с городом  «37240 Aleksandrovac»
    строка «Адреса: …»         до конца предложения

Найденное место переводится в рејон теми же картами, что и весь разбор
(`sobrat-rejony.py`), и сравнивается с нашим. Расхождение печатается —
но само по себе оно ничего не меняет: место правится руками, в
`raion-hozyaistv.json`, и только после того, как человек посмотрит.
Ложных тревог тут будет много: у хозяйства бывает контора в городе,
а сайт бывает общий на несколько подвалов.

    python3 _rabota/rejtingi/sverit-adresa.py [часть имени]

Пишет `sverka-adresov.json` и печатает расхождения. Кеш — `kesh-adresa/`.
"""
import concurrent.futures
import html
import importlib.util
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-adresa"
SROK = 10
POTOKOV = 10       # хозяйства разные, и каждое опрашивается по одному
PAUZA = 0.4
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Страницы, где обычно стоит адрес. Больше десятка не берём: это чужой
# сайт, и ходить по нему стоит ровно столько, сколько нужно.
STRANICY = ("", "/kontakt", "/kontakt/", "/contact", "/o-nama")
# Строка адреса ловится по почтовому индексу — пять цифр, — и он стоит
# то перед городом («34310 Topola»), то после («Topola – Oplenac,34310»).
# Поэтому берётся вся строка целиком, а разбирать её — дело `po_mestu`:
# оно и по запятым поделит, и по словам укоротит, и признает только то,
# что знают карты рејонизације.
INDEKS = re.compile(r"^.{0,90}\b\d{5}\b.{0,60}$", re.M)
ADRESA = re.compile(r"^.{0,40}[Aa]dres[ае]?\s*:?\s*([^\n<|•]{5,90})$", re.M)
# Строки, в которых индекс есть, а адреса нет: телефоны, цены, годы.
NE_ADRES = re.compile(r"(rsd|din\b|€|\$|tel|\+381|\bwww\b|@)", re.I)
# То, что стоит за словом «адрес», но адресом не является.
NE_MESTO = re.compile(r"^(srbij|serbia|republika|ulica|bb\b|tel|e-?mail|www)", re.I)


# Расхождения, просмотренные руками. Тут они разобраны, и в следующий
# раз проверка о них не кричит — но и не прячет: пишет, что разобрано.
RAZOBRANO_RUKAMI = {
    "Vinarija Pet Hrastova":
        "Не ошибка: «Štulac 36210» — село под Врњачком Бањом, индекс её. "
        "Рејонизација знает другой Штулац, кадастровую општину Винарачког "
        "виногорја под Лесковцем, и карта хватается за него. Место "
        "хозяйства — Врњачка Бања, и Рејон Три Мораве ему ставит "
        "справочник vinarijesrbije.rs прямо.",
    "Vinarija Tana":
        "Не ошибка: «Vladetina 5, Beograd» — контора. Виноградник "
        "в Тамничу, как и пишет регистр, а Тамнич — кадастровая општина "
        "Рогљевачко-рајачког виногорја.",
}


def modul(imya, fajl):
    spec = importlib.util.spec_from_file_location(imya, ZDES / fajl)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def vzjat(adres):
    for nomer in range(2):
        try:
            z = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
            with urllib.request.urlopen(z, timeout=SROK) as o:
                return o.status, o.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception:
            if nomer:
                return 0, ""
            time.sleep(2)
    return 0, ""


def tekst(razmetka):
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", razmetka)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return re.sub(r"[ \t\xa0]+", " ", t)


def mesta_so_stranicy(razmetka):
    """Строки, в которых может стоять место, по убыванию надёжности."""
    najdeno = []
    for kus in re.finditer(r'(?s)<script[^>]*ld\+json[^>]*>(.*?)</script>',
                           razmetka):
        try:
            d = json.loads(kus.group(1).strip())
        except ValueError:
            continue
        stopka = [d] if isinstance(d, dict) else (d if isinstance(d, list) else [])
        while stopka:
            z = stopka.pop()
            if not isinstance(z, dict):
                continue
            stopka += [v for v in z.values() if isinstance(v, (dict, list))]
            if z.get("@type") == "PostalAddress" and z.get("addressLocality"):
                najdeno.append(("schema", str(z["addressLocality"]).strip()))
    t = tekst(razmetka)
    for kus in INDEKS.finditer(t):
        stroka = kus.group(0).strip(" ,.;:|")
        if stroka and not NE_ADRES.search(stroka):
            najdeno.append(("индекс", stroka))
    for kus in ADRESA.finditer(t):
        stroka = kus.group(1).strip(" ,.;:|")
        # «E-mail adresa» и подобное: за словом «адрес» стоит не адрес.
        if stroka and not NE_MESTO.match(stroka) and not NE_ADRES.search(stroka):
            najdeno.append(("строка адреса", stroka))
    vidano, itog = set(), []
    for kak, mesto in najdeno:
        if mesto.lower() not in vidano:
            vidano.add(mesto.lower())
            itog.append((kak, mesto))
    return itog


def kogo_sverjat(sr):
    """Кого сверять: у кого место стоит по регистру и есть свой сайт.

    Регистр — самый частый источник места и самый уязвимый: насеље в нём
    это адрес общества. Сайты берутся из карточек хозяйств Vivino. Сайт,
    записанный сразу у нескольких хозяйств, в свидетели не годится:
    у трёх подрумов Жупе в карточках стоит один и тот же адрес.
    """
    rejony = json.loads((ZDES / "rejony-hozyaistv.json")
                        .read_text(encoding="utf-8"))["hozyaistva"]
    sajty, skolko = {}, {}
    for fajl in sorted((ZDES / "kesh-vivino-adresa").glob("*.json")):
        try:
            z = json.loads(fajl.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not z.get("sajt") or not z.get("imya"):
            continue
        host = re.sub(r"^https?://", "", z["sajt"].strip()).split("/")[0]
        if not host:
            continue
        skolko[host] = skolko.get(host, 0) + 1
        sajty.setdefault(sr.klyuch_hozyaistva(z["imya"]), (z["sajt"], host))

    spisok = []
    for v in rejony.values():
        pokazaniya = v.get("pokazaniya") or []
        registr = [x for x in pokazaniya if x.startswith("registar:")]
        if not (v.get("rejon") and registr and v.get("istochnik") == "mesto"):
            continue
        para = sajty.get(sr.klyuch_hozyaistva(v["hozyaistvo"]))
        if not para or skolko[para[1]] > 1:
            continue
        spisok.append([v["hozyaistvo"], para[0], v["rejon"],
                       v.get("gorod"), registr[0]])
    return sorted(spisok)


def odno(zapis, karty, po_mestu):
    imya, sajt, nash_rejon, nash_gorod, reg = zapis
    host = re.sub(r"^https?://", "", sajt.strip()).split("/")[0]
    if not host:
        return None
    nashlos = []
    for put in STRANICY:
        imya_kesha = re.sub(r"\W+", "-", host + put)[:60] + ".html"
        fajl = KESH / imya_kesha
        if fajl.exists():
            telo, kod = fajl.read_text(encoding="utf-8", errors="replace"), 200
        else:
            kod, telo = vzjat("https://" + host + put)
            if kod == 200 and telo:
                KESH.mkdir(exist_ok=True)
                fajl.write_text(telo, encoding="utf-8")
            time.sleep(PAUZA)
        if kod != 200 or not telo:
            continue
        nashlos += mesta_so_stranicy(telo)
        if nashlos:
            break            # место названо — дальше по чужому сайту не ходим
    # Место → рејон теми же картами, что и весь разбор.
    razobrano = []
    for kak, mesto in nashlos[:12]:
        # Строку пробуем дважды: как есть и без чисел. `kandidaty`
        # укорачивает кусок с конца, и в «34310 Topola, Srbija» до самой
        # Тополе дело не доходит — от неё остаётся индекс. Числа при этом
        # снимаются только вторым заходом: в имени места они бывают
        # значимы, а первый заход точнее.
        bez_chisel = re.sub(r"\s+", " ", re.sub(r"\b\d+[a-zA-ZбБ]?\b|\bbb\b",
                                                " ", mesto)).strip(" ,.-")
        for kus_mesto in [mesto] + ([bez_chisel] if bez_chisel != mesto else []):
            rejon, vinogorje, kusok = po_mestu(kus_mesto, karty)
            if rejon:
                razobrano.append({"kak": kak, "mesto": mesto, "rejon": rejon,
                                  "vinogorje": vinogorje, "po_kusku": kusok})
                break
    return {"hozyaistvo": imya, "sajt": "https://" + host,
            "nash_rejon": nash_rejon, "nash_gorod": nash_gorod,
            "registr": reg, "najdeno": nashlos[:12], "razobrano": razobrano}


def main():
    tolko = next((a for a in sys.argv[1:] if not a.startswith("--")), "")
    sr = modul("sobrat_rejony", "sobrat-rejony.py")
    _, _, karty = sr.spravochnik()
    spisok = [z for z in kogo_sverjat(sr)
              if not tolko or tolko.lower() in z[0].lower()]

    itogi = []
    with concurrent.futures.ThreadPoolExecutor(POTOKOV) as b:
        for nomer, z in enumerate(b.map(
                lambda x: odno(x, karty, sr.po_mestu), spisok), 1):
            if not z:
                continue
            itogi.append(z)
            rejony = {r["rejon"] for r in z["razobrano"]}
            metka = ("—" if not rejony else
                     "совпало" if rejony == {z["nash_rejon"]} else
                     "РАСХОЖДЕНИЕ" if z["nash_rejon"] not in rejony else "и то и то")
            print("%3d/%3d %-30s %-12s %s" % (
                nomer, len(spisok), z["hozyaistvo"][:30], metka,
                "; ".join(sorted(rejony)) or ""))

    (ZDES / "sverka-adresov.json").write_text(json.dumps({
        "chto_eto": "Сверка места хозяйства с адресом на его собственном сайте. "
                    "Расхождение — повод посмотреть глазами, а не править машиной.",
        "sobrano": time.strftime("%Y-%m-%d"),
        "hozyaistv": len(itogi),
        "sverka": itogi,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    spor = [z for z in itogi if z["razobrano"]
            and z["nash_rejon"] not in {r["rejon"] for r in z["razobrano"]}]
    print("\nсверено %d хозяйств, сайт назвал место у %d, расходится у %d"
          % (len(itogi), sum(1 for z in itogi if z["razobrano"]), len(spor)))
    novye = [z for z in spor if z["hozyaistvo"] not in RAZOBRANO_RUKAMI]
    if len(spor) != len(novye):
        print("из них разобрано руками раньше: %d" % (len(spor) - len(novye)))
    for z in spor:
        razbor = RAZOBRANO_RUKAMI.get(z["hozyaistvo"])
        print("\n   %s: у нас %s (%s), сайт — %s" % (
            z["hozyaistvo"], z["nash_rejon"], z["nash_gorod"],
            "; ".join("%s → %s" % (r["mesto"], r["rejon"]) for r in z["razobrano"])))
        if razbor:
            print("      %s" % razbor)


if __name__ == "__main__":
    main()
