#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Переложить собранные конкурсы в сырьё наград и оценок.

Сборщики — `vzjat-biwc.py`, `vzjat-iwc.py`, `vzjat-cmb.py`, `vzjat-awc.py`,
`vzjat-wine-trophy.py`, `vzjat-gilbert-gaillard.py` — пишут каждый свой
JSON. Дальше их записи должны попасть в две общие дорожки: медали и
трофеи в `nagrady-zapisi.jsonl`, стобалльные баллы в `kritiki-zapisi.jsonl`.

Раньше этот шаг делался руками, разовой командой в оболочке. Он нигде не
записан, повторить его нельзя, и всё, что сборщики добрали потом, в общие
файлы не попадало. Отсюда скрипт: шаг тот же, но воспроизводимый.

Медаль и балл — два разных высказывания об одном вине, поэтому конкурс со
стобалльной шкалой (BIWC, AWC) даёт и награду, и оценку. Трофей — третье:
он стоит выше медали, шкалы у него нет, и одно вино берёт трофей и медаль
сразу. Поэтому трофей — своя запись, а не поле при медали.

    python3 _rabota/rejtingi/svesti-konkursy.py

Ничего не удаляет: записи сводятся по ключу, чужие источники не трогает.
"""
import json
import os
import sys

for _potok in (sys.stdout, sys.stderr):
    if hasattr(_potok, "reconfigure"):
        try:
            _potok.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ZDES = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(ZDES, *ch)

# Имя медали по-русски и её код. Коды те же, что у остальных источников:
# по ним медали сортируются, поэтому писать их надо одинаково.
MEDALI = {
    "platinum": ("платина", "platina"),
    "double gold": ("двойное золото", "dvojno-zlato"),
    "grand gold": ("большое золото", "veliko-zlato"),
    "gold": ("золото", "zlato"),
    "silver": ("серебро", "srebro"),
    "bronze": ("бронза", "bronza"),
    "commended": ("отмечено", "commended"),
    "approval": ("одобрение", "approval"),
    "seal of approval": ("одобрение", "approval"),
    "trophy": ("трофей", "trofej"),
}


def medal(nazvanie):
    """Медаль по её английскому имени — или ничего, но громко.

    Молчаливый пропуск незнакомой медали — та самая ошибка, из-за которой
    у DWWA полтора десятка лет терялась восьмая ступень. Поэтому здесь
    незнакомое имя не пропускается тихо, а называется в отчёте.
    """
    return MEDALI.get((nazvanie or "").strip().lower())


def chitat(imya):
    if not os.path.exists(put(imya)):
        return None
    return json.load(open(put(imya), encoding="utf-8"))


def nagrada(istochnik, god, imya_medali, kod, hozyaistvo, vino,
            urozhaj, stranica, cvet=""):
    return {"istochnik": istochnik, "god": god, "kategoriya": imya_medali,
            "mesto": kod, "hozyaistvo": hozyaistvo, "vino": vino,
            "urozhaj": urozhaj, "cvet": cvet, "stranica": stranica}


def ocenka(istochnik, hozyaistvo, vino, urozhaj, konkurs_god, ball,
           stranica, cvet=""):
    return {"istochnik": istochnik, "hozyaistvo": hozyaistvo, "vino": vino,
            "god": str(urozhaj) if urozhaj else None,
            "konkurs_god": konkurs_god, "ball": int(round(ball)),
            "cvet": cvet, "stranica": stranica}


def sobrat():
    nagrady, ocenki, neopoznano, svoi = [], [], [], set()

    d = chitat("biwc-zapisi.json")
    if d:
        svoi.add("biwc")
        for z in d["zapisi"]:
            adres = "%s, BIWC %d" % (z["stranica"], z["god"])
            if z.get("medal"):
                m = medal(z["medal"])
                if m:
                    nagrady.append(nagrada("biwc", z["god"], m[0], m[1],
                                           z["hozyaistvo"], z["vino"],
                                           z.get("urozhaj"), adres,
                                           z.get("cvet") or ""))
                else:
                    neopoznano.append(("biwc", z["medal"]))
            if z.get("ball"):
                ocenki.append(ocenka("biwc", z["hozyaistvo"], z["vino"],
                                     z.get("urozhaj"), z["god"], z["ball"],
                                     adres, z.get("cvet") or ""))
        # Трофей записывается своим именем: «Grand Trophy», «Best of Show
        # Serbia». Это не ступень медали, у него нет ни шкалы, ни ранга,
        # который можно было бы с медалью сравнить.
        for z in d.get("trofei", []):
            nagrady.append(nagrada("biwc", z["god"], z["kategoriya"], "trofej",
                                   z["hozyaistvo"], z["vino"], z.get("urozhaj"),
                                   "%s, BIWC %d" % (z["stranica"], z["god"]),
                                   z.get("cvet") or ""))

    d = chitat("iwc-zapisi.json")
    if d:
        svoi.add("iwc")
        for z in d["zapisi"]:
            m = medal(z.get("medal"))
            if not m:
                if z.get("medal"):
                    neopoznano.append(("iwc", z["medal"]))
                continue
            nagrady.append(nagrada("iwc", z["god"], m[0], m[1], z["hozyaistvo"],
                                   z["vino"], z.get("urozhaj"), z["stranica"]))

    d = chitat("cmb-zapisi.json")
    if d:
        svoi.add("cmb")
        for z in d["zapisi"]:
            m = medal(z.get("medal"))
            if not m:
                if z.get("medal"):
                    neopoznano.append(("cmb", z["medal"]))
                continue
            nagrady.append(nagrada("cmb", z["god"], m[0], m[1], z["hozyaistvo"],
                                   z["vino"], z.get("urozhaj"), z["stranica"]))

    d = chitat("awc-zapisi.json")
    if d:
        svoi.add("awc-vienna")
        for z in d["zapisi"]:
            m = medal(z.get("medal"))
            if m:
                nagrady.append(nagrada("awc-vienna", z["god"], m[0], m[1],
                                       z["hozyaistvo"], z["vino"],
                                       z.get("urozhaj"), z["stranica"]))
            elif z.get("medal"):
                neopoznano.append(("awc-vienna", z["medal"]))
            if z.get("ball"):
                ocenki.append(ocenka("awc-vienna", z["hozyaistvo"], z["vino"],
                                     z.get("urozhaj"), z["god"], z["ball"],
                                     z["stranica"]))
            # Трофей — своя запись, как у балканского конкурса. Поле
            # `trofej` до сих пор не читалось, и все трофеи AWC пропадали.
            if z.get("trofej"):
                nagrady.append(nagrada("awc-vienna", z["god"], "Trophy",
                                       "trofej", z["hozyaistvo"], z["vino"],
                                       z.get("urozhaj"), z["stranica"]))

    d = chitat("wine-trophy-zapisi.json")
    if d:
        svoi.add("wine-trophy")
        for z in d["zapisi"]:
            m = medal(z.get("medal"))
            if not m:
                if z.get("medal"):
                    neopoznano.append(("wine-trophy", z["medal"]))
                continue
            nagrady.append(nagrada("wine-trophy", z["god"], m[0], m[1],
                                   z["hozyaistvo"], z["vino"], z.get("urozhaj"),
                                   "%s, %s %d" % (z["stranica"], z["konkurs"],
                                                  z["god"])))

    d = chitat("gilbert-gaillard-zapisi.json")
    if d:
        svoi.add("gilbert-gaillard")
        for z in d["zapisi"]:
            if z.get("ball"):
                # У гида имя вина бывает пустым: «Tri SuncA 2015» — всё,
                # что о нём сказано. Тогда именем вина служит имя
                # хозяйства: запись без имени вина дальше не проходит.
                ocenki.append({"istochnik": "gilbert-gaillard",
                               "hozyaistvo": z["hozyaistvo"],
                               "vino": z["vino"] or z["hozyaistvo"],
                               "god": str(z["urozhaj"]) if z.get("urozhaj") else None,
                               "ball": int(z["ball"]), "cvet": "",
                               "stranica": z["stranica"]})

    return nagrady, ocenki, neopoznano, svoi


def slit(imya, novye, klyuch, svoi_istochniki=()):
    """Свести записи в общий файл по ключу. Чужого не трогает.

    Записи своих источников не только дописываются, но и снимаются, если
    сборщик их больше не даёт. Без этого исправление в сборщике оставляло
    старую строку рядом с новой: AWC писал одно вино то «Komsinice», то
    «Komšinice», и после починки ключа в файле лежали обе, с разным баллом.

    Снимается только то, что этот же скрипт и положил: `svoi_istochniki` —
    имена источников, чьи сборщики сейчас прочитаны. Записи, сделанные
    руками или другими скриптами (Falstaff, Wine-Searcher, vino.rs),
    не трогаются никогда.
    """
    dorozhka = put(imya)
    bylo, poryadok = {}, []
    if os.path.exists(dorozhka):
        for stroka in open(dorozhka, encoding="utf-8"):
            if stroka.strip():
                z = json.loads(stroka)
                k = klyuch(z)
                if k not in bylo:
                    poryadok.append(k)
                bylo[k] = z
    svezhie = {klyuch(z) for z in novye}
    snyato = [k for k in poryadok
              if bylo[k].get("istochnik") in svoi_istochniki
              and k not in svezhie]
    for k in snyato:
        del bylo[k]
    poryadok = [k for k in poryadok if k in bylo]
    dobavleno = 0
    for z in novye:
        k = klyuch(z)
        if k not in bylo:
            poryadok.append(k)
            dobavleno += 1
        bylo[k] = z
    with open(dorozhka, "w", encoding="utf-8") as f:
        for k in poryadok:
            f.write(json.dumps(bylo[k], ensure_ascii=False) + "\n")
    print("%s: всего %d, добавлено %d, снято устаревших %d"
          % (imya, len(bylo), dobavleno, len(snyato)))


def main():
    nagrady, ocenki, neopoznano, svoi = sobrat()
    print("из сборщиков: наград %d, оценок %d" % (len(nagrady), len(ocenki)))
    if neopoznano:
        print("\nмедали, которых нет в таблице, — записи потеряны:")
        for istochnik, imya in sorted(set(neopoznano)):
            print("   %s: %r" % (istochnik, imya))
    slit("nagrady-zapisi.jsonl", nagrady,
         lambda z: (z["istochnik"], z["god"], z["kategoriya"], z["hozyaistvo"],
                    z["vino"], z.get("urozhaj"), z.get("cvet") or ""),
         svoi)
    slit("kritiki-zapisi.jsonl", ocenki,
         lambda z: (z["istochnik"], z["hozyaistvo"], z["vino"], z["god"],
                    z.get("konkurs_god"), z.get("cvet") or ""),
         svoi)


if __name__ == "__main__":
    main()
