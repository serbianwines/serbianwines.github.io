# -*- coding: utf-8 -*-
"""Кандидаты в свод написаний вин: найти, но не решать.

Список `sinonimy-vin.json` ведётся руками, и это правильно: свести два
имени — значит сказать, что это одно вино, а такое решение принимается
глазами. Но искать кандидатов вручную дорого, и первый заход дал 31 пару
там, где их 87. Этот скрипт ищет; сводит по-прежнему человек.

Ищутся только те разряды расхождений, которые список признаёт:

  переставлены слова   «Bukovska Bagrina» и «Bagrina Bukovska»
  опечатка в букву     «Berment» вместо «Bermet»
  слово из словаря     «Sovinjon» и «Sauvignon», «Crveno» и «Red»

Словарь слов не задан заранее, а вычитан из уже сведённых пар: если
автор однажды признал, что «Sovinjon» — это «Sauvignon», то и в других
хозяйствах эта пара стоит проверки. Пары, уже стоящие в списке, отсеяны.

Разница в целом слове, которого нет в словаре, сюда не идёт: «Trijumf»
и «Trijumf Selection» — разные вина, и таких пар в данных две сотни.

    python3 _rabota/rejtingi/najti-sinonimy.py

Ничего не пишет — печатает список для просмотра.
"""
import json, os, re, sys, unicodedata, collections, itertools
import importlib.util

RYADOM = os.path.dirname(os.path.abspath(__file__))
put = lambda *ch: os.path.join(RYADOM, *ch)


def _tablicy():
    """Перевод письма берётся из sobrat-tablicy.py, а не пишется заново.

    Свой перевод разошёлся бы с основным: первая написанная здесь `slova`
    кириллицу просто выбрасывала, и «Гушт Шардоне (Guešt Chardonnay)»
    выглядело опечаткой в имени «Gušt Chardonnay».
    """
    spec = importlib.util.spec_from_file_location(
        "tablicy", put("sobrat-tablicy.py"))
    modul = importlib.util.module_from_spec(spec)
    sys.modules["tablicy"] = modul
    spec.loader.exec_module(modul)
    return modul


latinicej = _tablicy().latinicej


def slova(imya):
    """Имя вина → список слов латиницей, без диакритики и знаков."""
    razobrano = unicodedata.normalize("NFD", latinicej(imya or ""))
    bez = "".join(z for z in razobrano if unicodedata.category(z) != "Mn")
    bez = bez.replace("đ", "dj").replace("Đ", "dj").replace("ł", "l")
    return [s for s in re.split(r"[^0-9A-Za-z]+", bez.lower()) if s]


def rasstoyanie_odin(a, b):
    """Различаются ли строки ровно одной правкой буквы."""
    if abs(len(a) - len(b)) > 1 or a == b:
        return False
    if len(a) > len(b):
        a, b = b, a
    if len(a) == len(b):
        raznyh = [i for i in range(len(a)) if a[i] != b[i]]
        if len(raznyh) == 1:
            return True
        # Перестановка двух соседних букв — та же опечатка.
        return (len(raznyh) == 2 and raznyh[1] == raznyh[0] + 1
                and a[raznyh[0]] == b[raznyh[1]]
                and a[raznyh[1]] == b[raznyh[0]])
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == a:
            return True
    return False


def svedennye():
    """Пары, уже стоящие в списке, и словарь слов, вычитанный из них."""
    put_f = put("sinonimy-vin.json")
    if not os.path.exists(put_f):
        return set(), collections.Counter()
    d = json.load(open(put_f, encoding="utf-8"))["vina"]
    pary, slovar = set(), collections.Counter()
    for hozyaistvo, vina in d.items():
        for glavnoe, z in vina.items():
            for variant in z["varianty"]:
                a, b = tuple(slova(glavnoe)), tuple(slova(variant))
                pary.add(frozenset((a, b)))
                # Слово против слова — только когда всё остальное совпало.
                if len(a) == len(b):
                    raznye = [(x, y) for x, y in zip(a, b) if x != y]
                    if len(raznye) == 1 and not rasstoyanie_odin(*raznye[0]):
                        slovar[frozenset(raznye[0])] += 1
    return pary, slovar


def celoe_slovo_lishnee(a, b):
    """Одно имя — другое плюс целое слово: «Brut» и «Brut C», «Misterija»
    и «Misterija G». Это разные вина, и список такие пары не берёт."""
    menshe, bolshe = sorted((a, b), key=len)
    ostatok = collections.Counter(bolshe) - collections.Counter(menshe)
    return sum(ostatok.values()) and not (collections.Counter(menshe)
                                          - collections.Counter(bolshe))


def oboznachenie(para):
    """Различие не в букве, а в обозначении: «Edicija R» и «Edicija S»,
    «Victor 1» и «Victor 2». Одна буква разницы тут ничего не значит."""
    odno, drugoe = para
    if any(z.isdigit() for z in odno + drugoe):
        return True
    return len(odno) == 1 and len(drugoe) == 1


def razryad(a, b, slovar):
    """Чем различаются два имени. Пусто — значит расхождение не наше.

    Второе возвращаемое — правда, если различие похоже на наше, но
    упирается в номер или букву-обозначение. Такие пары показываются
    отдельно: обычно это разные вина, но решает всё равно человек.
    """
    if sorted(a) == sorted(b) and a != b:
        return "переставлены слова", False
    if celoe_slovo_lishnee(a, b):
        return "", False
    if len(a) == len(b):
        raznye = [(x, y) for x, y in zip(a, b) if x != y]
        if len(raznye) == 1:
            if rasstoyanie_odin(*raznye[0]):
                if oboznachenie(raznye[0]):
                    return "различие в обозначении: %s / %s" % raznye[0], True
                return "опечатка в букву", False
            if frozenset(raznye[0]) in slovar:
                return "слово из словаря: %s / %s" % raznye[0], False
    # Опечатка, слепившая или разорвавшая слово, — тоже одна буква.
    if rasstoyanie_odin("".join(a), "".join(b)):
        if any(z.isdigit() for z in "".join(a) + "".join(b)):
            return "различие в номере", True
        return "опечатка в букву", False
    return "", False


def main():
    pary, slovar = svedennye()
    print("уже сведено пар: %d, слов в словаре: %d"
          % (len(pary), len(slovar)))
    if slovar:
        print("словарь:", ", ".join(
            "%s/%s" % tuple(p) for p, _ in slovar.most_common(20)))

    po_hozyaistvu = collections.defaultdict(list)
    for stroka in open(put("vina.jsonl"), encoding="utf-8"):
        v = json.loads(stroka)
        po_hozyaistvu[v["hozyaistvo"]].append(v)

    najdeno, spornye = 0, []
    for hozyaistvo in sorted(po_hozyaistvu):
        svoi = po_hozyaistvu[hozyaistvo]
        stroki = []
        for odno, drugoe in itertools.combinations(svoi, 2):
            a, b = tuple(slova(odno["vino"])), tuple(slova(drugoe["vino"]))
            if not a or not b or a == b:
                continue
            if frozenset((a, b)) in pary:
                continue
            chem, spornoe = razryad(a, b, slovar)
            if not chem:
                continue
            # Два номера Vivino — это два разных места каталога, и свести
            # их значило бы решить за Vivino. Такие пары показываются,
            # но помечены: решение всё равно за человеком.
            oba = odno.get("vivino_id") and drugoe.get("vivino_id")
            stroka = "   %-40s ← %-40s %s%s" % (
                odno["vino"], drugoe["vino"], chem,
                "  [оба с номером Vivino]" if oba else "")
            (spornye if spornoe else stroki).append(
                ("%s: " % hozyaistvo if spornoe else "") + stroka)
        if stroki:
            print("\n### %s" % hozyaistvo)
            for stroka in stroki:
                print(stroka)
            najdeno += len(stroki)
    print("\nкандидатов: %d — просмотреть глазами, в файл ничего не записано"
          % najdeno)
    if spornye:
        print("\nПохоже, но различие в номере или букве-обозначении — "
              "обычно это разные вина (%d):" % len(spornye))
        for stroka in spornye:
            print(stroka)


if __name__ == "__main__":
    main()
