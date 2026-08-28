# -*- coding: utf-8 -*-
"""Gilbert & Gaillard: сербские вина со стобалльными оценками.

Французский гид, судят вслепую и ставят балл по стобалльной шкале —
это оценка критика, а не медаль, и идёт она в дорожку оценок.

Сербских вин у гида немного, но дорожка независимая: ни Decanter,
ни Falstaff этих вин не оценивали.

Страница результатов собирается Livewire, то есть список приходит
отдельным запросом. Поэтому сперва берётся сама страница — ради сессии,
токена и «отпечатка» составной части, — а потом список запрашивается
её же средствами. Браузер для этого не нужен.

    python3 _rabota/rejtingi/vzjat-gilbert-gaillard.py

Пишет `gilbert-gaillard-zapisi.json`.
"""
import json, os, re, html, urllib.error, urllib.parse, urllib.request
import http.cookiejar

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
STRANICA = "https://www.gilbertgaillard.com/en/resultats"
SOOBSHCHENIE = "https://www.gilbertgaillard.com/livewire/message/search-results"
SERBIYA = "44"          # номер Сербии в справочнике гида
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Карточка вина: ссылка с номером, хозяйство, имя с урожаем, категория, балл.
KARTOCHKA = re.compile(
    r'<a href="(?P<adres>[^"]*?/resultats/[^"]+?-(?P<nomer>\d+))">.*?'
    r'<div class="name">.*?</span>(?P<hozyaistvo>.*?)</div>.*?'
    r'<div class="info">\s*<span[^>]*></span>\s*(?P<vino>.*?)</div>.*?'
    r'<div class="info"><span[^>]*></span>(?P<kategoriya>.*?)</div>'
    r'(?:.*?<div class="wine__points">\s*<p>(?P<ball>\d+)</p>)?', re.S)


def chisto(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def otkryvatel():
    banka = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(banka))


def main():
    otkryt = otkryvatel()
    zapros = urllib.request.Request(STRANICA, headers={
        "User-Agent": BRAUZER, "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9"})
    stranica = otkryt.open(zapros, timeout=60).read().decode("utf-8", "replace")

    token = re.search(r'name="csrf-token"\s*content="([^"]+)"', stranica).group(1)
    chasti = [json.loads(html.unescape(x))
              for x in re.findall(r'wire:initial-data="([^"]+)"', stranica)]
    spisok = [c for c in chasti
              if c["fingerprint"]["name"] == "search-results"][0]

    telo = json.dumps({
        "fingerprint": spisok["fingerprint"],
        "serverMemo": spisok["serverMemo"],
        "updates": [{"type": "syncInput",
                     "payload": {"id": "a1", "name": "filters.country",
                                 "value": SERBIYA}}],
    }).encode()
    zapros = urllib.request.Request(SOOBSHCHENIE, data=telo, headers={
        "User-Agent": BRAUZER, "Content-Type": "application/json",
        "X-CSRF-TOKEN": token, "X-Livewire": "true", "Referer": STRANICA})
    otvet = json.loads(otkryt.open(zapros, timeout=60).read().decode())
    razmetka = (otvet.get("effects") or {}).get("html") or ""

    skolko = re.search(r'class="number">(\d+)\s+wines', razmetka)
    zapisi = []
    for m in KARTOCHKA.finditer(razmetka):
        imya = chisto(m.group("vino"))
        urozhaj = None
        sovpalo = re.search(r"\b(\d{4})\s*$", imya)
        if sovpalo:
            urozhaj = int(sovpalo.group(1))
            imya = imya[:sovpalo.start()].strip()
        zapisi.append({
            "nomer": m.group("nomer"),
            "hozyaistvo": chisto(m.group("hozyaistvo")),
            "vino": imya,
            "urozhaj": urozhaj,
            "ball": int(m.group("ball")) if m.group("ball") else None,
            "kategoriya": chisto(m.group("kategoriya")),
            "stranica": m.group("adres"),
        })
    json.dump({
        "chto_eto": "Сербские вина в гиде Gilbert & Gaillard: балл по стобалльной "
                    "шкале, то есть оценка критика, а не медаль.",
        "istochnik": STRANICA,
        "strana_v_spravochnike": SERBIYA,
        "obeshchano": int(skolko.group(1)) if skolko else None,
        "vsego": len(zapisi),
        "zapisi": zapisi,
    }, open(put("gilbert-gaillard-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("обещано %s, разобрано %d → gilbert-gaillard-zapisi.json"
          % (skolko.group(1) if skolko else "?", len(zapisi)))
    for z in zapisi:
        print("   %-16s %-28s %s  %s" % (z["hozyaistvo"], z["vino"],
                                         z["urozhaj"] or "—", z["ball"]))


if __name__ == "__main__":
    main()
