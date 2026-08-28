# Пятёрки по регионам, Vivino

Собрано в августе 2026-го. Ниже — вина, отобранные правилом: порог по числу
отзывов, затем сдвиг оценки к средней по выборке, затем потолок в два вина на
хозяйство. Разбор правила — в `README.md`.

**Как это читать.** Столбец «Vivino» — сырая оценка сайта. «Отзывов» — на
скольких она держится. «После сдвига» — то, по чему выстроен порядок: оценка,
подтянутая к средней тем сильнее, чем меньше отзывов. Вино с 4,4 по двадцати
пяти отзывам стоит ниже вина с 4,3 по тремстам сорока — так и задумано.

**Чего здесь нет.** Вин, у которых число отзывов установить не удалось. Их
почти две сотни, и они перечислены под каждым районом отдельной строкой —
это очередь, а не отбраковка: среди них есть вина с оценкой выше всех
попавших в таблицу. Пока неизвестно, на скольких отзывах эта оценка держится,
ставить их в список нельзя — это ровно то, чего вы просили избежать.

Числа отзывов, помеченные в `vivino-zapisi.jsonl` как «нижняя граница», взяты
из профиля вкуса или из отдельного урожая: настоящее число не меньше
указанного. Таких пять.

**Пересобрать файл:**

    cd _rabota/rejtingi
    cat po-regionam-vstuplenie.md > po-regionam.md
    python3 svesti-pyaterki.py --markdown >> po-regionam.md

---

<!-- Собрано скриптом svesti-pyaterki.py. Руками не править: -->
<!-- правьте vivino-zapisi.jsonl и перегенерируйте.          -->

Порог 25 отзывов · вес недоверия 50 · потолок 2 вина на хозяйство.
Средняя, к которой идёт сдвиг, — **3.91** по 115 винам, прошедшим порог.

## Фрушка гора

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Erdevik · Grand Trianon | 4.3 | 340 | 4.25 |
| 2 | Erdevik · Omnibus Lector Chardonnay | 4.3 | 283 | 4.24 |
| 3 | Kovačević · Edicija S Aurelius | 4.2 | 144 | 4.12 |
| 4 | Deurić · Chardonnay | 4.1 | 533 | 4.08 |
| 5 | Dukay-Sagmeister · Kanias Pinot Noir | 4.1 | 258 | 4.07 |

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Veritas Ćuković · Momentum Cabernet Sauvignon 4.4, Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 4.3, Erdevik · Stifler's Mom Shiraz 4.3, Kovačević · Edicija R Chardonnay 4.2, Erdevik · Trianon 4.1, Kovačević · Edicija R Sauvignon 4.1, Kovačević · Edicija S Sauvignon 4.1, Bikicki · Victor 4.1, Bikicki · Sfera Noir 4.1, Đurđić · Probus 4.1, Molovin · Inat Traminac 4.1, Šapat · Àkcent Réserve 4.1, Vinčić · Grand Fru 4.0, Bikicki · Makana 4.0 — и ещё 71.

## Суботичско-Хоргошская пешчара

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Zvonko Bogdan · Chardonnay | 4.0 | 100 | 3.97 |
| 2 | Tonković · Rapsodija Kadarka | 3.9 | 322 | 3.90 |
| 3 | Tonković · Fantazija Kadarka | 3.8 | 857 | 3.81 |

В списке 3 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Petra · Traminac Late Harvest 4.4, Zvonko Bogdan · Icon Campana Rubimus 4.3, Maurer · Kadarka Gravitation 4.3, Maurer · Kadarka Nagy-Krisztus 4.2, Maurer · Oszkar Babba 4.2, Petra · Cuvée 4.2, Zvonko Bogdan · Merlot 4.1, Zvonko Bogdan · Cuvée No.1 4.1, Zvonko Bogdan · Icon Campana Albus 4.1, Maurer · Oszkar Karom 4.1, Maurer · Sott 4.1, Maurer · Tamjanika 4.1, Zvonko Bogdan · Nebo Tamjanika 4.0, Zvonko Bogdan · Rosé Sec 4.0 — и ещё 8.

## Банат

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Čoka · Ždrepčeva Krv Forever | 4.0 | 66 | 3.96 |
| 2 | Čoka · Kupianovo Vino | 3.9 | 172 | 3.90 |

В списке 2 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Drašković · Muskat Otonel 4.1, Drašković · Chardonnay 3.8, Drašković · Horizont Chardonnay 3.7, Drašković · Mahago 3.7, Drašković · Divlja Ruža Rosé 3.7, Drašković · Ruža Vetrova Muskat Otonel 3.7, Drašković · Beli Pinot 3.6, Drašković · Triptih 3.5, Drašković · Rosé 3.5, Vršački vinogradi · Banatski Rizling 3.3.

## Шумадия

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Radovanović · Réserve Cabernet Sauvignon | 4.3 | 310 | 4.25 |
| 2 | Matijašević · SoviNoa Fumé Blanc | 4.3 | 189 | 4.22 |
| 3 | Despotika · Dodir Muscat Ottonel-Tamjanika | 4.2 | 460 | 4.17 |
| 4 | Matijašević · SoviNoa Sauvignon Blanc | 4.1 | 522 | 4.08 |
| 5 | Despotika · Morava Orange | 4.1 | 73 | 4.02 |

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Radovanović · Réserve Special Cabernet Sauvignon 4.4, Radovanović · Grand Reserve Cabernet Sauvignon 4.3, Radovanović · Cabernet Sauvignon 4.3, Aleksandrović · Rodoslov Reserve 4.3, Aleksandrović · Trijumf Gold 4.2, Aleksandrović · Prokupac 4.2, Arsenijević · Cabernet Sauvignon Limited Edition 4.2, Radovanović · Pino Sivi 4.1, Aleksandrović · Vizija Selection 4.1, Aleksandrović · Trijumf Selection 4.1, Aleksandrović · Trijumf Noir Brut 4.1, Radovanović · Chardonnay Selekcija 4.1, Aleksandrović · Harizma Selection 4.0, Despotika · Od Sorte Morava 4.0 — и ещё 4.

## Три Моравы и Жупа

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Temet · Three Morave Rezerva | 4.4 | 25 | 4.07 |
| 2 | Temet · Three Bele | 4.1 | 43 | 4.00 |
| 3 | Ivanović · Prokupac | 3.9 | 294 | 3.90 |

В списке 3 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Ivanović · No 1/2 4.3, Jovac · Single Vineyard Stella Noir 4.3, Jovac · Single Vineyard Selection Chardonnay 4.3, Ivanović · No 3/4 Tamjanika 4.2, Jovac · Single Vineyard Selection Tamjanika 4.2, Rubin · Double Barrique Cabernet Sauvignon 4.1, Rubin · Double Barrique Sauvignon Blanc 4.1, Jovac · Single Vineyard Selection Sauvignon Blanc 4.0, Ivanović · Tamjanika 3.9, Zupa · Kupinovo Vino 3.9, Rubin · Amante Matea Merlot 3.8, Rubin · Amante Aurora 3.8, Rubin · Merlot 3.6, Ivanović · Petite Rose 3.6 — и ещё 4.

## Неготинска Крайина

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Matalj · Kremen Kamen Cabernet Sauvignon | 4.5 | 120 | 4.33 |

В списке 1 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Matalj · Zemna Reserva 4.2, Matalj · Kremen Cabernet-Merlot 4.1, Matalj · Začinak Bukovski 4.1, Matalj · Kremen Cabernet Sauvignon 4.0, Matalj · Cuvée Bukovski 4.0, Matalj · Crna Tamjanika 4.0, Matalj · Kremen Kremenjača 4.0, Matalj · Bagrina Bukovska 3.9, Raj · Crna Tamjanika 3.7, Raj · Bela Tamjanika 3.7.

## Топлица

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Toplički vinogradi · Gvozdeni Puk Rujno | 4.3 | 42 | 4.09 |
| 2 | Doja · Breg Prokupac | 4.1 | 99 | 4.04 |
| 3 | Toplički vinogradi · Epigenia Cabernet Sauvignon | 3.8 | 34 | 3.86 |
| 4 | Doja · Rosé | 3.5 | 180 | 3.59 |

В списке 4 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Doja · Breg Cabernet Sauvignon 4.3, Doja · Breg Merlot 4.0, Doja · Cabernet Sauvignon-Merlot 3.9, Doja · Prokupac 3.9, Doja · Tamjanika 3.9, Doja · Belo Chardonnay-Pinot Grigio 3.7.

## Юго-восток

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Aleksić · Amanet Vranac | 4.0 | 200 | 3.98 |
| 2 | Džervin · Rosé Romansa | 3.5 | 61 | 3.68 |

В списке 2 вина из пяти: у остальных района число отзывов не установлено.

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Aleksić · Žuti Cvet 4.1, Aleksić · Limited Bonaca Chardonnay 4.1, Jović · Vranac 4.0, Džervin · Schlossberg Merlot 3.9, Džervin · Sauvignon 3.9, Aleksić · Kardaš Cabernet Sauvignon 3.8, Aleksić · Morava 3.8, Aleksić · Prokupac 3.8, Aleksić · Nostalgija 3.6, Džervin · Despot Crveni 3.3, Džervin · Dubravka 3.0.

## Подунавье и Белградский район

Пятёрка не собирается: ни одного вина с известным числом отзывов.

## Косово и Метохия

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Lakićević · Cuvée No.5 Merula | 4.2 | 178 | 4.14 |
| 2 | Lakićević · Upupa Tamjanika | 4.2 | 133 | 4.12 |

В списке 2 вина из пяти: у остальных района число отзывов не установлено.

## Хозяйства без района

Вина есть, к какой главе книги отнести — не установлено:

- Virtus · Prokupac 733 — 4.4 (26)
- Virtus · Cuvée Virtus Credo — 4.3 (312)
- Virtus · Credo Beli — 4.2 (122)
- Grabak · Vivak Prokupac — 4.1 (35)
- Virtus · Pinot Noir — 4.0 (607)
- Grabak · Siva Vrana — 4.0 (32)
- Grabak · Ćuk Merlot — 4.0 (72)
- Virtus · Marselan — 3.9 (288)
- Virtus · Gewürztraminer — 3.9 (132)
- Grabak · Modrovrana — 3.9 (30)
- Virtus · Mlavac Crveni — 3.8 (198)
- Virtus · Pinot Grigio — 3.8 (131)
- Virtus · Sauvignon Blanc — 3.8 (484)
- Grabak · Prva Lasta — 3.7 (58)
- Grabak · Grabak Prokupac — 3.7 (52)
- Virtus · Prokupac — 3.6 (47)
- Grabak · Bela Galubica — 3.6 (27)

