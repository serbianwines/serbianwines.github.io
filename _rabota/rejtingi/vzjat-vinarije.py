#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Цены из собственных магазинов хозяйств.

Зачем. У флагманов цены не было как раз там, где она нужнее всего:
из 122 вин с баллом 93 и выше её знали у шестидесяти. Винотеки держат
ходовое, а «Момент» Веритаса или «Вожд» Александровића стоят у самого
хозяйства. Цена хозяйства — не полочная и не доставка, это третий канал,
и помечается он отдельно (`kanal: "hozyaistvo"`).

Как берётся. Сербские винарије почти поголовно сидят на WooCommerce,
а у него есть открытый Store API:

    https://<сайт>/wp-json/wc/store/products?per_page=100&page=N

Он отдаёт JSON с именем, ценой, наличием, категориями и адресом
карточки — разбирать вёрстку не нужно. Цена приходит в мелких единицах
(`price` 285000 при `currency_minor_unit` 2 — это 2850,00 динара).

Адреса сайтов берутся из `kesh-vivino-adresa/*.json`: там их 226,
и это те же страницы хозяйств, откуда взяты адреса и телефоны.

Две ловушки, обе стоили времени.

1. **Схема.** Vivino почти везде записал адрес как `http://`, а здешний
   прокси пропускает только `https`. На `http` он отвечает
   `403 host_not_allowed`, и это легко принять за отказ самого сайта —
   у пятнадцати хозяйств подряд. Поэтому адрес приводится к `https`.
2. **В магазине хозяйства не только вино.** Ракије, поклон-пакеты,
   деревянные шкатулки, чаше. «Trijumf XO» и «Trijumf Special» —
   ракије Александровића, и по началу имени они сошлись бы с винами
   «Trijumf». Поэтому товары с такими категориями отсеиваются здесь же,
   а категория сохраняется в записи: отсев видно.

Пишет `vinarije-ceny.json`. Кеш — в `kesh-vinarije/`.
"""
import concurrent.futures
import html
import json, os, pathlib, re, sys, time, urllib.error, urllib.request

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-vinarije"
PAUZA = 1.0
SROK = 15          # секунд на запрос: мёртвых адресов больше, чем живых
POTOKOV = 6        # хозяйства опрашиваются вперемешку, но каждое — по одному
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# Два адреса Store API: старый и с номером версии. Сайты держат то один,
# то другой, поэтому пробуются оба.
PUTI = ("/wp-json/wc/store/products?per_page=100&page=%d",
        "/wp-json/wc/store/v1/products?per_page=100&page=%d")
# Разделы магазина, где вина нет. Совпадение ищется по началу слова:
# «Rakije», «Rakija», «Poklon paketi», «Čaše», «Suveniri».
NE_VINO = re.compile(r"rakij|lozova[cč]|liker|poklon|suvenir|[cč]a[sš]e|"
                     r"maslin|med\b|[cč]aj|mast\b|kozmetik|knjig|majic|"
                     r"gift|souvenir|glass|meso|sir\b|[dž]em\b", re.I)


def vzjat(adres, popytok=2):
    """Скачать; при обрыве туннеля — ещё попытка с ожиданием.

    Обрыв здесь — не отказ сайта: туннель прокси рвётся сам по себе,
    и повтор через несколько секунд обычно проходит. Но и мёртвых
    адресов в списке много — Vivino собирал его годами, — поэтому
    попыток две, а не три, и срок короткий: иначе весь обход упирается
    в десяток доменов, которых давно нет.
    """
    for nomer in range(popytok):
        try:
            zapros = urllib.request.Request(adres, headers={"User-Agent": BRAUZER})
            with urllib.request.urlopen(zapros, timeout=SROK) as otvet:
                return otvet.status, otvet.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as oshibka:
            return oshibka.code, ""
        except Exception as oshibka:                       # обрыв, DNS, TLS
            if nomer == popytok - 1:
                return 0, str(oshibka)[:80]
            time.sleep(2 ** (nomer + 1))
    return 0, ""


def https(adres):
    """Адрес Vivino → https без пути. Прокси пропускает только его."""
    adres = (adres or "").strip()
    if not adres:
        return ""
    host = re.sub(r"^https?://", "", adres).split("/")[0]
    return "https://" + host if host else ""


def sajty():
    """Хозяйство → адрес сайта, из кеша адресов Vivino."""
    pary = {}
    for fajl in sorted((ZDES / "kesh-vivino-adresa").glob("*.json")):
        try:
            z = json.loads(fajl.read_text(encoding="utf-8"))
        except ValueError:
            continue
        adres = https(z.get("sajt"))
        if adres and z.get("imya"):
            pary.setdefault(adres, z["imya"])
    return pary


def imya_tovara(syroe):
    """Имя товара: без разметки и без экранированных знаков.

    WooCommerce кладёт в поле имени и то, и другое: у Јовца это
    «Merlot &lt;p&gt;Grand Reserve&lt;/p&gt;», у Дулке
    «Love&#038;Sunshine», у манастира Буково «Filigran &#8211;
    Cabernet sauvignon 1,5 L». Без чистки буквы разметки уходят
    в имя вина словами — «p», — и сведение с нашими именами врёт.
    """
    syroe = re.sub(r"<[^>]+>", " ", html.unescape(syroe or ""))
    return re.sub(r"\s+", " ", syroe).strip()


def cena(tovar):
    """Цена в динарах и валюта. У WooCommerce она в мелких единицах."""
    p = tovar.get("prices") or {}
    syroe, edinic = p.get("price"), p.get("currency_minor_unit")
    valyuta = p.get("currency_code") or ""
    if syroe in (None, "", "0") or edinic is None:
        return None, valyuta
    try:
        znachenie = int(syroe) / (10 ** int(edinic))
    except (TypeError, ValueError):
        return None, valyuta
    return (znachenie if valyuta == "RSD" else None), valyuta


def tovary_hozyaistva(adres, imya):
    """Все товары одного магазина. Возвращает список и пометку, что вышло."""
    kod = None
    for shablon in PUTI:
        # Сайт, который вовсе не отвечает, вторым адресом не оживёт.
        if kod == 0:
            break
        stranica, vsego, vidano = 1, [], set()
        while stranica <= 10:
            put_kesha = KESH / ("%s-%d.json" % (
                re.sub(r"\W+", "-", adres.replace("https://", "")), stranica))
            if put_kesha.exists():
                telo, kod = put_kesha.read_text(encoding="utf-8"), 200
            else:
                kod, telo = vzjat(adres + shablon % stranica)
                if kod == 200:
                    KESH.mkdir(exist_ok=True)
                    put_kesha.write_text(telo, encoding="utf-8")
                time.sleep(PAUZA)
            if kod != 200:
                break
            try:
                kusok = json.loads(telo)
            except ValueError:
                break
            if not isinstance(kusok, list) or not kusok:
                break
            # Часть магазинов на `page=2` отдаёт ту же страницу, что
            # и на первой: у Тривановића и Рубина оттого выходило по два
            # одинаковых товара. Повтор ловится по номеру товара — имени
            # мало: у Подрума Малча две «Crna Tamjanika» с разной ценой,
            # и это два разных товара, а не один дважды.
            novyh = [t for t in kusok if t.get("id") not in vidano]
            vidano.update(t.get("id") for t in kusok)
            vsego += novyh
            if len(kusok) < 100 or not novyh:
                break
            stranica += 1
        if vsego:
            return vsego, "est"
        if kod == 200:
            return [], "pusto"
    return [], "net-api" if kod else "ne-otvechaet"


def molchuny():
    """Кого прошлый обход не дозвался. Кеш хранит удачи, а неудачи —
    это две попытки по пятнадцать секунд на каждый из шести десятков
    мёртвых адресов, то есть минуты пустого ожидания при каждом
    перезапуске. Прошлая сводка их помнит, и по умолчанию они
    пропускаются; `--vse` заставляет обойти всех заново."""
    put = ZDES / "vinarije-ceny.json"
    if "--vse" in sys.argv or not put.exists():
        return set()
    try:
        d = json.loads(put.read_text(encoding="utf-8"))
    except ValueError:
        return set()
    return {s["sajt"] for s in d.get("po_hozyaistvam", [])
            if s.get("kak") == "ne-otvechaet"}


def main():
    tolko = next((a for a in sys.argv[1:] if not a.startswith("--")), "")
    pary = sajty()
    mimo = molchuny()
    spisok = [(a, i) for a, i in sorted(pary.items(), key=lambda p: p[1])
              if (not tolko or tolko.lower() in i.lower()) and a not in mimo]
    if mimo:
        print("пропущено молчунов прошлого обхода: %d (обойти всех — `--vse`)"
              % len(mimo))
    vina, svodka = [], []

    def odno(para):
        """Один магазин целиком. Возвращает записи вин и строку сводки."""
        adres, imya = para
        tovary, kak = tovary_hozyaistva(adres, imya)
        svoi = []
        for tovar in tovary:
            razdely = [html.unescape(k.get("name", ""))
                       for k in (tovar.get("categories") or [])]
            if NE_VINO.search(" ".join(razdely)):
                continue
            v_rsd, valyuta = cena(tovar)
            svoi.append({
                # Имя приходит с экранированными знаками — «Love&#038;Sunshine»,
                # «Filigran &#8211; Cabernet sauvignon». В таком виде оно
                # не сойдётся ни с нашим именем, ни глазами не прочтётся.
                "vino": imya_tovara(tovar.get("name")),
                "hozyaistvo": imya,
                "cena_rsd": v_rsd,
                "valyuta": valyuta,
                "v_prodazhe": bool(tovar.get("is_in_stock", True)),
                "razdel": "; ".join(razdely),
                "kanal": "hozyaistvo",
                "magazin": adres.replace("https://", ""),
                "stranica": tovar.get("permalink") or adres,
            })
        return svoi, {"hozyaistvo": imya, "sajt": adres, "kak": kak,
                      "tovarov": len(tovary), "vzyato": len(svoi)}

    # Хозяйства опрашиваются вперемешку: список чужой, мёртвых адресов
    # в нём больше, чем живых, и последовательный обход упирается в них
    # на часы. Каждый отдельный сайт при этом опрашивается по-прежнему
    # в один поток и с паузой между страницами.
    with concurrent.futures.ThreadPoolExecutor(POTOKOV) as bassejn:
        for nomer, (svoi, stroka) in enumerate(
                bassejn.map(odno, spisok), 1):
            vina += svoi
            svodka.append(stroka)
            print("%3d/%3d %-34s %-12s товаров %3d, вина %3d"
                  % (nomer, len(spisok), stroka["hozyaistvo"][:34],
                     stroka["kak"], stroka["tovarov"], stroka["vzyato"]))

    # Пропущенные молчуны остаются в сводке — иначе следующий обход
    # снова пойдёт их будить, и пропуск не работает второй раз.
    imena_po_adresu = {a: i for a, i in pary.items()}
    for adres in sorted(mimo):
        svodka.append({"hozyaistvo": imena_po_adresu.get(adres, adres),
                       "sajt": adres, "kak": "ne-otvechaet",
                       "tovarov": 0, "vzyato": 0})

    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "vinarije-ceny.json").write_text(json.dumps({
        "chto_eto": "Цены из собственных интернет-магазинов хозяйств. "
                    "Канал третий: не полка винотеки и не доставка, "
                    "а цена у самого производителя.",
        "istochnik": "WooCommerce Store API сайтов хозяйств; адреса — "
                     "из карточек хозяйств Vivino",
        "sobrano": time.strftime("%Y-%m-%d"),
        "hozyaistv_s_magazinom": sum(1 for s in svodka if s["vzyato"]),
        "po_hozyaistvam": svodka,
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nмагазин нашёлся у %d хозяйств; позиций %d, из них с ценой в динарах %d"
          " → vinarije-ceny.json"
          % (sum(1 for s in svodka if s["vzyato"]), len(vina), s_cenoj))


if __name__ == "__main__":
    main()
