# -*- coding: utf-8 -*-
"""Berliner / Asia / Portugal Wine Trophy: сербские вина.

Три конкурса одного устроителя (Deutsche Wein Marketing) с общей базой
результатов на results.wine-trophy.com. Сербских вин там немного —
два десятка, — но это независимая дорожка медалей.

**Сайт не досылает промежуточный сертификат.** Из-за этого запрос падает
с «unable to verify the first certificate», и это легко принять за запрет
среды. Проверку отключать не надо: недостающий промежуточный лежит по
адресу из самого сертификата (расширение AIA) и добирается отдельно —
цепочка проверяется целиком, просто мы досылаем то, чего не шлёт сервер.

    python3 _rabota/rejtingi/vzjat-wine-trophy.py

Пишет `wine-trophy-zapisi.json`, страницы кладёт в `kesh-wine-trophy/`.
"""
import json, os, re, html, ssl, time, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-wine-trophy")
SPISOK = "https://results.wine-trophy.com/en?sf=cultivation_country:Serbia"
# Страница показывает десять карточек за раз, а всего сербских вин
# два десятка. Пагинации в разметке нет, зато есть фасет года, и в каждом
# году сербских вин меньше десяти — значит, обходим по годам.
PO_GODU = SPISOK + "&sf=trophy_year:%d"
GODY = range(2009, 2027)
PROMEZHUTOCHNYJ = "https://cacerts.digicert.com/ThawteTLSRSACAG1.crt"
SVOJ_CA = "/root/.ccr/ca-bundle.crt"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

KARTOCHKA = re.compile(
    r'<h3><a href="(?P<adres>/en/wine/[^"]+)">(?P<vino>[^<]*)</a></h3>.*?'
    r'<div>Producer:\s*(?P<hozyaistvo>.*?)</div>.*?'
    r'(?:<div>Origin:\s*(?P<mesto>.*?)</div>.*?)?'
    r'(?:<div>Grape varieties:\s*(?P<sorta>.*?)</div>.*?)?'
    r'<div class="award">Award:\s*(?P<nagrada>.*?)</div>', re.S)


def sreda():
    """Проверка сертификатов с досланным промежуточным."""
    put_ca = os.path.join(KESH, "bundle.pem")
    os.makedirs(KESH, exist_ok=True)
    if not os.path.exists(put_ca):
        zapros = urllib.request.Request(PROMEZHUTOCHNYJ,
                                        headers={"User-Agent": BRAUZER})
        der = urllib.request.urlopen(zapros, timeout=45).read()
        pem = ssl.DER_cert_to_PEM_cert(der)
        with open(put_ca, "w", encoding="utf-8") as f:
            f.write(open(SVOJ_CA, encoding="utf-8").read())
            f.write("\n" + pem)
    return ssl.create_default_context(cafile=put_ca)


def chisto(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def vzjat(adres, imya, kontekst):
    fajl = os.path.join(KESH, imya)
    if os.path.exists(fajl):
        return open(fajl, encoding="utf-8").read()
    zapros = urllib.request.Request(adres, headers={
        "User-Agent": BRAUZER, "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(zapros, timeout=60, context=kontekst) as o:
        stranica = o.read().decode("utf-8", "replace")
    open(fajl, "w", encoding="utf-8").write(stranica)
    time.sleep(1.0)
    return stranica


def razobrat(stranica, god=None):
    zapisi = []
    for m in KARTOCHKA.finditer(stranica):
        nagrada = chisto(m.group("nagrada"))
        razbor = re.match(r"(?P<medal>.*?)\s+-\s+(?P<konkurs>.*?)\s+(?P<god>\d{4})$",
                          nagrada)
        urozhaj = re.search(r"_(\d{4})(?:\?|$)", m.group("adres"))
        zapisi.append({
            "god": int(razbor.group("god")) if razbor else god,
            "konkurs": razbor.group("konkurs") if razbor else "",
            "medal": razbor.group("medal").lower() if razbor else None,
            "hozyaistvo": chisto(m.group("hozyaistvo")),
            "vino": chisto(m.group("vino")),
            "urozhaj": int(urozhaj.group(1)) if urozhaj else None,
            "sorta": chisto(m.group("sorta")),
            "mesto": chisto(m.group("mesto")),
            "stranica": "results.wine-trophy.com" + m.group("adres").split("?")[0],
        })
    return zapisi


def main():
    kontekst = sreda()
    obshchaya = vzjat(SPISOK, "serbia.html", kontekst)
    obeshchano = re.search(r"(\d+)\s+results", obshchaya)
    gody = sorted({int(g) for g in
                   re.findall(r"trophy_year:(\d{4})\"", obshchaya)}) or list(GODY)

    po_klyuchu = {}
    for god in gody:
        stranica = vzjat(PO_GODU % god, "serbia-%d.html" % god, kontekst)
        for z in razobrat(stranica, god):
            po_klyuchu[z["stranica"]] = z
    zapisi = list(po_klyuchu.values())

    json.dump({
        "chto_eto": "Сербские вина Berliner, Asia и Portugal Wine Trophy. "
                    "Конкурсы ставят медали, балла не публикуют.",
        "istochnik": SPISOK,
        "obeshchano": int(obeshchano.group(1)) if obeshchano else None,
        "vsego": len(zapisi),
        "zapisi": sorted(zapisi, key=lambda z: (-(z["god"] or 0), z["hozyaistvo"])),
    }, open(put("wine-trophy-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("обещано %s, разобрано %d → wine-trophy-zapisi.json"
          % (obeshchano.group(1) if obeshchano else "?", len(zapisi)))
    for z in sorted(zapisi, key=lambda z: (-(z["god"] or 0), z["hozyaistvo"])):
        print("   %s %-8s %-28s %-32s %s" % (z["god"], z["medal"],
                                             z["hozyaistvo"][:28], z["vino"][:32],
                                             z["konkurs"]))


if __name__ == "__main__":
    main()
