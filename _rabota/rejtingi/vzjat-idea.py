#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Разобрать сохранённые страницы винного раздела Idea (online.idea.rs).

Второй супермаркет к Maxi. Один магазин — это его закупка, а не полка
страны: у Maxi с нашей таблицей сошлись двадцать девять вин, на страновую
таблицу «что взять в супермаркете» хватает, на район — нет. Idea берёт
вино у других поставщиков, и пересечение с Maxi неполное.

Машиной не берётся по той же причине, что Maxi: каталог рисует
AngularJS, товарного API в разметке нет. Сохранённая человеком страница
(Ctrl+S) уже нарисована.

    py -3 _rabota/rejtingi/vzjat-idea.py "Belo vino - IDEA.html" ...

Раздел разбит на страницы по 96 позиций, и сохранять надо каждую.

**Цвет со страницы не берётся.** Автор предупредил, что раздел магазина
врёт: на странице белых стоят красные бутылки. Цвет вина у нас свой,
в `vina.jsonl`; отсюда идёт только цена, а имя раздела пишется в
`razdel` — как след происхождения, не как свойство вина.

Чужие вина в разделе тоже есть — Casillero del Diablo, Freschello,
Baron d'Arignac. Поля страны у Idea нет, и отсекать их здесь нечем;
отсекаются они сведением: в нашей таблице только сербские вина, и
несербское просто не находит пары.

Пишет `idea-ceny.json`.
"""
import html
import json
import pathlib
import re
import sys
import time

ZDES = pathlib.Path(__file__).resolve().parent

# Карточка товара. Меток в разметке две: `ng-repeat` по продукту и
# `class="ime-proizvoda"`. Взята вторая: первая встречается дважды
# на карточку (директива остаётся и на шаблоне, и на клоне), а вторая —
# ровно по разу, что и сверено счётом ссылок на товар.
METKA = 'class="ime-proizvoda"'
IMYA = re.compile(r'ng-bind="::product\.name"[^>]*>([^<]*)</a>')
ADRES = re.compile(r'href="(https://online\.idea\.rs/[^"]*)"')
TOVAR = re.compile(r'#!/products/(\d+)/')
# Цена нарисована двумя узлами: целая часть — голым текстом сразу за
# `<p class="cijena">`, копейки — надстрочным `decimalni-dio`. Разряды
# у Idea разделены запятой («1,829»), а не точкой, как у Maxi.
CENA = re.compile(r'class="cijena">\s*(?:<!---->\s*)?([\d.,]+)<!--\s*-->'
                  r'<span class="decimalni-dio"[^>]*>(\d+)</span>')
# Снятая с продажи позиция помечается классом на карточке. В сохранённых
# страницах таких не было ни одной, но состояние полки надо сохранять,
# а не выводить из того, что образец оказался полным.
NET_V_PRODAZHE = re.compile(r'class="[^"]*\bdisabled\b[^"]*"[^>]*'
                            r'im-wsc-product="product"')
OBEM = re.compile(r'(\d+(?:[.,]\d+)?)\s*(l|ml)\b', re.I)


def obem_litrov(imya):
    """Объём из имени: «0,75l», «750ml», «1l»."""
    sovpalo = OBEM.search(imya or "")
    if not sovpalo:
        return None
    chislo = float(sovpalo.group(1).replace(",", "."))
    return chislo / 1000 if sovpalo.group(2).lower() == "ml" else chislo


def razdel_iz_imeni_fajla(fajl):
    """«Belo vino2 - IDEA.html» → «Belo vino». Сохранёнка нумерует
    страницы раздела, а браузер ещё и пишет сербские буквы как «#U0161»."""
    imya = re.sub(r"\s*-\s*IDEA$", "", fajl.stem)
    imya = re.sub(r"#U([0-9a-f]{4})", lambda m: chr(int(m.group(1), 16)), imya)
    return re.sub(r"\d+$", "", imya).strip()


def razobrat(stranica, razdel):
    vina = []
    for hvost in stranica.split(METKA)[1:]:
        imya = IMYA.search(hvost)
        cena = CENA.search(hvost)
        if not imya:
            continue
        polnoe = html.unescape(imya.group(1)).strip()
        if not polnoe:
            continue
        tovar = TOVAR.search(hvost)
        adres = ADRES.search(hvost)
        vina.append({
            "vino": re.sub(r"\s+", " ", polnoe),
            # Хозяйство Idea отдельным полем не пишет: имя товара
            # начинается с марки («Aleksandrović Tema Selection vino
            # 0,75l»), и дом достаётся из начала имени при сведении.
            "hozyaistvo": "",
            "cena_rsd": (float("%s.%s" % (cena.group(1).replace(",", ""),
                                          cena.group(2))) if cena else None),
            "litrov": obem_litrov(polnoe),
            "v_prodazhe": not NET_V_PRODAZHE.search(hvost[:1200]),
            "razdel": razdel,
            "tovar": tovar.group(1) if tovar else "",
            "stranica": adres.group(1) if adres else "",
        })
    return vina


def main():
    fajly = [pathlib.Path(a) for a in sys.argv[1:]]
    if not fajly:
        raise SystemExit("нужны пути к сохранённым страницам раздела «Vino»")
    vina, vidano = [], set()
    for fajl in fajly:
        stranica = fajl.read_text(encoding="utf-8", errors="replace")
        razdel = razdel_iz_imeni_fajla(fajl)
        bylo = len(vina)
        for z in razobrat(stranica, razdel):
            # Товар один и тот же может стоять в двух разделах — цвет
            # у Idea проставлен небрежно. Первое вхождение и остаётся.
            klyuch = z["tovar"] or z["vino"]
            if klyuch in vidano:
                continue
            vidano.add(klyuch)
            vina.append(z)
        print("%s (%s): %d" % (fajl.name, razdel, len(vina) - bylo))
    s_cenoj = sum(1 for z in vina if z["cena_rsd"])
    (ZDES / "idea-ceny.json").write_text(json.dumps({
        "chto_eto": "Винный раздел Idea Online: цена в динарах, объём, "
                    "раздел магазина. Второй супермаркет к Maxi. "
                    "Раздел — не цвет вина: магазин путает.",
        "istochnik": "online.idea.rs, раздел «Вино», сохранённые страницы",
        "sobrano": time.strftime("%Y-%m-%d"),
        "vina": vina,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nсобрано %d позиций, с ценой %d → idea-ceny.json"
          % (len(vina), s_cenoj))


if __name__ == "__main__":
    main()
