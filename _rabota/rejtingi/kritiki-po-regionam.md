# Оценки критиков

Вторая дорожка, независимая от Vivino. Здесь стобалльная шкала и оценка
эксперта, а не средняя по толпе.

**Почему отдельно, а не вместе.** У Vivino пятибалльная оценка покупателей,
и её вес определяется числом отметок. У критика вес определяется тем, что он
критик; порога по числу отзывов здесь нет и быть не может. Это две разные
величины, и в одно число они не складываются. Если рейтинги пойдут в книгу,
показывать их надо порознь и подписывать, что именно показано.

## Две вещи, а не одна

**Оценки** — балл по стобалльной шкале. Лежат в `kritiki-zapisi.jsonl`,
79 записей.

**Награды** — место в категории или медаль. У них нет шкалы, зато есть год
и категория. Лежат отдельно, в `nagrady-zapisi.jsonl`, 55 записей.
Переводить «лучшее белое из местных сортов 2025 года» в число нельзя,
поэтому и таблицы разные.

## Источники

**Falstaff** — австрийский гид, ведёт отдельный раздел «Tasting Serbien»
и ранжирует сорок сербских хозяйств по стобалльной шкале. Самый широкий
охват Сербии из всего, что нашлось: списки лучших красных (52 вина), белых
и розе, оценки по урожаям, звёзды хозяйствам. Дегустирует Peter Moser.

**Wine-Searcher** — не оценивает сам, а усредняет оценки критиков и взвешивает
их по числу отзывов и числу критиков. Ровно тот приём, что применён и к
Vivino в соседней дорожке.

**vino.rs** — годовой тест «Najbolja vina Srbije»: сотня винных
профессионалов, 31–33 категории, с 2019 года. Книга уже опирается на этот
выбор за 2025-й; здесь собраны четыре года, 2022–2025. Отдельно — оценки
в баллах от Зорана Рапајића.

**Decanter** — медали DWWA. По годам: 2023 — 103 медали (5 золота, 38 серебра,
59 бронзы), 2024 — 4 золота, 45 серебра, 67 бронзы, 2025 — 7 золота,
2026 — 3 платины, 7 золота, 58 серебра, 78 бронзы. Поимённо серебро и бронзу
достать не удалось: база наград на сайте рисуется сценарием и в кэш поиска
не попадает. Собраны платины, золото и то, что нашлось у сербских продавцов.

**Tastings.com** — Beverage Testing Institute, отдельные сербские вина.

**Decanter** — в книге уже разобран, сюда не дублируется.

## Что важно для книги

Falstaff закрывает ровно ту дыру, которую Vivino оставляет. Грашац Vinčić:
Best in Show Decanter, на Vivino оценки нет вовсе — у Falstaff *Grašac Grand
Fru 2020* стоит 95 баллов, а само хозяйство держит четыре звезды. То же с
Doja: четыре звезды и 95 баллов за *Prokupac Breg 2019* при том, что на
Vivino район еле наскребает пятёрку.

Иначе говоря: **Vivino показывает, что пьют, Falstaff — что сделано хорошо.**
Для справочника вторая величина ближе к делу.

## Чего нет

**Подунавье пусто и здесь.** Ни оценки, ни награды. Единственное, что рядом, —
золото Decanter 2025 у Virtus, но Decanter относит его к району Млава, а не
к Белградскому; входит ли Млава в главу «Подунавье», решать автору.

**Метохия — только награды**, баллов нет: у Lakićević три места в годовом
тесте vino.rs (2023, 2024, 2025) и ни одной стобалльной оценки.

**Юго-восток — одна оценка** (Aleksić Biser Extra Brut 2016, 91 Falstaff)
и две награды. У Džervin и Jović баллов нет вовсе.

Поимённого списка серебра и бронзы Decanter нет ни за один год — а это
136 медалей только за 2026-й. Достать их можно лишь из базы наград на сайте
конкурса, которая поиском не читается.

**Пересобрать файл:**

    cd _rabota/rejtingi
    cat kritiki-vstuplenie.md > kritiki-po-regionam.md
    python3 svesti-kritikov.py --markdown >> kritiki-po-regionam.md

---

<!-- Собрано скриптом svesti-kritikov.py. Руками не править. -->

## Фрушка гора

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Deurić · La Rem Chardonnay | 2023 | 97 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2015 | 97 | decanter |
| Vinčić · Grašac | — | 97 | decanter |
| Vinčić · Grašac Grand Fru | 2020 | 95 | Falstaff |
| Chichateau · Chi Chardonnay | 2018 | 95 | Falstaff |
| Vinum · Grašac 26a | 2019 | 93 | Falstaff |
| Erdevik · Grand Trianon | 2017 | 93 | Falstaff |
| Molovin · Inat Frankovka | 2019 | 93 | Falstaff |
| Bjelica · Graffiti | 2018 | 93 | Falstaff |
| Deurić · Aksiom Beli | 2019 | 92 | Falstaff |
| Erdevik · Grand Trianon Deux Mers | 2016 | 92 | Falstaff |
| Bikicki · Sfera Noir (натуральное) | 2021 | 92 | Falstaff |
| Deurić · The Brut | 2018 | 92 | Falstaff |
| Erdevik · Grand Trianon | — | 91 | Wine-Searcher |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | — | 91 | Wine-Searcher |
| Kovačević · Aurelius Edicija S | 2019 | 90 | Falstaff |
| Erdevik · Trianon | — | 89 | Wine-Searcher |
| Kovačević · Edicija S Aurelius | — | 86 | Wine-Searcher |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | золото | zlato | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2017 | 
| 2026 | золото | zlato | Veritas Ćuković · Momentum 2017 | 
| 2026 | платина | platina | Deurić · La Rem Chardonnay 2023 | 
| 2025 | лучшее белое, местные сорта | 1 | Deurić · La Rem Morava 2023 | 
| 2025 | лучшее красное, органика, международные сорта | 1 | Dukay-Sagmeister · Kadarka Kew 2022 | 
| 2024 | винодельня года | 1 | Kovačević | 
| 2024 | лучшая малая винодельня | 1 | Bikicki | 
| 2024 | лучшее белое, международные сорта | 1 | Kovačević · Sauvignon S Edicija 2021 | 
| 2024 | лучшее белое, органика, международные сорта | 1 | Dukay-Sagmeister · Furmint Kew 2020 | 
| 2023 | Best in Show | best-in-show | Vinčić · Grašac | 
| 2023 | винодельня года | 1 | Erdevik | 
| 2023 | вклад в винный туризм | 1 | Šapat | 
| 2023 | лучшее белое | 1 | Erdevik · Sauvignon Blanc Ex Cathedra 2021 | 
| 2023 | лучшее из местных сортов, белое | 1 | Vinčić · Grašac 2020 | 
| 2022 | лучшее белое | 1 | Deurić · Aksiom beli 2019 | 
| 2022 | лучшее игристое | 1 | Deurić · The 2019 | 
| 2020 | платина | platina | Erdevik · Omnibus Lector Chardonnay 2015 | 

## Суботичско-Хоргошская пешчара

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Maurer · Kadarka 1880 (натуральное) | 2021 | 95 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Merlot Single Vineyard | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2019 | 94 | Wine-Searcher |
| Zvonko Bogdan · Chardonnay | 2017 | 93 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2017 | 93 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2023 | 91 | Wine-Searcher |
| Tonković · Kadarka | — | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2022 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2021 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2018 | 90 | Wine-Searcher |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | золото | zlato | Zvonko Bogdan · Chardonnay 2022 | 
| 2026 | золото | zlato | Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature 2018 | 
| 2025 | лучшее белое, органика, местные сорта | 1 | Maurer · Karom 2023 | 
| 2024 | лучшее красное, органика, местные сорта | 1 | Maurer · Kadarka 1880 2022 | 
| 2023 | лучшее игристое | 1 | Zvonko Bogdan · Éclater 2018 | 
| 2017 | серебро | srebro | Tonković · Kadarka | 
| 2011 | бронза | bronza | Tonković · Fantazija Kadarka | 

## Банат

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Drašković · Beli Pinot | 2020 | 90 | decanter |
| Drašković · Horizont Chardonnay | 2021 | 89 | decanter |

_Наград не найдено._

## Шумадия

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 2022 | 97 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 94 | Falstaff |
| Matijašević · SoviNoa Fumé Blanc | 2020 | 94 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2020 | 93 | Falstaff |
| Aleksandrović · Trijumf Terroir | 2022 | 93 | Falstaff |
| Matijašević · SoviNoa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection | 2021 | 93 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 93 | Falstaff |
| Radovanović · Cabernet Sauvignon Reserve | 2019 | 92 | Falstaff |
| Aleksandrović · Trijumf Brut Rosé | 2019 | 92 | Falstaff |
| Matijašević · Prokupac Čukundeda | 2020 | 92 | Falstaff |
| Aleksandrović · Rodoslov Reserve | — | 91 | Wine-Searcher |
| Radovanović · Reserve Cabernet Sauvignon | 2013 | 91 | Tastings.com |
| Despotika · Morava | 2021 | 91 | Falstaff |
| Despotika · Zmajeviti Prokupac | — | 91 | Falstaff |
| Aleksandrović · Vizija Selection | 2020 | 91 | Falstaff |
| Radovanović · Réserve Cabernet Sauvignon | — | 90 | Wine-Searcher |
| Radovanović · Classique Cabernet Sauvignon | 2015 | 90 | Tastings.com |
| Despotika · Nemir rosé | 2024 | 89 | Falstaff |
| Despotika · Dodir Tamjanika | 2022 | 89 | Falstaff |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | золото | zlato | Tarpoš · Chardonnay Extra Brut 2021 | 
| 2026 | платина | platina | Aleksandrović · Kameničarka Prokupac 2022 | 
| 2025 | лучшее белое, международные сорта | 1 | Matijašević · SoviNoa Fumé Blanc 2023 | 
| 2024 | лучшая молодая винодельня | 1 | Draganić | 
| 2024 | лучшее красное, международные сорта | 1 | Arsenijević · Cabernet Sauvignon 2020 | 
| 2024 | лучшее красное, местные сорта | 1 | Marko · Doajen Prokupac 2022 | 
| 2023 | лучшее красное | 1 | Radovanović · Cabernet Sauvignon Grand Reserva 2017 | 

## Три Моравы и Жупа

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Ivanović · Prokupac Gaga | 2017 | 96 | Falstaff |
| Temet · Tamjanika | 2016 | 95 | Falstaff |
| Temet · Tri Morave Belo Reserve | 2018 | 95 | Falstaff |
| Čokot · Prokupac Radovan 100% | 2020 | 94 | Falstaff |
| Temet · Tri Morave Crveno Reserve | 2009 | 94 | Falstaff |
| Ivanović · No 1/2 | 2019 | 94 | vino.rs |
| Temet · Tri Morave Crveno Reserve | 2019 | 94 | Falstaff |
| Budimir · Svb Rosa | 2009 | 94 | Falstaff |
| Čokot · Radovan 100% Prokupac | 2019 | 93 | Falstaff |
| Čokot · Tamjanika Radovan 100% | 2022 | 93 | Falstaff |
| Čokot · Tamjanika Experiment | 2022 | 92 | Falstaff |
| Ivanović · Tamjanika | 2022 | 92 | Falstaff |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | золото | zlato | Jovac · Stella Noir 2020 | 
| 2025 | лучшая малая винодельня | 1 | Ralević | 
| 2025 | лучшее красное, международные сорта | 1 | Ralević · Aurum 2020 | 
| 2025 | лучшее красное, органика, местные сорта | 1 | Vujić · Prokupac Gmitar 2021 | 
| 2024 | лучшее белое, местные сорта | 1 | Yotta · Hysteresis Tamjanika 2022 | 
| 2024 | лучшее белое, органика, местные сорта | 1 | Ivanović · No 3/4 2023 | 
| 2022 | лучшее красное | 4 | Budimir · Triada crveno 2020 | 

## Неготинска Крайина

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Matalj · Kremen Kamen | 2021 | 97 | decanter |
| Matalj · Zamna Cabernet Sauvignon | 2020 | 96 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2017 | 95 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2020 | 95 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2016 | 95 | Falstaff |
| Matalj · Bagrina Buksovska | 2022 | 94 | Falstaff |
| Matalj · Terasa Chardonnay | 2022 | 92 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | — | 92 | Wine-Searcher |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | платина | platina | Matalj · Kremen Kamen 2021 | 
| 2025 | винодельня года | 1 | Matalj | 
| 2025 | лучшее красное, местные сорта | 1 | Matalj · Bukovski Cuvee 2021 | 
| 2023 | лучшее из местных сортов, красное | 1 | Matalj · Bukovski Cuvee 2019 | 
| 2022 | лучшее красное | 5 | Manastir Bukovo · Filigran Merlot 2021 | 

## Топлица

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Doja · Prokupac Breg | 2019 | 95 | Falstaff |
| Doja · Cabernet Sauvignon Breg | 2019 | 94 | Falstaff |
| Doja · Merlot Breg | 2019 | 94 | Falstaff |
| Doja · Prokupac | 2019 | 93 | Falstaff |
| Doja · Chardonnay Barik | 2022 | 91 | Falstaff |
| Doja · Rosé | 2022 | 91 | Falstaff |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2024 | вклад в винный туризм | 1 | Doja | 

## Юго-восток

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksić · Biser Extra Brut | 2016 | 91 | Falstaff |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2023 | лучшая малая винодельня | 1 | Jović | 
| 2015 | лучшая национальная винодельня | 1 | Aleksić | 

## Подунавье и Белградский район

Оценок критиков не найдено.

## Косово и Метохия

Оценок критиков не найдено.

