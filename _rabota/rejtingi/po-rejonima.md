# Рејоны и виногорја

Настоящее место каждого хозяйства — по действующей сербской рејонизацији,
а не по главам книги.

**Зачем отдельно от книги.** Книга делит Сербию на десять глав; официальное
деление — три региона, 22 рејона, 77 виногорја. Это разные сетки, и совпадать
они не обязаны: одна глава книги может покрывать три рејона, а целые рејоны
в книгу не попасть вовсе. Пока рейтинги были разложены только по главам,
проверить это было нечем — теперь есть чем.

## Это виноградарские единицы, а не административные

Проверено, потому что вопрос законный: у пяти рејонов имя совпадает
с именем управног округа, и легко решить, что это одно и то же.

Не одно. Границы у них разные, а в одном случае они вовсе не пересекаются:

| Имя | Общины рејона, которых нет в округе | Общины округа, которых нет в рејоне |
|---|---|---|
| **Нишавски** | Пирот, Бела Паланка, Димитровград, Бабушница | Ниш, Алексинац, Сврљиг, Мерошина, Дољевац, Гаџин Хан, Ражањ |
| Сремски | Бачка Паланка, Беочин, Нови Сад, Сремски Карловци | Пећинци |
| Шумадијски | Смедеревска Паланка, Велика Плана | — |
| Топлички | Дољевац, Мерошина | Куршумлија |
| Јужнобанатски | — | Ковачица, Опово, Панчево, Пландиште |

Нишавски рејон и Нишавски округ не делят ни одной общины: рејон — это
пиротская сторона, округ — нишка. Совпадает только слово.

В таблице хозяйств стоят три виноградарские величины и одна географическая:
**регион**, **рејон** и **виногорје** — по рејонизацији, и **город** —
населённый пункт, куда ехать. Округ в таблицу не выводится вовсе: он
служебный, по нему только ищется рејон и отсекаются чужие.

## Откуда берётся

| Источник | Что даёт | Хозяйств |
|---|---|---|
| **Винарски регистар** | официальный перечень производителей вина: насеље с почтовым индексом и округ | 530 записей, из них узнано 281 |
| **ivv.rs** | «Вина и винарије Србије»: место с округом — «Vinča, Topola - Oplenac, Šumadijski okrug» | 142 |
| **vinarijesrbije.rs** | справочник винарий: рејон, город, адрес | 129 |
| **Decanter** | `region` + `subRegion` у каждого вина — единственный источник, доходящий до виногорја | 997 записей |
| **Vivino, страница хозяйства** | адрес: улица, город, индекс — в листинге его нет | 83 из 433 |
| **Vivino, вино** | плоский `region`, до виногорја не доходит | 2786 вин |
| **Falstaff** | область в печатном списке | 116 позиций |
| **книга** | город хозяйства в `raion-hozyaistv.json` | 32 |

## Винарски регистар

Главный источник места. Министарство пољопривреде публикует «Преглед
произвођача вина» таблицей: регистрационный номер, вид лица, полное
название, округ и насеље с индексом. На 21 июля 2026 года — 530
производителей. Берётся `vzjat-registar.py`, сводится с нашими именами
`svesti-registar.py`.

Сводятся имена по значимым словам. Регистр пишет юридическое имя —
«Milan Aleksić PR, proizvodnja vina i agro saveti “FITOMEDIK” Venčac», —
а Vivino и Decanter знают марку: «Fitomedik». Служебные слова («винарија»,
«подрум», «д.о.о.», «пр», «производња вина») ничего не различают и
отбрасываются; остальное ищется внутри записи регистра.

Три ограничения, и все три существенные:

**Насеље регистра — адрес юридического лица, а не виноградника.**
У восемнадцати хозяйств он городской, столичный: «Beograd — Врачар»,
«Нови Београд», «Земун». Виноградника там нет, это контора. Такие
записи местом не считаются вовсе.

**Одна запись регистра — одно хозяйство.** Если на неё притязают двое,
место не ставится ни одному: либо это одно хозяйство под двумя именами,
и тогда его сводят руками с доказательством, либо совпадение ложное.
«Manufaktura Spasić» садится на единственного в регистре Спасића из Жупы,
хотя делает сремску зеленику.

**Совпадение по одному слову проверяется глазами.** Оно и даёт ошибки:
«Vinarija Vrbica» совпала с «VINARIJA VELES VELIKA VRBICA» — не именем,
а селом в имени чужой записи. Отклонённые руками — в `OTKLONENO` внутри
`svesti-registar.py`, с разбором у каждого.

Имена источников переводятся в официальные таблицей в `sobrat-rejony.py`.
Таблица явная, и это не занудство: часть имён у Vivino и Decanter осталась
от **старой рејонизације**, где рејонов было девять. «Šumadija-Great Morava»
покрывает нынешние Шумадијски, Београдски, Млавски и Три Мораве; «Nišava-South
Morava» — пять рејонов сразу. По таким именам рејон не ставится, но
записывается регион и короткий список, в котором рејон точно есть.

## Округ у справочников — административный, не виноградарский

Это стоит держать в голове. Последнее слово в адресе у ivv.rs — всегда
**управни округ**: Шумадијски, Јужно-бачки, Расински. Их двадцать, и это
единицы государственного управления, а не виноградарские области; с
рејонима они не совпадают ни границами, ни числом. У vinarijesrbije.rs
наоборот: там названы именно рејоны, но их ярлыки местами ошибочны — тот
же Vino Budimir у них в Сремском рејону при адресе в Александровцу.

Поэтому ни один ярлык источника не берётся как рејон напрямую. Округ
работает двояко. Как **вместилище**: если все общины округа лежат в одном
рејоне, рејон известен. Так получается у 14 округов из 23; по остальным —
Зајечарски делится между Књажевачким и Нишким, Јужно-бачки между четырьмя
рејонима — по округу не ставится ничего. И как **отсечка**: названный
округ отбрасывает чужие рејоны, даже когда сам однозначного ответа не
даёт. «Rajac, Borski okrug» — Рајац есть и в Јеличком виногорју под
Чачком, но Борски округ это Неготинска Крајина, и чачанский Рајац
отпадает. Без этого Vinarija Raj уезжала под Чачак.

На одном округе держатся двенадцать хозяйств: Matalj, Milanović,
Petković Latin, Porodična Vinarija Stanimirović, Probus Vineyards,
Radovan, Varina, Vinarija Eden, Vinarija Lalić, Vinarija Mihailović,
Vinarija Timacvm Minvs, Vinarija Tomić - Rošci. Все остальные опираются
на общину или село.

## Место ищется по уровням достоверности

Имена мест по Сербии повторяются, и уровень решает всё. «Aleksandrovac» —
община Рејона Три Мораве и одновременно кадастровое село ещё в четырёх
виногорјима по стране; «Topola» — община Шумадијског рејона и село
Јагодинског виногорја. Пока обе карты были свалены в одну, девять жупских
винарий оставались без рејона, а Александровић уезжал из Шумадије.

Порядок такой, от точного к общему:

1. **названное виногорје** — если в поле прямо стоит «Levačko vinogorje»;
2. **община рејона** — административная единица, её и имеют в виду справочники;
3. **кадастровая община виногорја** — село, 2162 имени;
4. **округ** — годится только тот, что целиком лежит в одном рејоне. Таких
   14 из 23; Зајечарски, например, делится между Књажевачким и Нишким, и по
   нему ставить нечего. Округ выводится не по выборке, а по официальным
   спискам: община → округ, община → рејон;
5. **город из чужого справочника** — последним.

Рејон находится первым, виногорје ищется уже внутри него.

Кадастровые имена пришлось разбирать отдельно. В официальном тексте они
перечислены не списком, а прозой: «Северни део: делови катастарских
општина Речка, Мокрање, …, Рајац. Јужни део: делови катастарских општина
Браћевац, …». При разборе по запятым такая фраза целиком становилась одним
«именем», и место терялось — так из карты выпал Рајац, то самое село
роглевачко-рајачких пивниц. Слипшихся строк 58 из 2162; они разбираются
обратно в `imena_kadastra`.

## У источников места разный вес

Каталог пишет, где хозяйство стоит; регистр — где оно зарегистрировано.
Это разные вещи, и спорить им незачем: у Амбелоса ivv.rs даёт Велику
Плану, а регистр — Пожаревац, потому что контора в городе, а виноградник
за ним. Поэтому места разбираются по старшинству, и слабый источник не
спорит с сильным, а молчит при нём:

1. **город из книги** — данные автора;
2. **ivv.rs и vinarijesrbije.rs** — каталоги винарий: они описывают, где
   хозяйство стоит;
3. **Винарски регистар** — официально, но это юридический адрес;
4. **ярлык источника** — рејон, названный Vivino, Decanter или Falstaff;
5. **адрес со страницы Vivino** — последним. Его вписывает тот, кто занял
   страницу, и это часто контора: у Fleur d'Oranger там Нови Сад, а
   Decanter относит вина к северу Баната.

Спор внутри одного веса рејон не ставит: у Urošević ivv.rs пишет Баноштор
на Фрушкој гори, а vinarijesrbije — Књажевац, и выбирать тут не из чего.

## Как решается спор внутри одного веса

1. **Место старше ярлыка источника.** Справочник vinarijesrbije пишет
   Vino Budimir в Сремски рејон, а адресом даёт Александровац — то есть Жупу;
   он же держит Vinarija Čoka в Суботичком, хотя Чока — община Потиског
   рејона. Ярлык у них ошибочный, адрес — нет.
2. **Если спорят сами города** — рејон не ставится. У Urošević ivv.rs пишет
   Баноштор на Фрушкој гори, а vinarijesrbije — Књажевац; это разные концы
   страны, и выбирать тут не из чего.
3. **Подавляющее большинство.** Восемьдесят семь записей за Сремски рејон
   против одной за Суботички — опечатка у источника, а не второе место работы
   хозяйства. Порог — вчетверо.
4. **Иначе рејон не ставится**, а расхождение пишется в `rejon_raznoglasie`.

Виногорје из чужого рејона отбрасывается: у Savić рејон вышел Нишавски по
четырём записям, а виногорје — Опленачко по одной, и второе неверно.

## Чего делать нельзя

**Выводить место из имени хозяйства.** Проверено: даёт тринадцать ответов,
из них верных два. «Подрум Вина Тодор» садится в село Вина Књажевачког
рејона, потому что «вина» — родительный падеж слова «вино»; «Weingut Jović» —
в Мališevsko виногорје по фамилии; «Манастир Студеница» — в Метохију.

**Сводить хозяйства по похожести имён.** Тоже проверено: Jovanović и Jovanov,
Madžić и Adžić, Stojković и Stojanović, Radlović и Aranđelović — разные
хозяйства. Свёденные имена лежат в `sinonimy-hozyaistv.json`, и у каждого
записано доказательство.

## Одно хозяйство под пятью именами

По ходу вскрылось, что часть строк в таблице — не разные хозяйства,
а одно и то же под разными написаниями. Три корня:

**«dj» вместо «đ».** Decanter пишет «Mrdjanin», «Djurdjic», «Medje» там,
где у Vivino стоит «Mrđanin», «Đurđić», «Međe». Ключ теперь считает их
одной буквой — три слияния, ложных нет.

**Служебные слова.** «Vino Budimir» и «Budimir», «Krstašica Doo» и
«Krstašica», «Podrum Vina Žarković» и «Žarković», «Pr Anjino Vino» и
«Anjino Vino» — одни и те же дома. Слова «вино», «вина», «д.о.о.», «пр»,
«vineyards», «wines» ничего не различают и отброшены — одиннадцать
слияний, ложных нет.

**Кириллица через тире.** «Орлић Породична Винарија - Orlić Family
Winery» — одно имя дважды, как и «X (Y)» в скобках. Разбирается так же.

**Разные алфавиты целиком.** «Podrum Pevac» у Decanter и «Подрум Певац»
у Vivino — одно хозяйство, и линейка совпадает вином в вино: Гушт, Гушт
Шардоне Барик, Прокупац, Тишина Малвазийа, Загрљај. Такая пара в таблице
оказалась одна: «Vinarija Milojević» и «Подрум Милојевић» на неё похожи,
но это разные дома — в регистре Милојевића два, один в Зеокама под
Лазаревцем, другой в Остриковцу под Јагодином, и линейки у них разные.

**Регистр как судья.** Он и вскрыл остальные повторы: если два имени
из таблицы садятся на одну и ту же запись Винарског регистра, это повод
проверить каждое. Так нашлись и сведены пять пар: Aglaya (Аглая) и
Vinarija Frunza Aglaja (в регистре Аглаја одна на всю Сербию),
Spasić и Vinarska Kuća Spasić (Тржац у Александровцу, обе делают
тамјанику), Radenković и WinEco (общее вино «Carigrad Barrique»),
Radovan и Čokot (книга сама пишет «бывш. Čokot»), Veritas и Veritas
Ćuković (общие «Bela Hormonya», «Momentum», «Cuvée Suvo»).

Ещё четыре пары регистр свёл ложно — по слову внутри чужого имени: Gora
и La Gora (слово «gora» из «Fruška Gora»), Moravski Val и Val d'Ov,
Perun Wine и Plavi Perun, Manufaktura Spasić и жупский Спасић. Они
помечены в `ne_odno_i_to_zhe` и оставлены порознь.

Остальное сведено руками, по одному, с доказательством — в
`sinonimy-hozyaistv.json`. Всего строк стало 437 вместо 472.

## Три строки, которые вообще не хозяйства

У Decanter в поле производителя иногда стоит название сорта:

- **Belina**, DWWA 2021 — то же вино урожаев 2020–2022 подано за
  Matijašević, и других «Belina» на конкурсе нет. Привязано.
- **Chardonnay**, DWWA 2026 — вино «Omnibus Lector Chardonnay», а это
  линейка Erdevik. Привязано.
- **Marselan** (DWWA 2023) и **Prokupac** (DWWA 2021) — привязать не
  к кому: эти сорта делают десятки хозяйств. Строки остались как есть,
  с пометкой в `sinonimy-hozyaistv.json`.

Отдельно: **Mihajlovacko** — не хозяйство, а обломок разбора у Vivino.
За именем стоит одна запись «Codrum Vina Dajit Gamay Kvalitetno Suvo
Crveno»: это текст с этикетки, попавший в поле имени.

## Хозяйства без рејона существуют — проверено живьём

Разумное сомнение: не выдумка ли те, у кого рејон не установлен. Проверено
28 августа 2026 года, тогда таких было 214; после Винарског регистра
осталось 139, но проверка касалась всех.

**204 из них** пришли из листинга хозяйств Vivino — у каждого свой номер
и адрес в скачанных страницах. Все 204 адреса открыты сейчас: **HTTP 200
у всех, имя на странице совпало у всех 204**. Построчный итог — в
`proverka-vivino.json`.

**Остальные десять** в листинге Vivino не значатся, но каждое прослежено
до записи с номером, а четыре открыты живьём:

- **Lakićević** — на Vivino есть, но не в сербском листинге:
  `vinarija-lakicevic`, HTTP 200. Вина 8890518, 8920751, 11593426.
- **Vinarija Val d'Ov** (вино 13984418) и **Walc & Grozd** (9794815) —
  обе страницы открылись, имена совпали.
- **Vinarija Fleur D'Oranger** — вино 11386572 на Vivino плюс две записи
  Decanter; API конкурса и сейчас отдаёт «Krokan Muskat 2024» за ним.
- **Gardijan**, **Vinarija Mira**, **Rubinov** — записи DWWA 2026, 2025
  и 2021 с номерами 786344, 769318, 697216.
- **Josic Winery** — печатный список Falstaff, «Zmajevac Prokupac» и
  «Zmajevac Tamjanika» по 92 балла. Zmajevac — марка Josić.
- **Marselan** и **Prokupac** — не хозяйства, а разобранная выше ошибка
  ввода у Decanter.

Отдельно проверено, не затесались ли иностранцы. Тринадцать вин в сборе
Vivino помечены несербской страной, но **ни одно хозяйство не иностранное
целиком** — это отдельные позиции, которые Vivino отнёс к другой стране:
у Imperator Vino два вина из Косова из двадцати семи, у Vinski Dvor два
из пятнадцати, у Ralević одно из тринадцати.

## Сбор Vivino полон — проверено дважды

**Счётчиком самого Vivino.** У каждой страницы хозяйства есть свой счётчик
вин. По 408 ключам из 424 он сходится с нашим сбором точно. Расхождение —
11 вин у восьми хозяйств, и это не потеря разбора: у Milinčić счётчик пишет
три вина, страница не показывает ни одного, а API отдаёт пустой список.
Ещё у восьми ключей вин на одно больше, чем говорит счётчик, — счётчик
отстаёт.

**Листингом.** Он перекачан заново: те же 433 хозяйства, ни одного нового,
ни одного пропавшего; девятнадцатая страница пуста. Но в карточке страны
Vivino пишет, что винарий у него 455.

**Разницу закрыли поиском.** По 199 производителям из Винарског регистра,
которых в наших таблицах нет, сделан поиск по хозяйствам Vivino; 235
найденных страниц открыты и проверены по стране в адресе. Сербских среди
них четыре — Vina Đurđević, Vinarija Župančić, Vinogradi Urošević, Župski
Podrum, — и **у всех четырёх ноль вин и ноль отзывов**. Разница между 433
и 455 сложена из таких пустых страниц; собирать там нечего. Построчно —
в `poisk-vivino.json`.

## Как проверить глазами

Хозяйство на Vivino открывается по слагу:
`https://www.vivino.com/wineries/<слаг>` — слаг лежит в поле
`vivino_slug` таблицы хозяйств. Награда Decanter — по номеру вина из
поля `stranica`: `https://awards.decanter.com/DWWA/<год>/wines/<номер>`.
Карточка ivv.rs — `https://www.ivv.rs/vinarija/<слаг>/`.

Адрес хозяйства со страницы Vivino лежит в
`kesh-vivino-adresa/<слаг>.json`, запись Винарског регистра — в
`vinarski-registar.json`, а с чем она свелась — в `registar-hozyaistv.json`.

**Пересобрать файл:**

    python3 _rabota/rejtingi/vzjat-registar.py        # раз в сезон: реестр обновляется
    python3 _rabota/rejtingi/vzjat-adresa-vivino.py   # уже скачанное не перекачивает
    python3 _rabota/rejtingi/svesti-registar.py
    python3 _rabota/rejtingi/sobrat-rejony.py
    python3 _rabota/rejtingi/sobrat-tablicy.py
    python3 _rabota/rejtingi/svesti-rejony.py --otchet

<!-- Собрано скриптом svesti-rejony.py. Руками не править. -->

## Что собралось по рејонима

Хозяйства разложены по действующей рејонизацији: 3 региона, 22 рејона, 77 виногорја. Глава книги — отдельный столбец, она не обязана совпадать.

| Регион | Рејон | Хозяйств | Оценок Vivino | Оценок критиков | Наград |
|---|---|---|---|---|---|
| Vojvodina | Rejon Bačka | 6 | 0 | 5 | 9 |
| Vojvodina | Banatski rejon | 2 | 0 | 15 | 16 |
| Centralna Srbija | Beogradski rejon | 16 | 35 | 70 | 106 |
| Centralna Srbija | Čačansko–kraljevački rejon | 4 | 1 | 3 | 3 |
| Vojvodina | Južnobanatski rejon | 16 | 31 | 53 | 81 |
| Kosovo i Metohija | Južnometohijski rejon | 1 | 2 | 0 | 0 |
| Centralna Srbija | Knjaževački rejon | 4 | 22 | 30 | 60 |
| Centralna Srbija | Leskovački rejon | 5 | 3 | 1 | 1 |
| Centralna Srbija | Mlavski rejon | 6 | 14 | 96 | 101 |
| Centralna Srbija | Nišavski rejon | 1 | 2 | 3 | 3 |
| Centralna Srbija | Niški rejon | 6 | 14 | 13 | 17 |
| Centralna Srbija | Pocersko Valjevski Rejon | 7 | 24 | 19 | 30 |
| Vojvodina | Potiski rejon | 2 | 19 | 9 | 15 |
| Centralna Srbija | Rejon Negotinska Krajina | 22 | 56 | 119 | 154 |
| Vojvodina | Rejon Telečka | 3 | 2 | 2 | 2 |
| Centralna Srbija | Rejon Tri Morave | 78 | 227 | 339 | 468 |
| Vojvodina | Sremski rejon | 88 | 338 | 662 | 934 |
| Vojvodina | Subotički rejon | 18 | 94 | 148 | 199 |
| Centralna Srbija | Šumadijski rejon | 33 | 167 | 291 | 423 |
| Centralna Srbija | Toplički rejon | 5 | 22 | 67 | 95 |
| Centralna Srbija | Vranjski rejon | 3 | 24 | 56 | 83 |
| — | **рејон не установлен** | 132 | 83 | 96 | 137 |

**Рејоны, из которых не собралось ни одного хозяйства:** Severnometohijski rejon.


## Главы книги и рејоны

Столбец слева — глава книги, справа — в какие рејоны попадают её хозяйства по действующей рејонизацији.

| Глава книги | Рејоны её хозяйств |
|---|---|
| Фрушка гора | Sremski rejon — 27 |
| Суботичко-Хоргошская пешчара | Subotički rejon — 4 |
| Банат | Južnobanatski rejon — 4; Potiski rejon — 1 |
| Шумадия | Šumadijski rejon — 9; Rejon Tri Morave — 1 |
| Три Моравы и Жупа | Rejon Tri Morave — 16; Šumadijski rejon — 1 |
| Неготинска Крайина | Rejon Negotinska Krajina — 5 |
| Топлица | Toplički rejon — 3 |
| Юго-восток | Knjaževački rejon — 2; Vranjski rejon — 1; Niški rejon — 1 |
| Подунавье и Белградский район | Beogradski rejon — 4 |
| Косово и Метохия | не установлен — 1 |

**Рејоны, где хозяйства есть, а в книге их нет:**

- **Rejon Bačka** (Vojvodina) — 117 Wine, Fekete, Sila, Vinarija Baza, Vinarija Ždrnja, Vindulo d.o.o.
- **Banatski rejon** (Vojvodina) — Kepul, Vinarija Gnezdo
- **Čačansko–kraljevački rejon** (Centralna Srbija) — Vinarija S. Milošević, Vinarija Tomić - Rošci, Vinarija Čolaković, Винарија Ступови (Vinarija Stupovi)
- **Južnometohijski rejon** (Kosovo i Metohija) — Monastery Visoki Decani  (Манастирско Дечанско)
- **Leskovački rejon** (Centralna Srbija) — Hrusija d.o.o. Leskovac, Prima, Vinarija Aquila, Козарак, Митровиђ Винарија
- **Mlavski rejon** (Centralna Srbija) — Kuća Vina Popović, Pruna, VINARIJA STANKOVIĆ, Vinarija Necak, Vinarija Unikat, Virtus
- **Nišavski rejon** (Centralna Srbija) — Vinarija Savic
- **Pocersko Valjevski Rejon** (Centralna Srbija) — Andrića Vinograd, Karić Vinarija, Milijan Jelić, Podrum Lukic, Puce, Pusula Winery, Vinarija Đurđevića Legat
- **Rejon Telečka** (Vojvodina) — Dimalis, Enellion, Milisavljević

## Виногорја внутри рејонов

Официальных виногорја 77. Пустое виногорје — не ошибка: хозяйство может быть, но без установленного места.

| Рејон | Виногорје | Хозяйств |
|---|---|---|
| Rejon Bačka | *виногорје не установлено* | 6 |
| Banatski rejon | Kikindsko vinogorje | 1 |
| Banatski rejon | Srednjebanatsko vinogorje | — |
| Banatski rejon | *виногорје не установлено* | 1 |
| Beogradski rejon | Avalsko-kosmajsko vinogorje | 2 |
| Beogradski rejon | Gročansko vinogorje | 3 |
| Beogradski rejon | Smederevsko vinogorje | 4 |
| Beogradski rejon | Dubonsko vinogorje | — |
| Beogradski rejon | Lazarevačko vinogorje | 3 |
| Beogradski rejon | *виногорје не установлено* | 4 |
| Čačansko–kraljevački rejon | Ljubićko vinogorje | 1 |
| Čačansko–kraljevački rejon | Jeličko vinogorje | 1 |
| Čačansko–kraljevački rejon | Ibarsko vinogorje | — |
| Čačansko–kraljevački rejon | *виногорје не установлено* | 2 |
| Južnobanatski rejon | Vršačko vinogorje | 10 |
| Južnobanatski rejon | Belocrkvansko vinogorje | — |
| Južnobanatski rejon | Vinogorje Deliblatske peščare | 2 |
| Južnobanatski rejon | *виногорје не установлено* | 4 |
| Južnometohijski rejon | Đakovačko vinogorje | — |
| Južnometohijski rejon | Orahovačko vinogorje | 1 |
| Južnometohijski rejon | Prizrensko vinogorje | — |
| Južnometohijski rejon | Suvorečko vinogorje | — |
| Južnometohijski rejon | Mališevsko vinogorje | — |
| Knjaževački rejon | Borsko vinogorje | — |
| Knjaževački rejon | Boljevačko vinogorje | — |
| Knjaževački rejon | Zaječarsko vinogorje | 1 |
| Knjaževački rejon | Potrkanjsko vinogorje | 2 |
| Knjaževački rejon | *виногорје не установлено* | 1 |
| Leskovački rejon | Babičko vinogorje | — |
| Leskovački rejon | Pustorečko vinogorje | — |
| Leskovački rejon | Vinaračko vinogorje | 2 |
| Leskovački rejon | Vlasotinačko vinogorje | — |
| Leskovački rejon | *виногорје не установлено* | 3 |
| Mlavski rejon | Braničevsko vinogorje | 1 |
| Mlavski rejon | Požarevačko vinogorje | 4 |
| Mlavski rejon | Resavsko vinogorje | — |
| Mlavski rejon | *виногорје не установлено* | 1 |
| Nišavski rejon | Belopalanačko vinogorje | — |
| Nišavski rejon | Pirotsko vinogorje | — |
| Nišavski rejon | Babušničko vinogorje | — |
| Nišavski rejon | *виногорје не установлено* | 1 |
| Niški rejon | Sokobanjsko vinogorje | 1 |
| Niški rejon | Aleksinačko vinogorje | — |
| Niški rejon | Žitkovačko vinogorje | — |
| Niški rejon | Čegarsko vinogorje | 3 |
| Niški rejon | Kutinsko vinogorje | — |
| Niški rejon | Svrljiško vinogorje | 1 |
| Niški rejon | *виногорје не установлено* | 1 |
| Pocersko Valjevski Rejon | Pocersko vinogorje | 1 |
| Pocersko Valjevski Rejon | Podgorsko vinogorje | 4 |
| Pocersko Valjevski Rejon | Kolubarsko-ljiško vinogorje | 1 |
| Pocersko Valjevski Rejon | *виногорје не установлено* | 1 |
| Potiski rejon | Severnopotisko vinogorje | 1 |
| Potiski rejon | Srednjepotisko vinogorje | 1 |
| Potiski rejon | Južnopotisko vinogorje | — |
| Rejon Negotinska Krajina | Ključko vinogorje | — |
| Rejon Negotinska Krajina | Brzopalanačko vinogorje | — |
| Rejon Negotinska Krajina | Mihajlovačko vinogorje | 1 |
| Rejon Negotinska Krajina | Negotinsko vinogorje | 6 |
| Rejon Negotinska Krajina | Rogljevačko-rajačko vinogorje | 7 |
| Rejon Negotinska Krajina | *виногорје не установлено* | 8 |
| Rejon Telečka | Zapadnotelečko vinogorje | 2 |
| Rejon Telečka | Centralnotelečko vinogorje | 1 |
| Rejon Telečka | Istočnotelečko vinogorje | — |
| Rejon Tri Morave | Paraćinsko vinogorje | 4 |
| Rejon Tri Morave | Jagodinsko vinogorje | 7 |
| Rejon Tri Morave | Jovačko vinogorje | — |
| Rejon Tri Morave | Levačko vinogorje | 7 |
| Rejon Tri Morave | Temnićko vinogorje | 1 |
| Rejon Tri Morave | Trsteničko vinogorje | 5 |
| Rejon Tri Morave | Kruševačko vinogorje | 5 |
| Rejon Tri Morave | Župsko vinogorje | 37 |
| Rejon Tri Morave | Ražanjsko vinogorje | — |
| Rejon Tri Morave | *виногорје не установлено* | 12 |
| Sremski rejon | Fruškogorsko vinogorje | 88 |
| Subotički rejon | Riđičko vinogorje | 5 |
| Subotički rejon | Palićko vinogorje | 6 |
| Subotički rejon | Horgoško vinogorje | 1 |
| Subotički rejon | *виногорје не установлено* | 6 |
| Šumadijski rejon | Krnjevačko vinogorje | 3 |
| Šumadijski rejon | Oplenačko vinogorje | 22 |
| Šumadijski rejon | Račansko vinogorje | 1 |
| Šumadijski rejon | Kragujevačko vinogorje | 3 |
| Šumadijski rejon | *виногорје не установлено* | 4 |
| Toplički rejon | Prokupačko vinogorje | 3 |
| Toplički rejon | Jugbogdanovačko vinogorje | — |
| Toplički rejon | Žitorađsko vinogorje | — |
| Toplički rejon | *виногорје не установлено* | 2 |
| Vranjski rejon | Surduličko vinogorje | — |
| Vranjski rejon | Vrtogoško vinogorje | 3 |
| Vranjski rejon | Buštranjsko vinogorje | — |

## Хозяйства по рејонима

Город — куда ехать. Это населённый пункт хозяйства, а не округ: округ единица государственного управления, к виноградарству отношения не имеет.


### Rejon Bačka — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| 117 Wine | — | — | vivino | — |
| Fekete | — | — | vivino | — |
| Sila | — | — | vivino | — |
| Vinarija Baza | — | — | vivino | — |
| Vinarija Ždrnja | — | Temerin | mesto | — |
| Vindulo d.o.o. | — | Temerin | mesto | — |

### Banatski rejon — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Kepul | Kikindsko vinogorje | Iđoš | mesto | — |
| Vinarija Gnezdo | — | Bečej | konkurs | — |

### Beogradski rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Janko | Smederevsko vinogorje | Smederevo | mesto | Подунавье и Белградский район |
| Janovi Vinogradi | Avalsko-kosmajsko vinogorje | Sopot | mesto | — |
| Plavinac | Smederevsko vinogorje | Smederevo | mesto | Подунавье и Белградский район |
| Plavinci | Gročansko vinogorje | Zaklopača | mesto | — |
| Vinarija Jeremić | Smederevsko vinogorje | Smederevo | mesto | — |
| Vinarija Milićević | Avalsko-kosmajsko vinogorje | Sopot | mesto | — |
| Vinarija Milojević | Lazarevačko vinogorje | Lazarevac | mesto | — |
| Vinarija Panjković | Smederevsko vinogorje | Smederevo | mesto | — |
| Vinarija Pantić | — | Mladenovac | mesto | — |
| Vinarija Vojinović | — | Mladenovac | mesto | — |
| Vinarija Zorča | Lazarevačko vinogorje | Lazarevac | mesto | — |
| Винарија Тришић (Vinarija Trišić) | — | Vranić | decanter+vinarijesrbije | Подунавье и Белградский район |
| Виногради Гроцка (Vinogradi Grocka) | Gročansko vinogorje | Гроцка | mesto | Подунавье и Белградский район |
| Краљвеска Винарија (Royal Winery) | Gročansko vinogorje | Grocka | mesto | — |
| Подрум Милојевић | Lazarevačko vinogorje | Zeoke | mesto | — |
| Фенек (Fenek Monastery) | — | Beograd | mesto | — |

### Čačansko–kraljevački rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Vinarija S. Milošević | Jeličko vinogorje | Riđage | mesto | — |
| Vinarija Tomić - Rošci | — | — | mesto | — |
| Vinarija Čolaković | Ljubićko vinogorje | Miločaj | mesto | — |
| Винарија Ступови (Vinarija Stupovi) | — | — | vinarijesrbije | — |

### Južnobanatski rejon — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Bahus | Vršačko vinogorje | Gudurica | mesto | — |
| Galot | Vinogorje Deliblatske peščare | Banatski Karlovac | mesto | Банат |
| Porodična Vinarija Stanimirović | — | — | mesto | — |
| Rnjak | Vršačko vinogorje | Gudurica | mesto | Банат |
| Soul Wine | Vršačko vinogorje | Vršac | mesto | — |
| Vinarija Aleksandar | — | — | vinarijesrbije | — |
| Vinarija Drašković | Vršačko vinogorje | Вршац | mesto | Банат |
| Vinarija Lalić | — | — | mesto | — |
| Vinarija Nedin | Vršačko vinogorje | Gudurica | mesto | — |
| Vinarija Selecta | Vršačko vinogorje | Gudurica | mesto | — |
| Vinarija Sočanski | Vršačko vinogorje | Veliko Središte | mesto | — |
| Vinarija ĐORĐE | Vinogorje Deliblatske peščare | Banatski Karlovac | mesto | — |
| Vinik | Vršačko vinogorje | Vršac | mesto | — |
| Vinska Kuća Rajić | — | — | mesto | — |
| Vršački Vinogradi | Vršačko vinogorje | Вршац | mesto | Банат |
| Орлић Породична Винарија - Orlić Family Winery | Vršačko vinogorje | Vršac | vivino-adres | — |

### Južnometohijski rejon — Kosovo i Metohija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Monastery Visoki Decani  (Манастирско Дечанско) | Orahovačko vinogorje | Velika Hoča | mesto | — |

### Knjaževački rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Dzervin | Potrkanjsko vinogorje | Knjaževac | mesto | Юго-восток |
| Jović | Potrkanjsko vinogorje | Потркање | mesto | Юго-восток |
| Nikolas | Zaječarsko vinogorje | Zvezdan | mesto | — |
| Vinarija Todorović | — | — | bolshinstvo | — |

### Leskovački rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Hrusija d.o.o. Leskovac | Vinaračko vinogorje | Leskovac | mesto | — |
| Prima | — | Donja Lokošnica | mesto | — |
| Vinarija Aquila | Vinaračko vinogorje | Leskovac | mesto | — |
| Козарак | — | — | vivino | — |
| Митровиђ Винарија | — | — | vivino | — |

### Mlavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Kuća Vina Popović | Požarevačko vinogorje | Krvije | mesto | — |
| Pruna | — | Vuković | mesto | — |
| VINARIJA STANKOVIĆ | Braničevsko vinogorje | Rabrovo | mesto | — |
| Vinarija Necak | Požarevačko vinogorje | Petrovac | mesto | — |
| Vinarija Unikat | Požarevačko vinogorje | Požarevac | mesto | — |
| Virtus | Požarevačko vinogorje | Žabari | mesto | — |

### Nišavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Vinarija Savic | — | — | bolshinstvo | — |

### Niški rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Podrum Ljubisavljević | Sokobanjsko vinogorje | Sokobanja | mesto | — |
| Podrum Malča | Čegarsko vinogorje | Малча | mesto | Юго-восток |
| Status | Svrljiško vinogorje | Svrljig | mesto | — |
| Vinarija 100 Žena | Čegarsko vinogorje | Vele Polje | mesto | — |
| Виница Грковић (Vinica Grković) | — | — | vivino | — |
| Изба Јовановић (Izba Jovanovic) | Čegarsko vinogorje | Vele Polje | mesto | — |

### Pocersko Valjevski Rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Andrića Vinograd | — | — | vivino | — |
| Karić Vinarija | Pocersko vinogorje | Varna | mesto | — |
| Milijan Jelić | Podgorsko vinogorje | Valjevo | mesto | — |
| Podrum Lukic | Kolubarsko-ljiško vinogorje | Babajić | mesto | — |
| Puce | Podgorsko vinogorje | Miličinica | mesto | — |
| Pusula Winery | Podgorsko vinogorje | Miličinica | mesto | — |
| Vinarija Đurđevića Legat | Podgorsko vinogorje | Ključ | mesto | — |

### Potiski rejon — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Vinarija Coka | Severnopotisko vinogorje | Чока | mesto | Банат |
| Vinartos Vinarija | Srednjepotisko vinogorje | Bečej | mesto | — |

### Rejon Negotinska Krajina — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Cubra | Negotinsko vinogorje | Negotin | mesto | — |
| Dalia | — | — | vivino | — |
| Francuska Vinarija - Estelle et Cyrille Bongiraud | Rogljevačko-rajačko vinogorje | Rogljevo | mesto | Неготинска Крайина |
| Manastir Bukovo | — | — | decanter+vivino | Неготинска Крайина |
| Matalj | — | — | mesto | Неготинска Крайина |
| Mikić | Rogljevačko-rajačko vinogorje | Rečka | mesto | — |
| Radu Group Vinarija | Rogljevačko-rajačko vinogorje | Crnomasnica | mesto | — |
| Raj | Negotinsko vinogorje | Negotin | mesto | Неготинска Крайина |
| Tenuta Est Winery | Negotinsko vinogorje | Negotin | mesto | — |
| Traško Vinarija | Negotinsko vinogorje | Negotin | mesto | — |
| Vimmid | Negotinsko vinogorje | Negotin | mesto | Неготинска Крайина |
| Vinarija Boierescu | Negotinsko vinogorje | Negotin | mesto | — |
| Vinarija Dajic | Mihajlovačko vinogorje | Mihajlovac | mesto | — |
| Vinarija Gamanović | — | Kladovo | decanter+vivino | — |
| Vinarija Janucic | Rogljevačko-rajačko vinogorje | Veljkovo | mesto | — |
| Vinarija Novak (Новак) | — | — | vivino | — |
| Vinarija Porta | — | — | vivino | — |
| Vinarija Tana | Rogljevačko-rajačko vinogorje | Tamnič | mesto | — |
| Vinarija Timacvm Minvs | — | Bor | mesto | — |
| Vinarija Timahus | — | — | vivino | — |
| Vinski Podrum Mirjana | Rogljevačko-rajačko vinogorje | Rogljevo | mesto | — |
| Винарија Королија | Rogljevačko-rajačko vinogorje | Tamnič | mesto | — |

### Rejon Telečka — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Dimalis | Centralnotelečko vinogorje | Stara Moravica | mesto | — |
| Enellion | Zapadnotelečko vinogorje | Vrbas | vivino-adres | — |
| Milisavljević | Zapadnotelečko vinogorje | Kula | mesto | — |

### Rejon Tri Morave — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Adora | Jagodinsko vinogorje | Jagodina | mesto | — |
| Aleksandar Todorović | — | — | vivino | — |
| Bacina vino d.o.o. | Temnićko vinogorje | Varvarin | mesto | — |
| Botunjac | Župsko vinogorje | Aleksandrovac | mesto | — |
| Braća Rajković | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Budimir | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Cilić | — | Lozovik | vivino | Три Моравы и Жупа |
| Cvetković Vinarija | — | — | mesto | — |
| Damjanovic | Župsko vinogorje | Garevina | mesto | — |
| Fragaria | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Grabak | Kruševačko vinogorje | Vrnjačka Banja | mesto | — |
| Ivanović | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Kalem | Trsteničko vinogorje | Velika Drenova | mesto | — |
| Lastar | Levačko vinogorje | Rekovac | mesto | Три Моравы и Жупа |
| Marko | Trsteničko vinogorje | Ясиковица | mesto | Шумадия |
| Milan Nikolić | Jagodinsko vinogorje | — | decanter | — |
| Milanov Podrum | Župsko vinogorje | Aleksandrovac | mesto | — |
| Milić | Župsko vinogorje | Aleksandrovac | vivino-adres | — |
| Podrum Dremina | Paraćinsko vinogorje | Drenovac | mesto | — |
| Podrum Pevac | Jagodinsko vinogorje | Kragujevac | konkurs | — |
| Podrum Tošići | Župsko vinogorje | Aleksandrovac | mesto | — |
| Radosavljevic | Kruševačko vinogorje | Kruševac | mesto | — |
| Radovan | Kruševačko vinogorje | — | mesto | Три Моравы и Жупа |
| Rajković wine office | Župsko vinogorje | Novaci | mesto | — |
| Rakicevic | Župsko vinogorje | Aleksandrovac | mesto | — |
| Ralević | Paraćinsko vinogorje | Парачин | mesto | Три Моравы и Жупа |
| Rubin | Kruševačko vinogorje | Крушевац | mesto | Три Моравы и Жупа |
| Saboss | Župsko vinogorje | Aleksandrovac | mesto | — |
| Savković | Župsko vinogorje | Aleksandrovac | mesto | — |
| Spasić | Župsko vinogorje | Александровац | mesto | Три Моравы и Жупа |
| Stemina winery | Trsteničko vinogorje | Trstenik | mesto | — |
| Temet | Jagodinsko vinogorje | Jagodina | mesto | Три Моравы и Жупа |
| Uziwa Winery | — | Vrnjačka Banja | vivino-adres | — |
| Varina | — | — | mesto | — |
| Vert | — | — | vivino | — |
| Vertiz | Levačko vinogorje | — | mesto | — |
| Vila Vina | — | — | vivino | — |
| Vilimonovic | Trsteničko vinogorje | Medveđa | mesto | — |
| Vina Jelenković | Župsko vinogorje | Stubal | mesto | — |
| Vinarija A. Rajković | Župsko vinogorje | Gornja Zleginja | mesto | — |
| Vinarija Agatija | Levačko vinogorje | Rabenovac | mesto | — |
| Vinarija Bada | Župsko vinogorje | Aleksandrovac | mesto | — |
| Vinarija Bora | Levačko vinogorje | Lepojević | mesto | — |
| Vinarija Jovac | Jagodinsko vinogorje | Jovac | mesto | Три Моравы и Жупа |
| Vinarija Levač | Levačko vinogorje | Rekovac | mesto | — |
| Vinarija Milovanovic | Župsko vinogorje | Gornja Zleginja | mesto | — |
| Vinarija Mozaik Milan | — | — | vivino | — |
| Vinarija Pet Hrastova | — | Vrnjačka Banja | mesto | — |
| Vinarija Piano | Jagodinsko vinogorje | Jagodina | mesto | — |
| Vinarija Rajić | Paraćinsko vinogorje | Glavica | mesto | — |
| Vinarija Slatina | Župsko vinogorje | Lesenovci | mesto | — |
| Vinarija Smiljković 90 | Župsko vinogorje | Aleksandrovac | mesto | — |
| Vinarija Venčac | Jagodinsko vinogorje | — | decanter | — |
| Vinarija Ćosić | Župsko vinogorje | Aleksandrovac | mesto | — |
| Vinarska Kuća Miljković | — | — | mesto | — |
| Vinex Grozd | Levačko vinogorje | Belušić | mesto | — |
| Vinis | Paraćinsko vinogorje | Dobra Voda | mesto | — |
| Vinogradi i vinarija Miletić | Levačko vinogorje | Oparić | mesto | — |
| Vinska Kuća Milinčić | Župsko vinogorje | Aleksandrovac | mesto | — |
| Vinska Kuća Minića | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Vinska Kuća Rakićević | Župsko vinogorje | Velja Glava | mesto | — |
| Vladavina | Župsko vinogorje | Gornja Zleginja | mesto | — |
| Vujić | Župsko vinogorje | Aleksandrovac | mesto | Три Моравы и Жупа |
| Winery Milosavljevic | — | — | mesto | — |
| Yotta | — | — | mesto | Три Моравы и Жупа |
| Zupa | Župsko vinogorje | Александровац | mesto | Три Моравы и Жупа |
| Ćirić | Župsko vinogorje | Aleksandrovac | mesto | — |
| Žarković | Župsko vinogorje | Aleksandrovac | mesto | — |
| Винарија Живковић (Vinarija Živković) | Župsko vinogorje | Aleksandrovac | mesto | — |
| Винарија Живковића (Vinarija Živkovića-Tržac) | Župsko vinogorje | Tržac | mesto | — |
| Винарија Манастира Студеница | Župsko vinogorje | Aleksandrovac | mesto | — |
| Магаза (Magaza) | Trsteničko vinogorje | Velika Drenova | mesto | — |
| Мали Подрум Гајић - Mali Podrum Gajić | Župsko vinogorje | Gornja Zleginja | mesto | — |
| Манастир Студеница (Manastir Studenica) | Kruševačko vinogorje | — | decanter+vivino | — |
| Подрум Вина Лазаревић | Župsko vinogorje | Aleksandrovac | mesto | — |
| Подрум вина Рашковић - (Rašković Winery) | Župsko vinogorje | Vitkovo | mesto | — |
| Полрум Вина Тодор (Podrum Vina Todor) | Župsko vinogorje | Aleksandrovac | mesto | — |
| Три Планине (Vinarija Tri Planine) | Župsko vinogorje | Aleksandrovac | mesto | — |

### Sremski rejon — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| 45. Paralela | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Agrina | Fruškogorsko vinogorje | Irig | mesto | — |
| Alchemy Winery | Fruškogorsko vinogorje | — | vivino | — |
| Antonijević Family Winery | Fruškogorsko vinogorje | Ledinci | mesto | — |
| Art Et Vinum | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Atos-Fructum | Fruškogorsko vinogorje | Mala Remeta | mesto | — |
| Ačanski | Fruškogorsko vinogorje | Banoštor | mesto | — |
| BT Winery | Fruškogorsko vinogorje | — | decanter | — |
| Bajilo | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Belo Brdo | Fruškogorsko vinogorje | — | mesto | Фрушка гора |
| Benišek Veselinović | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Bikicki | Fruškogorsko vinogorje | Banoštor | mesto | Фрушка гора |
| Bjelica | Fruškogorsko vinogorje | — | mesto | Фрушка гора |
| Bojan Basa | Fruškogorsko vinogorje | Сремски Карловци | mesto | Фрушка гора |
| Breg | Fruškogorsko vinogorje | Janda | mesto | — |
| Chichateau | Fruškogorsko vinogorje | Лежимир | mesto | Фрушка гора |
| Deurić | Fruškogorsko vinogorje | Mala Remeta | mesto | Фрушка гора |
| Do Kraja Sveta | Fruškogorsko vinogorje | — | vivino | — |
| Dragojlović Vinarija | Fruškogorsko vinogorje | — | vivino | Фрушка гора |
| Dukay | Fruškogorsko vinogorje | Ириг | mesto | Фрушка гора |
| Dukay-Sagmeister | Fruškogorsko vinogorje | Ириг | mesto | Фрушка гора |
| Dulka | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Erdevik | Fruškogorsko vinogorje | Erdevik | mesto | Фрушка гора |
| Fruškogorski | Fruškogorsko vinogorje | Banoštor | mesto | — |
| Gora | Fruškogorsko vinogorje | — | decanter | — |
| Hadži Popović | Fruškogorsko vinogorje | Stari Slankamen | mesto | — |
| Kiš | Fruškogorsko vinogorje | Sremski Karlovci | mesto | Фрушка гора |
| Kovačević | Fruškogorsko vinogorje | Irig | mesto | Фрушка гора |
| Krstašica Doo | Fruškogorsko vinogorje | Irig | mesto | — |
| La Gora | Fruškogorsko vinogorje | Irig | mesto | — |
| La Grande Bellezza | Fruškogorsko vinogorje | — | decanter | — |
| Langov Podrum | Fruškogorsko vinogorje | Inđija | mesto | — |
| Manufaktura Spasić | Fruškogorsko vinogorje | — | decanter | — |
| Mačkov podrum | Fruškogorsko vinogorje | Irig | mesto | Фрушка гора |
| Mcculloch Wines | Fruškogorsko vinogorje | Novi Sad | mesto | — |
| Milanović | Fruškogorsko vinogorje | Surduk | mesto | Фрушка гора |
| Mister | Fruškogorsko vinogorje | — | decanter | — |
| Molovin | Fruškogorsko vinogorje | Моловин | mesto | Фрушка гора |
| Nera | Fruškogorsko vinogorje | — | vivino | — |
| Patkov Vinograd | Fruškogorsko vinogorje | Krčedin | mesto | — |
| Petković Latin | Fruškogorsko vinogorje | — | mesto | — |
| Podrum Petrović | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Podrum Stojković | Fruškogorsko vinogorje | Banoštor | mesto | — |
| Podrum Šukac | Fruškogorsko vinogorje | Sremska Kamenica | mesto | — |
| Probus Vineyards | Fruškogorsko vinogorje | — | mesto | — |
| Quet | Fruškogorsko vinogorje | — | decanter | — |
| Radošević | Fruškogorsko vinogorje | Banoštor | mesto | — |
| Rittium | Fruškogorsko vinogorje | — | vivino | — |
| Salaxia | Fruškogorsko vinogorje | Rakovac | vivino | — |
| Teodora | Fruškogorsko vinogorje | — | vivino | — |
| The Sparkling Winery | Fruškogorsko vinogorje | Mala Remeta | mesto | Фрушка гора |
| Tri Medje I Oblak | Fruškogorsko vinogorje | Neštin | mesto | — |
| Trivanović | Fruškogorsko vinogorje | — | mesto | Фрушка гора |
| Veritas Ćuković | Fruškogorsko vinogorje | Sremski Karlovci | mesto | Фрушка гора |
| Verkat | Fruškogorsko vinogorje | Čerević | mesto | Фрушка гора |
| Vinarija Acumincum | Fruškogorsko vinogorje | Сремски Карловци | mesto | Фрушка гора |
| Vinarija Apatović | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija Aven | Fruškogorsko vinogorje | Inđija | mesto | — |
| Vinarija Brestovački | Fruškogorsko vinogorje | Erdevik | mesto | — |
| Vinarija Burma Fruška Gora | Fruškogorsko vinogorje | — | vivino | Фрушка гора |
| Vinarija Djurdjic | Fruškogorsko vinogorje | Sremski Karlovci | mesto | Фрушка гора |
| Vinarija Dosen | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija Dumo | Fruškogorsko vinogorje | Rakovac | mesto | — |
| Vinarija Fleur D'Oranger | Fruškogorsko vinogorje | Novi Sad | mesto | — |
| Vinarija Frug | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija Grumen | Fruškogorsko vinogorje | Novi Sad | mesto | — |
| Vinarija Imperator | Fruškogorsko vinogorje | Rakovac | decanter+vivino | — |
| Vinarija KM | Fruškogorsko vinogorje | Novi Sad | mesto | — |
| Vinarija Komazec | Fruškogorsko vinogorje | Inđija | mesto | — |
| Vinarija Komuna PR | Fruškogorsko vinogorje | Rivica | mesto | — |
| Vinarija Kurjak | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija MK Kosović | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija Mira | Fruškogorsko vinogorje | Vrdnik | mesto | — |
| Vinarija Mrdjanin | Fruškogorsko vinogorje | Sremski Karlovci | mesto | — |
| Vinarija Podrum Danguba | Fruškogorsko vinogorje | Šid | mesto | — |
| Vinarija Praška | Fruškogorsko vinogorje | Bačka Palanka | mesto | — |
| Vinarija Sokolov Zamak | Fruškogorsko vinogorje | Beška | mesto | — |
| Vinarija Tanasković | Fruškogorsko vinogorje | Krušedol Prnjavor | mesto | — |
| Vinarija Šijački | Fruškogorsko vinogorje | Баноштор | mesto | Фрушка гора |
| Vinarium winery | Fruškogorsko vinogorje | Banoštor | mesto | — |
| Vinograd Hopovo | Fruškogorsko vinogorje | Irig | mesto | — |
| Vinum | Fruškogorsko vinogorje | Sremski Karlovci | mesto | Фрушка гора |
| Vinčić | Fruškogorsko vinogorje | Šid | mesto | Фрушка гора |
| Vista Hill | Fruškogorsko vinogorje | — | decanter | — |
| Vučurević | Fruškogorsko vinogorje | Novi Sad | mesto | — |
| Šapat | Fruškogorsko vinogorje | Нови Сланкамен | mesto | Фрушка гора |
| Živanović | Fruškogorsko vinogorje | Сремски Карловци | mesto | Фрушка гора |
| ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) | Fruškogorsko vinogorje | Slankamenački Vinogradi | mesto | — |

### Subotički rejon — Vojvodina

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| AE projekt centar | Riđičko vinogorje | Sombor | decanter | — |
| DiBonis Winery | Palićko vinogorje | Subotica | mesto | — |
| Jelena Munizaba PR Radnja za proizvodnju grozdja i vina, turizam i ugostiteljstvo. | Riđičko vinogorje | Riđica | mesto | — |
| Maurer | — | — | vivino | Суботичко-Хоргошская пешчара |
| Max-Ex Doo | Palićko vinogorje | Subotica | mesto | — |
| Podrum Palić | Palićko vinogorje | Palić | mesto | — |
| Reljić Vinarija | — | Palić | decanter | — |
| The Collective Presents | — | — | vivino | — |
| Tonković | Palićko vinogorje | Subotica | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Petra | Palićko vinogorje | Palić | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Salaš Naš | Horgoško vinogorje | Horgoš | mesto | — |
| Vinarija VRT | — | Sombor | vinarijesrbije | — |
| Vinarija Zaba | Riđičko vinogorje | — | decanter | — |
| Vinarija Šveljo | Riđičko vinogorje | Riđica | mesto | — |
| Vinski Dvor | — | — | vivino | — |
| WOW Winery | — | — | decanter | — |
| Zvonko Bogdan | Palićko vinogorje | Palić | mesto | Суботичко-Хоргошская пешчара |
| Драгић Винарија (Vina Dragic) | Riđičko vinogorje | Riđica | mesto | — |

### Šumadijski rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Aleksandrović | Oplenačko vinogorje | Vinča | mesto | Шумадия |
| Arsenijević | Oplenačko vinogorje | Topola | mesto | Шумадия |
| Art Wine | — | Kragujevac | mesto | — |
| Château Prince | Oplenačko vinogorje | Topola | mesto | — |
| Despotika | Krnjevačko vinogorje | Vlaški Do | mesto | Шумадия |
| Djordjevic Estate Winery | Račansko vinogorje | Lapovo | mesto | Шумадия |
| Draganić | Oplenačko vinogorje | Lipovac | mesto | Шумадия |
| Eden | Oplenačko vinogorje | Ranilović | mesto | Шумадия |
| Jelenac organic | Oplenačko vinogorje | Topola | mesto | — |
| Katanic | Kragujevačko vinogorje | Kamenica | mesto | — |
| Koreni 1934 | Oplenačko vinogorje | Lipovac | mesto | — |
| Legat | Oplenačko vinogorje | Banja | mesto | — |
| Matijašević Vinogradi | Oplenačko vinogorje | Orašac | mesto | Шумадия |
| PIK OPLENAC | Oplenačko vinogorje | Topola | mesto | — |
| Podrum Madžić | — | Smederevska Palanka | mesto | — |
| Podrum Stari Hrast | Kragujevačko vinogorje | Žirovnica | mesto | — |
| Radovanović | Krnjevačko vinogorje | Krnjevo | mesto | Шумадия |
| Rogan | Oplenačko vinogorje | Lipovac | mesto | — |
| Stari Oplenac | Oplenačko vinogorje | Topola | mesto | — |
| Tarpoš | Oplenačko vinogorje | Arandjelovac | mesto | Шумадия |
| Vina Mives | Kragujevačko vinogorje | Vlakča | mesto | — |
| Vinarija DeLena | Oplenačko vinogorje | Topola | mesto | — |
| Vinarija Mihailović | — | — | mesto | — |
| Vinarija PIRG | Oplenačko vinogorje | — | decanter | — |
| Vinarija VinoIlić | Oplenačko vinogorje | Topola | mesto | — |
| Vinarija Vladimir | Oplenačko vinogorje | Topola | mesto | — |
| Vinarija Vrbica | Oplenačko vinogorje | Aranđelovac | vivino-adres | — |
| Vinarija Žir | Krnjevačko vinogorje | Krnjevo | mesto | — |
| Vinogradi Veličković Vinarija | Oplenačko vinogorje | Aranđelovac | mesto | Три Моравы и Жупа |
| Zmajevac | Oplenačko vinogorje | Lipovac | mesto | — |
| Амбелос Винарија (Ambelos Winery) | — | Velika Plana | mesto | — |
| Дика Винарија | Oplenačko vinogorje | Lipovac | mesto | — |
| Трилогия Винария - Vinarija Trilogija | Oplenačko vinogorje | Banja | mesto | — |

### Toplički rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Doja | Prokupačko vinogorje | Blace | mesto | Топлица |
| Kostić | Prokupačko vinogorje | Prokuplje | mesto | Топлица |
| Tody | — | — | mesto | — |
| Vinarija Toplički Vinogradi | Prokupačko vinogorje | Gojinovac | mesto | Топлица |
| Аранђеловић 1920 (Aranđelović 1920) | — | — | vivino | — |

### Vranjski rejon — Centralna Srbija

| Хозяйство | Виногорје | Город | Откуда рејон | В книге |
|---|---|---|---|---|
| Aleksić | Vrtogoško vinogorje | Vranje | mesto | Юго-восток |
| Navip | Vrtogoško vinogorje | Vranje | mesto | — |
| Stari Dani | Vrtogoško vinogorje | Rakovac | mesto | — |
