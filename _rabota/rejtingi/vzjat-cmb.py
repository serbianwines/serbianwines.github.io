# -*- coding: utf-8 -*-
"""Concours Mondial de Bruxelles: сербские медали.

CMB — крупный международный конкурс, результаты открыты и фильтруются
по стране прямо в адресе. Сербских вин у него мало: за все годы считанные
единицы, — но это независимая дорожка, и брать её дёшево.

Медали CMB: Grand Gold, Gold, Silver. Балла конкурс не публикует, поэтому
записи идут в награды.

    python3 _rabota/rejtingi/vzjat-cmb.py

Пишет `cmb-zapisi.json`, страницы кладёт в `kesh-cmb/`.
"""
import json, os, re, html, time, urllib.error, urllib.request

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)
KESH = put("kesh-cmb")
SPISOK = ("https://results.concoursmondial.com/en/results/%d"
          "?search%%5Bcountry%%5D=Serbia&page=%d")
# У конкурса результаты выложены с 2010 года. Сбор начинался с 2012-го,
# и две сербские медали 2011 года — оба серебра Подрума Радовановић —
# в него не попадали. За 2010-й сербских вин нет.
GODY = range(2010, 2027)
BRAUZER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
SSYLKA = re.compile(r'href="(?:https://results\.concoursmondial\.com)?'
                    r'(/en/results/(\d{4})/(\d+)-[a-z0-9\-]*)"')


def vzjat(adres, imya):
    fajl = os.path.join(KESH, imya)
    if os.path.exists(fajl):
        return open(fajl, encoding="utf-8").read()
    zapros = urllib.request.Request(adres, headers={
        "User-Agent": BRAUZER, "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(zapros, timeout=60) as otvet:
        tekst = otvet.read().decode("utf-8", "replace")
    os.makedirs(KESH, exist_ok=True)
    open(fajl, "w", encoding="utf-8").write(tekst)
    time.sleep(1.2)
    return tekst


def chisto(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def razobrat(stranica, god):
    """Карточки результатов: имя с урожаем, хозяйство, страна, медаль."""
    # Резать надо после закрывающей скобки тега, иначе сам адрес ссылки
    # попадает в текст карточки и садится в имя вина.
    mesta = []
    for m in SSYLKA.finditer(stranica):
        if m.group(2) != str(god):
            continue
        posle = stranica.find(">", m.end())
        mesta.append((m.start(), posle + 1 if posle > 0 else m.end(),
                      m.group(1), m.group(3)))
    zapisi = []
    for i, (metka, nachalo, adres, nomer) in enumerate(mesta):
        konec = mesta[i + 1][0] if i + 1 < len(mesta) else len(stranica)
        tekst = chisto(stranica[nachalo:konec])
        medal = re.search(r"(Grand Gold|Gold|Silver|Bronze)\s+Medal", tekst)
        # Текст карточки идёт «Имя вина 2019 Хозяйство Serbia … Gold Medal»
        do_medali = tekst[:medal.start()] if medal else tekst
        chasti = [c.strip() for c in do_medali.split("Serbia") if c.strip()]
        imya_i_hoz = chasti[0] if chasti else ""
        sovpalo = re.search(r"^(.*?\b(\d{4})\b)\s+(.+)$", imya_i_hoz)
        if sovpalo:
            vino, urozhaj, hozyaistvo = (sovpalo.group(1).strip(),
                                         int(sovpalo.group(2)),
                                         sovpalo.group(3).strip())
            vino = re.sub(r"\s*\b%d\b\s*$" % urozhaj, "", vino).strip()
        else:
            vino, urozhaj, hozyaistvo = imya_i_hoz, None, ""
        zapisi.append({
            "god": god, "nomer": nomer,
            "hozyaistvo": hozyaistvo, "vino": vino, "urozhaj": urozhaj,
            "medal": medal.group(1) if medal else None,
            "stranica": "results.concoursmondial.com" + adres,
        })
    return zapisi


def god_celikom(god):
    """Все страницы года, а не только первая.

    Адрес принимает номер страницы, и сбор его подставлял — но всегда
    единицу. Сербских вин у конкурса мало, и до второй страницы дело
    пока не доходило; но код при этом делал вид, что листает, а год
    с длинной выдачей обрезался бы молча.
    """
    najdeno, vidano = [], set()
    for nomer in range(1, 21):
        imya = "cmb-%d%s.html" % (god, "" if nomer == 1 else "-%d" % nomer)
        stranica = vzjat(SPISOK % (god, nomer), imya)
        svezhee = [z for z in razobrat(stranica, god)
                   if z["nomer"] not in vidano]
        if not svezhee:
            return najdeno
        vidano.update(z["nomer"] for z in svezhee)
        najdeno += svezhee
    print("  CMB %d: страниц больше двадцати — проверить вручную" % god)
    return najdeno


def main():
    vse = []
    for god in GODY:
        najdeno = god_celikom(god)
        if najdeno:
            print("  CMB %d: %d" % (god, len(najdeno)))
        vse += najdeno
    json.dump({
        "chto_eto": "Сербские вина, отмеченные на Concours Mondial de Bruxelles. "
                    "Конкурс ставит медали, а не баллы — это награды, не оценки.",
        "istochnik": "results.concoursmondial.com",
        "vsego": len(vse),
        "zapisi": vse,
    }, open(put("cmb-zapisi.json"), "w", encoding="utf-8"),
        ensure_ascii=False, indent=1)
    print("всего записей: %d → cmb-zapisi.json" % len(vse))


if __name__ == "__main__":
    main()
