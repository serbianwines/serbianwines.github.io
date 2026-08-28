# -*- coding: utf-8 -*-
"""Поиск на Vivino тех производителей, которых нет в сербском листинге.

Листинг Vivino отдаёт 433 сербских хозяйства и на этом кончается —
девятнадцатая страница пуста. Но сам Vivino в карточке страны пишет,
что винарий у него 455. Разница — хозяйства, которые он считает, но
в листинге не показывает: так у нас едва не потерялся Lakićević.

Проверка идёт от Винарског регистра: берутся производители, которых
в наших таблицах нет, и каждый ищется на Vivino поиском по хозяйствам.
Найденный слаг, которого нет в листинге, — потеря сбора.

    python3 _rabota/rejtingi/poiskat-vivino.py

Пишет `poisk-vivino.json`. Уже проверенные запросы не перезапрашивает.
"""
import json, os, re, sys, time, unicodedata, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
POISK = "https://www.vivino.com/search/wineries?q=%s"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
SLUZHEBNYE_SLUGI = {"countries", "regions", "backgrounds"}


def prosto(s):
    s = (s or "").lower().replace("dj", "đ")
    for a, b in (("š", "s"), ("đ", "d"), ("č", "c"), ("ć", "c"), ("ž", "z")):
        s = s.replace(a, b)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(z for z in s if not unicodedata.combining(z))
    return re.sub(r"[^a-z0-9]+", " ", s).split()


def iz_listinga():
    """Слаги, которые листинг уже отдал."""
    import glob
    tekst = "".join(open(f, encoding="utf-8").read()
                    for f in sorted(glob.glob(put("kesh-vivino/listing-*.html"))))
    return set(re.findall(r'href="/en/wineries/([a-z0-9\-]+)"', tekst))


def najti(zapros):
    adres = POISK % urllib.parse.quote(zapros)
    zapr = urllib.request.Request(adres, headers={
        "User-Agent": BRAUZER, "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(zapr, timeout=45) as otvet:
        stranica = otvet.read().decode("utf-8", "replace")
    slugi = [s for s in dict.fromkeys(re.findall(r'/wineries/([a-z0-9\-]+)', stranica))
             if s not in SLUZHEBNYE_SLUGI]
    return slugi


def main():
    import urllib.parse
    zaprosy = json.load(open(put("zaprosy-registra.json"), encoding="utf-8"))
    listing = iz_listinga()
    itog = {}
    if os.path.exists(put("poisk-vivino.json")):
        itog = json.load(open(put("poisk-vivino.json"), encoding="utf-8"))["zaprosy"]
    novoe = 0
    for zapros, zapisi in sorted(zaprosy.items()):
        if zapros in itog:
            continue
        try:
            slugi = najti(zapros)
        except urllib.error.HTTPError as beda:
            # 404 у поиска Vivino значит «ничего не нашлось», а не поломку.
            if beda.code != 404:
                sys.stderr.write("  %s: %s\n" % (zapros, beda))
                time.sleep(4)
                continue
            slugi = []
        except (urllib.error.URLError, OSError) as beda:
            sys.stderr.write("  %s: %s\n" % (zapros, beda))
            time.sleep(4)
            continue
        # Ответ поиска нестрогий: он вернёт что угодно похожее. Оставляем
        # только те слаги, в которых есть слово запроса, — иначе к каждой
        # винарии припишется случайная.
        slova = [w for w in prosto(zapros) if len(w) > 3]
        podhodyat = [s for s in slugi
                     if any(w in s.replace("-", "") for w in slova)]
        itog[zapros] = {
            "zapisi_registra": zapisi,
            "nashlos": slugi[:8],
            "podhodyat": podhodyat,
            "vne_listinga": [s for s in podhodyat if s not in listing],
        }
        novoe += 1
        if novoe % 20 == 0:
            print("  запросов сделано: %d" % novoe)
            json.dump({"chto_eto": "Поиск Vivino по производителям из регистра, "
                                   "которых нет в наших таблицах.",
                       "zaprosy": itog},
                      open(put("poisk-vivino.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
        time.sleep(1.5)
    json.dump({"chto_eto": "Поиск Vivino по производителям из регистра, "
                           "которых нет в наших таблицах.",
               "zaprosy": itog},
              open(put("poisk-vivino.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    vne = {s for z in itog.values() for s in z["vne_listinga"]}
    print("запросов: %d, из них что-то подошло: %d, слагов вне листинга: %d"
          % (len(itog), sum(1 for z in itog.values() if z["podhodyat"]), len(vne)))
    for s in sorted(vne):
        print("   ", s)


if __name__ == "__main__":
    import urllib.parse
    main()
