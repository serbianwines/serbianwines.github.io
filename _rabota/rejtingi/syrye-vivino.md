# Сырые выписки Vivino

Как собрано: прямой доступ к vivino.com из рабочей среды закрыт (см. README.md
в этом каталоге). Данные получены через поиск с ограничением по домену
`vivino.com`: поисковая выдача возвращает адреса страниц и краткие выжимки,
в которых встречаются оценки, а иногда и число отзывов.

**Чему здесь можно верить.** Адресам страниц и идентификаторам вин (`/w/<id>`) —
да, они приходят из выдачи как есть. Оценкам по отдельным винам — с оговоркой:
это пересказ, а не значение из API. Числу отзывов на уровне хозяйства — нет:
формулировка «3 wines and 3.8 rating based on 69 total ratings» пришла дословно
одинаковой для Mačkov Podrum, Zvonko Bogdan и Maurer, то есть это шаблон
страницы, а не их данные. Такие числа ниже помечены как негодные.

Всё, что здесь записано, — заготовка для скрипта `sobrat-rejtingi.py`,
который добирает точные значения по идентификаторам.

---

## Фрушка гора (Vivino: Srem, Fruška Gora)

**Vinarija Deurić** — `/wineries/vinarija-deuric`
Chardonnay 4,1 (533) · Marmalade Orange 4,0 (821) · Aksiom 4,0 (68) · Probus 276 3,9 (107) ·
Aksiom Beli 3,9 · Severna Morava 3,9 · Avangarda 3,8 · Urban Rosé 3,7 · Classic Chardonnay 3,7 ·
Pinot Noir 3,7 · Gewürztraminer / Merlot / Sauvignon Blanc / Talas Beli / Talas Crveni 3,6.
Замечание: платиновой *La Rem Chardonnay 2023* и *La Rem Morava 2023* в выдаче нет вовсе.

**Vinčić** — Grand Fru 4,0 · Grašac — «недостаточно оценок».
Замечание, важное для книги: грашац Vinčić взял Best in Show Decanter 2023, а на Vivino у него
оценки нет. Совпадения между конкурсом и народным рейтингом ждать не приходится.

**Erdevik** — `/wineries/erdevik`
Omnibus Lector Chardonnay 4,3 · Grand Trianon 4,3 · Marlon Delon Cab.Sauv.-Merlot 4,3 ·
Stifler's Mom Shiraz 4,3 · Roza Nostra 4,1 (2019 — 4,3) · Trianon 4,1.

**Vinarija Kovačević** — `/wineries/vinarija-kovacevic` · около 40 вин, средняя 3,9, порядка 12–14 тыс. оценок
Edicija S Aurelius 4,2 · Edicija R Chardonnay 4,2 · Edicija R Sauvignon 4,1 · Edicija S Sauvignon 4,1 ·
Aurelius 3,9 · Brut 3,9 · Chardonnay 3,9 · Sauvignon 3,9 · Cuvée Blanc 3,9 · Cuvée Piquant 3,7 · Cuvée Rouge 3,5.

**Mačkov podrum** — `/wineries/mackov-podrum`
Frajla Rosé 3,5 · Camerlot 3,5 · Mirisavi Traminac 3,5 · Sauvignon Blanc 3,5 · Chardonnay 3,4 ·
Incognito 3,4 · Merlot 3,3 · Portugizer 3,0 · Pinot Noir и Mačkov Bermet Diškrecija — мало оценок.

**Bikicki** — `/wineries/bikicki`
Victor 4,1 · Sfera Noir 4,1 · Makana 4,0 · Uncensored 4,0 · Lily 4,0 · Nikka 4,0 ·
Crna Tamjanika 3,9 · S/O 3,9 · Sfera 3,9 · Cu 3,8 · Pinotte 3,8.

**Vinarija Đurđić** — `/wineries/vinarija-durdic`
Probus 4,1 · Cabernet Franc 4,0 · Traminac 3,9 · Simonida Mlada 3,9 · Neoplanta 3,9 ·
Crni Vitez Bermet 3,8 · Sauvignon Blanc 3,8.

**Veritas Ćuković** — `/wineries/veritas-srem`
Momentum Cabernet Sauvignon 4,4 · Ćuk Cuvée Dry Red 4,0 · Bela Hormonya 4,0.
(Momentum 2017 — золото Decanter 2026.)

Из региональной страницы `/wine-regions/srem` дополнительно: Molovin — Inat Traminac 4,1,
Inat Frankovka 3,9. В книге Molovin не назван.

## Суботичско-Хоргошская пешчара

**Maurer** — `/wineries/maurer`
Kadarka Gravitation 4,3 · Kadarka Nagy-Krisztus 4,2 · Oszkar Babba 4,2 · Oszkar Karom 4,1 ·
Sott 4,1 · Tamjanika 4,1.

**Zvonko Bogdan** — `/wineries/zvonko-bogdan`
Icon Campana Rubimus 4,3 · Merlot 4,1 · Cuvée No.1 4,1 · Icon Campana Albus 4,1 ·
Chardonnay 4,0 · Rosé Sec 4,0 · Sauvignon Blanc 3,8.
Двух золотых медалей Decanter 2026 — *Chardonnay 2022* и *Éclater Blanc de Blancs
Brut Nature 2018* — в выдаче отдельными позициями нет.

**Tonković** — `/wineries/vinarija-tonkovic`
Rapsodija Kadarka 3,9 (322) · Fantazija Kadarka 3,8 (857) · Kadarka Rosé 3,7 (127) ·
Allegro Kadarka Blanc de Noir 3,6 (114).
Здесь числа отзывов пришли по каждому вину — из всей выборки это самый надёжный кусок.

**Petra** — `/wineries/vinarija-petra` — страница есть, оценок выдача не показала.

## Банат

**Vršački vinogradi** — `/wineries/vrsacki-vinogradi`
Banatski Rizling 3,3; у Burgundac Beli, Kutres Chardonnay, Vršački Rizling Kasna Berba,
Muscat Ottonel — «недостаточно оценок».

**Vinarija Drašković** — `/wineries/vinarija-draskovic`
Muskat Otonel 4,1 · Chardonnay 3,8 · Horizont Chardonnay 3,7 · Mahago 3,7 ·
Divlja Ruža Rosé 3,7 · Ruža Vetrova Muskat Otonel 3,7 · Beli Pinot 3,6 ·
Triptih 3,5 · Rosé 3,5.

**Galot, Rnjak** — на Vivino не нашлись.

## Шумадия

**Aleksandrović** — `/wineries/aleksandrovic`
Rodoslov Reserve 4,3 · Trijumf Gold 4,2 · Vizija Selection 4,1 · Trijumf Selection 4,1 ·
Trijumf Noir Brut 4,1 · Harizma Selection 4,0.
Замечание: платиновой *Kameničarka Prokupac 2022* в выдаче нет; Aleksandrovic Prokupac — 4,2.

**Radovanović** — `/wineries/radovanovic` · 20 вин, порядка 6 977 оценок
Réserve Special Cab.Sauv. 4,4 · Réserve Cab.Sauv. 4,3 · Grand Reserve Cab.Sauv. 4,3 ·
Cabernet Sauvignon 4,3 · Pino Sivi 4,1 · Cab.Sauv. Classique 3,8 · Sovinjon 3,3.

**Tarpoš** — `/wineries/tarpos` · 18 вин, средняя 4,0, 669 оценок
Lipar Sauvignon Blanc 4,2 (28) · Cabernet Sauvignon 4,1 (61) · Sauvignon Blanc 4,0 (71) ·
1804 Selekcija 4,0 (92) · Tarpos Merlot 4,0 (47) · Merlot 3,9 (73) · Cuvée Beli 3,9 (29) ·
Tamjanika 3,8 (37) · Menuet Chardonnay 3,8 (33) · Cuvée 3,6 (38).
Золотой *Chardonnay Extra Brut 2021* в выдаче не встретился.

**Despotika** — `/wineries/despotika-despotika`
Dodir Muscat Ottonel-Tamjanika 4,2 (460) · Morava Orange 4,1 (73) ·
Nemir Cab.Sauv.-Prokupac Rosé 4,0 (133) · Od Sorte Morava 4,0.

**Arsenijević** — `/wineries/arsenijevic`
Cabernet Sauvignon Limited Edition 4,2.

**Matijašević, Marko** — на Vivino не нашлись.

## Три Моравы и Жупа

**Temet** — `/wineries/temet`
Three Morave Rezerva 4,4 · Dobra Godina 4,3 · Three Bele 4,1 · Tri Morave White Rezerva 4,1 ·
Ergo Red / Tri Morave / Ergo White / Prokupac III / Three Morave Red — 3,9–4,0.

**Vinarija Ivanović** — `/wineries/vinarija-ivanovic`
No 1/2 — 4,3 · No 3/4 Tamjanika 4,2 · Tamjanika 3,9 · Prokupac 3,9 · Zanos, Serdar — мало оценок.

**Vino Budimir** — `/wineries/budimir` — страница есть, оценок выдача не показала.
Названы Svb Rosa, Triada, Tamjanika Slatka Mala.

**Vinogradi Veličković**, **Vinarija Vujić** (Тамјаника, `/w/7211859`) — страницы есть,
оценок нет. **Cilić**, **Fragaria**, **Yotta**, **Ralević** (кроме Vranac `/w/10623790`,
без оценки) — не нашлись.

**Vinarija Jovac** — `/wineries/vinarija-jovac`
Single Vineyard Stella Noir 4,3 · SV Selection Chardonnay 4,3 ·
SV Selection Tamjanika 4,2 · SV Selection Sauvignon Blanc 4,0.
(*Stella Noir 2020* — золото Decanter 2026.)

## Неготинска Крайина

**Matalj** — `/wineries/matalj-vinarija`
Kremen Kamen Cabernet Sauvignon 4,5 · Zemna Reserva 4,2 · Kremen Cabernet-Merlot 4,1 ·
Začinak Bukovski 4,1 · Kremen Cabernet Sauvignon 4,0 · Cuvée Bukovski 4,0 ·
Crna Tamjanika 4,0 · Kremen Kremenjača 4,0 · Bagrina Bukovska 3,9.

**Francuska vinarija** — `/wineries/francuska-vinarija-estelle-et-cyrille-bongiraud`
Страницы вин есть (Istina `/w/1549948`, Tajna Rouge `/w/1235717`, Obećanje `/w/1209871`,
Brut C `/w/13028713`, Brut Macéré, Tam-Tam), оценок выдача не показала.

**Vinarija Raj** — Crna Tamjanika `/w/4830021`, Bela Tamjanika `/w/7281899` — 3,7.

**Буково, Vimmid, Frunza Aglaja, Krajinska vinska zadruga** — не нашлись.

## Топлица

**Toplički vinogradi** — `/wineries/toplicki-vinogradi`
Gvozdeni Puk Rujno 4,3 (42) · Tribus Villa Sauvignon Blanc 3,8 (411) · Epigenia Prokupac 3,8 (148) ·
Epigenia Cabernet Sauvignon 3,8 (34) · Epigenia Sauvignon Blanc 3,7 (65) · Tribus Villa Pinot Noir 3,6 (26) ·
Tribus Villa Merlot Rosé 3,5 (325) · Tribus Villa Prokupac 3,5 (26) · Epigenia Chardonnay 3,4 (41) ·
Epigenia Merlot 3,2 (37).

**Doja** — `/wineries/doja-vinarija`
Breg Cabernet Sauvignon 4,3 · Breg Prokupac 4,1 · Breg Merlot 4,0 ·
Cab.Sauv.-Merlot 3,9 · Prokupac 3,9 · Tamjanika 3,9 · Belo Chardonnay-Pinot Grigio 3,7 · Rosé 3,5 (180).

## Юго-восток

**Aleksić** — `/wineries/aleksic`
Žuti Cvet 4,1 · Amanet Vranac 4,0 (в верхних 3% вин мира по формулировке Vivino) ·
Nostalgija и Limited Kardaš Cab.Sauv. — оценка в выдаче не показана.

**Džervin** — `/wineries/dzervin` · 11 вин, порядка 56 оценок суммарно
Schlossberg Merlot 3,9 · Sauvignon 3,9 · Rosé Romansa 3,5 · Despot Crveni 3,3 · Dubravka 3,0.
*Dubravka Gold* — отдельная страница `/w/13474065`, оценки нет. Это то самое вино
за 500 динаров из шпаргалки: в рознице оно есть, на Vivino его почти не отмечают.

**Vinarija Jović** — `/wineries/vinarija-jovic`
Vranac 4,0 (`/w/1849220`). *Vranac Potrkanjski* отдельной страницей не найден.

## Метохия

**Vinarija Lakićević** — `/wineries/vinarija-lakicevic` · 13 вин, средняя 4,2, 810 оценок
Cuvée No.5 Merula 4,3 · Parus Sauvignon Blanc 4,2 · Cuvée Alcedo 4,2 · Upupa Tamjanika 4,2 ·
Solaris 4,2 · Picus Chardonnay 4,1 · Picus Selection Chardonnay 4,1 · Cuvée No.1 Oriolus 4,1.

## Подунавье и Белградский район

**Janko** — `/wineries/janko`, **Vinarija Plavinac** — `/wineries/vinarija-plavinac`
(Merlot Barrique `/w/7968248`). Страницы есть, оценок выдача не показала.
**Trišić** — не нашлось.

Регион на Vivino пуст. Это не сбой поиска: три малых хозяйства Белградского
района там просто никто не отмечает.

## Общее по стране

Из страницы `/explore/countries/republic-of-serbia` верх страны выглядит так:
Radovanović Réserve Special Cab.Sauv. 4,4 · Temet Three Morave Rezerva 4,4 ·
Radovanović Réserve Cab.Sauv. 4,3 · Radovanović Grand Reserve Cab.Sauv. 4,3 ·
Temet Dobra Godina 4,3 · Arsenijević Cab.Sauv. Limited Edition 4,2 ·
Rubin Double Barrique Cab.Sauv. 4,1 · Rubin Double Barrique Sauvignon Blanc 4,1 ·
Maurer Tamjanika 2018 4,1.

Rubin (Крушевац) в книге не назван вовсе, а по числу оценок это одно из самых
заметных сербских хозяйств на Vivino. То же с Molovin, Trivanović, Živanović,
Vinis, Podrum Malča, Virtus, Vinogradi Nikolić, Grabak, Vila Vina, Milinčić,
Belo Brdo, Imperator, Grumen. Полный список таких имён скрипт складывает
в `hozyaistva_vne_knigi`.

## Как Vivino считает

Оценка пятибалльная, средняя взвешенная — число отзывов учитывается. Если
данных мало, оценка не показывается вовсе («not enough ratings»). Значок
«популярное» вино получает от тысячи отзывов; для Сербии эта планка не
работает — её берут единицы. Сама Vivino сопоставляет свои 4,0 с примерно
90 баллами по стобалльной шкале критиков.
