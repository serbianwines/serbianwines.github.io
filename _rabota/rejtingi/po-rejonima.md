# Рејоны и виногорја

Настоящее место каждого хозяйства — по действующей сербской рејонизацији,
а не по главам книги.

**Зачем отдельно от книги.** Книга делит Сербию на десять глав; официальное
деление — три региона, 22 рејона, 77 виногорја. Это разные сетки, и совпадать
они не обязаны: одна глава книги может покрывать три рејона, а целые рејоны
в книгу не попасть вовсе. Пока рейтинги были разложены только по главам,
проверить это было нечем — теперь есть чем.

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
| Vojvodina | Rejon Bačka | 5 | 0 | 0 | 0 |
| Vojvodina | Banatski rejon | 1 | 0 | 0 | 0 |
| Centralna Srbija | Beogradski rejon | 15 | 35 | 25 | 27 |
| Centralna Srbija | Čačansko–kraljevački rejon | 3 | 1 | 1 | 1 |
| Vojvodina | Južnobanatski rejon | 14 | 23 | 14 | 14 |
| Centralna Srbija | Knjaževački rejon | 4 | 22 | 4 | 5 |
| Centralna Srbija | Leskovački rejon | 4 | 3 | 0 | 0 |
| Centralna Srbija | Mlavski rejon | 4 | 14 | 49 | 47 |
| Centralna Srbija | Nišavski rejon | 1 | 2 | 1 | 1 |
| Centralna Srbija | Niški rejon | 6 | 14 | 0 | 1 |
| Centralna Srbija | Pocersko Valjevski Rejon | 7 | 24 | 9 | 9 |
| Vojvodina | Potiski rejon | 4 | 19 | 4 | 4 |
| Centralna Srbija | Rejon Negotinska Krajina | 22 | 56 | 79 | 60 |
| Vojvodina | Rejon Telečka | 4 | 5 | 0 | 0 |
| Centralna Srbija | Rejon Tri Morave | 67 | 222 | 145 | 138 |
| Vojvodina | Sremski rejon | 84 | 317 | 273 | 276 |
| Vojvodina | Subotički rejon | 14 | 91 | 122 | 102 |
| Centralna Srbija | Šumadijski rejon | 31 | 164 | 173 | 129 |
| Centralna Srbija | Toplički rejon | 4 | 22 | 33 | 25 |
| Centralna Srbija | Vranjski rejon | 3 | 24 | 39 | 40 |
| — | **рејон не установлен** | 139 | 122 | 25 | 30 |

**Рејоны, из которых не собралось ни одного хозяйства:** Južnometohijski rejon, Severnometohijski rejon.


## Главы книги и рејоны

Столбец слева — глава книги, справа — в какие рејоны попадают её хозяйства по действующей рејонизацији.

| Глава книги | Рејоны её хозяйств |
|---|---|
| Фрушка гора | Sremski rejon — 20; не установлен — 2 |
| Суботичко-Хоргошская пешчара | Subotički rejon — 4 |
| Банат | Južnobanatski rejon — 1; Potiski rejon — 1; не установлен — 1 |
| Шумадия | Šumadijski rejon — 7; Rejon Tri Morave — 1 |
| Три Моравы и Жупа | Rejon Tri Morave — 12 |
| Неготинска Крайина | Rejon Negotinska Krajina — 3 |
| Топлица | Toplički rejon — 2 |
| Юго-восток | Knjaževački rejon — 2; Vranjski rejon — 1; Niški rejon — 1 |
| Подунавье и Белградский район | Beogradski rejon — 2 |
| Косово и Метохия | не установлен — 1 |

**Рејоны, где хозяйства есть, а в книге их нет:**

- **Rejon Bačka** (Vojvodina) — 117 Wine, Fekete, Sila, Vinarija Baza, Vindulo
- **Banatski rejon** (Vojvodina) — Kepul
- **Čačansko–kraljevački rejon** (Centralna Srbija) — Vinarija Tomić - Rošci, Vinarija Čolaković, Винарија Ступови (Vinarija Stupovi)
- **Leskovački rejon** (Centralna Srbija) — Prima, Vinarija Aquila, Козарак, Митровиђ Винарија
- **Mlavski rejon** (Centralna Srbija) — Pruna, Vinarija Necak, Vinarija Unikat, Virtus
- **Nišavski rejon** (Centralna Srbija) — Vinarija Savic
- **Pocersko Valjevski Rejon** (Centralna Srbija) — Andrića Vinograd, Karić Vinarija, Milijan Jelić, Podrum Lukic, Puce, Pusula, Vinarija Đurđevića Legat
- **Rejon Telečka** (Vojvodina) — Dimalis, Enellion, Milisavljević, Vinarija Radoslav Tripković

## Хозяйства по рејонима


### Rejon Bačka — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| 117 Wine | — | vivino | — |
| Fekete | — | vivino | — |
| Sila | — | vivino | — |
| Vinarija Baza | — | vivino | — |
| Vindulo | — | mesto | — |

### Banatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Kepul | Kikindsko vinogorje | mesto | — |

### Beogradski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Janovi Vinogradi | Avalsko-kosmajsko vinogorje | mesto | — |
| Plavinac | Smederevsko vinogorje | mesto | Подунавье и Белградский район |
| Plavinci | Gročansko vinogorje | mesto | — |
| Podrum Janko | Smederevsko vinogorje | mesto | — |
| Vinarija Jeremic | Smederevsko vinogorje | mesto | — |
| Vinarija Milićević | Avalsko-kosmajsko vinogorje | mesto | — |
| Vinarija Milojević | Lazarevačko vinogorje | mesto | — |
| Vinarija Panjković | Smederevsko vinogorje | mesto | — |
| Vinarija Pantić | — | mesto | — |
| Vinarija Vojinović | — | mesto | — |
| Vinarija Zorča | Lazarevačko vinogorje | mesto | — |
| Винарија Тришић (Vinarija Trišić) | Avalsko-kosmajsko vinogorje | mesto | — |
| Виногради Гроцка (Vinogradi Grocka) | Gročansko vinogorje | mesto | Подунавье и Белградский район |
| Краљвеска Винарија (Royal Winery) | Gročansko vinogorje | mesto | — |
| Фенек (Fenek Monastery) | — | mesto | — |

### Čačansko–kraljevački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Tomić - Rošci | — | mesto | — |
| Vinarija Čolaković | Ljubićko vinogorje | mesto | — |
| Винарија Ступови (Vinarija Stupovi) | — | vinarijesrbije | — |

### Južnobanatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Bahus | Vršačko vinogorje | mesto | — |
| Drašković | Vršačko vinogorje | mesto | Банат |
| Galot | Vinogorje Deliblatske peščare | mesto | — |
| Porodična Vinarija Stanimirović | — | mesto | — |
| Rnjak | Vršačko vinogorje | mesto | — |
| Soul Wine | Vršačko vinogorje | mesto | — |
| Vinarija Aleksandar | — | vinarijesrbije | — |
| Vinarija Lalić | — | mesto | — |
| Vinarija Nedin | Vršačko vinogorje | mesto | — |
| Vinarija Rajić | — | decanter | — |
| Vinarija Selecta | Vršačko vinogorje | mesto | — |
| Vinarija Sočanski | Vršačko vinogorje | mesto | — |
| Vinik | Vršačko vinogorje | mesto | — |
| Орлић Породична Винарија - Orlić Family Winery | Vršačko vinogorje | vivino-adres | — |

### Knjaževački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dzervin | Potrkanjsko vinogorje | mesto | Юго-восток |
| Jović | Potrkanjsko vinogorje | mesto | Юго-восток |
| Nikolas | Zaječarsko vinogorje | mesto | — |
| Vinarija Todorović | — | bolshinstvo | — |

### Leskovački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Prima | — | mesto | — |
| Vinarija Aquila | Vinaračko vinogorje | mesto | — |
| Козарак | — | vivino | — |
| Митровиђ Винарија | — | vivino | — |

### Mlavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Pruna | — | mesto | — |
| Vinarija Necak | Požarevačko vinogorje | mesto | — |
| Vinarija Unikat | Požarevačko vinogorje | mesto | — |
| Virtus | Požarevačko vinogorje | mesto | — |

### Nišavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Savic | — | bolshinstvo | — |

### Niški rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Podrum Ljubisavljević | Sokobanjsko vinogorje | mesto | — |
| Podrum Malča | Čegarsko vinogorje | mesto | Юго-восток |
| Status | Svrljiško vinogorje | mesto | — |
| Vinarija 100 Žena | Čegarsko vinogorje | mesto | — |
| Виница Грковић (Vinica Grković) | — | vivino | — |
| Изба Јовановић (Izba Jovanovic) | Čegarsko vinogorje | mesto | — |

### Pocersko Valjevski Rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Andrića Vinograd | — | vivino | — |
| Karić Vinarija | Pocersko vinogorje | mesto | — |
| Milijan Jelić | Podgorsko vinogorje | mesto | — |
| Podrum Lukic | Kolubarsko-ljiško vinogorje | mesto | — |
| Puce | Podgorsko vinogorje | mesto | — |
| Pusula | Podgorsko vinogorje | mesto | — |
| Vinarija Đurđevića Legat | Podgorsko vinogorje | mesto | — |

### Potiski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dukay | Severnopotisko vinogorje | mesto | — |
| Vinarija Coka | Severnopotisko vinogorje | mesto | Банат |
| Vinarija Gnezdo | Srednjepotisko vinogorje | mesto | — |
| Vinartos Vinarija | Srednjepotisko vinogorje | mesto | — |

### Rejon Negotinska Krajina — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Cubra | Negotinsko vinogorje | mesto | — |
| Dalia | — | vivino | — |
| Francuska Vinarija - Estelle et Cyrille Bongiraud | Rogljevačko-rajačko vinogorje | mesto | — |
| Manastir Bukovo | — | decanter | Неготинска Крайина |
| Matalj | — | mesto | Неготинска Крайина |
| Mikić | Rogljevačko-rajačko vinogorje | mesto | — |
| Radu Group Vinarija | Rogljevačko-rajačko vinogorje | mesto | — |
| Tenuta Est Winery | Negotinsko vinogorje | mesto | — |
| Traško Vinarija | Negotinsko vinogorje | mesto | — |
| Vinarija Boierescu | Negotinsko vinogorje | mesto | — |
| Vinarija Dajic | Mihajlovačko vinogorje | mesto | — |
| Vinarija Frunza Aglaja | Negotinsko vinogorje | mesto | — |
| Vinarija Gamanović | — | decanter+vivino | — |
| Vinarija Janucic | Rogljevačko-rajačko vinogorje | mesto | — |
| Vinarija Novak (Новак) | — | vivino | — |
| Vinarija Porta | — | vivino | — |
| Vinarija Raj | Negotinsko vinogorje | mesto | Неготинска Крайина |
| Vinarija Tana | Rogljevačko-rajačko vinogorje | mesto | — |
| Vinarija Timacvm Minvs | — | mesto | — |
| Vinarija Timahus | — | vivino | — |
| Винарија Королија | Rogljevačko-rajačko vinogorje | mesto | — |
| Винарија Манастира Буково | Negotinsko vinogorje | mesto | — |

### Rejon Telečka — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dimalis | Centralnotelečko vinogorje | mesto | — |
| Enellion | Zapadnotelečko vinogorje | vivino-adres | — |
| Milisavljević | Zapadnotelečko vinogorje | mesto | — |
| Vinarija Radoslav Tripković | — | vivino-adres | — |

### Rejon Tri Morave — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Adora | Jagodinsko vinogorje | mesto | — |
| Aleksandar Todorović | — | mesto | — |
| Botunjac | Župsko vinogorje | mesto | — |
| Braca Rajkovic | Župsko vinogorje | mesto | — |
| Budimir | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Cilić | — | vivino | Три Моравы и Жупа |
| Cvetković Vinarija | — | mesto | — |
| Damjanovic | Župsko vinogorje | mesto | — |
| Grabak | Kruševačko vinogorje | mesto | — |
| Ivanović | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Kalem | Trsteničko vinogorje | mesto | — |
| Marko | Trsteničko vinogorje | mesto | Шумадия |
| Milan Nikolić | Jagodinsko vinogorje | decanter | — |
| Milanov Podrum | Župsko vinogorje | mesto | — |
| Milić | Župsko vinogorje | vivino-adres | — |
| Pet Hrastova | — | mesto | — |
| Podrum Bačina | Temnićko vinogorje | mesto | — |
| Podrum Dremina | Paraćinsko vinogorje | mesto | — |
| Podrum Tošići | Župsko vinogorje | mesto | — |
| Radosavljevic | Kruševačko vinogorje | mesto | — |
| Radovan | Kruševačko vinogorje | mesto | Три Моравы и Жупа |
| Ralević | Paraćinsko vinogorje | mesto | Три Моравы и Жупа |
| Rubin | Kruševačko vinogorje | mesto | Три Моравы и Жупа |
| Saboss | Župsko vinogorje | mesto | — |
| Savković | Župsko vinogorje | mesto | — |
| Spasić | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Stemina | Trsteničko vinogorje | mesto | — |
| Temet | Jagodinsko vinogorje | mesto | Три Моравы и Жупа |
| Uziwa Winery | — | vivino-adres | — |
| Varina | — | mesto | — |
| Vert | — | vivino | — |
| Vertiz | Levačko vinogorje | mesto | — |
| Vila Vina | — | vivino | — |
| Vilimonovic | Trsteničko vinogorje | mesto | — |
| Vina Jelenković | Župsko vinogorje | mesto | — |
| Vinarija Agatija | Levačko vinogorje | mesto | — |
| Vinarija Bada | Župsko vinogorje | mesto | — |
| Vinarija Bora | Levačko vinogorje | mesto | — |
| Vinarija Fragaria | Župsko vinogorje | mesto | — |
| Vinarija Jovac | Jagodinsko vinogorje | mesto | Три Моравы и Жупа |
| Vinarija Lastar | Levačko vinogorje | mesto | — |
| Vinarija Levač | Levačko vinogorje | mesto | — |
| Vinarija Mozaik Milan | — | vivino | — |
| Vinarija Piano | Jagodinsko vinogorje | mesto | — |
| Vinarija Smiljković 90 | Župsko vinogorje | mesto | — |
| Vinarija Venčac | Jagodinsko vinogorje | decanter | — |
| Vinarija Vinis | Paraćinsko vinogorje | mesto | — |
| Vinarija Ćosić | Župsko vinogorje | mesto | — |
| Vinex Grozd | Levačko vinogorje | mesto | — |
| Vinska Kuća Milinčić | Župsko vinogorje | mesto | — |
| Vinska Kuća Minića | Župsko vinogorje | mesto | — |
| Vladavina | Župsko vinogorje | mesto | — |
| Vujić | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Yotta | — | mesto | Три Моравы и Жупа |
| Zupa | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Ćirić | Župsko vinogorje | mesto | — |
| Žarković | Župsko vinogorje | mesto | — |
| Винарија Живковић (Vinarija Živković) | Župsko vinogorje | mesto | — |
| Винарија Живковића (Vinarija Živkovića-Tržac) | Župsko vinogorje | mesto | — |
| Винарија Манастира Студеница | Župsko vinogorje | mesto | — |
| Магаза (Magaza) | Trsteničko vinogorje | mesto | — |
| Мали Подрум Гајић - Mali Podrum Gajić | Župsko vinogorje | mesto | — |
| Манастир Студеница (Manastir Studenica) | Kruševačko vinogorje | decanter+vivino | — |
| Подрум Вина Лазаревић | Župsko vinogorje | mesto | — |
| Подрум вина Рашковић - (Rašković Winery) | Župsko vinogorje | mesto | — |
| Полрум Вина Тодор (Podrum Vina Todor) | Župsko vinogorje | mesto | — |
| Три Планине (Vinarija Tri Planine) | Župsko vinogorje | mesto | — |

### Sremski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| 45. Paralela | Fruškogorsko vinogorje | mesto | — |
| Agrina | Fruškogorsko vinogorje | mesto | — |
| Alchemy Winery | Fruškogorsko vinogorje | vivino | — |
| Antonijević Family Winery | Fruškogorsko vinogorje | mesto | — |
| Art Et Vinum | Fruškogorsko vinogorje | mesto | — |
| Atos-Fructum | Fruškogorsko vinogorje | mesto | — |
| Ačanski | Fruškogorsko vinogorje | mesto | — |
| BT Winery | Fruškogorsko vinogorje | decanter | — |
| Bajilo | Fruškogorsko vinogorje | mesto | — |
| Belo Brdo | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Benišek Veselinović | Fruškogorsko vinogorje | mesto | — |
| Bikicki | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Bjelica | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Breg | Fruškogorsko vinogorje | mesto | — |
| Chichateau | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Deurić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Do Kraja Sveta | Fruškogorsko vinogorje | vivino | — |
| Dragojlović Vinarija | Fruškogorsko vinogorje | vivino | — |
| Dulka | Fruškogorsko vinogorje | mesto | — |
| Erdevik | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Fruškogorski | Fruškogorsko vinogorje | mesto | — |
| Gora | Fruškogorsko vinogorje | decanter | — |
| Hadži Popović | Fruškogorsko vinogorje | mesto | — |
| Kiš | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Kovačević | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Krstašica Doo | Fruškogorsko vinogorje | mesto | — |
| La Gora | Fruškogorsko vinogorje | mesto | — |
| La Grande Bellezza | Fruškogorsko vinogorje | decanter | — |
| Langov Podrum | Fruškogorsko vinogorje | mesto | — |
| Mackov Podrum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Manufaktura Spasić | Fruškogorsko vinogorje | decanter | — |
| Mcculloch Wines | Fruškogorsko vinogorje | mesto | — |
| Milanović | Fruškogorsko vinogorje | mesto | — |
| Mister | Fruškogorsko vinogorje | decanter | — |
| Molovin | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Nera | Fruškogorsko vinogorje | vivino | — |
| Patkov Vinograd | Fruškogorsko vinogorje | mesto | — |
| Petković Latin | Fruškogorsko vinogorje | mesto | — |
| Podrum Stojković | Fruškogorsko vinogorje | mesto | — |
| Podrum Šukac | Fruškogorsko vinogorje | mesto | — |
| Probus Vineyards | Fruškogorsko vinogorje | mesto | — |
| Quet | Fruškogorsko vinogorje | decanter | — |
| Radošević | Fruškogorsko vinogorje | mesto | — |
| Rittium | Fruškogorsko vinogorje | vivino | — |
| Salaxia | Fruškogorsko vinogorje | vivino | — |
| Teodora | Fruškogorsko vinogorje | vivino | — |
| The Sparkling Winery | Fruškogorsko vinogorje | mesto | — |
| Tri Medje I Oblak | Fruškogorsko vinogorje | mesto | — |
| Trivanović | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Veritas Ćuković | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Verkat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Acumincum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Apatović | Fruškogorsko vinogorje | mesto | — |
| Vinarija Aven | Fruškogorsko vinogorje | mesto | — |
| Vinarija Brestovački | Fruškogorsko vinogorje | mesto | — |
| Vinarija Burma Fruška Gora | Fruškogorsko vinogorje | vivino | — |
| Vinarija Dosen | Fruškogorsko vinogorje | mesto | — |
| Vinarija Dumo | Fruškogorsko vinogorje | mesto | — |
| Vinarija Fleur D'Oranger | Fruškogorsko vinogorje | mesto | — |
| Vinarija Frug | Fruškogorsko vinogorje | mesto | — |
| Vinarija Grumen | Fruškogorsko vinogorje | mesto | — |
| Vinarija Imperator | Fruškogorsko vinogorje | mesto | — |
| Vinarija KM | Fruškogorsko vinogorje | mesto | — |
| Vinarija Komazec | Fruškogorsko vinogorje | mesto | — |
| Vinarija Komuna | Fruškogorsko vinogorje | mesto | — |
| Vinarija Kurjak | Fruškogorsko vinogorje | mesto | — |
| Vinarija MK Kosović | Fruškogorsko vinogorje | mesto | — |
| Vinarija Mira | Fruškogorsko vinogorje | mesto | — |
| Vinarija Mrdjanin | Fruškogorsko vinogorje | mesto | — |
| Vinarija Podrum Danguba | Fruškogorsko vinogorje | mesto | — |
| Vinarija Praška | Fruškogorsko vinogorje | mesto | — |
| Vinarija Sokolov Zamak | Fruškogorsko vinogorje | mesto | — |
| Vinarija Tanasković | Fruškogorsko vinogorje | mesto | — |
| Vinarija Đurđić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Šijački | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarium | Fruškogorsko vinogorje | mesto | — |
| Vinograd Hopovo | Fruškogorsko vinogorje | mesto | — |
| Vinum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinčić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vista Hill | Fruškogorsko vinogorje | decanter | — |
| Vučurević | Fruškogorsko vinogorje | mesto | — |
| Šapat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Živanović | Fruškogorsko vinogorje | mesto | Фрушка гора |
| ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) | Fruškogorsko vinogorje | mesto | — |

### Subotički rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dibonis Winery | Palićko vinogorje | mesto | — |
| Maurer | — | vivino | Суботичко-Хоргошская пешчара |
| Max-Ex Doo | Palićko vinogorje | mesto | — |
| Podrum Palić | Palićko vinogorje | mesto | — |
| Reljić Vinarija | — | decanter | — |
| The Collective Presents | — | vivino | — |
| Tonković | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Petra | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Salaš Naš | Horgoško vinogorje | mesto | — |
| Vinarija Zaba | Riđičko vinogorje | decanter | — |
| Vinski Dvor | — | vivino | — |
| Zvonko Bogdan | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Šveljo | Riđičko vinogorje | mesto | — |
| Драгић Винарија (Vina Dragic) | Riđičko vinogorje | mesto | — |

### Šumadijski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Aleksandrović | Oplenačko vinogorje | mesto | Шумадия |
| Arsenijević | Oplenačko vinogorje | mesto | Шумадия |
| Art Wine | — | mesto | — |
| Château Prince | Oplenačko vinogorje | mesto | — |
| Despotika | Krnjevačko vinogorje | mesto | Шумадия |
| Draganić | Oplenačko vinogorje | mesto | Шумадия |
| Katanic | Kragujevačko vinogorje | mesto | — |
| Legat | Oplenačko vinogorje | mesto | — |
| Matijašević | Oplenačko vinogorje | mesto | Шумадия |
| PIK Oplenac | Oplenačko vinogorje | mesto | — |
| Podrum Madžić | — | mesto | — |
| Podrum Pevac | — | mesto | — |
| Podrum Stari Hrast | Kragujevačko vinogorje | mesto | — |
| Radovanović | Krnjevačko vinogorje | mesto | Шумадия |
| Rogan | Oplenačko vinogorje | mesto | — |
| Stari Oplenac | Oplenačko vinogorje | mesto | — |
| Tarpoš | Oplenačko vinogorje | mesto | Шумадия |
| Tref Line | Oplenačko vinogorje | decanter | — |
| Vina Mives | Kragujevačko vinogorje | mesto | — |
| Vinarija DeLena | Oplenačko vinogorje | mesto | — |
| Vinarija Eden | Oplenačko vinogorje | mesto | — |
| Vinarija Mihailović | — | mesto | — |
| Vinarija VinoIlić | Oplenačko vinogorje | mesto | — |
| Vinarija Vladimir | Oplenačko vinogorje | vivino-adres | — |
| Vinarija Vrbica | Oplenačko vinogorje | vivino-adres | — |
| Vinarija Žir | Krnjevačko vinogorje | mesto | — |
| Vinogradi Veličković Vinarija | Oplenačko vinogorje | mesto | — |
| Zmajevac | Oplenačko vinogorje | mesto | — |
| Амбелос Винарија (Ambelos Winery) | — | mesto | — |
| Дика Винарија | Oplenačko vinogorje | mesto | — |
| Трилогия Винария - Vinarija Trilogija | Oplenačko vinogorje | mesto | — |

### Toplički rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Doja | Prokupačko vinogorje | mesto | Топлица |
| Toplički Vinogradi | Prokupačko vinogorje | mesto | Топлица |
| Аранђеловић 1920 (Aranđelović 1920) | — | vivino | — |
| Костић (Kostić) | Prokupačko vinogorje | mesto | — |

### Vranjski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Aleksić | Vrtogoško vinogorje | mesto | Юго-восток |
| Navip | Vrtogoško vinogorje | mesto | — |
| Stari Dani | Vrtogoško vinogorje | mesto | — |
