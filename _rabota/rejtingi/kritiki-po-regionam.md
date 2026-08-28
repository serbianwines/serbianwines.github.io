# Оценки критиков

Вторая дорожка, независимая от Vivino. Здесь стобалльная шкала и оценка
эксперта, а не средняя по толпе.

**Почему отдельно, а не вместе.** У Vivino пятибалльная оценка покупателей,
и её вес определяется числом отметок. У критика вес определяется тем, что он
критик; порога по числу отзывов здесь нет и быть не может. Это две разные
величины, и в одно число они не складываются. Если рейтинги пойдут в книгу,
показывать их надо порознь и подписывать, что именно показано.

## Две вещи, а не одна

**Оценки** — балл по стобалльной шкале, 997 записей.

**Награды** — место в категории или медаль, 909 записей. У них нет шкалы,
зато есть год и категория. Переводить «лучшее белое из местных сортов
2025 года» в число нельзя, поэтому и таблицы разные.

Почти всё это — Decanter: база наград конкурса открылась целиком, и по
каждому вину там сразу медаль и балл. Двенадцать лет, 997 сербских медалей.

## Источники

**Falstaff** — 146 оценок, сербский список целиком. Австрийский гид ведёт
отдельный раздел «Tasting Serbien», ранжирует сорок сербских хозяйств по
стобалльной шкале и ставит им звёзды; дегустирует Peter Moser. Из всего,
что нашлось, это самый широкий по Сербии авторский охват.

Сайт отвечает страницей Cloudflare «you have been blocked», и поиском его
списки не индексируются. Обошли это дважды. Сохранённую человеком страницу
разбирает `vzjat-falstaff.py`: в её разметке лежит состояние Livewire, а в
нём те же данные полями, вплоть до имени дегустатора и названия дегустации.
Полный список пришёл иначе — автор открыл поиск по Сербии в браузере и
напечатал результат в PDF; двадцать четыре страницы перенесены в данные
вручную. Сколько всего сербских вин у Falstaff, страница пишет сама: 116.
Записей из неё 114: дважды в списке стоит одно и то же вино с расхождением
в балл (*Zvonko Bogdan Cuvée No 1 2019* — 94 и 93, *Zvonko Bogdan Pinot
Blanc 2019* — 93 и 92); второй балл отмечен в примечании к записи.

**Wine-Searcher** — не оценивает сам, а усредняет оценки критиков и взвешивает
их по числу отзывов и числу критиков. Ровно тот приём, что применён и к
Vivino в соседней дорожке.

**vino.rs** — годовой тест «Najbolja vina Srbije»: сотня винных
профессионалов, 31–33 категории, с 2019 года. Книга уже опирается на этот
выбор за 2025-й; здесь собраны все семь лет, 2019–2025, — 67 мест
в главных категориях. Отдельно — оценки в баллах от Зорана Рапајића.

**Tastings.com** — Beverage Testing Institute, отдельные сербские вина.

**Decanter** — база наград DWWA целиком, 2015–2026. По каждому вину:
хозяйство, имя, урожай, цвет, стиль, медаль и балл. Медали по годам:
2015 — 49, 2016 — 35, 2017 — 54, 2018 — 63, 2019 — 67, 2020 — 115,
2021 — 64, 2022 — 85, 2023 — 103, 2024 — 117, 2025 — 99, 2026 — 146.
Счёт за 2026-й сошёлся с книгой ровно: 3 платины, 7 золота, 58 серебра,
78 бронзы — то есть 146, а не 149, как писала пресса.

## Что важно для книги

Falstaff закрывает ровно ту дыру, которую Vivino оставляет. Грашац Vinčić:
Best in Show Decanter, на Vivino оценки нет вовсе — у Falstaff *Grašac Grand
Fru 2020* стоит 95 баллов, а само хозяйство держит четыре звезды. То же с
Doja: четыре звезды и 95 баллов за *Prokupac Breg 2019* при том, что на
Vivino район еле наскребает пятёрку.

Иначе говоря: **Vivino показывает, что пьют, Falstaff — что сделано хорошо.**
Для справочника вторая величина ближе к делу.

## Чего нет

**Подунавье — одна запись на весь район:** бронза DWWA 2026 у Plavinac за
смедеревку 2025 года, 88 баллов. На Vivino район не представлен вовсе.
Рядом стоит золото Decanter 2025 у Virtus, но Decanter относит его к району
Млава; входит ли Млава в главу «Подунавье», решать автору.

**Метохия — только награды**, баллов нет: у Lakićević три места в годовом
тесте vino.rs (2023, 2024, 2025) и ни одной стобалльной оценки. На Vivino
хозяйство есть — восемь вин, все около 4,1–4,2.

**Юго-восток держится на одном хозяйстве.** Тридцать восемь оценок в районе,
и все до одной — Aleksić. У Džervin и Jović нет ни балла, ни награды.

**Район известен у 60 хозяйств из 484.** Остальные Vivino сваливает в
«Central Serbia» и «Wine of Serbia» — по ним район не восстановить, и
расписывать их по главам книги придётся вручную.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-kritikov.py --otchet

---

<!-- Собрано скриптом svesti-kritikov.py. Руками не править. -->

## Где две дорожки пересекаются

Вин с оценкой Vivino — 1189, с оценкой критиков — 587, **с обеими — 182**.

| Район | Vivino | Критики | И то и другое |
|---|---|---|---|
| Фрушка гора | 212 | 89 | 34 |
| Суботичско-Хоргошская пешчара | 76 | 27 | 17 |
| Банат | 37 | 6 | 4 |
| Шумадия | 81 | 81 | 25 |
| Три Моравы и Жупа | 104 | 51 | 14 |
| Неготинска Крайина | 20 | 33 | 8 |
| Топлица | 20 | 16 | 6 |
| Юго-восток | 31 | 25 | 8 |
| Подунавье и Белградский район | 0 | 1 | 0 |
| Косово и Метохия | 8 | 0 | 0 |

## Фрушка гора

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Erdevik · Omnibus Lector Chardonnay | 2015 | 97 | decanter |
| Vinčić · Grašac | 2020 | 97 | decanter |
| Deurić · La Rem Chardonnay | 2023 | 97 | decanter |
| Bikicki · Uncensored | 2018 | 96 | decanter |
| Vinčić · Grašac Grand Fru | 2020 | 95 | Falstaff |
| Chichateau · Chi Chardonnay | 2018 | 95 | Falstaff |
| Erdevik · Stifler's Mom Shiraz | 2017 | 95 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2019 | 95 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2017 | 95 | decanter |
| Veritas Ćuković · Momentum | 2017 | 95 | decanter |
| Erdevik · Trianon | 2018 | 94 | decanter |
| Bikicki · Uncensored | 2020 | 94 | decanter |
| Erdevik · Stiflers Mom Shiraz | 2020 | 94 | decanter |
| Šapat · Cuvée | 2022 | 94 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2017 | 94 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2019 | 94 | decanter |
| Deurić · La Rem Chardonnay | 2023 | 94 | decanter |
| Vinum · Grašac 26a | 2019 | 93 | Falstaff |
| Erdevik · Grand Trianon | 2017 | 93 | Falstaff |
| Molovin · Inat Frankovka | 2019 | 93 | Falstaff |
| Bjelica · Graffiti | 2018 | 93 | Falstaff |
| Deurić · Severna Morava | 2020 | 93 | decanter |
| Deurić · Severna Morava | 2021 | 93 | decanter |
| Erdevik · Stiflers Mom Shiraz | 2019 | 93 | decanter |
| Deurić · Aksiom Crveni | 2019 | 93 | decanter |
| Deurić · Aksiom | 2021 | 93 | decanter |
| Erdevik · Grand Trianon | 2016 | 93 | Falstaff |
| Deurić · Aksiom Beli | 2019 | 92 | Falstaff |
| Erdevik · Grand Trianon Deux Mers | 2016 | 92 | Falstaff |
| Bikicki · Sfera Noir (натуральное) | 2021 | 92 | Falstaff |
| Deurić · The Brut | 2018 | 92 | Falstaff |
| Deurić · Princeps Brut Nature | 2015 | 92 | decanter |
| Bikicki · S/O | 2017 | 92 | decanter |
| Chichateau · Chi Chardonnay | 2024 | 92 | decanter |
| Chichateau · Fabula Lagum | 2021 | 92 | decanter |
| Šapat · Atila Cabernet Sauvignon | 2023 | 92 | decanter |
| Deurić · Aksiom | 2022 | 92 | decanter |
| Trivanović · Ultimo S | 2020 | 92 | decanter |
| Kovačević · R Edition Brut | 2012 | 92 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2017 | 92 | decanter |
| Erdevik · Trianon | 2018 | 92 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2021 | 92 | decanter |
| Erdevik · Grand Trianon | — | 91 | Wine-Searcher |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | — | 91 | Wine-Searcher |
| Deurić · Classic Chardonnay | 2018 | 91 | decanter |
| Deurić · Aksiom | 2016 | 91 | decanter |
| Deurić · Classic Chardonnay | 2021 | 91 | decanter |
| Verkat · Barrique Malvazija | 2021 | 91 | decanter |
| Verkat · Grašac Beli 4.0 | 2021 | 91 | decanter |
| Veritas Ćuković · Momentum | 2021 | 91 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2021 | 91 | decanter |
| Deurić · La Rem Morava Amf. | 2023 | 91 | decanter |
| Vinčić · Grand Fru | 2020 | 91 | decanter |
| Bikicki · Uncensored | 2022 | 91 | decanter |
| Kovačević · Riesling | 2021 | 91 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2023 | 91 | decanter |
| Chichateau · Blake Sauvignon Blanc | 2023 | 91 | decanter |
| Molovin · Inat Traminac | 2020 | 91 | Falstaff |
| Kovačević · Aurelius Edicija S | 2019 | 90 | Falstaff |
| Deurić · Talas Crveni | 2015 | 90 | decanter |
| Erdevik · Nostra | 2017 | 90 | decanter |
| Deurić · Probus | 2016 | 90 | decanter |
| Deurić · Talas Crveni | 2017 | 90 | decanter |
| Vinum · Frankovka | 2017 | 90 | decanter |
| Vinum · Pinot Noir | 2017 | 90 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2016 | 90 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2017 | 90 | decanter |
| Deurić · Severna Morava | 2018 | 90 | decanter |
| Deurić · Aksiom Beli | 2019 | 90 | decanter |
| Deurić · Classic Chardonnay | 2019 | 90 | decanter |
| Deurić · Aksiom | 2017 | 90 | decanter |
| Erdevik · Stifles Mom | 2017 | 90 | decanter |
| Deurić · Aksiom Beli | 2019 | 90 | decanter |
| Erdevik · Marlon Delon | 2017 | 90 | decanter |
| Veritas Ćuković · Monte Karlovci Merlot | 2021 | 90 | decanter |
| Veritas Ćuković · ćUk | 2021 | 90 | decanter |
| Deurić · Severna Morava | 2023 | 90 | decanter |
| Vinčić · Grand Fru | 2023 | 90 | decanter |
| Deurić · Gorska Tamjanika | 2024 | 90 | decanter |
| Chichateau · Fabula Lagum Cabernet Sauvignon-Cabernet Franc-Merlot | 2019 | 90 | decanter |
| Deurić · Aksiom | 2019 | 90 | decanter |
| Erdevik · Grand Trianon | 2020 | 90 | decanter |
| Šapat · Terol Teroldego | 2022 | 90 | decanter |
| Veritas Ćuković · Monte Karlovci | 2022 | 90 | decanter |
| Veritas Ćuković · Momentum Mali | 2023 | 90 | decanter |
| Kovačević · Chardonnay | 2025 | 90 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2020 | 90 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2019 | 90 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2021 | 90 | decanter |
| Erdevik · Trianon | — | 89 | Wine-Searcher |
| Kovačević · Aurelius | 2012 | 89 | decanter |
| Deurić · Talas Beli | 2015 | 89 | decanter |
| Deurić · The Brut | 2015 | 89 | decanter |
| Erdevik · Grand Trianon | 2016 | 89 | decanter |
| Bikicki · Uncensored | 2017 | 89 | decanter |
| Belo Brdo · Black Label Limited Edition Chardonnay | 2020 | 89 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2021 | 89 | decanter |
| Šapat · Atila Chardonnay | 2023 | 89 | decanter |
| Šapat · Chardonnay | 2023 | 89 | decanter |
| Deurić · Pinot Noir | 2018 | 89 | decanter |
| Šapat · Atila Cabernet Sauvignon | 2022 | 89 | decanter |
| Deurić · Sauvignon Blanc | 2024 | 89 | decanter |
| Veritas Ćuković · Ćuk | 2021 | 89 | decanter |
| Erdevik · Grand Trianon | 2019 | 89 | decanter |
| Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah | 2015 | 88 | decanter |
| Kovačević · R Edition Aurelius | 2012 | 88 | decanter |
| Kiš · Kišova Misterija | 2011 | 88 | decanter |
| Deurić · Princeps Probus | 2016 | 88 | decanter |
| Erdevik · Roza Nostra | 2019 | 88 | decanter |
| Kiš · Kišov Grašac Beli | 2019 | 88 | decanter |
| Deurić · Sauvignon Blanc | 2018 | 88 | decanter |
| Kovačević · Fresco Bianco Brut | 2019 | 88 | decanter |
| Bikicki · Makana | 2016 | 88 | decanter |
| Erdevik · Geronimo | 2020 | 88 | decanter |
| Deurić · Chardonnay Classic | 2020 | 88 | decanter |
| Belo Brdo · Belo Brdo | 2018 | 88 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2016 | 88 | decanter |
| Deurić · Probus 276 | 2018 | 88 | decanter |
| Deurić · Princeps Chardonnay | 2021 | 88 | decanter |
| Deurić · Severna Morava | 2020 | 88 | decanter |
| Deurić · The Brut | 2019 | 88 | decanter |
| Deurić · Pinot Noir | 2020 | 88 | decanter |
| Veritas Ćuković · Bela Harmonija | 2022 | 88 | decanter |
| Chichateau · Blake Sauvignon Blanc | 2023 | 88 | decanter |
| Erdevik · Trianon Pinot Blanc-Pinot Grigio-Sauvignon Blanc | 2023 | 88 | decanter |
| Veritas Ćuković · Cuk Cuvée | 2021 | 88 | decanter |
| Veritas Ćuković · Momentum | 2021 | 88 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2020 | 88 | decanter |
| Bikicki · Skins | 2022 | 88 | decanter |
| Chichateau · Chardonnay | 2021 | 88 | decanter |
| Verkat · Grašac Beli | 2024 | 88 | decanter |
| Deurić · Pinot Noir | 2021 | 88 | decanter |
| Deurić · 276 Probus | 2023 | 88 | decanter |
| Deurić · La Rem Morava Amf. | 2023 | 88 | decanter |
| Veritas Ćuković · Barrique Chardonay | 2023 | 88 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2015 | 88 | decanter |
| Vinčić · Grand Fru | 2020 | 88 | decanter |
| Deurić · Aksiom | 2021 | 88 | decanter |
| Deurić · Enigma | 2015 | 87 | decanter |
| Deurić · Urban Rose | 2015 | 87 | decanter |
| Deurić · Pinot Noir | 2015 | 87 | decanter |
| Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah | 2016 | 87 | decanter |
| Deurić · Pinot Noir | 2017 | 87 | decanter |
| Belo Brdo · Black Label Cabernet Sauvignon | 2018 | 87 | decanter |
| Deurić · Probus Princeps | 2016 | 87 | decanter |
| Vinčić · Grand Fru | 2020 | 87 | decanter |
| Bikicki · S/O | 2020 | 87 | decanter |
| Erdevik · Geronimo | 2021 | 87 | decanter |
| Bikicki · Cu | 2022 | 87 | decanter |
| Erdevik · Grand Trianon | 2016 | 87 | decanter |
| Kovačević · Edicija S Aurelius | — | 86 | Wine-Searcher |
| Bikicki · Cu | 2018 | 86 | decanter |
| Kovačević · Aurelius S Edicija | 2017 | 86 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2016 | 86 | decanter |
| Molovin · Inat Frankovka | 2019 | 86 | decanter |
| Molovin · Inat Limited Edition Rajnski Rizling | 2021 | 86 | decanter |
| Deurić · Princeps Probus | 2016 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Deurić · Sauvignon Blanc 2024 | 
| 2026 | бронза | bronza | Verkat · Grašac Beli 2024 | 
| 2026 | бронза | bronza | Veritas Ćuković · Ćuk 2021 | 
| 2026 | бронза | bronza | Deurić · Pinot Noir 2021 | 
| 2026 | бронза | bronza | Deurić · 276 Probus 2023 | 
| 2026 | бронза | bronza | Chichateau · Blake Sauvignon Blanc 2023 | 
| 2026 | бронза | bronza | Erdevik · Grand Trianon 2019 | 
| 2026 | бронза | bronza | Deurić · La Rem Morava Amf. 2023 | 
| 2026 | бронза | bronza | Veritas Ćuković · Barrique Chardonay 2023 | 
| 2026 | золото | zlato | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2017 | 
| 2026 | золото | zlato | Veritas Ćuković · Momentum 2017 | 
| 2026 | платина | platina | Deurić · La Rem Chardonnay 2023 | 
| 2026 | серебро | srebro | Chichateau · Chi Chardonnay 2024 | 
| 2026 | серебро | srebro | Kovačević · Riesling 2021 | 
| 2026 | серебро | srebro | Deurić · Aksiom 2022 | 
| 2026 | серебро | srebro | Chichateau · Fabula Lagum 2021 | 
| 2026 | серебро | srebro | Veritas Ćuković · Monte Karlovci 2022 | 
| 2026 | серебро | srebro | Veritas Ćuković · Momentum Mali 2023 | 
| 2026 | серебро | srebro | Šapat · Atila Cabernet Sauvignon 2023 | 
| 2026 | серебро | srebro | Kovačević · Chardonnay 2025 | 
| 2026 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2020 | 
| 2026 | серебро | srebro | Trivanović · Ultimo S 2020 | 
| 2026 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2023 | 
| 2026 | серебро | srebro | Kovačević · R Edition Brut 2012 | 
| 2025 | бронза | bronza | Erdevik · Trianon Pinot Blanc-Pinot Grigio-Sauvignon Blanc 2023 | 
| 2025 | бронза | bronza | Šapat · Atila Chardonnay 2023 | 
| 2025 | бронза | bronza | Šapat · Chardonnay 2023 | 
| 2025 | бронза | bronza | Deurić · Pinot Noir 2018 | 
| 2025 | бронза | bronza | Veritas Ćuković · Cuk Cuvée 2021 | 
| 2025 | бронза | bronza | Veritas Ćuković · Momentum 2021 | 
| 2025 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2021 | 
| 2025 | бронза | bronza | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2020 | 
| 2025 | бронза | bronza | Bikicki · Skins 2022 | 
| 2025 | бронза | bronza | Bikicki · Cu 2022 | 
| 2025 | бронза | bronza | Šapat · Atila Cabernet Sauvignon 2022 | 
| 2025 | бронза | bronza | Deurić · Aksiom 2021 | 
| 2025 | бронза | bronza | Chichateau · Chardonnay 2021 | 
| 2025 | золото | zlato | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2025 | лучшее белое, местные сорта | 1 | Deurić · La Rem Morava 2023 | 
| 2025 | лучшее красное, органика, международные сорта | 1 | Dukay-Sagmeister · Kadarka Kew 2022 | 
| 2025 | серебро | srebro | Chichateau · Blake Sauvignon Blanc 2023 | 
| 2025 | серебро | srebro | Deurić · La Rem Morava Amf. 2023 | 
| 2025 | серебро | srebro | Deurić · La Rem Chardonnay 2023 | 
| 2025 | серебро | srebro | Deurić · Severna Morava 2023 | 
| 2025 | серебро | srebro | Vinčić · Grand Fru 2020 | 
| 2025 | серебро | srebro | Deurić · Gorska Tamjanika 2024 | 
| 2025 | серебро | srebro | Chichateau · Fabula Lagum Cabernet Sauvignon-Cabernet Franc-Merlot 2019 | 
| 2025 | серебро | srebro | Deurić · Aksiom 2019 | 
| 2025 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2025 | серебро | srebro | Erdevik · Grand Trianon 2020 | 
| 2025 | серебро | srebro | Erdevik · Stiflers Mom Shiraz 2020 | 
| 2025 | серебро | srebro | Bikicki · Uncensored 2022 | 
| 2025 | серебро | srebro | Šapat · Cuvée 2022 | 
| 2025 | серебро | srebro | Šapat · Terol Teroldego 2022 | 
| 2024 | бронза | bronza | Vinčić · Grand Fru 2020 | 
| 2024 | бронза | bronza | Deurić · Pinot Noir 2020 | 
| 2024 | бронза | bronza | Molovin · Inat Limited Edition Rajnski Rizling 2021 | 
| 2024 | бронза | bronza | Erdevik · Geronimo 2021 | 
| 2024 | бронза | bronza | Veritas Ćuković · Bela Harmonija 2022 | 
| 2024 | винодельня года | 1 | Kovačević | 
| 2024 | лучшая малая винодельня | 1 | Bikicki | 
| 2024 | лучшее белое, международные сорта | 1 | Kovačević · Sauvignon S Edicija 2021 | 
| 2024 | лучшее белое, органика, международные сорта | 1 | Dukay-Sagmeister · Furmint Kew 2020 | 
| 2024 | серебро | srebro | Veritas Ćuković · Monte Karlovci Merlot 2021 | 
| 2024 | серебро | srebro | Veritas Ćuković · ćUk 2021 | 
| 2024 | серебро | srebro | Veritas Ćuković · Momentum 2021 | 
| 2024 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2024 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2024 | серебро | srebro | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2017 | 
| 2024 | серебро | srebro | Erdevik · Stiflers Mom Shiraz 2019 | 
| 2024 | серебро | srebro | Deurić · Aksiom Crveni 2019 | 
| 2023 | Best in Show | best-in-show | Vinčić · Grašac 2020 | 
| 2023 | бронза | bronza | Deurić · Probus 276 2018 | 
| 2023 | бронза | bronza | Molovin · Inat Frankovka 2019 | 
| 2023 | бронза | bronza | Deurić · Princeps Chardonnay 2021 | 
| 2023 | бронза | bronza | Deurić · Severna Morava 2020 | 
| 2023 | бронза | bronza | Vinčić · Grand Fru 2020 | 
| 2023 | бронза | bronza | Bikicki · S/O 2020 | 
| 2023 | бронза | bronza | Erdevik · Grand Trianon 2016 | 
| 2023 | бронза | bronza | Deurić · The Brut 2019 | 
| 2023 | винодельня года | 1 | Erdevik | 
| 2023 | вклад в винный туризм | 1 | Šapat | 
| 2023 | золото | zlato | Erdevik · Stifler's Mom Shiraz 2017 | 
| 2023 | лучшее белое | 1 | Erdevik · Sauvignon Blanc Ex Cathedra 2021 | 
| 2023 | лучшее из местных сортов, белое | 1 | Vinčić · Grašac 2020 | 
| 2023 | серебро | srebro | Erdevik · Trianon 2018 | 
| 2023 | серебро | srebro | Deurić · Aksiom Beli 2019 | 
| 2023 | серебро | srebro | Erdevik · Marlon Delon 2017 | 
| 2023 | серебро | srebro | Deurić · Classic Chardonnay 2021 | 
| 2023 | серебро | srebro | Deurić · Severna Morava 2021 | 
| 2023 | серебро | srebro | Bikicki · Uncensored 2020 | 
| 2023 | серебро | srebro | Verkat · Barrique Malvazija 2021 | 
| 2023 | серебро | srebro | Verkat · Grašac Beli 4.0 2021 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Limited Edition Chardonnay 2020 | 
| 2022 | бронза | bronza | Erdevik · Geronimo 2020 | 
| 2022 | бронза | bronza | Deurić · Chardonnay Classic 2020 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Cabernet Sauvignon 2018 | 
| 2022 | бронза | bronza | Belo Brdo · Belo Brdo 2018 | 
| 2022 | бронза | bronza | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2016 | 
| 2022 | бронза | bronza | Deurić · Probus Princeps 2016 | 
| 2022 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2016 | 
| 2022 | лучшее белое | 1 | Deurić · Aksiom beli 2019 | 
| 2022 | лучшее игристое | 1 | Deurić · The 2019 | 
| 2022 | серебро | srebro | Deurić · Severna Morava 2020 | 
| 2022 | серебро | srebro | Deurić · Aksiom Beli 2019 | 
| 2022 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2022 | серебро | srebro | Deurić · Classic Chardonnay 2019 | 
| 2022 | серебро | srebro | Erdevik · Trianon 2018 | 
| 2022 | серебро | srebro | Deurić · Aksiom 2017 | 
| 2022 | серебро | srebro | Erdevik · Stifles Mom 2017 | 
| 2021 | бронза | bronza | Kovačević · Fresco Bianco Brut 2019 | 
| 2021 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2021 | бронза | bronza | Bikicki · Cu 2018 | 
| 2021 | бронза | bronza | Deurić · Pinot Noir 2017 | 
| 2021 | бронза | bronza | Kovačević · Aurelius S Edicija 2017 | 
| 2021 | бронза | bronza | Bikicki · Makana 2016 | 
| 2021 | десятка лучших виноделен | 1 | Dukay-Sagmeister | 
| 2021 | золото | zlato | Bikicki · Uncensored 2018 | 
| 2021 | серебро | srebro | Deurić · Aksiom 2016 | 
| 2021 | серебро | srebro | Deurić · Severna Morava 2018 | 
| 2021 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2017 | 
| 2020 | бронза | bronza | Kiš · Kišova Misterija 2011 | 
| 2020 | бронза | bronza | Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah 2016 | 
| 2020 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2020 | бронза | bronza | Erdevik · Grand Trianon 2016 | 
| 2020 | бронза | bronza | Erdevik · Roza Nostra 2019 | 
| 2020 | бронза | bronza | Kiš · Kišov Grašac Beli 2019 | 
| 2020 | бронза | bronza | Bikicki · Uncensored 2017 | 
| 2020 | бронза | bronza | Deurić · Sauvignon Blanc 2018 | 
| 2020 | лучшая малая винодельня | 1 | Chichateau | 
| 2020 | лучшая молодая винодельня | 1 | Deurić | 
| 2020 | лучшее белое | 1 | Chichateau · Chardonnay Chi 2016 | 
| 2020 | платина | platina | Erdevik · Omnibus Lector Chardonnay 2015 | 
| 2020 | серебро | srebro | Vinum · Frankovka 2017 | 
| 2020 | серебро | srebro | Vinum · Pinot Noir 2017 | 
| 2020 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2016 | 
| 2020 | серебро | srebro | Bikicki · S/O 2017 | 
| 2020 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2017 | 
| 2020 | серебро | srebro | Deurić · Classic Chardonnay 2018 | 
| 2019 | бронза | bronza | Deurić · The Brut 2015 | 
| 2019 | лучшая малая винодельня | 1 | Bikicki | 
| 2019 | лучшее игристое | 1 | Deurić · Princeps Brut Nature 2015 | 
| 2019 | серебро | srebro | Deurić · Talas Crveni 2017 | 
| 2019 | серебро | srebro | Deurić · Princeps Brut Nature 2015 | 
| 2018 | бронза | bronza | Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah 2015 | 
| 2018 | бронза | bronza | Kovačević · R Edition Aurelius 2012 | 
| 2018 | серебро | srebro | Erdevik · Nostra 2017 | 
| 2018 | серебро | srebro | Deurić · Probus 2016 | 
| 2017 | бронза | bronza | Deurić · Talas Beli 2015 | 
| 2017 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2015 | 
| 2017 | бронза | bronza | Deurić · Enigma 2015 | 
| 2017 | бронза | bronza | Deurić · Urban Rose 2015 | 
| 2017 | бронза | bronza | Deurić · Pinot Noir 2015 | 
| 2017 | серебро | srebro | Deurić · Talas Crveni 2015 | 
| 2016 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2015 | бронза | bronza | Belo Brdo · Cabernet Franc 2012 | 
| 2015 | бронза | bronza | Belo Brdo · Alma Mons 2012 | 
| 2015 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2015 | бронза | bronza | Kiš · Kišova Misterija Polusuvo 2011 | 
| 2015 | серебро | srebro | Vinum · Sauvignon Blanc 2013 | 

## Суботичско-Хоргошская пешчара

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Maurer · Kadarka 1880 (натуральное) | 2021 | 95 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2016 | 95 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2017 | 95 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2017 | 95 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2019 | 95 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2019 | 95 | decanter |
| Zvonko Bogdan · Merlot | 2023 | 95 | decanter |
| Zvonko Bogdan · Chardonnay | 2022 | 95 | decanter |
| Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature | 2018 | 95 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2019 | 94 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No 1 | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Merlot Single Vineyard | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2017 | 93 | Wine-Searcher |
| Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature | 2020 | 93 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 93 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 93 | decanter |
| Zvonko Bogdan · Chardonnay | 2017 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 93 | Falstaff |
| Zvonko Bogdan · Pinot Blanc | 2019 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2013 | 92 | decanter |
| Zvonko Bogdan · Pinot blanc | 2017 | 92 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2017 | 92 | decanter |
| Tonković · Rapsodija | 2015 | 92 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2018 | 92 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 92 | decanter |
| Zvonko Bogdan · Cuvée No 1 | 2017 | 92 | Falstaff |
| Zvonko Bogdan · Rosé Sec | 2022 | 92 | Falstaff |
| Vinarija Petra · Pinot Grigio Orange | 2020 | 92 | Falstaff |
| Vinarija Petra · Pinot Noir Barrique | 2020 | 92 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2023 | 91 | Wine-Searcher |
| Zvonko Bogdan · Icon Campana Rubimus | 2015 | 91 | decanter |
| Tonković · Fantazija | 2012 | 91 | decanter |
| Tonković · Fantazija Kadarka | 2015 | 91 | decanter |
| Zvonko Bogdan · Chardonnay | 2019 | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2021 | 91 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 91 | decanter |
| Zvonko Bogdan · Cuvée no.1 | 2023 | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2023 | 91 | decanter |
| Zvonko Bogdan · Chardonnay | 2023 | 91 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 91 | decanter |
| Zvonko Bogdan · Cuvée No. 1 | 2016 | 91 | Falstaff |
| Vinarija Petra · Pinot Grigio Orange | 2021 | 91 | Falstaff |
| Zvonko Bogdan · Sauvignon Blanc | 2019 | 91 | Falstaff |
| Zvonko Bogdan · Chardonnay | 2018 | 91 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2022 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2021 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2018 | 90 | Wine-Searcher |
| Zvonko Bogdan · Icon Campana Rubimus | 2013 | 90 | decanter |
| Tonković · Rapsodija Kadarka | 2014 | 90 | decanter |
| Zvonko Bogdan · Život Teče | 2017 | 90 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2018 | 90 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2019 | 90 | decanter |
| Zvonko Bogdan · Rose Sec | 2021 | 90 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2024 | 90 | decanter |
| Zvonko Bogdan · Chardonnay | 2015 | 90 | decanter |
| Zvonko Bogdan · Chardonnay | 2018 | 90 | decanter |
| Vinarija Petra · Pinot Noir | 2020 | 90 | Falstaff |
| Vinarija Petra · Rose&co | 2020 | 90 | Falstaff |
| Vinarija Petra · Traminac | 2020 | 90 | Falstaff |
| Zvonko Bogdan · Éclater Blanc de Blancs Extra Brut | 2018 | 90 | Falstaff |
| Zvonko Bogdan · Život Teče | 2016 | 89 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2018 | 89 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2022 | 89 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2020 | 89 | decanter |
| Zvonko Bogdan · Cuvée No. 1 | 2024 | 89 | decanter |
| Vinarija Petra · Rosé | 2019 | 89 | Falstaff |
| Zvonko Bogdan · Cuvée No. 1 | 2015 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 88 | decanter |
| Zvonko Bogdan · Chardonnay | 2019 | 88 | decanter |
| Zvonko Bogdan · Sauvignon Blanc | 2021 | 88 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2021 | 88 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2022 | 88 | decanter |
| Zvonko Bogdan · Merlot | 2022 | 88 | decanter |
| Vinarija Petra · Pinot Grigio | 2017 | 88 | Falstaff |
| Tonković · Rapsodija | 2013 | 87 | decanter |
| Zvonko Bogdan · Život Teče | 2015 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2017 | 87 | decanter |
| Zvonko Bogdan · Pinot Grigio | 2019 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2018 | 87 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 87 | decanter |
| Zvonko Bogdan · Rosé Sec | 2022 | 87 | decanter |
| Tonković · Fantazija Organic Kadarka | 2022 | 87 | decanter |
| Zvonko Bogdan · Merlot | 2022 | 87 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2017 | 87 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2019 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2015 | 86 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2018 | 86 | decanter |
| Tonković · Rapsodija Kadarka | 2019 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Zvonko Bogdan · Cuvée No. 1 2024 | 
| 2026 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2022 | 
| 2026 | золото | zlato | Zvonko Bogdan · Chardonnay 2022 | 
| 2026 | золото | zlato | Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature 2018 | 
| 2026 | серебро | srebro | Zvonko Bogdan · Icon Campana Albus 2024 | 
| 2026 | серебро | srebro | Zvonko Bogdan · Cuvée No.1 2023 | 
| 2026 | серебро | srebro | Zvonko Bogdan · Chardonnay 2023 | 
| 2026 | серебро | srebro | Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature 2020 | 
| 2025 | бронза | bronza | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2025 | бронза | bronza | Zvonko Bogdan · Chardonnay 2018 | 
| 2025 | бронза | bronza | Zvonko Bogdan · Merlot 2022 | 
| 2025 | бронза | bronza | Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut 2020 | 
| 2025 | золото | zlato | Zvonko Bogdan · Merlot 2023 | 
| 2025 | лучшее белое, органика, местные сорта | 1 | Maurer · Karom 2023 | 
| 2025 | серебро | srebro | Zvonko Bogdan · Cuvée no.1 2023 | 
| 2025 | серебро | srebro | Zvonko Bogdan · Pinot Blanc 2019 | 
| 2024 | бронза | bronza | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2024 | бронза | bronza | Zvonko Bogdan · Cuvee No1 2022 | 
| 2024 | бронза | bronza | Tonković · Fantazija Organic Kadarka 2022 | 
| 2024 | бронза | bronza | Zvonko Bogdan · Merlot 2022 | 
| 2024 | бронза | bronza | Tonković · Rapsodija Kadarka 2019 | 
| 2024 | золото | zlato | Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut 2019 | 
| 2024 | лучшее красное, органика, местные сорта | 1 | Maurer · Kadarka 1880 2022 | 
| 2024 | серебро | srebro | Zvonko Bogdan · Merlot 2019 | 
| 2024 | серебро | srebro | Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut 2018 | 
| 2023 | бронза | bronza | Zvonko Bogdan · Sauvignon Blanc 2021 | 
| 2023 | бронза | bronza | Zvonko Bogdan · Rosé Sec 2022 | 
| 2023 | лучшее игристое | 1 | Zvonko Bogdan · Éclater 2018 | 
| 2023 | серебро | srebro | Zvonko Bogdan · Cuvée No.1 2021 | 
| 2022 | бронза | bronza | Zvonko Bogdan · Merlot 2019 | 
| 2022 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2019 | 
| 2022 | бронза | bronza | Zvonko Bogdan · Chardonnay 2019 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Rose Sec 2021 | 
| 2021 | десятка лучших виноделен | 3 | Maurer | 
| 2021 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2019 | 
| 2021 | лучшее белое | 1 | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Merlot 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Chardonnay 2019 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Pinot Grigio 2019 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2018 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Icon Campana Rubimus 2018 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Icon Campana Albus 2017 | 
| 2020 | серебро | srebro | Tonković · Fantazija Kadarka 2015 | 
| 2020 | серебро | srebro | Tonković · Rapsodija 2015 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Chardonnay 2018 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Cuvée No.1 2018 | 
| 2019 | бронза | bronza | Zvonko Bogdan · Icon Campana Albus 2017 | 
| 2019 | бронза | bronza | Zvonko Bogdan · Chardonnay 2017 | 
| 2019 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2017 | 
| 2019 | золото | zlato | Zvonko Bogdan · Icon Campana Rubimus 2017 | 
| 2019 | серебро | srebro | Zvonko Bogdan · Pinot blanc 2017 | 
| 2019 | серебро | srebro | Zvonko Bogdan · Život Teče 2017 | 
| 2018 | бронза | bronza | Zvonko Bogdan · Chardonnay 2015 | 
| 2018 | бронза | bronza | Zvonko Bogdan · Život Teče 2016 | 
| 2018 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2016 | 
| 2018 | серебро | srebro | Tonković · Rapsodija Kadarka 2014 | 
| 2018 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2013 | 
| 2017 | бронза | bronza | Tonković · Rapsodija 2013 | 
| 2017 | бронза | bronza | Zvonko Bogdan · Život Teče 2015 | 
| 2017 | бронза | bronza | Zvonko Bogdan · Cuvée No. 1 2015 | 
| 2017 | серебро | srebro | Zvonko Bogdan · Chardonnay 2015 | 
| 2017 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2015 | 
| 2017 | серебро | srebro | Tonković · Fantazija 2012 | 
| 2016 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2013 | 
| 2015 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2012 | 
| 2015 | бронза | bronza | Tonković · Kadarka Rapsodija 2012 | 

## Банат

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Drašković · Mahago | 2019 | 90 | decanter |
| Drašković · Beli Pinot | 2020 | 90 | decanter |
| Drašković · Beli Pinot | 2021 | 90 | decanter |
| Drašković · Frankovka Rezerva | 2018 | 90 | decanter |
| Drašković · Horizont Chardonnay | 2021 | 89 | decanter |
| Drašković · Mahago | 2017 | 88 | decanter |
| Drašković · Beli Pinot | 2019 | 87 | decanter |
| Drašković · Burgundac Beli | 2021 | 87 | decanter |
| Drašković · Mahago Frankovka | 2021 | 87 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2024 | бронза | bronza | Drašković · Mahago Frankovka 2021 | 
| 2024 | серебро | srebro | Drašković · Beli Pinot 2021 | 
| 2024 | серебро | srebro | Drašković · Frankovka Rezerva 2018 | 
| 2023 | бронза | bronza | Drašković · Horizont Chardonnay 2021 | 
| 2023 | бронза | bronza | Drašković · Burgundac Beli 2021 | 
| 2023 | серебро | srebro | Drašković · Mahago 2019 | 
| 2023 | серебро | srebro | Drašković · Beli Pinot 2020 | 
| 2021 | бронза | bronza | Drašković · Beli Pinot 2019 | 
| 2021 | бронза | bronza | Drašković · Mahago 2017 | 

## Шумадия

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 2022 | 97 | decanter |
| Matijašević · SoviNoa Fumé Blanc | 2020 | 96 | decanter |
| Matijašević · SoviNoa | 2019 | 95 | decanter |
| Aleksandrović · Regent Reserve | 2018 | 95 | decanter |
| Matijašević · Tri Doline | 2020 | 95 | decanter |
| Matijašević · Sovinoa Fumé Blanc | 2021 | 95 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 95 | decanter |
| Tarpoš · Prokupac | 2023 | 95 | decanter |
| Despotika · Krunski Dokaz | 2017 | 95 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 95 | decanter |
| Matijašević · SoviNoa Fumé Blanc | 2020 | 94 | Falstaff |
| Aleksandrović · Trijumf Gold | 2022 | 94 | Falstaff |
| Matijašević · Sovi Noa Fumé Blanc | 2020 | 94 | Falstaff |
| Matijašević · Sovi Noa Fumé Blanc | 2021 | 94 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 94 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2020 | 93 | Falstaff |
| Matijašević · SoviNoa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Noir | 2010 | 93 | decanter |
| Matijašević · Čukundeda Prokupac | 2019 | 93 | decanter |
| Aleksandrović · Trijumf Gold | 2023 | 93 | decanter |
| Despotika · Barik Morava | 2022 | 93 | decanter |
| Despotika · Krunski Dokas (The Key Evidence) Grand Reserve | 2017 | 93 | Falstaff |
| Aleksandrović · VOŽD | 2017 | 93 | Falstaff |
| Matijašević · Belina | 2022 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection | 2021 | 93 | Falstaff |
| Matijašević · Merlot Tri Doline | 2020 | 93 | Falstaff |
| Aleksandrović · Trijumf Chardonnay Brut | 2018 | 93 | Falstaff |
| Aleksandrović · Trijumf Terroir | 2022 | 93 | Falstaff |
| Matijašević · Sovi Noa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 93 | Falstaff |
| Aleksandrović · Prokupac | 2019 | 92 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 92 | decanter |
| Matijašević · Sovinoa Sauvignon Blanc | 2021 | 92 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 92 | decanter |
| Aleksandrović · Trijumf Noir Brut | 2010 | 92 | Falstaff |
| Despotika · Nemir (Turbulence) Rosé | — | 92 | Falstaff |
| Aleksandrović · Prokupac | 2021 | 92 | Falstaff |
| Matijašević · Prokupac Cukundeda | 2020 | 92 | Falstaff |
| Aleksandrović · Trijumf Prokupac | 2020 | 92 | Falstaff |
| Matijašević · Belina | 2020 | 92 | Falstaff |
| Matijašević · Prokupac Cukundeda Superiore | 2019 | 92 | Falstaff |
| Despotika · Trag (The Clue) Merlot | 2019 | 92 | Falstaff |
| Aleksandrović · Trijumf Brut Rosé | 2019 | 92 | Falstaff |
| Aleksandrović · Rodoslov Reserve | — | 91 | Wine-Searcher |
| Radovanović · Reserve Cabernet Sauvignon | 2013 | 91 | Tastings.com |
| Despotika · Zmajeviti Prokupac | — | 91 | Falstaff |
| Despotika · Trag | 2017 | 91 | decanter |
| Aleksandrović · Vizija Selection | 2016 | 91 | decanter |
| Matijašević · Sovinoa Sauvignon Blanc | 2020 | 91 | decanter |
| Matijašević · Čukundeda Superiore | 2019 | 91 | decanter |
| Matijašević · Cukundeda Prokupac | 2021 | 91 | decanter |
| Aleksandrović · Regent Reserve | 2019 | 91 | decanter |
| Matijašević · Belina | 2022 | 91 | decanter |
| Despotika · Zmajeviti Prokupac (The Dragons Wine) | — | 91 | Falstaff |
| Aleksandrović · Trijumf Rosé Pinot Noir | 2022 | 91 | Falstaff |
| Despotika · Morava | 2021 | 91 | Falstaff |
| Despotika · Morava Barik | 2021 | 91 | Falstaff |
| Despotika · Morava Glina | 2021 | 91 | Falstaff |
| Despotika · Morava Orange | 2020 | 91 | Falstaff |
| Aleksandrović · Oplen Rheinriesling | 2020 | 91 | Falstaff |
| Aleksandrović · Vizija Selection | 2020 | 91 | Falstaff |
| Radovanović · Cabernet Sauvignon Reserve | 2019 | 91 | Falstaff |
| Radovanović · Réserve Cabernet Sauvignon | — | 90 | Wine-Searcher |
| Radovanović · Classique Cabernet Sauvignon | 2015 | 90 | Tastings.com |
| Aleksandrović · Trijumf Barrique | 2012 | 90 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2009 | 90 | decanter |
| Despotika · Dokaz | 2015 | 90 | decanter |
| Aleksandrović · Vizija | 2015 | 90 | decanter |
| Aleksandrović · Trijumf Gold | 2018 | 90 | decanter |
| Aleksandrović · Trijumf Gold | 2019 | 90 | decanter |
| Aleksandrović · Trijumf Gold | 2020 | 90 | decanter |
| Tarpoš · Menuet | 2021 | 90 | decanter |
| Tarpoš · 1804 | 2015 | 90 | decanter |
| Tarpoš · Tamjanika | 2022 | 90 | decanter |
| Matijašević · Belina | 2021 | 90 | decanter |
| Aleksandrović · Prokupac | 2020 | 90 | decanter |
| Tarpoš · Tamjanika | 2023 | 90 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 90 | decanter |
| Aleksandrović · Regent Reserve | 2020 | 90 | decanter |
| Aleksandrović · Trijumf Rosé Brut | 2019 | 90 | decanter |
| Matijašević · Belina Inferno | 2022 | 90 | Falstaff |
| Despotika · Beckapaj (Infintiy) Sauvignon Blanc | 2021 | 90 | Falstaff |
| Despotika · Morava Inoks | 2021 | 90 | Falstaff |
| Radovanović · Chardonnay Classique | 2020 | 90 | Falstaff |
| Despotika · Nemir rosé | 2024 | 89 | Falstaff |
| Despotika · Dodir Tamjanika | 2022 | 89 | Falstaff |
| Despotika · Trag | 2015 | 89 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2012 | 89 | decanter |
| Despotika · Krunski Dokaz Cabernet Sauvignon | 2015 | 89 | decanter |
| Aleksandrović · Trijumf Terroir | 2018 | 89 | decanter |
| Tarpoš · Lipar | 2021 | 89 | decanter |
| Tarpoš · Chardonnay | 2022 | 89 | decanter |
| Despotika · Dokaz | 2019 | 89 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2016 | 89 | decanter |
| Despotika · Nemir | 2024 | 89 | Falstaff |
| Despotika · Dodir (Touch) Tamjanika | 2022 | 89 | Falstaff |
| Radovanović · 25 Reserve Cabernet Sauvignon | 2012 | 88 | decanter |
| Radovanović · Selekcija Chardonnay | 2013 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2012 | 88 | decanter |
| Despotika · TRAG Merlot | 2016 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2016 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2017 | 88 | decanter |
| Matijašević · Belina | 2020 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2017 | 88 | decanter |
| Tarpoš · Merlot | 2017 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2019 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 88 | decanter |
| Despotika · Dokaz Cabernet Sauvignon | 2021 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 88 | decanter |
| Matijašević · Tri Doline Merlot | 2021 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 88 | decanter |
| Despotika · Nebo Riesling-Pinot Blanc | 2016 | 87 | decanter |
| Despotika · Zmajeviti | 2017 | 87 | decanter |
| Aleksandrović · Regent Reserve | 2015 | 87 | decanter |
| Matijašević · Rock & Rose | 2019 | 87 | decanter |
| Aleksandrović · Trijumf Terroir | 2018 | 87 | decanter |
| Despotika · Morava | 2022 | 87 | decanter |
| Tarpoš · Sauvignon Blanc | 2023 | 87 | decanter |
| Tarpoš · Merlot | 2021 | 87 | decanter |
| Marko · Doajen Chardonnay | 2024 | 87 | decanter |
| Marko · Carine Merlot-Cabernet Sauvignon | 2020 | 87 | decanter |
| Aleksandrović · Trijumf Noir Brut | 2022 | 87 | decanter |
| Despotika · Morava | 2016 | 87 | decanter |
| Aleksandrović · Regent Reserve | 2012 | 86 | decanter |
| Despotika · Trag | 2013 | 86 | decanter |
| Despotika · Morava | 2016 | 86 | decanter |
| Aleksandrović · Vožd | 2017 | 86 | decanter |
| Aleksandrović · Trijumf Terroir | 2020 | 86 | decanter |
| Tarpoš · Tamjanika | 2021 | 86 | decanter |
| Tarpoš · Rosé | 2021 | 86 | decanter |
| Matijašević · 7 Hrastova Cuvée | 2021 | 86 | decanter |
| Despotika · Trag | 2021 | 86 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 86 | decanter |
| Despotika · Nemir | 2023 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2020 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 86 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Marko · Doajen Chardonnay 2024 | 
| 2026 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2021 | 
| 2026 | бронза | bronza | Matijašević · Tri Doline Merlot 2021 | 
| 2026 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2018 | 
| 2026 | бронза | bronza | Marko · Carine Merlot-Cabernet Sauvignon 2020 | 
| 2026 | бронза | bronza | Aleksandrović · Trijumf Noir Brut 2022 | 
| 2026 | золото | zlato | Tarpoš · Chardonnay Extra Brut 2021 | 
| 2026 | платина | platina | Aleksandrović · Kameničarka Prokupac 2022 | 
| 2026 | серебро | srebro | Matijašević · Belina 2022 | 
| 2025 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2020 | 
| 2025 | бронза | bronza | Tarpoš · Merlot 2021 | 
| 2025 | бронза | bronza | Despotika · Dokaz Cabernet Sauvignon 2021 | 
| 2025 | бронза | bronza | Tarpoš · Chardonnay Extra Brut 2021 | 
| 2025 | золото | zlato | Tarpoš · Prokupac 2023 | 
| 2025 | золото | zlato | Despotika · Krunski Dokaz 2017 | 
| 2025 | лучшее белое, международные сорта | 1 | Matijašević · SoviNoa Fumé Blanc 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Trijumf Gold 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2025 | серебро | srebro | Aleksandrović · Regent Reserve 2020 | 
| 2025 | серебро | srebro | Despotika · Barik Morava 2022 | 
| 2025 | серебро | srebro | Aleksandrović · Trijumf Rosé Brut 2019 | 
| 2024 | бронза | bronza | Despotika · Trag 2021 | 
| 2024 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2021 | 
| 2024 | бронза | bronza | Despotika · Morava 2022 | 
| 2024 | бронза | bronza | Tarpoš · Sauvignon Blanc 2023 | 
| 2024 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2019 | 
| 2024 | бронза | bronza | Despotika · Dokaz 2019 | 
| 2024 | бронза | bronza | Despotika · Nemir 2023 | 
| 2024 | золото | zlato | Aleksandrović · Vožd Cabernet Sauvignon 2017 | 
| 2024 | лучшая молодая винодельня | 1 | Draganić | 
| 2024 | лучшее красное, международные сорта | 1 | Arsenijević · Cabernet Sauvignon 2020 | 
| 2024 | лучшее красное, местные сорта | 1 | Marko · Doajen Prokupac 2022 | 
| 2024 | серебро | srebro | Aleksandrović · Prokupac 2020 | 
| 2024 | серебро | srebro | Matijašević · Cukundeda Prokupac 2021 | 
| 2024 | серебро | srebro | Tarpoš · Tamjanika 2023 | 
| 2024 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2024 | серебро | srebro | Aleksandrović · Regent Reserve 2019 | 
| 2023 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2017 | 
| 2023 | бронза | bronza | Tarpoš · Merlot 2017 | 
| 2023 | бронза | bronza | Tarpoš · Chardonnay 2022 | 
| 2023 | бронза | bronza | Matijašević · 7 Hrastova Cuvée 2021 | 
| 2023 | золото | zlato | Matijašević · Tri Doline 2020 | 
| 2023 | золото | zlato | Matijašević · Sovinoa Fumé Blanc 2021 | 
| 2023 | лучшее красное | 1 | Radovanović · Cabernet Sauvignon Grand Reserva 2017 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Matijašević · Belina 2021 | 
| 2023 | серебро | srebro | Matijašević · Sovinoa Sauvignon Blanc 2021 | 
| 2022 | бронза | bronza | Matijašević · Belina 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Trijumf Terroir 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2022 | бронза | bronza | Tarpoš · Lipar 2021 | 
| 2022 | бронза | bronza | Tarpoš · Tamjanika 2021 | 
| 2022 | бронза | bronza | Tarpoš · Rosé 2021 | 
| 2022 | золото | zlato | Matijašević · SoviNoa Fumé Blanc 2020 | 
| 2022 | золото | zlato | Aleksandrović · Regent Reserve 2018 | 
| 2022 | серебро | srebro | Aleksandrović · Trijumf Gold 2020 | 
| 2022 | серебро | srebro | Matijašević · Sovinoa Sauvignon Blanc 2020 | 
| 2022 | серебро | srebro | Matijašević · Čukundeda Prokupac 2019 | 
| 2022 | серебро | srebro | Matijašević · Čukundeda Superiore 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Prokupac 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Vožd Cabernet Sauvignon 2017 | 
| 2022 | серебро | srebro | Tarpoš · Menuet 2021 | 
| 2022 | серебро | srebro | Tarpoš · 1804 2015 | 
| 2021 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2021 | бронза | bronza | Matijašević · Rock & Rose 2019 | 
| 2021 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2021 | бронза | bronza | Aleksandrović · Regent Reserve 2017 | 
| 2021 | бронза | bronza | Aleksandrović · Vožd 2017 | 
| 2021 | золото | zlato | Matijašević · SoviNoa 2019 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Noir 2010 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Gold 2019 | 
| 2020 | бронза | bronza | Despotika · Zmajeviti 2017 | 
| 2020 | бронза | bronza | Despotika · Krunski Dokaz Cabernet Sauvignon 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Regent Reserve 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2020 | лучшее красное | 1 | Radovanović · Cabernet Sauvignon Reserve 2017 | 
| 2020 | серебро | srebro | Despotika · Trag 2017 | 
| 2020 | серебро | srebro | Aleksandrović · Vizija Selection 2016 | 
| 2020 | серебро | srebro | Aleksandrović · Trijumf Gold 2018 | 
| 2018 | бронза | bronza | Despotika · Nebo Riesling-Pinot Blanc 2016 | 
| 2018 | бронза | bronza | Despotika · Morava 2016 | 
| 2018 | бронза | bronza | Despotika · TRAG Merlot 2016 | 
| 2017 | бронза | bronza | Despotika · Morava 2016 | 
| 2017 | бронза | bronza | Despotika · Trag 2015 | 
| 2017 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2017 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2012 | 
| 2017 | серебро | srebro | Despotika · Dokaz 2015 | 
| 2017 | серебро | srebro | Aleksandrović · Vizija 2015 | 
| 2016 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2016 | бронза | bronza | Radovanović · 25 Reserve Cabernet Sauvignon 2012 | 
| 2016 | бронза | bronza | Despotika · Trag 2013 | 
| 2016 | бронза | bronza | Radovanović · Selekcija Chardonnay 2013 | 
| 2016 | серебро | srebro | Aleksandrović · Trijumf Barrique 2012 | 
| 2016 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2009 | 
| 2015 | бронза | bronza | Aleksandrović · Trijumf 2013 | 
| 2015 | бронза | bronza | Aleksandrović · Trijumf Barrique 2012 | 
| 2015 | бронза | bronza | Despotika · Dokaz 2012 | 
| 2015 | бронза | bronza | Aleksandrović · Regent 2009 | 
| 2015 | серебро | srebro | Aleksandrović · Rodoslov 2009 | 

## Три Моравы и Жупа

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Ivanović · Prokupac Gaga | 2017 | 96 | Falstaff |
| Temet · Tamjanika | 2016 | 95 | Falstaff |
| Temet · Tri Morave Belo Reserve | 2018 | 95 | Falstaff |
| Temet · Tri Morave Reserva | 2016 | 95 | decanter |
| Vinarija Jovac · Stella Noir | 2020 | 95 | decanter |
| Vinarija Jovac · Stella Noir | 2021 | 95 | decanter |
| Vinarija Jovac · Stella Noir | 2020 | 95 | decanter |
| Temet · Tri Morave Crveno Reserve | 2009 | 94 | Falstaff |
| Ivanović · No 1/2 | 2019 | 94 | vino.rs |
| Temet · Tri Morave Crveno Reserve | 2019 | 94 | Falstaff |
| Budimir · Svb Rosa | 2009 | 94 | Falstaff |
| Temet · Beli Kamen Merlot | 2019 | 94 | decanter |
| Temet · Ergo | 2018 | 94 | decanter |
| Ivanović · No ½ | 2018 | 94 | Falstaff |
| Ivanović · Prokupac | 2017 | 94 | Falstaff |
| Čokot · Prokupac Radovan 100% | 2020 | 94 | Falstaff |
| Čokot · Radovan 100% Prokupac | 2019 | 93 | Falstaff |
| Čokot · Tamjanika Radovan 100% | 2022 | 93 | Falstaff |
| Temet · Tri Morave Reserve | 2018 | 93 | decanter |
| Čokot · Tamjanika Radovon 100% | 2022 | 93 | Falstaff |
| Čokot · Prokupac Experiment | 2019 | 93 | Falstaff |
| Rubin · Rubinov Prokupac | 2017 | 92 | decanter |
| Čokot · Experiment Prokupac | 2019 | 92 | decanter |
| Vinarija Jovac · Cabernet Sauvignon | 2020 | 92 | decanter |
| Spasić · Tamjanika | 2021 | 92 | Falstaff |
| Cilić · Onyx Blanc | 2019 | 92 | Falstaff |
| Ivanović · Zanos | 2015 | 92 | Falstaff |
| Ivanović · Tamjanika | 2022 | 92 | Falstaff |
| Ivanović · No 3/4 Tamjanika | 2021 | 92 | Falstaff |
| Ivanović · Prokupac | 2021 | 92 | Falstaff |
| Čokot · Prokupac Experiment | 2018 | 92 | Falstaff |
| Čokot · Tamjanika Experiment | 2022 | 92 | Falstaff |
| Čokot · Experiment Prokupac | 2015 | 91 | decanter |
| Temet · Ergo | 2016 | 91 | decanter |
| Čokot · Radovan 100% Prokupac | 2020 | 91 | decanter |
| Temet · White Stone Merlot | 2017 | 91 | decanter |
| Temet · Ergo | 2018 | 91 | decanter |
| Ivanović · Jara Pet Net | 2022 | 91 | Falstaff |
| Čokot · Radovan Prokupac | 2015 | 90 | decanter |
| Temet · Tri Morave | 2019 | 90 | decanter |
| Ivanović · No 1/2 | 2019 | 90 | decanter |
| Temet · Ergo | 2019 | 90 | decanter |
| Vinarija Jovac · Merlot | 2020 | 90 | decanter |
| Čokot · Radovan 100% Prokupac | 2023 | 90 | decanter |
| Temet · Ergo Rosé | 2019 | 90 | decanter |
| Temet · Tri Morave | 2017 | 90 | decanter |
| Temet · Tri Morave Reserve | 2017 | 90 | decanter |
| Temet · Tri Morave Reserve | 2019 | 90 | decanter |
| Temet · Ergo | 2018 | 90 | decanter |
| Temet · Tri Morave Reserve | 2021 | 90 | decanter |
| Temet · Tri Morave | 2017 | 89 | decanter |
| Čokot · Experiment Prokupac | 2016 | 89 | decanter |
| Temet · Ergo Belo | 2016 | 89 | decanter |
| Temet · Ergo | 2017 | 89 | decanter |
| Temet · Tri Morave Brut | 2017 | 89 | decanter |
| Temet · Beli Kamen Merlot | 2018 | 89 | decanter |
| Temet · Tri Morave Red | 2019 | 89 | decanter |
| Temet · Tri Morave Reserve | 2021 | 89 | decanter |
| Vinarija Jovac · Cabernet Sauvignon | 2020 | 89 | decanter |
| Temet · Ergo White | 2015 | 88 | decanter |
| Temet · Tri Morave | 2016 | 88 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 88 | decanter |
| Temet · Burgundac Sivi | 2019 | 88 | decanter |
| Temet · Ergo | 2018 | 88 | decanter |
| Temet · Ergo | 2016 | 88 | decanter |
| Temet · Tri Morave | 2018 | 88 | decanter |
| Temet · Tri Morave | 2019 | 88 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 88 | decanter |
| Temet · Tri Morave Reserve | 2019 | 88 | decanter |
| Temet · Ergo | 2019 | 88 | decanter |
| Temet · Tri Morave Rosé | 2015 | 87 | decanter |
| Temet · Tri Morave Red | 2015 | 87 | decanter |
| Ivanović · Prokupac | 2016 | 87 | decanter |
| Čokot · Experiment Prokupac | 2017 | 87 | decanter |
| Rubin · Amante Carmen | 2016 | 87 | decanter |
| Rubin · Cabernet Sauvignon | 2016 | 87 | decanter |
| Temet · Pinot Grigio | 2018 | 87 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 87 | decanter |
| Temet · Tri Morave | 2020 | 87 | decanter |
| Temet · Tri Morave Reserve | 2019 | 87 | decanter |
| Rubin · Sauvignon Blanc | 2019 | 87 | decanter |
| Rubin · Prokupac | 2018 | 87 | decanter |
| Vinarija Jovac · Tamjanika | 2021 | 87 | decanter |
| Rubin · Amante Matea Merlot | 2018 | 87 | decanter |
| Temet · Beli Kamen Prokupac | 2019 | 87 | decanter |
| Temet · White Stone Syrah | 2017 | 87 | decanter |
| Temet · Ergo | 2017 | 87 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 87 | decanter |
| Vinarija Jovac · Merlot | 2020 | 87 | decanter |
| Temet · Tri Morave | 2015 | 86 | decanter |
| Temet · Tri Morave White | 2016 | 86 | decanter |
| Temet · Pinot Grigio | 2016 | 86 | decanter |
| Ivanović · No 1/2 | 2015 | 86 | decanter |
| Temet · Tri Morave | 2018 | 86 | decanter |
| Temet · Tri Morave Reserve | 2017 | 86 | decanter |
| Rubin · Amante Matea | 2018 | 86 | decanter |
| Temet · Beli Kamen Syrah | 2019 | 86 | decanter |
| Ivanović · No 3/4 | 2023 | 86 | decanter |
| Temet · Ergo | 2017 | 86 | decanter |
| Vinarija Jovac · Merlot | 2020 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Temet · Tri Morave Reserve 2019 | 
| 2026 | бронза | bronza | Temet · Ergo 2018 | 
| 2026 | бронза | bronza | Temet · White Stone Syrah 2017 | 
| 2026 | золото | zlato | Vinarija Jovac · Stella Noir 2020 | 
| 2026 | серебро | srebro | Temet · Ergo 2019 | 
| 2026 | серебро | srebro | Vinarija Jovac · Merlot 2020 | 
| 2026 | серебро | srebro | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2026 | серебро | srebro | Temet · White Stone Merlot 2017 | 
| 2026 | серебро | srebro | Temet · Ergo Rosé 2019 | 
| 2025 | бронза | bronza | Ivanović · No 3/4 2023 | 
| 2025 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2025 | бронза | bronza | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2025 | золото | zlato | Vinarija Jovac · Stella Noir 2021 | 
| 2025 | лучшая малая винодельня | 1 | Ralević | 
| 2025 | лучшее красное, международные сорта | 1 | Ralević · Aurum 2020 | 
| 2025 | лучшее красное, органика, местные сорта | 1 | Vujić · Prokupac Gmitar 2021 | 
| 2025 | серебро | srebro | Čokot · Radovan 100% Prokupac 2023 | 
| 2024 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2024 | бронза | bronza | Rubin · Amante Matea Merlot 2018 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Prokupac 2019 | 
| 2024 | лучшее белое, местные сорта | 1 | Yotta · Hysteresis Tamjanika 2022 | 
| 2024 | лучшее белое, органика, местные сорта | 1 | Ivanović · No 3/4 2023 | 
| 2024 | серебро | srebro | Temet · Tri Morave Reserve 2021 | 
| 2024 | серебро | srebro | Temet · Ergo 2018 | 
| 2024 | серебро | srebro | Čokot · Experiment Prokupac 2019 | 
| 2023 | бронза | bronza | Vinarija Jovac · Tamjanika 2021 | 
| 2023 | бронза | bronza | Temet · Tri Morave Reserve 2019 | 
| 2023 | бронза | bronza | Temet · Beli Kamen Syrah 2019 | 
| 2023 | бронза | bronza | Temet · Ergo 2019 | 
| 2023 | золото | zlato | Vinarija Jovac · Stella Noir 2020 | 
| 2023 | серебро | srebro | Temet · Ergo 2018 | 
| 2023 | серебро | srebro | Temet · Tri Morave Reserve 2019 | 
| 2023 | серебро | srebro | Ivanović · No 1/2 2019 | 
| 2023 | серебро | srebro | Temet · Tri Morave 2019 | 
| 2023 | серебро | srebro | Temet · Beli Kamen Merlot 2019 | 
| 2023 | серебро | srebro | Čokot · Radovan 100% Prokupac 2020 | 
| 2022 | бронза | bronza | Temet · Tri Morave 2020 | 
| 2022 | бронза | bronza | Temet · Tri Morave Red 2019 | 
| 2022 | бронза | bronza | Temet · Burgundac Sivi 2019 | 
| 2022 | бронза | bronza | Rubin · Sauvignon Blanc 2019 | 
| 2022 | бронза | bronza | Temet · Ergo 2017 | 
| 2022 | бронза | bronza | Rubin · Prokupac 2018 | 
| 2022 | лучшее красное | 4 | Budimir · Triada crveno 2020 | 
| 2022 | серебро | srebro | Temet · Tri Morave Reserve 2018 | 
| 2022 | серебро | srebro | Temet · Ergo 2018 | 
| 2021 | бронза | bronza | Rubin · Amante Matea 2018 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2021 | бронза | bronza | Temet · Ergo 2017 | 
| 2021 | бронза | bronza | Temet · Tri Morave Reserve 2017 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2020 | бронза | bronza | Temet · Ergo 2017 | 
| 2020 | бронза | bronza | Rubin · Cabernet Sauvignon 2016 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2018 | 
| 2020 | бронза | bronza | Temet · Pinot Grigio 2018 | 
| 2020 | бронза | bronza | Temet · Tri Morave Brut 2017 | 
| 2020 | винодельня года | 1 | Temet | 
| 2020 | лучшее розе | 1 | Temet · Ergo Rose 2018 | 
| 2020 | серебро | srebro | Temet · Tri Morave Reserve 2017 | 
| 2020 | серебро | srebro | Rubin · Rubinov Prokupac 2017 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2017 | 
| 2019 | бронза | bronza | Čokot · Experiment Prokupac 2017 | 
| 2019 | бронза | bronza | Temet · Ergo Belo 2016 | 
| 2019 | бронза | bronza | Rubin · Amante Carmen 2016 | 
| 2019 | винодельня года | 1 | Temet | 
| 2019 | золото | zlato | Temet · Tri Morave Reserva 2016 | 
| 2019 | лучшее белое | 1 | Cilić · Onyx Belo 2017 | 
| 2019 | лучшее красное | 1 | Temet · Tri Morave Rezerva Crveno 2016 | 
| 2019 | серебро | srebro | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Temet · Pinot Grigio 2016 | 
| 2018 | бронза | bronza | Temet · Tri Morave 2016 | 
| 2018 | бронза | bronza | Ivanović · No 1/2 2015 | 
| 2018 | бронза | bronza | Čokot · Experiment Prokupac 2016 | 
| 2018 | бронза | bronza | Ivanović · Prokupac 2016 | 
| 2018 | серебро | srebro | Temet · Tri Morave 2017 | 
| 2018 | серебро | srebro | Čokot · Radovan Prokupac 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave White 2016 | 
| 2017 | бронза | bronza | Temet · Ergo White 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Rosé 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Red 2015 | 
| 2017 | серебро | srebro | Čokot · Experiment Prokupac 2015 | 
| 2016 | бронза | bronza | Temet · Tri Morave 2015 | 
| 2015 | бронза | bronza | Temet · Tri  Bele 2014 | 
| 2015 | бронза | bronza | Temet · Pinot Grigio 2014 | 
| 2015 | серебро | srebro | Temet · Dobra Godina 2011 | 

## Неготинска Крайина

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Matalj · Kremen Kamen | 2021 | 97 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2019 | 97 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2020 | 96 | Falstaff |
| Matalj · Zamna Cabernet Sauvignon | 2020 | 96 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2016 | 95 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2017 | 95 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2016 | 95 | decanter |
| Matalj · Bukovski Cuvée | 2021 | 95 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2017 | 95 | Falstaff |
| Matalj · Bagrina Buksovska | 2022 | 94 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | — | 92 | Wine-Searcher |
| Matalj · Terasa Chardonnay | 2013 | 92 | decanter |
| Manastir Bukovo · Filigran Гаме | 2017 | 92 | decanter |
| Matalj · Zemna Reserva | 2021 | 92 | decanter |
| Matalj · Black Tamjanika | 2022 | 92 | Falstaff |
| Matalj · Terasa Sauvignon Blanc | 2022 | 92 | Falstaff |
| Manastir Bukovo · Chardonnay Oaked | 2021 | 92 | Falstaff |
| Matalj · Kremen | 2020 | 92 | Falstaff |
| Matalj · Terasa Chardonnay | 2022 | 92 | Falstaff |
| Matalj · Bukovski Prokupac | 2020 | 91 | decanter |
| Matalj · Bagrina | 2023 | 91 | decanter |
| Matalj · Bukovski Cuvée | 2022 | 91 | decanter |
| Manastir Bukovo · Black Tamjanika | 2020 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Cabernet Sauvignon | 2019 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Gamay | 2019 | 91 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2013 | 90 | decanter |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 2013 | 90 | decanter |
| Matalj · Kremen | 2017 | 90 | decanter |
| Matalj · Crna Tamjanika | 2021 | 90 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2022 | 90 | decanter |
| Matalj · Terasa Chardonnay | 2022 | 90 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2023 | 90 | decanter |
| Matalj · Zemna Reserva | 2021 | 90 | decanter |
| Manastir Bukovo · Filigran Chardonnay | 2022 | 90 | Falstaff |
| Matalj · Bukovski | 2020 | 90 | Falstaff |
| Manastir Bukovo · Bez | 2018 | 90 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2015 | 89 | decanter |
| Matalj · Bukovski Cuvée | 2018 | 89 | decanter |
| Matalj · Bukovski Prokupac-Začinak | 2021 | 89 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2024 | 89 | decanter |
| Matalj · Dušica Rosé | 2022 | 89 | Falstaff |
| Manastir Bukovo · Filigran Rosé | 2022 | 89 | Falstaff |
| Manastir Bukovo · Cabernet Sauvignon | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Gamay | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Reserve Merlot | 2019 | 89 | Falstaff |
| Manastir Bukovo · Filigran Гаме | 2015 | 88 | decanter |
| Matalj · Terasa Chardonnay | 2016 | 88 | decanter |
| Manastir Bukovo · Filigran Pinot Noir | 2016 | 88 | decanter |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 2017 | 88 | decanter |
| Matalj · Zamna | 2020 | 88 | decanter |
| Matalj · Kremen | 2022 | 88 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2015 | 87 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2016 | 87 | decanter |
| Manastir Bukovo · Filigran Chardonnay | 2017 | 87 | decanter |
| Matalj · Terasa Chardonnay | 2018 | 87 | decanter |
| Manastir Bukovo · Filigran Merlot | 2017 | 87 | decanter |
| Matalj · Terasa Chardonnay | 2019 | 87 | decanter |
| Matalj · Kremen | 2020 | 87 | decanter |
| Matalj · Kremen Cabernet-Merlot | 2021 | 87 | decanter |
| Matalj · Kremen | 2023 | 87 | decanter |
| Matalj · Terasa Chardonnay | 2017 | 86 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2020 | 86 | decanter |
| Matalj · Bagrina | 2024 | 86 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2016 | 86 | decanter |
| Matalj · Bukovski Cuvée | 2018 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Matalj · Bagrina 2024 | 
| 2026 | бронза | bronza | Matalj · Kremen 2023 | 
| 2026 | платина | platina | Matalj · Kremen Kamen 2021 | 
| 2026 | серебро | srebro | Matalj · Bukovski Cuvée 2022 | 
| 2025 | бронза | bronza | Matalj · Terasa Sauvignon Blanc 2024 | 
| 2025 | бронза | bronza | Matalj · Kremen 2022 | 
| 2025 | винодельня года | 1 | Matalj | 
| 2025 | золото | zlato | Matalj · Bukovski Cuvée 2021 | 
| 2025 | лучшее красное, местные сорта | 1 | Matalj · Bukovski Cuvee 2021 | 
| 2025 | серебро | srebro | Matalj · Bagrina 2023 | 
| 2025 | серебро | srebro | Matalj · Zemna Reserva 2021 | 
| 2024 | бронза | bronza | Matalj · Kremen Cabernet-Merlot 2021 | 
| 2024 | бронза | bronza | Matalj · Bukovski Prokupac-Začinak 2021 | 
| 2024 | серебро | srebro | Matalj · Bukovski Prokupac 2020 | 
| 2024 | серебро | srebro | Matalj · Zemna Reserva 2021 | 
| 2024 | серебро | srebro | Matalj · Terasa Chardonnay 2022 | 
| 2024 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2023 | 
| 2023 | бронза | bronza | Matalj · Zamna 2020 | 
| 2023 | бронза | bronza | Matalj · Kremen 2020 | 
| 2023 | лучшее из местных сортов, красное | 1 | Matalj · Bukovski Cuvee 2019 | 
| 2023 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2022 | 
| 2022 | бронза | bronza | Matalj · Terasa Chardonnay 2019 | 
| 2022 | бронза | bronza | Matalj · Bukovski Cuvée 2018 | 
| 2022 | лучшее красное | 5 | Manastir Bukovo · Filigran Merlot 2021 | 
| 2022 | серебро | srebro | Matalj · Kremen 2017 | 
| 2022 | серебро | srebro | Matalj · Crna Tamjanika 2021 | 
| 2021 | бронза | bronza | Matalj · Bukovski Cuvée 2018 | 
| 2021 | бронза | bronza | Matalj · Terasa Sauvignon Blanc 2020 | 
| 2021 | бронза | bronza | Manastir Bukovo · Filigran Cabernet Sauvignon 2017 | 
| 2021 | бронза | bronza | Manastir Bukovo · Filigran Merlot 2017 | 
| 2021 | серебро | srebro | Manastir Bukovo · Filigran Гаме 2017 | 
| 2020 | бронза | bronza | Matalj · Terasa Chardonnay 2018 | 
| 2020 | бронза | bronza | Manastir Bukovo · Filigran Pinot Noir 2016 | 
| 2020 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2016 | 
| 2020 | бронза | bronza | Manastir Bukovo · Filigran Chardonnay 2017 | 
| 2020 | золото | zlato | Matalj · Kremen Kamen Cabernet Sauvignon 2016 | 
| 2019 | бронза | bronza | Matalj · Terasa Chardonnay 2017 | 
| 2019 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2016 | 
| 2019 | бронза | bronza | Manastir Bukovo · Filigran Гаме 2015 | 
| 2019 | бронза | bronza | Matalj · Kremen Kamen Cabernet Sauvignon 2015 | 
| 2017 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2015 | 
| 2017 | серебро | srebro | Matalj · Terasa Chardonnay 2013 | 
| 2017 | серебро | srebro | Matalj · Kremen Kamen Cabernet Sauvignon 2013 | 
| 2017 | серебро | srebro | Manastir Bukovo · Filigran Cabernet Sauvignon 2013 | 
| 2015 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2013 | 

## Топлица

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Doja · Prokupac | 2018 | 95 | decanter |
| Doja · Breg Prokupac | 2017 | 95 | decanter |
| Doja · Breg Prokupac | 2020 | 95 | decanter |
| Doja · Prokupac Breg | 2019 | 95 | Falstaff |
| Doja · Cabernet Sauvignon Breg | 2019 | 94 | Falstaff |
| Doja · Cabernet Sauvigon Breg | 2019 | 94 | Falstaff |
| Doja · Breg Merlot | 2019 | 93 | decanter |
| Doja · Merlot Breg | 2019 | 93 | Falstaff |
| Doja · Prokupac | 2019 | 93 | Falstaff |
| Doja · Breg Prokupac | 2015 | 92 | decanter |
| Doja · Breg Prokupac | 2019 | 92 | decanter |
| Doja · Breg Merlot | 2019 | 92 | decanter |
| Doja · Merlot & Cabernet Sauvignon | 2020 | 92 | Falstaff |
| Doja · Breg Cabernet Sauvignon | 2019 | 91 | decanter |
| Doja · Prokupac | 2021 | 91 | decanter |
| Doja · Chardonnay Barik | 2022 | 91 | Falstaff |
| Doja · Rosé | 2022 | 91 | Falstaff |
| Doja · Prokupac | 2019 | 90 | decanter |
| Doja · Chardonnay & Pinot Grigio | 2022 | 90 | Falstaff |
| Doja · Prokupac | 2017 | 89 | decanter |
| Doja · Tamjanica | 2022 | 89 | Falstaff |
| Doja · Belo | 2015 | 88 | decanter |
| Doja · Merlot-Cabernet Sauvignon | 2018 | 88 | decanter |
| Doja · Merlot-Cabernet Sauvignon | 2021 | 88 | decanter |
| Doja · Breg Prokupac | 2021 | 88 | decanter |
| Doja · Prokupac | 2015 | 87 | decanter |
| Doja · Breg Prokupac-Cabernet | 2017 | 87 | decanter |
| Doja · Prokupac | 2017 | 87 | decanter |
| Doja · Tamjanika | 2020 | 87 | decanter |
| Doja · Breg Prokupac | 2021 | 87 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 87 | decanter |
| Doja · Merlot-Cabernet Sauvignon | 2016 | 86 | decanter |
| Doja · Chardonnay-Pinot Grigio | 2019 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Doja · Breg Prokupac 2021 | 
| 2026 | серебро | srebro | Doja · Prokupac 2021 | 
| 2025 | бронза | bronza | Doja · Breg Prokupac 2021 | 
| 2025 | бронза | bronza | Doja · Breg Cabernet Sauvignon 2020 | 
| 2024 | бронза | bronza | Doja · Merlot-Cabernet Sauvignon 2021 | 
| 2024 | вклад в винный туризм | 1 | Doja | 
| 2024 | золото | zlato | Doja · Breg Prokupac 2020 | 
| 2024 | серебро | srebro | Doja · Breg Merlot 2019 | 
| 2023 | серебро | srebro | Doja · Prokupac 2019 | 
| 2023 | серебро | srebro | Doja · Breg Prokupac 2019 | 
| 2023 | серебро | srebro | Doja · Breg Cabernet Sauvignon 2019 | 
| 2023 | серебро | srebro | Doja · Breg Merlot 2019 | 
| 2022 | золото | zlato | Doja · Prokupac 2018 | 
| 2022 | золото | zlato | Doja · Breg Prokupac 2017 | 
| 2021 | бронза | bronza | Doja · Chardonnay-Pinot Grigio 2019 | 
| 2021 | бронза | bronza | Doja · Merlot-Cabernet Sauvignon 2018 | 
| 2021 | бронза | bronza | Doja · Tamjanika 2020 | 
| 2021 | бронза | bronza | Doja · Prokupac 2017 | 
| 2020 | бронза | bronza | Doja · Breg Prokupac-Cabernet 2017 | 
| 2020 | бронза | bronza | Doja · Prokupac 2017 | 
| 2020 | бронза | bronza | Doja · Merlot-Cabernet Sauvignon 2016 | 
| 2020 | серебро | srebro | Doja · Breg Prokupac 2015 | 
| 2017 | бронза | bronza | Doja · Belo 2015 | 
| 2017 | бронза | bronza | Doja · Prokupac 2015 | 

## Юго-восток

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksić · Amanet Vranac | 2019 | 95 | decanter |
| Aleksić · Biser Smederevka Extra Brut | 2016 | 95 | decanter |
| Aleksić · Žuti Cvet Penuśavo Tamnjanika Sec | 2019 | 95 | decanter |
| Aleksić · Biser Smederevka Brut | 2014 | 92 | decanter |
| Aleksić · Kardas Cabernet Sauvignon | 2021 | 92 | decanter |
| Aleksić · Biser Extra Brut | 2016 | 91 | Falstaff |
| Aleksić · Žuti Cvet Tamjanika | 2025 | 91 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2015 | 90 | decanter |
| Aleksić · Kardaş Limited Cabernet Sauvignon | 2012 | 90 | decanter |
| Aleksić · Žuti Cvet Tamjanika | 2017 | 90 | decanter |
| Aleksić · Amanet Vranac | 2013 | 90 | decanter |
| Aleksić · Žuti Cvet Tamjanika Dry | 2019 | 90 | decanter |
| Aleksić · Cabernet Franc | 2020 | 90 | decanter |
| Aleksić · Kardas Limited Cabernet Sauvignon | 2021 | 90 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2018 | 89 | decanter |
| Aleksić · Zuti Cvet Tamjanika Extra Brut | 2023 | 89 | decanter |
| Aleksić · Kardaš Limited | 2011 | 88 | decanter |
| Aleksić · Temperament Merlot | 2015 | 88 | decanter |
| Aleksić · Amanet Vranac | 2015 | 88 | decanter |
| Aleksić · Prokupac | 2021 | 88 | decanter |
| Aleksić · Zuti Cvet Extra Brut | 2022 | 88 | decanter |
| Aleksić · Morava | 2025 | 88 | decanter |
| Aleksić · Zuti Cvet Penusavo | 2015 | 87 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2019 | 87 | decanter |
| Aleksić · Temperament Merlot | 2015 | 87 | decanter |
| Aleksić · Bonaca Chardonnay | 2021 | 87 | decanter |
| Aleksić · Zuti Cvet | 2023 | 87 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2023 | 87 | decanter |
| Aleksić · Zuti Cvet Tamjanica | 2024 | 87 | decanter |
| Aleksić · Prokupac | 2021 | 87 | decanter |
| Aleksić · Kardaš | 2013 | 86 | decanter |
| Aleksić · Nostalgija | 2017 | 86 | decanter |
| Aleksić · Kardaš Cabernet Sauvignon | 2017 | 86 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2019 | 86 | decanter |
| Aleksić · Kardaš Limited Cabernet Sauvignon | 2015 | 86 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2021 | 86 | decanter |
| Aleksić · Kontra | 2020 | 86 | decanter |
| Aleksić · Zuti Cvet Tamjanika Sec | 2021 | 86 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Aleksić · Morava 2025 | 
| 2026 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika Extra Brut 2023 | 
| 2026 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2025 | 
| 2025 | бронза | bronza | Aleksić · Zuti Cvet Tamjanica 2024 | 
| 2025 | бронза | bronza | Aleksić · Zuti Cvet Extra Brut 2022 | 
| 2025 | серебро | srebro | Aleksić · Kardas Cabernet Sauvignon 2021 | 
| 2024 | бронза | bronza | Aleksić · Prokupac 2021 | 
| 2024 | бронза | bronza | Aleksić · Zuti Cvet 2023 | 
| 2024 | бронза | bronza | Aleksić · Arno Sauvignon Blanc 2023 | 
| 2024 | серебро | srebro | Aleksić · Kardas Limited Cabernet Sauvignon 2021 | 
| 2023 | бронза | bronza | Aleksić · Prokupac 2021 | 
| 2023 | бронза | bronza | Aleksić · Kontra 2020 | 
| 2023 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika Sec 2021 | 
| 2023 | лучшая малая винодельня | 1 | Jović | 
| 2022 | бронза | bronza | Aleksić · Bonaca Chardonnay 2021 | 
| 2022 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2021 | 
| 2022 | золото | zlato | Aleksić · Amanet Vranac 2019 | 
| 2022 | золото | zlato | Aleksić · Biser Smederevka Extra Brut 2016 | 
| 2022 | золото | zlato | Aleksić · Žuti Cvet Penuśavo Tamnjanika Sec 2019 | 
| 2022 | серебро | srebro | Aleksić · Cabernet Franc 2020 | 
| 2021 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2021 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika Dry 2019 | 
| 2020 | бронза | bronza | Aleksić · Kardaš Cabernet Sauvignon 2017 | 
| 2020 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2019 | 
| 2020 | бронза | bronza | Aleksić · Arno Sauvignon Blanc 2019 | 
| 2020 | бронза | bronza | Aleksić · Kardaš Limited Cabernet Sauvignon 2015 | 
| 2019 | бронза | bronza | Aleksić · Nostalgija 2017 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2018 | 
| 2019 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2019 | бронза | bronza | Aleksić · Amanet Vranac 2015 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Penusavo 2015 | 
| 2018 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2017 | 
| 2018 | серебро | srebro | Aleksić · Amanet Vranac 2013 | 
| 2018 | серебро | srebro | Aleksić · Biser Smederevka Brut 2014 | 
| 2017 | серебро | srebro | Aleksić · Arno Sauvignon Blanc 2015 | 
| 2017 | серебро | srebro | Aleksić · Kardaş Limited Cabernet Sauvignon 2012 | 
| 2016 | бронза | bronza | Aleksić · Kardaš Limited 2011 | 
| 2016 | бронза | bronza | Aleksić · Kardaš 2013 | 
| 2015 | лучшая национальная винодельня | 1 | Aleksić | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 

## Подунавье и Белградский район

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Plavinac · Smederevka | 2025 | 88 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Plavinac · Smederevka 2025 | 

## Косово и Метохия

Оценок критиков не найдено.

## Хозяйства без района

- Veritas · Momentum Cabernet Sauvignon 2017 — 95 [decanter]
- Grabak · Vivak Prokupac 2017 — 95 [decanter]
- BT Winery · Limited Edition King Supreme Marselan 2018 — 95 [decanter]
- Reljić Vinarija · Rebus  Merlot-Cabernet Sauvignon-Probus 2018 — 95 [decanter]
- BT Winery · Mister Marselan 2021 — 95 [decanter]
- šApat Wine Atelier · Atila Chardonnay 2022 — 95 [decanter]
- Virtus · Morava 2023 — 95 [decanter]
- La Gora · Bello 2025 — 95 [decanter]
- Molowinery · Vista Hill Red Reserve 2010 — 94 [decanter]
- Vinarija Trišić · Dimasid 2013 — 94 [decanter]
- Stemina · Draga 2008 — 94 [decanter]
- Dibonis Winery · Di Icewine 2020 — 94 [decanter]
- Vinarija Dragić · Crni Biser 2023 — 94 [decanter]
- Vino Budimir · Svb Rosa 2009 — 94 [Falstaff]
- šApat Wine Atelier · Reserve Cabernet Sauvignon 2020 — 93 [decanter]
- Virtus · Pinot Grigio 2024 — 93 [decanter]
- Vinarija Frug · Signum Cabernet Sauvignon 2021 — 93 [decanter]
- Dolina · Cuveé Barrique 2019 — 93 [decanter]
- Vinarija Eden · Velvet 2020 — 93 [decanter]
- Veritas · Momentum Cabernet Sauvignon 2017 — 93 [decanter]
- Vinarija Lastar · Triangl Pinot Noir 2017 — 92 [decanter]
- Vinarija Frunza Aglaja · Dentelle 2016 — 92 [decanter]
- Vista Hill Plus · White Reserve 2012 — 92 [decanter]
- Virtus · Credo Beli 2019 — 92 [decanter]
- Vinarija Sokolov Zamak · Moscato Giallo 2021 — 92 [decanter]
- Vinarija Sokolov Zamak · Marselan 2019 — 92 [decanter]
- Grabak · Prokupac 2020 — 92 [decanter]
- Vinarija Frug · Cuvée 2022 — 92 [decanter]
- Traško Vinarija · Edición Limitada Bagrina 2024 — 92 [decanter]
- Podrum Pevac · Tišina Malvazija 2025 — 92 [decanter]
- La Gora · Lupo 2025 — 92 [decanter]
- Vinarija Frug · Grašac 2025 — 92 [decanter]
- Dolina · Euphonia Gran Reserva 2018 — 92 [decanter]
- Virtus · Credo 2013 — 92 [decanter]
- Vinarija Frug · Signum Chardonnay 2023 — 92 [decanter]
- Vinarija DeLena · 1903 Merlot 2017 — 92 [Falstaff]
- Vino Budimir · Angel 2016 — 92 [Falstaff]
- Vino Budimir · Prokupac boje lila 2012 — 92 [Falstaff]
- Vinarija Jeremic · Kanon Merlot Cabernet Sauvignon 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Tamjanika 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Prokupac 2018 — 92 [Falstaff]
- Virtus W · Prokupac 2016 — 91 [decanter]
- Podrum Janko · Crveni Zapis 2016 — 91 [decanter]
- Podrum Janko · Zavet Stari 2016 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Vinarija Aven · Merlot 2019 — 91 [decanter]
- Podrum Janko · Zavet Stari 2017 — 91 [decanter]
- Podrum Stari Hrast · Selekcija Merlot 2017 — 91 [decanter]
- Reljić Vinarija · Rebus Reserve 2019 — 91 [decanter]
- Vinarija Lastar · Sofijin Izbor Pinot Noir 2019 — 91 [decanter]
- Matalj Vainarija · Bukovski Cuvée 2019 — 91 [decanter]
- Vinarija Stupovi · Merlot 2021 — 91 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2021 — 91 [decanter]
- Virtus · Prokupac 2020 — 91 [decanter]
- Vinarija Lastar · Cabernet Franc 2020 — 91 [decanter]
- Vinarija Savic · Merlot 2021 — 91 [decanter]
- šApat Wine Atelier · Bianca Moscato Giallo 2023 — 91 [decanter]
- Vinarija Komuna · Rara Avis 2020 — 91 [decanter]
- Virtus · Marselan 2020 — 91 [decanter]
- Vinarija Dragić · Beli Biser 2022 — 91 [decanter]
- Vinarija Frug · Signum Syrah 2022 — 91 [decanter]
- Vinarija Stanković · Chardonnay 2024 — 91 [decanter]
- Chardonnay · Omnibus Lector Chardonnay 2024 — 91 [decanter]
- Vinarija Frug · Pinot Noir 2022 — 91 [decanter]
- Vinarija Imperator · Constantius 2023 — 91 [decanter]
- Vinarija Dragić · Mitra 2025 — 91 [decanter]
- Dolina · Barrique Xix Reserve 2019 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Podrum Džervin 1927 · Trifun Grand Cabernet Sauvignon 2019 — 91 [decanter]
- PIK Oplenac · Monarh Immortal S 2017 — 91 [Falstaff]
- Vinarija Jeremic · Sonata Sauvignon Blanc 2021 — 91 [Falstaff]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2019 — 91 [Falstaff]
- Virtus · Credo 2013 — 90 [decanter]
- Molowinery · Plavi Princip 2013 — 90 [decanter]
- Winery Aleksić Doo · Bonaca Limited 2014 — 90 [decanter]
- Podrum Janko · Vrtlog 2015 — 90 [decanter]
- Vinarija Dumo · Pinot Noir 2015 — 90 [decanter]
- Manastira Bukovo · Merlot 2015 — 90 [decanter]
- Virtus W · Pinot Grigio 2017 — 90 [decanter]
- Podrum Janko · Zavet Stari 2015 — 90 [decanter]
- Virtus · Marselan 2016 — 90 [decanter]
- Pusula · Traminac 2017 — 90 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2017 — 90 [decanter]
- Virtus · Prokupac 2016 — 90 [decanter]
- Virtus · 733 Prokupac  — 90 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2017 — 90 [decanter]
- Zmajevac · Prokupac 2018 — 90 [decanter]
- Vinarija Sokolov Zamak · Marselan 2020 — 90 [decanter]
- Virtus · 733 2017 — 90 [decanter]
- Vinarija Fragaria · Selekcija 2019 — 90 [decanter]
- Vinarija Unikat · Vranac 2019 — 90 [decanter]
- Grabak · Sojka 2021 — 90 [decanter]
- Vinarija Đurđevića Legat · Otisak Vremena 2020 — 90 [decanter]
- Reljić Vinarija · Rebus Crveni 2020 — 90 [decanter]
- Podrum Petrović · Grašac 2022 — 90 [decanter]
- Vinarija Venčac · Legat 1903 Muscat Petit Grain 2021 — 90 [decanter]
- Château Prince · Velika Morava 2021 — 90 [decanter]
- Art Et Vinum · Meduza 2021 — 90 [decanter]
- Podrum Janko · Bifora 2020 — 90 [decanter]
- Vinarija Dragić · Crni Biser 2020 — 90 [decanter]
- Manufaktura Spasić · Rebo 2020 — 90 [decanter]
- šApat Wine Atelier · Magnus 2020 — 90 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2021 — 90 [decanter]
- Vinarija Milićević · Vladavina Icone Merlot 2021 — 90 [decanter]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2021 — 90 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2022 — 90 [decanter]
- Vina Dragić · Nemirac 2022 — 90 [decanter]
- Vinarija Sokolov Zamak · Tamjanika 2022 — 90 [decanter]
- šApat Wine Atelier · šU-šU Blaufrankisch 2022 — 90 [decanter]
- Vinarija Dragić · Carski Drum Manzoni 2023 — 90 [decanter]
- Vinarija Dragić · Crni Biser 2023 — 90 [decanter]
- Vinarija Frug · Sauvignon Blanc 2024 — 90 [decanter]
- Gora · Grašac 2024 — 90 [decanter]
- Nikolich Neuzinsky · Monah Cabernet Franc-Merlot 2020 — 90 [decanter]
- Vinarija Frug · Signum Chardonnay 2022 — 90 [decanter]
- Vinarija Gnezdo · Kadarka 2024 — 90 [decanter]
- Karić Vinarija · Adria 2024 — 90 [decanter]
- Vinarija Gnezdo · Belo 2024 — 90 [decanter]
- Vinarija Frug · Signum Chardonnay 2024 — 90 [decanter]
- Virtus · Marselan 2022 — 90 [decanter]
- šApat Wine Atelier · Nera 2023 — 90 [decanter]
- Vinarija Dragić · Carski Drum Cabernet Franc 2023 — 90 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2023 — 90 [decanter]
- Vinarija Zorča · Velika Dusa Merlot 2019 — 90 [decanter]
- Vinarija Trišić · Trišino 2020 — 90 [decanter]
- Zmajevac · Cuvée 2017 — 90 [decanter]
- Vinarija Dragić · Carski Drum Manzoni 2023 — 90 [decanter]
- Vinarija Frug · Signum Chardonnay 2022 — 90 [decanter]
- Vinarija DeLena · 70/30 Sauvignon Blanc /Semillon 2020 — 90 [Falstaff]
- Vinarija Vimmid · Aglaja Cabernet Sauvignon 2015 — 89 [decanter]
- Virtus · W 2019 — 89 [decanter]
- Stemina · Panta Rei Chardonnay 2018 — 89 [decanter]
- BT Winery · President Gold Vranac 2018 — 89 [decanter]
- Vinarija Dumo · Pinot Noir 2019 — 89 [decanter]
- Podrum Janko · Zavet 2019 — 89 [decanter]
- Virtus · Prokupac 2018 — 89 [decanter]
- Vinarija Fragaria · Fragari Votazi 2019 — 89 [decanter]
- Marselan · Marselan 2019 — 89 [decanter]
- Trilogija Vinery · Pečat Grand Reserve 2017 — 89 [decanter]
- Vina Dragić · Randes 2021 — 89 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2020 — 89 [decanter]
- Vinarija Mrdjanin · Family Edition Probus 2020 — 89 [decanter]
- Vinarija Todorović · Merlot 2020 — 89 [decanter]
- Virtus · Credo 2020 — 89 [decanter]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 89 [decanter]
- Vinarija Sokolov Zamak · Marselan 2021 — 89 [decanter]
- Podrum Pevac · Gušt 2023 — 89 [decanter]
- Karić Vinarija · Adria Belo 2023 — 89 [decanter]
- Vinarija Stanković · Chardonnay 2023 — 89 [decanter]
- Krstašica · Konekicja Sauvignon Blanc 2023 — 89 [decanter]
- Vinarija Frug · Signum Chardonnay 2023 — 89 [decanter]
- Breg · Tamjanika 2024 — 89 [decanter]
- Vinarija Grumen · Morava 2024 — 89 [decanter]
- Virtus · Credo 2024 — 89 [decanter]
- Vinarija Rajić · Tamjanika 2024 — 89 [decanter]
- Vinarija Rajić · Triva Souvignier Gris 2024 — 89 [decanter]
- La Gora · Lupo 2024 — 89 [decanter]
- Vinarija Imperator · Max 2021 — 89 [decanter]
- šApat Wine Atelier · Atila Cabernet Sauvignon 2022 — 89 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2022 — 89 [decanter]
- šApat Wine Atelier · Cuvée 2023 — 89 [decanter]
- Vinarija Frug · Pinot Noir 2023 — 89 [decanter]
- La Gora · Sauvignon Blanc 2025 — 89 [decanter]
- PIK Oplenac · Constanta Muse Sauvignon Blanc 2021 — 89 [Falstaff]
- PIK Oplenac · Constanta Muse Rose 2019 — 89 [Falstaff]
- Podrum Janko · Misija Chardonnay 2013 — 88 [decanter]
- Bacina Vino · Dolina XII  — 88 [decanter]
- Molowinery · Crveni Inat 2010 — 88 [decanter]
- Virtus · Gewürztraminer 2014 — 88 [decanter]
- Vinarija Komuna · Chardonnay 2015 — 88 [decanter]
- Virtus · Marselan 2015 — 88 [decanter]
- Vinarija Lastar · Pinot Noir 2015 — 88 [decanter]
- Vinarija Lastar · Tamjanika 2016 — 88 [decanter]
- Podrum Janko · Bifora 2016 — 88 [decanter]
- Pusula · Sauvignon Blanc 2017 — 88 [decanter]
- Grabak · Prokupac 2017 — 88 [decanter]
- PIK Oplenac · Monarh S 2015 — 88 [decanter]
- Podrum Janko · Zapis Testament 2016 — 88 [decanter]
- Nikad Nije Kasno · Signature 2016 — 88 [decanter]
- Winery Djurdjic · Cabernet Franc 2017 — 88 [decanter]
- Vinarija Dumo · Pinot Noir 2017 — 88 [decanter]
- PIK Oplenac · Monarh Immortal S 2017 — 88 [decanter]
- Vinarija DeLena · 1903 Merlot 2016 — 88 [decanter]
- Vinarija Dragić · Carski Drum Manzoni 2019 — 88 [decanter]
- Probus Vineyards · Traminac 2018 — 88 [decanter]
- Vinarija Eden · Chardonnay 2019 — 88 [decanter]
- Vinarija Aven · Balance 2018 — 88 [decanter]
- Vinarija Frunza Aglaja · Aglaja Sauvignon-Semillon 2020 — 88 [decanter]
- Podrum Janko · Bifora 2017 — 88 [decanter]
- Grabak · Prva Lasta Prokupac 2021 — 88 [decanter]
- BT Winery · Kings Crown 2020 — 88 [decanter]
- Nikolich Neuzinsky Vineyards · The Secret Code of Our Terroir 2020 — 88 [decanter]
- Vinarija Aven · Balance 2019 — 88 [decanter]
- Max-Ex Doo · Rebus Crveni 2019 — 88 [decanter]
- Podrum Petrović · Cabernet Sauvignon 2019 — 88 [decanter]
- Virtus · Marselan 2018 — 88 [decanter]
- Vinarija Komazec · Palava 2021 — 88 [decanter]
- Virtus · Sauvignon Blanc 2021 — 88 [decanter]
- Vinarija Lastar · Chardonnay 2018 — 88 [decanter]
- Nikolich Neuzinsky Vineyards · Santa Maria 2021 — 88 [decanter]
- Vinarija Eden · Genesis 2019 — 88 [decanter]
- Reljić Vinarija · Rebus Crveni 2019 — 88 [decanter]
- Vinarija Zaba · Barrique Merlot 2019 — 88 [decanter]
- Probus Vineyards CCLXXX · Magis 2017 — 88 [decanter]
- Château Prince · Chateau Shiraz 2021 — 88 [decanter]
- Vina Dragić · Aurora 2020 — 88 [decanter]
- Tri Medje I Oblak · Bigfoot Chardonnay 2021 — 88 [decanter]
- Podrum Pevac · Gušt Barrique Chardonnay 2021 — 88 [decanter]
- Podrum Stari Hrast · Sauvignon Blanc 2021 — 88 [decanter]
- Virtus · Marselan 2020 — 88 [decanter]
- Krstašica Doo · Konekcija Merlot 2020 — 88 [decanter]
- Krstašica · Konekcija Merlot 2021 — 88 [decanter]
- BT Winery · Mister Marselan 2022 — 88 [decanter]
- Virtus · Credo Beli 2022 — 88 [decanter]
- šApat Wine Atelier · Chardonnay 2022 — 88 [decanter]
- Winery Djurdjic · Grašac Beli 2022 — 88 [decanter]
- Karić Vinarija · Adria Belo 2022 — 88 [decanter]
- Grabak · Modrovrana Cabernet Sauvignon 2018 — 88 [decanter]
- Vina Dragić · Kibic 2022 — 88 [decanter]
- Vinarija Frug · Chardonnay 2023 — 88 [decanter]
- Breg · Grašac 2024 — 88 [decanter]
- Gora · White Blend 2024 — 88 [decanter]
- Vinarija Mira · La Baba Morava 2024 — 88 [decanter]
- Vinarija Rajić · Prokupac 2024 — 88 [decanter]
- šApat Wine Atelier · Atila Chardonnay 2024 — 88 [decanter]
- šApat Wine Atelier · Chardonnay 2024 — 88 [decanter]
- La Gora · Bello 2024 — 88 [decanter]
- Vinarija Imperator · Gratianus Traminac 2021 — 88 [decanter]
- Vinarija Trišić · Dimasid 2021 — 88 [decanter]
- Traško Vinarija · Fucking Fabulous Edición Limitada 2021 — 88 [decanter]
- Château Prince · Gospodar 2021 — 88 [decanter]
- Traško Vinarija · Fabulous Cabernet Sauvignon 2022 — 88 [decanter]
- La Gora · Chardonnay 2025 — 88 [decanter]
- Breg · Grašac 2025 — 88 [decanter]
- Vinarija Imperator · VAL Rajnski Rizling 2022 — 88 [decanter]
- Grabak · Vivak Prokupac 2019 — 88 [decanter]
- Vinarija Zorča · Mali Ratnik Cabernet Sauvignon 2020 — 88 [decanter]
- The Sparkling Winery · The Extra Brut 2023 — 88 [decanter]
- Virtus · Marselan 2016 — 88 [decanter]
- Vinarija Unikat · Vranac 2019 — 88 [decanter]
- Virtus · Prokupac 2019 — 88 [decanter]
- Vinarija Sokolov Zamak · Marselan 2021 — 88 [decanter]
- BT Winery · Mister Marselan 2022 — 88 [decanter]
- Vinarija Sokolov Zamak · Chardonnay 2023 — 88 [decanter]
- Podrum Džervin 1927 · Trifun Grand Cabernet Sauvignon 2019 — 88 [decanter]
- Podrum Janko · Misija 2016 — 87 [decanter]
- Atos-Fructum · The 2015 — 87 [decanter]
- Probus Vineyards · Magis 2017 — 87 [decanter]
- Vinarija Lastar · Pinot Noir 2016 — 87 [decanter]
- Grabak · Siva Vrana 2017 — 87 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2017 — 87 [decanter]
- Virtus · W Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Noir 2017 — 87 [decanter]
- Vinarija Janucic · Vulkan Merlot 2017 — 87 [decanter]
- Zmajevac · Cuvée 2017 — 87 [decanter]
- Zmajevac · Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2019 — 87 [decanter]
- PIK Oplenac · Monarh Immortal Cuvée 2015 — 87 [decanter]
- Vinogradi Veličković Vinarija · Sauvignon Blanc 2015 — 87 [decanter]
- Vinarija Aven · Merlot 2018 — 87 [decanter]
- Zmajevac · Chardonnay 2019 — 87 [decanter]
- Virtus · Marselan 2017 — 87 [decanter]
- Vinarija Lastar · Merlot-Cabernet Franc 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2020 — 87 [decanter]
- BT Winery · King Supreme Marselan 2020 — 87 [decanter]
- Virtus · Gewurztraminer 2021 — 87 [decanter]
- Virtus · Prokupac 2018 — 87 [decanter]
- Podrum Bačina · Dolina 2018 — 87 [decanter]
- Vinarija Eden · Cabernet Franc 2019 — 87 [decanter]
- Podrum Pevac · Zagrljaj 2019 — 87 [decanter]
- Virtus · Prokupac 2019 — 87 [decanter]
- Probus Vineyards CCLXXX · Belim 2017 — 87 [decanter]
- Vinarija Gamanović · Cabernet Sauvignon 2020 — 87 [decanter]
- Virtus · Pinot Grigio 2022 — 87 [decanter]
- Vinarija Dragić · Carski Drum Rajnski Rizling 2020 — 87 [decanter]
- Vinarija Manastira Studenica · 1186 Prokupac 2020 — 87 [decanter]
- Vinarija Fragaria · Votazi 2020 — 87 [decanter]
- Vinarija Bora · Frenk 2020 — 87 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2021 — 87 [decanter]
- Podrum Pevac · Prokupac 2021 — 87 [decanter]
- Tref Line · Pirg Sauvignon Blanc 2021 — 87 [decanter]
- Vinarija Fragaria · Jagoda 2022 — 87 [decanter]
- Vinarija Manastira Studenica · Tamjanika Bela Reč 2022 — 87 [decanter]
- Vinarija Dragić · Carski Drum Chardonnay 2022 — 87 [decanter]
- Vinarija Stanković · Chardonnay 2022 — 87 [decanter]
- Vina Dragić · Randes 2022 — 87 [decanter]
- Vinarija Sokolov Zamak · Chardonnay 2023 — 87 [decanter]
- Podrum Džervin 1927 · Trifun Grand Cabernet Sauvignon 2019 — 87 [decanter]
- Podrum Janko · Zlatno Runo Cabernet Sauvignon 2019 — 87 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2019 — 87 [decanter]
- šApat Wine Atelier · Pi' Crveno Premium 2019 — 87 [decanter]
- Vinarija Dragić · Carski Drum Manzoni 2024 — 87 [decanter]
- Breg · Sila 2024 — 87 [decanter]
- Vinarija Frug · Grašac 2024 — 87 [decanter]
- Virtus · Prokupac 2020 — 87 [decanter]
- Pr Anjino Vino · Suton Merlot 2022 — 87 [decanter]
- La Grande Bellezza · Blanc De Blancs Extra Brut 2021 — 87 [decanter]
- Château Prince · Charm Chardonnay-Morava 2024 — 87 [decanter]
- Vinarija Gnezdo · Krokan Muskat 2024 — 87 [decanter]
- Natural Grape Concept · Tamjanika 2024 — 87 [decanter]
- Vinarija Fleur D'Oranger · Krokan Muskat 2024 — 87 [decanter]
- Vinarija Imperator · Cargraš 2024 — 87 [decanter]
- Virtus · Prokupac 2021 — 87 [decanter]
- Vinarija Eden · Genesis 2021 — 87 [decanter]
- Vinarija Frug · Signum Cuvée 2022 — 87 [decanter]
- Mister · Marselan 2022 — 87 [decanter]
- Virtus · Prokupac 2022 — 87 [decanter]
- Vinarija Rajić · Monika 2023 — 87 [decanter]
- Vinarija Lastar · Sofijin Izbor Pinot Noir 2023 — 87 [decanter]
- Natural Grape Concept · Prokupac 2023 — 87 [decanter]
- Vinarija Orlić · MMXXIII Shiraz 2023 — 87 [decanter]
- The Sparkling Winery · The Blanc de Noirs 2023 — 87 [decanter]
- Vinarija Imperator · Frušet Rosé Brut 2022 — 87 [decanter]
- Vinarija Dragić · Carski Drum Rajnski Rizling 2020 — 87 [decanter]
- Grabak · Prokupac 2020 — 87 [decanter]
- Vinarija Dragić · Carski Drum Manzoni 2024 — 87 [decanter]
- Vinarija Dragić · Carski Drum Sauvignon Blanc 2024 — 87 [decanter]
- Vinarija Frug · Signum Syrah 2022 — 87 [decanter]
- Mcculloch Wines · Mcc Traminac 2013 — 86 [decanter]
- Vinarija Lastar · Chardonnay 2015 — 86 [decanter]
- Virtus · Credo Beli 2015 — 86 [decanter]
- Podrum Janko · Smederevka 2017 — 86 [decanter]
- Virtus W · Gewürztraminer 2017 — 86 [decanter]
- Vinarija Lastar · Chardonnay 2016 — 86 [decanter]
- Podrum Janko · Vrtlog 2016 — 86 [decanter]
- Grabak · Modrovrana 2015 — 86 [decanter]
- Virtus W · Pinot Noir 2015 — 86 [decanter]
- PIK Oplenac · Villa Muscat Ottonel 2015 — 86 [decanter]
- Vinarija Komuna · Chardonnay 2017 — 86 [decanter]
- Pusula · Cabernet 2015 — 86 [decanter]
- Vinarija Vimmid · Aglaja Dantelle Cabernet Sauvignon 2016 — 86 [decanter]
- Nikad Nije Kasno · Simfonija 2017 — 86 [decanter]
- Vista Hills Plus · Premium 2019 — 86 [decanter]
- Vinarija Dragić · Carski Drum Sauvignon Blanc 2019 — 86 [decanter]
- Virtus · Sauvignon Blanc 2019 — 86 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2018 — 86 [decanter]
- Belina · Belina 2019 — 86 [decanter]
- Rubinov · Prokupac 2018 — 86 [decanter]
- BT Winery · King's Crown 2018 — 86 [decanter]
- Prokupac · Prokupac 2018 — 86 [decanter]
- Pusula · Cabernet 2017 — 86 [decanter]
- Grabak · Modrovrana 2017 — 86 [decanter]
- Zmajevac · Cuvée Reserve 2017 — 86 [decanter]
- Vinarija Komazec · Rose 2021 — 86 [decanter]
- Vinarija Lastar · Pinot Noir 2019 — 86 [decanter]
- Grabak · Prokupac 2019 — 86 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2020 — 86 [decanter]
- Vinarija Đurđevića Legat · Otisak 2020 — 86 [decanter]
- Tri Medje I Oblak · Vagabundo Cabernet Sauvignon 2020 — 86 [decanter]
- Vina Dragić · Kibic 2021 — 86 [decanter]
- Vinarija Podrum Danguba · Ponovo Naše Tamjanika 2021 — 86 [decanter]
- Vinarija Gamanović · Bela Tamjanika 2021 — 86 [decanter]
- Vinarija Dragić · Carski Drum Cabernet Franc 2020 — 86 [decanter]
- Manufaktura Spasić · Krivac 2020 — 86 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2021 — 86 [decanter]
- Salaš Gnezdo Doo Bečej · Genzdo Muskat Krokan 2022 — 86 [decanter]
- Krstašica · Konekicja Chardonnay 2023 — 86 [decanter]
- Vinarija Dragić · Carski Drum Sauvignon Blanc 2024 — 86 [decanter]
- Château Prince · Premium Shiraz 2021 — 86 [decanter]
- Vinarija Dragić · Crni Biser 2024 — 86 [decanter]
- Vinarija Milićević · Vladavina Riesling-Grašac 2024 — 86 [decanter]
- Tri Medje I Oblak · Vagabundo Sauvignon Blanc 2025 — 86 [decanter]
- Gardijan · Stigma Chardonnay 2023 — 86 [decanter]
- Virtus · Credo 2013 — 86 [decanter]
- Molowinery · Crveni Inat 2010 — 86 [decanter]
- Virtus · Credo 2017 — 86 [decanter]
