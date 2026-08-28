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
| **ivv.rs** | «Вина и винарије Србије»: место с округом — «Vinča, Topola - Oplenac, Šumadijski okrug» | 142 |
| **vinarijesrbije.rs** | справочник винарий: рејон, город, адрес | 129 |
| **Decanter** | `region` + `subRegion` у каждого вина — единственный источник, доходящий до виногорја | 997 записей |
| **Vivino** | плоский `region` у вина, до виногорја не доходит | 2786 вин |
| **Falstaff** | область в печатном списке | 116 позиций |
| **книга** | город хозяйства в `raion-hozyaistv.json` | 32 |

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
работает только как **вместилище**: если все общины округа лежат в одном
рејоне, рејон известен. Так получается у 14 округов из 23; по остальным —
Зајечарски делится между Књажевачким и Нишким, Јужно-бачки между четырьмя
рејонима — по округу не ставится ничего.

На одном округе держатся девять хозяйств: Vinarija Eden, Katanić,
Matalj, Matijašević, Milanović, Podrum Probus, Rogan, Tarpoš, Zmajevac.
Все остальные опираются на общину или село.

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

## Как решается спор

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

Остальное сведено руками, по одному, с доказательством — в
`sinonimy-hozyaistv.json`. Всего строк стало 443 вместо 472.

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

## Как проверить глазами

Хозяйство на Vivino открывается по слагу:
`https://www.vivino.com/wineries/<слаг>` — слаг лежит в поле
`vivino_slug` таблицы хозяйств. Награда Decanter — по номеру вина из
поля `stranica`: `https://awards.decanter.com/DWWA/<год>/wines/<номер>`.
Карточка ivv.rs — `https://www.ivv.rs/vinarija/<слаг>/`.

**Пересобрать файл:**

    python3 _rabota/rejtingi/sobrat-rejony.py
    python3 _rabota/rejtingi/sobrat-tablicy.py
    python3 _rabota/rejtingi/svesti-rejony.py --otchet

<!-- Собрано скриптом svesti-rejony.py. Руками не править. -->

## Что собралось по рејонима

Хозяйства разложены по действующей рејонизацији: 3 региона, 22 рејона, 77 виногорја. Глава книги — отдельный столбец, она не обязана совпадать.

| Регион | Рејон | Хозяйств | Оценок Vivino | Оценок критиков | Наград |
|---|---|---|---|---|---|
| Vojvodina | Rejon Bačka | 6 | 0 | 0 | 0 |
| Vojvodina | Banatski rejon | 1 | 0 | 0 | 0 |
| Centralna Srbija | Beogradski rejon | 12 | 32 | 24 | 26 |
| Centralna Srbija | Čačansko–kraljevački rejon | 2 | 1 | 1 | 1 |
| Vojvodina | Južnobanatski rejon | 8 | 23 | 13 | 13 |
| Kosovo i Metohija | Južnometohijski rejon | 1 | 0 | 0 | 0 |
| Centralna Srbija | Knjaževački rejon | 3 | 20 | 4 | 5 |
| Centralna Srbija | Leskovački rejon | 4 | 3 | 0 | 0 |
| Centralna Srbija | Mlavski rejon | 2 | 14 | 46 | 44 |
| Centralna Srbija | Nišavski rejon | 1 | 2 | 1 | 1 |
| Centralna Srbija | Niški rejon | 3 | 10 | 0 | 0 |
| Centralna Srbija | Pocersko Valjevski Rejon | 5 | 24 | 9 | 9 |
| Vojvodina | Potiski rejon | 3 | 19 | 0 | 0 |
| Centralna Srbija | Rejon Negotinska Krajina | 15 | 52 | 79 | 59 |
| Vojvodina | Rejon Telečka | 1 | 2 | 0 | 0 |
| Centralna Srbija | Rejon Tri Morave | 44 | 182 | 144 | 137 |
| Vojvodina | Sremski rejon | 76 | 319 | 269 | 272 |
| Vojvodina | Subotički rejon | 13 | 91 | 122 | 102 |
| Centralna Srbija | Šumadijski rejon | 24 | 164 | 174 | 130 |
| Centralna Srbija | Toplički rejon | 4 | 22 | 33 | 25 |
| Centralna Srbija | Vranjski rejon | 1 | 16 | 39 | 40 |
| — | **рејон не установлен** | 214 | 190 | 38 | 45 |

**Рејоны, из которых не собралось ни одного хозяйства:** Severnometohijski rejon.


## Главы книги и рејоны

Столбец слева — глава книги, справа — в какие рејоны попадают её хозяйства по действующей рејонизацији.

| Глава книги | Рејоны её хозяйств |
|---|---|
| Фрушка гора | Sremski rejon — 20; не установлен — 2 |
| Суботичко-Хоргошская пешчара | Subotički rejon — 4 |
| Банат | Južnobanatski rejon — 1; Potiski rejon — 1; не установлен — 1 |
| Шумадия | Šumadijski rejon — 7; Rejon Tri Morave — 1 |
| Три Моравы и Жупа | Rejon Tri Morave — 11; Šumadijski rejon — 1 |
| Неготинска Крайина | Rejon Negotinska Krajina — 3 |
| Топлица | Toplički rejon — 2 |
| Юго-восток | Knjaževački rejon — 2; Vranjski rejon — 1; Niški rejon — 1 |
| Подунавье и Белградский район | не установлен — 1; Beogradski rejon — 1 |
| Косово и Метохия | не установлен — 1 |

**Рејоны, где хозяйства есть, а в книге их нет:**

- **Rejon Bačka** (Vojvodina) — 117 Wine, Dimalis, Fekete, Sila, Vinarija Baza, Vindulo
- **Banatski rejon** (Vojvodina) — Vinarija Sočanski
- **Čačansko–kraljevački rejon** (Centralna Srbija) — Vinarija Tomić - Rošci, Винарија Ступови (Vinarija Stupovi)
- **Južnometohijski rejon** (Kosovo i Metohija) — Podrum Lukic
- **Leskovački rejon** (Centralna Srbija) — Prima, Vinarija Aquila, Козарак, Митровиђ Винарија
- **Mlavski rejon** (Centralna Srbija) — Pruna, Virtus
- **Nišavski rejon** (Centralna Srbija) — Vinarija Savic
- **Pocersko Valjevski Rejon** (Centralna Srbija) — Andrića Vinograd, Karić Vinarija, Milijan Jelić, Pusula, Vinarija Đurđevića Legat
- **Rejon Telečka** (Vojvodina) — Milisavljević

## Хозяйства по рејонима


### Rejon Bačka — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| 117 Wine | — | vivino | — |
| Dimalis | — | vivino | — |
| Fekete | — | vivino | — |
| Sila | — | vivino | — |
| Vinarija Baza | — | vivino | — |
| Vindulo | — | mesto | — |

### Banatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Sočanski | — | vinarijesrbije | — |

### Beogradski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Janovi Vinogradi | Avalsko-kosmajsko vinogorje | mesto | — |
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

### Čačansko–kraljevački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Tomić - Rošci | — | vivino | — |
| Винарија Ступови (Vinarija Stupovi) | — | vinarijesrbije | — |

### Južnobanatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Drašković | Vršačko vinogorje | mesto | Банат |
| Galot | Vinogorje Deliblatske peščare | mesto | — |
| Rnjak | Vršačko vinogorje | mesto | — |
| Vinarija Aleksandar | — | vinarijesrbije | — |
| Vinarija Nedin | Vršačko vinogorje | mesto | — |
| Vinarija Rajić | — | decanter | — |
| Vinarija Selecta | Vršačko vinogorje | mesto | — |
| Vinik | Vršačko vinogorje | mesto | — |

### Južnometohijski rejon — Kosovo i Metohija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Podrum Lukic | — | vinarijesrbije | — |

### Knjaževački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dzervin | Potrkanjsko vinogorje | mesto | Юго-восток |
| Jović | Potrkanjsko vinogorje | mesto | Юго-восток |
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
| Virtus | Požarevačko vinogorje | mesto | — |

### Nišavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Savic | — | bolshinstvo | — |

### Niški rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Podrum Malča | Čegarsko vinogorje | mesto | Юго-восток |
| Vinarija 100 Žena | — | vinarijesrbije+vivino | — |
| Виница Грковић (Vinica Grković) | — | vivino | — |

### Pocersko Valjevski Rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Andrića Vinograd | — | vivino | — |
| Karić Vinarija | Pocersko vinogorje | mesto | — |
| Milijan Jelić | Podgorsko vinogorje | mesto | — |
| Pusula | Podgorsko vinogorje | mesto | — |
| Vinarija Đurđevića Legat | Podgorsko vinogorje | mesto | — |

### Potiski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dukay | Severnopotisko vinogorje | mesto | — |
| Vinarija Coka | Severnopotisko vinogorje | mesto | Банат |
| Vinartos Vinarija | — | vivino | — |

### Rejon Negotinska Krajina — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dalia | — | vivino | — |
| Francuska Vinarija - Estelle et Cyrille Bongiraud | — | vivino | — |
| Manastir Bukovo | — | decanter | Неготинска Крайина |
| Matalj | — | mesto | Неготинска Крайина |
| Tenuta Est Winery | — | vivino | — |
| Traško Vinarija | — | decanter+vivino | — |
| Vinarija Frunza Aglaja | Negotinsko vinogorje | mesto | — |
| Vinarija Gamanović | — | decanter+vivino | — |
| Vinarija Janucic | — | decanter+vivino | — |
| Vinarija Novak (Новак) | — | vivino | — |
| Vinarija Porta | — | vivino | — |
| Vinarija Raj | Negotinsko vinogorje | mesto | Неготинска Крайина |
| Vinarija Timahus | — | vivino | — |
| ΒИММИД ΒИΗΑΡИЈΑ (Vimmid Winery) | Negotinsko vinogorje | mesto | — |
| Винарија Манастира Буково | — | vivino | — |

### Rejon Telečka — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Milisavljević | — | vinarijesrbije | — |

### Rejon Tri Morave — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Adora | Jagodinsko vinogorje | mesto | — |
| Aleksandar Todorović | — | vivino | — |
| Botunjac | Župsko vinogorje | mesto | — |
| Braca Rajkovic | Župsko vinogorje | mesto | — |
| Budimir | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Cvetković Vinarija | — | mesto | — |
| Grabak | Kruševačko vinogorje | decanter | — |
| Ivanović | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Marko | Trsteničko vinogorje | mesto | Шумадия |
| Milan Nikolić | Jagodinsko vinogorje | decanter | — |
| Milanov Podrum | Župsko vinogorje | mesto | — |
| Pet Hrastova | — | mesto | — |
| Podrum Bačina | Kruševačko vinogorje | mesto | — |
| Podrum Tošići | Župsko vinogorje | mesto | — |
| Radovan | — | vinarijesrbije | — |
| Ralević | — | mesto | Три Моравы и Жупа |
| Rubin | Kruševačko vinogorje | mesto | Три Моравы и Жупа |
| Spasić | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Stemina | Kruševačko vinogorje | mesto | — |
| Temet | Jagodinsko vinogorje | mesto | Три Моравы и Жупа |
| Varina | — | vivino | — |
| Vert | — | vivino | — |
| Vertiz | Levačko vinogorje | mesto | — |
| Vila Vina | — | vivino | — |
| Vinarija Bora | — | vivino | — |
| Vinarija Fragaria | Župsko vinogorje | mesto | — |
| Vinarija Jovac | Jagodinsko vinogorje | decanter+vivino | Три Моравы и Жупа |
| Vinarija Lastar | Levačko vinogorje | mesto | — |
| Vinarija Mozaik Milan | — | vivino | — |
| Vinarija Smiljković 90 | Župsko vinogorje | mesto | — |
| Vinarija Venčac | Jagodinsko vinogorje | decanter | — |
| Vinarija Vinis | Jagodinsko vinogorje | decanter | — |
| Vinarija Ćosić | Župsko vinogorje | mesto | — |
| Vinska Kuća Milinčić | — | vivino | — |
| Vinska Kuća Minića | Župsko vinogorje | mesto | — |
| Vujić | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Yotta | — | mesto | Три Моравы и Жупа |
| Zupa | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Čokot | Kruševačko vinogorje | decanter | Три Моравы и Жупа |
| Žarković | Župsko vinogorje | mesto | — |
| Винарија Живковић (Vinarija Živković) | Župsko vinogorje | mesto | — |
| Манастир Студеница (Manastir Studenica) | Kruševačko vinogorje | decanter+vivino | — |
| Полрум Вина Тодор (Podrum Vina Todor) | Župsko vinogorje | mesto | — |
| Три Планине (Vinarija Tri Planine) | Župsko vinogorje | mesto | — |

### Sremski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| 45. Paralela | Fruškogorsko vinogorje | mesto | — |
| Alchemy Winery | Fruškogorsko vinogorje | vivino | — |
| Art Et Vinum | Fruškogorsko vinogorje | mesto | — |
| Atos-Fructum | Fruškogorsko vinogorje | decanter | — |
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
| Hadži Popović | Fruškogorsko vinogorje | vivino | — |
| Kiš | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Kovačević | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Krstašica Doo | Fruškogorsko vinogorje | decanter+vivino | — |
| La Gora | Fruškogorsko vinogorje | mesto | — |
| La Grande Bellezza | Fruškogorsko vinogorje | decanter | — |
| Mackov Podrum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Manufaktura Spasić | Fruškogorsko vinogorje | decanter | — |
| Mcculloch Wines | Fruškogorsko vinogorje | decanter+vivino | — |
| Milanović | Fruškogorsko vinogorje | mesto | — |
| Mister | Fruškogorsko vinogorje | decanter | — |
| Molovin | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Nera | Fruškogorsko vinogorje | vivino | — |
| Patkov Vinograd | Fruškogorsko vinogorje | mesto | — |
| Petković Latin | Fruškogorsko vinogorje | vivino | — |
| Podrum Stojković | Fruškogorsko vinogorje | mesto | — |
| Probus Vineyards | Fruškogorsko vinogorje | mesto | — |
| Quet | Fruškogorsko vinogorje | decanter | — |
| Radošević | Fruškogorsko vinogorje | mesto | — |
| Rittium | Fruškogorsko vinogorje | vivino | — |
| Salaxia | Fruškogorsko vinogorje | vivino | — |
| Teodora | Fruškogorsko vinogorje | vivino | — |
| The Sparkling Winery | Fruškogorsko vinogorje | decanter | — |
| Tri Medje I Oblak | Fruškogorsko vinogorje | mesto | — |
| Trivanović | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Veritas | Fruškogorsko vinogorje | mesto | — |
| Veritas Ćuković | Fruškogorsko vinogorje | decanter+vinarijesrbije+vivino | Фрушка гора |
| Verkat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Acumincum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Aven | Fruškogorsko vinogorje | bolshinstvo | — |
| Vinarija Brestovački | Fruškogorsko vinogorje | mesto | — |
| Vinarija Burma Fruška Gora | Fruškogorsko vinogorje | vivino | — |
| Vinarija Dosen | Fruškogorsko vinogorje | mesto | — |
| Vinarija Dumo | Fruškogorsko vinogorje | mesto | — |
| Vinarija Frug | Fruškogorsko vinogorje | decanter | — |
| Vinarija Grumen | Fruškogorsko vinogorje | vivino | — |
| Vinarija Imperator | Fruškogorsko vinogorje | mesto | — |
| Vinarija KM | Fruškogorsko vinogorje | mesto | — |
| Vinarija Komazec | Fruškogorsko vinogorje | decanter+vivino | — |
| Vinarija Komuna | Fruškogorsko vinogorje | mesto | — |
| Vinarija Kurjak | Fruškogorsko vinogorje | mesto | — |
| Vinarija MK Kosović | Fruškogorsko vinogorje | vivino | — |
| Vinarija Mrdjanin | Fruškogorsko vinogorje | mesto | — |
| Vinarija Podrum Danguba | Fruškogorsko vinogorje | mesto | — |
| Vinarija Sokolov Zamak | Fruškogorsko vinogorje | mesto | — |
| Vinarija Tanasković | Fruškogorsko vinogorje | vivino | — |
| Vinarija Đurđić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Šijački | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarium | Fruškogorsko vinogorje | mesto | — |
| Vinum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinčić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vista Hill | Fruškogorsko vinogorje | decanter | — |
| Šapat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Šveljo | Fruškogorsko vinogorje | vinarijesrbije | — |
| Živanović | Fruškogorsko vinogorje | mesto | Фрушка гора |
| ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) | Fruškogorsko vinogorje | mesto | — |

### Subotički rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dibonis Winery | — | decanter+vivino | — |
| Maurer | — | vivino | Суботичко-Хоргошская пешчара |
| Max-Ex Doo | — | decanter | — |
| Porodična Vinarija Stanimirović | — | vivino | — |
| Reljić Vinarija | — | decanter | — |
| The Collective Presents | — | vivino | — |
| Tonković | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Petra | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Salaš Naš | Horgoško vinogorje | mesto | — |
| Vinarija Zaba | Riđičko vinogorje | decanter | — |
| Vinski Dvor | — | vivino | — |
| Zvonko Bogdan | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Драгић Винарија (Vina Dragic) | Riđičko vinogorje | mesto | — |

### Šumadijski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Aleksandrović | Oplenačko vinogorje | mesto | Шумадия |
| Arsenijević | — | mesto | Шумадия |
| Art Wine | — | mesto | — |
| Château Prince | Oplenačko vinogorje | mesto | — |
| Cilić | Krnjevačko vinogorje | mesto | Три Моравы и Жупа |
| Despotika | Krnjevačko vinogorje | mesto | Шумадия |
| Draganić | Oplenačko vinogorje | mesto | Шумадия |
| Katanic | Kragujevačko vinogorje | mesto | — |
| Matijašević | Oplenačko vinogorje | mesto | Шумадия |
| PIK Oplenac | Oplenačko vinogorje | decanter | — |
| Podrum Madžić | — | mesto | — |
| Podrum Pevac | — | mesto | — |
| Podrum Stari Hrast | Kragujevačko vinogorje | mesto | — |
| Radovanović | Krnjevačko vinogorje | mesto | Шумадия |
| Rogan | Oplenačko vinogorje | mesto | — |
| Tarpoš | Oplenačko vinogorje | mesto | Шумадия |
| Tref Line | Oplenačko vinogorje | decanter | — |
| Vinarija DeLena | Oplenačko vinogorje | mesto | — |
| Vinarija Eden | Oplenačko vinogorje | mesto | — |
| Vinarija Žir | Krnjevačko vinogorje | mesto | — |
| Vinogradi Veličković Vinarija | Oplenačko vinogorje | mesto | — |
| Zmajevac | Oplenačko vinogorje | mesto | — |
| Амбелос Винарија (Ambelos Winery) | — | mesto | — |
| Трилогия Винария - Vinarija Trilogija | Oplenačko vinogorje | mesto | — |

### Toplički rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Doja | Prokupačko vinogorje | mesto | Топлица |
| Toplički Vinogradi | Prokupačko vinogorje | mesto | Топлица |
| Аранђеловић 1920 (Aranđelović 1920) | — | vivino | — |
| Костић (Kostić) | — | vinarijesrbije | — |

### Vranjski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Aleksić | — | mesto | Юго-восток |
