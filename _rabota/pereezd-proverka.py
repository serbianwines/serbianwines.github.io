"""Подсказки в живом браузере: открываются, закрываются, старый механизм цел.

Нужен playwright: pip install playwright. Путь к браузеру задаётся
переменной среды CHROME, если он лежит не там, где playwright ищет сам.

    python3 _rabota/pereezd-proverka.py terroir eruptiv normirov

Проверяется по каждой подсказке: до нажатия панель скрыта, после — открыта
и в верхнем слое, плавающие кнопки спрятаны, панель закрывается Esc,
крестиком и нажатием вне. Отдельно — что подсказки на радиокнопках,
которые ещё не переехали, работают по-прежнему.
"""
import os, sys, json
from playwright.sync_api import sync_playwright

FILE = "file://" + os.path.abspath(os.environ.get("KNIGA", "index.html"))
kljuchi = sys.argv[1:]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROME") or None)
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(FILE)
    pg.evaluate("document.querySelectorAll('.op-in').forEach(c => c.checked = true); document.querySelectorAll('details').forEach(d => d.open = true)")
    pg.wait_for_timeout(300)
    itog = []
    for k in kljuchi:
        try:
            knopka = pg.locator('button[popovertarget="gp-%s"]:not(.gp-x)' % k).first
            panel = pg.locator("#gp-%s" % k)
            knopka.scroll_into_view_if_needed()
            r = {"kljuch": k, "do": panel.is_visible()}
            knopka.click(); pg.wait_for_timeout(350)
            r["otkrylas"] = panel.is_visible()
            r["verhnij_sloj"] = pg.evaluate("k => document.getElementById('gp-'+k).matches(':popover-open')", k)
            r["ctl_skryt"] = pg.evaluate("getComputedStyle(document.querySelector('.ctl')).opacity") == "0"
            pg.keyboard.press("Escape"); pg.wait_for_timeout(350)
            r["esc"] = not panel.is_visible()
            knopka.click(); pg.wait_for_timeout(300)
            pg.locator("#gp-%s button.gp-x" % k).click(); pg.wait_for_timeout(300)
            r["krest"] = not panel.is_visible()
            knopka.click(); pg.wait_for_timeout(300)
            pg.mouse.click(3, 3); pg.wait_for_timeout(300)
            r["vne"] = not panel.is_visible()
            itog.append(r)
        except Exception as e:
            itog.append({"kljuch": k, "oshibka": str(e).split("\n")[0][:90]})
    # Берём любую подсказку, которая ещё сидит на радиокнопке.
    kljuch_staroj = pg.evaluate("""() => {
        const e = document.querySelector('label.t[for^="gl-"]');
        return e ? e.getAttribute('for').slice(3) : null;
    }""")
    if kljuch_staroj:
        staraja = pg.locator('label.t[for="gl-%s"]' % kljuch_staroj).first
        staraja.scroll_into_view_if_needed(); staraja.click(); pg.wait_for_timeout(400)
        staraja_zhiva = pg.locator(".gp-%s" % kljuch_staroj).is_visible()
    else:
        staraja_zhiva = None
    b.close()

ploho = []
for r in itog:
    print(json.dumps(r, ensure_ascii=False))
    if "oshibka" in r or r["do"] or not all([r["otkrylas"], r["verhnij_sloj"], r["ctl_skryt"],
                                             r["esc"], r["krest"], r["vne"]]):
        ploho.append(r["kljuch"])
if staraja_zhiva is None:
    print("старый механизм: не осталось подсказок на радиокнопках")
else:
    print("старый механизм (%s):" % kljuch_staroj, "жив" if staraja_zhiva else "СЛОМАН")
print("ДЕФЕКТЫ: " + ", ".join(ploho) if ploho or staraja_zhiva is False else "всё чисто")
