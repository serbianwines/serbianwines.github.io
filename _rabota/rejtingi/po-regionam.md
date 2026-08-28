# Пятёрки по регионам, Vivino

Собрано 28 августа 2026 года сплошным обходом: 433 сербских хозяйства,
2786 вин. Оценка есть у 1189, и **у 99% из них известно число отзывов** —
то, чего не хватало, пока сбор шёл через поисковую выдачу.

Ниже — вина, отобранные правилом: порог по числу отзывов, затем сдвиг
оценки к средней по выборке, затем потолок в два вина на хозяйство.
Разбор правила — в `README.md`.

**Как это читать.** Столбец «Vivino» — сырая оценка сайта. «Отзывов» —
на скольких она держится. «После сдвига» — то, по чему выстроен порядок:
оценка, подтянутая к средней тем сильнее, чем меньше отзывов. Вино с 4,4
по тридцати пяти отзывам стоит ниже вина с 4,3 по двум тысячам — так
и задумано.

**Чего здесь нет.** Вин хозяйств, которые не удалось отнести к главе книги:
район известен только у 59 хозяйств из 479. У остальных Vivino пишет
«Central Serbia» или «Wine of Serbia» — свалка на полторы тысячи вин,
по ней судить нельзя. Такие вина в пятёрки не идут; их 600.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-pyaterki.py --otchet

---

<!-- Собрано скриптом svesti-pyaterki.py. Руками не править: -->
<!-- правьте vivino-zapisi.jsonl и перегенерируйте.          -->

Порог 25 отзывов · вес недоверия 50 · потолок 2 вина на хозяйство.
Средняя, к которой идёт сдвиг, — **3.85** по 1176 винам, прошедшим порог.

## Фрушка гора

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Bjelica · Babaroga Chardonnay | 4.4 | 1025 | 4.38 |
| 2 | Erdevik · Grand Trianon | 4.3 | 2931 | 4.29 |
| 3 | Erdevik · Stifler's Mom Shiraz | 4.3 | 1359 | 4.28 |
| 4 | Veritas Ćuković · Momentum Cabernet Sauvignon | 4.4 | 83 | 4.19 |
| 5 | Kovačević · Edicija S Edition Aurelius | 4.2 | 1008 | 4.18 |

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Kovačević · Edicija R Chardonnay 4.2, Kovačević · Edicija R Sauvignon 4.1, Kovačević · Edicija S Sauvignon 4.1.

## Суботичско-Хоргошская пешчара

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Zvonko Bogdan · Icon Campana Rubimus | 4.3 | 224 | 4.22 |
| 2 | Maurer · Oszkar Babba | 4.2 | 533 | 4.17 |
| 3 | Zvonko Bogdan · Cuvée No.1 | 4.1 | 2750 | 4.10 |
| 4 | Vinarija Petra · Traminac Late Harvest | 4.4 | 35 | 4.08 |
| 5 | Maurer · Tamjanika | 4.1 | 324 | 4.07 |

Ждут уточнения (оценка есть, числа отзывов нет), по убыванию оценки:

Zvonko Bogdan · Nebo Tamjanika 4.0.

## Банат

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Drašković · Muskat Otonel | 4.1 | 317 | 4.07 |
| 2 | Vinarija Coka · Kupianovo Vino | 4.0 | 186 | 3.97 |
| 3 | Vinarija Coka · Ždrepčeva Krv Forever | 4.0 | 68 | 3.94 |
| 4 | Vršački Vinogradi · Kvalitetno Muskat Ottonel | 4.0 | 35 | 3.91 |
| 5 | Vršački Vinogradi · Вршачкн Брег Вранац | 4.0 | 34 | 3.91 |

## Шумадия

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Aleksandrović · Вожд (Vožd) Cabernet Sauvignon | 4.5 | 237 | 4.39 |
| 2 | Aleksandrović · Rodoslov Grand Reserve | 4.4 | 1721 | 4.38 |
| 3 | Radovanović · Rèserve Cabernet Sauvignon | 4.3 | 2043 | 4.29 |
| 4 | Despotika · Додир Мускат Отонел - Тамјаника (Dodir Muscat Ottonel - Тamjanika) | 4.3 | 517 | 4.26 |
| 5 | Matijašević · Sovinoa Fumé Blanc | 4.3 | 213 | 4.21 |

## Три Моравы и Жупа

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Ivanović · No 1/2 | 4.3 | 336 | 4.24 |
| 2 | Temet · Three Morave Rezerva (Три Mораве Резерва) | 4.4 | 113 | 4.23 |
| 3 | Cilić · Onyx Rouge | 4.2 | 792 | 4.18 |
| 4 | Vinarija Jovac · Single Vineyard Stella Noir | 4.3 | 134 | 4.18 |
| 5 | Budimir · Svb Rosa | 4.2 | 653 | 4.17 |

## Неготинска Крайина

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Matalj · Kremen Kamen Cabernet Sauvignon | 4.5 | 865 | 4.46 |
| 2 | Matalj · Zemna Reserva | 4.2 | 142 | 4.11 |
| 3 | Vinarija Raj · Plot | 4.1 | 152 | 4.04 |
| 4 | Vinarija Raj · Crna Tamjanika | 4.0 | 113 | 3.96 |

В списке 4 вина из пяти: у остальных района число отзывов не установлено.

## Топлица

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Doja · Breg Cabernet Sauvignon | 4.3 | 139 | 4.18 |
| 2 | Toplički Vinogradi · Гвоздени Пук Ирьено (Gvozdeni Puk Ryeno) | 4.4 | 48 | 4.12 |
| 3 | Doja · Breg Prokupac | 4.1 | 519 | 4.08 |
| 4 | Toplički Vinogradi · Tribus Villa Sauvignon Blanc | 3.8 | 57 | 3.83 |

В списке 4 вина из пяти: у остальных района число отзывов не установлено.

## Юго-восток

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Aleksić · Žuti Cvet | 4.1 | 1996 | 4.09 |
| 2 | Aleksić · Limited Bonaca Chardonnay | 4.1 | 215 | 4.05 |
| 3 | Jović · Vranac | 4.0 | 516 | 3.99 |
| 4 | Jović · Petrkanjski Roze | 4.0 | 32 | 3.91 |
| 5 | Dzervin · Sauvignon | 3.9 | 62 | 3.88 |

## Подунавье и Белградский район

Пятёрка не собирается: ни одного вина с известным числом отзывов.

## Косово и Метохия

| # | Вино | Vivino | Отзывов | После сдвига |
|---|---|---|---|---|
| 1 | Lakićević · Cuvée No.5 Merula | 4.2 | 178 | 4.12 |
| 2 | Lakićević · Upupa Tamjanika | 4.2 | 133 | 4.11 |

В списке 2 вина из пяти: у остальных района число отзывов не установлено.

## Хозяйства без района

Вина есть, к какой главе книги отнести — не установлено:

- Vinarija Vinis · Crveno Vino — 4.6 (27)
- Tri Oraha · 750 Barrique Barrels — 4.5 (60)
- Stemina · Драга (Draga) — 4.5 (62)
- Podrum Janko · Запис Тестамент (Crveni Zapis Testament) — 4.4 (66)
- Podrum Janko · Zlatno Runo Cabernet Sauvignon — 4.4 (58)
- Braca Rajkovic · 33 Red — 4.4 (311)
- Tri Oraha · Cabernet Sauvignon — 4.4 (386)
- Tri Oraha · Crnomasnica — 4.4 (206)
- Tri Oraha · Merlot — 4.4 (75)
- Tri Oraha · 500 Barrique Barrels — 4.4 (25)
- Vinarija DeLena · 1903 Merlot — 4.4 (266)
- Vinarija DeLena · Kota 376 Malbec — 4.4 (136)
- Vinarija Fragaria · Jagoda — 4.4 (176)
- Vinarija Fragaria · Red — 4.4 (52)
- Stemina · Stephanos Cabernet Sauvignon — 4.4 (32)
- Vinarija Vladimir · 1 Hektar — 4.4 (157)
- Petica · Stih Suvignon Blanc — 4.4 (32)
- Vinarija Dajic · Gamay Barrique — 4.4 (51)
- Virtus · Prokupac 733 — 4.3 (36)
- Virtus · Cuvée Virtus Credo — 4.3 (349)
- Vinarija Jeremic · Kanon Superior Merlot - Cabernet Sauvignon — 4.3 (118)
- Podrum Janko · Zavet Stari Red Blend — 4.3 (302)
- Podrum Janko · Бифора (Bifora) — 4.3 (122)
- Tri Oraha · Single Vineyard Grand Reserve — 4.3 (65)
- Винарија Манастира Буково · Вез — 4.3 (51)
- Podrum Stari Hrast · Selekcija Merlot — 4.3 (79)
- BT Winery · King Supreme Limited Edition Marselan — 4.3 (58)
- Zmajevac · Cuvée — 4.3 (70)
- Nikad Nije Kasno · Signature — 4.3 (263)
- Изба Јовановић (Izba Jovanovic) · Жетва (Žetva) — 4.3 (58)
- Vinarija Fragaria · Votaži — 4.3 (90)
- Vinarija Fragaria · Sauvignon Blanc — 4.3 (47)
- Vinarija Frug · Chardonnay Signum — 4.3 (93)
- Aleksandar Todorović · Ibis Crveni — 4.3 (59)
- Vinarija Frunza Aglaja · Аглаjа Dentelle Cabernet Sauvignon — 4.3 (64)
- Магаза (Magaza) · Тамјаника (Tamjanika) — 4.3 (86)
- Vinarija Vladimir · Plato — 4.3 (26)
- Manufaktura Spasić · Tamjanika — 4.3 (58)
- Vinarija Fleur D'Oranger · Гроф — 4.3 (102)
- Три Планине (Vinarija Tri Planine) · Заборављена Бајка (A Forgotten Fairy Tale) — 4.3 (32)
- Basha Vino · Tamjanika Prva — 4.3 (66)
- Virtus · Credo Beli — 4.2 (127)
- Vinarija Vinis · Merlot - Cabernet Sauvignon — 4.2 (106)
- Vinarija Jeremic · Sonata Icon Sauvignon Blanc — 4.2 (53)
- Vinarija Lastar · Tamjanika — 4.2 (1010)
- Vinarija Imperator · Constantivs Cabernet Franc- Cabernet Sauvignon — 4.2 (28)
- Vinarija 100 Žena · Monsieur Merlot Premium — 4.2 (124)
- Винарија Манастира Буково · Филигран (Filigran) Cabernet Sauvignon — 4.2 (236)
- Винарија Манастира Буково · Chardonnay — 4.2 (110)
- Винарија Манастира Буково · Filigran Merlot (Филигран Мерлот) — 4.2 (89)
- Винарија Манастира Буково · Filigran Reserve Merlot — 4.2 (27)
- Vinarija DeLena · 70/30 Sauvignon Blanc - Sémillon — 4.2 (255)
- Vinarija Komuna · Viognier — 4.2 (44)
- Quet · Grašac — 4.2 (150)
- Изба Јовановић (Izba Jovanovic) · Merlot — 4.2 (433)
- Dibonis Winery · Di Cabernet Sauvignon — 4.2 (133)
- Dibonis Winery · 1697 — 4.2 (51)
- Vinarija Frug · Cuvée — 4.2 (83)
- Vinarija Frug · Syrah Signum — 4.2 (50)
- Monastery Visoki Decani  (Манастирско Дечанско) · Cabernet Sauvignon Barrique — 4.2 (43)
- Aleksandar Todorović · 333 — 4.2 (134)
- Aleksandar Todorović · Čarolija — 4.2 (32)
- Legat · Pinot Noir — 4.2 (145)
- Legat · Viognier — 4.2 (128)
- Legat · Chardonnay — 4.2 (77)
- Tri Medje I Oblak · Bigfoot Chardonnay — 4.2 (66)
- Plavinci · Good Boy Bruno! Pét Nat — 4.2 (39)
- Костић (Kostić) · Прокупац (Prokupac) Barrique — 4.2 (246)
- Rnjak · Merlot Limited Edition — 4.2 (32)
- Probus Vineyards · Magis Cabernet Sauvignon - Merlot — 4.2 (64)
- Djokovic · Syrah — 4.2 (162)
- Манастир Студеница (Manastir Studenica) · 1186 Cabernet Sauvignon — 4.2 (146)
- Vinarija Đurđevića Legat · Otisak Merlot - Cabernet Sauvignon Crveno — 4.2 (149)
- Vista Hill · Reserve White — 4.2 (49)
- Miletic · Impresija Cuvée — 4.2 (46)
- Pruna · Cabernet Sauvignon — 4.2 (108)
- Reljić Vinarija · Rebus Crveno — 4.2 (114)
- Katanic · Oskar — 4.2 (106)
- MV Vinarija · Tamjanika — 4.2 (37)
- Salaxia · Burlesque Crveno — 4.2 (30)
- Три Планине (Vinarija Tri Planine) · Два Другара (Two Friends) — 4.2 (25)
- Basha Vino · Furmint — 4.2 (40)
- Vinarija Radlović · Cabernet Sauvignon — 4.2 (28)
- Virtus · Pinot Noir — 4.1 (286)
- Milijan Jelić · Nebiolo — 4.1 (33)
- Vinarija Vinis · Merlot — 4.1 (34)
- Grabak · Vivak Prokupac — 4.1 (44)
- Grabak · Siva Vrana — 4.1 (37)
- Vinarija Jeremic · Merlot Terroire — 4.1 (126)
- Vinarija Jeremic · Kanon Merlot - Cabernet Sauvignon — 4.1 (785)
- Art Wine · Argument Cabernet Sauvignon — 4.1 (32)
- Брояница (Brojanica) · Кадарка (Kadarka) — 4.1 (2842)
- Брояница (Brojanica) · Изабелла Красное Полусладкое (Isabella Red Semi-Sweet) — 4.1 (342)
- Брояница (Brojanica) · Кагор (Kagor) — 4.1 (45)
- Vinarija Lastar · Triangl Sauvignon - Viognier — 4.1 (114)
- Milijan Jelić · Millennium — 4.1 (188)
- Milijan Jelić · Millennium Barrique — 4.1 (178)
- Podrum Janko · Zapis Crveni Merlot — 4.1 (446)
- Podrum Janko · Vrtlog Sauvignon Blanc — 4.1 (78)
- Braca Rajkovic · 33 Bela — 4.1 (41)
- Vinarija Imperator · Quintillus Malbec - Merlot — 4.1 (134)
- Vinarija Imperator · Animus — 4.1 (36)
- Vinska Kuća Minića · Tamnjanika Stota Suza — 4.1 (887)
- Vinarija 100 Žena · Rosé — 4.1 (180)
- Vinarija 100 Žena · Tamjanika — 4.1 (164)
- Botunjac · Pino Svetih Ratnika Reserve Pinot Noir — 4.1 (80)
- Vinarija DeLena · 100 Jazz Mirisni Traminac — 4.1 (108)
- Vinarija Eden · Genesis — 4.1 (212)
- Vinarija Eden · Chardonnay — 4.1 (115)
- Vinarija Eden · Sauvignon Blanc — 4.1 (116)
- Quet · Merlot 18+ Edition — 4.1 (116)
- BT Winery · Mister Marselan — 4.1 (71)
- Zmajevac · Tamjanika — 4.1 (228)
- Zmajevac · Prokupac — 4.1 (148)
- Nikad Nije Kasno · Simfonija — 4.1 (154)
- Galot · Balerina — 4.1 (297)
- Château Prince · Velika Morava — 4.1 (93)
- Vinarija Fragaria · Tamjanika — 4.1 (61)
- Vinarija Frug · Pinot Noir — 4.1 (60)
- Vinarija Frug · Grašac — 4.1 (59)
- Legat · Muscat Petit Grain — 4.1 (57)
- Vinarija Mrdjanin · Probus — 4.1 (105)
- Vinarija Mrdjanin · Bermet — 4.1 (35)
- Podrum Pevac · Izazov Tamjanika — 4.1 (123)
- Probus Vineyards · BeliM Believe in Yourself — 4.1 (54)
- Probus Vineyards · Traminac — 4.1 (33)
- Mcculloch Wines · Coupage — 4.1 (50)
- Djokovic · Chardonnay — 4.1 (85)
- Манастир Студеница (Manastir Studenica) · Прокупац 1186 (Prokupac 1186) — 4.1 (33)
- Vinarija PIRG · Barrique Sauvignon Blanc — 4.1 (159)
- Vinarija PIRG · Škriljac — 4.1 (27)
- The Collective Presents · Kadarka 1880 — 4.1 (31)
- Pruna · Umbra Tamjanika — 4.1 (41)
- Manufaktura Spasić · Krivac — 4.1 (32)
- Manufaktura Spasić · Rebo — 4.1 (34)
- ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) · Пехарник (Peharnik) — 4.1 (61)
- Vert · Sauvignon Blanc — 4.1 (51)
- Vinarija Burma Fruška Gora · Sila — 4.1 (40)
- Adora · Merlot - Cabernet — 4.1 (25)
- Traško Vinarija · Fabulous Cabernet Franc — 4.1 (40)
- Plavi Perun · Chardonnay — 4.1 (66)
- Vinarija MK Kosović · Beli Bermet — 4.1 (25)
- Podrum Šukac · Merlot — 4.1 (31)
- Žarković · Мерлот (Merlot) — 4.1 (28)
- Митровиђ Винарија · Монограм (Monogram) — 4.1 (25)
- Intuicija · Tamjanika - Morava — 4.1 (32)
- Vinarija Timacvm Minvs · Cabernet Sauvignon — 4.1 (25)
- Virtus · Marselan — 4.0 (650)
- Art Wine · Tangenta Chardonnay — 4.0 (30)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Obecanje Pinot Noir — 4.0 (67)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Tam-Tam — 4.0 (65)
- Vinarija Lastar · Triangl Pinot Noir — 4.0 (121)
- Vinarija Lastar · Triagl Chardonnay — 4.0 (101)
- Vinarija Lastar · Sofijin Izbor Pinot Noir — 4.0 (42)
- Podrum Janko · Zavet Red Blend — 4.0 (137)
- PIK Oplenac · Monarh S — 4.0 (115)
- Vinarija Imperator · Maximianvs — 4.0 (204)
- Vinarija Imperator · Gratianus Traminac — 4.0 (93)
- Vinarija Imperator · Grašac — 4.0 (66)
- Vinarija Imperator · Maq I Primus — 4.0 (30)
- Vinarija 100 Žena · Mlad Momak Merlot — 4.0 (93)
- Tri Oraha · Chardonnay — 4.0 (57)
- Винарија Манастира Буково · Filigran Gamay (Филигран Гаме) — 4.0 (113)
- Vila Vina · Jefimija — 4.0 (30)
- Vinarija Eden · Velvet — 4.0 (170)
- Vinarija Eden · Vivid Sauvignon Blanc — 4.0 (91)
- Quet · Cuvée — 4.0 (88)
- Quet · Traminac — 4.0 (57)
- Vinarija Grumen · Rhine Riesling — 4.0 (29)
- BT Winery · President Vranac Gold — 4.0 (143)
- BT Winery · King Supreme Winemaker's Selection No.1 Pinot Noir — 4.0 (45)
- Galot · Chardonnay — 4.0 (35)
- Vinarija Todorović · Shiraz — 4.0 (103)
- Vinarija Todorović · Merlot — 4.0 (83)
- Vinarija Todorović · Tod'Orange — 4.0 (73)
- Château Prince · Shiraz Premium — 4.0 (37)
- Podrum Đorđević · Tamjanika — 4.0 (107)
- Podrum Đorđević · Bravura Cuvée — 4.0 (107)
- Vinarija Frug · Sauvignon Blanc — 4.0 (66)
- Aleksandar Todorović · Doodle White — 4.0 (99)
- Aleksandar Todorović · Župljanka — 4.0 (45)
- Aleksandar Todorović · Doodle Roze — 4.0 (25)
- Bajilo · Sila — 4.0 (99)
- Tri Medje I Oblak · Vagabundo Crveno — 4.0 (94)
- Tri Medje I Oblak · Pagan Roze — 4.0 (26)
- Pusula · Traminac — 4.0 (67)
- Podrum Madžić · Merlot Limited — 4.0 (275)
- Podrum Madžić · The Rosé Merlot — 4.0 (29)
- Podrum Pevac · Загрљај (Embrace) Cabernet Franc - Cabernet Sauvignon — 4.0 (63)
- Краљвеска Винарија (Royal Winery) · Pinot Blanc — 4.0 (26)
- Костић (Kostić) · Cuvée — 4.0 (28)
- Rnjak · Pinot Noir — 4.0 (127)
- Vinarium · Crna Tamjanika — 4.0 (31)
- Vinarija Frunza Aglaja · ΑΓЛΑЈΑ Cabernet Sauvignon — 4.0 (88)
- Probus Vineyards · Smells Like Love Chardonnay — 4.0 (25)
- Mcculloch Wines · Pinot Noir — 4.0 (33)
- Манастир Студеница (Manastir Studenica) · Бели Рец Тамјаника (Bela Reč Tamjanika) — 4.0 (70)
- Vinarija Đurđevića Legat · Do Neba i Nazad Belo — 4.0 (53)
- Serbika Wine · Sunce Rizling — 4.0 (27)
- Vinarija Dumo · Blanc de Noir Pinot Noir — 4.0 (27)
- Miletic · Impresija Sauvignon Blanc — 4.0 (31)
- Reljić Vinarija · Rebus Belo — 4.0 (39)
- Vilimonovic · Tamjanika — 4.0 (105)
- Katanic · Leon Chardonnay — 4.0 (44)
- Tenuta Est Winery · Nera Crna Tamjanika — 4.0 (35)
- MV Vinarija · Hope Special Edition Organic — 4.0 (66)
- Stari Dani · Dert Cabernet Sauvignon - Merlot — 4.0 (98)
- Petica · Tvrđava Cabernet Sauvignon — 4.0 (131)
- Dalia · Splet Gamay - Vranac — 4.0 (65)
- Dalia · Trač Traminac — 4.0 (36)
- Dalia · Gaamez Gamay — 4.0 (29)
- Vinarija Sokolov Zamak · Tamjanika — 4.0 (43)
- Vinarija Savic · Tamjanika — 4.0 (41)
- Chicha · Zlatna Reserva Cabernet Sauvignon — 4.0 (54)
- Chicha · Reserva Cabernet Sauvignon — 4.0 (35)
- ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) · Крокан (Krokan) — 4.0 (73)
- Podrum Panajotovic · Victor Barrique — 4.0 (47)
- Vert · Rhine Riesling — 4.0 (41)
- Амбелос Винарија (Ambelos Winery) · Тамјаника — 4.0 (47)
- Три Планине (Vinarija Tri Planine) · Поноћна Прича (Midnight Story) — 4.0 (33)
- Status · Vranac — 4.0 (36)
- Винарија Тришић (Vinarija Trišić) · Тришино (Triša's) — 4.0 (50)
- Varina · Prokupac — 4.0 (28)
- Винарија Живковића (Vinarija Živkovića-Tržac) · Тамјаника (Tamjanika) — 4.0 (38)
- Vinarija Bogunovic · Cabernet Sauvignon — 4.0 (44)
- Vinska Kuća Rajić · Tamjanika — 4.0 (35)
- Virtus · Gewürztraminer — 3.9 (310)
- Virtus · Mlavac Crveni — 3.9 (144)
- Milijan Jelić · Kameničanka Prokupac — 3.9 (230)
- Grabak · Ćuk Merlot — 3.9 (33)
- Grabak · Modrovrana — 3.9 (75)
- Vinarija Panjković · Mudrost — 3.9 (27)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Poema — 3.9 (409)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Tajna Rouge — 3.9 (115)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Brut — 3.9 (79)
- Virtus · Morava — 3.9 (43)
- Vinarija Lastar · Merlot - Cabernet Franc — 3.9 (249)
- Vinarija Lastar · Riesling — 3.9 (83)
- Vinarija Lastar · Brut — 3.9 (35)
- Milijan Jelić · Mammoth Pinot Noir — 3.9 (277)
- Podrum Janko · Zavet — 3.9 (314)
- Podrum Janko · Bas Prokupac (Баш Прокупац) — 3.9 (198)
- Podrum Janko · Misija Barrique Chardonnay — 3.9 (34)
- Podrum Janko · Mesečina Penušavo Belo — 3.9 (33)
- PIK Oplenac · Constanta Muse Rosé — 3.9 (143)
- PIK Oplenac · Monarh Cabernet Sauvignon — 3.9 (62)
- Kalem · 1892 Dominant Prokupac — 3.9 (27)
- Vinarija Imperator · Valerius Rajnski Rizling — 3.9 (207)
- Vinarija Imperator · Cargraš Grašac — 3.9 (33)
- Vinarija 100 Žena · Shao Linda Orange — 3.9 (74)
- Tri Oraha · Classic — 3.9 (35)
- Botunjac · Pino Botunjac Pinot Noir — 3.9 (366)
- Botunjac · Sveti Gral Prokupac — 3.9 (202)
- Vila Vina · Barrique Cabernet Sauvignon — 3.9 (65)
- Vinarija Komuna · Muscat Petit Grain — 3.9 (250)
- Quet · Pinot Noir — 3.9 (43)
- Vinarija Grumen · Petit Verdot — 3.9 (193)
- BT Winery · Tam Tam — 3.9 (105)
- BT Winery · Fingerprint Collection Tamjanika — 3.9 (52)
- Nikad Nije Kasno · Melodija — 3.9 (94)
- Vinarija Todorović · Sauvignon Blanc — 3.9 (57)
- Vinarija Todorović · Chardonnay — 3.9 (60)
- Vinarija Todorović · Cabernet Sauvignon — 3.9 (36)
- Château Prince · Château Shiraz — 3.9 (142)
- Château Prince · Magija Rosé — 3.9 (94)
- Podrum Đorđević · Chardonnay — 3.9 (90)
- Dolina · Barrique Crveno Suvo — 3.9 (227)
- Bajilo · Bermet — 3.9 (118)
- Stemina · Panta Rei Chardonnay — 3.9 (91)
- Stemina · Stephanos Kruna — 3.9 (92)
- Stemina · Minna Rosé — 3.9 (84)
- Tri Medje I Oblak · Grašac Beli — 3.9 (122)
- Tri Medje I Oblak · Vagabundo Belo — 3.9 (75)
- Vinarija Mrdjanin · Sila — 3.9 (79)
- Vinarija Mrdjanin · Cabernet Sauvignon — 3.9 (37)
- Vinarija Mrdjanin · Chardonnay — 3.9 (29)
- Podrum Pevac · Гушт Шардоне (Guešt Chardonnay) — 3.9 (64)
- Podrum Pevac · Гушт Шардоне Барик (Guešt Chardonnay Barik) — 3.9 (26)
- Plavinci · Ćilibar — 3.9 (77)
- Plavinci · Selena Tamjanika — 3.9 (81)
- Краљвеска Винарија (Royal Winery) · Cabernet Sauvignon — 3.9 (194)
- Rnjak · Sauvignon Blanc — 3.9 (63)
- Rnjak · Cabernet Sauvignon — 3.9 (33)
- Vinarium · Beloš — 3.9 (46)
- Vinarija Frunza Aglaja · Аглаја Sauvignon Blanc - Semillon (Aglaja) — 3.9 (71)
- Vinarija Frunza Aglaja · Аглаја Chardonnay (Aglaja) — 3.9 (34)
- Probus Vineyards · Impossible Pet-Nat — 3.9 (76)
- Mcculloch Wines · Traminac — 3.9 (73)
- Vinarija PIRG · Vranac — 3.9 (38)
- The Collective Presents · Szerémi Sárgamuskotály — 3.9 (28)
- Магаза (Magaza) · Merlot — 3.9 (85)
- Магаза (Magaza) · Chardonnay Barrique — 3.9 (36)
- Vista Hill · Selection Red — 3.9 (52)
- Vinarija Dumo · Pinot Noir — 3.9 (181)
- Tenuta Est Winery · Stara Kupaža — 3.9 (37)
- Stari Dani · Basma Pinot Noir — 3.9 (26)
- Karić Vinarija · Adria Belo — 3.9 (162)
- Rogan · Shiraz — 3.9 (139)
- Vinarija Sokolov Zamak · Marselan — 3.9 (78)
- Salaxia · Bela Vrana Pinot Grigio — 3.9 (36)
- Traško Vinarija · Bagrina Edición Limitada — 3.9 (36)
- Подрум вина Рашковић - (Rašković Winery) · Мегдан (Megdan) — 3.9 (66)
- Vinarija Gamanović · Grašac Beli — 3.9 (55)
- Vinarija Gamanović · Cabernet Sauvignon — 3.9 (25)
- Vinarija Radoslav Tripković · Pesak Plavi — 3.9 (34)
- Vinarija Bela Kula · Askurđel — 3.9 (25)
- Vinarija Bela Kula · Burgundac Sivi — 3.9 (26)
- Винарија Ступови (Vinarija Stupovi) · Cabernet Sauvignon — 3.9 (27)
- Vinarija Frunza Aglaja · Cabernet Sauvignon — 3.9 (63)
- Vinarija Novak (Новак) · Багрина (Bagrina) — 3.9 (50)
- Vinarija Vojnović · Пунаjeдpa (Puna Jedra) — 3.9 (27)
- Virtus · Pinot Grigio — 3.8 (223)
- Virtus · Sauvignon Blanc — 3.8 (148)
- Virtus · Prokupac — 3.8 (561)
- Milijan Jelić · Morava — 3.8 (852)
- Milijan Jelić · Morange — 3.8 (178)
- Grabak · Prva Lasta — 3.8 (36)
- Vinarija Jeremic · Rondo Rosé — 3.8 (48)
- Vinarija Jeremic · Sonata Sauvignon Blanc — 3.8 (488)
- Vinarija Panjković · Radost — 3.8 (29)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Obecanje — 3.8 (467)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Tajna Blanc — 3.8 (198)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Želja — 3.8 (93)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Brut Macéré — 3.8 (31)
- Vinarija Lastar · Chardonnay — 3.8 (332)
- Vinarija Lastar · Cru 6 — 3.8 (98)
- Vinarija Lastar · Rose — 3.8 (50)
- Milijan Jelić · Slovenski San Kameničanka — 3.8 (59)
- Podrum Janko · Misija Chardonnay — 3.8 (131)
- Podrum Janko · Sauvignon Blanc — 3.8 (90)
- PIK Oplenac · Monarh Immortal S — 3.8 (404)
- PIK Oplenac · Monarh Immortal Cabernet Sauvignon — 3.8 (151)
- PIK Oplenac · Constanta Muse Chardonnay — 3.8 (116)
- PIK Oplenac · Monarh Cuvée — 3.8 (110)
- PIK Oplenac · Constanta Muse Sauvignon Blanc — 3.8 (89)
- PIK Oplenac · Villa Nota Chardonnay — 3.8 (62)
- PIK Oplenac · Monarh Immortal Merlot — 3.8 (40)
- Vinarija Jeremic · Duetto Smederevka - Tamnjanika — 3.8 (57)
- Braca Rajkovic · Sofia Tamjanika — 3.8 (333)
- Vinarija Imperator · Sila Nika — 3.8 (56)
- Vinarija 100 Žena · Veliki Dečko — 3.8 (206)
- Vinarija 100 Žena · Crna Ovca Franc - Cabernet Franc — 3.8 (83)
- Винарија Манастира Буково · Филигран Црна Тамјаника (Filigree Crna Tamjanika) — 3.8 (194)
- Vinarija DeLena · Rosélena — 3.8 (28)
- Vila Vina · Tamjanika — 3.8 (337)
- Vinarija Eden · Semillon — 3.8 (42)
- Vinarija Komuna · Chardonnay — 3.8 (183)
- Vinarija Komuna · Merlot — 3.8 (101)
- Vinarija Komuna · Rajnski Rizling — 3.8 (85)
- Podrum Stari Hrast · Sauvignon Blanc — 3.8 (201)
- Podrum Stari Hrast · Chardonnay — 3.8 (61)
- Podrum Stari Hrast · Merlot — 3.8 (60)
- Quet · Pinot Noir Rosé — 3.8 (29)
- Vinarija Grumen · Sauvignon Blanc — 3.8 (185)
- Vinarija Grumen · Chardonnay — 3.8 (105)
- Vinarija Grumen · Merlot — 3.8 (63)
- BT Winery · Vranac Red Dry — 3.8 (63)
- Milanović · Probus — 3.8 (321)
- Zmajevac · Chardonnay — 3.8 (54)
- Galot · Cabernet Sauvignon — 3.8 (41)
- Vinarija Todorović · Vranac — 3.8 (51)
- Vinarija Todorović · Opus — 3.8 (29)
- Château Prince · CharM — 3.8 (88)
- Podrum Đorđević · Sauvignon Blanc — 3.8 (101)
- Dibonis Winery · Di Shiraz — 3.8 (130)
- Monastery Visoki Decani  (Манастирско Дечанско) · Red (Црвени) — 3.8 (447)
- Do Kraja Sveta · Merlot — 3.8 (166)
- Do Kraja Sveta · Sauvignon Blanc — 3.8 (38)
- Pusula · Cabernet Cuvee — 3.8 (56)
- Vinarija Mrdjanin · Rosse — 3.8 (33)
- Plavinci · Indigo Regent — 3.8 (87)
- Краљвеска Винарија (Royal Winery) · Sauvignon Blanc — 3.8 (78)
- Mcculloch Wines · Merlot - Malbec — 3.8 (65)
- Vista Hill · Premium Rosé — 3.8 (68)
- Tenuta Est Winery · Bianco Chardonnay — 3.8 (40)
- Damjanovic · Gar Barrique Cabernet Sauvignon - Merlot — 3.8 (72)
- Vinarija Savic · Prokupac — 3.8 (42)
- Chicha · Reserva Merlot — 3.8 (37)
- Три Планине (Vinarija Tri Planine) · Боjа Зоре (Dawn Color) — 3.8 (28)
- Podrum Tošići · Ponoc Cabernet Sauvignon — 3.8 (49)
- Podrum Tošići · Nesanica Tamjanika — 3.8 (37)
- Krstašica Doo · Sauvignon Blanc — 3.8 (59)
- Krstašica Doo · Merlot — 3.8 (43)
- Plavi Perun · Pinot Noir — 3.8 (34)
- Vinarija Vrbica · Barriques — 3.8 (30)
- Драгић Винарија (Vina Dragic) · Аурора (Aurora) — 3.8 (39)
- Vinogradi Nikolic · Прокупац (Prokupac) — 3.8 (70)
- Nelt · Doba Cabernet Franc — 3.8 (40)
- M. Dubrana - N. Scheidt · Exode Blanc — 3.8 (27)
- Мали Подрум Гајић - Mali Podrum Gajić · Црвени Витез (Crveni Vite) — 3.8 (35)
- Grabak · Grabak Prokupac — 3.7 (70)
- Grabak · Bela Galubica — 3.7 (61)
- Art Wine · Sumarum Merlot — 3.7 (50)
- Francuska Vinarija - Estelle et Cyrille Bongiraud · Istina — 3.7 (534)
- Брояница (Brojanica) · Рислинг (Riesling) — 3.7 (1024)
- Vinarija Lastar · Pinot Noir — 3.7 (530)
- Milijan Jelić · Barrique Chardonnay — 3.7 (78)
- Milijan Jelić · Eva — 3.7 (50)
- Milijan Jelić · Tamuz Frankovka Barrique — 3.7 (30)
- Podrum Janko · Zapis Rajnski Rizling — 3.7 (32)
- PIK Oplenac · Villa Nota Muscat Ottonel — 3.7 (112)
- PIK Oplenac · Monarh Immortal Cuvée — 3.7 (70)
- PIK Oplenac · Tron Rosé — 3.7 (75)
- PIK Oplenac · Villa Nota Rosé — 3.7 (25)
- Kalem · Poluslatko Roze — 3.7 (100)
- Kalem · Rosé — 3.7 (56)
- Braca Rajkovic · Sofia Cuvée — 3.7 (157)
- Braca Rajkovic · Sofia Rosé — 3.7 (48)
- Vinarija Imperator · Claudius Sauvignon Blanc — 3.7 (43)
- Botunjac · Rasplet Riesling Italico — 3.7 (36)
- Vila Vina · Prokupac — 3.7 (225)
- Podrum Stari Hrast · Cabernet - Merlot — 3.7 (188)
- Milanović · Sila — 3.7 (196)
- Galot · Gala Extra Brut — 3.7 (69)
- Château Prince · Dobra Vila Tamjanika — 3.7 (46)
- Dibonis Winery · Di Merlot — 3.7 (30)
- Dolina · Crveno Suvo — 3.7 (167)
- Do Kraja Sveta · Cabernet Sauvignon — 3.7 (61)
- Pusula · Chardonnay — 3.7 (34)
- Vinarija Mrdjanin · Grašac — 3.7 (28)
- Rnjak · Chardonnay — 3.7 (30)
- Vinarium · Dedovac — 3.7 (70)
- Vinarium · Pinoranž — 3.7 (66)
- Mcculloch Wines · Rajnski Riesling — 3.7 (41)
- Serbika Wine · Rizling — 3.7 (122)
- Serbika Wine · Vranac — 3.7 (84)
- The Collective Presents · Szerémi Kékfrankos — 3.7 (125)
- Ilic Nijemcevic · Chardonnay — 3.7 (56)
- Ilic Nijemcevic · Sauvignon Blanc — 3.7 (50)
- Miletic · Impresija Cabernet Sauvignon — 3.7 (42)
- Damjanovic · Dry Red — 3.7 (65)
- Podrum Petrović · Sila — 3.7 (63)
- Vinarija Piano · Cabernet Sauvignon - Merlot — 3.7 (58)
- Mikić · Cuvée I — 3.7 (34)
- Vinarija Radoslav Tripković · Vrt Pesak Žuti — 3.7 (25)
- Vinarija Vrbica · Barrique — 3.7 (35)
- Patkov Vinograd · Majstor i Margarita — 3.7 (36)
- Probus Vineyards · Sremski Karlovci Venera — 3.7 (32)
- Vinarija Đorđe · Фреска Бела (Freska White) — 3.7 (25)
- Andrića Vinograd · Consul Prokupac - Merlot — 3.7 (48)
- Vinarija Burma Fruška Gora · Neoplanta — 3.6 (26)
- Брояница (Brojanica) · Вранац Красное Сухое (Vranac Red Dry) — 3.6 (1759)
- Брояница (Brojanica) · Каберне Совиньон (Cabernet Sauvignon) — 3.6 (130)
- Virtus · Rosé — 3.6 (48)
- PIK Oplenac · Tron Red — 3.6 (185)
- PIK Oplenac · Tron White — 3.6 (82)
- PIK Oplenac · Tron Cabernet Sauvignon — 3.6 (53)
- PIK Oplenac · Villa Nota Traminac — 3.6 (40)
- PIK Oplenac · Villa Sauvignon Blanc — 3.6 (25)
- Vinarija Jeremic · Duet Beli Smederevka - Sauvignon Blanc — 3.6 (28)
- Kalem · Rizling — 3.6 (730)
- Kalem · Vranac — 3.6 (511)
- Kalem · Impuls Vranac — 3.6 (172)
- Botunjac · Jagoda Botunjac — 3.6 (258)
- Vila Vina · Sauvignon Blanc — 3.6 (38)
- Dibonis Winery · Di Franc — 3.6 (66)
- Pusula · Sauvignon Blanc — 3.6 (109)
- Podrum Pevac · Прокупац (Prokupac) — 3.6 (32)
- Vinarium · Župljanka — 3.6 (44)
- Serbika Wine · Simbol Rose — 3.6 (29)
- Vista Hill · Selection White — 3.6 (32)
- Boemi · Sauvignon Blanc — 3.6 (128)
- Ilic Nijemcevic · Frankovka — 3.6 (46)
- Miletic · Impresija Merlot — 3.6 (36)
- Vinski Dvor · Bermet Crni — 3.6 (27)
- Подрум вина Рашковић - (Rašković Winery) · Тамјаника (Tamjanika) — 3.6 (27)
- Vinarija Radoslav Tripković · Pesak Sivi — 3.6 (31)
- Milisavljević · Karo Nero Pinot Noir — 3.6 (33)
- Patkov Vinograd · Князь Мышкин — 3.6 (49)
- Vinarija Salaš Naš · Chardonnay — 3.6 (32)
- Ukusi Moga Kraja · Prokupac — 3.6 (45)
- Robert Rudinski · Rizling — 3.6 (62)
- Moderato · Cabernet — 3.6 (38)
- Dulka · Bermet — 3.6 (27)
- Vinogradi Veličković Vinarija · Prvo Belo Sauvignon Blanc — 3.6 (34)
- Milijan Jelić · Adam — 3.5 (71)
- Podrum Janko · Smederevka — 3.5 (111)
- Podrum Janko · Jelena Rosé — 3.5 (45)
- PIK Oplenac · Monarh Merlot — 3.5 (59)
- PIK Oplenac · Villa Chardonnay — 3.5 (50)
- Kalem · 1892 Tamjanika — 3.5 (37)
- Kalem · 1892 Sauvignon Blanc — 3.5 (25)
- Braca Rajkovic · Prince Rskavac — 3.5 (173)
- Vinska Kuća Minića · Dorotej Pinot Noir — 3.5 (31)
- Vila Vina · Cabernet Sauvignon — 3.5 (83)
- Vinarija Komuna · Rosé — 3.5 (79)
- Milanović · Neoplanta — 3.5 (47)
- Galot · Sauvignon Blanc — 3.5 (28)
- Podrum Đorđević · Merlot - Cabernet Sauvignon — 3.5 (102)
- Perun Wine · Вранац — 3.5 (250)
- Perun Wine · Ризлинг (Riesling) — 3.5 (261)
- Bajilo · Cabernet Sauvignon — 3.5 (64)
- Grabak · Plava Paunica — 3.5 (31)
- The Collective Presents · Szerémi Mézes Fehér — 3.5 (37)
- Boemi · Cabernet Sauvignon — 3.5 (80)
- Ilic Nijemcevic · Cabernet Sauvignon — 3.5 (28)
- Damjanovic · Damjan Barrique Sauvignon Blanc — 3.5 (28)
- Enigma · White — 3.5 (42)
- Enigma · Rosé — 3.5 (32)
- Козарак · Хамбург (Hamburg) — 3.5 (41)
- Vinarija Salaš Naš · Merlot — 3.5 (29)
- Vinokratija · Mangup Cabernet Sauvignon — 3.5 (32)
- ODPF-Radmilovac · Rektorsko Cabernet Sauvignon — 3.5 (47)
- WinEco · Podrum Carigrad — 3.5 (29)
- Milijan Jelić · Tamuz Crveno — 3.4 (29)
- Vila Vina · Rose — 3.4 (35)
- Navip · Muscat Ottonel — 3.4 (45)
- Bajilo · Neoplanta Bajilo — 3.4 (26)
- Do Kraja Sveta · Mlad Mesec Belo — 3.4 (66)
- Pusula · Cabernet Sauvignon — 3.4 (60)
- Pusula · Rose — 3.4 (44)
- Agrina · Portuguiser — 3.4 (225)
- Nikolas · Žilavka — 3.4 (60)
- Sava Minić · Tamjanika — 3.4 (103)
- Enigma · Red — 3.4 (67)
- Vina Pešić · Tamjanika — 3.4 (30)
- Sunčani Breg · Sauvignon Blanc — 3.4 (26)
- Navip · Cabernet Sauvignon — 3.3 (172)
- Fruškogorski · Fruškać Crveni — 3.3 (59)
- Fruškogorski · Fruškać Beli — 3.3 (40)
- Status · Калча (Kalča) — 3.3 (26)
- Vinarija Vojinović · Istina Réservée — 3.3 (27)
- PIK Oplenac · Tron Cuvée — 3.2 (25)
- Dolina · Rosé — 3.2 (28)
- Do Kraja Sveta · Mlad Mesec Crveno — 3.2 (75)
- Milisavljević · Cuvée Mistique — 3.2 (36)
- Vinarija Selecta · Pinot Noir — 3.2 (28)
- Navip · Riesling Fruška Gora — 3.1 (56)
- Брояница (Brojanica) · Шардоне (Chardonnay) — 3.1 (28)
- Milijan Jelić · Baby Mammoth — 3.1 (28)
- Navip · Adria Muscat Ottonel — 3.1 (95)
- Vina Pešić · Sauvignon Blanc — 3.1 (32)
- Козарак · Рислинг (Riesling) — 3.1 (33)
- Kalem · Graševina — 3.0 (37)
- Nikolas · Vranac — 3.0 (115)
- Navip · Riesling Italico — 2.9 (71)
- Navip · Merlot Dionis — 2.9 (40)
- Vinex Grozd · Vranac Suvo Crveno — 2.9 (103)
- Vinex Grozd · Vranac Poluslatko Crveno — 2.8 (43)
- Ukusi Moga Kraja · Tamjanika — 2.8 (46)
- Sava Minić · Prokupac — 2.7 (68)

