# Оценки критиков

Вторая дорожка, независимая от Vivino. Здесь стобалльная шкала и оценка
эксперта, а не средняя по толпе.

**Почему отдельно, а не вместе.** У Vivino пятибалльная оценка покупателей,
и её вес определяется числом отметок. У критика вес определяется тем, что он
критик; порога по числу отзывов здесь нет и быть не может. Это две разные
величины, и в одно число они не складываются. Если рейтинги пойдут в книгу,
показывать их надо порознь и подписывать, что именно показано.

## Две вещи, а не одна

**Оценки** — балл по стобалльной шкале, 2099 записей.

**Награды** — место в категории или медаль, 2937 записей. У них нет шкалы,
зато есть год и категория. Переводить «лучшее белое из местных сортов
2025 года» в число нельзя, поэтому и таблицы разные.

Держится это на двух конкурсах. Decanter — база наград открылась целиком,
девятнадцать лет, 2008–2026, 1096 сербских медалей, и у 941 ещё балл.
Balkans International Wine Competition — софийский конкурс, для Сербии
ближайший крупный: 1072 медали, 33 трофея и 421 балл за тринадцать лет.

## Источники

**Falstaff** — 144 оценки, сербский список целиком. Австрийский гид ведёт
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

**Gilbert & Gaillard** — французский гид, дегустация вслепую, стобалльная
шкала. Сербских вин у него пять, и это единственные их оценки: ни Decanter,
ни Falstaff этих вин не судили. Plavinac взял 88 за тамјанику и 88 за
совиньон 2025 года — то есть Подунавље держится уже не на одной бронзе.
Ещё 93 у Фрушкогорског за «Три сунца» 2015 и 88 и 90 у Рубина за «Аманте
Кармен» и «Аманте Аурору» 2019 года.

Список собирается Livewire, то есть приходит отдельным запросом; браузер
для этого не нужен, `vzjat-gilbert-gaillard.py` повторяет запрос сам.
В поле хозяйства гид местами пишет марку: «Amante» — линейка Рубина,
«Tri SuncA» — линейка Фрушкогорског; сведено с доказательством.

**Balkans International Wine Competition** — софийский конкурс, с 2013 года.
Для Сербии он ближе любого другого крупного: 1085 сербских вин за 2014
и 2017–2026 годы, у 422 есть балл, у 1004 — медаль. Это больше, чем дал
Decanter, и в иные годы под полтораста сербских вин зараз.

Таблицы у него простые, без сценариев, но раскладка гуляет от года к году:
колонок от пяти до восьми, цвет стоит то до страны, то после имени вина,
балл и медаль местами меняются, а до 2021 года балла не было вовсе и медаль
стояла заголовком раздела. Поэтому `vzjat-biwc.py` читает ячейки не по
местам, а по виду. Четыре вина в источнике поданы дважды с разным баллом —
расхождения выписаны в `biwc-zapisi.json`, в таблицу идёт больший балл.

Конкурс дал и одиннадцать хозяйств, которых не было нигде: Vinarija VRT
из Риђице, Lutak, Vinarija Teodos, Vinarija Tasa, Vinarija Tri Tachke,
Rajković wine office, Vinarija Slatina, Jelenac, Damalis, Anja Džipković,
Vinogradi i vinarija Miletić.

**AWC Vienna** — крупнейший конкурс, признанный OIV, около десяти тысяч
вин в год. Сербских 573 за 2014–2026, у всех и балл (с десятой долей),
и медаль. База
живёт отдельно от сайта конкурса; фильтра по стране нет, а выдача обрезана
сотней записей, и по категориям листается только текущий год — за прошлые
отдаётся общий список, полсотни-сотня лучших. Что взято, то верхушка,
и это надо помнить.

**Berliner, Asia и Portugal Wine Trophy** — три конкурса одного устроителя
с общей базой: 21 сербское вино за 2019–2026, почти всё Тодоровић. Балла
не публикуют.

**International Wine Challenge** — лондонский конкурс, судят вслепую.
Сербия у него есть с 2009 по 2022 год: 63 отмеченных вина — 11 серебра,
21 бронза, 31 «отмечено». Балла IWC не ставит, поэтому записи идут
в награды. Больше всего у Александровића (18) и Ластара (16), дальше
Алексић, PIK Опленац, Рубин, Doja, Matalj, Вино Будимир, Звонко Богдан.
С 2023 года сербских вин на конкурсе нет.

**Concours Mondial de Bruxelles** — шесть сербских медалей за все годы:
большое золото 2013 Рубину за «Terra Lazarica Cabernet Sauvignon Barrique»,
золото 2019 «Nikad Nije Kasno», серебро 2019 Рубину, золото и серебро 2023
Подруму Певац, золото 2024 Ралевићу.

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

**Подунавье почти пусто:** бронза DWWA 2026 у Plavinac за смедеревку
2025 года, 88 баллов, и два восьмидесятивосьмибалльных вина того же
Plavinac у Gilbert & Gaillard. На Vivino район не представлен вовсе.
Рядом стоит золото Decanter 2025 у Virtus, но Decanter относит его к району
Млава; входит ли Млава в главу «Подунавье», решать автору.

**Метохия — только награды**, баллов нет: у Lakićević три места в годовом
тесте vino.rs (2023, 2024, 2025) и ни одной стобалльной оценки. На Vivino
хозяйство есть — восемь вин, все около 4,1–4,2.

**Юго-восток держится на одном хозяйстве.** Тридцать восемь оценок в районе,
и все до одной — Aleksić. У Džervin и Jović нет ни балла, ни награды.

**Глава книги известна у 61 хозяйства из 458**, а настоящий рејон —
у 297. Остальных Vivino сваливает в «Central Serbia» и «Wine of Serbia»,
и Винарски регистар не узнаёт по имени. Разбор — в `po-rejonima.md`.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-kritikov.py --otchet

---

<!-- Собрано скриптом svesti-kritikov.py. Руками не править. -->

## Где две дорожки пересекаются

Вин с оценкой Vivino — 1180, с оценкой критиков — 866, **с обеими — 287**.

| Район | Vivino | Критики | И то и другое |
|---|---|---|---|
| Фрушка гора | 228 | 164 | 68 |
| Суботичско-Хоргошская пешчара | 76 | 26 | 17 |
| Банат | 37 | 11 | 6 |
| Шумадия | 93 | 93 | 33 |
| Три Моравы и Жупа | 126 | 73 | 23 |
| Неготинска Крайина | 27 | 37 | 14 |
| Топлица | 20 | 14 | 9 |
| Юго-восток | 31 | 45 | 12 |
| Подунавье и Белградский район | 0 | 5 | 0 |
| Косово и Метохия | 8 | 9 | 1 |

## Фрушка гора

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Erdevik · Omnibus Lector Chardonnay | 2015 | 97 | decanter |
| Vinčić · Grašac | 2020 | 97 | decanter |
| Deurić · La Rem Chardonnay | 2023 | 97 | decanter |
| Bikicki · Uncensored | 2018 | 96 | decanter |
| Vinčić · Grašac Grand Fru | 2020 | 95 | Falstaff |
| Chichateau · Chi Chardonnay | 2018 | 95 | Falstaff |
| Veritas Ćuković · Momentum Cabernet Sauvignon | 2017 | 95 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2017 | 95 | decanter |
| Šapat · Atila Chardonnay | 2022 | 95 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2019 | 95 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2017 | 95 | decanter |
| Veritas Ćuković · Momentum | 2017 | 95 | decanter |
| Vinčić · Grasac | 2020 | 95 | biwc |
| Vinum · Grasac beli | 2019 | 95 | biwc |
| Šapat · Atila Chardonnay | 2023 | 95 | biwc |
| Vinčić · Grand V | 2023 | 95 | biwc |
| Molovin · Vista Hill Red Reserve | 2010 | 94 | decanter |
| Erdevik · Trianon | 2018 | 94 | decanter |
| Bikicki · Uncensored | 2020 | 94 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2017 | 94 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2019 | 94 | decanter |
| Deurić · La Rem Chardonnay | 2023 | 94 | decanter |
| Erdevik · Stiflers Mom Shiraz | 2020 | 94 | decanter |
| Šapat · Cuvée | 2022 | 94 | decanter |
| Vinum · Grašac 26A | 2021 | 94 | biwc |
| Vinum · Grasac 26a | 2019 | 94 | biwc |
| Vinum · Chardonnay | 2021 | 94 | biwc |
| Vinum · Chardonnay | 2019 | 94 | biwc |
| Verkat · Malvazija | 2023 | 94 | biwc |
| Vinčić · Grand Fru | 2020 | 94 | biwc |
| Šapat · Atila Plavi | 2024 | 94 | biwc |
| Vinum · Grašac 26a | 2019 | 93 | Falstaff |
| Erdevik · Grand Trianon | 2017 | 93 | Falstaff |
| Molovin · Inat Frankovka | 2019 | 93 | Falstaff |
| Bjelica · Graffiti | 2018 | 93 | Falstaff |
| Erdevik · Grand Trianon | 2016 | 93 | Falstaff |
| Veritas Ćuković · Momentum Cabernet Sauvignon | 2017 | 93 | decanter |
| Deurić · Severna Morava | 2020 | 93 | decanter |
| Deurić · Severna Morava | 2021 | 93 | decanter |
| Šapat · Reserve Cabernet Sauvignon | 2020 | 93 | decanter |
| Erdevik · Stiflers Mom Shiraz | 2019 | 93 | decanter |
| Deurić · Aksiom Crveni | 2019 | 93 | decanter |
| Deurić · Aksiom | 2021 | 93 | decanter |
| Deurić · Aksiom Beli | 2019 | 92 | Falstaff |
| Erdevik · Grand Trianon Deux Mers | 2016 | 92 | Falstaff |
| Bikicki · Sfera Noir (натуральное) | 2021 | 92 | Falstaff |
| Deurić · The Brut | 2018 | 92 | Falstaff |
| Vinum · Bermet Crveni | 2023 | 92 | awc-vienna |
| Deurić · Princeps Brut Nature | 2015 | 92 | decanter |
| Bikicki · S/O | 2017 | 92 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2017 | 92 | decanter |
| Erdevik · Trianon | 2018 | 92 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2021 | 92 | decanter |
| Chichateau · Chi Chardonnay | 2024 | 92 | decanter |
| Chichateau · Fabula Lagum | 2021 | 92 | decanter |
| Šapat · Atila Cabernet Sauvignon | 2023 | 92 | decanter |
| Deurić · Aksiom | 2022 | 92 | decanter |
| Trivanović · Ultimo S | 2020 | 92 | decanter |
| Kovačević · R Edition Brut | 2012 | 92 | decanter |
| Vinarija Šijački · Superćelijski Grašac | 2023 | 92 | biwc |
| Erdevik · Grand Trianon | — | 91 | Wine-Searcher |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | — | 91 | Wine-Searcher |
| Molovin · Inat Traminac | 2020 | 91 | Falstaff |
| Deurić · Classic Chardonnay | 2018 | 91 | decanter |
| Deurić · Aksiom | 2016 | 91 | decanter |
| Deurić · Classic Chardonnay | 2021 | 91 | decanter |
| Verkat · Barrique Malvazija | 2021 | 91 | decanter |
| Verkat · Grašac Beli 4.0 | 2021 | 91 | decanter |
| Veritas Ćuković · Momentum | 2021 | 91 | decanter |
| Šapat · Bianca Moscato Giallo | 2023 | 91 | decanter |
| Chichateau · Blake Sauvignon Blanc | 2023 | 91 | decanter |
| Deurić · La Rem Morava Amf | 2023 | 91 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2021 | 91 | decanter |
| Vinčić · Grand Fru | 2020 | 91 | decanter |
| Bikicki · Uncensored | 2022 | 91 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2024 | 91 | decanter |
| Kovačević · Rizling | 2021 | 91 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2023 | 91 | decanter |
| Verkat · Roze | 2022 | 91 | biwc |
| Kiš · Verus Grasac Beli | 2023 | 91 | biwc |
| Kiš · Biser crni | — | 91 | biwc |
| Kovačević · Aurelius Edicija S | 2019 | 90 | Falstaff |
| Vinum · Grašac Beli | 2025 | 90 | awc-vienna |
| Vinum · Frankovka | 2022 | 90 | awc-vienna |
| Molovin · Plavi Princip | 2013 | 90 | decanter |
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
| Erdevik · Omnibus Lector Chardonnay | 2019 | 90 | decanter |
| Deurić · Classic Chardonnay | 2019 | 90 | decanter |
| Deurić · Aksiom | 2017 | 90 | decanter |
| Erdevik · Stifles Mom | 2017 | 90 | decanter |
| Deurić · Aksiom Beli | 2019 | 90 | decanter |
| Erdevik · Marlon Delon | 2017 | 90 | decanter |
| Šapat · Magnus | 2020 | 90 | decanter |
| Veritas Ćuković · Monte Karlovci Merlot | 2021 | 90 | decanter |
| Veritas Ćuković · ćUk | 2021 | 90 | decanter |
| Erdevik · Ex Cathedra Sauvignon Blanc | 2021 | 90 | decanter |
| Šapat · šU-šU Blaufrankisch | 2022 | 90 | decanter |
| Deurić · Severna Morava | 2023 | 90 | decanter |
| Vinčić · Grand Fru | 2023 | 90 | decanter |
| Deurić · Gorska Tamjanika | 2024 | 90 | decanter |
| Chichateau · Fabula Lagum Cabernet Sauvignon-Cabernet Franc-Merlot | 2019 | 90 | decanter |
| Deurić · Aksiom | 2019 | 90 | decanter |
| Erdevik · Grand Trianon | 2020 | 90 | decanter |
| Šapat · Terol Teroldego | 2022 | 90 | decanter |
| Veritas Ćuković · Monte Karlovci | 2022 | 90 | decanter |
| Šapat · Nera | 2023 | 90 | decanter |
| Veritas Ćuković · Momentum Mali | 2023 | 90 | decanter |
| Kovačević · Chardonnay | 2025 | 90 | decanter |
| Erdevik · Stifler's Mom Shiraz | 2020 | 90 | decanter |
| Veritas Ćuković · Bela Harmonija | 2021 | 90 | biwc |
| Verkat · Malvazija | 2022 | 90 | biwc |
| Vinarija Djurdjic · Grasac Djurdjic | 2022 | 90 | biwc |
| Vinarija Šijački · Seduša | 2022 | 90 | biwc |
| Trivanović · Ultimo S | 2020 | 90 | biwc |
| Trivanović · Toca | 2018 | 90 | biwc |
| Šapat · Cuvee | 2023 | 90 | biwc |
| Erdevik · Trianon | — | 89 | Wine-Searcher |
| Vinum · Chardonnay | 2022 | 89 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2015 | 89 | awc-vienna |
| Kovačević · Aurelius | 2012 | 89 | decanter |
| Deurić · Talas Beli | 2015 | 89 | decanter |
| Deurić · The Brut | 2015 | 89 | decanter |
| Bikicki · Uncensored | 2017 | 89 | decanter |
| Belo Brdo · Black Label Limited Edition Chardonnay | 2020 | 89 | decanter |
| Erdevik · Grand Trianon | 2016 | 89 | decanter |
| Šapat · Atila Chardonnay | 2023 | 89 | decanter |
| Šapat · Chardonnay | 2023 | 89 | decanter |
| Deurić · Pinot Noir | 2018 | 89 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2021 | 89 | decanter |
| Šapat · Atila Cabernet Sauvignon | 2022 | 89 | decanter |
| Deurić · Sauvignon Blanc | 2024 | 89 | decanter |
| Veritas Ćuković · Ćuk | 2021 | 89 | decanter |
| Šapat · Atila Cabernet Sauvignon | 2022 | 89 | decanter |
| Šapat · Cuvée | 2023 | 89 | decanter |
| Erdevik · Grand Trianon | 2019 | 89 | decanter |
| Molovin · Inat Traminac | 2021 | 89 | biwc |
| Veritas Ćuković · Momentum Mali | 2020 | 89 | biwc |
| Vinum · Chardonnay | 2021 | 89 | biwc |
| Vinum · Grasac 26a | 2020 | 89 | biwc |
| Vinum · Chardonnay | 2020 | 89 | biwc |
| Vinum · Grasac beli | 2020 | 89 | biwc |
| Vinum · Grasac beli | 2021 | 89 | biwc |
| Vinum · Grasac beli | 2022 | 89 | biwc |
| Vinum · white | 2023 | 89 | biwc |
| Vinum · Frankovka | 2022 | 89 | biwc |
| Vinum · Mustra | 2023 | 89 | biwc |
| Vinarija Djurdjic · Probus Djurdjic | 2020 | 89 | biwc |
| Kiš · Verus GT | 2023 | 89 | biwc |
| Kiš · Kisov Grasac beli | 2024 | 89 | biwc |
| Kiš · Verus GT | 2024 | 89 | biwc |
| Šapat · Atila Cabernet sauvignon | 2023 | 89 | biwc |
| Šapat · Atila Sauvignon blanc | 2024 | 89 | biwc |
| Belo Brdo · Chardonnay | 2015 | 88 | awc-vienna |
| Erdevik · Omnibus Lector Chardonnay | 2015 | 88 | decanter |
| Molovin · Crveni Inat | 2010 | 88 | decanter |
| Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah | 2015 | 88 | decanter |
| Kovačević · R Edition Aurelius | 2012 | 88 | decanter |
| Kiš · Misterija Kišova | 2011 | 88 | decanter |
| Vinarija Djurdjic · Cabernet Franc | 2017 | 88 | decanter |
| Erdevik · Roza Nostra | 2019 | 88 | decanter |
| Kiš · Kišov Grašac Beli | 2019 | 88 | decanter |
| Deurić · Sauvignon Blanc | 2018 | 88 | decanter |
| Kovačević · Fresco Bianco Brut | 2019 | 88 | decanter |
| Deurić · Princeps Probus | 2016 | 88 | decanter |
| Bikicki · Makana | 2016 | 88 | decanter |
| Erdevik · Geronimo | 2020 | 88 | decanter |
| Deurić · Classic Chardonnay | 2020 | 88 | decanter |
| Belo Brdo · Belo Brdo | 2018 | 88 | decanter |
| Erdevik · Omnibus Lector Chardonnay | 2016 | 88 | decanter |
| Deurić · Probus 276 | 2018 | 88 | decanter |
| Deurić · Princeps Chardonnay | 2021 | 88 | decanter |
| Deurić · Severna Morava | 2020 | 88 | decanter |
| Vinčić · Grand Fru | 2020 | 88 | decanter |
| Deurić · The Brut | 2019 | 88 | decanter |
| Deurić · Pinot Noir | 2020 | 88 | decanter |
| Šapat · Chardonnay | 2022 | 88 | decanter |
| Veritas Ćuković · Bela Harmonija | 2022 | 88 | decanter |
| Vinarija Djurdjic · Grašac Beli | 2022 | 88 | decanter |
| Erdevik · Trianon Pinot Blanc-Pinot Grigio-Sauvignon Blanc | 2023 | 88 | decanter |
| Veritas Ćuković · Cuk Cuvée | 2021 | 88 | decanter |
| Veritas Ćuković · Momentum | 2021 | 88 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2020 | 88 | decanter |
| Bikicki · Skins | 2022 | 88 | decanter |
| Deurić · Aksiom | 2021 | 88 | decanter |
| Chichateau · Chardonnay | 2021 | 88 | decanter |
| Šapat · Atila Chardonnay | 2024 | 88 | decanter |
| Šapat · Chardonnay | 2024 | 88 | decanter |
| Verkat · Grašac Beli | 2024 | 88 | decanter |
| Deurić · Pinot Noir | 2021 | 88 | decanter |
| Deurić · Probus 276 | 2023 | 88 | decanter |
| Chichateau · Blake Sauvignon Blanc | 2023 | 88 | decanter |
| Deurić · La Rem Morava Amf | 2023 | 88 | decanter |
| Veritas Ćuković · Barrique Chardonay | 2023 | 88 | decanter |
| Vinum · Grasac 26a | 2022 | 88 | biwc |
| Kiš · Biser Bermet crveni | 2024 | 88 | biwc |
| Šapat · Chardonnay | 2023 | 88 | biwc |
| Vinčić · Grand Fru | 2023 | 88 | biwc |
| Kiš · Kisov Bermet | 2025 | 88 | biwc |
| Kiš · Kisov Grasac beli | 2025 | 88 | biwc |
| Kiš · Misterija | 2025 | 88 | biwc |
| Vinum · Grašac 26A | 2023 | 87 | awc-vienna |
| Deurić · Enigma | 2015 | 87 | decanter |
| Deurić · Urban Rose | 2015 | 87 | decanter |
| Deurić · Pinot Noir | 2015 | 87 | decanter |
| Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah | 2016 | 87 | decanter |
| Erdevik · Grand Trianon | 2016 | 87 | decanter |
| Deurić · Pinot Noir | 2017 | 87 | decanter |
| Belo Brdo · Black Label Cabernet Sauvignon | 2018 | 87 | decanter |
| Deurić · Probus Princeps | 2016 | 87 | decanter |
| Bikicki · S/O | 2020 | 87 | decanter |
| Vinčić · Grand Fru | 2020 | 87 | decanter |
| Erdevik · Geronimo | 2021 | 87 | decanter |
| Šapat · Pi'Crveno Premium | 2019 | 87 | decanter |
| Bikicki · Cu | 2022 | 87 | decanter |
| Molovin · Inat Frankovka | 2020 | 87 | biwc |
| Vinum · Grasac 26a | 2021 | 87 | biwc |
| Vinum · Chardonnay | 2022 | 87 | biwc |
| Vinum · Grasac beli | 2018 | 87 | biwc |
| Vinum · Dina | 2022 | 87 | biwc |
| Kiš · Verus Chardonnay | 2023 | 87 | biwc |
| Vinarija Šijački · Seduša | 2021 | 87 | biwc |
| Šapat · Atila Caberne | 2022 | 87 | biwc |
| Trivanović · Optimus | 2024 | 87 | biwc |
| Šapat · Atila Chardonnay | 2024 | 87 | biwc |
| Kovačević · Edicija S Aurelius | — | 86 | Wine-Searcher |
| Molovin · Crveni Inat | 2010 | 86 | decanter |
| Deurić · Princeps Probus | 2016 | 86 | decanter |
| Bikicki · Cu | 2018 | 86 | decanter |
| Kovačević · Aurelius S Edicija | 2017 | 86 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2016 | 86 | decanter |
| Molovin · Inat Frankovka | 2019 | 86 | decanter |
| Molovin · Inat Limited Edition Rajnski Rizling | 2021 | 86 | decanter |
| Veritas Ćuković · Cuk | 2020 | 86 | biwc |
| Trivanović · Reserve Shiraz | 2018 | 86 | biwc |
| Vinum · Bermet Cerveni | 2023 | 86 | biwc |
| Verkat · Frankovka | 2022 | 86 | biwc |
| Vinarija Djurdjic · Neoplanta Djurdjic | 2022 | 86 | biwc |
| Kiš · Verus Mister & Ja | 2023 | 86 | biwc |
| Molovin · Inat Rajnski Risling | 2021 | 86 | biwc |
| Molovin · Inat | 2012 | 85 | decanter |
| Kiš · Misterija | 2011 | 85 | decanter |
| Kovačević · Chardonnay | 2017 | 85 | decanter |
| Deurić · Pinot noir | 2016 | 85 | decanter |
| Molovin · Graševina | 2012 | 85 | decanter |
| Deurić · Probus 276 | 2017 | 85 | decanter |
| Deurić · Pinot Noir | 2017 | 85 | decanter |
| Molovin · Vista Hill Selection | 2017 | 85 | decanter |
| Deurić · Aksiom | 2016 | 85 | decanter |
| Deurić · Princeps Pinot Noir | 2016 | 85 | decanter |
| Deurić · Princeps Merlot | 2016 | 85 | decanter |
| Deurić · Probus 276 | 2018 | 85 | decanter |
| Deurić · Barrique Sauvignon Blanc | 2017 | 85 | decanter |
| Mačkov podrum · Camerlot | 2021 | 85 | biwc |
| Veritas Ćuković · Domina Rose | 2021 | 85 | biwc |
| Kiš · Kisova Misterija, black label | 2024 | 85 | biwc |
| Šapat · Šu-Šu | 2024 | 85 | biwc |
| Kiš · Misterija polusuva | 2025 | 85 | biwc |
| Šapat · Bianca | 2025 | 85 | biwc |
| Kovačević · Sauvignon | 2012 | 84 | decanter |
| Deurić · Gewürztraminer | 2015 | 84 | decanter |
| Deurić · Avangarda | 2015 | 84 | decanter |
| Deurić · Merlot | 2015 | 84 | decanter |
| Kovačević · S Edition Aurelius | 2014 | 84 | decanter |
| Deurić · Chardonnay | 2016 | 84 | decanter |
| Kovačević · S Edition Sauvignon | 2016 | 84 | decanter |
| Kovačević · Brut | 2010 | 84 | decanter |
| Deurić · Aksiom | 2017 | 84 | decanter |
| Kiš · Kišov Rosé | 2019 | 84 | decanter |
| Veritas Ćuković · Monte Carlovci | 2020 | 84 | biwc |
| Vinčić · Vincic | 2017 | 84 | biwc |
| Vinum · Mustra | 2022 | 84 | biwc |
| Šapat · Nera | 2022 | 84 | biwc |
| Deurić · Chardonnay | 2015 | 83 | decanter |
| Erdevik · Roza Nostra | 2015 | 83 | decanter |
| Kovačević · S Edition Chardonnay | 2015 | 83 | decanter |
| Vinarija Djurdjic · Simonida Mlada | — | 83 | biwc |
| Vinarija Djurdjic · Cabernet Franc Djurdjic | 2021 | 83 | biwc |
| Kiš · Misterija Kišova | 2024 | 83 | biwc |
| Kiš · Biser Bermet beli | 2024 | 83 | biwc |
| Verkat · Grasac Beli | 2023 | 82 | biwc |
| Kiš · Kišov Bermet Belo | 2024 | 82 | biwc |
| Mačkov podrum · Sauvignon blanc | 2024 | 82 | biwc |
| Šapat · Cuvee | 2022 | 82 | biwc |
| Trivanović · Trigio Blanc | 2024 | 82 | biwc |
| Vinarija Djurdjic · Neoplanta | — | 81 | biwc |
| Trivanović · Reserve Cabernet Sauvignon | 2017 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Šapat · Atila Chardonnay 2024 | 
| 2026 | бронза | bronza | Deurić · Sauvignon Blanc 2024 | 
| 2026 | бронза | bronza | Šapat · Chardonnay 2024 | 
| 2026 | бронза | bronza | Verkat · Grašac Beli 2024 | 
| 2026 | бронза | bronza | Veritas Ćuković · Ćuk 2021 | 
| 2026 | бронза | bronza | Deurić · Pinot Noir 2021 | 
| 2026 | бронза | bronza | Šapat · Atila Cabernet Sauvignon 2022 | 
| 2026 | бронза | bronza | Deurić · Probus 276 2023 | 
| 2026 | бронза | bronza | Šapat · Cuvée 2023 | 
| 2026 | бронза | bronza | Chichateau · Blake Sauvignon Blanc 2023 | 
| 2026 | бронза | bronza | Erdevik · Grand Trianon 2019 | 
| 2026 | бронза | bronza | Deurić · La Rem Morava Amf 2023 | 
| 2026 | бронза | bronza | Veritas Ćuković · Barrique Chardonay 2023 | 
| 2026 | бронза | bronza | Trivanović · Trigio Blanc 2024 | 
| 2026 | двойное золото | dvojno-zlato | Šapat · Atila Plavi 2024 | 
| 2026 | золото | zlato | Vinum · Grašac Beli 2025 | 
| 2026 | золото | zlato | Vinum · Bermet Crveni 2023 | 
| 2026 | золото | zlato | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2017 | 
| 2026 | золото | zlato | Veritas Ćuković · Momentum 2017 | 
| 2026 | золото | zlato | Trivanović · Ultimo S 2020 | 
| 2026 | золото | zlato | Trivanović · Toca 2018 | 
| 2026 | золото | zlato | Šapat · Atila Cabernet sauvignon 2023 | 
| 2026 | золото | zlato | Šapat · Cuvee 2023 | 
| 2026 | золото | zlato | Šapat · Atila Sauvignon blanc 2024 | 
| 2026 | одобрение | approval | Vinum · Grašac 26A 2023 | 
| 2026 | платина | platina | Deurić · La Rem Chardonnay 2023 | 
| 2026 | серебро | srebro | Vinum · Chardonnay 2022 | 
| 2026 | серебро | srebro | Vinum · Frankovka 2022 | 
| 2026 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2024 | 
| 2026 | серебро | srebro | Chichateau · Chi Chardonnay 2024 | 
| 2026 | серебро | srebro | Kovačević · Rizling 2021 | 
| 2026 | серебро | srebro | Deurić · Aksiom 2021 | 
| 2026 | серебро | srebro | Chichateau · Fabula Lagum 2021 | 
| 2026 | серебро | srebro | Veritas Ćuković · Monte Karlovci 2022 | 
| 2026 | серебро | srebro | Šapat · Nera 2023 | 
| 2026 | серебро | srebro | Veritas Ćuković · Momentum Mali 2023 | 
| 2026 | серебро | srebro | Šapat · Atila Cabernet Sauvignon 2023 | 
| 2026 | серебро | srebro | Kovačević · Chardonnay 2025 | 
| 2026 | серебро | srebro | Deurić · Aksiom 2022 | 
| 2026 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2020 | 
| 2026 | серебро | srebro | Trivanović · Ultimo S 2020 | 
| 2026 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2023 | 
| 2026 | серебро | srebro | Kovačević · R Edition Brut 2012 | 
| 2026 | серебро | srebro | Kiš · Kisov Bermet 2025 | 
| 2026 | серебро | srebro | Kiš · Kisov Grasac beli 2025 | 
| 2026 | серебро | srebro | Kiš · Misterija polusuva 2025 | 
| 2026 | серебро | srebro | Kiš · Misterija 2025 | 
| 2026 | серебро | srebro | Trivanović · Optimus 2024 | 
| 2026 | серебро | srebro | Šapat · Bianca 2025 | 
| 2026 | серебро | srebro | Šapat · Atila Chardonnay 2024 | 
| 2025 | TROPHY DRY WHITE WINE | trofej | Šapat · Atila Chardonnay 2023 | 
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
| 2025 | бронза | bronza | Kiš · Kišov Bermet Belo 2024 | 
| 2025 | бронза | bronza | Kiš · Misterija Kišova 2024 | 
| 2025 | бронза | bronza | Mačkov podrum · Sauvignon blanc 2024 | 
| 2025 | бронза | bronza | Kiš · Biser Bermet beli 2024 | 
| 2025 | бронза | bronza | Šapat · Nera 2022 | 
| 2025 | бронза | bronza | Šapat · Cuvee 2022 | 
| 2025 | двойное золото | dvojno-zlato | Šapat · Atila Chardonnay 2023 | 
| 2025 | двойное золото | dvojno-zlato | Šapat · Atila Chardonnay 2023 | 
| 2025 | двойное золото | dvojno-zlato | Vinčić · Grand V 2023 | 
| 2025 | золото | zlato | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2025 | золото | zlato | Kiš · Kisov Grasac beli 2024 | 
| 2025 | золото | zlato | Vinarija Šijački · Seduša 2022 | 
| 2025 | золото | zlato | Vinarija Šijački · Superćelijski Grašac 2023 | 
| 2025 | золото | zlato | Kiš · Verus GT 2024 | 
| 2025 | лучшее белое, местные сорта | 1 | Deurić · La Rem Morava 2023 | 
| 2025 | лучшее красное, органика, международные сорта | 1 | Dukay-Sagmeister · Kew Kadarka 2022 | 
| 2025 | серебро | srebro | Chichateau · Blake Sauvignon Blanc 2023 | 
| 2025 | серебро | srebro | Deurić · La Rem Morava Amf 2023 | 
| 2025 | серебро | srebro | Deurić · La Rem Chardonnay 2023 | 
| 2025 | серебро | srebro | Deurić · Severna Morava 2023 | 
| 2025 | серебро | srebro | Vinčić · Grand Fru 2023 | 
| 2025 | серебро | srebro | Deurić · Gorska Tamjanika 2024 | 
| 2025 | серебро | srebro | Chichateau · Fabula Lagum Cabernet Sauvignon-Cabernet Franc-Merlot 2019 | 
| 2025 | серебро | srebro | Deurić · Aksiom 2019 | 
| 2025 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2025 | серебро | srebro | Erdevik · Grand Trianon 2020 | 
| 2025 | серебро | srebro | Erdevik · Stiflers Mom Shiraz 2020 | 
| 2025 | серебро | srebro | Vinčić · Grand Fru 2020 | 
| 2025 | серебро | srebro | Bikicki · Uncensored 2022 | 
| 2025 | серебро | srebro | Šapat · Cuvée 2022 | 
| 2025 | серебро | srebro | Šapat · Terol Teroldego 2022 | 
| 2025 | серебро | srebro | Kiš · Kisova Misterija, black label 2024 | 
| 2025 | серебро | srebro | Kiš · Biser Bermet crveni 2024 | 
| 2025 | серебро | srebro | Vinarija Šijački · Seduša 2021 | 
| 2025 | серебро | srebro | Šapat · Atila Caberne 2022 | 
| 2025 | серебро | srebro | Šapat · Šu-Šu 2024 | 
| 2025 | серебро | srebro | Šapat · Chardonnay 2023 | 
| 2025 | серебро | srebro | Vinčić · Grand Fru 2023 | 
| 2024 | GRAND TROPHY BEST WINE IN THE BALKANS | trofej | Vinum · Grasac beli 2019 | 
| 2024 | TROPHY DRY WHITE WINE | trofej | Vinum · Grasac beli 2019 | 
| 2024 | бронза | bronza | Vinčić · Grand Fru 2020 | 
| 2024 | бронза | bronza | Deurić · Pinot Noir 2020 | 
| 2024 | бронза | bronza | Molovin · Inat Limited Edition Rajnski Rizling 2021 | 
| 2024 | бронза | bronza | Erdevik · Geronimo 2021 | 
| 2024 | бронза | bronza | Šapat · Chardonnay 2022 | 
| 2024 | бронза | bronza | Veritas Ćuković · Bela Harmonija 2022 | 
| 2024 | бронза | bronza | Vinarija Djurdjic · Grašac Beli 2022 | 
| 2024 | бронза | bronza | Šapat · Pi'Crveno Premium 2019 | 
| 2024 | бронза | bronza | Vinum · Mustra 2022 | 
| 2024 | бронза | bronza | Verkat · Grasac Beli 2023 | 
| 2024 | бронза | bronza | Vinarija Djurdjic · Cabernet Franc Djurdjic 2021 | 
| 2024 | винодельня года | 1 | Kovačević | 
| 2024 | двойное золото | dvojno-zlato | Vinum · Grasac beli 2019 | 
| 2024 | двойное золото | dvojno-zlato | Vinum · Grasac 26a 2019 | 
| 2024 | двойное золото | dvojno-zlato | Vinum · Chardonnay 2021 | 
| 2024 | двойное золото | dvojno-zlato | Vinum · Chardonnay 2019 | 
| 2024 | двойное золото | dvojno-zlato | Verkat · Malvazija 2023 | 
| 2024 | двойное золото | dvojno-zlato | Vinčić · Grand Fru 2020 | 
| 2024 | золото | zlato | Šapat · Atila Chardonnay 2022 | 
| 2024 | золото | zlato | Vinum · Grasac 26a 2020 | 
| 2024 | золото | zlato | Vinum · Chardonnay 2020 | 
| 2024 | золото | zlato | Vinum · Grasac beli 2020 | 
| 2024 | золото | zlato | Vinum · Grasac beli 2021 | 
| 2024 | золото | zlato | Vinum · Grasac beli 2022 | 
| 2024 | золото | zlato | Vinum · white 2023 | 
| 2024 | золото | zlato | Vinum · Frankovka 2022 | 
| 2024 | золото | zlato | Vinum · Mustra 2023 | 
| 2024 | золото | zlato | Verkat · Malvazija 2022 | 
| 2024 | золото | zlato | Verkat · Roze 2022 | 
| 2024 | золото | zlato | Vinarija Djurdjic · Grasac Djurdjic 2022 | 
| 2024 | золото | zlato | Vinarija Djurdjic · Probus Djurdjic 2020 | 
| 2024 | золото | zlato | Kiš · Verus Grasac Beli 2023 | 
| 2024 | золото | zlato | Kiš · Verus GT 2023 | 
| 2024 | золото | zlato | Kiš · Biser crni | 
| 2024 | лучшая малая винодельня | 1 | Bikicki | 
| 2024 | лучшее белое, международные сорта | 1 | Kovačević · Edicija S Sauvignon 2021 | 
| 2024 | лучшее белое, органика, международные сорта | 1 | Dukay-Sagmeister · Kew Furmint 2020 | 
| 2024 | серебро | srebro | Šapat · Magnus 2020 | 
| 2024 | серебро | srebro | Šapat · Reserve Cabernet Sauvignon 2020 | 
| 2024 | серебро | srebro | Veritas Ćuković · Monte Karlovci Merlot 2021 | 
| 2024 | серебро | srebro | Veritas Ćuković · ćUk 2021 | 
| 2024 | серебро | srebro | Veritas Ćuković · Momentum 2021 | 
| 2024 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2021 | 
| 2024 | серебро | srebro | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2024 | серебро | srebro | Šapat · šU-šU Blaufrankisch 2022 | 
| 2024 | серебро | srebro | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2017 | 
| 2024 | серебро | srebro | Šapat · Bianca Moscato Giallo 2023 | 
| 2024 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2024 | серебро | srebro | Erdevik · Stiflers Mom Shiraz 2019 | 
| 2024 | серебро | srebro | Deurić · Aksiom Crveni 2019 | 
| 2024 | серебро | srebro | Vinum · Grasac 26a 2021 | 
| 2024 | серебро | srebro | Vinum · Grasac 26a 2022 | 
| 2024 | серебро | srebro | Vinum · Chardonnay 2022 | 
| 2024 | серебро | srebro | Vinum · Grasac beli 2018 | 
| 2024 | серебро | srebro | Vinum · Dina 2022 | 
| 2024 | серебро | srebro | Vinum · Bermet Cerveni 2023 | 
| 2024 | серебро | srebro | Verkat · Frankovka 2022 | 
| 2024 | серебро | srebro | Vinarija Djurdjic · Neoplanta Djurdjic 2022 | 
| 2024 | серебро | srebro | Kiš · Verus Mister & Ja 2023 | 
| 2024 | серебро | srebro | Kiš · Verus Chardonnay 2023 | 
| 2024 | серебро | srebro | Molovin · Inat Rajnski Risling 2021 | 
| 2023 | Best Indigenous White Wine Trophy | trofej | Vinčić · Grasac 2020 | 
| 2023 | Best in Show | best-in-show | Vinčić · Grašac 2020 | 
| 2023 | Best of Show Serbia | trofej | Vinčić · Grasac 2020 | 
| 2023 | бронза | bronza | Deurić · Probus 276 2018 | 
| 2023 | бронза | bronza | Molovin · Inat Frankovka 2019 | 
| 2023 | бронза | bronza | Deurić · Princeps Chardonnay 2021 | 
| 2023 | бронза | bronza | Deurić · Severna Morava 2020 | 
| 2023 | бронза | bronza | Vinčić · Grand Fru 2020 | 
| 2023 | бронза | bronza | Bikicki · S/O 2020 | 
| 2023 | бронза | bronza | Erdevik · Grand Trianon 2016 | 
| 2023 | бронза | bronza | Deurić · The Brut 2019 | 
| 2023 | бронза | bronza | Vinarija Djurdjic · Simonida Mlada | 
| 2023 | бронза | bronza | Vinarija Djurdjic · Neoplanta | 
| 2023 | бронза | bronza | Veritas Ćuković · Monte Carlovci 2020 | 
| 2023 | бронза | bronza | Trivanović · Reserve Cabernet Sauvignon 2017 | 
| 2023 | бронза | bronza | Vinčić · Vincic 2017 | 
| 2023 | винодельня года | 1 | Erdevik | 
| 2023 | вклад в винный туризм | 1 | Šapat | 
| 2023 | двойное золото | dvojno-zlato | Vinčić · Grasac 2020 | 
| 2023 | двойное золото | dvojno-zlato | Vinum · Grašac 26A 2021 | 
| 2023 | золото | zlato | Erdevik · Stifler's Mom Shiraz 2017 | 
| 2023 | золото | zlato | Molovin · Inat Traminac 2021 | 
| 2023 | золото | zlato | Veritas Ćuković · Bela Harmonija 2021 | 
| 2023 | золото | zlato | Veritas Ćuković · Momentum Mali 2020 | 
| 2023 | золото | zlato | Vinum · Chardonnay 2021 | 
| 2023 | лучшее белое | 1 | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2023 | лучшее из местных сортов, белое | 1 | Vinčić · Grašac 2020 | 
| 2023 | серебро | srebro | Erdevik · Trianon 2018 | 
| 2023 | серебро | srebro | Deurić · Aksiom Beli 2019 | 
| 2023 | серебро | srebro | Erdevik · Marlon Delon 2017 | 
| 2023 | серебро | srebro | Deurić · Classic Chardonnay 2021 | 
| 2023 | серебро | srebro | Deurić · Severna Morava 2021 | 
| 2023 | серебро | srebro | Bikicki · Uncensored 2020 | 
| 2023 | серебро | srebro | Verkat · Barrique Malvazija 2021 | 
| 2023 | серебро | srebro | Verkat · Grašac Beli 4.0 2021 | 
| 2023 | серебро | srebro | Mačkov podrum · Camerlot 2021 | 
| 2023 | серебро | srebro | Molovin · Inat Frankovka 2020 | 
| 2023 | серебро | srebro | Veritas Ćuković · Domina Rose 2021 | 
| 2023 | серебро | srebro | Veritas Ćuković · Cuk 2020 | 
| 2023 | серебро | srebro | Trivanović · Reserve Shiraz 2018 | 
| 2022 | Best of Show Serbia | trofej | Vinčić · White Reserve 2012 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Limited Edition Chardonnay 2020 | 
| 2022 | бронза | bronza | Erdevik · Geronimo 2020 | 
| 2022 | бронза | bronza | Deurić · Classic Chardonnay 2020 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Cabernet Sauvignon 2018 | 
| 2022 | бронза | bronza | Belo Brdo · Belo Brdo 2018 | 
| 2022 | бронза | bronza | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2016 | 
| 2022 | бронза | bronza | Deurić · Probus Princeps 2016 | 
| 2022 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2016 | 
| 2022 | бронза | bronza | Mačkov podrum · Chardonnay 2021 | 
| 2022 | бронза | bronza | Vinčić · Anfora 2017 | 
| 2022 | двойное золото | dvojno-zlato | Vinum · Grašac 26a 2019 | 
| 2022 | двойное золото | dvojno-zlato | Vinčić · White reserva 2012 | 
| 2022 | золото | zlato | Veritas Ćuković · Momentum Cabernet Sauvignon 2017 | 
| 2022 | золото | zlato | Verkat · Grašac beli 4.0 2021 | 
| 2022 | золото | zlato | Verkat · Malvazija 2021 | 
| 2022 | золото | zlato | Vinarija Djurdjic · Probus 2019 | 
| 2022 | золото | zlato | Vinarija Djurdjic · Rose Mlada Simonda 2021 | 
| 2022 | золото | zlato | Kiš · Kišov Grašac beli 2021 | 
| 2022 | золото | zlato | Mačkov podrum · Sauvignon Blanc 2021 | 
| 2022 | золото | zlato | Vinčić · Grand fru (grasac) 2020 | 
| 2022 | лучшее белое | 1 | Deurić · Aksiom beli 2019 | 
| 2022 | лучшее игристое | 1 | Deurić · The 2019 | 
| 2022 | серебро | srebro | Deurić · Severna Morava 2020 | 
| 2022 | серебро | srebro | Deurić · Aksiom Beli 2019 | 
| 2022 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2019 | 
| 2022 | серебро | srebro | Deurić · Classic Chardonnay 2019 | 
| 2022 | серебро | srebro | Erdevik · Trianon 2018 | 
| 2022 | серебро | srebro | Deurić · Aksiom 2017 | 
| 2022 | серебро | srebro | Erdevik · Stifles Mom 2017 | 
| 2022 | серебро | srebro | Vinarija Djurdjic · Neoplanta 2021 | 
| 2022 | серебро | srebro | Kiš · Kišov rose 2021 | 
| 2022 | серебро | srebro | Vinum · Chardonnay 2019 | 
| 2021 | Best of Show Serbia | trofej | Vinum · Dina Grasac sparkling 2018 | 
| 2021 | бронза | bronza | Kovačević · Fresco Bianco Brut 2019 | 
| 2021 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2021 | бронза | bronza | Bikicki · Cu 2018 | 
| 2021 | бронза | bronza | Deurić · Pinot Noir 2017 | 
| 2021 | бронза | bronza | Kovačević · Aurelius S Edicija 2017 | 
| 2021 | бронза | bronza | Bikicki · Makana 2016 | 
| 2021 | бронза | bronza | Belo Brdo · Cabernet Franc Limited Edition 2018 | 
| 2021 | бронза | bronza | Belo Brdo · Cabernet Sauvignon Limited Edition 2018 | 
| 2021 | бронза | bronza | Belo Brdo · Marselan Limited Edition 2018 | 
| 2021 | двойное золото | dvojno-zlato | Vinum · Chardonnay 2018 | 
| 2021 | двойное золото | dvojno-zlato | Vinum · Dina Sparkling Grašac 2018 | 
| 2021 | десятка лучших виноделен | 1 | Dukay-Sagmeister | 
| 2021 | золото | zlato | Bikicki · Uncensored 2018 | 
| 2021 | золото | zlato | Vinum · Grašac Beli 2019 | 
| 2021 | золото | zlato | Kiš · Kišov Grašac Beli 2020 | 
| 2021 | золото | zlato | Kiš · Kišovo Penušavo Vino 2019 | 
| 2021 | золото | zlato | Kiš · Kišov Bermet 2012 | 
| 2021 | золото | zlato | Vinarija Djurdjic · Cabernet Franc-Djurdjic 2015 | 
| 2021 | золото | zlato | Belo Brdo · Petit Verdot Limited Edition 2018 | 
| 2021 | серебро | srebro | Deurić · Aksiom 2016 | 
| 2021 | серебро | srebro | Deurić · Severna Morava 2018 | 
| 2021 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2017 | 
| 2021 | серебро | srebro | Vinarija Djurdjic · Rose Mlada Simonida-Djurdjic 2020 | 
| 2021 | серебро | srebro | Mačkov podrum · Sauvignon Blanc 2020 | 
| 2021 | серебро | srebro | Mačkov podrum · Chardonnay 2020 | 
| 2021 | серебро | srebro | Kiš · Kišov Chardonnay 2020 | 
| 2021 | серебро | srebro | Kiš · Kišov Rose 2020 | 
| 2021 | серебро | srebro | Kiš · Kišov Grašac Beli bariqque 2019 | 
| 2021 | серебро | srebro | Kiš · Kišov Chardonnay bariqque 2019 | 
| 2021 | серебро | srebro | Belo Brdo · Cabernet Franc Black Label 2017 | 
| 2020 | Best of Show Serbia | trofej | Veritas Ćuković · Momentum Cabernet Sauvignon 2017 | 
| 2020 | бронза | bronza | Kiš · Misterija Kišova 2011 | 
| 2020 | бронза | bronza | Vinarija Djurdjic · Cabernet Franc 2017 | 
| 2020 | бронза | bronza | Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah 2016 | 
| 2020 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2020 | бронза | bronza | Erdevik · Grand Trianon 2016 | 
| 2020 | бронза | bronza | Erdevik · Roza Nostra 2019 | 
| 2020 | бронза | bronza | Kiš · Kišov Grašac Beli 2019 | 
| 2020 | бронза | bronza | Bikicki · Uncensored 2017 | 
| 2020 | бронза | bronza | Deurić · Sauvignon Blanc 2018 | 
| 2020 | бронза | bronza | Bikicki · Lily 2018 | 
| 2020 | бронза | bronza | Deurić · Chardonnay barrique 2017 | 
| 2020 | бронза | bronza | Deurić · Gewürztraminer 2018 | 
| 2020 | бронза | bronza | Kiš · Kišov Chardonnay 2019 | 
| 2020 | бронза | bronza | Kiš · Kišov Grašac barrique 2019 | 
| 2020 | бронза | bronza | Verkat · Malvazija 2018 | 
| 2020 | двойное золото | dvojno-zlato | Veritas Ćuković · Momentum Cabernet Sauvignon 2017 | 
| 2020 | двойное золото | dvojno-zlato | Deurić · Probus 276 2017 | 
| 2020 | золото | zlato | Bikicki · Cu 2018 | 
| 2020 | золото | zlato | Bikicki · Uncensored 2018 | 
| 2020 | золото | zlato | Bikicki · Makana 2015 | 
| 2020 | золото | zlato | Bikicki · Traminac 2017 | 
| 2020 | золото | zlato | Kiš · Kišov Bermet 2012 | 
| 2020 | золото | zlato | Vinum · Chardonnay 2017 | 
| 2020 | золото | zlato | Vinarija Djurdjic · Cabernet Franc 2017 | 
| 2020 | золото | zlato | Vinarija Djurdjic · Rose Cabernet Sauvignon 2019 | 
| 2020 | лучшая малая винодельня | 1 | Chichateau | 
| 2020 | лучшая молодая винодельня | 1 | Deurić | 
| 2020 | лучшее белое | 1 | Chichateau · Chi Chardonnay 2016 | 
| 2020 | отмечено | commended | Deurić · Aksiom 2017 | 
| 2020 | отмечено | commended | Deurić · Princeps Pinot Noir 2016 | 
| 2020 | отмечено | commended | Deurić · Princeps Merlot 2016 | 
| 2020 | отмечено | commended | Kiš · Kišov Rosé 2019 | 
| 2020 | отмечено | commended | Deurić · Probus 276 2018 | 
| 2020 | отмечено | commended | Deurić · Barrique Sauvignon Blanc 2017 | 
| 2020 | платина | platina | Erdevik · Omnibus Lector Chardonnay 2015 | 
| 2020 | серебро | srebro | Veritas Ćuković · Momentum Cabernet Sauvignon 2017 | 
| 2020 | серебро | srebro | Vinum · Frankovka 2017 | 
| 2020 | серебро | srebro | Vinum · Pinot Noir 2017 | 
| 2020 | серебро | srebro | Erdevik · Stifler's Mom Shiraz 2016 | 
| 2020 | серебро | srebro | Bikicki · S/O 2017 | 
| 2020 | серебро | srebro | Erdevik · Omnibus Lector Chardonnay 2017 | 
| 2020 | серебро | srebro | Deurić · Classic Chardonnay 2018 | 
| 2020 | серебро | srebro | Bikicki · SO 2017 | 
| 2020 | серебро | srebro | Bikicki · Crna Tamjanika 2017 | 
| 2020 | серебро | srebro | Verkat · Grasac beli 2019 | 
| 2020 | серебро | srebro | Deurić · Aksiom 2017 | 
| 2020 | серебро | srebro | Deurić · Classic Chardonnay 2018 | 
| 2020 | серебро | srebro | Deurić · Sauvignon blanc 2018 | 
| 2020 | серебро | srebro | Kiš · Kišov Rose 2019 | 
| 2020 | серебро | srebro | Kiš · Kišovo Penušavo Vino 2019 | 
| 2020 | серебро | srebro | Kiš · Kišov Chardonnay barrique 2019 | 
| 2020 | серебро | srebro | Kiš · Kišov Grašac 2019 | 
| 2020 | серебро | srebro | Veritas Ćuković · Sauvignon Blanc 2019 | 
| 2020 | серебро | srebro | Vinum · Pinot Noir 2017 | 
| 2020 | серебро | srebro | Vinum · Rose Pinot Noir 2019 | 
| 2020 | серебро | srebro | Vinarija Djurdjic · Crni Vitez Bermet 2018 | 
| 2020 | серебро | srebro | Vinarija Djurdjic · Sauvignon Blanc 2019 | 
| 2019 | Orange Wine Trophy | trofej | Bikicki · Uncensored 2017 | 
| 2019 | бронза | bronza | Deurić · The Brut 2015 | 
| 2019 | бронза | bronza | Deurić · Aksiom 2016 | 
| 2019 | бронза | bronza | Deurić · Talas crveni 2015 | 
| 2019 | золото | zlato | Bikicki · Pinotte 2015 | 
| 2019 | золото | zlato | Bikicki · Cu 2017 | 
| 2019 | золото | zlato | Deurić · Pinot Noir 2017 | 
| 2019 | золото | zlato | Kiš · Grasac beli 2017 | 
| 2019 | лучшая малая винодельня | 1 | Bikicki | 
| 2019 | лучшее игристое | 1 | Deurić · Princeps Brut Nature 2015 | 
| 2019 | отмечено | commended | Deurić · Probus 276 2017 | 
| 2019 | отмечено | commended | Deurić · Pinot Noir 2017 | 
| 2019 | отмечено | commended | Molovin · Vista Hill Selection 2017 | 
| 2019 | отмечено | commended | Deurić · Aksiom 2016 | 
| 2019 | серебро | srebro | Deurić · Talas Crveni 2017 | 
| 2019 | серебро | srebro | Molovin · Vista Hill Red Reserve 2010 | 
| 2019 | серебро | srebro | Deurić · Princeps Brut Nature 2015 | 
| 2019 | серебро | srebro | Bikicki · Makana 2016 | 
| 2019 | серебро | srebro | Vinarija Šijački · Rizling italijanski Šijački 2018 | 
| 2019 | серебро | srebro | Vinarija Šijački · Seduša Šijački 2017 | 
| 2019 | серебро | srebro | Deurić · Probus 276 2017 | 
| 2019 | серебро | srebro | Deurić · Urban Rose 2018 | 
| 2019 | серебро | srebro | Deurić · Classic Chardonnay 2018 | 
| 2019 | серебро | srebro | Deurić · Sauvignon blanc 2017 | 
| 2019 | серебро | srebro | Vinarija Djurdjic · Sauvignon Bland Djurdjic 2018 | 
| 2019 | серебро | srebro | Vinarija Djurdjic · Cabernet Franc Djurdjic 2016 | 
| 2019 | серебро | srebro | Kiš · Bermet 2012 | 
| 2019 | серебро | srebro | Vinarija Šijački · Neoplanta Šijacki 2017 | 
| 2019 | серебро | srebro | Kiš · Rose 2018 | 
| 2019 | серебро | srebro | Kiš · Bermet 2012 | 
| 2018 | бронза | bronza | Molovin · Crveni Inat 2010 | 
| 2018 | бронза | bronza | Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah 2015 | 
| 2018 | бронза | bronza | Kovačević · R Edition Aurelius 2012 | 
| 2018 | бронза | bronza | Trivanović · Pinot Grigio 2017 | 
| 2018 | бронза | bronza | Trivanović · Rose 2017 | 
| 2018 | бронза | bronza | Deurić · Gewurztraminer 2016 | 
| 2018 | бронза | bronza | Deurić · Urban Rose 2017 | 
| 2018 | бронза | bronza | Deurić · Red Blend 2016 | 
| 2018 | бронза | bronza | Deurić · Avangarda 2016 | 
| 2018 | двойное золото | dvojno-zlato | Bikicki · Cu Orange Wine 2016 | 
| 2018 | золото | zlato | Deurić · Pinot Noir 2016 | 
| 2018 | золото | zlato | Kiš · Kišov Bermet | 
| 2018 | золото | zlato | Bikicki · Crna Tamjanika 2015 | 
| 2018 | золото | zlato | Bikicki · Makana 2015 | 
| 2018 | отмечено | commended | Kovačević · S Edition Chardonnay 2015 | 
| 2018 | отмечено | commended | Kovačević · Chardonnay 2017 | 
| 2018 | отмечено | commended | Kovačević · S Edition Aurelius 2014 | 
| 2018 | отмечено | commended | Deurić · Chardonnay 2016 | 
| 2018 | отмечено | commended | Kovačević · S Edition Sauvignon 2016 | 
| 2018 | отмечено | commended | Deurić · Pinot noir 2016 | 
| 2018 | отмечено | commended | Molovin · Graševina 2012 | 
| 2018 | отмечено | commended | Kovačević · Brut 2010 | 
| 2018 | серебро | srebro | Erdevik · Nostra 2017 | 
| 2018 | серебро | srebro | Deurić · Probus 2016 | 
| 2018 | серебро | srebro | Bikicki · Traminac 2016 | 
| 2018 | серебро | srebro | Deurić · Merlot 2016 | 
| 2018 | серебро | srebro | Deurić · Chardonnay 2016 | 
| 2018 | серебро | srebro | Deurić · Talas crveni 2016 | 
| 2018 | серебро | srebro | Deurić · Probus 2016 | 
| 2018 | серебро | srebro | Deurić · The 2015 | 
| 2018 | серебро | srebro | Kiš · Kišov Rose 2017 | 
| 2018 | серебро | srebro | Vinum · Mustra 2017 | 
| 2018 | серебро | srebro | Vinum · Rose 2017 | 
| 2017 | бронза | bronza | Deurić · Talas Beli 2015 | 
| 2017 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2015 | 
| 2017 | бронза | bronza | Deurić · Enigma 2015 | 
| 2017 | бронза | bronza | Deurić · Urban Rose 2015 | 
| 2017 | бронза | bronza | Deurić · Pinot Noir 2015 | 
| 2017 | бронза | bronza | Deurić · Talas Crveni 2015 | 
| 2017 | бронза | bronza | Deurić · Merlot 2015 | 
| 2017 | бронза | bronza | Deurić · Avangarda Sauvignon Blanc 2016 | 
| 2017 | бронза | bronza | Vinarija Djurdjic · Crni Vitez Bermet 2011 | 
| 2017 | бронза | bronza | Kiš · Grašac beli 2016 | 
| 2017 | бронза | bronza | Kovačević · Chardonnay 2016 | 
| 2017 | бронза | bronza | Trivanović · Pinot Grigio 2016 | 
| 2017 | бронза | bronza | Trivanović · Trigio 2016 | 
| 2017 | золото | zlato | Kiš · Bermet | 
| 2017 | золото | zlato | Kovačević · Brut 2010 | 
| 2017 | отмечено | commended | Deurić · Gewürztraminer 2015 | 
| 2017 | отмечено | commended | Deurić · Avangarda 2015 | 
| 2017 | отмечено | commended | Deurić · Chardonnay 2015 | 
| 2017 | отмечено | commended | Erdevik · Roza Nostra 2015 | 
| 2017 | отмечено | commended | Deurić · Merlot 2015 | 
| 2017 | серебро | srebro | Deurić · Talas Crveni 2015 | 
| 2017 | серебро | srebro | Bjelica · Saga 2016 | 
| 2017 | серебро | srebro | Bjelica · Babaroga 2015 | 
| 2017 | серебро | srebro | Deurić · Enigma 2015 | 
| 2017 | серебро | srebro | Deurić · Chardonnay 2015 | 
| 2017 | серебро | srebro | Deurić · Urban Rosé 2016 | 
| 2017 | серебро | srebro | Deurić · Pinot Noir 2015 | 
| 2017 | серебро | srebro | Deurić · Talas Beli 2015 | 
| 2017 | серебро | srebro | Deurić · Gewürztraminer 2016 | 
| 2017 | серебро | srebro | Vinarija Djurdjic · Sauvignon Blanc 2016 | 
| 2017 | серебро | srebro | Kiš · Misterija 2011 | 
| 2017 | серебро | srebro | Kiš · Bermet Beli | 
| 2017 | серебро | srebro | Kovačević · Orphe Line 2016 | 
| 2017 | серебро | srebro | Kovačević · Chardonnay | 
| 2016 | Rose Wine Trophy | trofej | Vinum · Rose 2015 | 
| 2016 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2016 | бронза | bronza | Molovin · Crveni Inat 2010 | 
| 2016 | бронза | bronza | Deurić · Enigma 2015 | 
| 2016 | бронза | bronza | Deurić · Talas Crveni 2015 | 
| 2016 | бронза | bronza | Deurić · Talas Crveni 2014 | 
| 2016 | бронза | bronza | Kovačević · Chardonnay Vinarija Kovacevic 2015 | 
| 2016 | бронза | bronza | Kiš · Kišov Bermet Belo | 
| 2016 | золото | zlato | Deurić · Chardonnay 2015 | 
| 2016 | золото | zlato | Deurić · Gewurztraminer 2015 | 
| 2016 | золото | zlato | Deurić · Avangarda 2015 | 
| 2016 | золото | zlato | Deurić · Talas Beli 2014 | 
| 2016 | золото | zlato | Bjelica · Saga 2015 | 
| 2016 | золото | zlato | Bjelica · Babaroga Penušavac 2014 | 
| 2016 | отмечено | commended | Molovin · Inat 2012 | 
| 2016 | отмечено | commended | Kovačević · Sauvignon 2012 | 
| 2016 | отмечено | commended | Kiš · Misterija 2011 | 
| 2016 | серебро | srebro | Belo Brdo · Chardonnay 2015 | 
| 2016 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2015 | 
| 2016 | серебро | srebro | Molovin · Plavi Princip 2013 | 
| 2016 | серебро | srebro | Bjelica · Babaroga 2015 | 
| 2016 | серебро | srebro | Deurić · Talas Beli 2015 | 
| 2016 | серебро | srebro | Deurić · Urban Rose 2015 | 
| 2016 | серебро | srebro | Kovačević · Aurelius R Vinarija Kovacevic 2012 | 
| 2016 | серебро | srebro | Kovačević · Rosetto Vinarija Kovacevic 2015 | 
| 2015 | бронза | bronza | Belo Brdo · Cabernet Franc 2012 | 
| 2015 | бронза | bronza | Belo Brdo · Alma Mons 2012 | 
| 2015 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2015 | бронза | bronza | Kiš · Kišova Misterija Polusuvo 2011 | 
| 2015 | бронза | bronza | Kiš · Kisov Bermet | 
| 2015 | золото | zlato | Kiš · Kisova Misterija polusuva 2011 | 
| 2015 | золото | zlato | Kiš · Kišov Bermet Belo | 
| 2015 | отмечено | commended | Bjelica · Graffiti Crveno 2013 | 
| 2015 | отмечено | commended | Bjelica · Babaroga 2013 | 
| 2015 | отмечено | commended | Molovin · Inat 2013 | 
| 2015 | отмечено | commended | Belo Brdo · Cabernet Sauvignon 2011 | 
| 2015 | отмечено | commended | Molovin · Princip 2012 | 
| 2015 | отмечено | commended | Molovin · Inat Crown Plaza 2012 | 
| 2015 | отмечено | commended | Vinum · Italijanski rizling 2013 | 
| 2015 | серебро | srebro | Veritas Ćuković · Momentum Cabernet Sauvignon 2012 | 
| 2015 | серебро | srebro | Vinum · Sauvignon Blanc 2013 | 
| 2015 | серебро | srebro | Kiš · Misterija Kišova 2013 | 
| 2015 | серебро | srebro | Veritas Ćuković · Momentum Cabernet Sauvignon 2012 | 
| 2014 | Rose Wine Trophy | trofej | Kiš · Kišov Rose 2013 | 
| 2014 | бронза | bronza | Bjelica · Saga 2013 | 
| 2014 | бронза | bronza | Bjelica · Graffiti 2013 | 
| 2014 | бронза | bronza | Kiš · Kišov Bermet 2014 | 
| 2014 | золото | zlato | Kiš · Kišov Rose 2013 | 
| 2014 | золото | zlato | Kiš · Bermet white | 
| 2014 | отмечено | commended | Kovačević · Chardonnay 2012 | 
| 2014 | отмечено | commended | Bjelica · Graffiti 2012 | 
| 2014 | отмечено | commended | Kovačević · Rosetto 2013 | 
| 2014 | серебро | srebro | Kiš · Misterija Kišova 2011 | 
| 2013 | бронза | bronza | Molovin · Plavi Princip 2011 | 
| 2013 | бронза | bronza | Belo Brdo · Alma Mons 2011 | 
| 2013 | отмечено | commended | Molovin · Princip 2010 | 
| 2013 | отмечено | commended | Molovin · Inat 2010 | 
| 2013 | отмечено | commended | Molovin · Rosé 2012 | 
| 2013 | отмечено | commended | Belo Brdo · Chardonnay 2011 | 
| 2013 | отмечено | commended | Molovin · Inat 2011 | 
| 2012 | бронза | bronza | Molovin · Eastern Vintage Rizzling Caravan White 2010 | 
| 2012 | отмечено | commended | Molovin · Molovinski 2011 | 

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
| Zvonko Bogdan · Cuvée No.1 | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Merlot Single Vineyard | 2019 | 94 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2017 | 93 | Wine-Searcher |
| Zvonko Bogdan · Chardonnay | 2017 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 93 | Falstaff |
| Zvonko Bogdan · Pinot Blanc | 2019 | 93 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 93 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 93 | decanter |
| Zvonko Bogdan · Éclater Blanc de Blancs Brut Nature | 2020 | 93 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2017 | 92 | Falstaff |
| Zvonko Bogdan · Rosé Sec | 2022 | 92 | Falstaff |
| Vinarija Petra · Pinot Grigio Orange | 2020 | 92 | Falstaff |
| Vinarija Petra · Pinot Noir Barrique | 2020 | 92 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2013 | 92 | decanter |
| Zvonko Bogdan · Pinot blanc | 2017 | 92 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2017 | 92 | decanter |
| Tonković · Rapsodija | 2015 | 92 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 92 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2018 | 92 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2023 | 91 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2016 | 91 | Falstaff |
| Vinarija Petra · Pinot Grigio Orange | 2021 | 91 | Falstaff |
| Zvonko Bogdan · Sauvignon Blanc | 2019 | 91 | Falstaff |
| Zvonko Bogdan · Chardonnay | 2018 | 91 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2015 | 91 | decanter |
| Tonković · Fantazija | 2012 | 91 | decanter |
| Tonković · Fantazija Kadarka | 2015 | 91 | decanter |
| Zvonko Bogdan · Chardonnay | 2019 | 91 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2021 | 91 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 91 | decanter |
| Zvonko Bogdan · Cuvée no.1 | 2023 | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2023 | 91 | decanter |
| Zvonko Bogdan · Chardonnay | 2023 | 91 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2022 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2021 | 90 | Wine-Searcher |
| Zvonko Bogdan · Cuvée No.1 | 2018 | 90 | Wine-Searcher |
| Vinarija Petra · Pinot Noir | 2020 | 90 | Falstaff |
| Vinarija Petra · Rose&co | 2020 | 90 | Falstaff |
| Vinarija Petra · Traminac | 2020 | 90 | Falstaff |
| Zvonko Bogdan · Éclater Blanc de Blancs Extra Brut | 2018 | 90 | Falstaff |
| Zvonko Bogdan · Icon Campana Rubimus | 2013 | 90 | decanter |
| Zvonko Bogdan · Chardonnay | 2015 | 90 | decanter |
| Tonković · Rapsodija Kadarka | 2014 | 90 | decanter |
| Zvonko Bogdan · Život Teče | 2017 | 90 | decanter |
| Zvonko Bogdan · Chardonnay | 2018 | 90 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2018 | 90 | decanter |
| Zvonko Bogdan · Rose Sec | 2021 | 90 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2019 | 90 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2024 | 90 | decanter |
| Vinarija Petra · Rosé | 2019 | 89 | Falstaff |
| Zvonko Bogdan · Život Teče | 2016 | 89 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2018 | 89 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2022 | 89 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2020 | 89 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2024 | 89 | decanter |
| Vinarija Petra · Pinot Grigio | 2017 | 88 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2015 | 88 | decanter |
| Zvonko Bogdan · Chardonnay | 2019 | 88 | decanter |
| Zvonko Bogdan · Sauvignon Blanc | 2021 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 88 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2021 | 88 | decanter |
| Zvonko Bogdan · Merlot | 2022 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 88 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2022 | 88 | decanter |
| Tonković · Rapsodija | 2013 | 87 | decanter |
| Zvonko Bogdan · Život Teče | 2015 | 87 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2017 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2017 | 87 | decanter |
| Zvonko Bogdan · Pinot Grigio | 2019 | 87 | decanter |
| Zvonko Bogdan · Merlot | 2019 | 87 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2019 | 87 | decanter |
| Zvonko Bogdan · Rosé Sec | 2022 | 87 | decanter |
| Tonković · Fantazija Organic Kadarka | 2022 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2018 | 87 | decanter |
| Zvonko Bogdan · Merlot | 2022 | 87 | decanter |
| Zvonko Bogdan · Chardonnay | 2015 | 86 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2018 | 86 | decanter |
| Tonković · Rapsodija Kadarka | 2019 | 86 | decanter |
| Zvonko Bogdan · Rose Sec | 2016 | 85 | decanter |
| Tonković · Fantazija | 2013 | 85 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2024 | 
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
| 2024 | бронза | bronza | Zvonko Bogdan · Cuvee No1 2021 | 
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
| 2022 | двойное золото | dvojno-zlato | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2022 | золото | zlato | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2022 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2019 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Rose Sec 2021 | 
| 2022 | серебро | srebro | Zvonko Bogdan · Rose sec 2021 | 
| 2021 | двойное золото | dvojno-zlato | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2021 | десятка лучших виноделен | 3 | Maurer | 
| 2021 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2019 | 
| 2021 | золото | zlato | Zvonko Bogdan · Icon Campana Rubimus 2017 | 
| 2021 | золото | zlato | Zvonko Bogdan · Cuvee No.1 2019 | 
| 2021 | золото | zlato | Zvonko Bogdan · Merlot 2019 | 
| 2021 | золото | zlato | Zvonko Bogdan · Chardonnay 2020 | 
| 2021 | золото | zlato | Zvonko Bogdan · Pinot Grigio 2020 | 
| 2021 | золото | zlato | Zvonko Bogdan · Sauvignon Blanc 2020 | 
| 2021 | золото | zlato | Tonković · Allegro 2020 | 
| 2021 | золото | zlato | Tonković · Rapsodija 2015 | 
| 2021 | лучшее белое | 1 | Zvonko Bogdan · Icon Campana Albus 2020 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Merlot 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Chardonnay 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Chardonnay 2019 | 
| 2021 | серебро | srebro | Zvonko Bogdan · Pinot Blanc 2019 | 
| 2021 | серебро | srebro | Tonković · Fantazija 2015 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Pinot Grigio 2019 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2018 | 
| 2020 | бронза | bronza | Zvonko Bogdan · Icon Campana Rubimus 2018 | 
| 2020 | бронза | bronza | Tonković · Rapsodija 2015 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Icon Campana Albus 2017 | 
| 2020 | серебро | srebro | Tonković · Fantazija Kadarka 2015 | 
| 2020 | серебро | srebro | Tonković · Rapsodija 2015 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Chardonnay 2018 | 
| 2020 | серебро | srebro | Zvonko Bogdan · Cuvée No.1 2018 | 
| 2020 | серебро | srebro | Tonković · Fantazija 2015 | 
| 2019 | бронза | bronza | Zvonko Bogdan · Icon Campana Albus 2017 | 
| 2019 | бронза | bronza | Zvonko Bogdan · Chardonnay 2017 | 
| 2019 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2017 | 
| 2019 | золото | zlato | Zvonko Bogdan · Icon Campana Rubimus 2017 | 
| 2019 | серебро | srebro | Zvonko Bogdan · Pinot blanc 2017 | 
| 2019 | серебро | srebro | Zvonko Bogdan · Život Teče 2017 | 
| 2018 | бронза | bronza | Zvonko Bogdan · Chardonnay 2015 | 
| 2018 | бронза | bronza | Zvonko Bogdan · Život Teče 2016 | 
| 2018 | золото | zlato | Zvonko Bogdan · Cuvée No.1 2016 | 
| 2018 | золото | zlato | Tonković · Karadrka Rose 2017 | 
| 2018 | отмечено | commended | Tonković · Fantazija 2013 | 
| 2018 | серебро | srebro | Tonković · Rapsodija Kadarka 2014 | 
| 2018 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2013 | 
| 2018 | серебро | srebro | Tonković · Rapsodija 2014 | 
| 2018 | серебро | srebro | Tonković · Fantazija 2013 | 
| 2017 | бронза | bronza | Tonković · Rapsodija 2013 | 
| 2017 | бронза | bronza | Zvonko Bogdan · Život Teče 2015 | 
| 2017 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2015 | 
| 2017 | отмечено | commended | Zvonko Bogdan · Rose Sec 2016 | 
| 2017 | серебро | srebro | Zvonko Bogdan · Chardonnay 2015 | 
| 2017 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2015 | 
| 2017 | серебро | srebro | Tonković · Fantazija 2012 | 
| 2016 | бронза | bronza | Zvonko Bogdan · Icon Campana Albus 2014 | 
| 2016 | бронза | bronza | Zvonko Bogdan · Icon Campana Albus 2013 | 
| 2016 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2014 | 
| 2016 | золото | zlato | Zvonko Bogdan · Pinot Grigio 2015 | 
| 2016 | золото | zlato | Zvonko Bogdan · Rose Sec 2015 | 
| 2016 | отмечено | commended | Zvonko Bogdan · Icon Campana Rubimus 2013 | 
| 2016 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubimus 2013 | 
| 2016 | серебро | srebro | Zvonko Bogdan · Sauvignon Blanc 2015 | 
| 2015 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2012 | 
| 2015 | бронза | bronza | Tonković · Rapsodija Kadarka 2012 | 
| 2015 | отмечено | commended | Tonković · Kadarka Rosé 2014 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Rosé Sec 2014 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Icon Campana 2013 | 
| 2015 | отмечено | commended | Tonković · Fantazija Kadarka 2011 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Zivot Tece 2013 | 
| 2015 | отмечено | commended | Tonković · Kadarka Icon 2011 | 
| 2015 | серебро | srebro | Zvonko Bogdan · Sauvignon blanc 2014 | 
| 2014 | бронза | bronza | Tonković · Fantazija Kadarka 2011 | 
| 2014 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2013 | 
| 2014 | бронза | bronza | Tonković · Kadarka 2013 | 
| 2014 | отмечено | commended | Zvonko Bogdan · Cuvee No.1 2012 | 
| 2014 | отмечено | commended | Tonković · Icon Kadarka 2011 | 
| 2014 | отмечено | commended | Zvonko Bogdan · Sauvignon Blanc 2013 | 
| 2013 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2012 | 
| 2013 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2010 | 
| 2013 | отмечено | commended | Zvonko Bogdan · Sauvignon Blanc 2012 | 
| 2013 | отмечено | commended | Zvonko Bogdan · Rose | 
| 2013 | отмечено | commended | Zvonko Bogdan · Život Teče 2010 | 
| 2012 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2008 | 
| 2012 | бронза | bronza | Zvonko Bogdan · Cuvee Zivot Tece 2009 | 

## Банат

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Drašković · Mahago Frankovka | 2019 | 92 | biwc |
| Drašković · Mahago | 2019 | 90 | decanter |
| Drašković · Beli Pinot | 2020 | 90 | decanter |
| Drašković · Beli Pinot | 2021 | 90 | decanter |
| Drašković · Frankovka Rezerva | 2018 | 90 | decanter |
| Drašković · Horizont Chardonnay | 2021 | 89 | decanter |
| Drašković · Classic Chardonnay | 2022 | 89 | biwc |
| Drašković · Mahago | 2017 | 88 | decanter |
| Drašković · Beli Pinot | 2019 | 87 | decanter |
| Drašković · Burgundac Beli | 2021 | 87 | decanter |
| Drašković · Mahago Frankovka | 2021 | 87 | decanter |
| Drašković · Beli Pinot Authentic | 2020 | 87 | biwc |
| Drašković · Frankovka rezerva | 2018 | 87 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2022 | 86 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2022 | 85 | biwc |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2022 | 85 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2022 | 85 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2022 | 85 | biwc |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2020 | 84 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2021 | 84 | biwc |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2022 | 84 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2020 | 82 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2025 | бронза | bronza | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2022 | 
| 2025 | серебро | srebro | Vinarija Coka · Muštuluk Crveni 2022 | 
| 2025 | серебро | srebro | Vinarija Coka · Grof Lederer MERLOT 2022 | 
| 2024 | бронза | bronza | Drašković · Mahago Frankovka 2021 | 
| 2024 | серебро | srebro | Drašković · Beli Pinot 2021 | 
| 2024 | серебро | srebro | Drašković · Frankovka Rezerva 2018 | 
| 2024 | серебро | srebro | Vinarija Coka · Grof Lederer MERLOT 2022 | 
| 2024 | серебро | srebro | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2022 | 
| 2024 | серебро | srebro | Vinarija Coka · Muštuluk Crveni 2022 | 
| 2023 | бронза | bronza | Drašković · Horizont Chardonnay 2021 | 
| 2023 | бронза | bronza | Drašković · Burgundac Beli 2021 | 
| 2023 | бронза | bronza | Vinarija Coka · Grof Lederer MERLOT 2021 | 
| 2023 | бронза | bronza | Vinarija Coka · Muštuluk Crveni 2020 | 
| 2023 | золото | zlato | Drašković · Classic Chardonnay 2022 | 
| 2023 | золото | zlato | Drašković · Mahago Frankovka 2019 | 
| 2023 | серебро | srebro | Drašković · Mahago 2019 | 
| 2023 | серебро | srebro | Drašković · Beli Pinot 2020 | 
| 2023 | серебро | srebro | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2020 | 
| 2023 | серебро | srebro | Drašković · Beli Pinot Authentic 2020 | 
| 2023 | серебро | srebro | Drašković · Frankovka rezerva 2018 | 
| 2022 | бронза | bronza | Drašković · Beli Pinot Authentic 2020 | 
| 2022 | золото | zlato | Drašković · Ruža vetrova 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Grof Lederer Merlot 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Grof Lederer Cabernet Sauvignon 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Muštuluk 2020 | 
| 2022 | серебро | srebro | Drašković · Burgundac beli Classic 2021 | 
| 2022 | серебро | srebro | Drašković · Classic Chardonnay 2021 | 
| 2021 | бронза | bronza | Drašković · Beli Pinot 2019 | 
| 2021 | бронза | bronza | Drašković · Mahago 2017 | 
| 2021 | бронза | bronza | Drašković · Mahago 2017 | 
| 2021 | бронза | bronza | Vinarija Coka · Grof Lederer Cabernet Sauvignon 2019 | 
| 2021 | золото | zlato | Vinarija Coka · Grof Lederer Merlot 2019 | 
| 2021 | серебро | srebro | Drašković · Beli Pinot 2019 | 
| 2021 | серебро | srebro | Drašković · Ruža Vetrova 2018 | 
| 2021 | серебро | srebro | Drašković · Muskat Otonel 2019 | 
| 2020 | бронза | bronza | Vinarija Coka · Lederer Merlot 2018 | 

## Шумадия

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 2022 | 97 | decanter |
| Matijašević · SoviNoa Fumé Blanc | 2020 | 96 | decanter |
| Arsenijević · Kaberne | 2021 | 96 | biwc |
| Matijašević · SoviNoa | 2019 | 95 | decanter |
| Aleksandrović · Regent Reserve | 2018 | 95 | decanter |
| Matijašević · Tri Doline | 2020 | 95 | decanter |
| Matijašević · Sovinoa Fumé Blanc | 2021 | 95 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 95 | decanter |
| Tarpoš · Prokupac | 2023 | 95 | decanter |
| Despotika · Krunski Dokaz | 2017 | 95 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 95 | decanter |
| Tarpoš · Merlot | 2021 | 95 | biwc |
| Matijašević · SoviNoa Fumé Blanc | 2020 | 94 | Falstaff |
| Aleksandrović · Trijumf Gold | 2022 | 94 | Falstaff |
| Matijašević · Sovi Noa Fumé Blanc | 2020 | 94 | Falstaff |
| Matijašević · Sovi Noa Fumé Blanc | 2021 | 94 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 94 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2020 | 93 | Falstaff |
| Matijašević · SoviNoa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2021 | 93 | Falstaff |
| Despotika · Krunski Dokas (The Key Evidence) Grand Reserve | 2017 | 93 | Falstaff |
| Aleksandrović · VOŽD | 2017 | 93 | Falstaff |
| Matijašević · Belina | 2022 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection | 2021 | 93 | Falstaff |
| Matijašević · Tri Doline Merlot | 2020 | 93 | Falstaff |
| Aleksandrović · Trijumf Chardonnay Brut | 2018 | 93 | Falstaff |
| Aleksandrović · Trijumf Terroir | 2022 | 93 | Falstaff |
| Matijašević · Sovi Noa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 93 | Falstaff |
| Aleksandrović · Trijumf Noir | 2010 | 93 | decanter |
| Matijašević · Čukundeda Prokupac | 2019 | 93 | decanter |
| Aleksandrović · Trijumf Gold | 2023 | 93 | decanter |
| Despotika · Barik Morava | 2022 | 93 | decanter |
| Despotika · Neizbrisivi trag | 2021 | 93 | biwc |
| Aleksandrović · Trijumf Noir Brut | 2010 | 92 | Falstaff |
| Despotika · Nemir (Turbulence) Rosé | — | 92 | Falstaff |
| Aleksandrović · Prokupac | 2021 | 92 | Falstaff |
| Matijašević · Čukundeda Prokupac | 2020 | 92 | Falstaff |
| Aleksandrović · Trijumf Prokupac | 2020 | 92 | Falstaff |
| Matijašević · Belina | 2020 | 92 | Falstaff |
| Matijašević · Prokupac Cukundeda Superiore | 2019 | 92 | Falstaff |
| Despotika · Trag (The Clue) Merlot | 2019 | 92 | Falstaff |
| Aleksandrović · Trijumf Rosé Brut | 2019 | 92 | Falstaff |
| Aleksandrović · Prokupac | 2019 | 92 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 92 | decanter |
| Matijašević · Sovinoa Sauvignon Blanc | 2021 | 92 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 92 | decanter |
| Aleksandrović · Rodoslov Reserve | — | 91 | Wine-Searcher |
| Radovanović · Reserve Cabernet Sauvignon | 2013 | 91 | Tastings.com |
| Despotika · Zmajeviti Prokupac | — | 91 | Falstaff |
| Despotika · Zmajeviti Prokupac (The Dragons Wine) | — | 91 | Falstaff |
| Aleksandrović · Trijumf Rosé Pinot Noir | 2022 | 91 | Falstaff |
| Despotika · Morava | 2021 | 91 | Falstaff |
| Despotika · Morava Barik | 2021 | 91 | Falstaff |
| Despotika · Morava Glina | 2021 | 91 | Falstaff |
| Despotika · Morava Orange | 2020 | 91 | Falstaff |
| Aleksandrović · Oplen Rheinriesling | 2020 | 91 | Falstaff |
| Aleksandrović · Vizija Selection | 2020 | 91 | Falstaff |
| Radovanović · Rèserve Cabernet Sauvignon | 2019 | 91 | Falstaff |
| Despotika · Trag | 2017 | 91 | decanter |
| Aleksandrović · Vizija Selection | 2016 | 91 | decanter |
| Matijašević · Sovinoa Sauvignon Blanc | 2020 | 91 | decanter |
| Matijašević · Čukundeda Superiore | 2019 | 91 | decanter |
| Matijašević · Cukundeda Prokupac | 2021 | 91 | decanter |
| Aleksandrović · Regent Reserve | 2019 | 91 | decanter |
| Matijašević · Belina | 2022 | 91 | decanter |
| Radovanović · Réserve Cabernet Sauvignon | — | 90 | Wine-Searcher |
| Radovanović · Cabernet Sauvignon Classique | 2015 | 90 | Tastings.com |
| Matijašević · Belina Inferno | 2022 | 90 | Falstaff |
| Despotika · Beckapaj (Infintiy) Sauvignon Blanc | 2021 | 90 | Falstaff |
| Despotika · Morava Inoks | 2021 | 90 | Falstaff |
| Radovanović · Chardonnay Classique | 2020 | 90 | Falstaff |
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
| Despotika · Nebo | 2023 | 90 | biwc |
| Despotika · Morava | 2022 | 90 | biwc |
| Tarpoš · Cabernet Sauvignon | 2021 | 90 | biwc |
| Matijašević · Cukundeda | 2021 | 90 | biwc |
| Matijašević · 7 hrastova cuvee belo | 2022 | 90 | biwc |
| Despotika · Trag | 2022 | 90 | biwc |
| Despotika · Nemir rosé | 2024 | 89 | Falstaff |
| Despotika · Dodir Tamjanika | 2022 | 89 | Falstaff |
| Despotika · Nemir | 2024 | 89 | Falstaff |
| Despotika · Dodir (Touch) Tamjanika | 2022 | 89 | Falstaff |
| Despotika · Trag | 2015 | 89 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2012 | 89 | decanter |
| Despotika · Krunski Dokaz Cabernet Sauvignon | 2015 | 89 | decanter |
| Aleksandrović · Trijumf Terroir | 2018 | 89 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2016 | 89 | decanter |
| Tarpoš · Lipar | 2021 | 89 | decanter |
| Tarpoš · Chardonnay | 2022 | 89 | decanter |
| Despotika · Dokaz | 2019 | 89 | decanter |
| Despotika · Nemir | 2022 | 89 | biwc |
| Matijašević · Belina | 2021 | 89 | biwc |
| Matijašević · Belina Oranz | 2020 | 89 | biwc |
| Despotika · Dokaz | 2019 | 89 | biwc |
| Despotika · Beskraj | 2023 | 89 | biwc |
| Tarpoš · Sauvignon Blanc | 2023 | 89 | biwc |
| Despotika · Nemir | 2024 | 89 | biwc |
| Despotika · Morava | 2023 | 89 | biwc |
| Despotika · Morava | 2024 | 89 | biwc |
| Despotika · Morava Glina | 2024 | 89 | biwc |
| Despotika · Zmajeviti | 2024 | 89 | biwc |
| Arsenijević · Sauvignon | 2025 | 89 | biwc |
| Despotika · Morava | 2023 | 88 | awc-vienna |
| Radovanović · 25 Reserve Cabernet Sauvignon | 2012 | 88 | decanter |
| Radovanović · Chardonnay Selekcija | 2013 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2012 | 88 | decanter |
| Despotika · Trag Merlot | 2016 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2017 | 88 | decanter |
| Matijašević · Belina | 2020 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2016 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2017 | 88 | decanter |
| Tarpoš · Merlot | 2017 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2019 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 88 | decanter |
| Despotika · Dokaz Cabernet Sauvignon | 2021 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 88 | decanter |
| Matijašević · Tri Doline Merlot | 2021 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 88 | decanter |
| Despotika · Nemir | 2023 | 88 | biwc |
| Tarpoš · Merlot | 2019 | 88 | biwc |
| Despotika · Svedok | 2022 | 88 | biwc |
| Arsenijević · Prokupac „Starosedelac“ | 2024 | 88 | biwc |
| Despotika · Morava | 2016 | 87 | decanter |
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
| Despotika · Dodir | 2025 | 87 | biwc |
| Aleksandrović · Regent Reserve | 2012 | 86 | decanter |
| Despotika · Trag | 2013 | 86 | decanter |
| Despotika · Morava | 2016 | 86 | decanter |
| Matijašević · Belina | 2019 | 86 | decanter |
| Aleksandrović · Vožd | 2017 | 86 | decanter |
| Aleksandrović · Trijumf Terroir | 2020 | 86 | decanter |
| Tarpoš · Tamjanika | 2021 | 86 | decanter |
| Tarpoš · Rosé | 2021 | 86 | decanter |
| Matijašević · 7 Hrastova Cuvée | 2021 | 86 | decanter |
| Despotika · Trag | 2021 | 86 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 86 | decanter |
| Despotika · Nemir | 2023 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2020 | 86 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 86 | decanter |
| Matijašević · Cukundeda | 2020 | 86 | biwc |
| Tarpoš · Cabernet Sauvignon | 2017 | 86 | biwc |
| Tarpoš · Chardonnay | 2022 | 86 | biwc |
| Tarpoš · Tamjanika | 2022 | 86 | biwc |
| Despotika · Dokaz | 2018 | 86 | biwc |
| Despotika · Dokaz | 2021 | 86 | biwc |
| Despotika · Nebo | 2024 | 86 | biwc |
| Arsenijević · Tamjanika „Starosedelac“ | 2025 | 86 | biwc |
| Despotika · Zmajeviti | 2015 | 85 | decanter |
| Despotika · Nebo | 2017 | 85 | decanter |
| Arsenijević · Cabernet Sauvignon | 2019 | 85 | biwc |
| Despotika · Beskraj | 2021 | 85 | biwc |
| Despotika · Dokaz | 2020 | 85 | biwc |
| Tarpoš · Tamjanika | 2023 | 85 | biwc |
| Matijašević · Belina | 2022 | 85 | biwc |
| Despotika · Beskraj | 2024 | 85 | biwc |
| Despotika · Dodir | 2025 | 85 | biwc |
| Aleksandrović · Trijumf Selection | 2016 | 84 | decanter |
| Despotika · Morava | 2021 | 84 | biwc |
| Arsenijević · Sauvignon Blanc | 2022 | 84 | biwc |
| Despotika · Nebo | 2025 | 84 | biwc |
| Aleksandrović · Trijumf Noir | 2012 | 83 | decanter |
| Aleksandrović · Trijumf Gold | 2015 | 83 | decanter |
| Despotika · Krunski Dokaz | 2015 | 83 | decanter |
| Arsenijević · Starosedelac | 2021 | 83 | biwc |
| Tarpoš · Syrah | 2022 | 81 | biwc |
| Despotika · Dodir | 2022 | 81 | biwc |
| Despotika · Nebo | 2022 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Marko · Doajen Chardonnay 2024 | 
| 2026 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2021 | 
| 2026 | бронза | bronza | Matijašević · Tri Doline Merlot 2021 | 
| 2026 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2026 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2018 | 
| 2026 | бронза | bronza | Marko · Carine Merlot-Cabernet Sauvignon 2020 | 
| 2026 | бронза | bronza | Aleksandrović · Trijumf Noir Brut 2022 | 
| 2026 | бронза | bronza | Despotika · Nebo 2025 | 
| 2026 | золото | zlato | Tarpoš · Chardonnay Extra Brut 2021 | 
| 2026 | золото | zlato | Despotika · Morava 2024 | 
| 2026 | золото | zlato | Despotika · Morava Glina 2024 | 
| 2026 | золото | zlato | Despotika · Trag 2022 | 
| 2026 | золото | zlato | Despotika · Neizbrisivi trag 2021 | 
| 2026 | золото | zlato | Despotika · Zmajeviti 2024 | 
| 2026 | золото | zlato | Arsenijević · Sauvignon 2025 | 
| 2026 | одобрение | approval | Despotika · Morava 2023 | 
| 2026 | платина | platina | Aleksandrović · Kameničarka Prokupac 2022 | 
| 2026 | платина | platina | Arsenijević · Kaberne 2021 | 
| 2026 | серебро | srebro | Matijašević · Belina 2022 | 
| 2026 | серебро | srebro | Despotika · Dodir 2025 | 
| 2026 | серебро | srebro | Despotika · Svedok 2022 | 
| 2026 | серебро | srebro | Arsenijević · Tamjanika „Starosedelac“ 2025 | 
| 2026 | серебро | srebro | Arsenijević · Prokupac „Starosedelac“ 2024 | 
| 2025 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2018 | 
| 2025 | бронза | bronza | Tarpoš · Merlot 2021 | 
| 2025 | бронза | bronza | Despotika · Dokaz Cabernet Sauvignon 2021 | 
| 2025 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2020 | 
| 2025 | бронза | bronza | Tarpoš · Chardonnay Extra Brut 2021 | 
| 2025 | золото | zlato | Tarpoš · Prokupac 2023 | 
| 2025 | золото | zlato | Despotika · Krunski Dokaz 2017 | 
| 2025 | золото | zlato | Despotika · Nemir 2024 | 
| 2025 | золото | zlato | Despotika · Morava 2023 | 
| 2025 | лучшее белое, международные сорта | 1 | Matijašević · SoviNoa Fumé Blanc 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Trijumf Gold 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2025 | серебро | srebro | Aleksandrović · Regent Reserve 2020 | 
| 2025 | серебро | srebro | Despotika · Barik Morava 2022 | 
| 2025 | серебро | srebro | Aleksandrović · Trijumf Rosé Brut 2019 | 
| 2025 | серебро | srebro | Despotika · Beskraj 2024 | 
| 2025 | серебро | srebro | Despotika · Nebo 2024 | 
| 2025 | серебро | srebro | Despotika · Dodir 2025 | 
| 2024 | TROPHY SEMI DRY WINE | trofej | Despotika · Nebo 2023 | 
| 2024 | бронза | bronza | Despotika · Trag 2021 | 
| 2024 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2021 | 
| 2024 | бронза | bronza | Despotika · Morava 2022 | 
| 2024 | бронза | bronza | Tarpoš · Sauvignon Blanc 2023 | 
| 2024 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2019 | 
| 2024 | бронза | bronza | Despotika · Dokaz 2019 | 
| 2024 | бронза | bronza | Despotika · Nemir 2023 | 
| 2024 | двойное золото | dvojno-zlato | Tarpoš · Merlot 2021 | 
| 2024 | золото | zlato | Aleksandrović · Vožd Cabernet Sauvignon 2017 | 
| 2024 | золото | zlato | Despotika · Nebo 2023 | 
| 2024 | золото | zlato | Despotika · Morava 2022 | 
| 2024 | золото | zlato | Despotika · Beskraj 2023 | 
| 2024 | золото | zlato | Tarpoš · Sauvignon Blanc 2023 | 
| 2024 | золото | zlato | Tarpoš · Cabernet Sauvignon 2021 | 
| 2024 | золото | zlato | Matijašević · Cukundeda 2021 | 
| 2024 | золото | zlato | Matijašević · 7 hrastova cuvee belo 2022 | 
| 2024 | лучшая молодая винодельня | 1 | Draganić | 
| 2024 | лучшее красное, международные сорта | 1 | Arsenijević · Cabernet Sauvignon 2020 | 
| 2024 | лучшее красное, местные сорта | 1 | Marko · Doajen Prokupac 2022 | 
| 2024 | серебро | srebro | Aleksandrović · Prokupac 2020 | 
| 2024 | серебро | srebro | Matijašević · Cukundeda Prokupac 2021 | 
| 2024 | серебро | srebro | Tarpoš · Tamjanika 2023 | 
| 2024 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2024 | серебро | srebro | Aleksandrović · Regent Reserve 2019 | 
| 2024 | серебро | srebro | Despotika · Nemir 2023 | 
| 2024 | серебро | srebro | Despotika · Dokaz 2020 | 
| 2024 | серебро | srebro | Despotika · Dokaz 2021 | 
| 2024 | серебро | srebro | Tarpoš · Tamjanika 2023 | 
| 2024 | серебро | srebro | Tarpoš · Merlot 2019 | 
| 2024 | серебро | srebro | Matijašević · Belina 2022 | 
| 2023 | Best Semi Dry Wine Trophy | trofej | Despotika · Nemir 2022 | 
| 2023 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2017 | 
| 2023 | бронза | bronza | Tarpoš · Merlot 2017 | 
| 2023 | бронза | bronza | Tarpoš · Chardonnay 2022 | 
| 2023 | бронза | bronza | Matijašević · 7 Hrastova Cuvée 2021 | 
| 2023 | бронза | bronza | Tarpoš · Syrah 2022 | 
| 2023 | бронза | bronza | Despotika · Dodir 2022 | 
| 2023 | бронза | bronza | Despotika · Nebo 2022 | 
| 2023 | бронза | bronza | Despotika · Morava 2021 | 
| 2023 | бронза | bronza | Arsenijević · Starosedelac 2021 | 
| 2023 | бронза | bronza | Arsenijević · Sauvignon Blanc 2022 | 
| 2023 | золото | zlato | Matijašević · Tri Doline 2020 | 
| 2023 | золото | zlato | Matijašević · Sovinoa Fumé Blanc 2021 | 
| 2023 | золото | zlato | Matijašević · Belina 2021 | 
| 2023 | золото | zlato | Matijašević · Belina Oranz 2020 | 
| 2023 | золото | zlato | Despotika · Dokaz 2019 | 
| 2023 | лучшее красное | 1 | Radovanović · Cabernet Sauvignon Grand Reserva 2017 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Matijašević · Belina 2021 | 
| 2023 | серебро | srebro | Matijašević · Sovinoa Sauvignon Blanc 2021 | 
| 2023 | серебро | srebro | Matijašević · Cukundeda 2020 | 
| 2023 | серебро | srebro | Tarpoš · Cabernet Sauvignon 2017 | 
| 2023 | серебро | srebro | Tarpoš · Chardonnay 2022 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Arsenijević · Cabernet Sauvignon 2019 | 
| 2023 | серебро | srebro | Despotika · Beskraj 2021 | 
| 2023 | серебро | srebro | Despotika · Dokaz 2018 | 
| 2022 | бронза | bronza | Matijašević · Belina 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Trijumf Terroir 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2022 | бронза | bronza | Tarpoš · Lipar 2021 | 
| 2022 | бронза | bronza | Tarpoš · Tamjanika 2021 | 
| 2022 | бронза | bronza | Tarpoš · Rosé 2021 | 
| 2022 | бронза | bronza | Matijašević · Rock&Rose 2021 | 
| 2022 | бронза | bronza | Matijašević · Belina Oranz 2020 | 
| 2022 | двойное золото | dvojno-zlato | Matijašević · Sovinoa Fumé Blanc 2020 | 
| 2022 | двойное золото | dvojno-zlato | Aleksandrović · Trijumf Noir Brut 2010 | 
| 2022 | двойное золото | dvojno-zlato | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2022 | золото | zlato | Matijašević · SoviNoa Fumé Blanc 2020 | 
| 2022 | золото | zlato | Aleksandrović · Regent Reserve 2018 | 
| 2022 | золото | zlato | Aleksandrović · Regent Reserve 2018 | 
| 2022 | золото | zlato | Aleksandrović · Trijumf Gold 2021 | 
| 2022 | золото | zlato | Aleksandrović · Vožd 2017 | 
| 2022 | золото | zlato | Aleksandrović · Trijumf Terroir 2020 | 
| 2022 | золото | zlato | Despotika · Trag 2019 | 
| 2022 | золото | zlato | Despotika · Morava 2020 | 
| 2022 | золото | zlato | Despotika · Beskraj 2021 | 
| 2022 | золото | zlato | Despotika · Morava kasna berba 2020 | 
| 2022 | золото | zlato | Matijašević · Tri doline 2020 | 
| 2022 | серебро | srebro | Aleksandrović · Trijumf Gold 2020 | 
| 2022 | серебро | srebro | Matijašević · Sovinoa Sauvignon Blanc 2020 | 
| 2022 | серебро | srebro | Matijašević · Čukundeda Prokupac 2019 | 
| 2022 | серебро | srebro | Matijašević · Čukundeda Superiore 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Prokupac 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Vožd Cabernet Sauvignon 2017 | 
| 2022 | серебро | srebro | Tarpoš · Menuet 2021 | 
| 2022 | серебро | srebro | Tarpoš · 1804 2015 | 
| 2022 | серебро | srebro | Despotika · Dokaz 2019 | 
| 2022 | серебро | srebro | Despotika · Nemir 2021 | 
| 2022 | серебро | srebro | Matijašević · Belina 2020 | 
| 2022 | серебро | srebro | Matijašević · 7 hrastova cuvee belo 2020 | 
| 2022 | серебро | srebro | Matijašević · Čukundeda 2020 | 
| 2021 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2021 | бронза | bronza | Matijašević · Rock & Rose 2019 | 
| 2021 | бронза | bronza | Matijašević · Belina 2019 | 
| 2021 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2021 | бронза | bronza | Aleksandrović · Regent Reserve 2017 | 
| 2021 | бронза | bronza | Aleksandrović · Vožd 2017 | 
| 2021 | бронза | bronza | Aleksandrović · Vožd 2017 | 
| 2021 | бронза | bronza | Despotika · Krunski Dokaz 2017 | 
| 2021 | двойное золото | dvojno-zlato | Aleksandrović · Prokupac 2018 | 
| 2021 | золото | zlato | Matijašević · SoviNoa 2019 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Selection 2020 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Gold 2019 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Gold 2020 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Terroir 2018 | 
| 2021 | золото | zlato | Despotika · Dokaz 2018 | 
| 2021 | золото | zlato | Despotika · Nemir 2020 | 
| 2021 | золото | zlato | Matijašević · Belina 2019 | 
| 2021 | золото | zlato | Matijašević · Cukundeda 2019 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Noir 2010 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Gold 2019 | 
| 2021 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2021 | серебро | srebro | Despotika · Beskraj 2020 | 
| 2021 | серебро | srebro | Despotika · Nebo barrique 2019 | 
| 2021 | серебро | srebro | Matijašević · SoviNoa 2019 | 
| 2021 | серебро | srebro | Matijašević · Rock & Rose 2019 | 
| 2020 | Grand Trophy | trofej | Aleksandrović · Trijumf Selection 2019 | 
| 2020 | White Wine Trophy | trofej | Aleksandrović · Trijumf Selection 2019 | 
| 2020 | бронза | bronza | Despotika · Zmajeviti 2017 | 
| 2020 | бронза | bronza | Despotika · Krunski Dokaz Cabernet Sauvignon 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Regent Reserve 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2020 | бронза | bronza | Matijašević · Rock & Rose 2019 | 
| 2020 | бронза | bronza | Matijašević · SoviNoa 2019 | 
| 2020 | бронза | bronza | Aleksandrović · Trijumf Rose 2019 | 
| 2020 | двойное золото | dvojno-zlato | Aleksandrović · Trijumf Terroir 2018 | 
| 2020 | золото | zlato | Despotika · Krunski Dokaz 2015 | 
| 2020 | золото | zlato | Despotika · Zmajeviti 2017 | 
| 2020 | золото | zlato | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2020 | золото | zlato | Aleksandrović · Rodoslov Grand Reserve 2009 | 
| 2020 | золото | zlato | Aleksandrović · Trijumf Gold 2019 | 
| 2020 | лучшее красное | 1 | Radovanović · Rèserve Cabernet Sauvignon 2017 | 
| 2020 | отмечено | commended | Despotika · Nebo 2017 | 
| 2020 | серебро | srebro | Despotika · Trag 2017 | 
| 2020 | серебро | srebro | Aleksandrović · Vizija Selection 2016 | 
| 2020 | серебро | srebro | Aleksandrović · Trijumf Gold 2018 | 
| 2020 | серебро | srebro | Despotika · Trag 2017 | 
| 2020 | серебро | srebro | Despotika · Beskraj 2019 | 
| 2020 | серебро | srebro | Aleksandrović · Vožd 2018 | 
| 2020 | серебро | srebro | Aleksandrović · Regent Reserve 2016 | 
| 2019 | двойное золото | dvojno-zlato | Aleksandrović · Trijumf Gold 2018 | 
| 2019 | двойное золото | dvojno-zlato | Despotika · Dodir 2018 | 
| 2019 | двойное золото | dvojno-zlato | Despotika · Beskraj 2017 | 
| 2019 | серебро | srebro | Despotika · Dokaz 2016 | 
| 2019 | серебро | srebro | Despotika · Nebo 2018 | 
| 2018 | бронза | bronza | Despotika · Nebo Riesling-Pinot Blanc 2016 | 
| 2018 | бронза | bronza | Despotika · Morava 2016 | 
| 2018 | бронза | bronza | Despotika · Trag Merlot 2016 | 
| 2018 | бронза | bronza | Despotika · Trag 2016 | 
| 2018 | бронза | bronza | Despotika · Morava 2016 | 
| 2018 | отмечено | commended | Despotika · Krunski Dokaz 2015 | 
| 2018 | серебро | srebro | Despotika · Nebo 2017 | 
| 2018 | серебро | srebro | Despotika · Dodir 2017 | 
| 2018 | серебро | srebro | Despotika · Zmajeviti 2016 | 
| 2017 | бронза | bronza | Despotika · Morava 2016 | 
| 2017 | бронза | bronza | Despotika · Trag 2015 | 
| 2017 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2017 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2012 | 
| 2017 | бронза | bronza | Despotika · Zmajeviti Prokupac 2015 | 
| 2017 | бронза | bronza | Despotika · Beskraj Sovinjon Beli 2016 | 
| 2017 | отмечено | commended | Aleksandrović · Trijumf Selection 2016 | 
| 2017 | отмечено | commended | Aleksandrović · Trijumf Gold 2015 | 
| 2017 | отмечено | commended | Despotika · Zmajeviti 2015 | 
| 2017 | серебро | srebro | Despotika · Dokaz 2015 | 
| 2017 | серебро | srebro | Aleksandrović · Vizija 2015 | 
| 2017 | серебро | srebro | Despotika · Dokaz Cabernet Sauvignon 2015 | 
| 2016 | бронза | bronza | Aleksandrović · Trijumf Noir 2012 | 
| 2016 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2016 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2016 | бронза | bronza | Radovanović · 25 Reserve Cabernet Sauvignon 2012 | 
| 2016 | бронза | bronza | Despotika · Trag 2013 | 
| 2016 | бронза | bronza | Radovanović · Chardonnay Selekcija 2013 | 
| 2016 | бронза | bronza | Despotika · BESKRAJ Sauvignon Blanc 2015 | 
| 2016 | бронза | bronza | Despotika · MORAVA 2015 | 
| 2016 | отмечено | commended | Aleksandrović · Trijumf Noir 2012 | 
| 2016 | серебро | srebro | Aleksandrović · Trijumf Barrique 2012 | 
| 2016 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2009 | 
| 2016 | серебро | srebro | Despotika · DODIR Muscat Ottonel Tamjanika 2015 | 
| 2016 | серебро | srebro | Despotika · DOKAZ Cabernet Sauvignon 2013 | 
| 2015 | бронза | bronza | Aleksandrović · Trijumf Selection 2013 | 
| 2015 | бронза | bronza | Aleksandrović · Regent Reserve 2009 | 
| 2015 | бронза | bronza | Aleksandrović · Trijumf 2013 | 
| 2015 | бронза | bronza | Aleksandrović · Trijumf Barrique 2012 | 
| 2015 | бронза | bronza | Despotika · Dokaz 2012 | 
| 2015 | бронза | bronza | Aleksandrović · Regent 2009 | 
| 2015 | бронза | bronza | Despotika · Morava 2014 | 
| 2015 | золото | zlato | Despotika · Dokaz Cabernet Sauvignon 2012 | 
| 2015 | отмечено | commended | Aleksandrović · Trijumf Gold 2012 | 
| 2015 | отмечено | commended | Aleksandrović · Trijumf Noir 2012 | 
| 2015 | серебро | srebro | Aleksandrović · Trijumf Barrique 2012 | 
| 2015 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2009 | 
| 2015 | серебро | srebro | Aleksandrović · Rodoslov 2009 | 
| 2015 | серебро | srebro | Despotika · Drag Merlot 2013 | 
| 2014 | бронза | bronza | Aleksandrović · Regent 2009 | 
| 2014 | бронза | bronza | Aleksandrović · Rodoslov 2006 | 
| 2014 | бронза | bronza | Aleksandrović · Trijumf Noir 2009 | 
| 2014 | бронза | bronza | Aleksandrović · Trijumf Noir 2012 | 
| 2014 | бронза | bronza | Aleksandrović · Rodoslov 2006 | 
| 2014 | золото | zlato | Aleksandrović · Trijumf Noir 2009 | 
| 2014 | отмечено | commended | Aleksandrović · Trijumf Gold 2012 | 
| 2014 | отмечено | commended | Aleksandrović · Regent 2008 | 
| 2014 | отмечено | commended | Aleksandrović · Trijumf Barrique 2012 | 
| 2014 | отмечено | commended | Aleksandrović · Regent Reserve 2009 | 
| 2014 | отмечено | commended | Aleksandrović · Trijumf Noir 2009 | 
| 2014 | отмечено | commended | Aleksandrović · Trijumf Noir 2009 | 
| 2014 | серебро | srebro | Aleksandrović · Trijumf Barrique 2012 | 
| 2014 | серебро | srebro | Aleksandrović · Trijumf Gold 2012 | 
| 2014 | серебро | srebro | Aleksandrović · Trijumf Gold 2012 | 
| 2014 | серебро | srebro | Aleksandrović · Regent Reserve 2009 | 
| 2013 | бронза | bronza | Aleksandrović · Rodoslov Reserve 2006 | 
| 2013 | бронза | bronza | Radovanović · Rèserve Cabernet Sauvignon 2009 | 
| 2013 | бронза | bronza | Radovanović · Chardonnay Selekcija 2011 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf 2011 | 
| 2013 | отмечено | commended | Aleksandrović · Harizma 2011 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf Noir 2009 | 
| 2013 | отмечено | commended | Aleksandrović · Regent 2008 | 
| 2013 | отмечено | commended | Aleksandrović · Rodoslov 2006 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf 2010 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf Noir 2009 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf 2011 | 
| 2013 | отмечено | commended | Aleksandrović · Trijumf Selection 2011 | 
| 2013 | отмечено | commended | Aleksandrović · Harizma 2011 | 
| 2013 | серебро | srebro | Aleksandrović · Trijumf 2010 | 
| 2013 | серебро | srebro | Aleksandrović · Trijumf Barrique 2009 | 
| 2013 | серебро | srebro | Aleksandrović · Regent Reserve 2008 | 
| 2013 | серебро | srebro | Aleksandrović · Trijumf Barrique 2009 | 
| 2012 | бронза | bronza | Aleksandrović · Trijumf Noir 2008 | 
| 2012 | бронза | bronza | Aleksandrović · Trijumf Barrique 2009 | 
| 2012 | бронза | bronza | Aleksandrović · Harizma 2009 | 
| 2012 | бронза | bronza | Aleksandrović · Oplen 2010 | 
| 2012 | бронза | bronza | Aleksandrović · Trijumf Selection 2010 | 
| 2012 | отмечено | commended | Aleksandrović · Trijumf Rose 2010 | 
| 2012 | отмечено | commended | Aleksandrović · Vizija 2008 | 
| 2012 | отмечено | commended | Radovanović · Rèserve Cabernet Sauvignon 2008 | 
| 2012 | отмечено | commended | Aleksandrović · Rodoslov Reserve 2006 | 
| 2012 | отмечено | commended | Radovanović · PinoAs 2010 | 
| 2012 | серебро | srebro | Aleksandrović · Oplen 2010 | 
| 2012 | серебро | srebro | Aleksandrović · Harizma 2009 | 
| 2011 | бронза | bronza | Radovanović · Rèserve Cabernet Sauvignon 2008 | 
| 2011 | бронза | bronza | Aleksandrović · Trijumf 2009 | 
| 2011 | бронза | bronza | Aleksandrović · Harizma 2009 | 
| 2011 | бронза | bronza | Aleksandrović · Harizma 2008 | 
| 2011 | отмечено | commended | Aleksandrović · Trijumf Noir 2008 | 
| 2011 | отмечено | commended | Radovanović · Pinoas 2010 | 
| 2011 | отмечено | commended | Aleksandrović · Oplen 2009 | 
| 2011 | отмечено | commended | Aleksandrović · Regent Reserve 2007 | 
| 2011 | отмечено | commended | Aleksandrović · Regent 2007 | 
| 2011 | отмечено | commended | Aleksandrović · Trijumf Barrique 2007 | 
| 2011 | серебро | srebro | Aleksandrović · Trijumf Barrique 2007 | 
| 2011 | серебро | srebro | Radovanović · Chardonnay Selekcija 2009 | 
| 2011 | серебро | srebro | Radovanović · Rèserve Cabernet Sauvignon 2008 | 
| 2010 | бронза | bronza | Aleksandrović · Trijumf Barrique 2007 | 
| 2010 | отмечено | commended | Aleksandrović · Regent 2007 | 
| 2010 | отмечено | commended | Aleksandrović · Harizma 2008 | 
| 2010 | отмечено | commended | Aleksandrović · Regent 2007 | 
| 2010 | отмечено | commended | Aleksandrović · Vizija Balavaud 2006 | 
| 2010 | серебро | srebro | Aleksandrović · Trijumf 2008 | 
| 2009 | бронза | bronza | Aleksandrović · Trijumf Barrique 2006 | 
| 2009 | бронза | bronza | Aleksandrović · Trijumf Noir 2006 | 
| 2009 | бронза | bronza | Aleksandrović · Trijumf Barrique 2006 | 

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
| Ralević · RaRa Tamjanika PETNAT | 2024 | 95 | biwc |
| Temet · Tri Morave Crveno Reserve | 2009 | 94 | Falstaff |
| Ivanović · No 1/2 | 2019 | 94 | vino.rs |
| Temet · Tri Morave Crveno Reserve | 2019 | 94 | Falstaff |
| Budimir · Svb Rosa | 2009 | 94 | Falstaff |
| Ivanović · No ½ | 2018 | 94 | Falstaff |
| Ivanović · Prokupac | 2017 | 94 | Falstaff |
| Radovan · Prokupac Radovan 100% | 2020 | 94 | Falstaff |
| Temet · Ergo | 2018 | 94 | decanter |
| Temet · Beli Kamen Merlot | 2019 | 94 | decanter |
| Ralević · Virgo | 2021 | 94 | biwc |
| Radovan · 100% Prokupac | 2019 | 93 | Falstaff |
| Radovan · Tamjanika Radovan 100% | 2022 | 93 | Falstaff |
| Radovan · Tamjanika Radovon 100% | 2022 | 93 | Falstaff |
| Radovan · Experiment Prokupac | 2019 | 93 | Falstaff |
| Temet · Tri Morave Reserve | 2018 | 93 | decanter |
| Spasić · Tamjanika | 2021 | 92 | Falstaff |
| Cilić · Onyx Blanc | 2019 | 92 | Falstaff |
| Budimir · Angel | 2016 | 92 | Falstaff |
| Ivanović · Zanos | 2015 | 92 | Falstaff |
| Budimir · Lila Prokupac Boje | 2012 | 92 | Falstaff |
| Ivanović · Tamjanika | 2022 | 92 | Falstaff |
| Ivanović · No 3/4 Tamjanika | 2021 | 92 | Falstaff |
| Ivanović · Prokupac | 2021 | 92 | Falstaff |
| Radovan · Experiment Prokupac | 2018 | 92 | Falstaff |
| Radovan · Experiment Tamjanika | 2022 | 92 | Falstaff |
| Rubin · Rubinov Prokupac | 2017 | 92 | decanter |
| Temet · Ergo | 2018 | 92 | decanter |
| Radovan · Experiment Prokupac | 2019 | 92 | decanter |
| Vinarija Jovac · Cabernet Sauvignon | 2020 | 92 | decanter |
| Ralević · VIRGO Tamjanika | 2024 | 92 | biwc |
| Ivanović · Jara Pet Net | 2022 | 91 | Falstaff |
| Radovan · Experiment Prokupac | 2015 | 91 | decanter |
| Temet · Ergo | 2016 | 91 | decanter |
| Radovan · 100% Prokupac | 2020 | 91 | decanter |
| Temet · Ergo | 2018 | 91 | decanter |
| Temet · White Stone Merlot | 2017 | 91 | decanter |
| Rubin · Aurora | 2019 | 90 | gilbert-gaillard |
| Temet · Tri Morave | 2017 | 90 | decanter |
| Radovan · Prokupac | 2015 | 90 | decanter |
| Temet · Tri Morave Reserve | 2017 | 90 | decanter |
| Temet · Tri Morave Reserve | 2019 | 90 | decanter |
| Temet · Ergo | 2018 | 90 | decanter |
| Temet · Tri Morave Reserve | 2019 | 90 | decanter |
| Ivanović · No 1/2 | 2019 | 90 | decanter |
| Temet · Tri Morave | 2019 | 90 | decanter |
| Temet · Tri Morave Reserve | 2021 | 90 | decanter |
| Radovan · 100% Prokupac | 2023 | 90 | decanter |
| Temet · Ergo | 2019 | 90 | decanter |
| Vinarija Jovac · Merlot | 2020 | 90 | decanter |
| Temet · Ergo Rosé | 2019 | 90 | decanter |
| Ralević · Aurum | 2020 | 90 | biwc |
| Radovan · Experiment Prokupac | 2016 | 89 | decanter |
| Temet · Ergo White | 2016 | 89 | decanter |
| Temet · Tri Morave | 2017 | 89 | decanter |
| Temet · Tri Morave Brut | 2017 | 89 | decanter |
| Temet · Beli Kamen Merlot | 2018 | 89 | decanter |
| Temet · Tri Morave Red | 2019 | 89 | decanter |
| Temet · Ergo | 2017 | 89 | decanter |
| Vinarija Jovac · Cabernet Sauvignon | 2020 | 89 | decanter |
| Temet · Tri Morave Reserve | 2021 | 89 | decanter |
| Ivanović · No 1/2 | 2019 | 89 | biwc |
| Ralević · Vranac | 2020 | 89 | biwc |
| Ivanović · Tamjanika | 2023 | 89 | biwc |
| Ivanović · Prokupac | 2022 | 89 | biwc |
| Ivanović · No ½ | 2019 | 89 | biwc |
| Ivanović · JARA Pet Nat | 2025 | 89 | biwc |
| Ivanović · Prokupac | 2024 | 89 | biwc |
| Ivanović · No ½ | 2021 | 89 | biwc |
| Rubin · Carmen | 2019 | 88 | gilbert-gaillard |
| Temet · Ergo White | 2015 | 88 | decanter |
| Temet · Tri Morave | 2016 | 88 | decanter |
| Temet · Ergo | 2016 | 88 | decanter |
| Temet · Tri Morave | 2018 | 88 | decanter |
| Temet · Ergo | 2017 | 88 | decanter |
| Temet · Tri Morave | 2019 | 88 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 88 | decanter |
| Temet · Burgundac Sivi | 2019 | 88 | decanter |
| Temet · Tri Morave Reserve | 2019 | 88 | decanter |
| Temet · Ergo | 2019 | 88 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 88 | decanter |
| Temet · Ergo | 2018 | 88 | decanter |
| Ralević · Cabernet sauvignon | 2018 | 88 | biwc |
| Temet · Tri Morave | 2015 | 87 | decanter |
| Temet · Tri Morave Rosé | 2015 | 87 | decanter |
| Temet · Tri Morave Red | 2015 | 87 | decanter |
| Ivanović · Prokupac | 2016 | 87 | decanter |
| Temet · Tri Morave | 2017 | 87 | decanter |
| Radovan · Experiment Prokupac | 2017 | 87 | decanter |
| Rubin · Amante Carmen | 2016 | 87 | decanter |
| Rubin · Cabernet Sauvignon | 2016 | 87 | decanter |
| Temet · Pinot Grigio | 2018 | 87 | decanter |
| Temet · Ergo | 2017 | 87 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 87 | decanter |
| Temet · Tri Morave | 2020 | 87 | decanter |
| Rubin · Sauvignon Blanc | 2019 | 87 | decanter |
| Temet · Ergo | 2018 | 87 | decanter |
| Rubin · Prokupac | 2018 | 87 | decanter |
| Vinarija Jovac · Tamjanika | 2021 | 87 | decanter |
| Rubin · Amante Matea Merlot | 2018 | 87 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 87 | decanter |
| Temet · Beli Kamen Prokupac | 2019 | 87 | decanter |
| Vinarija Jovac · Merlot | 2020 | 87 | decanter |
| Temet · Tri Morave Reserve | 2019 | 87 | decanter |
| Temet · White Stone Syrah | 2017 | 87 | decanter |
| Ralević · RARA PETNAT Tamjanika | 2025 | 87 | biwc |
| Ralević · ETER Chardonnay | 2020 | 87 | biwc |
| Temet · Tri Morave | 2015 | 86 | decanter |
| Temet · Tri Morave White | 2016 | 86 | decanter |
| Temet · Ergo | 2016 | 86 | decanter |
| Temet · Pinot Grigio | 2016 | 86 | decanter |
| Temet · Tri Morave | 2016 | 86 | decanter |
| Ivanović · No 1/2 | 2015 | 86 | decanter |
| Temet · Tri Morave | 2019 | 86 | decanter |
| Temet · Tri Morave | 2018 | 86 | decanter |
| Temet · Ergo | 2017 | 86 | decanter |
| Rubin · Amante Matea | 2018 | 86 | decanter |
| Temet · Tri Morave Reserve | 2017 | 86 | decanter |
| Temet · Beli Kamen Syrah | 2019 | 86 | decanter |
| Vinarija Jovac · Merlot | 2020 | 86 | decanter |
| Ivanović · No 3/4 | 2023 | 86 | decanter |
| Ralević · Tamjanika | 2022 | 86 | biwc |
| Temet · Tri Morave Belo Penušavo Brut | 2014 | 85 | decanter |
| Temet · Ergo Red | 2015 | 85 | decanter |
| Radovan · 100% Prokupac | 2017 | 85 | decanter |
| Ivanović · No ¾ | 2023 | 85 | biwc |
| Ivanović · No ½ | 2020 | 85 | biwc |
| Ivanović · Tamjanika | 2024 | 85 | biwc |
| Temet · Dobra Godina | 2011 | 84 | decanter |
| Temet · Ergo Red | 2013 | 84 | decanter |
| Temet · Ergo Blush | 2015 | 84 | decanter |
| Ivanović · Prokupac | 2016 | 84 | decanter |
| Rubin · Merlot | 2017 | 84 | decanter |
| Rubin · Amante Carmen Prokupac-Marselan-Merlot | 2016 | 84 | decanter |
| Ralević · VIRGO Sauvignon blanc | 2021 | 84 | biwc |
| Radovan · 100% Prokupac | 2023 | 84 | biwc |
| Radovan · 100% Zuplianka | 2023 | 84 | biwc |
| Ivanović · ЦФ | 2025 | 84 | biwc |
| Temet · Pinot Grigio | 2014 | 83 | decanter |
| Ralević · Chardonnay | 2020 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | Best of Show Serbia | trofej | Ralević · Virgo Sauvignon Blanc 2021 | 
| 2026 | бронза | bronza | Temet · Tri Morave Reserve 2021 | 
| 2026 | бронза | bronza | Temet · Tri Morave Reserve 2019 | 
| 2026 | бронза | bronza | Temet · Ergo 2018 | 
| 2026 | бронза | bronza | Temet · White Stone Syrah 2017 | 
| 2026 | бронза | bronza | Ivanović · ЦФ 2025 | 
| 2026 | двойное золото | dvojno-zlato | Ralević · Virgo 2021 | 
| 2026 | золото | zlato | Vinarija Jovac · Stella Noir 2020 | 
| 2026 | золото | zlato | Ivanović · JARA Pet Nat 2025 | 
| 2026 | золото | zlato | Ivanović · Prokupac 2024 | 
| 2026 | золото | zlato | Ivanović · No ½ 2021 | 
| 2026 | золото | zlato | Ralević · VIRGO Tamjanika 2024 | 
| 2026 | серебро | srebro | Temet · Ergo 2019 | 
| 2026 | серебро | srebro | Vinarija Jovac · Merlot 2020 | 
| 2026 | серебро | srebro | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2026 | серебро | srebro | Temet · White Stone Merlot 2017 | 
| 2026 | серебро | srebro | Temet · Ergo Rosé 2019 | 
| 2026 | серебро | srebro | Ivanović · Tamjanika 2024 | 
| 2026 | серебро | srebro | Ralević · RARA PETNAT Tamjanika 2025 | 
| 2026 | серебро | srebro | Ralević · ETER Chardonnay 2020 | 
| 2025 | бронза | bronza | Ivanović · No 3/4 2023 | 
| 2025 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2025 | бронза | bronza | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2025 | бронза | bronza | Ralević · VIRGO Sauvignon blanc 2021 | 
| 2025 | бронза | bronza | Radovan · 100% Prokupac 2023 | 
| 2025 | бронза | bronza | Radovan · 100% Zuplianka 2023 | 
| 2025 | вклад в сербское виноделие | 1 | Radovan | 
| 2025 | двойное золото | dvojno-zlato | Ralević · RaRa Tamjanika PETNAT 2024 | 
| 2025 | золото | zlato | Vinarija Jovac · Stella Noir 2021 | 
| 2025 | золото | zlato | Ivanović · Tamjanika 2023 | 
| 2025 | золото | zlato | Ivanović · Prokupac 2022 | 
| 2025 | золото | zlato | Ivanović · No ½ 2019 | 
| 2025 | лучшая малая винодельня | 1 | Ralević | 
| 2025 | лучшее красное, международные сорта | 1 | Ralević · Aurum 2020 | 
| 2025 | лучшее красное, органика, местные сорта | 1 | Vujić · Gmitar Prokupac 2021 | 
| 2025 | серебро | srebro | Radovan · 100% Prokupac 2023 | 
| 2025 | серебро | srebro | Ralević · Cabernet sauvignon 2018 | 
| 2025 | серебро | srebro | Ivanović · No ¾ 2023 | 
| 2025 | серебро | srebro | Ivanović · No ½ 2020 | 
| 2024 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2024 | бронза | bronza | Rubin · Amante Matea Merlot 2018 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Prokupac 2019 | 
| 2024 | золото | zlato | Ralević · Eter Chardonnay 2019 | 
| 2024 | золото | zlato | Ralević · Aurum 2020 | 
| 2024 | лучшее белое, местные сорта | 1 | Yotta · Hysteresis Tamjanika 2022 | 
| 2024 | лучшее белое, органика, местные сорта | 1 | Ivanović · No 3/4 2023 | 
| 2024 | серебро | srebro | Temet · Tri Morave Reserve 2021 | 
| 2024 | серебро | srebro | Temet · Ergo 2018 | 
| 2024 | серебро | srebro | Radovan · Experiment Prokupac 2019 | 
| 2023 | бронза | bronza | Vinarija Jovac · Tamjanika 2021 | 
| 2023 | бронза | bronza | Temet · Tri Morave Reserve 2019 | 
| 2023 | бронза | bronza | Temet · Beli Kamen Syrah 2019 | 
| 2023 | бронза | bronza | Temet · Ergo 2019 | 
| 2023 | бронза | bronza | Ralević · Chardonnay 2020 | 
| 2023 | золото | zlato | Vinarija Jovac · Stella Noir 2020 | 
| 2023 | золото | zlato | Ivanović · No 1/2 2019 | 
| 2023 | золото | zlato | Ralević · Vranac 2020 | 
| 2023 | серебро | srebro | Temet · Ergo 2018 | 
| 2023 | серебро | srebro | Temet · Tri Morave Reserve 2019 | 
| 2023 | серебро | srebro | Ivanović · No 1/2 2019 | 
| 2023 | серебро | srebro | Temet · Tri Morave 2019 | 
| 2023 | серебро | srebro | Temet · Beli Kamen Merlot 2019 | 
| 2023 | серебро | srebro | Radovan · 100% Prokupac 2020 | 
| 2023 | серебро | srebro | Ralević · Tamjanika 2022 | 
| 2022 | Best Dry Red Wine Trophy | trofej | Ivanović · N 1/2 | 
| 2022 | бронза | bronza | Temet · Tri Morave 2020 | 
| 2022 | бронза | bronza | Temet · Tri Morave Red 2019 | 
| 2022 | бронза | bronza | Temet · Burgundac Sivi 2019 | 
| 2022 | бронза | bronza | Rubin · Sauvignon Blanc 2019 | 
| 2022 | бронза | bronza | Temet · Ergo 2018 | 
| 2022 | бронза | bronza | Rubin · Prokupac 2018 | 
| 2022 | бронза | bronza | Temet · Ergo 2017 | 
| 2022 | золото | zlato | Ivanović · Prokupac 2019 | 
| 2022 | золото | zlato | Ivanović · Tamjanika 2021 | 
| 2022 | золото | zlato | Ivanović · No ½ 2018 | 
| 2022 | лучшее красное | 4 | Budimir · Triada crveno 2020 | 
| 2022 | серебро | srebro | Temet · Tri Morave Reserve 2019 | 
| 2022 | серебро | srebro | Temet · Ergo 2018 | 
| 2022 | серебро | srebro | Temet · Tri Morave Reserve 2018 | 
| 2022 | серебро | srebro | Temet · Ergo 2018 | 
| 2022 | серебро | srebro | Ivanović · No ¾ 2020 | 
| 2021 | бронза | bronza | Rubin · Amante Matea 2018 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Merlot 2018 | 
| 2021 | бронза | bronza | Temet · Ergo 2017 | 
| 2021 | бронза | bronza | Temet · Tri Morave Reserve 2017 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2020 | Orange Wine Trophy | trofej | Temet · Tri Morave reserve white 2017 | 
| 2020 | бронза | bronza | Temet · Ergo 2017 | 
| 2020 | бронза | bronza | Rubin · Cabernet Sauvignon 2016 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2019 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2019 | 
| 2020 | бронза | bronza | Temet · Pinot Grigio 2018 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2018 | 
| 2020 | бронза | bronza | Temet · Ergo 2017 | 
| 2020 | бронза | bronza | Temet · Tri Morave Brut 2017 | 
| 2020 | бронза | bronza | Ralević · RoseRa 2018 | 
| 2020 | бронза | bronza | Ralević · Sauvignon blanc barrel fermented 2018 | 
| 2020 | бронза | bronza | Rubin · Chardonnay 2018 | 
| 2020 | бронза | bronza | Rubin · Amante Carmen 2016 | 
| 2020 | винодельня года | 1 | Temet | 
| 2020 | золото | zlato | Temet · Ergo red 2017 | 
| 2020 | лучшее розе | 1 | Temet · Ergo Rose 2018 | 
| 2020 | отмечено | commended | Rubin · Merlot 2017 | 
| 2020 | отмечено | commended | Rubin · Amante Carmen Prokupac-Marselan-Merlot 2016 | 
| 2020 | серебро | srebro | Temet · Tri Morave Reserve 2017 | 
| 2020 | серебро | srebro | Rubin · Rubinov Prokupac 2017 | 
| 2020 | серебро | srebro | Ralević · Sauvignon blanc 2018 | 
| 2020 | серебро | srebro | Temet · Ergo rose 2018 | 
| 2020 | серебро | srebro | Temet · Ergo Burgundac sivi 2018 | 
| 2020 | серебро | srebro | Temet · Ergo white 2017 | 
| 2020 | серебро | srebro | Temet · Tri Morave reserve red 2017 | 
| 2020 | серебро | srebro | Rubin · Merlot 2017 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2017 | 
| 2019 | бронза | bronza | Radovan · Experiment Prokupac 2017 | 
| 2019 | бронза | bronza | Temet · Ergo White 2016 | 
| 2019 | бронза | bronza | Rubin · Amante Carmen 2016 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2018 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2017 | 
| 2019 | бронза | bronza | Temet · Ergo Red 2016 | 
| 2019 | бронза | bronza | Temet · Tri Morave Red 2017 | 
| 2019 | винодельня года | 1 | Temet | 
| 2019 | золото | zlato | Temet · Tri Morave Reserva 2016 | 
| 2019 | золото | zlato | Temet · Tri Morave sparkling 2017 | 
| 2019 | золото | zlato | Temet · Ergo white 2016 | 
| 2019 | лучшее белое | 1 | Cilić · Onyx Belo 2017 | 
| 2019 | лучшее красное | 1 | Temet · Tri Morave Rezerva Crveno 2016 | 
| 2019 | отмечено | commended | Radovan · 100% Prokupac 2017 | 
| 2019 | отмечено | commended | Ivanović · Prokupac 2016 | 
| 2019 | серебро | srebro | Rubin · Amante Carmen 2016 | 
| 2019 | серебро | srebro | Temet · Ergo 2016 | 
| 2019 | серебро | srebro | Ralević · Sauvignon Blanc 2017 | 
| 2019 | серебро | srebro | Ralević · Cabernet Sauvignon 2017 | 
| 2019 | серебро | srebro | Temet · Tri Morave rose 2018 | 
| 2019 | серебро | srebro | Temet · Tri Morave wihite 2018 | 
| 2018 | White Wine Trophy | trofej | Temet · Ergo White 2016 | 
| 2018 | бронза | bronza | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Temet · Pinot Grigio 2016 | 
| 2018 | бронза | bronza | Temet · Tri Morave 2016 | 
| 2018 | бронза | bronza | Ivanović · No 1/2 2015 | 
| 2018 | бронза | bronza | Temet · Tri Morave 2016 | 
| 2018 | бронза | bronza | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Radovan · Experiment Prokupac 2016 | 
| 2018 | бронза | bronza | Ivanović · Prokupac 2016 | 
| 2018 | бронза | bronza | Temet · Tri Morave rose 2017 | 
| 2018 | бронза | bronza | Temet · Tri Morave red 2016 | 
| 2018 | серебро | srebro | Temet · Tri Morave 2017 | 
| 2018 | серебро | srebro | Radovan · Prokupac 2015 | 
| 2018 | серебро | srebro | Temet · Tri Morave white 2017 | 
| 2018 | серебро | srebro | Temet · Dobra Godina 2011 | 
| 2018 | серебро | srebro | Temet · Ergo red 2016 | 
| 2017 | бронза | bronza | Temet · Tri Morave White 2016 | 
| 2017 | бронза | bronza | Temet · Ergo White 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Rosé 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Red 2015 | 
| 2017 | бронза | bronza | Spasić · Tamjanika 2016 | 
| 2017 | бронза | bronza | Spasić · Lekcija Tamjanika 2015 | 
| 2017 | отмечено | commended | Temet · Ergo Blush 2015 | 
| 2017 | отмечено | commended | Temet · Ergo Red 2015 | 
| 2017 | серебро | srebro | Radovan · Experiment Prokupac 2015 | 
| 2016 | бронза | bronza | Temet · Tri Morave 2015 | 
| 2016 | бронза | bronza | Temet · Tri Morave 2015 | 
| 2016 | отмечено | commended | Temet · Dobra Godina 2011 | 
| 2016 | отмечено | commended | Temet · Ergo Red 2013 | 
| 2016 | отмечено | commended | Temet · Pinot Grigio 2014 | 
| 2016 | отмечено | commended | Temet · Tri Morave Belo Penušavo Brut 2014 | 
| 2015 | бронза | bronza | Temet · Tri Bele 2014 | 
| 2015 | бронза | bronza | Temet · Pinot Grigio 2014 | 
| 2015 | золото | zlato | Ivanović · No 1/2 2013 | 
| 2015 | отмечено | commended | Temet · Ergo White 2013 | 
| 2015 | отмечено | commended | Temet · Ergo White 2012 | 
| 2015 | отмечено | commended | Temet · Ergo Red 2012 | 
| 2015 | отмечено | commended | Temet · Ergo 2011 | 
| 2015 | серебро | srebro | Temet · Dobra Godina 2011 | 
| 2014 | бронза | bronza | Temet · Tri Morave 2012 | 
| 2014 | бронза | bronza | Temet · Pinot Grigio 2012 | 
| 2014 | бронза | bronza | Temet · Ergo 2011 | 
| 2014 | бронза | bronza | Temet · Ergo White 2012 | 
| 2014 | бронза | bronza | Temet · Rose 2013 | 
| 2014 | золото | zlato | Temet · Pinot G 2013 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Chardonnay Barrique 2008 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Sauvignon blanc Barrique 2009 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Merlot Barrique 2008 | 
| 2014 | серебро | srebro | Temet · Tri morave 2013 | 
| 2013 | большое золото | veliko-zlato | Rubin · Terra Lazarica Cabernet Sauvignon Barrique 2007 | 
| 2013 | бронза | bronza | Temet · Ergo 2011 | 
| 2013 | отмечено | commended | Temet · Tri Morave Belo 2012 | 
| 2013 | отмечено | commended | Temet · Pinot Noir 2011 | 
| 2012 | бронза | bronza | Budimir · Triada 2009 | 
| 2012 | отмечено | commended | Budimir · Tamjanika Zupska 2009 | 

## Неготинска Крайина

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Matalj · Kremen Kamen Cabernet Sauvignon | 2019 | 97 | Falstaff |
| Matalj · Kremen Kamen | 2021 | 97 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2020 | 96 | Falstaff |
| Matalj · Zamna Cabernet Sauvignon | 2020 | 96 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2016 | 95 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2017 | 95 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2017 | 95 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2016 | 95 | decanter |
| Matalj · Cuvée Bukovski | 2021 | 95 | decanter |
| Matalj · Bagrina Bukovska | 2022 | 94 | Falstaff |
| Matalj · Zemna | 2021 | 94 | biwc |
| Matalj · Bukovski | 2020 | 94 | biwc |
| Matalj · Kremen Kamen Cabernet Sauvignon | — | 92 | Wine-Searcher |
| Matalj · Crna Tamjanika | 2022 | 92 | Falstaff |
| Matalj · Terasa Sauvignon Blanc | 2022 | 92 | Falstaff |
| Manastir Bukovo · Chardonnay Oaked | 2021 | 92 | Falstaff |
| Matalj · Kremen | 2020 | 92 | Falstaff |
| Matalj · Terasa Chardonnay | 2022 | 92 | Falstaff |
| Matalj · Terasa Chardonnay | 2013 | 92 | decanter |
| Manastir Bukovo · Filigran Гаме | 2017 | 92 | decanter |
| Matalj · Zemna Reserva | 2021 | 92 | decanter |
| Manastir Bukovo · Black Tamjanika | 2020 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Cabernet Sauvignon | 2019 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Gamay | 2019 | 91 | Falstaff |
| Matalj · Cuvée Bukovski | 2019 | 91 | decanter |
| Matalj · Bukovski Prokupac | 2020 | 91 | decanter |
| Matalj · Bagrina | 2023 | 91 | decanter |
| Matalj · Cuvée Bukovski | 2022 | 91 | decanter |
| Manastir Bukovo · Filigran Chardonnay | 2022 | 90 | Falstaff |
| Matalj · Bukovski | 2020 | 90 | Falstaff |
| Manastir Bukovo · Bez | 2018 | 90 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2013 | 90 | decanter |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 2013 | 90 | decanter |
| Manastir Bukovo · Merlot | 2015 | 90 | decanter |
| Matalj · Kremen | 2017 | 90 | decanter |
| Matalj · Crna Tamjanika | 2021 | 90 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2022 | 90 | decanter |
| Matalj · Zemna Reserva | 2021 | 90 | decanter |
| Matalj · Terasa Chardonnay | 2022 | 90 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2023 | 90 | decanter |
| Matalj · Dušica Rosé | 2022 | 89 | Falstaff |
| Manastir Bukovo · Filigran Rosé | 2022 | 89 | Falstaff |
| Manastir Bukovo · Cabernet Sauvignon | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Gamay | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Reserve Merlot | 2019 | 89 | Falstaff |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2015 | 89 | decanter |
| Matalj · Cuvée Bukovski | 2018 | 89 | decanter |
| Matalj · Bukovski Prokupac-Začinak | 2021 | 89 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2024 | 89 | decanter |
| Matalj · Kremen | 2020 | 89 | biwc |
| Manastir Bukovo · Filigran Гаме | 2015 | 88 | decanter |
| Matalj · Terasa Chardonnay | 2016 | 88 | decanter |
| Manastir Bukovo · Filigran Pinot Noir | 2016 | 88 | decanter |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 2017 | 88 | decanter |
| Matalj · Zamna | 2020 | 88 | decanter |
| Matalj · Kremen | 2022 | 88 | decanter |
| Matalj · Kremen | 2021 | 88 | biwc |
| Matalj · Kremen Cabernet Sauvignon | 2015 | 87 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2016 | 87 | decanter |
| Manastir Bukovo · Filigran Chardonnay | 2017 | 87 | decanter |
| Matalj · Terasa Chardonnay | 2018 | 87 | decanter |
| Manastir Bukovo · Filigran Merlot | 2017 | 87 | decanter |
| Matalj · Terasa Chardonnay | 2019 | 87 | decanter |
| Matalj · Kremen | 2020 | 87 | decanter |
| Matalj · Kremen Cabernet-Merlot | 2021 | 87 | decanter |
| Matalj · Kremen | 2023 | 87 | decanter |
| Matalj · Bagrina Bukovska | 2022 | 87 | biwc |
| Matalj · Terasa Chardonnay | 2017 | 86 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2016 | 86 | decanter |
| Matalj · Cuvée Bukovski | 2018 | 86 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2020 | 86 | decanter |
| Matalj · Bagrina | 2024 | 86 | decanter |
| Matalj · Cuvée Bukovski | 2019 | 86 | biwc |
| Matalj · Zamna | 2020 | 86 | biwc |
| Matalj · Terasa Sauvignon Blanc | 2015 | 85 | decanter |
| Manastir Bukovo · Chardonnay | 2016 | 85 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2017 | 85 | decanter |
| Manastir Bukovo · Filigran Црна Тамјаника | 2017 | 85 | decanter |
| Manastir Bukovo · Filigran Roze | 2017 | 85 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2017 | 85 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Matalj · Bagrina 2024 | 
| 2026 | бронза | bronza | Matalj · Kremen 2023 | 
| 2026 | платина | platina | Matalj · Kremen Kamen 2021 | 
| 2026 | серебро | srebro | Matalj · Cuvée Bukovski 2022 | 
| 2025 | бронза | bronza | Matalj · Terasa Sauvignon Blanc 2024 | 
| 2025 | бронза | bronza | Matalj · Kremen 2022 | 
| 2025 | винодельня года | 1 | Matalj | 
| 2025 | золото | zlato | Matalj · Cuvée Bukovski 2021 | 
| 2025 | лучшее красное, местные сорта | 1 | Matalj · Cuvée Bukovski 2021 | 
| 2025 | серебро | srebro | Matalj · Bagrina 2023 | 
| 2025 | серебро | srebro | Matalj · Zemna Reserva 2021 | 
| 2024 | бронза | bronza | Matalj · Kremen Cabernet-Merlot 2021 | 
| 2024 | бронза | bronza | Matalj · Bukovski Prokupac-Začinak 2021 | 
| 2024 | двойное золото | dvojno-zlato | Matalj · Zemna 2021 | 
| 2024 | двойное золото | dvojno-zlato | Matalj · Bukovski 2020 | 
| 2024 | серебро | srebro | Matalj · Bukovski Prokupac 2020 | 
| 2024 | серебро | srebro | Matalj · Zemna Reserva 2021 | 
| 2024 | серебро | srebro | Matalj · Terasa Chardonnay 2022 | 
| 2024 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2023 | 
| 2024 | серебро | srebro | Matalj · Kremen 2021 | 
| 2023 | бронза | bronza | Matalj · Zamna 2020 | 
| 2023 | бронза | bronza | Matalj · Kremen 2020 | 
| 2023 | золото | zlato | Matalj · Kremen 2020 | 
| 2023 | лучшее из местных сортов, красное | 1 | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2022 | 
| 2023 | серебро | srebro | Matalj · Bagrina Bukovska 2022 | 
| 2023 | серебро | srebro | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Zamna 2020 | 
| 2022 | бронза | bronza | Matalj · Terasa Chardonnay 2019 | 
| 2022 | бронза | bronza | Matalj · Cuvée Bukovski 2018 | 
| 2022 | бронза | bronza | Matalj · Bukovski Cuve 2019 | 
| 2022 | золото | zlato | Matalj · Terasa Chardonnay 2020 | 
| 2022 | лучшее красное | 5 | Manastir Bukovo · Filigran Merlot 2021 | 
| 2022 | серебро | srebro | Matalj · Kremen 2017 | 
| 2022 | серебро | srebro | Matalj · Crna Tamjanika 2021 | 
| 2022 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2021 | 
| 2022 | серебро | srebro | Matalj · Kremen 2019 | 
| 2021 | бронза | bronza | Matalj · Cuvée Bukovski 2018 | 
| 2021 | бронза | bronza | Matalj · Terasa Sauvignon Blanc 2020 | 
| 2021 | бронза | bronza | Manastir Bukovo · Filigran Cabernet Sauvignon 2017 | 
| 2021 | бронза | bronza | Manastir Bukovo · Filigran Merlot 2017 | 
| 2021 | золото | zlato | Matalj · Terasa Chardonnay 2020 | 
| 2021 | серебро | srebro | Manastir Bukovo · Filigran Гаме 2017 | 
| 2021 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2019 | 
| 2021 | серебро | srebro | Matalj · Dušica 2019 | 
| 2021 | серебро | srebro | Matalj · Kremen 2018 | 
| 2021 | серебро | srebro | Matalj · Crna Tamjanika 2020 | 
| 2020 | бронза | bronza | Matalj · Terasa Chardonnay 2016 | 
| 2020 | бронза | bronza | Manastir Bukovo · Filigran Pinot Noir 2016 | 
| 2020 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2016 | 
| 2020 | бронза | bronza | Manastir Bukovo · Filigran Chardonnay 2017 | 
| 2020 | бронза | bronza | Matalj · Terasa Chardonnay 2018 | 
| 2020 | бронза | bronza | Matalj · Crna Tamjanika 2018 | 
| 2020 | бронза | bronza | Raj · Game 2017 | 
| 2020 | золото | zlato | Matalj · Kremen Kamen Cabernet Sauvignon 2017 | 
| 2020 | золото | zlato | Matalj · Kremen Kamen Cabernet Sauvignon 2016 | 
| 2020 | золото | zlato | Matalj · Kremen 2017 | 
| 2020 | золото | zlato | Matalj · Terasa Sauvignon Blanc 2019 | 
| 2020 | золото | zlato | Raj · Sova 2018 | 
| 2020 | отмечено | commended | Manastir Bukovo · Filigran Roze 2017 | 
| 2020 | отмечено | commended | Matalj · Kremen Cabernet Sauvignon 2017 | 
| 2020 | серебро | srebro | Matalj · Dušica 2018 | 
| 2020 | серебро | srebro | Matalj · Bagrina 2019 | 
| 2020 | серебро | srebro | Matalj · Terasa Chardonnay 2018 | 
| 2019 | Red Wine Trophy | trofej | Matalj · Kremen Kamen 2016 | 
| 2019 | бронза | bronza | Matalj · Terasa Chardonnay 2017 | 
| 2019 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2016 | 
| 2019 | бронза | bronza | Manastir Bukovo · Filigran Гаме 2015 | 
| 2019 | бронза | bronza | Matalj · Kremen Kamen Cabernet Sauvignon 2015 | 
| 2019 | бронза | bronza | Matalj · Bagrina 2018 | 
| 2019 | бронза | bronza | Matalj · Terasa Sauvignon Blanc 2017 | 
| 2019 | бронза | bronza | Matalj · Crna Tamjanika 2018 | 
| 2019 | отмечено | commended | Matalj · Kremen 2016 | 
| 2019 | отмечено | commended | Matalj · Kremen Kamen 2015 | 
| 2019 | отмечено | commended | Matalj · Terasa Sauvignon Blanc 2017 | 
| 2019 | отмечено | commended | Matalj · Terasa Sauvignon Blanc 2017 | 
| 2019 | отмечено | commended | Manastir Bukovo · Filigran Црна Тамјаника 2017 | 
| 2019 | серебро | srebro | Matalj · Kremen 2016 | 
| 2019 | серебро | srebro | Matalj · Terasa Chardonnay 2017 | 
| 2018 | отмечено | commended | Manastir Bukovo · Chardonnay 2016 | 
| 2018 | серебро | srebro | Manastir Bukovo · Merlot 2015 | 
| 2018 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2016 | 
| 2018 | серебро | srebro | Matalj · Kremen 2016 | 
| 2017 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2015 | 
| 2017 | бронза | bronza | Raj · Plot 2012 | 
| 2017 | золото | zlato | Matalj · Kremen Kamen 2013 | 
| 2017 | отмечено | commended | Matalj · Terasa Sauvignon Blanc 2015 | 
| 2017 | серебро | srebro | Matalj · Terasa Chardonnay 2013 | 
| 2017 | серебро | srebro | Matalj · Kremen Kamen Cabernet Sauvignon 2013 | 
| 2017 | серебро | srebro | Manastir Bukovo · Filigran Cabernet Sauvignon 2013 | 
| 2017 | серебро | srebro | Matalj · Dusica 2015 | 
| 2017 | серебро | srebro | Matalj · Crna Tamjanika 2015 | 
| 2016 | бронза | bronza | Matalj · Dušica 2015 | 
| 2016 | бронза | bronza | Matalj · Crna Tamjanika 2015 | 
| 2016 | серебро | srebro | Matalj · Terasa Chardonnay 2013 | 
| 2015 | Grand Trophy | trofej | Matalj · Kremen Kamen 2012 | 
| 2015 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2013 | 
| 2015 | золото | zlato | Matalj · Kremen Kamen 2012 | 
| 2015 | золото | zlato | Matalj · Kremen 2013 | 
| 2015 | отмечено | commended | Matalj · Terasa Chardonnay 2013 | 
| 2015 | отмечено | commended | Matalj · Kremen Kamen 2012 | 
| 2015 | серебро | srebro | Matalj · Terasa Chardonnay 2013 | 
| 2015 | серебро | srebro | Matalj · Dusica Rose 2014 | 
| 2014 | бронза | bronza | Matalj · Kremen 2012 | 
| 2014 | бронза | bronza | Matalj · Terasa Chardonnay 2012 | 
| 2014 | бронза | bronza | Matalj · Dušica 2013 | 
| 2014 | золото | zlato | Matalj · Kamen 2011 | 
| 2014 | отмечено | commended | Matalj · Kremen Kamen 2011 | 
| 2014 | серебро | srebro | Matalj · Kremen 2012 | 
| 2013 | бронза | bronza | Matalj · Kremen 2011 | 
| 2013 | отмечено | commended | Matalj · Terasa 2011 | 
| 2012 | отмечено | commended | Matalj · Kremen 2009 | 

## Топлица

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Doja · Breg Prokupac | 2019 | 95 | Falstaff |
| Doja · Prokupac | 2018 | 95 | decanter |
| Doja · Breg Prokupac | 2017 | 95 | decanter |
| Doja · Breg Prokupac | 2020 | 95 | decanter |
| Doja · Breg Cabernet Sauvignon | 2019 | 94 | Falstaff |
| Doja · Cabernet Sauvigon Breg | 2019 | 94 | Falstaff |
| Doja · BREG Cabernet Sauvignon | 2020 | 94 | biwc |
| Doja · Breg Merlot | 2019 | 93 | Falstaff |
| Doja · Prokupac | 2019 | 93 | Falstaff |
| Doja · Breg Merlot | 2019 | 93 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2020 | 92 | Falstaff |
| Doja · Breg Prokupac | 2015 | 92 | decanter |
| Doja · Breg Prokupac | 2019 | 92 | decanter |
| Doja · Breg Merlot | 2019 | 92 | decanter |
| Doja · Prokupac | 2020 | 92 | biwc |
| Doja · Chardonnay Barrique | 2022 | 91 | Falstaff |
| Doja · Rosé | 2022 | 91 | Falstaff |
| Doja · Breg Cabernet Sauvignon | 2019 | 91 | decanter |
| Doja · Prokupac | 2021 | 91 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 91 | biwc |
| Doja · Chardonnay & Pinot Grigio | 2022 | 90 | Falstaff |
| Doja · Prokupac | 2019 | 90 | decanter |
| Doja · Cabernet & Merlot | 2020 | 90 | biwc |
| Doja · BREG Prokupac | 2020 | 90 | biwc |
| Doja · Tamjanika | 2022 | 89 | Falstaff |
| Doja · Prokupac | 2017 | 89 | decanter |
| Doja · Breg Prokupac | 2020 | 89 | biwc |
| Doja · Prokupac | 2021 | 89 | biwc |
| Doja · Belo | 2015 | 88 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2018 | 88 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2021 | 88 | decanter |
| Doja · Breg Prokupac | 2021 | 88 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 88 | biwc |
| Doja · Chardonnay Barrique | 2022 | 88 | biwc |
| Doja · Prokupac | 2020 | 88 | biwc |
| Doja · Tamjanika | 2025 | 88 | biwc |
| Doja · Prokupac | 2015 | 87 | decanter |
| Doja · Breg Prokupac-Cabernet | 2017 | 87 | decanter |
| Doja · Tamjanika | 2020 | 87 | decanter |
| Doja · Prokupac | 2017 | 87 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 87 | decanter |
| Doja · Breg Prokupac | 2021 | 87 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2019 | 87 | biwc |
| Doja · Tamjanika | 2023 | 87 | biwc |
| Doja · Breg Prokupac | 2021 | 87 | biwc |
| Doja · Cabernet Sauvignon - Merlot | 2016 | 86 | decanter |
| Doja · Chardonnay-Pinot Grigio | 2019 | 86 | decanter |
| Doja · Prokupac | 2019 | 86 | biwc |
| Doja · Tamjanika | 2022 | 85 | biwc |
| Doja · Belo Chardonnay-Pinot Grigio | 2016 | 84 | decanter |
| Doja · Tamjanika | 2024 | 84 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Doja · Breg Prokupac 2021 | 
| 2026 | золото | zlato | Doja · Breg Cabernet Sauvignon 2020 | 
| 2026 | золото | zlato | Doja · Prokupac 2021 | 
| 2026 | серебро | srebro | Doja · Prokupac 2021 | 
| 2026 | серебро | srebro | Doja · Tamjanika 2025 | 
| 2026 | серебро | srebro | Doja · Breg Prokupac 2021 | 
| 2025 | бронза | bronza | Doja · Breg Prokupac 2021 | 
| 2025 | бронза | bronza | Doja · Breg Cabernet Sauvignon 2020 | 
| 2025 | бронза | bronza | Doja · Tamjanika 2024 | 
| 2025 | двойное золото | dvojno-zlato | Doja · BREG Cabernet Sauvignon 2020 | 
| 2025 | золото | zlato | Doja · BREG Prokupac 2020 | 
| 2025 | серебро | srebro | Doja · Prokupac 2020 | 
| 2024 | бронза | bronza | Doja · Cabernet Sauvignon - Merlot 2021 | 
| 2024 | вклад в винный туризм | 1 | Doja | 
| 2024 | золото | zlato | Doja · Breg Prokupac 2020 | 
| 2024 | золото | zlato | Doja · Prokupac 2020 | 
| 2024 | золото | zlato | Doja · Breg Prokupac 2020 | 
| 2024 | золото | zlato | Doja · Cabernet & Merlot 2020 | 
| 2024 | серебро | srebro | Doja · Breg Merlot 2019 | 
| 2024 | серебро | srebro | Doja · Breg Cabernet Sauvignon 2020 | 
| 2024 | серебро | srebro | Doja · Chardonnay Barrique 2022 | 
| 2024 | серебро | srebro | Doja · Tamjanika 2023 | 
| 2023 | серебро | srebro | Doja · Prokupac 2019 | 
| 2023 | серебро | srebro | Doja · Breg Prokupac 2019 | 
| 2023 | серебро | srebro | Doja · Breg Cabernet Sauvignon 2019 | 
| 2023 | серебро | srebro | Doja · Breg Merlot 2019 | 
| 2023 | серебро | srebro | Doja · Cabernet Sauvignon - Merlot 2019 | 
| 2023 | серебро | srebro | Doja · Prokupac 2019 | 
| 2023 | серебро | srebro | Doja · Tamjanika 2022 | 
| 2022 | золото | zlato | Doja · Prokupac 2018 | 
| 2022 | золото | zlato | Doja · Breg Prokupac 2017 | 
| 2022 | золото | zlato | Doja · Tamjanika 2021 | 
| 2022 | золото | zlato | Doja · Prokupac 2019 | 
| 2022 | золото | zlato | Doja · Breg Prokupac 2019 | 
| 2022 | серебро | srebro | Doja · Breg Cabernet Sauvignon 2019 | 
| 2021 | бронза | bronza | Doja · Chardonnay-Pinot Grigio 2019 | 
| 2021 | бронза | bronza | Doja · Cabernet Sauvignon - Merlot 2018 | 
| 2021 | бронза | bronza | Doja · Tamjanika 2020 | 
| 2021 | бронза | bronza | Doja · Prokupac 2017 | 
| 2021 | бронза | bronza | Doja · Breg Cabernet Sauvignon 2017 | 
| 2021 | двойное золото | dvojno-zlato | Doja · Prokupac 2018 | 
| 2021 | двойное золото | dvojno-zlato | Vinarija Toplički Vinogradi · Epigenia Cabernet sauvignon 2018 | 
| 2021 | золото | zlato | Doja · Cabernet Sauvignon & Merlot 2018 | 
| 2021 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Pinot Noir 2019 | 
| 2021 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Merlot 2019 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Sauvignon blanc 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Chardonnay 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Prkos rose 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Prokupac 2019 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Gvozdeni puk crveno 2019 | 
| 2021 | серебро | srebro | Doja · Chardonnay & Pinot Grigio 2019 | 
| 2021 | серебро | srebro | Doja · Breg Prokupac 2017 | 
| 2020 | бронза | bronza | Doja · Breg Prokupac-Cabernet 2017 | 
| 2020 | бронза | bronza | Doja · Prokupac 2017 | 
| 2020 | бронза | bronza | Doja · Cabernet Sauvignon - Merlot 2016 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Tribus villa Pinot Noir 2017 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Epigenia Chardonnay 2018 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Epigenia Sauvignon Blanc 2018 | 
| 2020 | золото | zlato | Doja · Cabernet Sauvignon & Merlot 2016 | 
| 2020 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Cabernet Sauvignon 2015 | 
| 2020 | серебро | srebro | Doja · Breg Prokupac 2015 | 
| 2020 | серебро | srebro | Doja · Prokupac 2017 | 
| 2020 | серебро | srebro | Doja · Chardonnay & Pinot Grigio 2018 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Tribus villa Pinot Noir 2015 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Prokupac 2015 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Gvozdeni Puk crveno 2013 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Prkos 2018 | 
| 2018 | отмечено | commended | Doja · Prokupac 2016 | 
| 2018 | отмечено | commended | Doja · Belo Chardonnay & Pinot Grigio 2016 | 
| 2018 | отмечено | commended | Doja · Belo Chardonnay-Pinot Grigio 2016 | 
| 2018 | серебро | srebro | Doja · Rose 2017 | 
| 2018 | серебро | srebro | Doja · Prokupac 2016 | 
| 2017 | Best Indigenous Red variety Trophy | trofej | Doja · Prokupac 2015 | 
| 2017 | бронза | bronza | Doja · Belo 2015 | 
| 2017 | бронза | bronza | Doja · Prokupac 2015 | 
| 2017 | бронза | bronza | Doja · Belo 2015 | 
| 2017 | бронза | bronza | Doja · Rose 2015 | 
| 2017 | отмечено | commended | Doja · Belo 2015 | 

## Юго-восток

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksić · Amanet Vranac | 2019 | 95 | decanter |
| Aleksić · Biser Smederevka Extra Brut | 2016 | 95 | decanter |
| Aleksić · Žuti Cvet Penuśavo Tamnjanika Sec | 2019 | 95 | decanter |
| Jović · VRANAC POTRKANJSKI | 2021 | 94 | biwc |
| Dzervin · Lozana | 2021 | 94 | biwc |
| Aleksić · Biser Smederevka Brut | 2014 | 92 | decanter |
| Aleksić · Kardas Cabernet Sauvignon | 2021 | 92 | decanter |
| Aleksić · Biser Extra Brut | 2016 | 91 | Falstaff |
| Dzervin · Trifun Grand Cabernet Sauvignon | 2019 | 91 | decanter |
| Aleksić · Žuti Cvet Tamjanika | 2025 | 91 | decanter |
| Aleksić · Bonaca Limited | 2014 | 90 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2015 | 90 | decanter |
| Aleksić · Limited Kardaš Cabernet Sauvignon | 2012 | 90 | decanter |
| Aleksić · Žuti Cvet Tamjanika | 2017 | 90 | decanter |
| Aleksić · Amanet Vranac | 2013 | 90 | decanter |
| Aleksić · Žuti Cvet Tamjanika Dry | 2019 | 90 | decanter |
| Aleksić · Cabernet Franc | 2020 | 90 | decanter |
| Aleksić · Limited Kardaš Cabernet Sauvignon | 2021 | 90 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2018 | 89 | decanter |
| Aleksić · Zuti Cvet Tamjanika Extra Brut | 2023 | 89 | decanter |
| Jović · ROSE DIONIZIJE | 2021 | 89 | biwc |
| Dzervin · Sauvignon | 2023 | 89 | biwc |
| Dzervin · Cuvee 69 | 2021 | 89 | biwc |
| Dzervin · Grasac | 2024 | 89 | biwc |
| Dzervin · Sauvignon | 2025 | 89 | biwc |
| Dzervin · Dubravka Gold | 2025 | 89 | biwc |
| Aleksić · Bonaca Chardonnay | 2019 | 88 | awc-vienna |
| Aleksić · Kardaš Limited | 2011 | 88 | decanter |
| Aleksić · Temperament Merlot | 2015 | 88 | decanter |
| Aleksić · Amanet Vranac | 2015 | 88 | decanter |
| Aleksić · Prokupac | 2021 | 88 | decanter |
| Dzervin · Trifun Grand Cabernet Sauvignon | 2019 | 88 | decanter |
| Aleksić · Zuti Cvet Extra Brut | 2022 | 88 | decanter |
| Aleksić · Morava | 2025 | 88 | decanter |
| Jović · POTRKANJSKI DIONIZIJE | 2021 | 88 | biwc |
| Aleksić · Limited Bonaca Chardonnay | 2018 | 87 | awc-vienna |
| Aleksić · Zuti Cvet Penusavo | 2015 | 87 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2019 | 87 | decanter |
| Aleksić · Temperament Merlot | 2015 | 87 | decanter |
| Aleksić · Bonaca Chardonnay | 2021 | 87 | decanter |
| Aleksić · Prokupac | 2021 | 87 | decanter |
| Aleksić · Zuti Cvet | 2023 | 87 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2023 | 87 | decanter |
| Aleksić · Zuti Cvet Tamjanica | 2024 | 87 | decanter |
| Dzervin · Trifun Grand Cabernet Sauvignon | 2019 | 87 | decanter |
| Dzervin · Schlossberg | 2019 | 87 | biwc |
| Dzervin · Sauvignon | 2024 | 87 | biwc |
| Dzervin · Nijansa | 2024 | 87 | biwc |
| Dzervin · Cuvee 69 | 2022 | 87 | biwc |
| Aleksić · Kardaš | 2013 | 86 | decanter |
| Aleksić · Nostalgija | 2017 | 86 | decanter |
| Aleksić · Kardaš Cabernet Sauvignon | 2017 | 86 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2019 | 86 | decanter |
| Aleksić · Limited Kardaš Cabernet Sauvignon | 2015 | 86 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2021 | 86 | decanter |
| Aleksić · Kontra | 2020 | 86 | decanter |
| Aleksić · Zuti Cvet Tamjanika Sec | 2021 | 86 | decanter |
| Dzervin · Riesling | 2021 | 86 | biwc |
| Podrum Malča · Anonymous Crna Tamjanika | 2021 | 86 | biwc |
| Jović · RAJNSKI RIZLING POTRKANJSKI | 2021 | 86 | biwc |
| Dzervin · Trifun | 2019 | 86 | biwc |
| Aleksić · Arno | 2015 | 85 | decanter |
| Aleksić · Amanet Vranac | 2012 | 85 | decanter |
| Dzervin · Sauvignon | 2021 | 85 | biwc |
| Dzervin · Nijansa | 2023 | 85 | biwc |
| Dzervin · Lozana | 2023 | 85 | biwc |
| Aleksić · Limited Bonaca Chardonnay | 2017 | 84 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2017 | 84 | decanter |
| Dzervin · Dubravka Gold | 2024 | 84 | biwc |
| Dzervin · Nijansa | 2025 | 84 | biwc |
| Podrum Malča · Anonymous Sauvignon Blanc | 2021 | 83 | biwc |
| Dzervin · Pinot Noir | 2022 | 82 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Aleksić · Morava 2025 | 
| 2026 | бронза | bronza | Dzervin · Trifun Grand Cabernet Sauvignon 2019 | 
| 2026 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika Extra Brut 2023 | 
| 2026 | бронза | bronza | Dzervin · Nijansa 2025 | 
| 2026 | золото | zlato | Dzervin · Grasac 2024 | 
| 2026 | золото | zlato | Dzervin · Sauvignon 2025 | 
| 2026 | золото | zlato | Dzervin · Dubravka Gold 2025 | 
| 2026 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2025 | 
| 2026 | серебро | srebro | Dzervin · Lozana 2023 | 
| 2026 | серебро | srebro | Dzervin · Cuvee 69 2022 | 
| 2025 | бронза | bronza | Aleksić · Zuti Cvet Tamjanica 2024 | 
| 2025 | бронза | bronza | Aleksić · Zuti Cvet Extra Brut 2022 | 
| 2025 | бронза | bronza | Dzervin · Dubravka Gold 2024 | 
| 2025 | золото | zlato | Dzervin · Cuvee 69 2021 | 
| 2025 | серебро | srebro | Dzervin · Trifun Grand Cabernet Sauvignon 2019 | 
| 2025 | серебро | srebro | Aleksić · Kardas Cabernet Sauvignon 2021 | 
| 2025 | серебро | srebro | Dzervin · Sauvignon 2024 | 
| 2025 | серебро | srebro | Dzervin · Nijansa 2024 | 
| 2024 | бронза | bronza | Aleksić · Prokupac 2021 | 
| 2024 | бронза | bronza | Aleksić · Zuti Cvet 2023 | 
| 2024 | бронза | bronza | Aleksić · Arno Sauvignon Blanc 2023 | 
| 2024 | бронза | bronza | Dzervin · Trifun Grand Cabernet Sauvignon 2019 | 
| 2024 | двойное золото | dvojno-zlato | Jović · VRANAC POTRKANJSKI 2021 | 
| 2024 | двойное золото | dvojno-zlato | Dzervin · Lozana 2021 | 
| 2024 | золото | zlato | Jović · ROSE DIONIZIJE 2021 | 
| 2024 | золото | zlato | Dzervin · Sauvignon 2023 | 
| 2024 | серебро | srebro | Aleksić · Limited Kardaš Cabernet Sauvignon 2021 | 
| 2024 | серебро | srebro | Jović · POTRKANJSKI DIONIZIJE 2021 | 
| 2024 | серебро | srebro | Jović · RAJNSKI RIZLING POTRKANJSKI 2021 | 
| 2024 | серебро | srebro | Dzervin · Nijansa 2023 | 
| 2024 | серебро | srebro | Dzervin · Trifun 2019 | 
| 2023 | бронза | bronza | Aleksić · Prokupac 2021 | 
| 2023 | бронза | bronza | Aleksić · Kontra 2020 | 
| 2023 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika Sec 2021 | 
| 2023 | бронза | bronza | Dzervin · Pinot Noir 2022 | 
| 2023 | бронза | bronza | Podrum Malča · Anonymous Sauvignon Blanc 2021 | 
| 2023 | лучшая малая винодельня | 1 | Jović | 
| 2023 | серебро | srebro | Dzervin · Riesling 2021 | 
| 2023 | серебро | srebro | Dzervin · Sauvignon 2021 | 
| 2023 | серебро | srebro | Dzervin · Schlossberg 2019 | 
| 2023 | серебро | srebro | Podrum Malča · Anonymous Crna Tamjanika 2021 | 
| 2022 | бронза | bronza | Aleksić · Bonaca Chardonnay 2021 | 
| 2022 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2021 | 
| 2022 | золото | zlato | Aleksić · Amanet Vranac 2019 | 
| 2022 | золото | zlato | Aleksić · Biser Smederevka Extra Brut 2016 | 
| 2022 | золото | zlato | Aleksić · Žuti Cvet Penuśavo Tamnjanika Sec 2019 | 
| 2022 | золото | zlato | Dzervin · Sauvignon 2020 | 
| 2022 | золото | zlato | Dzervin · Rose Pinot 2021 | 
| 2022 | серебро | srebro | Aleksić · Cabernet Franc 2020 | 
| 2022 | серебро | srebro | Dzervin · Schlossberg 2019 | 
| 2021 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2021 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika Dry 2019 | 
| 2021 | серебро | srebro | Dzervin · Grasac 2019 | 
| 2021 | серебро | srebro | Dzervin · Sauvignon blanc 2020 | 
| 2021 | серебро | srebro | Dzervin · Rose Pinot 2019 | 
| 2020 | бронза | bronza | Aleksić · Kardaš Cabernet Sauvignon 2017 | 
| 2020 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2019 | 
| 2020 | бронза | bronza | Aleksić · Arno Sauvignon Blanc 2019 | 
| 2020 | бронза | bronza | Aleksić · Limited Kardaš Cabernet Sauvignon 2015 | 
| 2020 | золото | zlato | Aleksić · Amanet 2015 | 
| 2020 | золото | zlato | Aleksić · Biser 2015 | 
| 2020 | золото | zlato | Jović · Chardonnay Potrkanjski 2019 | 
| 2020 | золото | zlato | Jović · Vranac Potrkanjski 2016 | 
| 2020 | серебро | srebro | Aleksić · Bonaca Chardonnay 2019 | 
| 2020 | серебро | srebro | Aleksić · Limited Bonaca Chardonnay 2018 | 
| 2020 | серебро | srebro | Aleksić · Barbara 2019 | 
| 2020 | серебро | srebro | Dzervin · Schlossberg 2017 | 
| 2020 | серебро | srebro | Dzervin · Sauvignon blanc 2018 | 
| 2020 | серебро | srebro | Dzervin · Riesling 2017 | 
| 2020 | серебро | srebro | Jović · Potrkanjski Dionizije 2017 | 
| 2019 | бронза | bronza | Aleksić · Nostalgija 2017 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2018 | 
| 2019 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2019 | бронза | bronza | Aleksić · Amanet Vranac 2015 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Penusavo 2015 | 
| 2019 | бронза | bronza | Dzervin · Sauvignon Blanc 2017 | 
| 2019 | бронза | bronza | Dzervin · Riesling 2017 | 
| 2019 | серебро | srebro | Aleksić · Zuti Cvet 2018 | 
| 2019 | серебро | srebro | Dzervin · Schlossberg 2016 | 
| 2018 | отмечено | commended | Aleksić · Limited Bonaca Chardonnay 2017 | 
| 2018 | отмечено | commended | Aleksić · Arno Sauvignon Blanc 2017 | 
| 2018 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2017 | 
| 2018 | серебро | srebro | Aleksić · Amanet Vranac 2013 | 
| 2018 | серебро | srebro | Aleksić · Biser Smederevka Brut 2014 | 
| 2017 | серебро | srebro | Aleksić · Arno Sauvignon Blanc 2015 | 
| 2017 | серебро | srebro | Aleksić · Limited Kardaš Cabernet Sauvignon 2012 | 
| 2016 | бронза | bronza | Aleksić · Kardaš Limited 2011 | 
| 2016 | бронза | bronza | Aleksić · Kardaš 2013 | 
| 2016 | бронза | bronza | Aleksić · Arno 2015 | 
| 2016 | бронза | bronza | Aleksić · Barbara 2015 | 
| 2016 | отмечено | commended | Aleksić · Arno 2015 | 
| 2016 | отмечено | commended | Aleksić · Amanet Vranac 2012 | 
| 2016 | серебро | srebro | Aleksić · Bonaca Limited 2014 | 
| 2016 | серебро | srebro | Aleksić · Žuti cvet 2015 | 
| 2016 | серебро | srebro | Aleksić · Kardaš 2013 | 
| 2015 | бронза | bronza | Aleksić · Bonaca Limited 2013 | 
| 2015 | бронза | bronza | Aleksić · Sevdah 2014 | 
| 2015 | бронза | bronza | Aleksić · Kardas limited 2011 | 
| 2015 | бронза | bronza | Aleksić · Kardas 2012 | 
| 2015 | бронза | bronza | Aleksić · Barbara 2014 | 
| 2015 | лучшая национальная винодельня | 1 | Aleksić | 
| 2015 | отмечено | commended | Aleksić · Nostalgija 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2014 | бронза | bronza | Aleksić · Kardas Limited 2011 | 
| 2014 | золото | zlato | Aleksić · Amanet 2011 | 
| 2014 | отмечено | commended | Aleksić · Amanet 2011 | 
| 2014 | отмечено | commended | Aleksić · Kardas Limited 2011 | 
| 2014 | отмечено | commended | Aleksić · Zuti Cvet 2013 | 
| 2014 | отмечено | commended | Aleksić · Kardaš Limited 2011 | 
| 2014 | отмечено | commended | Aleksić · Amanet 2011 | 
| 2014 | отмечено | commended | Aleksić · Arno 2013 | 
| 2014 | серебро | srebro | Aleksić · Arno 2013 | 
| 2013 | бронза | bronza | Aleksić · Kardaš 2011 | 
| 2013 | бронза | bronza | Aleksić · Arno 2012 | 

## Подунавье и Белградский район

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Plavinac · Sauvignon Blanc | 2025 | 89 | awc-vienna |
| Plavinac · Traminac | 2025 | 89 | awc-vienna |
| Plavinac · Cabernet Sauvignon Barrique | — | 88 | awc-vienna |
| Plavinac · Tamjanika | 2025 | 88 | gilbert-gaillard |
| Plavinac · Sauvignon Blanc | 2025 | 88 | gilbert-gaillard |
| Plavinac · Smederevka | 2025 | 88 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Plavinac · Smederevka 2025 | 
| 2026 | одобрение | approval | Plavinac · Cabernet Sauvignon Barrique | 
| 2026 | серебро | srebro | Plavinac · Sauvignon Blanc 2025 | 
| 2026 | серебро | srebro | Plavinac · Traminac 2025 | 

## Косово и Метохия

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Lakićević · ALCEDO | 2021 | 89 | biwc |
| Lakićević · MERULA Selection | 2020 | 89 | biwc |
| Lakićević · ORIOLUS | 2020 | 89 | biwc |
| Lakićević · PARUS | 2022 | 89 | biwc |
| Lakićević · PICUS | 2023 | 89 | biwc |
| Lakićević · ORIOLUS | 2022 | 89 | biwc |
| Lakićević · PARUS | 2020 | 86 | biwc |
| Lakićević · PICUS Selection | 2020 | 85 | biwc |
| Lakićević · MERULA | 2021 | 84 | biwc |
| Lakićević · SOLARIS | 2023 | 84 | biwc |
| Lakićević · MERULA | 2020 | 82 | biwc |
| Lakićević · UPUPA | 2022 | 82 | biwc |
| Lakićević · PICUS | 2022 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2025 | бронза | bronza | Lakićević · MERULA 2021 | 
| 2025 | бронза | bronza | Lakićević · SOLARIS 2023 | 
| 2025 | золото | zlato | Lakićević · PARUS 2022 | 
| 2025 | золото | zlato | Lakićević · PICUS 2023 | 
| 2025 | золото | zlato | Lakićević · ORIOLUS 2022 | 
| 2025 | лучшее белое, органика, международные сорта | 1 | Lakićević · Parus 2022 | 
| 2024 | лучшее красное, органика, международные сорта | 1 | Lakićević · Corvus Cabernet Franc 2021 | 
| 2023 | бронза | bronza | Lakićević · MERULA 2020 | 
| 2023 | бронза | bronza | Lakićević · PICUS 2022 | 
| 2023 | бронза | bronza | Lakićević · UPUPA 2022 | 
| 2023 | золото | zlato | Lakićević · ALCEDO 2021 | 
| 2023 | золото | zlato | Lakićević · MERULA Selection 2020 | 
| 2023 | золото | zlato | Lakićević · ORIOLUS 2020 | 
| 2023 | лучшая молодая винодельня | 1 | Lakićević | 
| 2023 | серебро | srebro | Lakićević · PARUS 2020 | 
| 2023 | серебро | srebro | Lakićević · PICUS Selection 2020 | 
| 2022 | бронза | bronza | Lakićević · UPUPA 2020 | 
| 2022 | двойное золото | dvojno-zlato | Lakićević · PICUS 2019 | 
| 2022 | золото | zlato | Lakićević · ORIOLUS 2019 | 
| 2022 | золото | zlato | Lakićević · SOLARIS 2021 | 
| 2022 | серебро | srebro | Lakićević · PARUS 2019 | 
| 2022 | серебро | srebro | Lakićević · MERULA 2019 | 
| 2021 | золото | zlato | Lakićević · Oriolus 2018 | 
| 2021 | золото | zlato | Lakićević · Merula 2018 | 
| 2021 | серебро | srebro | Lakićević · Upupa 2019 | 

## Хозяйства без района

- La Gora · Aria 2025 — 96 [biwc]
- Grabak · Vivak Prokupac 2017 — 95 [decanter]
- BT Winery · King Supreme Limited Edition Marselan 2018 — 95 [decanter]
- Reljić Vinarija · Rebus Merlot-Cabernet Sauvignon-Probus 2018 — 95 [decanter]
- BT Winery · Mister Marselan 2021 — 95 [decanter]
- Virtus · Morava 2023 — 95 [decanter]
- La Gora · Bello 2025 — 95 [decanter]
- Винарија Тришић (Vinarija Trišić) · Dimasid 2013 — 94 [decanter]
- Stemina winery · Draga 2008 — 94 [decanter]
- Dibonis Winery · Di Icewine 2020 — 94 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2023 — 94 [decanter]
- Podrum Pevac · GUŠT BARIK 2021 — 94 [biwc]
- Vinarija Dumo · MMXXI 2021 — 94 [biwc]
- Grabak · Prokupac 2020 — 94 [biwc]
- Vinarija Gamanović · Grasac beli 2020 — 94 [biwc]
- Vinarija Gnezdo · Sovinjon Kis 2021 — 94 [biwc]
- Fruškogorski · Tri SuncA 2015 — 93 [gilbert-gaillard]
- Virtus · Pinot Grigio 2024 — 93 [decanter]
- Vinarija Frug · Signum Cabernet Sauvignon 2021 — 93 [decanter]
- Dolina · Cuveé Barrique 2019 — 93 [decanter]
- Vinarija Eden · Velvet 2020 — 93 [decanter]
- Vinarija DeLena · 1903 Merlot 2017 — 92 [Falstaff]
- Vinarija Jeremić · Kanon Merlot Cabernet Sauvignon 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Tamjanika 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Prokupac 2018 — 92 [Falstaff]
- Virtus · Credo 2013 — 92 [decanter]
- Vinarija Lastar · Triangl Pinot Noir 2017 — 92 [decanter]
- Vinarija Frunza Aglaja · Dentelle 2016 — 92 [decanter]
- Vista Hill · Reserve White 2012 — 92 [decanter]
- Virtus · Credo Beli 2019 — 92 [decanter]
- Vinarija Sokolov Zamak · Moscato Giallo 2021 — 92 [decanter]
- Vinarija Sokolov Zamak · Marselan 2019 — 92 [decanter]
- Vinarija Frug · Chardonnay Signum 2023 — 92 [decanter]
- Vinarija Frug · Cuvée 2022 — 92 [decanter]
- Traško Vinarija · Bagrina Edición Limitada 2024 — 92 [decanter]
- Podrum Pevac · Tišina Malvazija 2025 — 92 [decanter]
- La Gora · Lupo 2025 — 92 [decanter]
- Vinarija Frug · Grašac 2025 — 92 [decanter]
- Dolina · Euphonia Gran Reserva 2018 — 92 [decanter]
- Grabak · Prokupac 2020 — 92 [decanter]
- Gora · White Bland 2024 — 92 [biwc]
- La Gora · Chardonnay 2025 — 92 [biwc]
- Vinarija Radlović doo · Cabernet Sauvignon 2020 — 92 [biwc]
- PIK OPLENAC · Monarh Immortal S 2017 — 91 [Falstaff]
- Vinarija Jeremić · Sonata Sauvignon Blanc 2021 — 91 [Falstaff]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2019 — 91 [Falstaff]
- Virtus · Prokupac 2016 — 91 [decanter]
- Podrum Janko · Crveni Zapis 2016 — 91 [decanter]
- Podrum Janko · Zavet Stari 2016 — 91 [decanter]
- Vinarija Aven · Merlot 2019 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Podrum Janko · Zavet Stari 2017 — 91 [decanter]
- Podrum Stari Hrast · Selekcija Merlot 2017 — 91 [decanter]
- Reljić Vinarija · Rebus Reserve 2019 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Vinarija Lastar · Sofijin Izbor Pinot Noir 2019 — 91 [decanter]
- Винарија Ступови (Vinarija Stupovi) · Merlot 2021 — 91 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2021 — 91 [decanter]
- Virtus · Prokupac 2020 — 91 [decanter]
- Vinarija Lastar · Cabernet Franc 2020 — 91 [decanter]
- Vinarija Savic · Merlot 2021 — 91 [decanter]
- Komuna Vinarija · Rara Avis 2020 — 91 [decanter]
- Virtus · Marselan 2020 — 91 [decanter]
- Драгић Винарија (Vina Dragic) · Beli Biser 2022 — 91 [decanter]
- Vinarija Stanković · Chardonnay 2024 — 91 [decanter]
- Vinarija Frug · Pinot Noir 2022 — 91 [decanter]
- Vinarija Frug · Syrah Signum 2022 — 91 [decanter]
- Vinarija Imperator · Constantius 2023 — 91 [decanter]
- Драгић Винарија (Vina Dragic) · Mitra 2025 — 91 [decanter]
- Dolina · Barrique Xix Reserve 2019 — 91 [decanter]
- Podrum Pevac · PROKUPAC 2021 — 91 [biwc]
- Vinarija Mrdjanin · Bermet Vinarija Mrdjanin 2021 — 91 [biwc]
- Vinarija Tri Tachke · Rezonanca 2022 — 91 [biwc]
- La Gora · Lupo 2025 — 91 [biwc]
- Vinarija DeLena · 70/30 Sauvignon Blanc /Semillon 2020 — 90 [Falstaff]
- AURUS Winery & Distillery · Cabernet 2022 — 90 [awc-vienna]
- Podrum Dremina · Cabernet Sauvignon 2023 — 90 [awc-vienna]
- PR Anjino Vino · Vino 2024 — 90 [awc-vienna]
- Podrum Zlatanović · Branko Savić - Podrum Zlatanović 2025 — 90 [awc-vienna]
- Podrum Janko · Vrtlog 2015 — 90 [decanter]
- Vinarija Dumo · Pinot Noir 2015 — 90 [decanter]
- Virtus · Pinot Grigio 2017 — 90 [decanter]
- Podrum Janko · Zavet Stari 2015 — 90 [decanter]
- Virtus · Credo 2013 — 90 [decanter]
- Pusula Winery · Traminac 2017 — 90 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2017 — 90 [decanter]
- Virtus · Prokupac 2016 — 90 [decanter]
- Virtus · Marselan 2016 — 90 [decanter]
- Virtus · Prokupac 733  — 90 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2017 — 90 [decanter]
- Zmajevac · Cuvée 2017 — 90 [decanter]
- Zmajevac · Prokupac 2018 — 90 [decanter]
- Vinarija Sokolov Zamak · Marselan 2020 — 90 [decanter]
- Virtus · 733 2017 — 90 [decanter]
- Vinarija Fragaria · Selekcija 2019 — 90 [decanter]
- Grabak · Sojka 2021 — 90 [decanter]
- Vinarija Đurđevića Legat · Otisak Vremena 2020 — 90 [decanter]
- Reljić Vinarija · Rebus Crveno 2020 — 90 [decanter]
- Podrum Petrović · Grašac 2022 — 90 [decanter]
- Vinarija Venčac · Legat 1903 Muscat Petit Grain 2021 — 90 [decanter]
- Château Prince · Velika Morava 2021 — 90 [decanter]
- Art Et Vinum · Meduza 2021 — 90 [decanter]
- Podrum Janko · Bifora 2020 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2020 — 90 [decanter]
- Manufaktura Spasić · Rebo 2020 — 90 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2021 — 90 [decanter]
- Vinarija Milićević · Vladavina Icone Merlot 2021 — 90 [decanter]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2021 — 90 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2022 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Nemirac 2022 — 90 [decanter]
- Vinarija Sokolov Zamak · Tamjanika 2022 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2023 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2023 — 90 [decanter]
- Vinarija Frug · Sauvignon Blanc 2024 — 90 [decanter]
- Gora · Grašac 2024 — 90 [decanter]
- Николић Неyзински (Nikolićh Neuzinsky) · Monah Cabernet Franc-Merlot 2020 — 90 [decanter]
- Vinarija Frug · Chardonnay Signum 2022 — 90 [decanter]
- Vinarija Gnezdo · Kadarka 2024 — 90 [decanter]
- Karić Vinarija · Adria 2024 — 90 [decanter]
- Vinarija Gnezdo · Belo 2024 — 90 [decanter]
- Vinarija Frug · Chardonnay Signum 2024 — 90 [decanter]
- Virtus · Marselan 2022 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Cabernet Franc 2023 — 90 [decanter]
- Vinarija Stanković · Cabernet Sauvignon 2023 — 90 [decanter]
- Vinarija Frug · Chardonnay Signum 2022 — 90 [decanter]
- Vinarija Zorča · Velika Dusa Merlot 2019 — 90 [decanter]
- Vinarija Unikat · Vranac 2019 — 90 [decanter]
- Винарија Тришић (Vinarija Trišić) · Trišino 2020 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2023 — 90 [decanter]
- Podrum Pevac · ZAGRLJAJ 2019 — 90 [biwc]
- Vinarija Gamanović · Grasac Beli 2020 — 90 [biwc]
- Rakicevic · Blagoslov 2020 — 90 [biwc]
- Podrum Pevac · KABERNE FRAN 2023 — 90 [biwc]
- VINARIJA RNJAK · CUVEE DE RGNAC 2019 — 90 [biwc]
- MV Vinarija · Tamjanika Hope 2022 — 90 [biwc]
- Vinarija Frug · Grašac 2024 — 90 [biwc]
- Vinarija Frug · Chardonnay Signum 2023 — 90 [biwc]
- Vinarija Frug · Cuvee 2022 — 90 [biwc]
- Vinarija Milićević · VladaVina 2023 — 90 [biwc]
- Vinarija Ilić-Nijemčević · IG 2025 — 90 [biwc]
- Château Prince · Charm 2024 — 90 [biwc]
- Vinarija Ilić-Nijemčević · IG 2024 — 90 [biwc]
- La Gora · Bello 2025 — 90 [biwc]
- PIK OPLENAC · Constanta Muse Sauvignon Blanc 2021 — 89 [Falstaff]
- PIK OPLENAC · Constanta Muse Rose 2019 — 89 [Falstaff]
- Mikić · Chardonnay 2025 — 89 [awc-vienna]
- Podrum Dremina · Blanc Coupage 2024 — 89 [awc-vienna]
- AURUS Winery & Distillery · Merlot 2022 — 89 [awc-vienna]
- Vinarija Frunza Aglaja · Cabernet Sauvignon 2015 — 89 [decanter]
- Virtus · W 2019 — 89 [decanter]
- Stemina winery · Panta Rei Chardonnay 2018 — 89 [decanter]
- BT Winery · President Vranac Gold 2018 — 89 [decanter]
- Vinarija Dumo · Pinot Noir 2019 — 89 [decanter]
- Podrum Janko · Zavet 2019 — 89 [decanter]
- Virtus · Prokupac 2018 — 89 [decanter]
- Vinarija Fragaria · Fragari Votazi 2019 — 89 [decanter]
- Marselan · Marselan 2019 — 89 [decanter]
- Трилогия Винария - Vinarija Trilogija · Pečat Grand Reserve 2017 — 89 [decanter]
- Драгић Винарија (Vina Dragic) · Randes 2021 — 89 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2020 — 89 [decanter]
- Vinarija Mrdjanin · Family Edition Probus 2020 — 89 [decanter]
- Vinarija Todorović · Merlot 2020 — 89 [decanter]
- Virtus · Credo 2020 — 89 [decanter]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 89 [decanter]
- Podrum Pevac · Gušt 2023 — 89 [decanter]
- Karić Vinarija · Adria Belo 2023 — 89 [decanter]
- Vinarija Stanković · Chardonnay 2023 — 89 [decanter]
- Krstašica Doo · Konekicja Sauvignon Blanc 2023 — 89 [decanter]
- Breg · Tamjanika 2024 — 89 [decanter]
- Vinarija Grumen · Morava 2024 — 89 [decanter]
- Vinarija Sokolov Zamak · Marselan 2021 — 89 [decanter]
- Virtus · Credo 2024 — 89 [decanter]
- Vinarija Rajić · Tamjanika 2024 — 89 [decanter]
- Vinarija Rajić · Triva Souvignier Gris 2024 — 89 [decanter]
- La Gora · Lupo 2024 — 89 [decanter]
- Vinarija Imperator · Max 2021 — 89 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2022 — 89 [decanter]
- Vinarija Frug · Pinot Noir 2023 — 89 [decanter]
- La Gora · Sauvignon Blanc 2025 — 89 [decanter]
- Vinarija Frug · Chardonnay Signum 2023 — 89 [decanter]
- Château Prince · Probus M barrique 2020 — 89 [biwc]
- Château Prince · Chateau Shiraz 2021 — 89 [biwc]
- Podrum Petrović · Grašac „Podrum Petrović“ 2022 — 89 [biwc]
- Milanov Podrum · Prolog 2017 — 89 [biwc]
- Vinarija Dumo · Pinot Noir 2020 — 89 [biwc]
- Vinarija Komazec · Gazdino Crveno – Tesla 2020 — 89 [biwc]
- Vinarija Komazec · Palava 2021 — 89 [biwc]
- Vinarija Mrdjanin · Merlot Vinarija Mrdjanin 2021 — 89 [biwc]
- Vinarija Teodos · Traminac 2021 — 89 [biwc]
- Vinarija VRT · ROSSE 2022 — 89 [biwc]
- Podrum Pevac · TIHO TEČE 2023 — 89 [biwc]
- VINARIJA RNJAK · PINOT NOIR 2021 — 89 [biwc]
- Vinarija Blagojević · Probus M barrique 2021 — 89 [biwc]
- Château Prince · Shiraz Premium 2021 — 89 [biwc]
- Vinarija VRT · pesak kvarcni 2023 — 89 [biwc]
- Poljoprivredno Gazdinstvo Anja Džipković · Siesta 2023 — 89 [biwc]
- Château Prince · Cuvee 2021 — 89 [biwc]
- Château Prince · Princess 2021 — 89 [biwc]
- Château Prince · Velika 2023 — 89 [biwc]
- Vinarija Frug · Pinot Noir 2023 — 89 [biwc]
- Podrum Pevac · Izazov 2024 — 89 [biwc]
- Vinska Kuća Rajić · RAJIĆ TAMJANIKA 2024 — 89 [biwc]
- Vinska Kuća Rajić · RAJIĆ MONIKA 2023 — 89 [biwc]
- Vinarija Milićević · Merlo Classic 2021 — 89 [biwc]
- Vinarija Gnezdo · Belo 2024 — 89 [biwc]
- Vinarija Gnezdo · Belo 2025 — 89 [biwc]
- Vinarija Blagojević · Probus M Barik 2022 — 89 [biwc]
- La Gora · Lupo 2024 — 89 [biwc]
- Podrum Pevac · Gušt, Chardonnay Sur Lie 2023 — 89 [biwc]
- Vinarija 100 Žena · Velikidečko 2022 — 89 [biwc]
- Vinarija Milićević · Cabernet ICONE 2023 — 89 [biwc]
- Vinarija Milićević · Grašac 2024 — 89 [biwc]
- Vinarija Slatina · Grašac 2025 — 89 [biwc]
- Vinarija Tasa · Morava 2025 — 89 [biwc]
- Jelena Munizaba PR Radnja za proizvodnju grozdja i vina, turizam i ugostiteljstvo. · Cabernet Franc 2021 — 88 [awc-vienna]
- Podrum Janko · Misija Chardonnay 2013 — 88 [decanter]
- Podrum Bačina · Dolina XII  — 88 [decanter]
- Virtus · Gewürztraminer 2014 — 88 [decanter]
- Komuna Vinarija · Chardonnay 2015 — 88 [decanter]
- Virtus · Marselan 2015 — 88 [decanter]
- Vinarija Lastar · Pinot Noir 2015 — 88 [decanter]
- Vinarija Lastar · Tamjanika 2016 — 88 [decanter]
- Virtus · Marselan 2016 — 88 [decanter]
- Podrum Janko · Bifora 2016 — 88 [decanter]
- Pusula Winery · Sauvignon Blanc 2017 — 88 [decanter]
- Grabak · Prokupac 2017 — 88 [decanter]
- PIK OPLENAC · Monarh S 2015 — 88 [decanter]
- Podrum Janko · Zapis Testament 2016 — 88 [decanter]
- Nikad Nije Kasno · Signature 2016 — 88 [decanter]
- Vinarija Dumo · Pinot Noir 2017 — 88 [decanter]
- PIK OPLENAC · Monarh Immortal S 2017 — 88 [decanter]
- Vinarija DeLena · 1903 Merlot 2016 — 88 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2019 — 88 [decanter]
- Probus Vineyards · Traminac 2018 — 88 [decanter]
- Vinarija Eden · Chardonnay 2019 — 88 [decanter]
- Vinarija Aven · Balance 2018 — 88 [decanter]
- Vinarija Frunza Aglaja · Sauvignon-Semillon 2020 — 88 [decanter]
- Podrum Janko · Bifora 2017 — 88 [decanter]
- Grabak · Prva Lasta Prokupac 2021 — 88 [decanter]
- BT Winery · Kings Crown 2020 — 88 [decanter]
- Николић Неyзински (Nikolićh Neuzinsky) · The Secret Code of Our Terroir 2020 — 88 [decanter]
- Vinarija Aven · Balance 2019 — 88 [decanter]
- Max-Ex Doo · Rebus Crveni 2019 — 88 [decanter]
- Podrum Petrović · Cabernet Sauvignon 2019 — 88 [decanter]
- Virtus · Marselan 2018 — 88 [decanter]
- Vinarija Komazec · Palava 2021 — 88 [decanter]
- Virtus · Sauvignon Blanc 2021 — 88 [decanter]
- Vinarija Lastar · Chardonnay 2018 — 88 [decanter]
- Николић Неyзински (Nikolićh Neuzinsky) · Santa Maria 2021 — 88 [decanter]
- Vinarija Eden · Genesis 2019 — 88 [decanter]
- Reljić Vinarija · Rebus Crveno 2019 — 88 [decanter]
- Vinarija Unikat · Vranac 2019 — 88 [decanter]
- Virtus · Prokupac 2019 — 88 [decanter]
- Vinarija Zaba · Barrique Merlot 2019 — 88 [decanter]
- Probus Vineyards · Magis 2017 — 88 [decanter]
- Château Prince · Chateau Shiraz 2021 — 88 [decanter]
- Драгић Винарија (Vina Dragic) · Aurora 2020 — 88 [decanter]
- Tri Medje I Oblak · Bigfoot Chardonnay 2021 — 88 [decanter]
- Podrum Pevac · Gušt Barrique Chardonnay 2021 — 88 [decanter]
- Podrum Stari Hrast · Sauvignon Blanc 2021 — 88 [decanter]
- Virtus · Marselan 2020 — 88 [decanter]
- Krstašica Doo · Konekcija Merlot 2020 — 88 [decanter]
- Krstašica Doo · Konekcija Merlot 2021 — 88 [decanter]
- Vinarija Sokolov Zamak · Marselan 2021 — 88 [decanter]
- BT Winery · Mister Marselan 2022 — 88 [decanter]
- Virtus · Credo Beli 2022 — 88 [decanter]
- Karić Vinarija · Adria Belo 2022 — 88 [decanter]
- Grabak · Modrovrana Cabernet Sauvignon 2018 — 88 [decanter]
- Vinarija Sokolov Zamak · Chardonnay 2023 — 88 [decanter]
- Драгић Винарија (Vina Dragic) · Kibic 2022 — 88 [decanter]
- Vinarija Frug · Chardonnay 2023 — 88 [decanter]
- Breg · Grašac 2024 — 88 [decanter]
- Gora · White Blend 2024 — 88 [decanter]
- Vinarija Mira · La Baba Morava 2024 — 88 [decanter]
- BT Winery · Mister Marselan 2022 — 88 [decanter]
- Vinarija Rajić · Prokupac 2024 — 88 [decanter]
- La Gora · Bello 2024 — 88 [decanter]
- Vinarija Imperator · Gratianus Traminac 2021 — 88 [decanter]
- Винарија Тришић (Vinarija Trišić) · Dimasid 2021 — 88 [decanter]
- Traško Vinarija · Fucking Fabulous Edición Limitada 2021 — 88 [decanter]
- Château Prince · Gospodar 2021 — 88 [decanter]
- Traško Vinarija · Fabulous Cabernet Sauvignon 2022 — 88 [decanter]
- La Gora · Chardonnay 2025 — 88 [decanter]
- Breg · Grašac 2025 — 88 [decanter]
- Vinarija Imperator · VAL Rajnski Rizling 2022 — 88 [decanter]
- Grabak · Vivak Prokupac 2019 — 88 [decanter]
- Vinarija Zorča · Mali Ratnik Cabernet Sauvignon 2020 — 88 [decanter]
- The Sparkling Winery · The Extra Brut 2023 — 88 [decanter]
- Vinarija Baza · Barre 2021 — 88 [biwc]
- Vinarija Komazec · Palava 2022 — 88 [biwc]
- Vinarija Radlović doo · Cirkuz Rose 2022 — 88 [biwc]
- Vinarija Lastar · Chardonnay 2023 — 88 [biwc]
- Podrum Šukac · Merlot 2019 — 88 [biwc]
- Vinarija VRT · pesak beli 2023 — 88 [biwc]
- Gora · Grašac 2024 — 88 [biwc]
- Vinska Kuća Rajić · RAJIĆ CHARDONNAY 2023 — 88 [biwc]
- Vinarija 100 Žena · Veliki Dečko 2022 — 88 [biwc]
- Vinarija Lastar · Chardonnay 2024 — 88 [biwc]
- Plavinci · Indigo Reserva 2019 — 88 [biwc]
- Château Prince · Gospodar 2021 — 88 [biwc]
- Djordjevic Estate Winery · Rose Djordjevic Estate 2024 — 88 [biwc]
- Vinarija Gamanović · Grasac Beli 2025 — 88 [biwc]
- Langov Podrum · Lang Grašac beli 2025 — 88 [biwc]
- Vinarija Lastar · Tamjanika Lastar 2025 — 88 [biwc]
- Vinarija Milićević · Grašac 2025 — 88 [biwc]
- AURUS Winery & Distillery · Chardonnay 2023 — 87 [awc-vienna]
- Vinarija Ždrnja · Grašac 2025 — 87 [awc-vienna]
- Mikić · Bagrina 2024 — 87 [awc-vienna]
- Podrum Janko · Misija 2016 — 87 [decanter]
- Atos-Fructum · The 2015 — 87 [decanter]
- Probus Vineyards · Magis 2017 — 87 [decanter]
- Vinarija Lastar · Pinot Noir 2016 — 87 [decanter]
- Grabak · Siva Vrana 2017 — 87 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2017 — 87 [decanter]
- Virtus · W Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Noir 2017 — 87 [decanter]
- Vinarija Janucic · Vulkan Merlot 2017 — 87 [decanter]
- Zmajevac · Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2019 — 87 [decanter]
- PIK OPLENAC · Monarh Immortal Cuvée 2015 — 87 [decanter]
- Vinogradi Veličković Vinarija · Sauvignon Blanc 2015 — 87 [decanter]
- Vinarija Aven · Merlot 2018 — 87 [decanter]
- Zmajevac · Chardonnay 2019 — 87 [decanter]
- Virtus · Marselan 2017 — 87 [decanter]
- Vinarija Lastar · Merlot-Cabernet Franc 2017 — 87 [decanter]
- Zmajevac · Cuvée 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2020 — 87 [decanter]
- BT Winery · King Supreme Marselan 2020 — 87 [decanter]
- Virtus · Gewurztraminer 2021 — 87 [decanter]
- Virtus · Prokupac 2018 — 87 [decanter]
- Podrum Bačina · Dolina 2018 — 87 [decanter]
- Vinarija Eden · Cabernet Franc 2019 — 87 [decanter]
- Podrum Pevac · Zagrljaj 2019 — 87 [decanter]
- Probus Vineyards · Belim 2017 — 87 [decanter]
- Vinarija Gamanović · Cabernet Sauvignon 2020 — 87 [decanter]
- Virtus · Pinot Grigio 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Rajnski Rizling 2020 — 87 [decanter]
- Манастир Студеница (Manastir Studenica) · Prokupac 1186 2020 — 87 [decanter]
- Vinarija Fragaria · Votazi 2020 — 87 [decanter]
- Vinarija Bora · Frenk 2020 — 87 [decanter]
- Grabak · Prokupac 2020 — 87 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2021 — 87 [decanter]
- Podrum Pevac · Prokupac 2021 — 87 [decanter]
- Tref Line · Pirg Sauvignon Blanc 2021 — 87 [decanter]
- Vinarija Fragaria · Jagoda 2022 — 87 [decanter]
- Манастир Студеница (Manastir Studenica) · Bela Reč Tamjanika 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Chardonnay 2022 — 87 [decanter]
- Vinarija Stanković · Chardonnay 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Randes 2022 — 87 [decanter]
- Virtus · Prokupac 2019 — 87 [decanter]
- Podrum Janko · Zlatno Runo Cabernet Sauvignon 2019 — 87 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2019 — 87 [decanter]
- Vinarija Sokolov Zamak · Chardonnay 2023 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2024 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Sauvignon Blanc 2024 — 87 [decanter]
- Breg · Sila 2024 — 87 [decanter]
- Vinarija Frug · Grašac 2024 — 87 [decanter]
- Virtus · Prokupac 2020 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Rajnski Rizling 2020 — 87 [decanter]
- Vinarija Frug · Syrah Signum 2022 — 87 [decanter]
- PR Anjino Vino · Suton Merlot 2022 — 87 [decanter]
- La Grande Bellezza · Blanc De Blancs Extra Brut 2021 — 87 [decanter]
- Château Prince · Charm Chardonnay-Morava 2024 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2024 — 87 [decanter]
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
- Орлић Породична Винарија - Orlić Family Winery · MMXXIII Shiraz 2023 — 87 [decanter]
- The Sparkling Winery · The Blanc de Noirs 2023 — 87 [decanter]
- Vinarija Imperator · Frušet Rosé Brut 2022 — 87 [decanter]
- Podrum Petrović · Bermet Braće Petrović 2021 — 87 [biwc]
- Grabak · Vivak Prokupac 2019 — 87 [biwc]
- Vinarija Komazec · Cabernet Sauvignon 2021 — 87 [biwc]
- Vinarija Komazec · Gazdino Crveno 2019 — 87 [biwc]
- Винарија Ступови (Vinarija Stupovi) · Cabernet Sauvignon 2021 — 87 [biwc]
- Винарија Ступови (Vinarija Stupovi) · Merlot 2021 — 87 [biwc]
- VINARIJA RNJAK · CRVENI PUŽ 2019 — 87 [biwc]
- Château Prince · CUVEE 2021 — 87 [biwc]
- Vinska Kuća Rajić · RAJIĆ 2023 — 87 [biwc]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 87 [biwc]
- MV Vinarija · Tamjanika – Hope 2021 — 87 [biwc]
- Poljoprivredno Gazdinstvo Anja Džipković · Suton 2022 — 87 [biwc]
- Bajilo · Grasac 2021 — 87 [biwc]
- Lutak winery · Merlo 2022 — 87 [biwc]
- Grabak · Bela golubica 2024 — 87 [biwc]
- Djordjevic Estate Winery · Merlot Djordjevic Estate 2024 — 87 [biwc]
- Vinarija Gamanović · Samotok 2022 — 87 [biwc]
- Vinarija Slatina · Tamjanika 2025 — 87 [biwc]
- Vinarija 100 Žena · Roze 100 žena 2025 — 87 [biwc]
- Vinarija Radlović doo · Chardonnay 2024 — 87 [biwc]
- Vinarija Radlović doo · Cirkuz Rose 2025 — 87 [biwc]
- Anatea Vinarija · Anatea 2025 — 86 [awc-vienna]
- Virtus · Credo 2013 — 86 [decanter]
- Mcculloch Wines · Traminac 2013 — 86 [decanter]
- Vinarija Lastar · Chardonnay 2015 — 86 [decanter]
- Virtus · Credo Beli 2015 — 86 [decanter]
- Podrum Janko · Smederevka 2017 — 86 [decanter]
- Virtus · Gewürztraminer 2017 — 86 [decanter]
- Vinarija Lastar · Chardonnay 2016 — 86 [decanter]
- Podrum Janko · Vrtlog 2016 — 86 [decanter]
- Grabak · Modrovrana 2015 — 86 [decanter]
- Virtus · Pinot Noir 2015 — 86 [decanter]
- PIK OPLENAC · Villa Muscat Ottonel 2015 — 86 [decanter]
- Komuna Vinarija · Chardonnay 2017 — 86 [decanter]
- Pusula Winery · Cabernet 2015 — 86 [decanter]
- Vinarija Frunza Aglaja · Dantelle Cabernet Sauvignon 2016 — 86 [decanter]
- Virtus · Credo 2017 — 86 [decanter]
- Nikad Nije Kasno · Simfonija 2017 — 86 [decanter]
- Vista Hill · Premium 2019 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Sauvignon Blanc 2019 — 86 [decanter]
- Virtus · Sauvignon Blanc 2019 — 86 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2018 — 86 [decanter]
- Rubinov · Prokupac 2018 — 86 [decanter]
- BT Winery · King's Crown 2018 — 86 [decanter]
- Prokupac · Prokupac 2018 — 86 [decanter]
- Pusula Winery · Cabernet 2017 — 86 [decanter]
- Grabak · Modrovrana 2017 — 86 [decanter]
- Zmajevac · Cuvée Reserve 2017 — 86 [decanter]
- Vinarija Komazec · Rose 2021 — 86 [decanter]
- Vinarija Lastar · Pinot Noir 2019 — 86 [decanter]
- Grabak · Prokupac 2019 — 86 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2020 — 86 [decanter]
- Vinarija Đurđevića Legat · Otisak 2020 — 86 [decanter]
- Tri Medje I Oblak · Vagabundo Cabernet Sauvignon 2020 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Kibic 2021 — 86 [decanter]
- Vinarija Podrum Danguba · Ponovo Naše Tamjanika 2021 — 86 [decanter]
- Vinarija Gamanović · Bela Tamjanika 2021 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Cabernet Franc 2020 — 86 [decanter]
- Manufaktura Spasić · Krivac 2020 — 86 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2021 — 86 [decanter]
- Vinarija Gnezdo · Genzdo Muskat Krokan 2022 — 86 [decanter]
- Krstašica Doo · Konekicja Chardonnay 2023 — 86 [decanter]
- Château Prince · Shiraz Premium 2021 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2024 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Sauvignon Blanc 2024 — 86 [decanter]
- Vinarija Milićević · Vladavina Riesling-Grašac 2024 — 86 [decanter]
- Tri Medje I Oblak · Vagabundo Sauvignon Blanc 2025 — 86 [decanter]
- Gardijan · Stigma Chardonnay 2023 — 86 [decanter]
- Plavinci · Ćilibar 2021 — 86 [biwc]
- Bajilo · Sauvignon blanc 2021 — 86 [biwc]
- VINARIJA RNJAK · PINOT NOIR 2019 — 86 [biwc]
- Vinarija VRT · PESAK BELI 2022 — 86 [biwc]
- Podrum Pevac · PROKUPAC ROZE 2023 — 86 [biwc]
- Vinarija Lastar · Cru 6 Lastar  — 86 [biwc]
- VINARIJA RNJAK · CHARDONNAY 2023 — 86 [biwc]
- Podrum Šukac · Sauvignon Blanc 2023 — 86 [biwc]
- Vinarija Gnezdo · Belo 2023 — 86 [biwc]
- Vinarija VRT · pesak plavi 2021 — 86 [biwc]
- Lutak winery · Lutkovo crno 2022 — 86 [biwc]
- Lutak winery · S-Kvark 2022 — 86 [biwc]
- Vinarija Dumo · Pinot Noir 2022 — 86 [biwc]
- Vinarija Tri Tachke · Rezonanca limited 2021 — 86 [biwc]
- Vinarija Lastar · Merlot Cabernet Franc 2020 — 86 [biwc]
- Château Prince · Velika 2024 — 86 [biwc]
- La Gora · Sauvignon Blanc 2025 — 86 [biwc]
- Vinarija Lastar · Sofijin Izbor Pinot Noir 2022 — 86 [biwc]
- Vinarija Milićević · Sauvignon Blanc 2025 — 86 [biwc]
- Vinarija Radlović doo · Morava 2025 — 86 [biwc]
- Vinarija Podrum Danguba · "Nema dalje" Chardonnay 2015 — 85 [awc-vienna]
- Podrum Bačina · Dolina 2012 — 85 [decanter]
- Podrum Janko · Zavet Stari 2012 — 85 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2015 — 85 [decanter]
- Podrum Janko · Misija 2015 — 85 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2015 — 85 [decanter]
- Virtus · Sauvignon Blanc 2017 — 85 [decanter]
- PIK OPLENAC · Monarh Cuvée 2014 — 85 [decanter]
- Vinarija Frunza Aglaja · Cabernet Sauvignon 2016 — 85 [decanter]
- Fruškogorski · Quet Pinot Noir 2016 — 85 [decanter]
- Vinarija Frunza Aglaja · Cabernet Sauvignon 2017 — 85 [decanter]
- PIK OPLENAC · Monarh Immortal Cuvée 2014 — 85 [decanter]
- Virtus · Pinot Noir 2015 — 85 [decanter]
- Podrum Janko · Misija 2016 — 85 [decanter]
- Vinarija Lastar · Triangl Chardonnay 2016 — 85 [decanter]
- Vinarija Dumo · Pinot Noir 2016 — 85 [decanter]
- Винарија Тришић (Vinarija Trišić) · Trisino 2013 — 85 [decanter]
- Винарија Тришић (Vinarija Trišić) · Trisino 2013 — 85 [decanter]
- Vista Hill · Selection Red 2017 — 85 [decanter]
- Podrum Bačina · Dolina Barrique XVII 2017 — 85 [decanter]
- PIK OPLENAC · Constanta Muse Sauvignon blanc 2019 — 85 [decanter]
- AE projekt centar · Carski Drum Chardonnay 2019 — 85 [decanter]
- Vinarija Podrum Danguba · Ima Noći Merlot 2015 — 85 [decanter]
- Virtus · W Credo Beli 2018 — 85 [decanter]
- Kuća Vina Jokić · Traminac 2018 — 85 [decanter]
- Château Prince · Rose 2021 — 85 [biwc]
- Vinarija Ilić-Nijemčević · Frankovka Ilić-Nijemčević 2020 — 85 [biwc]
- Vinarija Lastar · Cabernet Franc 2021 — 85 [biwc]
- Vinarija Lastar · Sofijin izbor 2021 — 85 [biwc]
- Vinarija Komazec · Chardonnay 2021 — 85 [biwc]
- Vinarija Mrdjanin · Cabernet Sauvignon 2020 — 85 [biwc]
- Vinarija Mrdjanin · Sila Vinarija Mrdjanin 2022 — 85 [biwc]
- VINARIJA RNJAK · CUVEE DE RGNAC 2018 — 85 [biwc]
- Vinarija VRT · PESAK SIVI 2022 — 85 [biwc]
- Podrum Pevac · GUŠT 2023 — 85 [biwc]
- Château Prince · Charm 2023 — 85 [biwc]
- Vinarija 100 Žena · Tamjanika 100 žena 2023 — 85 [biwc]
- Vinarija 100 Žena · Veliki dečko 2022 — 85 [biwc]
- Vinarija Gnezdo · Pino 2021 — 85 [biwc]
- Vinarija Savic · Cabernet Sauvignon  — 85 [biwc]
- Vinarija Frug · Rose 2023 — 85 [biwc]
- Vinarija Milićević · Cabernet Classic 2023 — 85 [biwc]
- Vinarija 100 Žena · Crna ovca 2023 — 85 [biwc]
- Vinarija Blagojević · Petite Arvine 2024 — 85 [biwc]
- Damalis · Sauvignon Blanc 2025 — 85 [biwc]
- Dimalis · Rosé 2025 — 85 [biwc]
- Dimalis · Sauvignon Blanc 2025 — 85 [biwc]
- Vinarija Ilić-Nijemčević · Frankovka 2021 — 85 [biwc]
- Podrum Pevac · Tišina, Malvazija 2025 — 85 [biwc]
- Vinarija Milićević · Morava 2025 — 85 [biwc]
- Vinis · Crveno Vino 2012 — 84 [decanter]
- Podrum Stari Hrast · Sauvignon Blanc 2017 — 84 [decanter]
- Vinarija Lastar · Chardonnay 2017 — 84 [decanter]
- Fruškogorski · Quet Grašac 2017 — 84 [decanter]
- Vinarija Aven · Merlot 2017 — 84 [decanter]
- Vinarija Lastar · Triangl Sauvignon-Viognier 2016 — 84 [decanter]
- Vindulo d.o.o. · Mirna Bačka 2016 — 84 [decanter]
- Probus Vineyards · Gewürztraminer 2018 — 84 [decanter]
- Virtus · W Marselan 2017 — 84 [decanter]
- Vinis · Merlot 2015 — 84 [decanter]
- Adora · Cabernet Sauvignon 2016 — 84 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum 2019 — 84 [decanter]
- Vinarija Frunza Aglaja · Cabernet Sauvignon 2018 — 84 [decanter]
- Fruškogorski · Tri Sunca Kasna Berba Traminac 2015 — 84 [decanter]
- Vinarija Baza · Talični 2022 — 84 [biwc]
- VINARIJA RNJAK · SAUVIGNON BLANC 2021 — 84 [biwc]
- Château Prince · Velika 2022 — 84 [biwc]
- Rajković wine office · Rajković Tamjanika 2023 — 84 [biwc]
- Vinarija Savic · Tamjanika Videlo 2022 — 84 [biwc]
- Podrum Pevac · Zagrljai 2020 — 84 [biwc]
- Vinarija Lastar · rose 2024 — 84 [biwc]
- Vinarija Milićević · rose 2022 — 84 [biwc]
- Vinarija Gnezdo · Roze 2024 — 84 [biwc]
- Vinarija Blagojević · Prokupac Barik 2023 — 84 [biwc]
- Vinarija Gnezdo · Roze 2025 — 84 [biwc]
- Vinarija Gnezdo · Kadarka 2024 — 84 [biwc]
- Virtus · Marselan 2014 — 83 [decanter]
- Tody · Doja Belo 2014 — 83 [decanter]
- Quet · 13/15 Merlot  — 83 [decanter]
- Virtus · W Gewurztraminer 2019 — 83 [decanter]
- Château Prince · Morava M 2022 — 83 [biwc]
- Podrum Pevac · IZAZOV 2022 — 83 [biwc]
- Podrum Pevac · Prokupac Penusavo vino 2022 — 83 [biwc]
- Milanov Podrum · Lutka 2022 — 83 [biwc]
- Poljoprivredno Gazdinstvo Anja Džipković · Zora 2022 — 83 [biwc]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 83 [biwc]
- Podrum Pevac · GUŠT (Barik) 2022 — 83 [biwc]
- Vinarija Lastar · Rose Lastar 2023 — 83 [biwc]
- Vinarija Blagojević · Petit Arvin M 2022 — 83 [biwc]
- Vinarija Unikat · Šeret 2021 — 83 [biwc]
- Vinarija Blagojević · Probus M barik 2021 — 83 [biwc]
- Vinska Kuća Rajić · RAJIĆ CRNA TAMJANIKA 2024 — 83 [biwc]
- Podrum Pevac · Zagrljaj, Cabarnet Franc, Merlo and Cabarnet Sauvignon 2020 — 83 [biwc]
- Vinarija 100 Žena · Crna ovca 2023 — 83 [biwc]
- Vinarija Tasa · Sauvignon Blanc 2025 — 83 [biwc]
- Vinarija Komazec · Rose 2022 — 82 [biwc]
- Vinarija Unikat · Vranac 2019 — 82 [biwc]
- Podrum Pevac · Kaberne Franc 2024 — 82 [biwc]
- Vinarija Gnezdo · Crno 2023 — 82 [biwc]
- Langov Podrum · Lang Chardonnay 2025 — 82 [biwc]
- Vinarija Baza · Baza-proseko 2021 — 81 [biwc]
- Vinarija Gamanović · Cabernet Sauvignon 2020 — 81 [biwc]
- Vinarija Lastar · Chardonnay 2021 — 81 [biwc]
- Lutak winery · Lutkovo Crno 2022 — 81 [biwc]
- VINARIJA RNJAK · CHARDONNAY 2021 — 81 [biwc]
- Vinarija Teodos · Krokan 2021 — 81 [biwc]
- Vinarija Unikat · Šeret 2021 — 81 [biwc]
- Vinarium winery · Merlot 2020 — 81 [biwc]
- Podrum Pevac · IZAZOV 2023 — 81 [biwc]
- Vinarija Gnezdo · Muskat Krokan 2022 — 81 [biwc]
- Poljoprivredno Gazdinstvo Anja Džipković · Zora 2023 — 81 [biwc]
- Vinarija Milićević · VladiVina 2024 — 81 [biwc]
- Vinska Kuća Rajić · RAJIĆ ROSE 2024 — 81 [biwc]
- Vinarija Gnezdo · Krokan 2024 — 81 [biwc]
