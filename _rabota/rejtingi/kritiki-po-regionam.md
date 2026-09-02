# Оценки критиков

Вторая дорожка, независимая от Vivino. Здесь стобалльная шкала и оценка
эксперта, а не средняя по толпе.

**Почему отдельно, а не вместе.** У Vivino пятибалльная оценка покупателей,
и её вес определяется числом отметок. У критика вес определяется тем, что он
критик; порога по числу отзывов здесь нет и быть не может. Это две разные
величины, и в одно число они не складываются. Если рейтинги пойдут в книгу,
показывать их надо порознь и подписывать, что именно показано.

## Две вещи, а не одна

**Оценки** — балл по стобалльной шкале, 2097 записей.

**Награды** — место в категории или медаль, 2937 записей. У них нет шкалы,
зато есть год и категория. Переводить «лучшее белое из местных сортов
2025 года» в число нельзя, поэтому и таблицы разные.

Держится это на двух конкурсах. Decanter — база наград открылась целиком,
девятнадцать лет, 2008–2026, 1096 сербских медалей, и у 941 ещё балл.
Balkans International Wine Competition — софийский конкурс, для Сербии
ближайший крупный: 1072 медали, 33 трофея и 421 балл за тринадцать лет.

## Источники

**Falstaff** — 142 оценки, сербский список целиком. Австрийский гид ведёт
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
Для Сербии он ближе любого другого крупного: 1085 сербских вин за 2014–2026
годы, у 421 есть балл, у 1072 — медаль. Это больше, чем дал Decanter,
и в иные годы под полтораста сербских вин зараз.

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
Сербия у него есть с 2009 по 2022 год: 66 отмеченных вин — 11 серебра,
22 бронзы, 33 «отмечено». Балла IWC не ставит, поэтому записи идут
в награды. Больше всего у Александровића (29) и Ластара (16), дальше
Алексић, PIK Опленац, Рубин, Doja, Matalj, Вино Будимир, Звонко Богдан.
С 2023 года сербских вин на конкурсе нет.

**Concours Mondial de Bruxelles** — восемь сербских медалей за все годы:
два серебра 2011 Радовановићу за «Chardonnay Selekcija» и «Cabernet
Sauvignon Reserve», большое золото 2013 Рубину за «Terra Lazarica Cabernet
Sauvignon Barrique», золото 2019 «Nikad Nije Kasno», серебро 2019 Рубину,
золото и серебро 2023 Подруму Певац, золото 2024 Ралевићу.

**Decanter** — база наград DWWA целиком, 2008–2026. По каждому вину:
хозяйство, имя, урожай, цвет, стиль, медаль и балл. Медали по годам:
2008 — 2, 2009 — 3, 2010 — 10, 2011 — 8, 2012 — 14, 2013 — 36, 2014 — 35,
2015 — 49, 2016 — 35, 2017 — 54, 2018 — 63, 2019 — 67, 2020 — 115,
2021 — 64, 2022 — 85, 2023 — 103, 2024 — 117, 2025 — 99, 2026 — 146.
Счёт за 2026-й сошёлся с книгой ровно: 3 платины, 7 золота, 58 серебра,
78 бронзы — то есть 146, а не 149, как писала пресса.

В таблицу из этих 1105 записей попадают 1096, и девять недостающих
объяснимы поимённо. У восьми вин Decanter не написал имени — только
хозяйство, медаль и балл, — а без имени вину неоткуда взяться в таблице;
три из восьми как раз в 2026 году: два у Frug, одно у La Gora. Девятая —
собственный повтор Decanter: «Sauvignon Blanc 2012» Звонка Богдана стоит
в списке DWWA 2013 дважды, под номерами 640263 и 640264, с одной и той же
наградой.

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

**Глава книги известна у 80 хозяйств из 454**, а настоящий рејон —
у 333. Остальных Vivino сваливает в «Central Serbia» и «Wine of Serbia»,
и Винарски регистар не узнаёт по имени. Разбор — в `po-rejonima.md`.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-kritikov.py --otchet

---

<!-- Собрано скриптом svesti-kritikov.py. Руками не править. -->

## Где две дорожки пересекаются

Вин с оценкой Vivino — 1180, с оценкой критиков — 1063, **с обеими — 346**.

| Район | Vivino | Критики | И то и другое |
|---|---|---|---|
| Фрушка гора | 233 | 215 | 83 |
| Суботичско-Хоргошская пешчара | 76 | 29 | 17 |
| Банат | 47 | 22 | 12 |
| Шумадия | 104 | 106 | 40 |
| Три Моравы и Жупа | 152 | 102 | 42 |
| Неготинска Крайина | 42 | 41 | 16 |
| Топлица | 22 | 21 | 11 |
| Юго-восток | 31 | 48 | 13 |
| Подунавье и Белградский район | 17 | 28 | 6 |
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
| Belo Brdo · Limited Edition Cabernet Sauvignon | 2018 | 93 | awc-vienna |
| Belo Brdo · Marselan Limited Edition | 2018 | 93 | awc-vienna |
| Belo Brdo · Marselan | 2013 | 93 | awc-vienna |
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
| Trivanović · Reserve Shiraz | 2018 | 92 | awc-vienna |
| Belo Brdo · Cabernet Franc Black Label Limited Edition | 2018 | 92 | awc-vienna |
| Belo Brdo · Cabernet Franc Black Label | 2017 | 92 | awc-vienna |
| Belo Brdo · Marselan Black Label | 2015 | 92 | awc-vienna |
| Erdevik · Grand Trianon | — | 91 | Wine-Searcher |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | — | 91 | Wine-Searcher |
| Molovin · Inat Traminac | 2020 | 91 | Falstaff |
| Deurić · Classic Chardonnay | 2018 | 91 | decanter |
| Deurić · Aksiom | 2016 | 91 | decanter |
| Deurić · Classic Chardonnay | 2021 | 91 | decanter |
| Verkat · Malvazija Barrique | 2021 | 91 | decanter |
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
| Belo Brdo · Bermet Black Label | 2020 | 91 | awc-vienna |
| Belo Brdo · Bermet White Label | 2020 | 91 | awc-vienna |
| Belo Brdo · Limited Edition Decade | 2018 | 91 | awc-vienna |
| Belo Brdo · Petit Verdot Limited Edition | 2020 | 91 | awc-vienna |
| Kovačević · Cuvee Piquant | 2017 | 91 | awc-vienna |
| Belo Brdo · Cabernet Sauvignon | 2012 | 91 | awc-vienna |
| Belo Brdo · Cabernet Sauvignon | 2011 | 91 | awc-vienna |
| Kovačević · Edicija S Aurelius | 2019 | 90 | Falstaff |
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
| Vinarija Djurdjic · Grasac | 2022 | 90 | biwc |
| Vinarija Šijački · Seduša | 2022 | 90 | biwc |
| Trivanović · Ultimo S | 2020 | 90 | biwc |
| Trivanović · Toca | 2018 | 90 | biwc |
| Šapat · Cuvee | 2023 | 90 | biwc |
| Vinum · Grašac 26a | 2022 | 90 | awc-vienna |
| Vinum · Grašac 26a | 2021 | 90 | awc-vienna |
| Trivanović · PINOT GRIGIO | 2023 | 90 | awc-vienna |
| Molovin · Rajnski Rizling | 2021 | 90 | awc-vienna |
| Veritas Ćuković · Monte Karlovci | 2020 | 90 | awc-vienna |
| Verkat · to Verkat Grašac beli 4.0 | 2021 | 90 | awc-vienna |
| Kovačević · Rizling | 2021 | 90 | awc-vienna |
| Belo Brdo · Pinot Noir Black Label Limited Edition | 2020 | 90 | awc-vienna |
| Trivanović · Reserve Shiraz | 2017 | 90 | awc-vienna |
| Deurić · Probus 276 | 2018 | 90 | awc-vienna |
| Belo Brdo · Cabernet Franc Black Label | 2018 | 90 | awc-vienna |
| Belo Brdo · Petit Verdot | 2018 | 90 | awc-vienna |
| Belo Brdo · Chardonnay | 2018 | 90 | awc-vienna |
| Belo Brdo · Pinot Noir Black Label | 2017 | 90 | awc-vienna |
| Trivanović · OPTIMUS | 2018 | 90 | awc-vienna |
| Trivanović · SHIRAZ LIMITED | 2017 | 90 | awc-vienna |
| Belo Brdo · Chardonnay | 2017 | 90 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2017 | 90 | awc-vienna |
| Belo Brdo · Bermet Black Label | 2012 | 90 | awc-vienna |
| Molovin · Plavi Princip Blaufränkisch | 2013 | 90 | awc-vienna |
| Belo Brdo · Alma Mons | 2013 | 90 | awc-vienna |
| Belo Brdo · Black Label Cabernet Sauvignon | 2013 | 90 | awc-vienna |
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
| Vinarija Djurdjic · Probus | 2020 | 89 | biwc |
| Kiš · Verus GT | 2023 | 89 | biwc |
| Kiš · Kisov Grasac beli | 2024 | 89 | biwc |
| Kiš · Verus GT | 2024 | 89 | biwc |
| Šapat · Atila Cabernet sauvignon | 2023 | 89 | biwc |
| Šapat · Atila Sauvignon blanc | 2024 | 89 | biwc |
| Vinum · Grašac 26a | 2023 | 89 | awc-vienna |
| Trivanović · Reserve Shiraz | 2020 | 89 | awc-vienna |
| Trivanović · Reserve Cabernet Sauvignon | 2017 | 89 | awc-vienna |
| Trivanović · PINOT GRIGIO | 2021 | 89 | awc-vienna |
| Trivanović · Reserve Shiraz | 2018 | 89 | awc-vienna |
| Belo Brdo · Black Label Limited Edition Chardonnay | 2020 | 89 | awc-vienna |
| Trivanović · CABERNET SAUVIGNON | 2016 | 89 | awc-vienna |
| Trivanović · Reserve Cabernet Sauvignon | 2017 | 89 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2019 | 89 | awc-vienna |
| Deurić · Probus 276 | 2017 | 89 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2018 | 89 | awc-vienna |
| Belo Brdo · Alma Mons | 2017 | 89 | awc-vienna |
| Belo Brdo · Alma Mons | 2016 | 89 | awc-vienna |
| Trivanović · Cabernet sauvignon | 2015 | 89 | awc-vienna |
| Kovačević · Chardonnay | 2017 | 89 | awc-vienna |
| Kovačević · Aurelius | 2016 | 89 | awc-vienna |
| Belo Brdo · Black Label Cabernet Sauvignon | 2015 | 89 | awc-vienna |
| Belo Brdo · Cabernet Franc Black Label | 2015 | 89 | awc-vienna |
| Kovačević · Brut | 2010 | 89 | awc-vienna |
| Belo Brdo · Reserve Music Edition | 2013 | 89 | awc-vienna |
| Vinum · Italijanski Rizling | 2016 | 89 | awc-vienna |
| Belo Brdo · Belo Brdo | 2013 | 89 | awc-vienna |
| Molovin · Plavi Princip | 2013 | 89 | awc-vienna |
| Belo Brdo · Alma Mons | 2012 | 89 | awc-vienna |
| Belo Brdo · Chardonnay | 2015 | 88 | awc-vienna |
| Erdevik · Omnibus Lector Chardonnay | 2015 | 88 | decanter |
| Molovin · Inat Crveni | 2010 | 88 | decanter |
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
| The Sparkling Winery · The Extra Brut | 2023 | 88 | decanter |
| Vinum · Grasac 26a | 2022 | 88 | biwc |
| Kiš · Biser Bermet crveni | 2024 | 88 | biwc |
| Šapat · Chardonnay | 2023 | 88 | biwc |
| Vinčić · Grand Fru | 2023 | 88 | biwc |
| Kiš · Kisov Bermet | 2025 | 88 | biwc |
| Kiš · Kisov Grasac beli | 2025 | 88 | biwc |
| Kiš · Misterija | 2025 | 88 | biwc |
| Vinum · Grašac 26a | 2022 | 88 | awc-vienna |
| Trivanović · Reserve Shiraz | 2020 | 88 | awc-vienna |
| Molovin · Inat Rajnski Rizling | 2021 | 88 | awc-vienna |
| Kovačević · Sauvignon | 2021 | 88 | awc-vienna |
| Kovačević · S Edition Sauvignon | 2020 | 88 | awc-vienna |
| Kovačević · S Edition Aurelius | 2017 | 88 | awc-vienna |
| Belo Brdo · Riesling Black Label Limited Edition | 2020 | 88 | awc-vienna |
| Verkat · Roze | 2021 | 88 | awc-vienna |
| Kiš · Kišov Grašac Beli | 2020 | 88 | awc-vienna |
| Trivanović · SHIRAZ | 2018 | 88 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2020 | 88 | awc-vienna |
| Belo Brdo · Rosé | 2020 | 88 | awc-vienna |
| Trivanović · CHARDONNAY BARRIQUE | 2018 | 88 | awc-vienna |
| Trivanović · PINOT GRIGIO | 2019 | 88 | awc-vienna |
| Trivanović · OPTIMUS | 2019 | 88 | awc-vienna |
| Trivanović · SHIRAZ | 2018 | 88 | awc-vienna |
| Belo Brdo · Decade | 2018 | 88 | awc-vienna |
| Vinarija Djurdjic · Cabernet Franc | 2017 | 88 | awc-vienna |
| Kovačević · Chardonnay | 2018 | 88 | awc-vienna |
| Belo Brdo · Merlot Black label | 2017 | 88 | awc-vienna |
| Kiš · Kišova Misterija Riesling | 2016 | 88 | awc-vienna |
| Kiš · Kišov rosé | 2018 | 88 | awc-vienna |
| Trivanović · CHARDONNAY BARRIQUE | 2017 | 88 | awc-vienna |
| Trivanović · PINOT GRIGIO | 2018 | 88 | awc-vienna |
| Trivanović · CABERNET SAUVIGNON LIMITED | 2017 | 88 | awc-vienna |
| Kovačević · S Edition Chardonnay | 2015 | 88 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2017 | 88 | awc-vienna |
| Belo Brdo · Alma Mons Black Label Reserve | 2015 | 88 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2016 | 88 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2016 | 88 | awc-vienna |
| Belo Brdo · Petit Verdot | 2015 | 88 | awc-vienna |
| Belo Brdo · Merlot Black Label | 2013 | 88 | awc-vienna |
| Belo Brdo · Cabernet Franc Black Label | 2013 | 88 | awc-vienna |
| Vinum · Rosé | 2015 | 88 | awc-vienna |
| Belo Brdo · Pinot Noir Reserve | 2012 | 88 | awc-vienna |
| Belo Brdo · Alma Mons White | 2013 | 88 | awc-vienna |
| Belo Brdo · Alma Mons Reserve | 2011 | 88 | awc-vienna |
| Belo Brdo · Cabernet Franc | 2012 | 88 | awc-vienna |
| Belo Brdo · Marselan | 2012 | 88 | awc-vienna |
| Vinum · Grašac 26A | 2023 | 87 | awc-vienna |
| Deurić · Enigma | 2015 | 87 | decanter |
| Deurić · Urban Rose | 2015 | 87 | decanter |
| Deurić · Pinot Noir | 2015 | 87 | decanter |
| Erdevik · Trianon Merlot-Cabernet Sauvignon-Syrah | 2016 | 87 | decanter |
| Erdevik · Grand Trianon | 2016 | 87 | decanter |
| Deurić · Pinot Noir | 2017 | 87 | decanter |
| Belo Brdo · Black Label Cabernet Sauvignon | 2018 | 87 | decanter |
| Deurić · Princeps Probus | 2016 | 87 | decanter |
| Bikicki · S/O | 2020 | 87 | decanter |
| Vinčić · Grand Fru | 2020 | 87 | decanter |
| Erdevik · Geronimo | 2021 | 87 | decanter |
| Šapat · Pi'Crveno Premium | 2019 | 87 | decanter |
| Bikicki · Cu | 2022 | 87 | decanter |
| The Sparkling Winery · The Blanc de Noirs | 2023 | 87 | decanter |
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
| Trivanović · OPTIMUS | 2023 | 87 | awc-vienna |
| Verkat · Malvazija | 2022 | 87 | awc-vienna |
| Veritas Ćuković · Bela Harmonija | 2021 | 87 | awc-vienna |
| Trivanović · OPTIMUS | 2021 | 87 | awc-vienna |
| Trivanović · Reserve Cabernet Sauvignon | 2017 | 87 | awc-vienna |
| Kiš · Kišov Rosé | 2020 | 87 | awc-vienna |
| Trivanović · Reserve Shiraz | 2017 | 87 | awc-vienna |
| Belo Brdo · Alma Mons Black Label | 2017 | 87 | awc-vienna |
| Belo Brdo · Alma Mons Black Label | 2018 | 87 | awc-vienna |
| Belo Brdo · Black Label Cabernet Sauvignon | 2018 | 87 | awc-vienna |
| Kovačević · Rizling | 2017 | 87 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2018 | 87 | awc-vienna |
| Belo Brdo · Rosé | 2018 | 87 | awc-vienna |
| Trivanović · ROSE | 2018 | 87 | awc-vienna |
| Trivanović · CABERNET SAUVIGNON LIMITED | 2016 | 87 | awc-vienna |
| Trivanović · SHIRAZ | 2017 | 87 | awc-vienna |
| Deurić · Probus | 2016 | 87 | awc-vienna |
| Kovačević · Sauvignon | 2017 | 87 | awc-vienna |
| Belo Brdo · Riesling Black Label | 2017 | 87 | awc-vienna |
| Belo Brdo · Pinot Noir Rose | 2017 | 87 | awc-vienna |
| Belo Brdo · Merlot Black Label | 2016 | 87 | awc-vienna |
| Kovačević · Chardonnay | 2016 | 87 | awc-vienna |
| Belo Brdo · Riesling | 2016 | 87 | awc-vienna |
| Belo Brdo · Pinot Noir | 2016 | 87 | awc-vienna |
| Deurić · Enigma | 2015 | 87 | awc-vienna |
| Belo Brdo · Chardonnay Black Label | 2013 | 87 | awc-vienna |
| Belo Brdo · Riesling | 2013 | 87 | awc-vienna |
| Belo Brdo · Gewuerztraminer | 2013 | 87 | awc-vienna |
| Kovačević · Edicija S Aurelius | — | 86 | Wine-Searcher |
| Molovin · Inat Crveni | 2010 | 86 | decanter |
| Deurić · Princeps Probus | 2016 | 86 | decanter |
| Bikicki · Cu | 2018 | 86 | decanter |
| Kovačević · Edicija S Aurelius | 2017 | 86 | decanter |
| Erdevik · Marlon Delon Cabernet Sauvignon-Merlot | 2016 | 86 | decanter |
| Molovin · Inat Frankovka | 2019 | 86 | decanter |
| Molovin · Inat Limited Edition Rajnski Rizling | 2021 | 86 | decanter |
| Veritas Ćuković · Cuk | 2020 | 86 | biwc |
| Trivanović · Reserve Shiraz | 2018 | 86 | biwc |
| Vinum · Bermet Crveni | 2023 | 86 | biwc |
| Verkat · Frankovka | 2022 | 86 | biwc |
| Vinarija Djurdjic · Neoplanta | 2022 | 86 | biwc |
| Kiš · Verus Mister & Ja | 2023 | 86 | biwc |
| Molovin · Inat Rajnski Rizling | 2021 | 86 | biwc |
| Trivanović · OPTIMUS | 2023 | 86 | awc-vienna |
| Verkat · Grašac beli | 2023 | 86 | awc-vienna |
| Trivanović · LEX | 2021 | 86 | awc-vienna |
| Molovin · Rajnski Rizling | 2019 | 86 | awc-vienna |
| Verkat · Grasac beli | 2019 | 86 | awc-vienna |
| Trivanović · OPTIMUS | 2020 | 86 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2019 | 86 | awc-vienna |
| Belo Brdo · Riesling | 2018 | 86 | awc-vienna |
| Belo Brdo · Riesling Black Label | 2018 | 86 | awc-vienna |
| Trivanović · CABERNET SAUVIGNON | 2015 | 86 | awc-vienna |
| Deurić · Princeps Brut nature | 2015 | 86 | awc-vienna |
| Trivanović · Rosé | 2017 | 86 | awc-vienna |
| Belo Brdo · Riesling | 2017 | 86 | awc-vienna |
| Belo Brdo · Alma Mons Cuvee Rouge | 2015 | 86 | awc-vienna |
| Belo Brdo · Merlot Black Label | 2015 | 86 | awc-vienna |
| Deurić · Enigma | 2016 | 86 | awc-vienna |
| Trivanović · GRAŠAC | 2016 | 86 | awc-vienna |
| Kovačević · S Edition Chardonnay | 2013 | 86 | awc-vienna |
| Belo Brdo · Konfuzija | 2016 | 86 | awc-vienna |
| Belo Brdo · Riesling | 2015 | 86 | awc-vienna |
| Belo Brdo · Rosé | 2015 | 86 | awc-vienna |
| Vinum · Sauvignon Blanc | 2015 | 86 | awc-vienna |
| Vinum · Italijanski Rizling | 2015 | 86 | awc-vienna |
| Belo Brdo · Chardonnay | 2013 | 86 | awc-vienna |
| Belo Brdo · Petit Verdot | 2012 | 86 | awc-vienna |
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
| Trivanović · ROSE | 2019 | 85 | awc-vienna |
| Belo Brdo · Riesling Black Label | 2019 | 85 | awc-vienna |
| Veritas Ćuković · Sauvignon Blanc | 2019 | 85 | awc-vienna |
| Belo Brdo · Infuzija | 2016 | 85 | awc-vienna |
| Belo Brdo · Petit Verdot Black Label | 2012 | 85 | awc-vienna |
| Belo Brdo · Riesling Black Label | 2013 | 85 | awc-vienna |
| Belo Brdo · Petra Pinot Gris | 2013 | 85 | awc-vienna |
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
| Veritas Ćuković · Monte Karlovci | 2020 | 84 | biwc |
| Vinčić · Vincic | 2017 | 84 | biwc |
| Vinum · Mustra | 2022 | 84 | biwc |
| Šapat · Nera | 2022 | 84 | biwc |
| Trivanović · Shiraz Limited | 2016 | 84 | awc-vienna |
| Belo Brdo · Rosé | 2016 | 84 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2015 | 84 | awc-vienna |
| Belo Brdo · Sauvignon Blanc | 2013 | 84 | awc-vienna |
| Vinum · Sauvignon Blanc | 2012 | 84 | awc-vienna |
| Vinum · Italijanski Rizling Grasevina | 2012 | 84 | awc-vienna |
| Deurić · Chardonnay | 2015 | 83 | decanter |
| Erdevik · Roza Nostra | 2015 | 83 | decanter |
| Kovačević · S Edition Chardonnay | 2015 | 83 | decanter |
| Vinarija Djurdjic · Simonida Mlada | — | 83 | biwc |
| Vinarija Djurdjic · Cabernet Franc | 2021 | 83 | biwc |
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
| 2026 | бронза | bronza | The Sparkling Winery · The Extra Brut 2023 | 
| 2026 | бронза | bronza | The Sparkling Winery · The Blanc de Noirs 2023 | 
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
| 2025 | золото | zlato | Vinum · Grašac 26a 2021 | 
| 2025 | лучшее белое, местные сорта | 1 | Deurić · La Rem Morava 2023 | 
| 2025 | лучшее красное, органика, международные сорта | 1 | Dukay-Sagmeister · Kew Kadarka 2022 | 
| 2025 | одобрение | approval | Trivanović · OPTIMUS 2023 | 
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
| 2025 | серебро | srebro | Vinum · Grašac 26a 2023 | 
| 2025 | серебро | srebro | Vinum · Grašac 26a 2022 | 
| 2025 | серебро | srebro | Trivanović · Reserve Shiraz 2020 | 
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
| 2024 | бронза | bronza | Vinarija Djurdjic · Cabernet Franc 2021 | 
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
| 2024 | золото | zlato | Vinarija Djurdjic · Grasac 2022 | 
| 2024 | золото | zlato | Vinarija Djurdjic · Probus 2020 | 
| 2024 | золото | zlato | Kiš · Verus Grasac Beli 2023 | 
| 2024 | золото | zlato | Kiš · Verus GT 2023 | 
| 2024 | золото | zlato | Kiš · Biser crni | 
| 2024 | лучшая малая винодельня | 1 | Bikicki | 
| 2024 | лучшее белое, международные сорта | 1 | Kovačević · Edicija S Sauvignon 2021 | 
| 2024 | лучшее белое, органика, международные сорта | 1 | Dukay-Sagmeister · Kew Furmint 2020 | 
| 2024 | одобрение | approval | Verkat · Grašac beli 2023 | 
| 2024 | одобрение | approval | Verkat · Malvazija 2022 | 
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
| 2024 | серебро | srebro | Vinum · Bermet Crveni 2023 | 
| 2024 | серебро | srebro | Verkat · Frankovka 2022 | 
| 2024 | серебро | srebro | Vinarija Djurdjic · Neoplanta 2022 | 
| 2024 | серебро | srebro | Kiš · Verus Mister & Ja 2023 | 
| 2024 | серебро | srebro | Kiš · Verus Chardonnay 2023 | 
| 2024 | серебро | srebro | Molovin · Inat Rajnski Rizling 2021 | 
| 2024 | серебро | srebro | Vinum · Grašac 26a 2022 | 
| 2024 | серебро | srebro | Trivanović · PINOT GRIGIO 2023 | 
| 2024 | серебро | srebro | Trivanović · OPTIMUS 2023 | 
| 2024 | серебро | srebro | Trivanović · Reserve Shiraz 2020 | 
| 2024 | серебро | srebro | Molovin · Inat Rajnski Rizling 2021 | 
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
| 2023 | бронза | bronza | Veritas Ćuković · Monte Karlovci 2020 | 
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
| 2023 | золото | zlato | Trivanović · Reserve Shiraz 2018 | 
| 2023 | золото | zlato | Molovin · Rajnski Rizling 2021 | 
| 2023 | золото | zlato | Veritas Ćuković · Monte Karlovci 2020 | 
| 2023 | лучшее белое | 1 | Erdevik · Ex Cathedra Sauvignon Blanc 2021 | 
| 2023 | лучшее из местных сортов, белое | 1 | Vinčić · Grašac 2020 | 
| 2023 | серебро | srebro | Erdevik · Trianon 2018 | 
| 2023 | серебро | srebro | Deurić · Aksiom Beli 2019 | 
| 2023 | серебро | srebro | Erdevik · Marlon Delon 2017 | 
| 2023 | серебро | srebro | Deurić · Classic Chardonnay 2021 | 
| 2023 | серебро | srebro | Deurić · Severna Morava 2021 | 
| 2023 | серебро | srebro | Bikicki · Uncensored 2020 | 
| 2023 | серебро | srebro | Verkat · Malvazija Barrique 2021 | 
| 2023 | серебро | srebro | Verkat · Grašac Beli 4.0 2021 | 
| 2023 | серебро | srebro | Mačkov podrum · Camerlot 2021 | 
| 2023 | серебро | srebro | Molovin · Inat Frankovka 2020 | 
| 2023 | серебро | srebro | Veritas Ćuković · Domina Rose 2021 | 
| 2023 | серебро | srebro | Veritas Ćuković · Cuk 2020 | 
| 2023 | серебро | srebro | Trivanović · Reserve Shiraz 2018 | 
| 2023 | серебро | srebro | Trivanović · Reserve Cabernet Sauvignon 2017 | 
| 2023 | серебро | srebro | Veritas Ćuković · Bela Harmonija 2021 | 
| 2022 | Best of Show Serbia | trofej | Vinčić · White Reserve 2012 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Limited Edition Chardonnay 2020 | 
| 2022 | бронза | bronza | Erdevik · Geronimo 2020 | 
| 2022 | бронза | bronza | Deurić · Classic Chardonnay 2020 | 
| 2022 | бронза | bronza | Belo Brdo · Black Label Cabernet Sauvignon 2018 | 
| 2022 | бронза | bronza | Belo Brdo · Belo Brdo 2018 | 
| 2022 | бронза | bronza | Erdevik · Marlon Delon Cabernet Sauvignon-Merlot 2016 | 
| 2022 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2022 | бронза | bronza | Erdevik · Omnibus Lector Chardonnay 2016 | 
| 2022 | бронза | bronza | Mačkov podrum · Chardonnay 2021 | 
| 2022 | бронза | bronza | Vinčić · Anfora 2017 | 
| 2022 | двойное золото | dvojno-zlato | Vinum · Grašac 26a 2019 | 
| 2022 | двойное золото | dvojno-zlato | Vinčić · White Reserve 2012 | 
| 2022 | золото | zlato | Veritas Ćuković · Momentum Cabernet Sauvignon 2017 | 
| 2022 | золото | zlato | Verkat · Grašac beli 4.0 2021 | 
| 2022 | золото | zlato | Verkat · Malvazija 2021 | 
| 2022 | золото | zlato | Vinarija Djurdjic · Probus 2019 | 
| 2022 | золото | zlato | Vinarija Djurdjic · Rose Mlada Simonda 2021 | 
| 2022 | золото | zlato | Kiš · Kišov Grašac beli 2021 | 
| 2022 | золото | zlato | Mačkov podrum · Sauvignon Blanc 2021 | 
| 2022 | золото | zlato | Vinčić · Grašac Grand Fru 2020 | 
| 2022 | золото | zlato | Verkat · to Verkat Grašac beli 4.0 2021 | 
| 2022 | золото | zlato | Kovačević · Rizling 2021 | 
| 2022 | золото | zlato | Belo Brdo · Pinot Noir Black Label Limited Edition 2020 | 
| 2022 | золото | zlato | Belo Brdo · Bermet Black Label 2020 | 
| 2022 | золото | zlato | Belo Brdo · Bermet White Label 2020 | 
| 2022 | лучшее белое | 1 | Deurić · Aksiom beli 2019 | 
| 2022 | лучшее игристое | 1 | Deurić · The 2019 | 
| 2022 | одобрение | approval | Trivanović · OPTIMUS 2021 | 
| 2022 | одобрение | approval | Trivanović · LEX 2021 | 
| 2022 | одобрение | approval | Molovin · Rajnski Rizling 2019 | 
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
| 2022 | серебро | srebro | Trivanović · PINOT GRIGIO 2021 | 
| 2022 | серебро | srebro | Trivanović · Reserve Shiraz 2018 | 
| 2022 | серебро | srebro | Kovačević · Sauvignon 2021 | 
| 2022 | серебро | srebro | Kovačević · S Edition Sauvignon 2020 | 
| 2022 | серебро | srebro | Kovačević · S Edition Aurelius 2017 | 
| 2022 | серебро | srebro | Belo Brdo · Black Label Limited Edition Chardonnay 2020 | 
| 2022 | серебро | srebro | Belo Brdo · Riesling Black Label Limited Edition 2020 | 
| 2022 | серебро | srebro | Verkat · Roze 2021 | 
| 2021 | Best of Show Serbia | trofej | Vinum · Dina Sparkling Grašac 2018 | 
| 2021 | Trophy | trofej | Belo Brdo · Limited Edition Cabernet Sauvignon 2018 | 
| 2021 | бронза | bronza | Kovačević · Fresco Bianco Brut 2019 | 
| 2021 | бронза | bronza | Deurić · Princeps Probus 2016 | 
| 2021 | бронза | bronza | Bikicki · Cu 2018 | 
| 2021 | бронза | bronza | Deurić · Pinot Noir 2017 | 
| 2021 | бронза | bronza | Kovačević · Edicija S Aurelius 2017 | 
| 2021 | бронза | bronza | Bikicki · Makana 2016 | 
| 2021 | бронза | bronza | Belo Brdo · Limited Edition Cabernet Franc 2018 | 
| 2021 | бронза | bronza | Belo Brdo · Limited Edition Cabernet Sauvignon 2018 | 
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
| 2021 | золото | zlato | Trivanović · Reserve Shiraz 2017 | 
| 2021 | золото | zlato | Belo Brdo · Limited Edition Decade 2018 | 
| 2021 | золото | zlato | Belo Brdo · Limited Edition Cabernet Sauvignon 2018 | 
| 2021 | золото | zlato | Belo Brdo · Marselan Limited Edition 2018 | 
| 2021 | золото | zlato | Belo Brdo · Petit Verdot Limited Edition 2020 | 
| 2021 | одобрение | approval | Verkat · Grasac beli 2019 | 
| 2021 | одобрение | approval | Trivanović · OPTIMUS 2020 | 
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
| 2021 | серебро | srebro | Kiš · Kišov Grašac Beli 2020 | 
| 2021 | серебро | srebro | Trivanović · Reserve Cabernet Sauvignon 2017 | 
| 2021 | серебро | srebro | Trivanović · SHIRAZ 2018 | 
| 2021 | серебро | srebro | Kiš · Kišov Rosé 2020 | 
| 2021 | серебро | srebro | Belo Brdo · Sauvignon Blanc 2020 | 
| 2021 | серебро | srebro | Belo Brdo · Rosé 2020 | 
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
| 2020 | золото | zlato | Belo Brdo · Cabernet Franc Black Label Limited Edition 2018 | 
| 2020 | лучшая малая винодельня | 1 | Chichateau | 
| 2020 | лучшая молодая винодельня | 1 | Deurić | 
| 2020 | лучшее белое | 1 | Chichateau · Chi Chardonnay 2016 | 
| 2020 | одобрение | approval | Trivanović · ROSE 2019 | 
| 2020 | одобрение | approval | Trivanović · Reserve Shiraz 2017 | 
| 2020 | одобрение | approval | Belo Brdo · Sauvignon Blanc 2019 | 
| 2020 | одобрение | approval | Belo Brdo · Riesling Black Label 2019 | 
| 2020 | одобрение | approval | Veritas Ćuković · Sauvignon Blanc 2019 | 
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
| 2020 | серебро | srebro | Bikicki · S/O 2017 | 
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
| 2020 | серебро | srebro | Deurić · Probus 276 2018 | 
| 2020 | серебро | srebro | Trivanović · CHARDONNAY BARRIQUE 2018 | 
| 2020 | серебро | srebro | Trivanović · PINOT GRIGIO 2019 | 
| 2020 | серебро | srebro | Trivanović · OPTIMUS 2019 | 
| 2020 | серебро | srebro | Trivanović · CABERNET SAUVIGNON 2016 | 
| 2020 | серебро | srebro | Trivanović · Reserve Cabernet Sauvignon 2017 | 
| 2020 | серебро | srebro | Trivanović · SHIRAZ 2018 | 
| 2020 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2019 | 
| 2020 | серебро | srebro | Belo Brdo · Alma Mons Black Label 2017 | 
| 2020 | серебро | srebro | Belo Brdo · Alma Mons Black Label 2018 | 
| 2020 | серебро | srebro | Belo Brdo · Decade 2018 | 
| 2020 | серебро | srebro | Belo Brdo · Black Label Cabernet Sauvignon 2018 | 
| 2020 | серебро | srebro | Belo Brdo · Cabernet Franc Black Label 2018 | 
| 2020 | серебро | srebro | Belo Brdo · Petit Verdot 2018 | 
| 2020 | серебро | srebro | Vinarija Djurdjic · Cabernet Franc 2017 | 
| 2019 | Orange Wine Trophy | trofej | Bikicki · Uncensored 2017 | 
| 2019 | бронза | bronza | Deurić · The Brut 2015 | 
| 2019 | бронза | bronza | Deurić · Aksiom 2016 | 
| 2019 | бронза | bronza | Deurić · Talas crveni 2015 | 
| 2019 | золото | zlato | Bikicki · Pinotte 2015 | 
| 2019 | золото | zlato | Bikicki · Cu 2017 | 
| 2019 | золото | zlato | Deurić · Pinot Noir 2017 | 
| 2019 | золото | zlato | Kiš · Grasac beli 2017 | 
| 2019 | золото | zlato | Belo Brdo · Chardonnay 2018 | 
| 2019 | золото | zlato | Belo Brdo · Cabernet Franc Black Label 2017 | 
| 2019 | лучшая малая винодельня | 1 | Bikicki | 
| 2019 | лучшее игристое | 1 | Deurić · Princeps Brut Nature 2015 | 
| 2019 | одобрение | approval | Belo Brdo · Sauvignon Blanc 2018 | 
| 2019 | одобрение | approval | Belo Brdo · Riesling 2018 | 
| 2019 | одобрение | approval | Belo Brdo · Riesling Black Label 2018 | 
| 2019 | одобрение | approval | Trivanović · ROSE 2018 | 
| 2019 | одобрение | approval | Trivanović · CABERNET SAUVIGNON 2015 | 
| 2019 | одобрение | approval | Trivanović · CABERNET SAUVIGNON LIMITED 2016 | 
| 2019 | одобрение | approval | Deurić · Princeps Brut nature 2015 | 
| 2019 | отмечено | commended | Deurić · Probus 276 2017 | 
| 2019 | отмечено | commended | Deurić · Pinot Noir 2017 | 
| 2019 | отмечено | commended | Molovin · Vista Hill Selection 2017 | 
| 2019 | отмечено | commended | Deurić · Aksiom 2016 | 
| 2019 | серебро | srebro | Deurić · Talas Crveni 2017 | 
| 2019 | серебро | srebro | Molovin · Vista Hill Red Reserve 2010 | 
| 2019 | серебро | srebro | Deurić · Princeps Brut Nature 2015 | 
| 2019 | серебро | srebro | Bikicki · Makana 2016 | 
| 2019 | серебро | srebro | Vinarija Šijački · Rizling italijanski 2018 | 
| 2019 | серебро | srebro | Vinarija Šijački · Seduša 2017 | 
| 2019 | серебро | srebro | Deurić · Probus 276 2017 | 
| 2019 | серебро | srebro | Deurić · Urban Rose 2018 | 
| 2019 | серебро | srebro | Deurić · Classic Chardonnay 2018 | 
| 2019 | серебро | srebro | Deurić · Sauvignon blanc 2017 | 
| 2019 | серебро | srebro | Vinarija Djurdjic · Sauvignon Blanc 2018 | 
| 2019 | серебро | srebro | Vinarija Djurdjic · Cabernet Franc 2016 | 
| 2019 | серебро | srebro | Kiš · Bermet 2012 | 
| 2019 | серебро | srebro | Vinarija Šijački · Neoplanta 2017 | 
| 2019 | серебро | srebro | Kiš · Rose 2018 | 
| 2019 | серебро | srebro | Kiš · Bermet 2012 | 
| 2019 | серебро | srebro | Deurić · Probus 276 2017 | 
| 2019 | серебро | srebro | Kovačević · Chardonnay 2018 | 
| 2019 | серебро | srebro | Kovačević · Rizling 2017 | 
| 2019 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2018 | 
| 2019 | серебро | srebro | Belo Brdo · Alma Mons 2017 | 
| 2019 | серебро | srebro | Belo Brdo · Alma Mons 2016 | 
| 2019 | серебро | srebro | Belo Brdo · Pinot Noir Black Label 2017 | 
| 2019 | серебро | srebro | Belo Brdo · Merlot Black label 2017 | 
| 2019 | серебро | srebro | Belo Brdo · Rosé 2018 | 
| 2019 | серебро | srebro | Kiš · Kišova Misterija Riesling 2016 | 
| 2019 | серебро | srebro | Kiš · Kišov rosé 2018 | 
| 2019 | серебро | srebro | Trivanović · CHARDONNAY BARRIQUE 2017 | 
| 2019 | серебро | srebro | Trivanović · PINOT GRIGIO 2018 | 
| 2019 | серебро | srebro | Trivanović · OPTIMUS 2018 | 
| 2019 | серебро | srebro | Trivanović · CABERNET SAUVIGNON LIMITED 2017 | 
| 2019 | серебро | srebro | Trivanović · SHIRAZ 2017 | 
| 2019 | серебро | srebro | Trivanović · SHIRAZ LIMITED 2017 | 
| 2018 | бронза | bronza | Molovin · Inat Crveni 2010 | 
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
| 2018 | золото | zlato | Kovačević · Cuvee Piquant 2017 | 
| 2018 | золото | zlato | Belo Brdo · Chardonnay 2017 | 
| 2018 | золото | zlato | Belo Brdo · Chardonnay Black Label 2017 | 
| 2018 | золото | zlato | Belo Brdo · Marselan Black Label 2015 | 
| 2018 | золото | zlato | Belo Brdo · Bermet Black Label 2012 | 
| 2018 | одобрение | approval | Trivanović · Rosé 2017 | 
| 2018 | одобрение | approval | Trivanović · Shiraz Limited 2016 | 
| 2018 | одобрение | approval | Belo Brdo · Riesling 2017 | 
| 2018 | одобрение | approval | Belo Brdo · Riesling Black Label 2017 | 
| 2018 | одобрение | approval | Belo Brdo · Alma Mons Cuvee Rouge 2015 | 
| 2018 | одобрение | approval | Belo Brdo · Merlot Black Label 2015 | 
| 2018 | одобрение | approval | Belo Brdo · Merlot Black Label 2016 | 
| 2018 | одобрение | approval | Deurić · Enigma 2016 | 
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
| 2018 | серебро | srebro | Deurić · Probus 2016 | 
| 2018 | серебро | srebro | Trivanović · Cabernet sauvignon 2015 | 
| 2018 | серебро | srebro | Kovačević · Chardonnay 2017 | 
| 2018 | серебро | srebro | Kovačević · S Edition Chardonnay 2015 | 
| 2018 | серебро | srebro | Kovačević · Sauvignon 2017 | 
| 2018 | серебро | srebro | Kovačević · Aurelius 2016 | 
| 2018 | серебро | srebro | Belo Brdo · Sauvignon Blanc 2017 | 
| 2018 | серебро | srebro | Belo Brdo · Pinot Noir Rose 2017 | 
| 2018 | серебро | srebro | Belo Brdo · Alma Mons Black Label Reserve 2015 | 
| 2018 | серебро | srebro | Belo Brdo · Black Label Cabernet Sauvignon 2015 | 
| 2018 | серебро | srebro | Belo Brdo · Cabernet Franc Black Label 2015 | 
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
| 2017 | золото | zlato | Belo Brdo · Cabernet Sauvignon 2012 | 
| 2017 | золото | zlato | Molovin · Plavi Princip Blaufränkisch 2013 | 
| 2017 | одобрение | approval | Trivanović · GRAŠAC 2016 | 
| 2017 | одобрение | approval | Kovačević · Chardonnay 2016 | 
| 2017 | одобрение | approval | Kovačević · S Edition Chardonnay 2013 | 
| 2017 | одобрение | approval | Belo Brdo · Infuzija 2016 | 
| 2017 | одобрение | approval | Belo Brdo · Konfuzija 2016 | 
| 2017 | одобрение | approval | Belo Brdo · Rosé 2016 | 
| 2017 | одобрение | approval | Belo Brdo · Pinot Noir 2016 | 
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
| 2017 | серебро | srebro | Kovačević · Brut 2010 | 
| 2017 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2016 | 
| 2017 | серебро | srebro | Belo Brdo · Sauvignon Blanc 2016 | 
| 2017 | серебро | srebro | Belo Brdo · Riesling 2016 | 
| 2017 | серебро | srebro | Belo Brdo · Petit Verdot 2015 | 
| 2017 | серебро | srebro | Belo Brdo · Reserve Music Edition 2013 | 
| 2017 | серебро | srebro | Vinum · Italijanski Rizling 2016 | 
| 2016 | Rose Wine Trophy | trofej | Vinum · Rose 2015 | 
| 2016 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2016 | бронза | bronza | Molovin · Inat Crveni 2010 | 
| 2016 | бронза | bronza | Deurić · Enigma 2015 | 
| 2016 | бронза | bronza | Deurić · Talas Crveni 2015 | 
| 2016 | бронза | bronza | Deurić · Talas Crveni 2014 | 
| 2016 | бронза | bronza | Kovačević · Chardonnay 2015 | 
| 2016 | бронза | bronza | Kiš · Kišov Bermet Belo | 
| 2016 | золото | zlato | Deurić · Chardonnay 2015 | 
| 2016 | золото | zlato | Deurić · Gewurztraminer 2015 | 
| 2016 | золото | zlato | Deurić · Avangarda 2015 | 
| 2016 | золото | zlato | Deurić · Talas Beli 2014 | 
| 2016 | золото | zlato | Bjelica · Saga 2015 | 
| 2016 | золото | zlato | Bjelica · Babaroga Penušavac 2014 | 
| 2016 | золото | zlato | Belo Brdo · Alma Mons 2013 | 
| 2016 | золото | zlato | Belo Brdo · Black Label Cabernet Sauvignon 2013 | 
| 2016 | золото | zlato | Belo Brdo · Marselan 2013 | 
| 2016 | одобрение | approval | Belo Brdo · Sauvignon Blanc 2015 | 
| 2016 | одобрение | approval | Belo Brdo · Riesling 2015 | 
| 2016 | одобрение | approval | Belo Brdo · Rosé 2015 | 
| 2016 | одобрение | approval | Belo Brdo · Petit Verdot Black Label 2012 | 
| 2016 | одобрение | approval | Vinum · Sauvignon Blanc 2015 | 
| 2016 | одобрение | approval | Vinum · Italijanski Rizling 2015 | 
| 2016 | отмечено | commended | Molovin · Inat 2012 | 
| 2016 | отмечено | commended | Kovačević · Sauvignon 2012 | 
| 2016 | отмечено | commended | Kiš · Misterija 2011 | 
| 2016 | серебро | srebro | Belo Brdo · Chardonnay 2015 | 
| 2016 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2015 | 
| 2016 | серебро | srebro | Molovin · Plavi Princip 2013 | 
| 2016 | серебро | srebro | Bjelica · Babaroga 2015 | 
| 2016 | серебро | srebro | Deurić · Talas Beli 2015 | 
| 2016 | серебро | srebro | Deurić · Urban Rose 2015 | 
| 2016 | серебро | srebro | Kovačević · Aurelius R 2012 | 
| 2016 | серебро | srebro | Kovačević · Rosetto 2015 | 
| 2016 | серебро | srebro | Belo Brdo · Belo Brdo 2013 | 
| 2016 | серебро | srebro | Belo Brdo · Merlot Black Label 2013 | 
| 2016 | серебро | srebro | Belo Brdo · Cabernet Franc Black Label 2013 | 
| 2016 | серебро | srebro | Molovin · Plavi Princip 2013 | 
| 2016 | серебро | srebro | Vinum · Rosé 2015 | 
| 2016 | серебро | srebro | Deurić · Enigma 2015 | 
| 2015 | бронза | bronza | Belo Brdo · Cabernet Franc 2012 | 
| 2015 | бронза | bronza | Belo Brdo · Alma Mons 2012 | 
| 2015 | бронза | bronza | Kovačević · Aurelius 2012 | 
| 2015 | бронза | bronza | Kiš · Kišova Misterija Polusuvo 2011 | 
| 2015 | бронза | bronza | Kiš · Kisov Bermet | 
| 2015 | золото | zlato | Kiš · Kišova Misterija Polusuvo 2011 | 
| 2015 | золото | zlato | Kiš · Kišov Bermet Belo | 
| 2015 | одобрение | approval | Belo Brdo · Riesling Black Label 2013 | 
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
| 2015 | серебро | srebro | Belo Brdo · Pinot Noir Reserve 2012 | 
| 2014 | Rose Wine Trophy | trofej | Kiš · Kišov Rose 2013 | 
| 2014 | бронза | bronza | Bjelica · Saga 2013 | 
| 2014 | бронза | bronza | Bjelica · Graffiti 2013 | 
| 2014 | бронза | bronza | Kiš · Kišov Bermet 2014 | 
| 2014 | золото | zlato | Kiš · Kišov Rose 2013 | 
| 2014 | золото | zlato | Kiš · Bermet Beli | 
| 2014 | золото | zlato | Belo Brdo · Cabernet Sauvignon 2011 | 
| 2014 | одобрение | approval | Belo Brdo · Chardonnay 2013 | 
| 2014 | одобрение | approval | Belo Brdo · Petra Pinot Gris 2013 | 
| 2014 | одобрение | approval | Belo Brdo · Sauvignon Blanc 2013 | 
| 2014 | одобрение | approval | Belo Brdo · Riesling 2013 | 
| 2014 | одобрение | approval | Belo Brdo · Petit Verdot 2012 | 
| 2014 | одобрение | approval | Vinum · Sauvignon Blanc 2012 | 
| 2014 | одобрение | approval | Vinum · Italijanski Rizling Grasevina 2012 | 
| 2014 | отмечено | commended | Kovačević · Chardonnay 2012 | 
| 2014 | отмечено | commended | Bjelica · Graffiti 2012 | 
| 2014 | отмечено | commended | Kovačević · Rosetto 2013 | 
| 2014 | серебро | srebro | Kiš · Misterija Kišova 2011 | 
| 2014 | серебро | srebro | Belo Brdo · Chardonnay Black Label 2013 | 
| 2014 | серебро | srebro | Belo Brdo · Alma Mons White 2013 | 
| 2014 | серебро | srebro | Belo Brdo · Gewuerztraminer 2013 | 
| 2014 | серебро | srebro | Belo Brdo · Alma Mons 2012 | 
| 2014 | серебро | srebro | Belo Brdo · Alma Mons Reserve 2011 | 
| 2014 | серебро | srebro | Belo Brdo · Cabernet Franc 2012 | 
| 2014 | серебро | srebro | Belo Brdo · Marselan 2012 | 
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
| Zvonko Bogdan · Icon Campana Rubinus Merlot, Caberndet Franc | 2013 | 90 | awc-vienna |
| Vinarija Petra · Rosé | 2019 | 89 | Falstaff |
| Zvonko Bogdan · Život Teče | 2016 | 89 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2018 | 89 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2022 | 89 | decanter |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 2020 | 89 | decanter |
| Zvonko Bogdan · Cuvée No.1 | 2024 | 89 | decanter |
| Zvonko Bogdan · Sauvignon Blanc | 2015 | 89 | awc-vienna |
| Vinarija Petra · Pinot Grigio | 2017 | 88 | Falstaff |
| Zvonko Bogdan · Cuvée No.1 | 2015 | 88 | decanter |
| Zvonko Bogdan · Chardonnay | 2019 | 88 | decanter |
| Zvonko Bogdan · Sauvignon Blanc | 2021 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Albus | 2020 | 88 | decanter |
| Zvonko Bogdan · Cuvee No1 | 2021 | 88 | decanter |
| Zvonko Bogdan · Merlot | 2022 | 88 | decanter |
| Zvonko Bogdan · Icon Campana Rubimus | 2019 | 88 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2022 | 88 | decanter |
| Vinarija Petra · Desertni Traminac | 2021 | 88 | awc-vienna |
| Vinarija Petra · Orange | 2021 | 88 | awc-vienna |
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
| Vinarija Petra · Rosé | 2023 | 87 | awc-vienna |
| Zvonko Bogdan · Chardonnay | 2015 | 86 | decanter |
| Zvonko Bogdan · Pinot Blanc | 2018 | 86 | decanter |
| Tonković · Rapsodija Kadarka | 2019 | 86 | decanter |
| Vinarija Petra · Rose & Co | 2023 | 86 | awc-vienna |
| Zvonko Bogdan · Pinot Blanc | 2013 | 86 | awc-vienna |
| Zvonko Bogdan · Sauvignon Blanc | 2013 | 86 | awc-vienna |
| Zvonko Bogdan · Rose Sec | 2016 | 85 | decanter |
| Tonković · Fantazija | 2013 | 85 | decanter |
| Vinarija Petra · Pinot Noir | 2021 | 85 | awc-vienna |

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
| 2025 | одобрение | approval | Vinarija Petra · Rosé 2023 | 
| 2025 | одобрение | approval | Vinarija Petra · Pinot Noir 2021 | 
| 2025 | одобрение | approval | Vinarija Petra · Desertni Traminac 2021 | 
| 2025 | одобрение | approval | Vinarija Petra · Rose & Co 2023 | 
| 2025 | одобрение | approval | Vinarija Petra · Orange 2021 | 
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
| 2016 | серебро | srebro | Zvonko Bogdan · Icon Campana Rubinus Merlot, Caberndet Franc 2013 | 
| 2016 | серебро | srebro | Zvonko Bogdan · Sauvignon Blanc 2015 | 
| 2015 | бронза | bronza | Zvonko Bogdan · Cuvée No.1 2012 | 
| 2015 | бронза | bronza | Tonković · Rapsodija Kadarka 2012 | 
| 2015 | отмечено | commended | Tonković · Kadarka Rosé 2014 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Rosé Sec 2014 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Icon Campana 2013 | 
| 2015 | отмечено | commended | Tonković · Fantazija Kadarka 2011 | 
| 2015 | отмечено | commended | Zvonko Bogdan · Zivot Tece 2013 | 
| 2015 | отмечено | commended | Tonković · Icon Kadarka 2011 | 
| 2015 | серебро | srebro | Zvonko Bogdan · Sauvignon blanc 2014 | 
| 2014 | бронза | bronza | Tonković · Fantazija Kadarka 2011 | 
| 2014 | бронза | bronza | Zvonko Bogdan · Pinot Blanc 2013 | 
| 2014 | бронза | bronza | Tonković · Kadarka 2013 | 
| 2014 | одобрение | approval | Zvonko Bogdan · Pinot Blanc 2013 | 
| 2014 | одобрение | approval | Zvonko Bogdan · Sauvignon Blanc 2013 | 
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
| Vinarija Drašković · Mahago Frankovka | 2019 | 92 | biwc |
| Vinarija Drašković · Mahago | 2019 | 90 | decanter |
| Vinarija Drašković · Beli Pinot | 2020 | 90 | decanter |
| Vinarija Drašković · Beli Pinot | 2021 | 90 | decanter |
| Vinarija Drašković · Frankovka Rezerva | 2018 | 90 | decanter |
| Rnjak · CUVEE DE RGNAC | 2019 | 90 | biwc |
| Vinarija Drašković · Muskat Otonel | 2020 | 90 | awc-vienna |
| Vinarija Drašković · Horizont Chardonnay | 2021 | 89 | decanter |
| Vinarija Drašković · Classic Chardonnay | 2022 | 89 | biwc |
| Rnjak · PINOT NOIR | 2021 | 89 | biwc |
| Vinarija Drašković · Burgundac beli Classic | 2021 | 89 | awc-vienna |
| Rnjak · CHARDONNAY | 2016 | 89 | awc-vienna |
| Vinarija Drašković · Mahago | 2017 | 88 | decanter |
| Vinarija Drašković · Beli Pinot Authentic | 2020 | 88 | awc-vienna |
| Rnjak · CHARDONNAY | 2018 | 88 | awc-vienna |
| Vinarija Drašković · Beli Pinot | 2019 | 87 | decanter |
| Vinarija Drašković · Burgundac Beli | 2021 | 87 | decanter |
| Vinarija Drašković · Mahago Frankovka | 2021 | 87 | decanter |
| Vinarija Drašković · Beli Pinot Authentic | 2020 | 87 | biwc |
| Vinarija Drašković · Frankovka rezerva | 2018 | 87 | biwc |
| Rnjak · CRVENI PUŽ | 2019 | 87 | biwc |
| Galot · Chardonnay | 2015 | 87 | awc-vienna |
| Rnjak · PINOT NOIR | 2019 | 86 | biwc |
| Rnjak · CHARDONNAY | 2023 | 86 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2022 | 86 | biwc |
| Vinarija Drašković · Ruža Vetrova Muskat Otonel | 2020 | 86 | awc-vienna |
| Rnjak · SAUVIGNON BLANC | 2018 | 86 | awc-vienna |
| Rnjak · PINOT NOIR | 2015 | 86 | awc-vienna |
| Galot · Balerina Traminer Tamjanika yellow | 2015 | 86 | awc-vienna |
| Rnjak · MERLOT | 2015 | 86 | awc-vienna |
| Rnjak · CUVEE DE RGNAC | 2018 | 85 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2022 | 85 | biwc |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2022 | 85 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2022 | 85 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2022 | 85 | biwc |
| Rnjak · CHARDONNAY | 2015 | 85 | awc-vienna |
| Rnjak · SAUVIGNON BLANC | 2015 | 85 | awc-vienna |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2020 | 84 | biwc |
| Vinarija Coka · Grof Lederer MERLOT | 2021 | 84 | biwc |
| Rnjak · SAUVIGNON BLANC | 2021 | 84 | biwc |
| Vinarija Coka · Grof Lederer CABERNET SAUVIGNON | 2022 | 84 | biwc |
| Vinarija Coka · Muštuluk Crveni | 2020 | 82 | biwc |
| Rnjak · CHARDONNAY | 2021 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2025 | бронза | bronza | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2022 | 
| 2025 | серебро | srebro | Vinarija Coka · Muštuluk Crveni 2022 | 
| 2025 | серебро | srebro | Vinarija Coka · Grof Lederer MERLOT 2022 | 
| 2024 | бронза | bronza | Vinarija Drašković · Mahago Frankovka 2021 | 
| 2024 | золото | zlato | Rnjak · CUVEE DE RGNAC 2019 | 
| 2024 | золото | zlato | Rnjak · PINOT NOIR 2021 | 
| 2024 | серебро | srebro | Vinarija Drašković · Beli Pinot 2021 | 
| 2024 | серебро | srebro | Vinarija Drašković · Frankovka Rezerva 2018 | 
| 2024 | серебро | srebro | Rnjak · CRVENI PUŽ 2019 | 
| 2024 | серебро | srebro | Rnjak · CHARDONNAY 2023 | 
| 2024 | серебро | srebro | Vinarija Coka · Grof Lederer MERLOT 2022 | 
| 2024 | серебро | srebro | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2022 | 
| 2024 | серебро | srebro | Vinarija Coka · Muštuluk Crveni 2022 | 
| 2023 | бронза | bronza | Vinarija Drašković · Horizont Chardonnay 2021 | 
| 2023 | бронза | bronza | Vinarija Drašković · Burgundac Beli 2021 | 
| 2023 | бронза | bronza | Vinarija Coka · Grof Lederer MERLOT 2021 | 
| 2023 | бронза | bronza | Vinarija Coka · Muštuluk Crveni 2020 | 
| 2023 | бронза | bronza | Rnjak · CHARDONNAY 2021 | 
| 2023 | бронза | bronza | Rnjak · SAUVIGNON BLANC 2021 | 
| 2023 | золото | zlato | Vinarija Drašković · Classic Chardonnay 2022 | 
| 2023 | золото | zlato | Vinarija Drašković · Mahago Frankovka 2019 | 
| 2023 | серебро | srebro | Vinarija Drašković · Mahago 2019 | 
| 2023 | серебро | srebro | Vinarija Drašković · Beli Pinot 2020 | 
| 2023 | серебро | srebro | Vinarija Coka · Grof Lederer CABERNET SAUVIGNON 2020 | 
| 2023 | серебро | srebro | Vinarija Drašković · Beli Pinot Authentic 2020 | 
| 2023 | серебро | srebro | Vinarija Drašković · Frankovka rezerva 2018 | 
| 2023 | серебро | srebro | Rnjak · CUVEE DE RGNAC 2018 | 
| 2023 | серебро | srebro | Rnjak · PINOT NOIR 2019 | 
| 2022 | бронза | bronza | Vinarija Drašković · Beli Pinot Authentic 2020 | 
| 2022 | золото | zlato | Vinarija Drašković · Ruža vetrova 2020 | 
| 2022 | одобрение | approval | Vinarija Drašković · Ruža Vetrova Muskat Otonel 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Grof Lederer Merlot 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Grof Lederer Cabernet Sauvignon 2020 | 
| 2022 | серебро | srebro | Vinarija Coka · Muštuluk 2020 | 
| 2022 | серебро | srebro | Vinarija Drašković · Burgundac beli Classic 2021 | 
| 2022 | серебро | srebro | Vinarija Drašković · Classic Chardonnay 2021 | 
| 2022 | серебро | srebro | Vinarija Drašković · Burgundac beli Classic 2021 | 
| 2022 | серебро | srebro | Vinarija Drašković · Beli Pinot Authentic 2020 | 
| 2022 | серебро | srebro | Vinarija Drašković · Muskat Otonel 2020 | 
| 2021 | бронза | bronza | Vinarija Drašković · Beli Pinot 2019 | 
| 2021 | бронза | bronza | Vinarija Drašković · Mahago 2017 | 
| 2021 | бронза | bronza | Vinarija Drašković · Mahago 2017 | 
| 2021 | бронза | bronza | Vinarija Coka · Grof Lederer Cabernet Sauvignon 2019 | 
| 2021 | золото | zlato | Vinarija Coka · Grof Lederer Merlot 2019 | 
| 2021 | серебро | srebro | Vinarija Drašković · Beli Pinot 2019 | 
| 2021 | серебро | srebro | Vinarija Drašković · Ruža Vetrova 2018 | 
| 2021 | серебро | srebro | Vinarija Drašković · Muskat Otonel 2019 | 
| 2020 | бронза | bronza | Vinarija Coka · Lederer Merlot 2018 | 
| 2020 | бронза | bronza | Rnjak · Cabernet Sauvignon 2017 | 
| 2020 | бронза | bronza | Rnjak · Chardonnay 2018 | 
| 2020 | золото | zlato | Rnjak · Merlot 2017 | 
| 2020 | золото | zlato | Rnjak · Pinot Noir 2017 | 
| 2020 | серебро | srebro | Rnjak · Sauvignon blanc 2018 | 
| 2019 | Best of Show Serbia | trofej | Rnjak · Merlot 2015 | 
| 2019 | золото | zlato | Rnjak · Cabernet Sauvignon 2015 | 
| 2019 | золото | zlato | Rnjak · Pinot Noir 2015 | 
| 2019 | одобрение | approval | Rnjak · SAUVIGNON BLANC 2018 | 
| 2019 | одобрение | approval | Rnjak · PINOT NOIR 2015 | 
| 2019 | серебро | srebro | Rnjak · Chardonnay 2018 | 
| 2019 | серебро | srebro | Rnjak · Sauvignon Blanc 2018 | 
| 2019 | серебро | srebro | Rnjak · CHARDONNAY 2018 | 
| 2018 | серебро | srebro | Rnjak · Cabernet Sauvignon 2015 | 
| 2017 | одобрение | approval | Galot · Balerina Traminer Tamjanika yellow 2015 | 
| 2017 | одобрение | approval | Galot · Chardonnay 2015 | 
| 2017 | одобрение | approval | Rnjak · MERLOT 2015 | 
| 2017 | серебро | srebro | Rnjak · CHARDONNAY 2016 | 
| 2016 | бронза | bronza | Rnjak · CHARDONNAY 2015 | 
| 2016 | одобрение | approval | Rnjak · CHARDONNAY 2015 | 
| 2016 | одобрение | approval | Rnjak · SAUVIGNON BLANC 2015 | 

## Шумадия

| Вино | Урожай | Балл | Источник |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 2022 | 97 | decanter |
| Matijašević Vinogradi · SoviNoa Fumé Blanc | 2020 | 96 | decanter |
| Arsenijević · Kaberne | 2021 | 96 | biwc |
| Matijašević Vinogradi · SoviNoa | 2019 | 95 | decanter |
| Aleksandrović · Regent Reserve | 2018 | 95 | decanter |
| Matijašević Vinogradi · Tri Doline | 2020 | 95 | decanter |
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 2021 | 95 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 95 | decanter |
| Tarpoš · Prokupac | 2023 | 95 | decanter |
| Despotika · Krunski Dokaz | 2017 | 95 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 95 | decanter |
| Tarpoš · Merlot | 2021 | 95 | biwc |
| Matijašević Vinogradi · SoviNoa Fumé Blanc | 2020 | 94 | Falstaff |
| Aleksandrović · Trijumf Gold | 2022 | 94 | Falstaff |
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 2021 | 94 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 94 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2020 | 93 | Falstaff |
| Matijašević Vinogradi · SoviNoa Sauvignon Blanc | 2021 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection Sauvignon Blanc | 2021 | 93 | Falstaff |
| Despotika · Krunski Dokas (The Key Evidence) Grand Reserve | 2017 | 93 | Falstaff |
| Aleksandrović · VOŽD | 2017 | 93 | Falstaff |
| Matijašević Vinogradi · Belina | 2022 | 93 | Falstaff |
| Aleksandrović · Trijumf Selection | 2021 | 93 | Falstaff |
| Matijašević Vinogradi · Tri Doline Merlot | 2020 | 93 | Falstaff |
| Aleksandrović · Trijumf Chardonnay Brut | 2018 | 93 | Falstaff |
| Aleksandrović · Trijumf Terroir | 2022 | 93 | Falstaff |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 93 | Falstaff |
| Aleksandrović · Trijumf Noir | 2010 | 93 | decanter |
| Matijašević Vinogradi · Čukundeda Prokupac | 2019 | 93 | decanter |
| Aleksandrović · Trijumf Gold | 2023 | 93 | decanter |
| Despotika · Morava Barik | 2022 | 93 | decanter |
| Eden · Velvet | 2020 | 93 | decanter |
| Despotika · Neizbrisivi trag | 2021 | 93 | biwc |
| Aleksandrović · Trijumf Noir Brut | 2010 | 92 | Falstaff |
| Despotika · Nemir (Turbulence) Rosé | — | 92 | Falstaff |
| Aleksandrović · Prokupac | 2021 | 92 | Falstaff |
| Matijašević Vinogradi · Čukundeda Prokupac | 2020 | 92 | Falstaff |
| Aleksandrović · Trijumf Prokupac | 2020 | 92 | Falstaff |
| Matijašević Vinogradi · Belina | 2020 | 92 | Falstaff |
| Matijašević Vinogradi · Prokupac Cukundeda Superiore | 2019 | 92 | Falstaff |
| Despotika · Trag (The Clue) Merlot | 2019 | 92 | Falstaff |
| Aleksandrović · Trijumf Rosé Brut | 2019 | 92 | Falstaff |
| Aleksandrović · Prokupac | 2019 | 92 | decanter |
| Aleksandrović · Vožd Cabernet Sauvignon | 2017 | 92 | decanter |
| Matijašević Vinogradi · Sovinoa Sauvignon Blanc | 2021 | 92 | decanter |
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
| Matijašević Vinogradi · Sovinoa Sauvignon Blanc | 2020 | 91 | decanter |
| Matijašević Vinogradi · Čukundeda Superiore | 2019 | 91 | decanter |
| Matijašević Vinogradi · Cukundeda Prokupac | 2021 | 91 | decanter |
| Aleksandrović · Regent Reserve | 2019 | 91 | decanter |
| Matijašević Vinogradi · Belina | 2022 | 91 | decanter |
| Despotika · Morava barik | 2022 | 91 | awc-vienna |
| Despotika · Dokaz Šumadija | 2021 | 91 | awc-vienna |
| Radovanović · Réserve Cabernet Sauvignon | — | 90 | Wine-Searcher |
| Radovanović · Cabernet Sauvignon Classique | 2015 | 90 | Tastings.com |
| Matijašević Vinogradi · Belina Inferno | 2022 | 90 | Falstaff |
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
| Matijašević Vinogradi · Belina | 2021 | 90 | decanter |
| Aleksandrović · Prokupac | 2020 | 90 | decanter |
| Tarpoš · Tamjanika | 2023 | 90 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 90 | decanter |
| Aleksandrović · Regent Reserve | 2020 | 90 | decanter |
| Aleksandrović · Trijumf Rosé Brut | 2019 | 90 | decanter |
| Despotika · Nebo | 2023 | 90 | biwc |
| Despotika · Morava | 2022 | 90 | biwc |
| Tarpoš · Cabernet Sauvignon | 2021 | 90 | biwc |
| Matijašević Vinogradi · Cukundeda | 2021 | 90 | biwc |
| Matijašević Vinogradi · 7 hrastova cuvee belo | 2022 | 90 | biwc |
| Despotika · Trag | 2022 | 90 | biwc |
| Despotika · Beskraj | 2024 | 90 | awc-vienna |
| Tarpoš · Sauvignon Blanc | 2023 | 90 | awc-vienna |
| Tarpoš · Merlot | 2021 | 90 | awc-vienna |
| Tarpoš · Chardonnay | 2022 | 90 | awc-vienna |
| Despotika · Morava kasna berba | 2020 | 90 | awc-vienna |
| Djordjevic Estate Winery · Sauvignon Blanc | 2021 | 90 | awc-vienna |
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
| Matijašević Vinogradi · Belina | 2021 | 89 | biwc |
| Matijašević Vinogradi · Belina Oranz | 2020 | 89 | biwc |
| Despotika · Dokaz | 2019 | 89 | biwc |
| Despotika · Beskraj | 2023 | 89 | biwc |
| Tarpoš · Sauvignon Blanc | 2023 | 89 | biwc |
| Despotika · Nemir | 2024 | 89 | biwc |
| Despotika · Morava | 2023 | 89 | biwc |
| Despotika · Morava | 2024 | 89 | biwc |
| Despotika · Morava Glina | 2024 | 89 | biwc |
| Despotika · Zmajeviti | 2024 | 89 | biwc |
| Arsenijević · Sauvignon | 2025 | 89 | biwc |
| Despotika · Morava clay | 2021 | 89 | awc-vienna |
| Tarpoš · Tamjanika | 2022 | 89 | awc-vienna |
| Tarpoš · Cabernet Sauvignon | 2017 | 89 | awc-vienna |
| Despotika · BESKRAJ | 2019 | 89 | awc-vienna |
| Despotika · MORAVA | 2016 | 89 | awc-vienna |
| Despotika · ZMAJEVITI Prokupac | 2015 | 89 | awc-vienna |
| Despotika · BESKRAJ Sauvignon Blanc | 2016 | 89 | awc-vienna |
| Radovanović · Rosé | 2013 | 89 | awc-vienna |
| Despotika · Morava | 2023 | 88 | awc-vienna |
| Radovanović · 25 Reserve Cabernet Sauvignon | 2012 | 88 | decanter |
| Radovanović · Chardonnay Selekcija | 2013 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2012 | 88 | decanter |
| Despotika · Trag Merlot | 2016 | 88 | decanter |
| Eden · Chardonnay | 2019 | 88 | decanter |
| Aleksandrović · Regent Reserve | 2017 | 88 | decanter |
| Matijašević Vinogradi · Belina | 2020 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2016 | 88 | decanter |
| Eden · Genesis | 2019 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2017 | 88 | decanter |
| Tarpoš · Merlot | 2017 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2019 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 88 | decanter |
| Despotika · Dokaz Cabernet Sauvignon | 2021 | 88 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 88 | decanter |
| Matijašević Vinogradi · Tri Doline Merlot | 2021 | 88 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2019 | 88 | decanter |
| Despotika · Nemir | 2023 | 88 | biwc |
| Tarpoš · Merlot | 2019 | 88 | biwc |
| Despotika · Svedok | 2022 | 88 | biwc |
| Djordjevic Estate Winery · Rose | 2024 | 88 | biwc |
| Arsenijević · Prokupac „Starosedelac“ | 2024 | 88 | biwc |
| Despotika · Morava | 2022 | 88 | awc-vienna |
| Despotika · Morava glina | 2022 | 88 | awc-vienna |
| Despotika · Dokaz Šumadija | 2020 | 88 | awc-vienna |
| Despotika · Beskraj | 2023 | 88 | awc-vienna |
| Despotika · Morava bariqque | 2021 | 88 | awc-vienna |
| Despotika · Beskraj | 2022 | 88 | awc-vienna |
| Djordjevic Estate Winery · Chardonnay | 2021 | 88 | awc-vienna |
| Despotika · BESKRAJ Sauvignon Blanc | 2020 | 88 | awc-vienna |
| Despotika · MORAVA | 2019 | 88 | awc-vienna |
| Arsenijević · Sauvignon Blanc | 2017 | 88 | awc-vienna |
| Despotika · MORAVA | 2014 | 88 | awc-vienna |
| Despotika · Morava | 2016 | 87 | decanter |
| Despotika · Nebo Riesling-Pinot Blanc | 2016 | 87 | decanter |
| Despotika · Zmajeviti | 2017 | 87 | decanter |
| Aleksandrović · Regent Reserve | 2015 | 87 | decanter |
| Matijašević Vinogradi · Rock & Rose | 2019 | 87 | decanter |
| Aleksandrović · Trijumf Terroir | 2018 | 87 | decanter |
| Eden · Cabernet Franc | 2019 | 87 | decanter |
| Despotika · Morava | 2022 | 87 | decanter |
| Tarpoš · Sauvignon Blanc | 2023 | 87 | decanter |
| Tarpoš · Merlot | 2021 | 87 | decanter |
| Marko · Doajen Chardonnay | 2024 | 87 | decanter |
| Eden · Genesis | 2021 | 87 | decanter |
| Marko · Carine Merlot-Cabernet Sauvignon | 2020 | 87 | decanter |
| Aleksandrović · Trijumf Noir Brut | 2022 | 87 | decanter |
| Despotika · Dodir | 2025 | 87 | biwc |
| Djordjevic Estate Winery · Merlot | 2024 | 87 | biwc |
| Despotika · Dokaz Šumadija | 2019 | 87 | awc-vienna |
| Djordjevic Estate Winery · BRAVURA CUVEE | 2018 | 87 | awc-vienna |
| Aleksandrović · Regent Reserve | 2012 | 86 | decanter |
| Despotika · Trag | 2013 | 86 | decanter |
| Despotika · Morava | 2016 | 86 | decanter |
| Matijašević Vinogradi · Belina | 2019 | 86 | decanter |
| Aleksandrović · Vožd | 2017 | 86 | decanter |
| Aleksandrović · Trijumf Terroir | 2020 | 86 | decanter |
| Tarpoš · Tamjanika | 2021 | 86 | decanter |
| Tarpoš · Rosé | 2021 | 86 | decanter |
| Matijašević Vinogradi · 7 Hrastova Cuvée | 2021 | 86 | decanter |
| Despotika · Trag | 2021 | 86 | decanter |
| Tarpoš · Cabernet Sauvignon | 2021 | 86 | decanter |
| Despotika · Nemir | 2023 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2020 | 86 | decanter |
| Tarpoš · Chardonnay Extra Brut | 2021 | 86 | decanter |
| Aleksandrović · Rodoslov Grand Reserve | 2018 | 86 | decanter |
| Matijašević Vinogradi · Cukundeda | 2020 | 86 | biwc |
| Tarpoš · Cabernet Sauvignon | 2017 | 86 | biwc |
| Tarpoš · Chardonnay | 2022 | 86 | biwc |
| Tarpoš · Tamjanika | 2022 | 86 | biwc |
| Despotika · Dokaz | 2018 | 86 | biwc |
| Despotika · Dokaz | 2021 | 86 | biwc |
| Despotika · Nebo | 2024 | 86 | biwc |
| Arsenijević · Tamjanika „Starosedelac“ | 2025 | 86 | biwc |
| Despotika · Morava | 2021 | 86 | awc-vienna |
| Tarpoš · Syrah | 2022 | 86 | awc-vienna |
| Despotika · Morava | 2020 | 86 | awc-vienna |
| Despotika · Beskraj | 2021 | 86 | awc-vienna |
| Despotika · BESKRAJ Sauvignon Blanc | 2017 | 86 | awc-vienna |
| Djordjevic Estate Winery · Chardonnay | 2016 | 86 | awc-vienna |
| Djordjevic Estate Winery · Sauvignon Blanc | 2016 | 86 | awc-vienna |
| Despotika · Zmajeviti | 2015 | 85 | decanter |
| Despotika · Nebo | 2017 | 85 | decanter |
| Arsenijević · Cabernet Sauvignon | 2019 | 85 | biwc |
| Despotika · Beskraj | 2021 | 85 | biwc |
| Despotika · Dokaz | 2020 | 85 | biwc |
| Tarpoš · Tamjanika | 2023 | 85 | biwc |
| Matijašević Vinogradi · Belina | 2022 | 85 | biwc |
| Despotika · Beskraj | 2024 | 85 | biwc |
| Despotika · Dodir | 2025 | 85 | biwc |
| Despotika · Morava | 2020 | 85 | awc-vienna |
| Aleksandrović · Trijumf Selection | 2016 | 84 | decanter |
| Despotika · Morava | 2021 | 84 | biwc |
| Arsenijević · Sauvignon Blanc | 2022 | 84 | biwc |
| Despotika · Nebo | 2025 | 84 | biwc |
| Despotika · Morava late harvest | 2021 | 84 | awc-vienna |
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
| 2026 | бронза | bronza | Eden · Genesis 2021 | 
| 2026 | бронза | bronza | Matijašević Vinogradi · Tri Doline Merlot 2021 | 
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
| 2026 | серебро | srebro | Matijašević Vinogradi · Belina 2022 | 
| 2026 | серебро | srebro | Eden · Velvet 2020 | 
| 2026 | серебро | srebro | Despotika · Dodir 2025 | 
| 2026 | серебро | srebro | Despotika · Svedok 2022 | 
| 2026 | серебро | srebro | Djordjevic Estate Winery · Rose 2024 | 
| 2026 | серебро | srebro | Djordjevic Estate Winery · Merlot 2024 | 
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
| 2025 | золото | zlato | Despotika · Beskraj 2024 | 
| 2025 | лучшее белое, международные сорта | 1 | Matijašević Vinogradi · SoviNoa Fumé Blanc 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Trijumf Gold 2023 | 
| 2025 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2025 | серебро | srebro | Aleksandrović · Regent Reserve 2020 | 
| 2025 | серебро | srebro | Despotika · Morava Barik 2022 | 
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
| 2024 | золото | zlato | Matijašević Vinogradi · Cukundeda 2021 | 
| 2024 | золото | zlato | Matijašević Vinogradi · 7 hrastova cuvee belo 2022 | 
| 2024 | золото | zlato | Despotika · Morava barik 2022 | 
| 2024 | золото | zlato | Despotika · Dokaz Šumadija 2021 | 
| 2024 | лучшая молодая винодельня | 1 | Draganić | 
| 2024 | лучшее красное, международные сорта | 1 | Arsenijević · Cabernet Sauvignon 2020 | 
| 2024 | лучшее красное, местные сорта | 1 | Marko · Doajen Prokupac 2022 | 
| 2024 | серебро | srebro | Aleksandrović · Prokupac 2020 | 
| 2024 | серебро | srebro | Matijašević Vinogradi · Cukundeda Prokupac 2021 | 
| 2024 | серебро | srebro | Tarpoš · Tamjanika 2023 | 
| 2024 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2019 | 
| 2024 | серебро | srebro | Aleksandrović · Regent Reserve 2019 | 
| 2024 | серебро | srebro | Despotika · Nemir 2023 | 
| 2024 | серебро | srebro | Despotika · Dokaz 2020 | 
| 2024 | серебро | srebro | Despotika · Dokaz 2021 | 
| 2024 | серебро | srebro | Tarpoš · Tamjanika 2023 | 
| 2024 | серебро | srebro | Tarpoš · Merlot 2019 | 
| 2024 | серебро | srebro | Matijašević Vinogradi · Belina 2022 | 
| 2024 | серебро | srebro | Despotika · Morava 2022 | 
| 2024 | серебро | srebro | Despotika · Morava glina 2022 | 
| 2024 | серебро | srebro | Despotika · Dokaz Šumadija 2020 | 
| 2024 | серебро | srebro | Despotika · Beskraj 2023 | 
| 2024 | серебро | srebro | Tarpoš · Sauvignon Blanc 2023 | 
| 2024 | серебро | srebro | Tarpoš · Merlot 2021 | 
| 2023 | Best Semi Dry Wine Trophy | trofej | Despotika · Nemir 2022 | 
| 2023 | бронза | bronza | Eden · Genesis 2019 | 
| 2023 | бронза | bronza | Eden · Cabernet Franc 2019 | 
| 2023 | бронза | bronza | Tarpoš · Cabernet Sauvignon 2017 | 
| 2023 | бронза | bronza | Tarpoš · Merlot 2017 | 
| 2023 | бронза | bronza | Tarpoš · Chardonnay 2022 | 
| 2023 | бронза | bronza | Matijašević Vinogradi · 7 Hrastova Cuvée 2021 | 
| 2023 | бронза | bronza | Tarpoš · Syrah 2022 | 
| 2023 | бронза | bronza | Despotika · Dodir 2022 | 
| 2023 | бронза | bronza | Despotika · Nebo 2022 | 
| 2023 | бронза | bronza | Despotika · Morava 2021 | 
| 2023 | бронза | bronza | Arsenijević · Starosedelac 2021 | 
| 2023 | бронза | bronza | Arsenijević · Sauvignon Blanc 2022 | 
| 2023 | золото | zlato | Matijašević Vinogradi · Tri Doline 2020 | 
| 2023 | золото | zlato | Matijašević Vinogradi · Sovinoa Fumé Blanc 2021 | 
| 2023 | золото | zlato | Matijašević Vinogradi · Belina 2021 | 
| 2023 | золото | zlato | Matijašević Vinogradi · Belina Oranz 2020 | 
| 2023 | золото | zlato | Despotika · Dokaz 2019 | 
| 2023 | золото | zlato | Tarpoš · Chardonnay 2022 | 
| 2023 | лучшее красное | 1 | Radovanović · Cabernet Sauvignon Grand Reserva 2017 | 
| 2023 | одобрение | approval | Despotika · Morava 2021 | 
| 2023 | одобрение | approval | Despotika · Morava late harvest 2021 | 
| 2023 | одобрение | approval | Tarpoš · Syrah 2022 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Matijašević Vinogradi · Belina 2021 | 
| 2023 | серебро | srebro | Matijašević Vinogradi · Sovinoa Sauvignon Blanc 2021 | 
| 2023 | серебро | srebro | Matijašević Vinogradi · Cukundeda 2020 | 
| 2023 | серебро | srebro | Tarpoš · Cabernet Sauvignon 2017 | 
| 2023 | серебро | srebro | Tarpoš · Chardonnay 2022 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Arsenijević · Cabernet Sauvignon 2019 | 
| 2023 | серебро | srebro | Despotika · Beskraj 2021 | 
| 2023 | серебро | srebro | Despotika · Dokaz 2018 | 
| 2023 | серебро | srebro | Despotika · Morava bariqque 2021 | 
| 2023 | серебро | srebro | Despotika · Morava clay 2021 | 
| 2023 | серебро | srebro | Tarpoš · Tamjanika 2022 | 
| 2023 | серебро | srebro | Despotika · Beskraj 2022 | 
| 2023 | серебро | srebro | Tarpoš · Cabernet Sauvignon 2017 | 
| 2022 | бронза | bronza | Matijašević Vinogradi · Belina 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Trijumf Terroir 2020 | 
| 2022 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2022 | бронза | bronza | Tarpoš · Lipar 2021 | 
| 2022 | бронза | bronza | Tarpoš · Tamjanika 2021 | 
| 2022 | бронза | bronza | Tarpoš · Rosé 2021 | 
| 2022 | бронза | bronza | Matijašević Vinogradi · Rock&Rose 2021 | 
| 2022 | бронза | bronza | Matijašević Vinogradi · Belina Oranz 2020 | 
| 2022 | двойное золото | dvojno-zlato | Matijašević Vinogradi · Sovinoa Fumé Blanc 2020 | 
| 2022 | двойное золото | dvojno-zlato | Aleksandrović · Trijumf Noir Brut 2010 | 
| 2022 | двойное золото | dvojno-zlato | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2022 | золото | zlato | Matijašević Vinogradi · SoviNoa Fumé Blanc 2020 | 
| 2022 | золото | zlato | Aleksandrović · Regent Reserve 2018 | 
| 2022 | золото | zlato | Aleksandrović · Regent Reserve 2018 | 
| 2022 | золото | zlato | Aleksandrović · Trijumf Gold 2021 | 
| 2022 | золото | zlato | Aleksandrović · Vožd 2017 | 
| 2022 | золото | zlato | Aleksandrović · Trijumf Terroir 2020 | 
| 2022 | золото | zlato | Despotika · Trag 2019 | 
| 2022 | золото | zlato | Despotika · Morava 2020 | 
| 2022 | золото | zlato | Despotika · Beskraj 2021 | 
| 2022 | золото | zlato | Despotika · Morava kasna berba 2020 | 
| 2022 | золото | zlato | Matijašević Vinogradi · Tri doline 2020 | 
| 2022 | золото | zlato | Despotika · Morava kasna berba 2020 | 
| 2022 | одобрение | approval | Despotika · Morava 2020 | 
| 2022 | одобрение | approval | Despotika · Dokaz Šumadija 2019 | 
| 2022 | одобрение | approval | Despotika · Beskraj 2021 | 
| 2022 | одобрение | approval | Djordjevic Estate Winery · BRAVURA CUVEE 2018 | 
| 2022 | серебро | srebro | Aleksandrović · Trijumf Gold 2020 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · Sovinoa Sauvignon Blanc 2020 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · Čukundeda Prokupac 2019 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · Čukundeda Superiore 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Prokupac 2019 | 
| 2022 | серебро | srebro | Aleksandrović · Vožd Cabernet Sauvignon 2017 | 
| 2022 | серебро | srebro | Tarpoš · Menuet 2021 | 
| 2022 | серебро | srebro | Tarpoš · 1804 2015 | 
| 2022 | серебро | srebro | Despotika · Dokaz 2019 | 
| 2022 | серебро | srebro | Despotika · Nemir 2021 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · Belina 2020 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · 7 hrastova cuvee belo 2020 | 
| 2022 | серебро | srebro | Matijašević Vinogradi · Čukundeda 2020 | 
| 2022 | серебро | srebro | Djordjevic Estate Winery · Chardonnay 2021 | 
| 2022 | серебро | srebro | Djordjevic Estate Winery · Sauvignon Blanc 2021 | 
| 2021 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2021 | бронза | bronza | Matijašević Vinogradi · Rock & Rose 2019 | 
| 2021 | бронза | bronza | Eden · Chardonnay 2019 | 
| 2021 | бронза | bronza | Matijašević Vinogradi · Belina 2019 | 
| 2021 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2021 | бронза | bronza | Aleksandrović · Regent Reserve 2017 | 
| 2021 | бронза | bronza | Aleksandrović · Vožd 2017 | 
| 2021 | бронза | bronza | Aleksandrović · Vožd 2017 | 
| 2021 | бронза | bronza | Despotika · Krunski Dokaz 2017 | 
| 2021 | двойное золото | dvojno-zlato | Aleksandrović · Prokupac 2018 | 
| 2021 | золото | zlato | Matijašević Vinogradi · SoviNoa 2019 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Selection 2020 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Gold 2019 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Gold 2020 | 
| 2021 | золото | zlato | Aleksandrović · Trijumf Terroir 2018 | 
| 2021 | золото | zlato | Despotika · Dokaz 2018 | 
| 2021 | золото | zlato | Despotika · Nemir 2020 | 
| 2021 | золото | zlato | Matijašević Vinogradi · Belina 2019 | 
| 2021 | золото | zlato | Matijašević Vinogradi · Cukundeda 2019 | 
| 2021 | одобрение | approval | Despotika · Morava 2020 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Noir 2010 | 
| 2021 | серебро | srebro | Aleksandrović · Trijumf Gold 2019 | 
| 2021 | серебро | srebro | Aleksandrović · Rodoslov Grand Reserve 2016 | 
| 2021 | серебро | srebro | Despotika · Beskraj 2020 | 
| 2021 | серебро | srebro | Despotika · Nebo barrique 2019 | 
| 2021 | серебро | srebro | Matijašević Vinogradi · SoviNoa 2019 | 
| 2021 | серебро | srebro | Matijašević Vinogradi · Rock & Rose 2019 | 
| 2021 | серебро | srebro | Despotika · BESKRAJ Sauvignon Blanc 2020 | 
| 2020 | Grand Trophy | trofej | Aleksandrović · Trijumf Selection 2019 | 
| 2020 | White Wine Trophy | trofej | Aleksandrović · Trijumf Selection 2019 | 
| 2020 | бронза | bronza | Despotika · Zmajeviti 2017 | 
| 2020 | бронза | bronza | Despotika · Krunski Dokaz Cabernet Sauvignon 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Regent Reserve 2015 | 
| 2020 | бронза | bronza | Aleksandrović · Trijumf Terroir 2018 | 
| 2020 | бронза | bronza | Matijašević Vinogradi · Rock & Rose 2019 | 
| 2020 | бронза | bronza | Matijašević Vinogradi · SoviNoa 2019 | 
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
| 2020 | серебро | srebro | Despotika · MORAVA 2019 | 
| 2020 | серебро | srebro | Despotika · BESKRAJ 2019 | 
| 2019 | двойное золото | dvojno-zlato | Aleksandrović · Trijumf Gold 2018 | 
| 2019 | двойное золото | dvojno-zlato | Despotika · Dodir 2018 | 
| 2019 | двойное золото | dvojno-zlato | Despotika · Beskraj 2017 | 
| 2019 | одобрение | approval | Despotika · BESKRAJ Sauvignon Blanc 2017 | 
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
| 2018 | серебро | srebro | Arsenijević · Sauvignon Blanc 2017 | 
| 2017 | бронза | bronza | Despotika · Morava 2016 | 
| 2017 | бронза | bronza | Despotika · Trag 2015 | 
| 2017 | бронза | bronza | Aleksandrović · Regent Reserve 2012 | 
| 2017 | бронза | bronza | Aleksandrović · Rodoslov Grand Reserve 2012 | 
| 2017 | бронза | bronza | Despotika · Zmajeviti Prokupac 2015 | 
| 2017 | бронза | bronza | Despotika · Beskraj Sovinjon Beli 2016 | 
| 2017 | одобрение | approval | Djordjevic Estate Winery · Chardonnay 2016 | 
| 2017 | одобрение | approval | Djordjevic Estate Winery · Sauvignon Blanc 2016 | 
| 2017 | отмечено | commended | Aleksandrović · Trijumf Selection 2016 | 
| 2017 | отмечено | commended | Aleksandrović · Trijumf Gold 2015 | 
| 2017 | отмечено | commended | Despotika · Zmajeviti 2015 | 
| 2017 | серебро | srebro | Despotika · Dokaz 2015 | 
| 2017 | серебро | srebro | Aleksandrović · Vizija 2015 | 
| 2017 | серебро | srebro | Despotika · Dokaz Cabernet Sauvignon 2015 | 
| 2017 | серебро | srebro | Despotika · MORAVA 2016 | 
| 2017 | серебро | srebro | Despotika · ZMAJEVITI Prokupac 2015 | 
| 2017 | серебро | srebro | Despotika · BESKRAJ Sauvignon Blanc 2016 | 
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
| 2015 | серебро | srebro | Despotika · Trag Merlot 2013 | 
| 2015 | серебро | srebro | Despotika · MORAVA 2014 | 
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
| 2014 | серебро | srebro | Radovanović · Rosé 2013 | 
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
| 2012 | отмечено | commended | Radovanović · Pino As 2010 | 
| 2012 | серебро | srebro | Aleksandrović · Oplen 2010 | 
| 2012 | серебро | srebro | Aleksandrović · Harizma 2009 | 
| 2011 | бронза | bronza | Radovanović · Rèserve Cabernet Sauvignon 2008 | 
| 2011 | бронза | bronza | Aleksandrović · Trijumf 2009 | 
| 2011 | бронза | bronza | Aleksandrović · Harizma 2009 | 
| 2011 | бронза | bronza | Aleksandrović · Harizma 2008 | 
| 2011 | отмечено | commended | Aleksandrović · Trijumf Noir 2008 | 
| 2011 | отмечено | commended | Radovanović · Pino As 2010 | 
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
| Temet · Tri Morave Reserve | 2016 | 95 | decanter |
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
| Lastar · Triangl Pinot Noir | 2017 | 92 | decanter |
| Rubin · Rubinov Prokupac | 2017 | 92 | decanter |
| Temet · Ergo | 2018 | 92 | decanter |
| Radovan · Experiment Prokupac | 2019 | 92 | decanter |
| Vinarija Jovac · Cabernet Sauvignon | 2020 | 92 | decanter |
| Ralević · VIRGO Tamjanika | 2024 | 92 | biwc |
| Ivanović · JARA Pet Nat | 2022 | 91 | Falstaff |
| Radovan · Experiment Prokupac | 2015 | 91 | decanter |
| Temet · Ergo | 2016 | 91 | decanter |
| Lastar · Sofijin Izbor Pinot Noir | 2019 | 91 | decanter |
| Radovan · 100% Prokupac | 2020 | 91 | decanter |
| Lastar · Cabernet Franc | 2020 | 91 | decanter |
| Temet · Ergo | 2018 | 91 | decanter |
| Temet · White Stone Merlot | 2017 | 91 | decanter |
| Ivanović · Prokupac | 2018 | 91 | awc-vienna |
| Fragaria · Red Votazi | 2019 | 91 | awc-vienna |
| Fragaria · Red | 2018 | 91 | awc-vienna |
| Rubin · Amante Aurora | 2019 | 90 | gilbert-gaillard |
| Temet · Tri Morave | 2017 | 90 | decanter |
| Radovan · Prokupac | 2015 | 90 | decanter |
| Temet · Tri Morave Reserve | 2017 | 90 | decanter |
| Lastar · Triangl Chardonnay | 2017 | 90 | decanter |
| Temet · Tri Morave Reserve | 2019 | 90 | decanter |
| Temet · Ergo | 2018 | 90 | decanter |
| Temet · Tri Morave Reserve | 2019 | 90 | decanter |
| Ivanović · No 1/2 | 2019 | 90 | decanter |
| Temet · Tri Morave | 2019 | 90 | decanter |
| Fragaria · Selekcija | 2019 | 90 | decanter |
| Temet · Tri Morave Reserve | 2021 | 90 | decanter |
| Radovan · 100% Prokupac | 2023 | 90 | decanter |
| Temet · Ergo | 2019 | 90 | decanter |
| Vinarija Jovac · Merlot | 2020 | 90 | decanter |
| Temet · Ergo Rosé | 2019 | 90 | decanter |
| Ralević · Aurum | 2020 | 90 | biwc |
| Ivanović · Prokupac | 2019 | 90 | awc-vienna |
| Rubin · Prokupac | 2018 | 90 | awc-vienna |
| Ivanović · Tamjanika | 2021 | 90 | awc-vienna |
| Rubin · Merlot | 2018 | 90 | awc-vienna |
| Fragaria · Red Votazi | 2020 | 90 | awc-vienna |
| Rubin · Sauvignon Blanc | 2018 | 90 | awc-vienna |
| Rubin · Merlot | 2018 | 90 | awc-vienna |
| Fragaria · Red | 2019 | 90 | awc-vienna |
| Rubin · Prokupac | 2017 | 90 | awc-vienna |
| Ivanović · Tamjanika | 2018 | 90 | awc-vienna |
| Braća Rajković · Sofia tamjanika | 2015 | 90 | awc-vienna |
| Braća Rajković · Cabernet | 2017 | 90 | awc-vienna |
| Lastar · Tamjanika | 2017 | 90 | awc-vienna |
| Rubin · Prokupac | 2016 | 90 | awc-vienna |
| Temet · Rose | 2013 | 90 | awc-vienna |
| Radovan · Experiment Prokupac | 2016 | 89 | decanter |
| Temet · Ergo White | 2016 | 89 | decanter |
| Temet · Tri Morave | 2017 | 89 | decanter |
| Temet · Tri Morave Brut | 2017 | 89 | decanter |
| Temet · Beli Kamen Merlot | 2018 | 89 | decanter |
| Temet · Tri Morave Red | 2019 | 89 | decanter |
| Temet · Ergo | 2017 | 89 | decanter |
| Fragaria · Fragari Votazi | 2019 | 89 | decanter |
| Lastar · Triangl Sauvignon-Viognier | 2020 | 89 | decanter |
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
| Ralević · Virgo Tamjanika | 2024 | 89 | awc-vienna |
| Ivanović · No 1/2 | 2018 | 89 | awc-vienna |
| Fragaria · Red | 2020 | 89 | awc-vienna |
| Rubin · Cabernet Sauvignon - Paraćinsko vinogorje | 2018 | 89 | awc-vienna |
| Ivanović · Prokupac | 2017 | 89 | awc-vienna |
| Braća Rajković · 33 premium wine red | 2016 | 89 | awc-vienna |
| Fragaria · red | 2017 | 89 | awc-vienna |
| Lastar · Tamjanika | 2018 | 89 | awc-vienna |
| Lastar · Pinot Noir | 2016 | 89 | awc-vienna |
| Lastar · Chardonnay | 2016 | 89 | awc-vienna |
| Lastar · Chardonnay | 2015 | 89 | awc-vienna |
| Rubin · Amante Carmen | 2019 | 88 | gilbert-gaillard |
| Temet · Ergo White | 2015 | 88 | decanter |
| Lastar · Pinot Noir | 2015 | 88 | decanter |
| Lastar · Tamjanika | 2016 | 88 | decanter |
| Temet · Tri Morave | 2016 | 88 | decanter |
| Temet · Ergo | 2016 | 88 | decanter |
| Temet · Tri Morave | 2018 | 88 | decanter |
| Temet · Ergo | 2017 | 88 | decanter |
| Temet · Tri Morave | 2019 | 88 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 88 | decanter |
| Temet · Burgundac Sivi | 2019 | 88 | decanter |
| Lastar · Chardonnay | 2018 | 88 | decanter |
| Temet · Tri Morave Reserve | 2019 | 88 | decanter |
| Temet · Ergo | 2019 | 88 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 88 | decanter |
| Temet · Ergo | 2018 | 88 | decanter |
| Lastar · Chardonnay | 2023 | 88 | biwc |
| Ralević · Cabernet sauvignon | 2018 | 88 | biwc |
| Lastar · Chardonnay | 2024 | 88 | biwc |
| Lastar · Tamjanika | 2025 | 88 | biwc |
| Vinska Kuća Minića · LiLi Prokupac Rosé | 2024 | 88 | awc-vienna |
| Fragaria · White Jagoda | 2021 | 88 | awc-vienna |
| Rubin · Prokupac | 2018 | 88 | awc-vienna |
| Rubin · Chardonnay | 2019 | 88 | awc-vienna |
| Rubin · Chardonnay | 2018 | 88 | awc-vienna |
| Fragaria · White Sauvignon Blanc | 2019 | 88 | awc-vienna |
| Fragaria · White Jagoda | 2019 | 88 | awc-vienna |
| Rubin · Amante Carmen Prokupac, Marselan, Merlot | 2016 | 88 | awc-vienna |
| Temet · Tri Morave | 2015 | 87 | decanter |
| Temet · Tri Morave Rosé | 2015 | 87 | decanter |
| Temet · Tri Morave Red | 2015 | 87 | decanter |
| Ivanović · Prokupac | 2016 | 87 | decanter |
| Temet · Tri Morave | 2017 | 87 | decanter |
| Radovan · Experiment Prokupac | 2017 | 87 | decanter |
| Rubin · Amante Carmen | 2016 | 87 | decanter |
| Lastar · Pinot Noir | 2016 | 87 | decanter |
| Lastar · Triangl Sauvignon-Viognier | 2017 | 87 | decanter |
| Rubin · Cabernet Sauvignon | 2016 | 87 | decanter |
| Vinogradi Veličković Vinarija · Sauvignon Blanc | 2015 | 87 | decanter |
| Temet · Pinot Grigio | 2018 | 87 | decanter |
| Lastar · Merlot-Cabernet Franc | 2017 | 87 | decanter |
| Temet · Ergo | 2017 | 87 | decanter |
| Temet · Beli Kamen Merlot | 2017 | 87 | decanter |
| Temet · Tri Morave | 2020 | 87 | decanter |
| Rubin · Sauvignon Blanc | 2019 | 87 | decanter |
| Temet · Ergo | 2018 | 87 | decanter |
| Rubin · Prokupac | 2018 | 87 | decanter |
| Vinarija Jovac · Tamjanika | 2021 | 87 | decanter |
| Fragaria · Votazi | 2020 | 87 | decanter |
| Fragaria · Jagoda | 2022 | 87 | decanter |
| Rubin · Amante Matea Merlot | 2018 | 87 | decanter |
| Temet · Beli Kamen Syrah | 2017 | 87 | decanter |
| Temet · Beli Kamen Prokupac | 2019 | 87 | decanter |
| Vinarija Jovac · Merlot | 2020 | 87 | decanter |
| Lastar · Sofijin Izbor Pinot Noir | 2023 | 87 | decanter |
| Temet · Tri Morave Reserve | 2019 | 87 | decanter |
| Temet · White Stone Syrah | 2017 | 87 | decanter |
| Ralević · RaRa Tamjanika PETNAT | 2025 | 87 | biwc |
| Ralević · ETER Chardonnay | 2020 | 87 | biwc |
| Fragaria · WHITE Jagoda | 2023 | 87 | awc-vienna |
| Ivanović · No 3/4 | 2020 | 87 | awc-vienna |
| Braća Rajković · Prince rskavac | 2016 | 87 | awc-vienna |
| Vinogradi Veličković Vinarija · Prvo belo | 2016 | 87 | awc-vienna |
| Lastar · Chardonnay | 2017 | 87 | awc-vienna |
| Vinogradi Veličković Vinarija · Prvo belo Sauvignon Blanc | 2016 | 87 | awc-vienna |
| Rubin · Chardonnay | 2016 | 87 | awc-vienna |
| Spasić · Tamjanika Lekcija | 2015 | 87 | awc-vienna |
| Lastar · Pinot Noir | 2015 | 87 | awc-vienna |
| Temet · Tri Morave | 2015 | 86 | decanter |
| Temet · Tri Morave White | 2016 | 86 | decanter |
| Lastar · Chardonnay | 2015 | 86 | decanter |
| Temet · Ergo | 2016 | 86 | decanter |
| Temet · Pinot Grigio | 2016 | 86 | decanter |
| Lastar · Chardonnay | 2016 | 86 | decanter |
| Temet · Tri Morave | 2016 | 86 | decanter |
| Ivanović · No 1/2 | 2015 | 86 | decanter |
| Temet · Tri Morave | 2019 | 86 | decanter |
| Temet · Tri Morave | 2018 | 86 | decanter |
| Temet · Ergo | 2017 | 86 | decanter |
| Rubin · Amante Matea | 2018 | 86 | decanter |
| Rubin · Rubinov Prokupac | 2018 | 86 | decanter |
| Temet · Tri Morave Reserve | 2017 | 86 | decanter |
| Lastar · Pinot Noir | 2019 | 86 | decanter |
| Temet · Beli Kamen Syrah | 2019 | 86 | decanter |
| Lastar · Triangl Chardonnay | 2020 | 86 | decanter |
| Vinarija Jovac · Merlot | 2020 | 86 | decanter |
| Lastar · Triangl Sauvignon-Viognier | 2021 | 86 | decanter |
| Ivanović · No 3/4 | 2023 | 86 | decanter |
| Ralević · Tamjanika | 2022 | 86 | biwc |
| Lastar · Cru 6 | — | 86 | biwc |
| Lastar · Merlot Cabernet Franc | 2020 | 86 | biwc |
| Lastar · Sofijin Izbor Pinot Noir | 2022 | 86 | biwc |
| Rubin · Prokupac | 2019 | 86 | awc-vienna |
| Rubin · Merlot | 2017 | 86 | awc-vienna |
| Spasić · Tamjanika | 2019 | 86 | awc-vienna |
| Lastar · Riesling | 2017 | 86 | awc-vienna |
| Lastar · Rose | 2017 | 86 | awc-vienna |
| Temet · Tri Morave Belo Penušavo Brut | 2014 | 85 | decanter |
| Lastar · Triangl Chardonnay | 2015 | 85 | decanter |
| Temet · Ergo Red | 2015 | 85 | decanter |
| Lastar · Triangl Chardonnay | 2015 | 85 | decanter |
| Radovan · 100% Prokupac | 2017 | 85 | decanter |
| Lastar · Triangl Chardonnay | 2016 | 85 | decanter |
| Lastar · Cabernet Franc | 2021 | 85 | biwc |
| Lastar · Sofijin izbor | 2021 | 85 | biwc |
| Ivanović · No ¾ | 2023 | 85 | biwc |
| Ivanović · No ½ | 2020 | 85 | biwc |
| Ivanović · Tamjanika | 2024 | 85 | biwc |
| Rubin · Sauvignon Blanc | 2013 | 85 | awc-vienna |
| Spasić · Tamjanika | 2016 | 85 | awc-vienna |
| Lastar · Rosé | 2016 | 85 | awc-vienna |
| Temet · Dobra Godina | 2011 | 84 | decanter |
| Temet · Ergo Red | 2013 | 84 | decanter |
| Temet · Ergo Blush | 2015 | 84 | decanter |
| Lastar · Chardonnay | 2017 | 84 | decanter |
| Lastar · Triangl Sauvignon-Viognier | 2016 | 84 | decanter |
| Ivanović · Prokupac | 2016 | 84 | decanter |
| Rubin · Merlot | 2017 | 84 | decanter |
| Rubin · Amante Carmen Prokupac-Marselan-Merlot | 2016 | 84 | decanter |
| Ralević · VIRGO Sauvignon blanc | 2021 | 84 | biwc |
| Lastar · rose | 2024 | 84 | biwc |
| Radovan · 100% Prokupac | 2023 | 84 | biwc |
| Radovan · 100% Zuplianka | 2023 | 84 | biwc |
| Ivanović · ЦФ | 2025 | 84 | biwc |
| Fragaria · Rose Fragolina | 2021 | 84 | awc-vienna |
| Temet · Pinot Grigio | 2014 | 83 | decanter |
| Lastar · Rose | 2023 | 83 | biwc |
| Lastar · Chardonnay | 2021 | 81 | biwc |
| Ralević · Chardonnay | 2020 | 81 | biwc |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | Best of Show Serbia | trofej | Ralević · Virgo Sauvignon Blanc 2021 | 
| 2026 | бронза | bronza | Temet · Tri Morave Reserve 2021 | 
| 2026 | бронза | bronza | Lastar · Sofijin Izbor Pinot Noir 2023 | 
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
| 2026 | одобрение | approval | Vinska Kuća Minića · LiLi Prokupac Rosé 2024 | 
| 2026 | серебро | srebro | Temet · Ergo 2019 | 
| 2026 | серебро | srebro | Vinarija Jovac · Merlot 2020 | 
| 2026 | серебро | srebro | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2026 | серебро | srebro | Temet · White Stone Merlot 2017 | 
| 2026 | серебро | srebro | Temet · Ergo Rosé 2019 | 
| 2026 | серебро | srebro | Ivanović · Tamjanika 2024 | 
| 2026 | серебро | srebro | Lastar · Tamjanika 2025 | 
| 2026 | серебро | srebro | Lastar · Sofijin Izbor Pinot Noir 2022 | 
| 2026 | серебро | srebro | Ralević · RaRa Tamjanika PETNAT 2025 | 
| 2026 | серебро | srebro | Ralević · ETER Chardonnay 2020 | 
| 2025 | бронза | bronza | Ivanović · No 3/4 2023 | 
| 2025 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2025 | бронза | bronza | Vinarija Jovac · Cabernet Sauvignon 2020 | 
| 2025 | бронза | bronza | Ralević · VIRGO Sauvignon blanc 2021 | 
| 2025 | бронза | bronza | Lastar · rose 2024 | 
| 2025 | бронза | bronza | Radovan · 100% Prokupac 2023 | 
| 2025 | бронза | bronza | Radovan · 100% Zuplianka 2023 | 
| 2025 | вклад в винный туризм | 1 | Lastar | 
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
| 2025 | серебро | srebro | Lastar · Merlot Cabernet Franc 2020 | 
| 2025 | серебро | srebro | Lastar · Chardonnay 2024 | 
| 2025 | серебро | srebro | Ralević · Virgo Tamjanika 2024 | 
| 2024 | бронза | bronza | Fragaria · Votazi 2020 | 
| 2024 | бронза | bronza | Vinarija Jovac · Merlot 2020 | 
| 2024 | бронза | bronza | Lastar · Triangl Sauvignon-Viognier 2021 | 
| 2024 | бронза | bronza | Fragaria · Jagoda 2022 | 
| 2024 | бронза | bronza | Rubin · Amante Matea Merlot 2018 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2024 | бронза | bronza | Temet · Beli Kamen Prokupac 2019 | 
| 2024 | бронза | bronza | Lastar · Rose 2023 | 
| 2024 | золото | zlato | Ralević · Eter Chardonnay 2019 | 
| 2024 | золото | zlato | Ralević · Aurum 2020 | 
| 2024 | лучшее белое, местные сорта | 1 | Yotta · Hysteresis Tamjanika 2022 | 
| 2024 | лучшее белое, органика, местные сорта | 1 | Ivanović · No 3/4 2023 | 
| 2024 | одобрение | approval | Fragaria · WHITE Jagoda 2023 | 
| 2024 | серебро | srebro | Lastar · Cabernet Franc 2020 | 
| 2024 | серебро | srebro | Temet · Tri Morave Reserve 2021 | 
| 2024 | серебро | srebro | Temet · Ergo 2018 | 
| 2024 | серебро | srebro | Radovan · Experiment Prokupac 2019 | 
| 2024 | серебро | srebro | Lastar · Cru 6 | 
| 2024 | серебро | srebro | Lastar · Chardonnay 2023 | 
| 2023 | бронза | bronza | Vinarija Jovac · Tamjanika 2021 | 
| 2023 | бронза | bronza | Lastar · Pinot Noir 2019 | 
| 2023 | бронза | bronza | Temet · Tri Morave Reserve 2019 | 
| 2023 | бронза | bronza | Temet · Beli Kamen Syrah 2019 | 
| 2023 | бронза | bronza | Fragaria · Fragari Votazi 2019 | 
| 2023 | бронза | bronza | Temet · Ergo 2019 | 
| 2023 | бронза | bronza | Lastar · Triangl Chardonnay 2020 | 
| 2023 | бронза | bronza | Lastar · Triangl Sauvignon-Viognier 2020 | 
| 2023 | бронза | bronza | Lastar · Chardonnay 2021 | 
| 2023 | бронза | bronza | Ralević · Chardonnay 2020 | 
| 2023 | золото | zlato | Vinarija Jovac · Stella Noir 2020 | 
| 2023 | золото | zlato | Ivanović · No 1/2 2019 | 
| 2023 | золото | zlato | Ralević · Vranac 2020 | 
| 2023 | одобрение | approval | Rubin · Prokupac 2019 | 
| 2023 | серебро | srebro | Temet · Ergo 2018 | 
| 2023 | серебро | srebro | Temet · Tri Morave Reserve 2019 | 
| 2023 | серебро | srebro | Ivanović · No 1/2 2019 | 
| 2023 | серебро | srebro | Temet · Tri Morave 2019 | 
| 2023 | серебро | srebro | Lastar · Sofijin Izbor Pinot Noir 2019 | 
| 2023 | серебро | srebro | Temet · Beli Kamen Merlot 2019 | 
| 2023 | серебро | srebro | Fragaria · Selekcija 2019 | 
| 2023 | серебро | srebro | Radovan · 100% Prokupac 2020 | 
| 2023 | серебро | srebro | Lastar · Cabernet Franc 2021 | 
| 2023 | серебро | srebro | Lastar · Sofijin izbor 2021 | 
| 2023 | серебро | srebro | Ralević · Tamjanika 2022 | 
| 2022 | Best Dry Red Wine Trophy | trofej | Ivanović · No 1/2 | 
| 2022 | бронза | bronza | Lastar · Chardonnay 2018 | 
| 2022 | бронза | bronza | Temet · Tri Morave 2020 | 
| 2022 | бронза | bronza | Temet · Tri Morave Red 2019 | 
| 2022 | бронза | bronza | Temet · Burgundac Sivi 2019 | 
| 2022 | бронза | bronza | Rubin · Sauvignon Blanc 2019 | 
| 2022 | бронза | bronza | Temet · Ergo 2018 | 
| 2022 | бронза | bronza | Rubin · Prokupac 2018 | 
| 2022 | бронза | bronza | Temet · Ergo 2017 | 
| 2022 | бронза | bronza | Lastar · Chardonnay 2018 | 
| 2022 | золото | zlato | Lastar · Triangl Chardonnay 2018 | 
| 2022 | золото | zlato | Braća Rajković · Prince 2017 | 
| 2022 | золото | zlato | Ivanović · Prokupac 2019 | 
| 2022 | золото | zlato | Ivanović · Tamjanika 2021 | 
| 2022 | золото | zlato | Ivanović · No ½ 2018 | 
| 2022 | золото | zlato | Ivanović · Tamjanika 2021 | 
| 2022 | золото | zlato | Fragaria · Red Votazi 2020 | 
| 2022 | лучшее красное | 4 | Budimir · Triada crveno 2020 | 
| 2022 | одобрение | approval | Ivanović · No 3/4 2020 | 
| 2022 | одобрение | approval | Fragaria · Rose Fragolina 2021 | 
| 2022 | отмечено | commended | Lastar · Pinot Noir 2017 | 
| 2022 | серебро | srebro | Temet · Tri Morave Reserve 2019 | 
| 2022 | серебро | srebro | Temet · Ergo 2018 | 
| 2022 | серебро | srebro | Temet · Tri Morave Reserve 2018 | 
| 2022 | серебро | srebro | Temet · Ergo 2018 | 
| 2022 | серебро | srebro | Braća Rajković · 33 Bela 2019 | 
| 2022 | серебро | srebro | Braća Rajković · Prince 2018 | 
| 2022 | серебро | srebro | Braća Rajković · Sofia Cuvée 2019 | 
| 2022 | серебро | srebro | Ivanović · No ¾ 2020 | 
| 2022 | серебро | srebro | Ivanović · Prokupac 2019 | 
| 2022 | серебро | srebro | Rubin · Prokupac 2018 | 
| 2022 | серебро | srebro | Ivanović · No 1/2 2018 | 
| 2022 | серебро | srebro | Rubin · Merlot 2018 | 
| 2022 | серебро | srebro | Fragaria · White Jagoda 2021 | 
| 2022 | серебро | srebro | Fragaria · Red 2020 | 
| 2021 | бронза | bronza | Lastar · Merlot Cabernet Franc 2017 | 
| 2021 | бронза | bronza | Rubin · Amante Matea 2018 | 
| 2021 | бронза | bronza | Rubin · Rubinov Prokupac 2018 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Merlot 2018 | 
| 2021 | бронза | bronza | Lastar · Merlot-Cabernet Franc 2017 | 
| 2021 | бронза | bronza | Temet · Ergo 2017 | 
| 2021 | бронза | bronza | Temet · Tri Morave Reserve 2017 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Syrah 2017 | 
| 2021 | бронза | bronza | Temet · Beli Kamen Merlot 2017 | 
| 2021 | бронза | bronza | Lastar · Pinot Nour Triangl 2017 | 
| 2021 | бронза | bronza | Braća Rajković · 33 2016 | 
| 2021 | бронза | bronza | Braća Rajković · Sofia Viognier Barrique 2019 | 
| 2021 | бронза | bronza | Braća Rajković · Sofia Traminer Late Harvest 2019 | 
| 2021 | бронза | bronza | Braća Rajković · Sofia Carmenere 2018 | 
| 2021 | двойное золото | dvojno-zlato | Lastar · Chardonnay 2018 | 
| 2021 | двойное золото | dvojno-zlato | Braća Rajković · Prince Rskavac 2018 | 
| 2021 | золото | zlato | Lastar · Triangl Sauvignon - Viognier 2017 | 
| 2021 | золото | zlato | Lastar · Merlot Cabernet Franc 2017 | 
| 2021 | золото | zlato | Braća Rajković · Sofia Rose 2020 | 
| 2021 | золото | zlato | Braća Rajković · 33 2018 | 
| 2021 | золото | zlato | Braća Rajković · Sofia Semillon 2020 | 
| 2021 | золото | zlato | Braća Rajković · ŽupanAja 2012 | 
| 2021 | золото | zlato | Ivanović · Prokupac 2018 | 
| 2021 | золото | zlato | Rubin · Sauvignon Blanc 2018 | 
| 2021 | золото | zlato | Fragaria · Red 2019 | 
| 2021 | золото | zlato | Fragaria · Red Votazi 2019 | 
| 2021 | серебро | srebro | Lastar · Triangl Chardonnay 2017 | 
| 2021 | серебро | srebro | Rubin · Prokupac 2018 | 
| 2021 | серебро | srebro | Rubin · Chardonnay 2019 | 
| 2021 | серебро | srebro | Rubin · Cabernet Sauvignon - Paraćinsko vinogorje 2018 | 
| 2021 | серебро | srebro | Rubin · Merlot 2018 | 
| 2020 | Orange Wine Trophy | trofej | Temet · Tri Morave reserve white 2017 | 
| 2020 | бронза | bronza | Temet · Ergo 2017 | 
| 2020 | бронза | bronza | Lastar · Triangl Sauvignon-Viognier 2017 | 
| 2020 | бронза | bronza | Rubin · Cabernet Sauvignon 2016 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2019 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2019 | 
| 2020 | бронза | bronza | Vinogradi Veličković Vinarija · Sauvignon Blanc 2015 | 
| 2020 | бронза | bronza | Temet · Pinot Grigio 2018 | 
| 2020 | бронза | bronza | Temet · Tri Morave 2018 | 
| 2020 | бронза | bronza | Temet · Ergo 2017 | 
| 2020 | бронза | bronza | Temet · Tri Morave Brut 2017 | 
| 2020 | бронза | bronza | Ralević · Rose Ra 2018 | 
| 2020 | бронза | bronza | Ralević · Sauvignon blanc barrel fermented 2018 | 
| 2020 | бронза | bronza | Rubin · Chardonnay 2018 | 
| 2020 | бронза | bronza | Rubin · Amante Carmen 2016 | 
| 2020 | винодельня года | 1 | Temet | 
| 2020 | двойное золото | dvojno-zlato | Braća Rajković · Sofija Tamnjanika Noble Rot Late Harvest 2017 | 
| 2020 | двойное золото | dvojno-zlato | Braća Rajković · Pinot Rose 2019 | 
| 2020 | золото | zlato | Braća Rajković · Prince Rskavac 2018 | 
| 2020 | золото | zlato | Braća Rajković · 33 2016 | 
| 2020 | золото | zlato | Temet · Ergo red 2017 | 
| 2020 | золото | zlato | Fragaria · Red 2018 | 
| 2020 | лучшее розе | 1 | Temet · Ergo Rose 2018 | 
| 2020 | одобрение | approval | Rubin · Merlot 2017 | 
| 2020 | одобрение | approval | Spasić · Tamjanika 2019 | 
| 2020 | одобрение | approval | Lastar · Riesling 2017 | 
| 2020 | отмечено | commended | Rubin · Merlot 2017 | 
| 2020 | отмечено | commended | Rubin · Amante Carmen Prokupac-Marselan-Merlot 2016 | 
| 2020 | серебро | srebro | Lastar · Triangl Chardonnay 2017 | 
| 2020 | серебро | srebro | Lastar · Triangl Sauvignon - Viognier 2017 | 
| 2020 | серебро | srebro | Lastar · Triangl Pinot Noir 2017 | 
| 2020 | серебро | srebro | Temet · Tri Morave Reserve 2017 | 
| 2020 | серебро | srebro | Lastar · Triangl Pinot Noir 2017 | 
| 2020 | серебро | srebro | Rubin · Rubinov Prokupac 2017 | 
| 2020 | серебро | srebro | Lastar · Triangl Chardonnay 2017 | 
| 2020 | серебро | srebro | Lastar · Rose 2018 | 
| 2020 | серебро | srebro | Ralević · Sauvignon blanc 2018 | 
| 2020 | серебро | srebro | Temet · Ergo rose 2018 | 
| 2020 | серебро | srebro | Temet · Ergo Burgundac sivi 2018 | 
| 2020 | серебро | srebro | Temet · Ergo white 2017 | 
| 2020 | серебро | srebro | Temet · Tri Morave reserve red 2017 | 
| 2020 | серебро | srebro | Rubin · Merlot 2017 | 
| 2020 | серебро | srebro | Ivanović · Prokupac 2017 | 
| 2020 | серебро | srebro | Rubin · Prokupac 2017 | 
| 2020 | серебро | srebro | Ivanović · Tamjanika 2018 | 
| 2020 | серебро | srebro | Braća Rajković · Sofia tamjanika 2015 | 
| 2020 | серебро | srebro | Braća Rajković · Cabernet 2017 | 
| 2020 | серебро | srebro | Braća Rajković · 33 premium wine red 2016 | 
| 2020 | серебро | srebro | Rubin · Chardonnay 2018 | 
| 2020 | серебро | srebro | Braća Rajković · Prince rskavac 2016 | 
| 2020 | серебро | srebro | Fragaria · White Sauvignon Blanc 2019 | 
| 2020 | серебро | srebro | Fragaria · White Jagoda 2019 | 
| 2020 | серебро | srebro | Fragaria · red 2017 | 
| 2019 | бронза | bronza | Lastar · Chardonnay 2017 | 
| 2019 | бронза | bronza | Lastar · Pinot Noir 2016 | 
| 2019 | бронза | bronza | Lastar · Triangl Chardonnay 2016 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2017 | 
| 2019 | бронза | bronza | Radovan · Experiment Prokupac 2017 | 
| 2019 | бронза | bronza | Temet · Ergo White 2016 | 
| 2019 | бронза | bronza | Rubin · Amante Carmen 2016 | 
| 2019 | бронза | bronza | Lastar · Pinot Noir 2016 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2018 | 
| 2019 | бронза | bronza | Temet · Tri Morave 2017 | 
| 2019 | бронза | bronza | Lastar · Riesling 2017 | 
| 2019 | бронза | bronza | Temet · Ergo Red 2016 | 
| 2019 | бронза | bronza | Temet · Tri Morave Red 2017 | 
| 2019 | винодельня года | 1 | Temet | 
| 2019 | золото | zlato | Temet · Tri Morave Reserve 2016 | 
| 2019 | золото | zlato | Lastar · Pinot Noir 2016 | 
| 2019 | золото | zlato | Temet · Tri Morave sparkling 2017 | 
| 2019 | золото | zlato | Temet · Ergo white 2016 | 
| 2019 | лучшее белое | 1 | Cilić · Onyx Belo 2017 | 
| 2019 | лучшее красное | 1 | Temet · Tri Morave Rezerva Crveno 2016 | 
| 2019 | одобрение | approval | Lastar · Chardonnay 2017 | 
| 2019 | отмечено | commended | Lastar · Triangl Sauvignon - Viognier 2016 | 
| 2019 | отмечено | commended | Lastar · Chardonnay 2017 | 
| 2019 | отмечено | commended | Radovan · 100% Prokupac 2017 | 
| 2019 | отмечено | commended | Lastar · Triangl Chardonnay 2016 | 
| 2019 | отмечено | commended | Lastar · Triangl Sauvignon-Viognier 2016 | 
| 2019 | отмечено | commended | Ivanović · Prokupac 2016 | 
| 2019 | серебро | srebro | Rubin · Amante Carmen 2016 | 
| 2019 | серебро | srebro | Temet · Ergo 2016 | 
| 2019 | серебро | srebro | Lastar · Triangl Chardonnay 2016 | 
| 2019 | серебро | srebro | Lastar · Chardonnay 2017 | 
| 2019 | серебро | srebro | Lastar · Triangl Sauvignon - Viognier 2016 | 
| 2019 | серебро | srebro | Lastar · Tamjanika 2018 | 
| 2019 | серебро | srebro | Ralević · Sauvignon Blanc 2017 | 
| 2019 | серебро | srebro | Ralević · Cabernet Sauvignon 2017 | 
| 2019 | серебро | srebro | Temet · Tri Morave rose 2018 | 
| 2019 | серебро | srebro | Temet · Tri Morave White 2018 | 
| 2019 | серебро | srebro | Rubin · Amante Carmen Prokupac, Marselan, Merlot 2016 | 
| 2019 | серебро | srebro | Lastar · Tamjanika 2018 | 
| 2019 | серебро | srebro | Vinogradi Veličković Vinarija · Prvo belo 2016 | 
| 2019 | серебро | srebro | Lastar · Pinot Noir 2016 | 
| 2018 | White Wine Trophy | trofej | Temet · Ergo White 2016 | 
| 2018 | бронза | bronza | Lastar · Chardonnay Lastar Triangle 2015 | 
| 2018 | бронза | bronza | Lastar · Chardonnay 2016 | 
| 2018 | бронза | bronza | Lastar · Tamjanika 2016 | 
| 2018 | бронза | bronza | Lastar · Tamjanika 2016 | 
| 2018 | бронза | bronza | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Temet · Pinot Grigio 2016 | 
| 2018 | бронза | bronza | Lastar · Chardonnay 2016 | 
| 2018 | бронза | bronza | Temet · Tri Morave 2016 | 
| 2018 | бронза | bronza | Ivanović · No 1/2 2015 | 
| 2018 | бронза | bronza | Temet · Tri Morave 2016 | 
| 2018 | бронза | bronza | Temet · Ergo 2016 | 
| 2018 | бронза | bronza | Radovan · Experiment Prokupac 2016 | 
| 2018 | бронза | bronza | Ivanović · Prokupac 2016 | 
| 2018 | бронза | bronza | Temet · Tri Morave rose 2017 | 
| 2018 | бронза | bronza | Temet · Tri Morave red 2016 | 
| 2018 | бронза | bronza | Vinogradi Veličković Vinarija · Prvo belo 2016 | 
| 2018 | одобрение | approval | Vinogradi Veličković Vinarija · Prvo belo Sauvignon Blanc 2016 | 
| 2018 | одобрение | approval | Rubin · Chardonnay 2016 | 
| 2018 | одобрение | approval | Rubin · Sauvignon Blanc 2013 | 
| 2018 | одобрение | approval | Lastar · Rose 2017 | 
| 2018 | отмечено | commended | Lastar · Triangl Chardonnay 2015 | 
| 2018 | серебро | srebro | Temet · Tri Morave 2017 | 
| 2018 | серебро | srebro | Radovan · Prokupac 2015 | 
| 2018 | серебро | srebro | Temet · Tri Morave white 2017 | 
| 2018 | серебро | srebro | Temet · Dobra Godina 2011 | 
| 2018 | серебро | srebro | Temet · Ergo red 2016 | 
| 2018 | серебро | srebro | Lastar · Rose 2017 | 
| 2018 | серебро | srebro | Lastar · Tamjanika 2017 | 
| 2018 | серебро | srebro | Lastar · Chardonnay 2016 | 
| 2018 | серебро | srebro | Vinogradi Veličković Vinarija · Drugo belo 2016 | 
| 2018 | серебро | srebro | Lastar · Tamjanika 2017 | 
| 2018 | серебро | srebro | Rubin · Prokupac 2016 | 
| 2018 | серебро | srebro | Lastar · Chardonnay 2016 | 
| 2017 | бронза | bronza | Lastar · Chardonnay 2015 | 
| 2017 | бронза | bronza | Lastar · Chardonnay Lastar Triangle 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave White 2016 | 
| 2017 | бронза | bronza | Temet · Ergo White 2015 | 
| 2017 | бронза | bronza | Lastar · Chardonnay 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Rosé 2015 | 
| 2017 | бронза | bronza | Temet · Tri Morave Red 2015 | 
| 2017 | бронза | bronza | Lastar · Pinot Noir 2015 | 
| 2017 | бронза | bronza | Lastar · Rose 2016 | 
| 2017 | бронза | bronza | Lastar · Pinot Noir 2015 | 
| 2017 | бронза | bronza | Spasić · Tamjanika 2016 | 
| 2017 | бронза | bronza | Spasić · Tamjanika Lekcija 2015 | 
| 2017 | бронза | bronza | Vinska Kuća Minića · Stota Suza 2014 | 
| 2017 | бронза | bronza | Vinska Kuća Minića · Tamjanika Kasna berba 2011 | 
| 2017 | золото | zlato | Lastar · Chardonnay 2015 | 
| 2017 | одобрение | approval | Spasić · Tamjanika 2016 | 
| 2017 | одобрение | approval | Lastar · Rosé 2016 | 
| 2017 | отмечено | commended | Lastar · Pinot Noir 2015 | 
| 2017 | отмечено | commended | Lastar · Triangl Chardonnay 2015 | 
| 2017 | отмечено | commended | Temet · Ergo Blush 2015 | 
| 2017 | отмечено | commended | Temet · Ergo Red 2015 | 
| 2017 | серебро | srebro | Radovan · Experiment Prokupac 2015 | 
| 2017 | серебро | srebro | Lastar · Tamjanika 2016 | 
| 2017 | серебро | srebro | Spasić · Tamjanika Lekcija 2015 | 
| 2017 | серебро | srebro | Lastar · Chardonnay 2015 | 
| 2017 | серебро | srebro | Lastar · Pinot Noir 2015 | 
| 2016 | бронза | bronza | Temet · Tri Morave 2015 | 
| 2016 | бронза | bronza | Temet · Tri Morave 2015 | 
| 2016 | отмечено | commended | Temet · Dobra Godina 2011 | 
| 2016 | отмечено | commended | Temet · Ergo Red 2013 | 
| 2016 | отмечено | commended | Temet · Pinot Grigio 2014 | 
| 2016 | отмечено | commended | Temet · Tri Morave Belo Penušavo Brut 2014 | 
| 2015 | бронза | bronza | Temet · Tri Bele 2014 | 
| 2015 | бронза | bronza | Temet · Pinot Grigio 2014 | 
| 2015 | бронза | bronza | Braća Rajković · 33 Premium 2011 | 
| 2015 | золото | zlato | Ivanović · No 1/2 2013 | 
| 2015 | отмечено | commended | Temet · Ergo White 2013 | 
| 2015 | отмечено | commended | Temet · Ergo White 2012 | 
| 2015 | отмечено | commended | Temet · Ergo Red 2012 | 
| 2015 | отмечено | commended | Temet · Ergo 2011 | 
| 2015 | серебро | srebro | Temet · Dobra Godina 2011 | 
| 2015 | серебро | srebro | Braća Rajković · Prince Rskavac 2011 | 
| 2014 | бронза | bronza | Temet · Tri Morave 2012 | 
| 2014 | бронза | bronza | Temet · Pinot Grigio 2012 | 
| 2014 | бронза | bronza | Temet · Ergo 2011 | 
| 2014 | бронза | bronza | Temet · Ergo White 2012 | 
| 2014 | бронза | bronza | Temet · Rose 2013 | 
| 2014 | золото | zlato | Temet · Pinot G 2013 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Chardonnay Barrique 2008 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Sauvignon blanc Barrique 2009 | 
| 2014 | отмечено | commended | Rubin · Terra Lazarica Merlot Barrique 2008 | 
| 2014 | отмечено | commended | Braća Rajković · Prince Rskavac 2011 | 
| 2014 | серебро | srebro | Temet · Tri morave 2013 | 
| 2014 | серебро | srebro | Temet · Rose 2013 | 
| 2013 | большое золото | veliko-zlato | Rubin · Terra Lazarica Cabernet Sauvignon Barrique 2007 | 
| 2013 | бронза | bronza | Braća Rajković · 33 2010 | 
| 2013 | бронза | bronza | Temet · Ergo 2011 | 
| 2013 | отмечено | commended | Temet · Tri Morave White 2012 | 
| 2013 | отмечено | commended | Braća Rajković · Sofia Cuvée 2010 | 
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
| Matalj · Zamna | 2021 | 94 | biwc |
| Matalj · Bukovski | 2020 | 94 | biwc |
| Matalj · Kremen Kamen Cabernet Sauvignon | — | 92 | Wine-Searcher |
| Matalj · Crna Tamjanika | 2022 | 92 | Falstaff |
| Matalj · Terasa Sauvignon Blanc | 2022 | 92 | Falstaff |
| Manastir Bukovo · Chardonnay Oaked | 2021 | 92 | Falstaff |
| Matalj · Kremen | 2020 | 92 | Falstaff |
| Matalj · Terasa Chardonnay | 2022 | 92 | Falstaff |
| Matalj · Terasa Chardonnay | 2013 | 92 | decanter |
| Vimmid · Dentelle | 2016 | 92 | decanter |
| Manastir Bukovo · Filigran Гаме | 2017 | 92 | decanter |
| Matalj · Zemna Reserva | 2021 | 92 | decanter |
| Manastir Bukovo · Black Tamjanika | 2020 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Cabernet Sauvignon | 2019 | 91 | Falstaff |
| Manastir Bukovo · Filigran Reserve Gamay | 2019 | 91 | Falstaff |
| Matalj · Cuvée Bukovski | 2019 | 91 | decanter |
| Matalj · Bukovski Prokupac | 2020 | 91 | decanter |
| Matalj · Bagrina | 2023 | 91 | decanter |
| Matalj · Cuvée Bukovski | 2022 | 91 | decanter |
| Matalj · Cuvée Bukovski | 2020 | 91 | awc-vienna |
| Manastir Bukovo · Filigran Chardonnay | 2022 | 90 | Falstaff |
| Matalj · Bukovski | 2020 | 90 | Falstaff |
| Manastir Bukovo · Вез | 2018 | 90 | Falstaff |
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
| Manastir Bukovo · Filigran Roze | 2022 | 89 | Falstaff |
| Manastir Bukovo · Cabernet Sauvignon | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Gamay | 2020 | 89 | Falstaff |
| Manastir Bukovo · Filigran Reserve Merlot | 2019 | 89 | Falstaff |
| Vimmid · Cabernet Sauvignon | 2015 | 89 | decanter |
| Matalj · Kremen Kamen Cabernet Sauvignon | 2015 | 89 | decanter |
| Matalj · Cuvée Bukovski | 2018 | 89 | decanter |
| Matalj · Bukovski Prokupac-Začinak | 2021 | 89 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2024 | 89 | decanter |
| Matalj · Kremen | 2020 | 89 | biwc |
| Matalj · Kremen | 2021 | 89 | awc-vienna |
| Manastir Bukovo · Filigran Гаме | 2015 | 88 | decanter |
| Matalj · Terasa Chardonnay | 2016 | 88 | decanter |
| Manastir Bukovo · Filigran Pinot Noir | 2016 | 88 | decanter |
| Vimmid · Sauvignon-Semillon | 2020 | 88 | decanter |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 2017 | 88 | decanter |
| Matalj · Zamna | 2020 | 88 | decanter |
| Matalj · Kremen | 2022 | 88 | decanter |
| Matalj · Kremen | 2021 | 88 | biwc |
| Matalj · Zamna | 2021 | 88 | awc-vienna |
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
| Raj · Red Tamjanika | 2020 | 87 | awc-vienna |
| Matalj · Terasa Chardonnay | 2017 | 86 | decanter |
| Vimmid · Dantelle Cabernet Sauvignon | 2016 | 86 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2016 | 86 | decanter |
| Matalj · Cuvée Bukovski | 2018 | 86 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2020 | 86 | decanter |
| Matalj · Bagrina | 2024 | 86 | decanter |
| Matalj · Cuvée Bukovski | 2019 | 86 | biwc |
| Matalj · Zamna | 2020 | 86 | biwc |
| Matalj · Terasa Sauvignon Blanc | 2015 | 85 | decanter |
| Manastir Bukovo · Chardonnay | 2016 | 85 | decanter |
| Vimmid · Cabernet Sauvignon | 2016 | 85 | decanter |
| Matalj · Terasa Sauvignon Blanc | 2017 | 85 | decanter |
| Manastir Bukovo · Filigran Црна Тамјаника | 2017 | 85 | decanter |
| Vimmid · Cabernet Sauvignon | 2017 | 85 | decanter |
| Manastir Bukovo · Filigran Roze | 2017 | 85 | decanter |
| Matalj · Kremen Cabernet Sauvignon | 2017 | 85 | decanter |
| Vimmid · Cabernet Sauvignon | 2018 | 84 | decanter |
| Raj · Zenit Semillon | 2016 | 84 | awc-vienna |

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
| 2024 | двойное золото | dvojno-zlato | Matalj · Zamna 2021 | 
| 2024 | двойное золото | dvojno-zlato | Matalj · Bukovski 2020 | 
| 2024 | золото | zlato | Matalj · Cuvée Bukovski 2020 | 
| 2024 | серебро | srebro | Matalj · Bukovski Prokupac 2020 | 
| 2024 | серебро | srebro | Matalj · Zemna Reserva 2021 | 
| 2024 | серебро | srebro | Matalj · Terasa Chardonnay 2022 | 
| 2024 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2023 | 
| 2024 | серебро | srebro | Matalj · Kremen 2021 | 
| 2024 | серебро | srebro | Matalj · Kremen 2021 | 
| 2024 | серебро | srebro | Matalj · Zamna 2021 | 
| 2023 | бронза | bronza | Matalj · Zamna 2020 | 
| 2023 | бронза | bronza | Matalj · Kremen 2020 | 
| 2023 | золото | zlato | Matalj · Kremen 2020 | 
| 2023 | лучшее из местных сортов, красное | 1 | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2022 | 
| 2023 | серебро | srebro | Matalj · Bagrina Bukovska 2022 | 
| 2023 | серебро | srebro | Matalj · Cuvée Bukovski 2019 | 
| 2023 | серебро | srebro | Matalj · Zamna 2020 | 
| 2023 | серебро | srebro | Raj · Red Tamjanika 2020 | 
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
| 2021 | бронза | bronza | Vimmid · Sauvignon-Semillon 2020 | 
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
| 2020 | отмечено | commended | Vimmid · Cabernet Sauvignon 2018 | 
| 2020 | серебро | srebro | Vimmid · Dentelle 2016 | 
| 2020 | серебро | srebro | Matalj · Dušica 2018 | 
| 2020 | серебро | srebro | Matalj · Bagrina 2019 | 
| 2020 | серебро | srebro | Matalj · Terasa Chardonnay 2018 | 
| 2019 | Red Wine Trophy | trofej | Matalj · Kremen Kamen 2016 | 
| 2019 | бронза | bronza | Matalj · Terasa Chardonnay 2017 | 
| 2019 | бронза | bronza | Vimmid · Dantelle Cabernet Sauvignon 2016 | 
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
| 2019 | отмечено | commended | Vimmid · Cabernet Sauvignon 2017 | 
| 2019 | серебро | srebro | Matalj · Kremen 2016 | 
| 2019 | серебро | srebro | Matalj · Terasa Chardonnay 2017 | 
| 2018 | одобрение | approval | Raj · Zenit Semillon 2016 | 
| 2018 | отмечено | commended | Manastir Bukovo · Chardonnay 2016 | 
| 2018 | отмечено | commended | Vimmid · Cabernet Sauvignon 2016 | 
| 2018 | серебро | srebro | Manastir Bukovo · Merlot 2015 | 
| 2018 | серебро | srebro | Matalj · Terasa Sauvignon Blanc 2016 | 
| 2018 | серебро | srebro | Matalj · Kremen 2016 | 
| 2017 | бронза | bronza | Matalj · Kremen Cabernet Sauvignon 2015 | 
| 2017 | бронза | bronza | Vimmid · Cabernet Sauvignon 2015 | 
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
| 2015 | серебро | srebro | Vimmid · Cabernet Sauvignon 2012 | 
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
| Vinarija Toplički Vinogradi · Epigenia Prokupac | 2019 | 92 | awc-vienna |
| Doja · Chardonnay Barrique | 2022 | 91 | Falstaff |
| Doja · Rosé | 2022 | 91 | Falstaff |
| Doja · Breg Cabernet Sauvignon | 2019 | 91 | decanter |
| Doja · Prokupac | 2021 | 91 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 91 | biwc |
| Vinarija Toplički Vinogradi · Epigenia Prokupac | 2015 | 91 | awc-vienna |
| Doja · Chardonnay & Pinot Grigio | 2022 | 90 | Falstaff |
| Doja · Prokupac | 2019 | 90 | decanter |
| Doja · Cabernet & Merlot | 2020 | 90 | biwc |
| Doja · BREG Prokupac | 2020 | 90 | biwc |
| Vinarija Toplički Vinogradi · President Vranac | 2020 | 90 | awc-vienna |
| Vinarija Toplički Vinogradi · President Vranac Barrique | 2017 | 90 | awc-vienna |
| Vinarija Toplički Vinogradi · Vranac Barrique | 2015 | 90 | awc-vienna |
| Vinarija Toplički Vinogradi · Virtus | 2015 | 90 | awc-vienna |
| Doja · Tamjanika | 2022 | 89 | Falstaff |
| Doja · Prokupac | 2017 | 89 | decanter |
| Doja · Breg Prokupac | 2020 | 89 | biwc |
| Doja · Prokupac | 2021 | 89 | biwc |
| Doja · Prokupac | 2017 | 89 | awc-vienna |
| Doja · Chardonnay & Pinot Grigio | 2019 | 89 | awc-vienna |
| Vinarija Toplički Vinogradi · Vranac Barrique | 2017 | 89 | awc-vienna |
| Doja · Belo | 2015 | 88 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2018 | 88 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2021 | 88 | decanter |
| Doja · Breg Prokupac | 2021 | 88 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 88 | biwc |
| Doja · Chardonnay Barrique | 2022 | 88 | biwc |
| Doja · Prokupac | 2020 | 88 | biwc |
| Doja · Tamjanika | 2025 | 88 | biwc |
| Vinarija Toplički Vinogradi · Epigenia Prokupac | 2017 | 88 | awc-vienna |
| Vinarija Toplički Vinogradi · Virtus 70/30 | 2017 | 88 | awc-vienna |
| Vinarija Toplički Vinogradi · Tribus Villa Prokupac | 2015 | 88 | awc-vienna |
| Doja · Prokupac | 2015 | 87 | decanter |
| Doja · Breg Prokupac-Cabernet | 2017 | 87 | decanter |
| Doja · Tamjanika | 2020 | 87 | decanter |
| Doja · Prokupac | 2017 | 87 | decanter |
| Doja · Breg Cabernet Sauvignon | 2020 | 87 | decanter |
| Doja · Breg Prokupac | 2021 | 87 | decanter |
| Doja · Cabernet Sauvignon - Merlot | 2019 | 87 | biwc |
| Doja · Tamjanika | 2023 | 87 | biwc |
| Doja · Breg Prokupac | 2021 | 87 | biwc |
| Vinarija Toplički Vinogradi · Epigenia Prokupac | 2018 | 87 | awc-vienna |
| Doja · Prokupac | 2015 | 87 | awc-vienna |
| Doja · Cabernet Sauvignon - Merlot | 2016 | 86 | decanter |
| Doja · Chardonnay-Pinot Grigio | 2019 | 86 | decanter |
| Doja · Prokupac | 2019 | 86 | biwc |
| Doja · Rosé | 2015 | 86 | awc-vienna |
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
| 2021 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Prokupac 2019 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Sauvignon blanc 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Chardonnay 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Prkos rose 2020 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Prokupac 2019 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · Gvozdeni puk crveno 2019 | 
| 2021 | серебро | srebro | Doja · Chardonnay & Pinot Grigio 2019 | 
| 2021 | серебро | srebro | Doja · Breg Prokupac 2017 | 
| 2021 | серебро | srebro | Vinarija Toplički Vinogradi · President Vranac 2020 | 
| 2020 | бронза | bronza | Doja · Breg Prokupac-Cabernet 2017 | 
| 2020 | бронза | bronza | Doja · Prokupac 2017 | 
| 2020 | бронза | bronza | Doja · Cabernet Sauvignon - Merlot 2016 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Tribus villa Pinot Noir 2017 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Epigenia Chardonnay 2018 | 
| 2020 | бронза | bronza | Vinarija Toplički Vinogradi · Epigenia Sauvignon Blanc 2018 | 
| 2020 | золото | zlato | Doja · Cabernet Sauvignon & Merlot 2016 | 
| 2020 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Cabernet Sauvignon 2015 | 
| 2020 | лучшее красное, органика | 1 | Kostić · Prokupac 2017 | 
| 2020 | одобрение | approval | Vinarija Toplički Vinogradi · Epigenia Prokupac 2018 | 
| 2020 | серебро | srebro | Doja · Breg Prokupac 2015 | 
| 2020 | серебро | srebro | Doja · Prokupac 2017 | 
| 2020 | серебро | srebro | Doja · Chardonnay & Pinot Grigio 2018 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Tribus villa Pinot Noir 2015 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Prokupac 2015 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Gvozdeni Puk crveno 2013 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · Prkos 2018 | 
| 2020 | серебро | srebro | Vinarija Toplički Vinogradi · President Vranac Barrique 2017 | 
| 2020 | серебро | srebro | Doja · Prokupac 2017 | 
| 2020 | серебро | srebro | Doja · Chardonnay & Pinot Grigio 2019 | 
| 2019 | серебро | srebro | Vinarija Toplički Vinogradi · Epigenia Prokupac 2017 | 
| 2019 | серебро | srebro | Vinarija Toplički Vinogradi · Vranac Barrique 2017 | 
| 2019 | серебро | srebro | Vinarija Toplički Vinogradi · Virtus 70/30 2017 | 
| 2018 | золото | zlato | Vinarija Toplički Vinogradi · Epigenia Prokupac 2015 | 
| 2018 | золото | zlato | Vinarija Toplički Vinogradi · Vranac Barrique 2015 | 
| 2018 | отмечено | commended | Doja · Prokupac 2016 | 
| 2018 | отмечено | commended | Doja · Belo Chardonnay & Pinot Grigio 2016 | 
| 2018 | отмечено | commended | Doja · Belo Chardonnay-Pinot Grigio 2016 | 
| 2018 | серебро | srebro | Doja · Rose 2017 | 
| 2018 | серебро | srebro | Doja · Prokupac 2016 | 
| 2018 | серебро | srebro | Vinarija Toplički Vinogradi · Virtus 2015 | 
| 2017 | Best Indigenous Red variety Trophy | trofej | Doja · Prokupac 2015 | 
| 2017 | бронза | bronza | Doja · Belo 2015 | 
| 2017 | бронза | bronza | Doja · Prokupac 2015 | 
| 2017 | бронза | bronza | Doja · Belo 2015 | 
| 2017 | бронза | bronza | Doja · Rose 2015 | 
| 2017 | одобрение | approval | Doja · Prokupac 2015 | 
| 2017 | одобрение | approval | Doja · Rosé 2015 | 
| 2017 | отмечено | commended | Doja · Belo 2015 | 
| 2017 | серебро | srebro | Vinarija Toplički Vinogradi · Tribus Villa Prokupac 2015 | 

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
| Jović · Vranac Potrkanjski | 2021 | 92 | awc-vienna |
| Aleksić · Amanet Vranac | 2019 | 92 | awc-vienna |
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
| Aleksić · Tamjanika zuti cvet penusavac | 2019 | 90 | awc-vienna |
| Aleksić · AMANET Vranac | 2013 | 90 | awc-vienna |
| Aleksić · Zuti Cvet Tamjanika | 2018 | 89 | decanter |
| Aleksić · Zuti Cvet Tamjanika Extra Brut | 2023 | 89 | decanter |
| Jović · ROSE DIONIZIJE | 2021 | 89 | biwc |
| Dzervin · Sauvignon | 2023 | 89 | biwc |
| Dzervin · Cuvee 69 | 2021 | 89 | biwc |
| Dzervin · Grasac | 2024 | 89 | biwc |
| Dzervin · Sauvignon | 2025 | 89 | biwc |
| Dzervin · Dubravka Gold | 2025 | 89 | biwc |
| Aleksić · Biser Smederevka | 2015 | 89 | awc-vienna |
| Aleksić · BISER Smederevka | 2014 | 89 | awc-vienna |
| Aleksić · Bonaca Chardonnay | 2019 | 88 | awc-vienna |
| Aleksić · Kardaš Limited | 2011 | 88 | decanter |
| Aleksić · Temperament Merlot | 2015 | 88 | decanter |
| Aleksić · Amanet Vranac | 2015 | 88 | decanter |
| Aleksić · Prokupac | 2021 | 88 | decanter |
| Dzervin · Trifun Grand Cabernet Sauvignon | 2019 | 88 | decanter |
| Aleksić · Zuti Cvet Extra Brut | 2022 | 88 | decanter |
| Aleksić · Morava | 2025 | 88 | decanter |
| Jović · POTRKANJSKI DIONIZIJE | 2021 | 88 | biwc |
| Jović · Rizling Rajnski Potrkanjski | 2021 | 88 | awc-vienna |
| Aleksić · Limited Bonaca Chardonnay | 2018 | 87 | awc-vienna |
| Aleksić · Zuti Cvet Penusavo | 2015 | 87 | decanter |
| Aleksić · Zuti Cvet Tamjanika | 2019 | 87 | decanter |
| Aleksić · Temperament Merlot | 2015 | 87 | decanter |
| Aleksić · Bonaca Chardonnay | 2021 | 87 | decanter |
| Aleksić · Prokupac | 2021 | 87 | decanter |
| Aleksić · Zuti Cvet | 2023 | 87 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2023 | 87 | decanter |
| Aleksić · Žuti Cvet Tamjanika | 2024 | 87 | decanter |
| Dzervin · Trifun Grand Cabernet Sauvignon | 2019 | 87 | decanter |
| Dzervin · Schlossberg | 2019 | 87 | biwc |
| Dzervin · Sauvignon | 2024 | 87 | biwc |
| Dzervin · Nijansa | 2024 | 87 | biwc |
| Dzervin · Cuvee 69 | 2022 | 87 | biwc |
| Aleksić · Žuti Cvet Tamjanika | 2021 | 87 | awc-vienna |
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
| Jović · Rizling Rajnski Potrkanjski | 2021 | 86 | biwc |
| Dzervin · Trifun | 2019 | 86 | biwc |
| Podrum Malča · Anonymous Crna Tamjanika | 2021 | 86 | awc-vienna |
| Jović · Vranac Potrkanjski | 2015 | 86 | awc-vienna |
| Aleksić · Zuti cvet Tamjanika | 2014 | 86 | awc-vienna |
| Aleksić · Zuti Cvet Tamjanika | 2013 | 86 | awc-vienna |
| Aleksić · Arno | 2015 | 85 | decanter |
| Aleksić · Amanet Vranac | 2012 | 85 | decanter |
| Dzervin · Sauvignon | 2021 | 85 | biwc |
| Dzervin · Nijansa | 2023 | 85 | biwc |
| Dzervin · Lozana | 2023 | 85 | biwc |
| Podrum Malča · Anonymous Grašac | 2020 | 85 | awc-vienna |
| Aleksić · Biser Smederevka | 2016 | 85 | awc-vienna |
| Aleksić · Mozaik Pinot Noir | 2019 | 85 | awc-vienna |
| Aleksić · Amanet Vranac | 2011 | 85 | awc-vienna |
| Aleksić · Limited Bonaca Chardonnay | 2017 | 84 | decanter |
| Aleksić · Arno Sauvignon Blanc | 2017 | 84 | decanter |
| Dzervin · Dubravka Gold | 2024 | 84 | biwc |
| Dzervin · Nijansa | 2025 | 84 | biwc |
| Dzervin · Grašac | 2019 | 84 | awc-vienna |
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
| 2025 | бронза | bronza | Aleksić · Žuti Cvet Tamjanika 2024 | 
| 2025 | бронза | bronza | Aleksić · Zuti Cvet Extra Brut 2022 | 
| 2025 | бронза | bronza | Dzervin · Dubravka Gold 2024 | 
| 2025 | золото | zlato | Dzervin · Cuvee 69 2021 | 
| 2025 | золото | zlato | Jović · Vranac Potrkanjski 2021 | 
| 2025 | серебро | srebro | Dzervin · Trifun Grand Cabernet Sauvignon 2019 | 
| 2025 | серебро | srebro | Aleksić · Kardas Cabernet Sauvignon 2021 | 
| 2025 | серебро | srebro | Dzervin · Sauvignon 2024 | 
| 2025 | серебро | srebro | Dzervin · Nijansa 2024 | 
| 2025 | серебро | srebro | Jović · Rizling Rajnski Potrkanjski 2021 | 
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
| 2024 | серебро | srebro | Jović · Rizling Rajnski Potrkanjski 2021 | 
| 2024 | серебро | srebro | Dzervin · Nijansa 2023 | 
| 2024 | серебро | srebro | Dzervin · Trifun 2019 | 
| 2023 | бронза | bronza | Aleksić · Prokupac 2021 | 
| 2023 | бронза | bronza | Aleksić · Kontra 2020 | 
| 2023 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika Sec 2021 | 
| 2023 | бронза | bronza | Dzervin · Pinot Noir 2022 | 
| 2023 | бронза | bronza | Podrum Malča · Anonymous Sauvignon Blanc 2021 | 
| 2023 | лучшая малая винодельня | 1 | Jović | 
| 2023 | одобрение | approval | Podrum Malča · Anonymous Grašac 2020 | 
| 2023 | одобрение | approval | Podrum Malča · Anonymous Crna Tamjanika 2021 | 
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
| 2022 | золото | zlato | Aleksić · Tamjanika zuti cvet penusavac 2019 | 
| 2022 | золото | zlato | Aleksić · Amanet Vranac 2019 | 
| 2022 | одобрение | approval | Aleksić · Biser Smederevka 2016 | 
| 2022 | серебро | srebro | Aleksić · Cabernet Franc 2020 | 
| 2022 | серебро | srebro | Dzervin · Schlossberg 2019 | 
| 2022 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2021 | 
| 2021 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2021 | одобрение | approval | Dzervin · Grašac 2019 | 
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
| 2020 | одобрение | approval | Aleksić · Mozaik Pinot Noir 2019 | 
| 2020 | серебро | srebro | Aleksić · Bonaca Chardonnay 2019 | 
| 2020 | серебро | srebro | Aleksić · Limited Bonaca Chardonnay 2018 | 
| 2020 | серебро | srebro | Aleksić · Barbara 2019 | 
| 2020 | серебро | srebro | Dzervin · Schlossberg 2017 | 
| 2020 | серебро | srebro | Dzervin · Sauvignon blanc 2018 | 
| 2020 | серебро | srebro | Dzervin · Riesling 2017 | 
| 2020 | серебро | srebro | Jović · Potrkanjski Dionizije 2017 | 
| 2020 | серебро | srebro | Aleksić · Biser Smederevka 2015 | 
| 2019 | бронза | bronza | Aleksić · Nostalgija 2017 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Tamjanika 2018 | 
| 2019 | бронза | bronza | Aleksić · Temperament Merlot 2015 | 
| 2019 | бронза | bronza | Aleksić · Amanet Vranac 2015 | 
| 2019 | бронза | bronza | Aleksić · Zuti Cvet Penusavo 2015 | 
| 2019 | бронза | bronza | Dzervin · Sauvignon Blanc 2017 | 
| 2019 | бронза | bronza | Dzervin · Riesling 2017 | 
| 2019 | серебро | srebro | Aleksić · Zuti Cvet 2018 | 
| 2019 | серебро | srebro | Dzervin · Schlossberg 2016 | 
| 2018 | одобрение | approval | Jović · Vranac Potrkanjski 2015 | 
| 2018 | отмечено | commended | Aleksić · Limited Bonaca Chardonnay 2017 | 
| 2018 | отмечено | commended | Aleksić · Arno Sauvignon Blanc 2017 | 
| 2018 | серебро | srebro | Aleksić · Žuti Cvet Tamjanika 2017 | 
| 2018 | серебро | srebro | Aleksić · Amanet Vranac 2013 | 
| 2018 | серебро | srebro | Aleksić · Biser Smederevka Brut 2014 | 
| 2018 | серебро | srebro | Aleksić · BISER Smederevka 2014 | 
| 2018 | серебро | srebro | Aleksić · AMANET Vranac 2013 | 
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
| 2015 | одобрение | approval | Aleksić · Zuti cvet Tamjanika 2014 | 
| 2015 | отмечено | commended | Aleksić · Nostalgija 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2015 | серебро | srebro | Aleksić · Amanet 2011 | 
| 2014 | бронза | bronza | Aleksić · Kardas Limited 2011 | 
| 2014 | золото | zlato | Aleksić · Amanet 2011 | 
| 2014 | одобрение | approval | Aleksić · Amanet Vranac 2011 | 
| 2014 | одобрение | approval | Aleksić · Zuti Cvet Tamjanika 2013 | 
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
| Винарија Тришић (Vinarija Trišić) · Dimasid | 2013 | 94 | decanter |
| Plavinac · Rebo | 2023 | 92 | awc-vienna |
| Janko · Stari Zavet | 2016 | 92 | awc-vienna |
| Janko · Zapis Crveni | 2016 | 91 | decanter |
| Janko · Stari Zavet | 2016 | 91 | decanter |
| Janko · Stari Zavet | 2017 | 91 | decanter |
| Janko · Stari Zavet | 2016 | 91 | awc-vienna |
| Janko · Vrtlog | 2015 | 90 | decanter |
| Janko · Stari Zavet | 2015 | 90 | decanter |
| Janko · Bifora | 2020 | 90 | decanter |
| Винарија Тришић (Vinarija Trišić) · Trišino | 2020 | 90 | decanter |
| Plavinac · Cabernet Sauvignon | 2021 | 90 | awc-vienna |
| Janko · Stari Zavet | 2016 | 90 | awc-vienna |
| Janko · Zavet Stari Cuvée | 2013 | 90 | awc-vienna |
| Plavinac · Sauvignon Blanc | 2025 | 89 | awc-vienna |
| Plavinac · Traminac | 2025 | 89 | awc-vienna |
| Janko · Zavet | 2019 | 89 | decanter |
| Plavinac · Chardonnay | 2025 | 89 | awc-vienna |
| Plavinac · Pinot Grigio | 2025 | 89 | awc-vienna |
| Plavinac · Marselan | 2022 | 89 | awc-vienna |
| Plavinac · Marselan Barrique | — | 89 | awc-vienna |
| Janko · Baš Prokupac | 2020 | 89 | awc-vienna |
| Janko · Stari Zavet | 2017 | 89 | awc-vienna |
| Janko · Stari Zavet | 2017 | 89 | awc-vienna |
| Janko · Stari Zavet | 2016 | 89 | awc-vienna |
| Plavinac · Cabernet Sauvignon Barrique | — | 88 | awc-vienna |
| Plavinac · Tamjanika | 2025 | 88 | gilbert-gaillard |
| Plavinac · Sauvignon Blanc | 2025 | 88 | gilbert-gaillard |
| Janko · Misija Chardonnay | 2013 | 88 | decanter |
| Janko · Bifora | 2016 | 88 | decanter |
| Janko · Zapis Testament | 2016 | 88 | decanter |
| Janko · Bifora | 2017 | 88 | decanter |
| Винарија Тришић (Vinarija Trišić) · Dimasid | 2021 | 88 | decanter |
| Plavinac · Smederevka | 2025 | 88 | decanter |
| Plavinac · Tamjanika | 2025 | 88 | awc-vienna |
| Plavinac · Komšinice | 2025 | 88 | awc-vienna |
| Plavinac · Rosé | 2025 | 88 | awc-vienna |
| Janko · Stari Zavet Cabernet Sauvignon, Merlot & Cabernet Franc | 2017 | 88 | awc-vienna |
| Janko · Misija | 2016 | 87 | decanter |
| Janko · Zlatno Runo Cabernet Sauvignon | 2019 | 87 | decanter |
| Janko · Smederevka | 2017 | 86 | decanter |
| Janko · Vrtlog | 2016 | 86 | decanter |
| Plavinac · Smederevka | 2025 | 86 | awc-vienna |
| Janko · Stari Zavet | 2012 | 85 | decanter |
| Janko · Misija | 2015 | 85 | decanter |
| Janko · Misija | 2016 | 85 | decanter |
| Винарија Тришић (Vinarija Trišić) · Trisino | 2013 | 85 | decanter |
| Винарија Тришић (Vinarija Trišić) · Trisino | 2013 | 85 | decanter |

**Награды**

| Год | Категория | Место | Кому |
|---|---|---|---|
| 2026 | бронза | bronza | Винарија Тришић (Vinarija Trišić) · Dimasid 2021 | 
| 2026 | бронза | bronza | Plavinac · Smederevka 2025 | 
| 2026 | золото | zlato | Plavinac · Rebo 2023 | 
| 2026 | золото | zlato | Plavinac · Cabernet Sauvignon 2021 | 
| 2026 | одобрение | approval | Plavinac · Cabernet Sauvignon Barrique | 
| 2026 | одобрение | approval | Plavinac · Smederevka 2025 | 
| 2026 | одобрение | approval | Plavinac · Rosé 2025 | 
| 2026 | серебро | srebro | Plavinac · Sauvignon Blanc 2025 | 
| 2026 | серебро | srebro | Plavinac · Traminac 2025 | 
| 2026 | серебро | srebro | Винарија Тришић (Vinarija Trišić) · Trišino 2020 | 
| 2026 | серебро | srebro | Plavinac · Tamjanika 2025 | 
| 2026 | серебро | srebro | Plavinac · Komšinice 2025 | 
| 2026 | серебро | srebro | Plavinac · Chardonnay 2025 | 
| 2026 | серебро | srebro | Plavinac · Pinot Grigio 2025 | 
| 2026 | серебро | srebro | Plavinac · Marselan 2022 | 
| 2026 | серебро | srebro | Plavinac · Marselan Barrique | 
| 2024 | бронза | bronza | Janko · Zlatno Runo Cabernet Sauvignon 2019 | 
| 2024 | серебро | srebro | Janko · Bifora 2020 | 
| 2024 | серебро | srebro | Janko · Baš Prokupac 2020 | 
| 2024 | серебро | srebro | Janko · Stari Zavet Cabernet Sauvignon, Merlot & Cabernet Franc 2017 | 
| 2023 | серебро | srebro | Janko · Stari Zavet 2017 | 
| 2022 | бронза | bronza | Janko · Zavet 2019 | 
| 2022 | золото | zlato | Janko · Stari Zavet 2016 | 
| 2022 | серебро | srebro | Janko · Stari Zavet 2017 | 
| 2021 | бронза | bronza | Janko · Bifora 2017 | 
| 2021 | серебро | srebro | Janko · Stari Zavet 2017 | 
| 2021 | серебро | srebro | Janko · Stari Zavet 2016 | 
| 2020 | золото | zlato | Janko · Stari Zavet 2016 | 
| 2020 | отмечено | commended | Винарија Тришић (Vinarija Trišić) · Trisino 2013 | 
| 2019 | бронза | bronza | Janko · Zapis Testament 2016 | 
| 2019 | отмечено | commended | Janko · Misija 2016 | 
| 2019 | отмечено | commended | Винарија Тришић (Vinarija Trišić) · Trisino 2013 | 
| 2019 | серебро | srebro | Janko · Stari Zavet 2016 | 
| 2019 | серебро | srebro | Винарија Тришић (Vinarija Trišić) · Dimasid 2013 | 
| 2019 | серебро | srebro | Janko · Stari Zavet 2016 | 
| 2018 | бронза | bronza | Janko · Smederevka 2017 | 
| 2018 | бронза | bronza | Janko · Vrtlog 2016 | 
| 2018 | бронза | bronza | Janko · Misija 2016 | 
| 2018 | бронза | bronza | Janko · Bifora 2016 | 
| 2018 | серебро | srebro | Janko · Stari Zavet 2015 | 
| 2018 | серебро | srebro | Janko · Zapis Crveni 2016 | 
| 2017 | бронза | bronza | Janko · Misija Barrique Chardonnay 2015 | 
| 2017 | бронза | bronza | Janko · Elena 2016 | 
| 2017 | бронза | bronza | Janko · Stari Zavet 2013 | 
| 2017 | бронза | bronza | Janko · Misija Chardonnay 2016 | 
| 2017 | золото | zlato | Janko · Vrtlog 2015 | 
| 2017 | отмечено | commended | Janko · Misija 2015 | 
| 2017 | серебро | srebro | Janko · Vrtlog 2015 | 
| 2017 | серебро | srebro | Janko · Zavet Stari Cuvée 2013 | 
| 2016 | бронза | bronza | Janko · Misija Chardonnay 2013 | 
| 2016 | отмечено | commended | Janko · Stari Zavet 2012 | 
| 2016 | серебро | srebro | Janko · Misija 2013 | 
| 2016 | серебро | srebro | Janko · Vrtlog 2015 | 
| 2015 | White wine Trophy | trofej | Janko · Vrtlog 2013 | 
| 2015 | бронза | bronza | Janko · Zavet 2013 | 
| 2015 | бронза | bronza | Janko · Stari Zavet 2012 | 
| 2015 | бронза | bronza | Janko · Misija 2013 | 
| 2015 | золото | zlato | Janko · Vrtlog 2013 | 
| 2015 | отмечено | commended | Janko · Zapis Crveni 2013 | 
| 2015 | отмечено | commended | Janko · Vrtlog 2013 | 
| 2014 | бронза | bronza | Janko · Zavet 2011 | 
| 2014 | золото | zlato | Janko · Misija 2011 | 
| 2014 | отмечено | commended | Janko · Vrtlog Sauvignon Blanc 2012 | 
| 2014 | отмечено | commended | Janko · Misija Chardonnay 2011 | 
| 2014 | платина | platina | Janko · Stari Zavet 2011 | 
| 2014 | серебро | srebro | Janko · Vrtlog 2012 | 
| 2013 | серебро | srebro | Janko · Zapis Crveni 2008 | 
| 2013 | серебро | srebro | Janko · Zavet Reserve 2008 | 

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
- Stemina winery · Draga 2008 — 94 [decanter]
- DiBonis Winery · Di Icewine 2020 — 94 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2023 — 94 [decanter]
- Podrum Pevac · GUŠT BARIK 2021 — 94 [biwc]
- Vinarija Dumo · MMXXI 2021 — 94 [biwc]
- Grabak · Prokupac 2020 — 94 [biwc]
- Vinarija Gamanović · Grasac beli 2020 — 94 [biwc]
- Vinarija Gnezdo · Sovinjon Kis 2021 — 94 [biwc]
- Fruškogorski · Tri SuncA 2015 — 93 [gilbert-gaillard]
- Virtus · Pinot Grigio 2024 — 93 [decanter]
- Vinarija Frug · Cabernet Sauvignon Signum 2021 — 93 [decanter]
- Dolina · Cuveé Barrique 2019 — 93 [decanter]
- DiBonis Winery · Di Icewine 2020 — 93 [awc-vienna]
- Vinarija DeLena · 1903 Merlot 2017 — 92 [Falstaff]
- Vinarija Jeremić · Kanon Merlot Cabernet Sauvignon 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Tamjanika 2020 — 92 [Falstaff]
- Josic Winery · Zmajevac Prokupac 2018 — 92 [Falstaff]
- Virtus · Credo 2013 — 92 [decanter]
- Vista Hill · Reserve White 2012 — 92 [decanter]
- Virtus · Credo Beli 2019 — 92 [decanter]
- Vinarija Sokolov Zamak · Moskato Giallo 2021 — 92 [decanter]
- Vinarija Sokolov Zamak · Marselan 2019 — 92 [decanter]
- Vinarija Frug · Chardonnay Signum 2023 — 92 [decanter]
- Vinarija Frug · Cuvée 2022 — 92 [decanter]
- Traško Vinarija · Bagrina Edición Limitada 2024 — 92 [decanter]
- Podrum Pevac · Tišina Malvazija 2025 — 92 [decanter]
- La Gora · Lupo 2025 — 92 [decanter]
- Vinarija Frug · Grašac 2025 — 92 [decanter]
- Dolina · Euphonia Gran Reserva 2018 — 92 [decanter]
- Grabak · Prokupac 2020 — 92 [decanter]
- Gora · White Blend 2024 — 92 [biwc]
- La Gora · Chardonnay 2025 — 92 [biwc]
- Vinarija Radlović doo · Cabernet Sauvignon 2020 — 92 [biwc]
- Podrum Pevac · Red wine Zagrljaj 2020 — 92 [awc-vienna]
- Vinarija Milićević · VLADAVINA Merlot 2021 — 92 [awc-vienna]
- PIK OPLENAC · Monarh Immortal S 2017 — 91 [Falstaff]
- Vinarija Jeremić · Sonata Sauvignon Blanc 2021 — 91 [Falstaff]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2019 — 91 [Falstaff]
- Virtus · Prokupac 2016 — 91 [decanter]
- Vinarija Aven · Merlot 2019 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Podrum Stari Hrast · Selekcija Merlot 2017 — 91 [decanter]
- Reljić Vinarija · Rebus Reserve 2019 — 91 [decanter]
- Virtus · Credo 2017 — 91 [decanter]
- Винарија Ступови (Vinarija Stupovi) · Merlot 2021 — 91 [decanter]
- VINARIJA STANKOVIĆ · Cabernet Sauvignon 2021 — 91 [decanter]
- Virtus · Prokupac 2020 — 91 [decanter]
- Vinarija Savic · Merlot 2021 — 91 [decanter]
- Vinarija Komuna PR · Rara Avis 2020 — 91 [decanter]
- Virtus · Marselan 2020 — 91 [decanter]
- Драгић Винарија (Vina Dragic) · Beli Biser 2022 — 91 [decanter]
- VINARIJA STANKOVIĆ · Chardonnay 2024 — 91 [decanter]
- Vinarija Frug · Pinot Noir 2022 — 91 [decanter]
- Vinarija Frug · Syrah Signum 2022 — 91 [decanter]
- Vinarija Imperator · Constantius 2023 — 91 [decanter]
- Драгић Винарија (Vina Dragic) · Mitra 2025 — 91 [decanter]
- Dolina · Barrique Xix Reserve 2019 — 91 [decanter]
- Podrum Pevac · PROKUPAC 2021 — 91 [biwc]
- Vinarija Mrdjanin · Bermet 2021 — 91 [biwc]
- Vinarija Tri Tachke · Rezonanca 2022 — 91 [biwc]
- La Gora · Lupo 2025 — 91 [biwc]
- Vinarija Pet Hrastova · Tamjanika 2024 — 91 [awc-vienna]
- Podrum Petrović · Grašac-Podrum 2024 — 91 [awc-vienna]
- Vinarija VRT · dark riđo wine 2021 — 91 [awc-vienna]
- Vinska Kuća Rajić · ROSÉ 2023 — 91 [awc-vienna]
- Podrum Pevac · Red Wine "ZAGRLJAJ" 2019 — 91 [awc-vienna]
- Krstašica Doo · Merlot 2020 — 91 [awc-vienna]
- BT Winery · SoutEast Prokupac 2017 — 91 [awc-vienna]
- Podrum Pevac · White wine "GUST" 2019 — 91 [awc-vienna]
- Bacina vino d.o.o. · Dolina red XVII 2017 — 91 [awc-vienna]
- Vista Hill · Red Selection Merlot 2017 — 91 [awc-vienna]
- Virtus · MARSELAN 2016 — 91 [awc-vienna]
- Mikić · Crveno vino 2013 — 91 [awc-vienna]
- Virtus · GEWURZTRAMINER 2016 — 91 [awc-vienna]
- Virtus · CREDO 2015 — 91 [awc-vienna]
- Virtus · CREDO BELI 2014 — 91 [awc-vienna]
- Vinarija DeLena · 70/30 Sauvignon Blanc /Semillon 2020 — 90 [Falstaff]
- AURUS Winery & Distillery · Cabernet 2022 — 90 [awc-vienna]
- Podrum Dremina · Cabernet Sauvignon 2023 — 90 [awc-vienna]
- PR Anjino Vino · Anjino Vino 2024 — 90 [awc-vienna]
- Podrum Zlatanović · Branko Savić 2025 — 90 [awc-vienna]
- Vinarija Dumo · Pinot Noir 2015 — 90 [decanter]
- Virtus · Pinot Grigio 2017 — 90 [decanter]
- Virtus · Credo 2013 — 90 [decanter]
- Pusula Winery · Traminac 2017 — 90 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2017 — 90 [decanter]
- Virtus · Prokupac 2016 — 90 [decanter]
- Virtus · Marselan 2016 — 90 [decanter]
- Virtus · Prokupac 733  — 90 [decanter]
- Zmajevac · Cuvée 2017 — 90 [decanter]
- Zmajevac · Prokupac 2018 — 90 [decanter]
- Vinarija Sokolov Zamak · Marselan 2020 — 90 [decanter]
- Virtus · 733 2017 — 90 [decanter]
- Grabak · Sojka 2021 — 90 [decanter]
- Vinarija Đurđevića Legat · Otisak Vremena 2020 — 90 [decanter]
- Reljić Vinarija · Rebus Crveno 2020 — 90 [decanter]
- Podrum Petrović · Grašac 2022 — 90 [decanter]
- Vinarija Venčac · Legat 1903 Muscat Petit Grain 2021 — 90 [decanter]
- Château Prince · Velika Morava 2021 — 90 [decanter]
- Art Et Vinum · Meduza 2021 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2020 — 90 [decanter]
- Manufaktura Spasić · Rebo 2020 — 90 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2021 — 90 [decanter]
- Vinarija Milićević · Vladavina Icone Merlot 2021 — 90 [decanter]
- Vinarija Fleur D'Oranger · Grof Muskat Krokan 2021 — 90 [decanter]
- VINARIJA STANKOVIĆ · Cabernet Sauvignon 2022 — 90 [decanter]
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
- VINARIJA STANKOVIĆ · Cabernet Sauvignon 2023 — 90 [decanter]
- Vinarija Frug · Chardonnay Signum 2022 — 90 [decanter]
- Vinarija Zorča · Velika Dusa Merlot 2019 — 90 [decanter]
- Vinarija Unikat · Vranac 2019 — 90 [decanter]
- Драгић Винарија (Vina Dragic) · Crni Biser 2023 — 90 [decanter]
- Podrum Pevac · ZAGRLJAJ 2019 — 90 [biwc]
- Vinarija Gamanović · Grasac Beli 2020 — 90 [biwc]
- Rakicevic · Blagoslov 2020 — 90 [biwc]
- Podrum Pevac · KABERNE FRAN 2023 — 90 [biwc]
- MV Vinarija · Tamjanika Hope 2022 — 90 [biwc]
- Vinarija Frug · Grašac 2024 — 90 [biwc]
- Vinarija Frug · Chardonnay Signum 2023 — 90 [biwc]
- Vinarija Frug · Cuvee 2022 — 90 [biwc]
- Vinarija Milićević · VladaVina 2023 — 90 [biwc]
- Vinarija Ilić-Nijemčević · IG 2025 — 90 [biwc]
- Château Prince · Charm 2024 — 90 [biwc]
- Vinarija Ilić-Nijemčević · IG 2024 — 90 [biwc]
- La Gora · Bello 2025 — 90 [biwc]
- Podrum Dremina · Prokupac 2022 — 90 [awc-vienna]
- Podrum Dremina · Tamjanika 2024 — 90 [awc-vienna]
- AURUS Winery & Distillery · Tamjanika 2022 — 90 [awc-vienna]
- AURUS Winery & Distillery · Red Cuvée Veritas 2021 — 90 [awc-vienna]
- Grabak · Bela Golubica 2024 — 90 [awc-vienna]
- Vinarija Milićević · VLADAVINA Cabernet Savignon 2023 — 90 [awc-vienna]
- Vinarija Milićević · Vladavina Icone Merlot 2021 — 90 [awc-vienna]
- Château Prince · Probus m Barik 2021 — 90 [awc-vienna]
- Podrum Pevac · WHITE WINE TINO TEČE 2023 — 90 [awc-vienna]
- Podrum Pevac · RED WINE KABERNE FRAN 2023 — 90 [awc-vienna]
- Podrum Petrović · Bermet "Braće 2021 — 90 [awc-vienna]
- Vinarija 100 Žena · 100 žena-100 women-Monsieur Merlot 2021 — 90 [awc-vienna]
- Bacina vino d.o.o. · Dolina Merlot 2018 — 90 [awc-vienna]
- Vinarija Podrum Danguba · "Ponovo naše" Tamjanika 2021 — 90 [awc-vienna]
- Podrum Pevac · White wine "GUŠT" (Barrique) 2020 — 90 [awc-vienna]
- Podrum Stari Hrast · Sauvignon Blanc 2021 — 90 [awc-vienna]
- Bacina vino d.o.o. · Dolina XIX red 2019 — 90 [awc-vienna]
- Vinarija Ilić-Nijemčević · Chardonnay 2020 — 90 [awc-vienna]
- Vista Hill · Reserve Red 2010 — 90 [awc-vienna]
- Bacina vino d.o.o. · Dolina XVIII red 2018 — 90 [awc-vienna]
- BT Winery · President Vranac 2017 — 90 [awc-vienna]
- Podrum Stari Hrast · Podrum Stari hrast 2017 — 90 [awc-vienna]
- Bacina vino d.o.o. · Dolina red 2017 — 90 [awc-vienna]
- Nikad Nije Kasno · Signature 2016 — 90 [awc-vienna]
- Podrum Stari Hrast · Chardonnay 2016 — 90 [awc-vienna]
- Podrum Stari Hrast · Podum Stari hrast Sauvignon blanc 2016 — 90 [awc-vienna]
- Vinarija KM · Merlot Stari 2016 — 90 [awc-vienna]
- Virtus · PINOT GRIGIO 2017 — 90 [awc-vienna]
- Virtus · PINOT NOIR 2015 — 90 [awc-vienna]
- Virtus · CREDO BELI 2015 — 90 [awc-vienna]
- Virtus · MARSELAN 2015 — 90 [awc-vienna]
- Virtus · SAUVIGNON BLANC 2014 — 90 [awc-vienna]
- Virtus · CREDO 2013 — 90 [awc-vienna]
- PIK OPLENAC · Constanta Muse Sauvignon Blanc 2021 — 89 [Falstaff]
- PIK OPLENAC · Constanta Muse Rose 2019 — 89 [Falstaff]
- Mikić · Chardonnay 2025 — 89 [awc-vienna]
- Podrum Dremina · Blanc Coupage 2024 — 89 [awc-vienna]
- AURUS Winery & Distillery · Merlot 2022 — 89 [awc-vienna]
- Virtus · W 2019 — 89 [decanter]
- Stemina winery · Panta Rei Chardonnay 2018 — 89 [decanter]
- BT Winery · President Vranac Gold 2018 — 89 [decanter]
- Vinarija Dumo · Pinot Noir 2019 — 89 [decanter]
- Virtus · Prokupac 2018 — 89 [decanter]
- Marselan · Marselan 2019 — 89 [decanter]
- Трилогия Винария - Vinarija Trilogija · Pečat Grand Reserve 2017 — 89 [decanter]
- Драгић Винарија (Vina Dragic) · Randes 2021 — 89 [decanter]
- Vinarija Mrdjanin · Family Edition Probus 2020 — 89 [decanter]
- Vinarija Todorović · Merlot 2020 — 89 [decanter]
- Virtus · Credo 2020 — 89 [decanter]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 89 [decanter]
- Podrum Pevac · Gušt 2023 — 89 [decanter]
- Karić Vinarija · Adria Belo 2023 — 89 [decanter]
- VINARIJA STANKOVIĆ · Chardonnay 2023 — 89 [decanter]
- Krstašica Doo · Konekicja Sauvignon Blanc 2023 — 89 [decanter]
- Breg · Tamjanika 2024 — 89 [decanter]
- Vinarija Grumen · Morava 2024 — 89 [decanter]
- Vinarija Sokolov Zamak · Marselan 2021 — 89 [decanter]
- Virtus · Credo 2024 — 89 [decanter]
- Vinska Kuća Rajić · Tamjanika 2024 — 89 [decanter]
- Vinska Kuća Rajić · Triva Souvignier Gris 2024 — 89 [decanter]
- La Gora · Lupo 2024 — 89 [decanter]
- Vinarija Imperator · Max 2021 — 89 [decanter]
- Traško Vinarija · Fabulous Cabernet Franc 2022 — 89 [decanter]
- Vinarija Frug · Pinot Noir 2023 — 89 [decanter]
- La Gora · Sauvignon Blanc 2025 — 89 [decanter]
- Vinarija Frug · Chardonnay Signum 2023 — 89 [decanter]
- Château Prince · Probus M barrique 2020 — 89 [biwc]
- Château Prince · Chateau Shiraz 2021 — 89 [biwc]
- Podrum Petrović · Grašac 2022 — 89 [biwc]
- Milanov Podrum · Prolog 2017 — 89 [biwc]
- Vinarija Dumo · Pinot Noir 2020 — 89 [biwc]
- Vinarija Komazec · Gazdino Crveno – Tesla 2020 — 89 [biwc]
- Vinarija Komazec · Palava 2021 — 89 [biwc]
- Vinarija Mrdjanin · Merlot 2021 — 89 [biwc]
- Vinarija Teodos · Traminac 2021 — 89 [biwc]
- Vinarija VRT · ROSSE 2022 — 89 [biwc]
- Podrum Pevac · TIHO TEČE 2023 — 89 [biwc]
- Vinarija Blagojević · Probus M barik 2021 — 89 [biwc]
- Château Prince · Shiraz Premium 2021 — 89 [biwc]
- Vinarija VRT · pesak kvarcni 2023 — 89 [biwc]
- PR Anjino Vino · Siesta 2023 — 89 [biwc]
- Château Prince · Cuvee 2021 — 89 [biwc]
- Château Prince · Princess 2021 — 89 [biwc]
- Château Prince · Velika 2023 — 89 [biwc]
- Vinarija Frug · Pinot Noir 2023 — 89 [biwc]
- Podrum Pevac · Izazov 2024 — 89 [biwc]
- Vinska Kuća Rajić · Tamjanika 2024 — 89 [biwc]
- Vinska Kuća Rajić · Monika 2023 — 89 [biwc]
- Vinarija Milićević · Merlo Classic 2021 — 89 [biwc]
- Vinarija Gnezdo · Belo 2024 — 89 [biwc]
- Vinarija Gnezdo · Belo 2025 — 89 [biwc]
- Vinarija Blagojević · Probus M Barik 2022 — 89 [biwc]
- La Gora · Lupo 2024 — 89 [biwc]
- Podrum Pevac · Gušt, Chardonnay Sur Lie 2023 — 89 [biwc]
- Vinarija 100 Žena · Veliki Dečko 2022 — 89 [biwc]
- Vinarija Milićević · Cabernet ICONE 2023 — 89 [biwc]
- Vinarija Milićević · Grašac 2024 — 89 [biwc]
- Vinarija Slatina · Grašac 2025 — 89 [biwc]
- Vinarija Tasa · Morava 2025 — 89 [biwc]
- VINARIJA STANKOVIĆ · CHARDONNAY 2024 — 89 [awc-vienna]
- Podrum Pevac · White wine "Malvazija", 0,75l 2025 — 89 [awc-vienna]
- Koreni 1934 · Vinary Koreni 1934 Merlot 2022 — 89 [awc-vienna]
- VINARIJA STANKOVIĆ · CHARDONNAY 2023 — 89 [awc-vienna]
- Podrum Petrović · Sila-Penušavo 2024 — 89 [awc-vienna]
- Vinarija PIRG · Sauvignon Blanc 2022 — 89 [awc-vienna]
- Anatea Vinarija · Nataša 2023 — 89 [awc-vienna]
- Vinarium winery · Pinoranž 2022 — 89 [awc-vienna]
- VINARIJA STANKOVIĆ · CABERNET SAUVIGNON 2022 — 89 [awc-vienna]
- Vinarija Dumo · Pinot Noir 2021 — 89 [awc-vienna]
- Podrum Pevac · WHITE WINE IZAZOV 2023 — 89 [awc-vienna]
- Podrum Petrović · Sila-Penušavo vino 2023 — 89 [awc-vienna]
- Bacina vino d.o.o. · Dolina XX 2020 — 89 [awc-vienna]
- HUP MIHAJLOVAC · Djurdjevica Legat - Otisak 2020 — 89 [awc-vienna]
- Podrum Petrović · Sila 2022 — 89 [awc-vienna]
- Podrum Pevac · White Wine "GUŠT" Barrique 2021 — 89 [awc-vienna]
- Vinarija Ilić-Nijemčević · Sauvignon Blanc 2020 — 89 [awc-vienna]
- Podrum Pevac · White wine "IZAZOV" 2021 — 89 [awc-vienna]
- Bacina vino d.o.o. · Dolina red 2018 — 89 [awc-vienna]
- Vinarija Praška · Cabernet Sauvignon 2021 — 89 [awc-vienna]
- Vinarija Komazec · Rosé Vinarije 2021 — 89 [awc-vienna]
- Vinarija Radlović doo · Cabernet Sauvignon 2017 — 89 [awc-vienna]
- Vinarija Radlović doo · Cabernet Sauvignon 2018 — 89 [awc-vienna]
- Vista Hill · White 2019 — 89 [awc-vienna]
- Vista Hill · Reserve White 2012 — 89 [awc-vienna]
- BT Winery · King Supreme Marselan 2018 — 89 [awc-vienna]
- Vinarija Ilić-Nijemčević · Chardonnay 2019 — 89 [awc-vienna]
- Fruškogorski · QUET Cuvée Limited Edition 2017 — 89 [awc-vienna]
- Nikad Nije Kasno · Signature 2017 — 89 [awc-vienna]
- Nikad Nije Kasno · Simfonija 2017 — 89 [awc-vienna]
- Vista Hill · red selection Merlot 2017 — 89 [awc-vienna]
- Podrum Stari Hrast · Chardonnay 2017 — 89 [awc-vienna]
- Vista Hill · White Reserve Grasac 2012 — 89 [awc-vienna]
- Winery Milosavljevic · Vila Vina Jefimija Tamjanika 2017 — 89 [awc-vienna]
- Vinarija KM · Merlot Stari 2016 — 89 [awc-vienna]
- Vinarija Komuna PR · Rajnski Rirzling Radoznao Taman Koliko Treba 2016 — 89 [awc-vienna]
- Vinarija ĐORĐE · FRESKA BELA 2017 — 89 [awc-vienna]
- Virtus · CREDO BELI 2016 — 89 [awc-vienna]
- Virtus · ROSE 2017 — 89 [awc-vienna]
- Mikić · Pinot Rosé 2016 — 89 [awc-vienna]
- Pusula Winery · rosé 2016 — 89 [awc-vienna]
- Pusula Winery · cabernet sauvignon 2013 — 89 [awc-vienna]
- Virtus · PINOT GRIGIO 2016 — 89 [awc-vienna]
- Virtus · PINOT NOIR 2014 — 89 [awc-vienna]
- Jelena Munizaba PR Radnja za proizvodnju grozdja i vina, turizam i ugostiteljstvo. · Cabernet Franc 2021 — 88 [awc-vienna]
- Bacina vino d.o.o. · Dolina XII  — 88 [decanter]
- Virtus · Gewürztraminer 2014 — 88 [decanter]
- Vinarija Komuna PR · Chardonnay 2015 — 88 [decanter]
- Virtus · Marselan 2015 — 88 [decanter]
- Virtus · Marselan 2016 — 88 [decanter]
- Pusula Winery · Sauvignon Blanc 2017 — 88 [decanter]
- Grabak · Prokupac 2017 — 88 [decanter]
- PIK OPLENAC · Monarh S 2015 — 88 [decanter]
- Nikad Nije Kasno · Signature 2016 — 88 [decanter]
- Vinarija Dumo · Pinot Noir 2017 — 88 [decanter]
- PIK OPLENAC · Monarh Immortal S 2017 — 88 [decanter]
- Vinarija DeLena · 1903 Merlot 2016 — 88 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Manzoni 2019 — 88 [decanter]
- Probus Vineyards · Traminac 2018 — 88 [decanter]
- Vinarija Aven · Balance 2018 — 88 [decanter]
- Grabak · Prva Lasta Prokupac 2021 — 88 [decanter]
- BT Winery · Kings Crown 2020 — 88 [decanter]
- Николић Неyзински (Nikolićh Neuzinsky) · The Secret Code of Our Terroir 2020 — 88 [decanter]
- Vinarija Aven · Balance 2019 — 88 [decanter]
- Max-Ex Doo · Rebus Crveni 2019 — 88 [decanter]
- Podrum Petrović · Cabernet Sauvignon 2019 — 88 [decanter]
- Virtus · Marselan 2018 — 88 [decanter]
- Vinarija Komazec · Palava 2021 — 88 [decanter]
- Virtus · Sauvignon Blanc 2021 — 88 [decanter]
- Николић Неyзински (Nikolićh Neuzinsky) · Santa Maria 2021 — 88 [decanter]
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
- Vinska Kuća Rajić · Prokupac 2024 — 88 [decanter]
- La Gora · Bello 2024 — 88 [decanter]
- Vinarija Imperator · Gratianus Traminac 2021 — 88 [decanter]
- Traško Vinarija · Fucking Fabulous Edición Limitada 2021 — 88 [decanter]
- Château Prince · Gospodar 2021 — 88 [decanter]
- Traško Vinarija · Fabulous Cabernet Sauvignon 2022 — 88 [decanter]
- La Gora · Chardonnay 2025 — 88 [decanter]
- Breg · Grašac 2025 — 88 [decanter]
- Vinarija Imperator · VAL Rajnski Rizling 2022 — 88 [decanter]
- Grabak · Vivak Prokupac 2019 — 88 [decanter]
- Vinarija Zorča · Mali Ratnik Cabernet Sauvignon 2020 — 88 [decanter]
- Vinarija Baza · Barre 2021 — 88 [biwc]
- Vinarija Komazec · Palava 2022 — 88 [biwc]
- Vinarija Radlović doo · Cirkuz Rose 2022 — 88 [biwc]
- Podrum Šukac · Merlot 2019 — 88 [biwc]
- Vinarija VRT · pesak beli 2023 — 88 [biwc]
- Gora · Grašac 2024 — 88 [biwc]
- Vinska Kuća Rajić · Chardonnay 2023 — 88 [biwc]
- Vinarija 100 Žena · Veliki Dečko 2022 — 88 [biwc]
- Plavinci · Indigo Reserva 2019 — 88 [biwc]
- Château Prince · Gospodar 2021 — 88 [biwc]
- Vinarija Gamanović · Grasac Beli 2025 — 88 [biwc]
- Langov Podrum · Lang Grašac beli 2025 — 88 [biwc]
- Vinarija Milićević · Grašac 2025 — 88 [biwc]
- Vinarija Pet Hrastova · Prokupac 2024 — 88 [awc-vienna]
- Podrum Pevac · White wine "GUŠT" sur-lie 0,75l 2023 — 88 [awc-vienna]
- Vinarija Milićević · VLADAVINA Riesling 2024 — 88 [awc-vienna]
- Vinarija 100 Žena · Tamjanika 2023 — 88 [awc-vienna]
- Vinska Kuća Rajić · Tamjanika 2023 — 88 [awc-vienna]
- Château Prince · Charm Morava and Chardonnay 2023 — 88 [awc-vienna]
- Podrum Pevac · ROSE WINE PROKUPAC 2023 — 88 [awc-vienna]
- Podrum Pevac · RED WINE PROKUPAC 2021 — 88 [awc-vienna]
- VINARIJA STANKOVIĆ · CHARDONNAY 2022 — 88 [awc-vienna]
- Fruškogorski · Quet Chardonnay 2016 — 88 [awc-vienna]
- Fruškogorski · Quet Merlot 18+ edition 2018 — 88 [awc-vienna]
- Podrum Petrović · Grašac 2022 — 88 [awc-vienna]
- Podrum Pevac · Red Wine "PROKUPAC" 2021 — 88 [awc-vienna]
- Vinarija Ilić-Nijemčević · Frankovka 2020 — 88 [awc-vienna]
- Podrum Pevac · White Wine "IZAZOV" 2022 — 88 [awc-vienna]
- Krstašica Doo · Chardonnay 2021 — 88 [awc-vienna]
- Vinarija Ilić-Nijemčević · Chardonnay 2020 — 88 [awc-vienna]
- Vinarija Praška · Rose 2021 — 88 [awc-vienna]
- Vinarija Komazec · Palava vinarije 2021 — 88 [awc-vienna]
- Vinarija Komazec · Gazdino Crveno Vinarije 2019 — 88 [awc-vienna]
- Fruškogorski · Quet Grašac 2019 — 88 [awc-vienna]
- Podrum Pevac · Red Wine "Prokupac" 2018 — 88 [awc-vienna]
- Vinarium winery · Dedovac 2018 — 88 [awc-vienna]
- Winery Milosavljevic · Vila Vina Prokupac 2017 — 88 [awc-vienna]
- Vinarija Podrum Danguba · Tek Smo Počeli-Rajnski Rizling 2015 — 88 [awc-vienna]
- Vinarija Šveljo · Heavenly Flower 2019 — 88 [awc-vienna]
- Vinarija VRT · PESAK PLAVI 2018 — 88 [awc-vienna]
- Nikad Nije Kasno · Melodija 2019 — 88 [awc-vienna]
- Podrum Pevac · White Wine "Izazov" Tamjanika 2017 — 88 [awc-vienna]
- Vinarija Ilić-Nijemčević · Sauvignon Blanc 2017 — 88 [awc-vienna]
- Podrum Pevac · Rosé Wine "Kukuriku" Cabernet Franc 2017 — 88 [awc-vienna]
- Podrum Pevac · Red Wine "Zagraljaj" Cabernet Franc, Cabernet Sauvignon 2017 — 88 [awc-vienna]
- Vinarija Komuna PR · Muscat Blanc a Petit Grain 2017 — 88 [awc-vienna]
- Vinarija Komuna PR · Merlot 2017 — 88 [awc-vienna]
- Pusula Winery · Sauvignon blanc 2017 — 88 [awc-vienna]
- Mikić · Crna Tamjanika 2017 — 88 [awc-vienna]
- Virtus · PROKUPAC 2016 — 88 [awc-vienna]
- Fruškogorski · Quet Pinot Noir 2016 — 88 [awc-vienna]
- Fruškogorski · Quet Merlot 18+ 2013 — 88 [awc-vienna]
- Vinarija Dumo · Pinot Noir 2016 — 88 [awc-vienna]
- Mikić · Chardonnay 2017 — 88 [awc-vienna]
- Mikić · Sovignon Blanc 2017 — 88 [awc-vienna]
- Virtus · SAUVIGNON BLANC 2017 — 88 [awc-vienna]
- Virtus · CREDO 2015 — 88 [awc-vienna]
- Vinarija ĐORĐE · SOVINJON BELI 2017 — 88 [awc-vienna]
- Vinarija ĐORĐE · Freska Rose 2017 — 88 [awc-vienna]
- Mikić · Crna Tamjanika 2016 — 88 [awc-vienna]
- Virtus · PROKUPAC 2014 — 88 [awc-vienna]
- Mikić · Pinot Noir 2015 — 88 [awc-vienna]
- Pusula Winery · chardonnay 2015 — 88 [awc-vienna]
- Pusula Winery · sauvignon blanc 2016 — 88 [awc-vienna]
- Pusula Winery · traminac 2016 — 88 [awc-vienna]
- Virtus · SAUVIGNON BLANC 2016 — 88 [awc-vienna]
- AURUS Winery & Distillery · Chardonnay 2023 — 87 [awc-vienna]
- Vinarija Ždrnja · Grašac 2025 — 87 [awc-vienna]
- Mikić · Bagrina 2024 — 87 [awc-vienna]
- Atos-Fructum · The 2015 — 87 [decanter]
- Probus Vineyards · Magis 2017 — 87 [decanter]
- Grabak · Siva Vrana 2017 — 87 [decanter]
- Virtus · W Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Noir 2017 — 87 [decanter]
- Vinarija Janucic · Vulkan Merlot 2017 — 87 [decanter]
- Zmajevac · Prokupac 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2019 — 87 [decanter]
- PIK OPLENAC · Monarh Immortal Cuvée 2015 — 87 [decanter]
- Vinarija Aven · Merlot 2018 — 87 [decanter]
- Zmajevac · Chardonnay 2019 — 87 [decanter]
- Virtus · Marselan 2017 — 87 [decanter]
- Zmajevac · Cuvée 2017 — 87 [decanter]
- Virtus · Pinot Grigio 2020 — 87 [decanter]
- BT Winery · King Supreme Marselan 2020 — 87 [decanter]
- Virtus · Gewurztraminer 2021 — 87 [decanter]
- Virtus · Prokupac 2018 — 87 [decanter]
- Bacina vino d.o.o. · Dolina 2018 — 87 [decanter]
- Podrum Pevac · Zagrljaj 2019 — 87 [decanter]
- Probus Vineyards · Belim 2017 — 87 [decanter]
- Vinarija Gamanović · Cabernet Sauvignon 2020 — 87 [decanter]
- Virtus · Pinot Grigio 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Rajnski Rizling 2020 — 87 [decanter]
- Манастир Студеница (Manastir Studenica) · Prokupac 1186 2020 — 87 [decanter]
- Vinarija Bora · Frenk 2020 — 87 [decanter]
- Grabak · Prokupac 2020 — 87 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2021 — 87 [decanter]
- Podrum Pevac · Prokupac 2021 — 87 [decanter]
- Vinarija PIRG · Sauvignon Blanc 2021 — 87 [decanter]
- Манастир Студеница (Manastir Studenica) · Bela Reč Tamjanika 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Chardonnay 2022 — 87 [decanter]
- VINARIJA STANKOVIĆ · Chardonnay 2022 — 87 [decanter]
- Драгић Винарија (Vina Dragic) · Randes 2022 — 87 [decanter]
- Virtus · Prokupac 2019 — 87 [decanter]
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
- Vinarija Gnezdo · Muskat Krokan 2024 — 87 [decanter]
- Natural Grape Concept · Tamjanika 2024 — 87 [decanter]
- Vinarija Fleur D'Oranger · Krokan Muskat 2024 — 87 [decanter]
- Vinarija Imperator · Cargraš 2024 — 87 [decanter]
- Virtus · Prokupac 2021 — 87 [decanter]
- Vinarija Frug · Signum Cuvée 2022 — 87 [decanter]
- Mister · Marselan 2022 — 87 [decanter]
- Virtus · Prokupac 2022 — 87 [decanter]
- Vinska Kuća Rajić · Monika 2023 — 87 [decanter]
- Natural Grape Concept · Prokupac 2023 — 87 [decanter]
- Орлић Породична Винарија - Orlić Family Winery · MMXXIII Shiraz 2023 — 87 [decanter]
- Vinarija Imperator · Frušet Rosé Brut 2022 — 87 [decanter]
- Podrum Petrović · Bermet Braće 2021 — 87 [biwc]
- Grabak · Vivak Prokupac 2019 — 87 [biwc]
- Vinarija Komazec · Cabernet Sauvignon 2021 — 87 [biwc]
- Vinarija Komazec · Gazdino Crveno 2019 — 87 [biwc]
- Винарија Ступови (Vinarija Stupovi) · Cabernet Sauvignon 2021 — 87 [biwc]
- Винарија Ступови (Vinarija Stupovi) · Merlot 2021 — 87 [biwc]
- Château Prince · CUVEE 2021 — 87 [biwc]
- Vinska Kuća Rajić · RAJIĆ 2023 — 87 [biwc]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 87 [biwc]
- MV Vinarija · Tamjanika – Hope 2021 — 87 [biwc]
- PR Anjino Vino · Suton 2022 — 87 [biwc]
- Bajilo · Grasac 2021 — 87 [biwc]
- Lutak winery · Merlo 2022 — 87 [biwc]
- Grabak · Bela golubica 2024 — 87 [biwc]
- Vinarija Gamanović · Samotok 2022 — 87 [biwc]
- Vinarija Slatina · Tamjanika 2025 — 87 [biwc]
- Vinarija 100 Žena · Roze 2025 — 87 [biwc]
- Vinarija Radlović doo · Chardonnay 2024 — 87 [biwc]
- Vinarija Radlović doo · Cirkuz Rose 2025 — 87 [biwc]
- Hrusija d.o.o. Leskovac · Simfonija - Prokupac 65%, Kaberne sovinjon 20%, Merlot 15% 2021 — 87 [awc-vienna]
- Vinarija VRT · pesak plavi 2024 — 87 [awc-vienna]
- Vinarija Gamanović · Grasac beli 2020 — 87 [awc-vienna]
- Fruškogorski · Quet Traminac 2022 — 87 [awc-vienna]
- Vinarija Dumo · Blanc de Noir Pinot Noir 2022 — 87 [awc-vienna]
- Château Prince · Princess Premium 2022 — 87 [awc-vienna]
- Milanov Podrum · Lutka Tamjanika Bela 2022 — 87 [awc-vienna]
- HUP MIHAJLOVAC · Djurdjevica Legat-Pinot Grigio 2021 — 87 [awc-vienna]
- HUP MIHAJLOVAC · Djurdjevica Legat - Do neba i nazad 2021 — 87 [awc-vienna]
- HUP MIHAJLOVAC · Djurdjevica Legat - Otisak vremena 2020 — 87 [awc-vienna]
- Krstašica Doo · Sauvignon Blanc 2021 — 87 [awc-vienna]
- Bacina vino d.o.o. · Dolina Rosé 2020 — 87 [awc-vienna]
- Winery Milosavljevic · Vila Vina Sauvignon Blanc 2019 — 87 [awc-vienna]
- Vista Hill · Reserve White 2012 — 87 [awc-vienna]
- Bacina vino d.o.o. · Dolina Rose 2019 — 87 [awc-vienna]
- Vinarija Ilić-Nijemčević · Cabernet Sauvignon 2017 — 87 [awc-vienna]
- Fruškogorski · Quet Merlot 2015 — 87 [awc-vienna]
- Vinarija Podrum Danguba · Tek smo počeli-Rajnski rizling 2017 — 87 [awc-vienna]
- Vinarija KM · Rhine riesling Ledeni 2016 — 87 [awc-vienna]
- Mikić · Porta Cuvée 2015 — 87 [awc-vienna]
- Vinarija ĐORĐE · TRAMINAC MIRISNI 2017 — 87 [awc-vienna]
- Vinarija ĐORĐE · FRESKA CRVENA 2017 — 87 [awc-vienna]
- Vinarija Podrum Danguba · Ponovo naše Tamjanika 2016 — 87 [awc-vienna]
- Virtus · PROKUPAC 2013 — 87 [awc-vienna]
- Virtus · GEWURZTRAMINER 2014 — 87 [awc-vienna]
- Virtus · ROSÉ 2014 — 87 [awc-vienna]
- Virtus · MARSELAN 2014 — 87 [awc-vienna]
- Anatea Vinarija · Anatea 2025 — 86 [awc-vienna]
- Virtus · Credo 2013 — 86 [decanter]
- Mcculloch Wines · Traminac 2013 — 86 [decanter]
- Virtus · Credo Beli 2015 — 86 [decanter]
- Virtus · Gewürztraminer 2017 — 86 [decanter]
- Grabak · Modrovrana 2015 — 86 [decanter]
- Virtus · Pinot Noir 2015 — 86 [decanter]
- PIK OPLENAC · Villa Muscat Ottonel 2015 — 86 [decanter]
- Vinarija Komuna PR · Chardonnay 2017 — 86 [decanter]
- Pusula Winery · Cabernet 2015 — 86 [decanter]
- Virtus · Credo 2017 — 86 [decanter]
- Nikad Nije Kasno · Simfonija 2017 — 86 [decanter]
- Vista Hill · Premium 2019 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Sauvignon Blanc 2019 — 86 [decanter]
- Virtus · Sauvignon Blanc 2019 — 86 [decanter]
- Vinarija Aven · Cabernet Sauvignon 2018 — 86 [decanter]
- BT Winery · King's Crown 2018 — 86 [decanter]
- Prokupac · Prokupac 2018 — 86 [decanter]
- Pusula Winery · Cabernet 2017 — 86 [decanter]
- Grabak · Modrovrana 2017 — 86 [decanter]
- Zmajevac · Cuvée Reserve 2017 — 86 [decanter]
- Vinarija Komazec · Rose 2021 — 86 [decanter]
- Grabak · Prokupac 2019 — 86 [decanter]
- Vinarija Đurđevića Legat · Otisak 2020 — 86 [decanter]
- Tri Medje I Oblak · Vagabundo Cabernet Sauvignon 2020 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Kibic 2021 — 86 [decanter]
- Vinarija Podrum Danguba · Ponovo Naše Tamjanika 2021 — 86 [decanter]
- Vinarija Gamanović · Tamjanika Bela 2021 — 86 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum Cabernet Franc 2020 — 86 [decanter]
- Manufaktura Spasić · Krivac 2020 — 86 [decanter]
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
- Vinarija VRT · PESAK BELI 2022 — 86 [biwc]
- Podrum Pevac · PROKUPAC ROZE 2023 — 86 [biwc]
- Podrum Šukac · Sauvignon Blanc 2023 — 86 [biwc]
- Vinarija Gnezdo · Belo 2023 — 86 [biwc]
- Vinarija VRT · pesak plavi 2021 — 86 [biwc]
- Lutak winery · Lutkovo crno 2022 — 86 [biwc]
- Lutak winery · S-Kvark 2022 — 86 [biwc]
- Vinarija Dumo · Pinot Noir 2022 — 86 [biwc]
- Vinarija Tri Tachke · Rezonanca limited 2021 — 86 [biwc]
- Château Prince · Velika 2024 — 86 [biwc]
- La Gora · Sauvignon Blanc 2025 — 86 [biwc]
- Vinarija Milićević · Sauvignon Blanc 2025 — 86 [biwc]
- Vinarija Radlović doo · Morava 2025 — 86 [biwc]
- Vinarija Pet Hrastova · Rosé 2023 — 86 [awc-vienna]
- Vinarija Ilić-Nijemčević · Cabernet Sauvignon 2018 — 86 [awc-vienna]
- Bacina vino d.o.o. · Dolina Rosé 2021 — 86 [awc-vienna]
- Vinarija Praška · Chardonnay 2020 — 86 [awc-vienna]
- Vinarija Ilić-Nijemčević · Sauvignon Blanc 2020 — 86 [awc-vienna]
- Драгић Винарија (Vina Dragic) · Carski Drum Rajnski Rizling 2020 — 86 [awc-vienna]
- Vinarium winery · Župljanka 2019 — 86 [awc-vienna]
- Vinarija Ilić-Nijemčević · Sauvignon Blanc 2019 — 86 [awc-vienna]
- Vinarija Ilić-Nijemčević · Rajnski Rizling 2019 — 86 [awc-vienna]
- Podrum Pevac · White wine "IZAZOV" 2019 — 86 [awc-vienna]
- Fruškogorski · Quet Grašac 2017 — 86 [awc-vienna]
- Vinarija Ilić-Nijemčević · Chardonnay 2017 — 86 [awc-vienna]
- Pusula Winery · Chardonnay 2017 — 86 [awc-vienna]
- Virtus · Rosé 2015 — 86 [awc-vienna]
- Virtus · PINOT GRIGIO 2014 — 86 [awc-vienna]
- Pusula Winery · ROSÉ 2013 — 86 [awc-vienna]
- Vinarija Podrum Danguba · "Nema dalje" Chardonnay 2015 — 85 [awc-vienna]
- Bacina vino d.o.o. · Dolina 2012 — 85 [decanter]
- Virtus · Sauvignon Blanc 2017 — 85 [decanter]
- PIK OPLENAC · Monarh Cuvée 2014 — 85 [decanter]
- Fruškogorski · Quet Pinot Noir 2016 — 85 [decanter]
- PIK OPLENAC · Monarh Immortal Cuvée 2014 — 85 [decanter]
- Virtus · Pinot Noir 2015 — 85 [decanter]
- Vinarija Dumo · Pinot Noir 2016 — 85 [decanter]
- Vista Hill · Selection Red 2017 — 85 [decanter]
- Bacina vino d.o.o. · Dolina Barrique XVII 2017 — 85 [decanter]
- PIK OPLENAC · Constanta Muse Sauvignon blanc 2019 — 85 [decanter]
- AE projekt centar · Carski Drum Chardonnay 2019 — 85 [decanter]
- Vinarija Podrum Danguba · Ima Noći Merlot 2015 — 85 [decanter]
- Virtus · W Credo Beli 2018 — 85 [decanter]
- Kuća Vina Jokić · Traminac 2018 — 85 [decanter]
- Château Prince · Rose 2021 — 85 [biwc]
- Vinarija Ilić-Nijemčević · Frankovka 2020 — 85 [biwc]
- Vinarija Komazec · Chardonnay 2021 — 85 [biwc]
- Vinarija Mrdjanin · Cabernet Sauvignon 2020 — 85 [biwc]
- Vinarija Mrdjanin · Sila 2022 — 85 [biwc]
- Vinarija VRT · PESAK SIVI 2022 — 85 [biwc]
- Podrum Pevac · GUŠT 2023 — 85 [biwc]
- Château Prince · Charm 2023 — 85 [biwc]
- Vinarija 100 Žena · Tamjanika 2023 — 85 [biwc]
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
- Bacina vino d.o.o. · Dolina Rizling 2023 — 85 [awc-vienna]
- Vinarija Ilić-Nijemčević · Cabernet Sauvignon 2018 — 85 [awc-vienna]
- Vinarium winery · Pinoranž 2019 — 85 [awc-vienna]
- Podrum Pevac · Red wine "ZAGRLJAJ" 2017 — 85 [awc-vienna]
- Fruškogorski · QUET Traminac 2018 — 85 [awc-vienna]
- Vista Hill · Selection White 2017 — 85 [awc-vienna]
- Vista Hill · Premium Rosé 2019 — 85 [awc-vienna]
- Vinarija KM · Rhine Riesling Ledeni 2016 — 85 [awc-vienna]
- Podrum Pevac · White Wine "Gust Chardonnay" 2017 — 85 [awc-vienna]
- Vinarija Komuna PR · Merlot 2018 — 85 [awc-vienna]
- Mikić · Traminer 2017 — 85 [awc-vienna]
- Winery ŠKRBIĆ · "CHICHA" Sauvignon Blanc 2017 — 85 [awc-vienna]
- Mikić · Merlot Barrique 2015 — 85 [awc-vienna]
- Pusula Winery · CHARDONNAY 2013 — 85 [awc-vienna]
- Vinis · Crveno Vino 2012 — 84 [decanter]
- Podrum Stari Hrast · Sauvignon Blanc 2017 — 84 [decanter]
- Fruškogorski · Quet Grašac 2017 — 84 [decanter]
- Vinarija Aven · Merlot 2017 — 84 [decanter]
- Vindulo d.o.o. · Mirna Bačka 2016 — 84 [decanter]
- Probus Vineyards · Gewürztraminer 2018 — 84 [decanter]
- Virtus · W Marselan 2017 — 84 [decanter]
- Vinis · Merlot 2015 — 84 [decanter]
- Adora · Cabernet Sauvignon 2016 — 84 [decanter]
- Драгић Винарија (Vina Dragic) · Carski Drum 2019 — 84 [decanter]
- Fruškogorski · Tri Sunca Traminac Kasna Berba 2015 — 84 [decanter]
- Vinarija Baza · Talični 2022 — 84 [biwc]
- Château Prince · Velika 2022 — 84 [biwc]
- Rajković wine office · Rajković Tamjanika 2023 — 84 [biwc]
- Vinarija Savic · Videlo Tamjanika 2022 — 84 [biwc]
- Podrum Pevac · Zagrljaj 2020 — 84 [biwc]
- Vinarija Milićević · rose 2022 — 84 [biwc]
- Vinarija Gnezdo · Roze 2024 — 84 [biwc]
- Vinarija Blagojević · Prokupac Barik 2023 — 84 [biwc]
- Vinarija Gnezdo · Roze 2025 — 84 [biwc]
- Vinarija Gnezdo · Kadarka 2024 — 84 [biwc]
- Fruškogorski · Quet Grašac 2020 — 84 [awc-vienna]
- Vinarija Sočanski · Classique Spiritoso Rizling Rajnski 2017 — 84 [awc-vienna]
- Mikić · Rosé 2017 — 84 [awc-vienna]
- Virtus · GEWURZTRAMINER 2017 — 84 [awc-vienna]
- Vinarija Podrum Danguba · "Ponovo naše" Tamjanika 2015 — 84 [awc-vienna]
- Pusula Winery · TRAMINAC 2013 — 84 [awc-vienna]
- Virtus · Marselan 2014 — 83 [decanter]
- Tody · Doja Belo 2014 — 83 [decanter]
- Quet · 13/15 Merlot  — 83 [decanter]
- Virtus · W Gewurztraminer 2019 — 83 [decanter]
- Château Prince · Morava M 2022 — 83 [biwc]
- Podrum Pevac · IZAZOV 2022 — 83 [biwc]
- Podrum Pevac · Prokupac Penusavo vino 2022 — 83 [biwc]
- Milanov Podrum · Lutka 2022 — 83 [biwc]
- PR Anjino Vino · Zora 2022 — 83 [biwc]
- Vinarija Unikat · Cabernet Sauvignon 2020 — 83 [biwc]
- Podrum Pevac · GUŠT (Barik) 2022 — 83 [biwc]
- Vinarija Blagojević · Petit Arvin M 2022 — 83 [biwc]
- Vinarija Unikat · Šeret 2021 — 83 [biwc]
- Vinarija Blagojević · Probus M barik 2021 — 83 [biwc]
- Vinska Kuća Rajić · RAJIĆ CRNA TAMJANIKA 2024 — 83 [biwc]
- Podrum Pevac · Zagrljaj, Cabarnet Franc, Merlo and Cabarnet Sauvignon 2020 — 83 [biwc]
- Vinarija 100 Žena · Crna ovca 2023 — 83 [biwc]
- Vinarija Tasa · Sauvignon Blanc 2025 — 83 [biwc]
- Vinarija Komazec · Rose 2022 — 82 [biwc]
- Vinarija Unikat · Vranac 2019 — 82 [biwc]
- Podrum Pevac · Kaberne Fran 2024 — 82 [biwc]
- Vinarija Gnezdo · Crno 2023 — 82 [biwc]
- Langov Podrum · Lang Chardonnay 2025 — 82 [biwc]
- Vinarija Baza · Baza-proseko 2021 — 81 [biwc]
- Vinarija Gamanović · Cabernet Sauvignon 2020 — 81 [biwc]
- Lutak winery · Lutkovo Crno 2022 — 81 [biwc]
- Vinarija Teodos · Krokan 2021 — 81 [biwc]
- Vinarija Unikat · Šeret 2021 — 81 [biwc]
- Vinarium winery · Merlot 2020 — 81 [biwc]
- Podrum Pevac · IZAZOV 2023 — 81 [biwc]
- Vinarija Gnezdo · Muskat Krokan 2022 — 81 [biwc]
- PR Anjino Vino · Zora 2023 — 81 [biwc]
- Vinarija Milićević · VladaVina 2024 — 81 [biwc]
- Vinska Kuća Rajić · Rosé 2024 — 81 [biwc]
- Vinarija Gnezdo · Krokan 2024 — 81 [biwc]
