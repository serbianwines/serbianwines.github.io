#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сбор рейтингов браузером. Запускать на машине, где сайты открываются.

Зачем нужен браузер. Три источника из четырёх рисуют свои списки сценарием:
в исходном HTML их нет, они подгружаются отдельным запросом за JSON. Поиск
такие страницы видит пустыми — отсюда вся неполнота собранного вручную.
Браузер эти запросы делает сам, и остаётся только подслушать ответы.

**Мы не разбираем нарисованную страницу.** Мы перехватываем JSON, который
страница получает от своего же сервера. Это и надёжнее (разметка меняется
часто, поля ответа — редко), и быстрее (одна загрузка вместо десятков),
и данные приходят уже разобранными.

    pip install playwright
    playwright install chromium

    python3 sobrat-brauzerom.py                  # все источники
    python3 sobrat-brauzerom.py --tolko falstaff
    python3 sobrat-brauzerom.py --tolko decanter --gody 2020 2026

Пишет в те же сырые файлы, что и ручной сбор:

    kritiki-zapisi.jsonl   стобалльные оценки
    nagrady-zapisi.jsonl   медали и места в категориях

Дальше без изменений: `sobrat-tablicy.py`, `proverit-dannye.py`,
`svesti-kritikov.py`. Книгу скрипт не трогает и трогать не должен.

Оговорка. Скрипт писался в среде, где все эти сайты закрыты политикой
исходящего трафика, — на живых страницах он не проверялся. Селекторы и имена
полей взяты по внешним признакам и почти наверняка потребуют правки при
первом запуске. Что править — сказано в комментариях у каждого сборщика;
`--pokazat-otvety` печатает адреса всех перехваченных JSON-ответов, с этого
и надо начинать.
"""

import argparse
import json
import os
import re
import sys
import time

RYADOM = os.path.dirname(os.path.abspath(__file__))
PAUZA = 1.5          # между переходами; сайты чужие, торопиться некуда


# --------------------------------------------------------------------------
# запись в сырьё
# --------------------------------------------------------------------------

def dopisat(imya_fajla, zapisi, klyuchi):
    """Дописать записи, не плодя повторов.

    Ключ повтора у каждого файла свой, поэтому передаётся списком имён полей.
    """
    put = os.path.join(RYADOM, imya_fajla)
    bylo = {}
    if os.path.exists(put):
        for stroka in open(put, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                bylo[tuple(z.get(k) for k in klyuchi)] = z
    dobavleno = 0
    for z in zapisi:
        k = tuple(z.get(x) for x in klyuchi)
        if k not in bylo:
            dobavleno += 1
        bylo[k] = z
    with open(put, "w", encoding="utf-8") as f:
        for z in bylo.values():
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    print("%s: всего %d, новых %d" % (imya_fajla, len(bylo), dobavleno))


# --------------------------------------------------------------------------
# перехват
# --------------------------------------------------------------------------

class Perehvat:
    """Копит JSON-ответы, которые страница получила, пока грузилась.

    Смысл всей затеи. Вместо того чтобы вытаскивать числа из вёрстки, берём
    их из того же ответа, из которого их берёт сама страница.
    """

    def __init__(self, stranica, pokazat=False):
        self.otvety = []
        self.pokazat = pokazat
        stranica.on("response", self._prishlo)

    def _prishlo(self, otvet):
        tip = (otvet.headers or {}).get("content-type", "")
        if "json" not in tip:
            return
        try:
            telo = otvet.json()
        except Exception:                                   # noqa: BLE001
            return
        self.otvety.append((otvet.url, telo))
        if self.pokazat:
            print("   ← %s" % otvet.url[:160])

    def najti(self, *kuski_adresa):
        """Ответы, в адресе которых встретился любой из кусков."""
        return [(u, t) for u, t in self.otvety
                if any(k in u for k in kuski_adresa)]

    def vse_slovari(self, priznak):
        """Пройти все ответы вглубь и вернуть словари, где есть нужное поле.

        Ответы у разных сайтов вложены по-разному, и угадывать путь заранее
        бессмысленно. Дешевле обойти дерево и собрать всё, что похоже на
        запись о вине.
        """
        najdeno = []

        def obojti(uzel):
            if isinstance(uzel, dict):
                if priznak in uzel:
                    najdeno.append(uzel)
                for v in uzel.values():
                    obojti(v)
            elif isinstance(uzel, list):
                for v in uzel:
                    obojti(v)

        for _, telo in self.otvety:
            obojti(telo)
        return najdeno


def otkryt(brauzer, adres, perehvat_pokazat=False, zhdat=2500):
    stranica = brauzer.new_page()
    perehvat = Perehvat(stranica, perehvat_pokazat)
    stranica.goto(adres, wait_until="networkidle", timeout=60000)
    stranica.wait_for_timeout(zhdat)
    return stranica, perehvat


# --------------------------------------------------------------------------
# Falstaff
# --------------------------------------------------------------------------

FALSTAFF_SPISKI = [
    ("https://www.falstaff.com/en/listings/red-wine-the-best-vintages-from-serbia", "красное"),
    ("https://www.falstaff.com/en/listings/white-wine-the-best-vintages-from-serbia", "белое"),
    ("https://www.falstaff.com/en/listings/rose-wine-the-best-vintages-from-serbia", "розе"),
]
FALSTAFF_HOZYAISTVA = "https://www.falstaff.com/en/listings/the-best-wineries-in-serbia"


def sobrat_falstaff(brauzer, pokazat):
    """Списки лучших сербских вин и хозяйств.

    Ожидается 52 красных, 48 белых, 12 розе и 40 хозяйств со звёздами.
    Если пришло меньше — список подгружается по прокрутке; тогда надо
    крутить страницу вниз, пока число записей не перестанет расти.
    """
    zapisi = []
    for adres, cvet in FALSTAFF_SPISKI:
        print("Falstaff, %s: %s" % (cvet, adres))
        stranica, perehvat = otkryt(brauzer, adres, pokazat)
        prokrutit_do_konca(stranica)
        # У Falstaff балл лежит в поле с «points» или «rating» в имени.
        for uzel in perehvat.vse_slovari("points") + perehvat.vse_slovari("rating"):
            zapis = razobrat_falstaff(uzel, cvet)
            if zapis:
                zapisi.append(zapis)
        stranica.close()
        time.sleep(PAUZA)

    if zapisi:
        dopisat("kritiki-zapisi.jsonl", zapisi,
                ["istochnik", "hozyaistvo", "vino", "god"])
    else:
        print("  Falstaff: ничего не перехвачено. Запустите с --pokazat-otvety")
        print("  и посмотрите, по какому адресу приходит список.")

    print("Falstaff, хозяйства: %s" % FALSTAFF_HOZYAISTVA)
    stranica, perehvat = otkryt(brauzer, FALSTAFF_HOZYAISTVA, pokazat)
    prokrutit_do_konca(stranica)
    zvezdy = []
    for uzel in perehvat.vse_slovari("stars") + perehvat.vse_slovari("rating"):
        imya = uzel.get("name") or uzel.get("title")
        zvezd = uzel.get("stars") or uzel.get("rating")
        if imya and isinstance(zvezd, (int, float)) and 1 <= zvezd <= 5:
            zvezdy.append({"hozyaistvo": imya, "zvezd": int(zvezd),
                           "gde": uzel.get("city") or uzel.get("location") or ""})
    stranica.close()
    if zvezdy:
        put = os.path.join(RYADOM, "falstaff-zvezdy.json")
        d = json.load(open(put, encoding="utf-8"))
        bylo = {z["hozyaistvo"]: z for z in d["hozyaistva"]}
        for z in zvezdy:
            bylo[z["hozyaistvo"]] = z
        d["hozyaistva"] = sorted(bylo.values(), key=lambda z: -z["zvezd"])
        json.dump(d, open(put, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("falstaff-zvezdy.json: хозяйств %d" % len(d["hozyaistva"]))


def razobrat_falstaff(uzel, cvet):
    ball = uzel.get("points") or uzel.get("rating")
    if not isinstance(ball, (int, float)) or not (50 <= ball <= 100):
        return None
    imya = uzel.get("name") or uzel.get("title") or ""
    hozyaistvo = ""
    for klyuch in ("producer", "winery", "manufacturer"):
        znachenie = uzel.get(klyuch)
        if isinstance(znachenie, dict):
            hozyaistvo = znachenie.get("name", "")
        elif isinstance(znachenie, str):
            hozyaistvo = znachenie
        if hozyaistvo:
            break
    god = uzel.get("vintage") or uzel.get("year")
    # Имя вина у Falstaff часто начинается с года: «2020 Vinčić Grašac».
    sovpalo = re.match(r"^(\d{4})\s+(.*)$", imya)
    if sovpalo and not god:
        god, imya = int(sovpalo.group(1)), sovpalo.group(2)
    if not (imya and hozyaistvo):
        return None
    return {
        "istochnik": "falstaff",
        "hozyaistvo": hozyaistvo,
        "vino": imya,
        "god": str(god) if god else None,
        "ball": int(ball),
        "stranica": "falstaff, список «%s»" % cvet,
    }


def prokrutit_do_konca(stranica, predel=40):
    """Дотянуть ленивый список до конца.

    Списки Falstaff подгружаются по прокрутке. Крутим, пока высота
    страницы растёт, но не больше `predel` раз — на случай бесконечной ленты.
    """
    bylo = 0
    for _ in range(predel):
        stranica.mouse.wheel(0, 20000)
        stranica.wait_for_timeout(700)
        stalo = stranica.evaluate("document.body.scrollHeight")
        if stalo == bylo:
            break
        bylo = stalo


# --------------------------------------------------------------------------
# Decanter World Wine Awards
# --------------------------------------------------------------------------

def sobrat_decanter(brauzer, gody, pokazat):
    """Медали DWWA по Сербии — то, чего не добыть поиском.

    Поиск наград на сайте конкурса — сценарий поверх собственного API.
    Открываем страницу поиска с нужными параметрами и слушаем, что ей
    отвечает сервер. Ответ даёт вино, хозяйство, урожай, медаль и балл
    сразу — то есть все 146 медалей 2026 года за один заход.

    Если параметры в адресе изменились, откройте поиск руками, выберите
    Serbia и нужный год и посмотрите, какой запрос уходит: `--pokazat-otvety`
    печатает адреса всех JSON-ответов.
    """
    nagrady, ocenki = [], []
    for god in gody:
        adres = ("https://awards.decanter.com/DWWA/%d/search/wines"
                 "?country=Serbia&pageSize=200" % god)
        print("Decanter %d: %s" % (god, adres))
        stranica, perehvat = otkryt(brauzer, adres, pokazat, zhdat=4000)
        for uzel in perehvat.vse_slovari("award") + perehvat.vse_slovari("medal"):
            zapis = razobrat_decanter(uzel, god)
            if not zapis:
                continue
            nagrady.append(zapis[0])
            if zapis[1]:
                ocenki.append(zapis[1])
        stranica.close()
        time.sleep(PAUZA)

    if nagrady:
        dopisat("nagrady-zapisi.jsonl", nagrady,
                ["istochnik", "god", "kategoriya", "hozyaistvo", "vino"])
    if ocenki:
        dopisat("kritiki-zapisi.jsonl", ocenki,
                ["istochnik", "hozyaistvo", "vino", "god"])
    if not nagrady:
        print("  Decanter: ничего не перехвачено. Запустите с --pokazat-otvety")


MEDALI = {
    "platinum": "platina", "gold": "zlato", "silver": "srebro",
    "bronze": "bronza", "best in show": "best-in-show",
}


def razobrat_decanter(uzel, god_konkursa):
    medal_syraya = (uzel.get("award") or uzel.get("medal") or "")
    if not isinstance(medal_syraya, str):
        return None
    medal = MEDALI.get(medal_syraya.strip().lower())
    if not medal:
        return None
    vino = uzel.get("wineName") or uzel.get("name") or ""
    hozyaistvo = uzel.get("producerName") or uzel.get("producer") or ""
    if isinstance(hozyaistvo, dict):
        hozyaistvo = hozyaistvo.get("name", "")
    if not (vino and hozyaistvo):
        return None
    urozhaj = uzel.get("vintage") or uzel.get("year")
    ball = uzel.get("points") or uzel.get("score")

    nagrada = {
        "istochnik": "decanter",
        "god": god_konkursa,
        "kategoriya": medal_syraya.strip().lower(),
        "mesto": medal,
        "hozyaistvo": hozyaistvo,
        "vino": vino,
        "urozhaj": int(urozhaj) if str(urozhaj).isdigit() else None,
        "stranica": "awards.decanter.com, DWWA %d" % god_konkursa,
    }
    ocenka = None
    if isinstance(ball, (int, float)) and 50 <= ball <= 100:
        ocenka = {
            "istochnik": "decanter",
            "hozyaistvo": hozyaistvo,
            "vino": vino,
            "god": str(urozhaj) if urozhaj else None,
            "ball": int(ball),
            "stranica": "awards.decanter.com, DWWA %d" % god_konkursa,
        }
    return nagrada, ocenka


# --------------------------------------------------------------------------
# vino.rs — годовой тест
# --------------------------------------------------------------------------

VINO_RS = "https://www.vino.rs/aktuelno/veliki-test-vino-rs/najbolja-vina-srbije-%d.html"


def sobrat_vino_rs(brauzer, gody, pokazat):
    """Годовой тест «Najbolja vina Srbije».

    Здесь браузер, строго говоря, не нужен: страницы обычные, их взял бы и
    urllib. Но раз он уже запущен — пусть берёт заодно, меньше кода.

    Разметка у них простая, но категорий три десятка и подписаны они прозой.
    Поэтому скрипт только вытаскивает текст блоков, а раскладывать по
    категориям придётся глазами: список печатается на экран, из него
    строчки переносятся в `dobavit-nagrady.py`. Автоматически угадывать
    категорию по прозе — как раз тот случай, когда машина ошибётся тихо.
    """
    for god in gody:
        adres = VINO_RS % god
        print("\nvino.rs %d: %s" % (god, adres))
        try:
            stranica, _ = otkryt(brauzer, adres, pokazat, zhdat=1200)
        except Exception as e:                              # noqa: BLE001
            print("   не открылось: %s" % e)
            continue
        tekst = stranica.inner_text("body")
        stranica.close()
        for stroka in tekst.splitlines():
            stroka = stroka.strip()
            # Строки итогов у них выглядят как «Najbolje crveno vino: X 2020 Y».
            if re.search(r"najbolj|vinarija godine|pobednik", stroka, re.I) and len(stroka) < 200:
                print("   ", stroka)
        time.sleep(PAUZA)
    print("\nПеренесите нужные строки в dobavit-nagrady.py руками:")
    print("   vino.rs | год | категория | место | Хозяйство | Вино | урожай | адрес")


# --------------------------------------------------------------------------

def main():
    razbor = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    razbor.add_argument("--tolko", choices=["falstaff", "decanter", "vino.rs"],
                        help="один источник вместо всех")
    razbor.add_argument("--gody", type=int, nargs="+",
                        default=[2020, 2021, 2022, 2023, 2024, 2025, 2026],
                        help="годы конкурса и годового теста")
    razbor.add_argument("--pokazat-otvety", action="store_true",
                        help="печатать адреса всех перехваченных JSON-ответов")
    razbor.add_argument("--vidimyj", action="store_true",
                        help="показать окно браузера, а не работать вслепую")
    dovody = razbor.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("нет playwright: pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        brauzer = p.chromium.launch(headless=not dovody.vidimyj)
        kontekst = brauzer.new_context(
            locale="en-US",
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"))
        try:
            if dovody.tolko in (None, "falstaff"):
                sobrat_falstaff(kontekst, dovody.pokazat_otvety)
            if dovody.tolko in (None, "decanter"):
                sobrat_decanter(kontekst, dovody.gody, dovody.pokazat_otvety)
            if dovody.tolko in (None, "vino.rs"):
                sobrat_vino_rs(kontekst, dovody.gody, dovody.pokazat_otvety)
        finally:
            kontekst.close()
            brauzer.close()

    print("\nДальше:")
    print("   python3 sobrat-tablicy.py")
    print("   python3 proverit-dannye.py")


if __name__ == "__main__":
    main()
