#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка книги в живом браузере: что она делает, а не как размечена.

check.py стережёт разметку, эта проверка — поведение. Обе нужны: разметка
бывает безупречной, а панель не открывается.

    pip install playwright && playwright install chromium
    python3 _rabota/proverka-knigi.py

    CHROME=/путь/к/chrome python3 _rabota/proverka-knigi.py   # свой браузер
    python3 _rabota/proverka-knigi.py --бегло                 # без офлайна

Часть проверок требует настоящего сервера: служебный сценарий на file://
не работает. Скрипт поднимает его сам на свободном порту.

Код возврата 0 — всё чисто, 1 — есть отказы.
"""

import http.server
import os
import socketserver
import sys
import threading

KNIGA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "index.html"))
KOREN = os.path.dirname(KNIGA)
BRAUZER = os.environ.get("CHROME") or None

otkazy = []


def proverka(chto, uslovie, podrobno=""):
    znak = "✓" if uslovie else "✗"
    print("  %s %s%s" % (znak, chto, ("" if uslovie else "  — " + str(podrobno))))
    if not uslovie:
        otkazy.append(chto)
    return uslovie


def ostanovilas(pg):
    """Прокрутка плавная — ждём, пока встанет."""
    proshloe = None
    for _ in range(40):
        pg.wait_for_timeout(120)
        tek = pg.evaluate("Math.round(scrollY)")
        if tek == proshloe:
            return tek
        proshloe = tek
    return proshloe


def server():
    class Tihij(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=KOREN, **kw)
        def log_message(self, *a):
            pass
    s = socketserver.TCPServer(("127.0.0.1", 0), Tihij)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, "http://127.0.0.1:%d/" % s.server_address[1]


def glavy_i_prilozhenija(pg, adres):
    print("\nГлавы и приложения")
    pg.goto(adres); pg.wait_for_timeout(800)
    svernuty = pg.evaluate("[...document.querySelectorAll('details.place-det, details.part-det')].every(d => !d.open)")
    proverka("при открытии книги всё свёрнуто", svernuty)

    razdely = pg.evaluate("""() => [...document.querySelectorAll('details.place-det, details.part-det')]
        .map(d => d.closest('[id]').id)""")
    proverka("разделов на месте: 21", len(razdely) == 21, len(razdely))

    ploho = []
    for ide in razdely:
        z = pg.locator("#%s summary" % ide).first
        z.scroll_into_view_if_needed(); z.click(); pg.wait_for_timeout(120)
        otkr = pg.evaluate("i => document.querySelector('#'+i+' details').open", ide)
        pod = pg.evaluate("""i => [...document.querySelectorAll('#'+i+' details.sub-det')].every(d => !d.open)""", ide)
        z.click(); pg.wait_for_timeout(120)
        zakr = not pg.evaluate("i => document.querySelector('#'+i+' details').open", ide)
        if not (otkr and zakr and pod):
            ploho.append(ide)
    proverka("каждый раздел раскрывается и закрывается, подглавы внутри закрыты",
             not ploho, ", ".join(ploho))


def podskazki(pg, adres):
    print("\nПодсказки")
    pg.goto(adres); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    pg.wait_for_timeout(400)
    kljuchi = pg.evaluate("""() => [...document.querySelectorAll('.gpanel[popover]')].map(p => p.id.slice(3))""")
    proverka("панелей на месте: 64", len(kljuchi) == 64, len(kljuchi))

    ploho = []
    for k in kljuchi:
        knopka = pg.locator('button[popovertarget="gp-%s"]:not(.gp-x)' % k).first
        panel = pg.locator("#gp-%s" % k)
        try:
            knopka.scroll_into_view_if_needed()
            if panel.is_visible():
                ploho.append(k + " (видна до нажатия)"); continue
            knopka.click()
            try:
                panel.wait_for(state="visible", timeout=2000)
            except Exception:
                ploho.append(k + " (не открылась)"); continue
            pg.keyboard.press("Escape")
            try:
                panel.wait_for(state="hidden", timeout=2000)
            except Exception:
                ploho.append(k + " (не закрылась)")
        except Exception as oshibka:
            ploho.append(k + " (" + str(oshibka).split("\n")[0][:40] + ")")
    proverka("каждая открывается нажатием и закрывается по Esc", not ploho, "; ".join(ploho[:5]))

    knopka = pg.locator('button[popovertarget="gp-terroir"]:not(.gp-x)').first
    knopka.scroll_into_view_if_needed(); knopka.click(); pg.wait_for_timeout(300)
    pg.locator("#gp-terroir button.gp-x").click(); pg.wait_for_timeout(300)
    proverka("крестик закрывает", not pg.locator("#gp-terroir").is_visible())
    knopka.click(); pg.wait_for_timeout(300)
    pg.mouse.click(3, 3); pg.wait_for_timeout(300)
    proverka("нажатие вне панели закрывает", not pg.locator("#gp-terroir").is_visible())


def soderzhanie(pg, adres):
    print("\nСодержание и полоса")
    pg.goto(adres); pg.wait_for_timeout(800)
    pg.evaluate("scrollTo(0, 3000)"); ostanovilas(pg)
    proverka("полоса держится сверху при прокрутке",
             pg.evaluate("Math.round(document.querySelector('.topbar').getBoundingClientRect().top)") == 0)
    pg.locator(".topbar-b").click(); pg.wait_for_timeout(600)
    proverka("содержание открывается", pg.locator("#menju").is_visible())
    bitye = pg.evaluate("""() => [...document.querySelectorAll('#menju a')]
        .map(a => a.getAttribute('href').slice(1))
        .filter(i => !document.getElementById(i))""")
    proverka("все пункты ведут в существующие места", not bitye, bitye)
    # содержание не должно отставать от книги
    zabytye = pg.evaluate("""() => {
        const v_menju = new Set([...document.querySelectorAll('#menju a')]
            .map(a => a.getAttribute('href').slice(1)));
        const razdely = [...document.querySelectorAll('section.place, section.part')].map(e => e.id);
        const podglavy = [...document.querySelectorAll('h3.sub-h[id]')].map(e => e.id);
        return [...razdely, ...podglavy].filter(i => !v_menju.has(i));}""")
    proverka("в содержании есть всё, что есть в книге", not zabytye, zabytye)
    pg.locator('#menju a[href="#et-marka"]').click(); ostanovilas(pg)
    proverka("пункт раскрывает и раздел, и подглаву в нём", pg.evaluate("""() => {
        const h = document.getElementById('et-marka');
        return h.closest('details.sub-det').open && h.closest('details.part-det').open;}"""))
    proverka("заголовок не уехал под полосу", pg.evaluate("""() => {
        const h = document.getElementById('et-marka').getBoundingClientRect();
        const t = document.querySelector('.topbar').getBoundingClientRect();
        return h.top >= t.bottom - 1;}"""))
    proverka("адрес показывает подглаву", pg.evaluate("location.hash") == "#et-marka",
             pg.evaluate("location.hash"))


def strelka_i_adres(pg, adres):
    print("\nСтрелка и адрес")
    pg.goto(adres); ostanovilas(pg)
    z = pg.locator("#negotin summary"); z.scroll_into_view_if_needed(); z.click(); ostanovilas(pg)
    proverka("раскрытая нажатием глава попадает в адрес",
             pg.evaluate("location.hash") == "#negotin", pg.evaluate("location.hash"))
    pg.reload(); ostanovilas(pg)
    proverka("после обновления глава раскрыта",
             pg.evaluate("document.querySelector('#negotin details').open"))
    pg.evaluate("scrollBy(0, 2500)"); ostanovilas(pg)
    pg.locator(".ctl .btn").click(); ostanovilas(pg)
    proverka("стрелка приводит к заголовку главы", pg.evaluate("""() => {
        const z = document.querySelector('#negotin summary').getBoundingClientRect();
        return z.top > 30 && z.top < 120;}"""))
    pg.locator(".ctl .btn").click(); ostanovilas(pg)
    proverka("следующая стрелка — в начало книги", pg.evaluate("scrollY") < 60,
             pg.evaluate("Math.round(scrollY)"))
    proverka("адрес отпущен", pg.evaluate("location.hash") == "",
             repr(pg.evaluate("location.hash")))


def karta(pg, adres):
    print("\nКарта")
    pg.goto(adres); pg.wait_for_timeout(800)
    imena = pg.evaluate("""() => [...document.querySelectorAll('.map a')]
        .filter(a => a.getAttribute('aria-hidden') !== 'true')
        .map(a => a.getAttribute('aria-label'))""")
    proverka("десять областей, и каждая названа", len(imena) == 10 and all(imena), imena)
    proverka("в обходе клавиатурой только они",
             pg.evaluate("""() => [...document.querySelectorAll('.map a')]
                 .filter(a => a.getAttribute('tabindex') !== '-1').length""") == 10)
    pg.evaluate("""() => document.querySelector('.map a.rg[href="#toplica"]')
        .dispatchEvent(new MouseEvent('click', {bubbles: true}))""")
    ostanovilas(pg)
    proverka("нажатие по области раскрывает главу",
             pg.evaluate("document.querySelector('#toplica details').open"))


def shrifty(pg, adres):
    print("\nШрифты")
    pg.goto(adres); pg.wait_for_timeout(1200)
    # курсив браузер тянет, только когда курсивный текст показан
    pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    pg.wait_for_timeout(700)
    sostoyanie = pg.evaluate("""async () => { await document.fonts.ready;
        return {tekst: document.fonts.check('400 17px Literata'),
                zhirnyj: document.fonts.check('700 17px Literata'),
                kursiv: document.fonts.check('italic 400 17px Literata'),
                zagolovok: document.fonts.check('800 40px Alegreya'),
                podpis: document.fonts.check('600 10px "IBM Plex Mono"')};}""")
    for chto, est in sostoyanie.items():
        proverka("применяется: " + chto, est)


def tema(b, adres):
    print("\nТема")
    for sistema, dolzhno in (("light", "светлая"), ("dark", "тёмная")):
        ctx = b.new_context(viewport={"width": 390, "height": 844}, color_scheme=sistema)
        pg = ctx.new_page(); pg.goto(adres); pg.wait_for_timeout(700)
        kak = lambda: ("тёмная" if pg.evaluate(
            "getComputedStyle(document.querySelector('.wrap')).getPropertyValue('--paper').trim()") == "#191E21"
            else "светлая")
        proverka("система %s → книга %s" % (sistema, dolzhno), kak() == dolzhno, kak())
        pg.locator(".themebtn").click(); pg.wait_for_timeout(400)
        naoborot = "светлая" if dolzhno == "тёмная" else "тёмная"
        proverka("  переключатель даёт %s" % naoborot, kak() == naoborot, kak())
        pg.reload(); pg.wait_for_timeout(700)
        proverka("  выбор пережил перезагрузку", kak() == naoborot, kak())
        ctx.close()


def bez_scenariev(b, adres):
    print("\nБез сценариев")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False)
    pg = ctx.new_page(); pg.goto(adres); pg.wait_for_timeout(600)
    z = pg.locator("#fruska summary"); z.scroll_into_view_if_needed(); z.click(); pg.wait_for_timeout(300)
    proverka("глава раскрывается нажатием", pg.evaluate("document.querySelector('#fruska details').open"))
    k = pg.locator('button[popovertarget="gp-terroir"]:not(.gp-x)').first
    k.scroll_into_view_if_needed(); k.click(); pg.wait_for_timeout(400)
    proverka("подсказка открывается", pg.locator("#gp-terroir").is_visible())
    pg.locator(".topbar-b").click(); pg.wait_for_timeout(400)
    proverka("содержание открывается", pg.locator("#menju").is_visible())
    ctx.close()


def pechat(b, adres):
    print("\nПечать")
    ctx = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False)
    pg = ctx.new_page(); pg.emulate_media(media="print")
    pg.goto(adres); pg.wait_for_timeout(900)
    nizkie = pg.evaluate("""() => [...document.querySelectorAll('.place-body, .part-body')]
        .filter(e => e.getBoundingClientRect().height < 200)
        .map(e => (e.closest('[id]')||{}).id)""")
    proverka("все разделы выводятся раскрытыми", not nizkie, nizkie)
    proverka("полоса и содержание не печатаются", pg.evaluate("""() =>
        getComputedStyle(document.querySelector('.topbar')).display === 'none'"""))
    ctx.close()


def raskladka(b, adres):
    print("\nРаскладка")
    for shirina in (320, 390, 768, 1440):
        ctx = b.new_context(viewport={"width": shirina, "height": 900})
        pg = ctx.new_page(); pg.goto(adres); pg.wait_for_timeout(900)
        vbok = pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 1")
        proverka("на %d px страница не едет вбок" % shirina, not vbok)
        d = pg.evaluate("""() => {const t = document.querySelector('.mtx'), h = document.querySelector('.mhint');
            return {prokrutka: t.scrollWidth > t.clientWidth + 1,
                    preduprezhdenie: getComputedStyle(h).display !== 'none'};}""")
        proverka("  таблица: прокрутка и предупреждение вместе",
                 d["prokrutka"] == d["preduprezhdenie"], d)
        ctx.close()


def oflajn(b, adres):
    print("\nЧтение без сети")
    ctx = b.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page(); pg.goto(adres); pg.wait_for_timeout(3500)
    proverka("копия книги отложена", pg.evaluate("""async () => {
        const h = await caches.open('terruary'); return (await h.keys()).length;}""") >= 10)
    ctx.set_offline(True)
    pg.goto(adres); pg.wait_for_timeout(1800)
    proverka("без сети книга открывается", pg.evaluate("!!document.querySelector('.title')"))
    proverka("  со шрифтами", pg.evaluate("""async () => { await document.fonts.ready;
        return document.fonts.check('400 17px Literata');}"""))
    proverka("  с картой и подсказками", pg.evaluate("""() =>
        !!document.querySelector('.map') && document.querySelectorAll('.gpanel').length === 64"""))
    ctx.set_offline(False)
    ctx.close()


def main():
    beglo = "--бегло" in sys.argv
    from playwright.sync_api import sync_playwright

    s, adres = server()
    print("книга: %s\nсервер: %s" % (KNIGA, adres))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=BRAUZER)
        pg = b.new_page(viewport={"width": 390, "height": 844})
        glavy_i_prilozhenija(pg, adres)
        podskazki(pg, adres)
        soderzhanie(pg, adres)
        strelka_i_adres(pg, adres)
        karta(pg, adres)
        shrifty(pg, adres)
        pg.close()
        tema(b, adres)
        bez_scenariev(b, adres)
        pechat(b, adres)
        raskladka(b, adres)
        if not beglo:
            oflajn(b, adres)
        b.close()
    s.shutdown()

    print()
    if otkazy:
        print("Отказов: %d" % len(otkazy))
        for o in otkazy:
            print("  ✗ " + o)
        sys.exit(1)
    print("Всё чисто. Проверено поведение, не текст: читать книгу всё равно приходится.")


if __name__ == "__main__":
    main()
