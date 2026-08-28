# -*- coding: utf-8 -*-
"""Адреса хозяйств со страниц Vivino.

Листинг сербских винарий даёт только имя, слаг и номер. Сама страница
хозяйства отдаёт в SSR-пропсах объект address: улица, город, индекс,
а рядом сайт, телефон и почту. Город — то, чего не хватало, чтобы
поставить рејон тем, кого Vivino сваливает в «Central Serbia».

Складывает по файлу на хозяйство в kesh-vivino-adresa/. Уже скачанное
не перекачивает.
"""
import json, re, html, sys, time, pathlib, urllib.request, urllib.error

ZDES = pathlib.Path(__file__).resolve().parent
KESH = ZDES / "kesh-vivino-adresa"
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def slagi():
    """Слаг и номер каждой винарии из скачанного листинга."""
    tekst = "".join(f.read_text(encoding="utf-8")
                    for f in sorted((ZDES / "kesh-vivino").glob("listing-*.html")))
    kartochki = re.findall(
        r'href="/en/wineries/([^"]+)"[^>]*data-mp-entity-id="(\d+)" '
        r'data-mp-entity-name="([^"]*)"', tekst)
    vyshlo = {}
    for slag, nomer, imya in kartochki:
        vyshlo[slag] = {"slug": slag, "vivino_id": int(nomer), "imya": html.unescape(imya)}
    return vyshlo


def vzjat(slag):
    adres = f"https://www.vivino.com/wineries/{slag}"
    zapros = urllib.request.Request(adres, headers={
        "User-Agent": BRAUZER,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(zapros, timeout=45) as otvet:
        return otvet.read().decode("utf-8", "replace")


def razobrat(stranica):
    """Вытащить объект winery из data-ssr-props."""
    metka = 'data-ssr-component="WineryPage" data-ssr-props="'
    nachalo = stranica.find(metka)
    if nachalo < 0:
        return None
    nachalo += len(metka)
    konec = stranica.find('">', nachalo)
    syroe = html.unescape(stranica[nachalo:konec])
    # За закрывающей кавычкой атрибута идёт следующий такой же блок,
    # поэтому берём первый объект, а хвост отбрасываем.
    try:
        dannye, _ = json.JSONDecoder().raw_decode(syroe)
    except json.JSONDecodeError:
        return None
    return dannye.get("winery")


def szhat(vinarija):
    """Оставить то, что нужно для места, и выбросить остальное."""
    adres = vinarija.get("address") or {}
    strana = (adres.get("country") or {}).get("code")
    return {
        "vivino_id": vinarija.get("id"),
        "imya": vinarija.get("name"),
        "slug": vinarija.get("seo_name"),
        "ulica": (adres.get("street") or "").strip(),
        "ulica2": (adres.get("street2") or "").strip(),
        "gorod": (adres.get("city") or "").strip(),
        "indeks": (adres.get("zip") or "").strip(),
        "strana": strana,
        "region_vivino": (vinarija.get("region") or {}).get("name")
                         if isinstance(vinarija.get("region"), dict) else None,
        "sajt": vinarija.get("website") or "",
        "telefon": vinarija.get("phone") or "",
        "pochta": vinarija.get("email") or "",
        "vin": (vinarija.get("statistics") or {}).get("wines_count"),
        "otzyvov": (vinarija.get("statistics") or {}).get("ratings_count"),
        "ocenka": (vinarija.get("statistics") or {}).get("ratings_average"),
    }


def main():
    tolko = sys.argv[1:] or None
    spisok = slagi()
    KESH.mkdir(exist_ok=True)
    vzjato = propushcheno = bedy = 0
    for slag, karta in sorted(spisok.items()):
        if tolko and slag not in tolko:
            continue
        fajl = KESH / f"{slag}.json"
        if fajl.exists():
            propushcheno += 1
            continue
        try:
            stranica = vzjat(slag)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as beda:
            print(f"  не открылось: {slag} — {beda}")
            bedy += 1
            time.sleep(3)
            continue
        vinarija = razobrat(stranica)
        if vinarija is None:
            print(f"  не разобралось: {slag}")
            bedy += 1
            time.sleep(1.5)
            continue
        zapis = szhat(vinarija)
        zapis["imya_listinga"] = karta["imya"]
        fajl.write_text(json.dumps(zapis, ensure_ascii=False, indent=1), encoding="utf-8")
        vzjato += 1
        if vzjato % 25 == 0:
            print(f"  взято {vzjato}")
        time.sleep(1.2)
    print(f"взято {vzjato}, было {propushcheno}, не вышло {bedy}")


if __name__ == "__main__":
    main()
