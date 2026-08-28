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
| **vinarijesrbije.rs** | справочник винарий: рејон и город | 129 |
| **Decanter** | `region` + `subRegion` у каждого вина — единственный источник, доходящий до виногорја | 997 записей |
| **Vivino** | плоский `region` у вина, до виногорја не доходит | 2786 вин |
| **Falstaff** | область в печатном списке | 116 позиций |
| **книга** | город хозяйства в `raion-hozyaistv.json` | 32 |

Имена источников переводятся в официальные таблицей в `sobrat-rejony.py`.
Таблица явная, и это не занудство: часть имён у Vivino и Decanter осталась
от **старой рејонизације**, где рејонов было девять. «Šumadija-Great Morava»
покрывает нынешние Шумадијски, Београдски, Млавски и Три Мораве; «Nišava-South
Morava» — пять рејонов сразу. По таким именам рејон не ставится вовсе: лучше
пустое поле, чем правдоподобная выдумка.

## Как решается спор

Источники расходятся у полутора десятков хозяйств. Порядок такой:

1. **Место решает.** Если известен город и он однозначно лежит в одном
   рејоне — берётся он. Город точнее любого счёта записей.
2. **Подавляющее большинство.** Восемьдесят семь записей за Сремски рејон
   против одной за Суботички — это опечатка у источника, а не второе место
   работы хозяйства. Порог — вчетверо.
3. **Иначе рејон не ставится**, а расхождение записывается в
   `rejon_raznoglasie`, чтобы его было видно.

Виногорје из чужого рејона отбрасывается: у Savić рејон вышел Нишавски по
четырём записям, а виногорје — Опленачко по одной, и второе неверно.

**Пересобрать файл:**

    python3 _rabota/rejtingi/sobrat-rejony.py
    python3 _rabota/rejtingi/sobrat-tablicy.py
    python3 _rabota/rejtingi/svesti-rejony.py --otchet

<!-- Собрано скриптом svesti-rejony.py. Руками не править. -->

## Что собралось по рејонима

Хозяйства разложены по действующей рејонизацији: 3 региона, 22 рејона, 77 виногорја. Глава книги — отдельный столбец, она не обязана совпадать.

| Регион | Рејон | Хозяйств | Оценок Vivino | Оценок критиков | Наград |
|---|---|---|---|---|---|
| Vojvodina | Rejon Bačka | 7 | 5 | 0 | 1 |
| Vojvodina | Banatski rejon | 3 | 1 | 7 | 7 |
| Centralna Srbija | Beogradski rejon | 12 | 32 | 24 | 26 |
| Centralna Srbija | Čačansko–kraljevački rejon | 2 | 1 | 1 | 1 |
| Vojvodina | Južnobanatski rejon | 8 | 23 | 13 | 13 |
| Kosovo i Metohija | Južnometohijski rejon | 1 | 0 | 0 | 0 |
| Centralna Srbija | Knjaževački rejon | 4 | 20 | 4 | 5 |
| Centralna Srbija | Leskovački rejon | 4 | 3 | 0 | 0 |
| Centralna Srbija | Mlavski rejon | 3 | 14 | 46 | 44 |
| Centralna Srbija | Nišavski rejon | 1 | 2 | 1 | 1 |
| Centralna Srbija | Niški rejon | 3 | 10 | 0 | 0 |
| Centralna Srbija | Pocersko Valjevski Rejon | 5 | 24 | 9 | 9 |
| Vojvodina | Potiski rejon | 3 | 19 | 0 | 0 |
| Centralna Srbija | Rejon Negotinska Krajina | 17 | 52 | 79 | 59 |
| Vojvodina | Rejon Telečka | 1 | 2 | 0 | 0 |
| Centralna Srbija | Rejon Tri Morave | 46 | 181 | 145 | 137 |
| Vojvodina | Sremski rejon | 86 | 310 | 269 | 269 |
| Vojvodina | Subotički rejon | 14 | 90 | 116 | 96 |
| Centralna Srbija | Šumadijski rejon | 23 | 164 | 172 | 128 |
| Centralna Srbija | Toplički rejon | 4 | 22 | 33 | 25 |
| Centralna Srbija | Vranjski rejon | 2 | 16 | 39 | 40 |
| — | **рејон не установлен** | 223 | 195 | 39 | 48 |

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

- **Rejon Bačka** (Vojvodina) — 117 Wine, Dimalis, Fekete, Sila, Tri Međe I Oblak, Vinarija Baza, Vindulo
- **Banatski rejon** (Vojvodina) — Salaš Gnezdo Doo Bečej, Vinarija Sočanski, Драгић Винарија (Vina Dragic)
- **Čačansko–kraljevački rejon** (Centralna Srbija) — Vinarija Tomić - Rošci, Винарија Ступови (Vinarija Stupovi)
- **Južnometohijski rejon** (Kosovo i Metohija) — Podrum Lukic
- **Leskovački rejon** (Centralna Srbija) — Prima, Vinarija Aquila, Козарак, Митровиђ Винарија
- **Mlavski rejon** (Centralna Srbija) — Pruna, Virtus, Virtus W
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
| Tri Međe I Oblak | — | vivino | — |
| Vinarija Baza | — | vivino | — |
| Vindulo | — | mesto | — |

### Banatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Salaš Gnezdo Doo Bečej | — | decanter | — |
| Vinarija Sočanski | — | vinarijesrbije | — |
| Драгић Винарија (Vina Dragic) | — | decanter | — |

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
| Podrum Džervin 1927 | — | decanter | — |
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
| Virtus W | — | decanter | — |

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
| Manastira Bukovo | — | decanter | — |
| Matalj | — | mesto | Неготинска Крайина |
| Matalj Vainarija | — | decanter | — |
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
| Bacina Vino | Kruševačko vinogorje | decanter | — |
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
| Vinarija Manastira Studenica | Kruševačko vinogorje | decanter | — |
| Vinarija Mozaik Milan | — | vivino | — |
| Vinarija Smiljković 90 | Župsko vinogorje | mesto | — |
| Vinarija Venčac | Jagodinsko vinogorje | decanter | — |
| Vinarija Vinis | Jagodinsko vinogorje | decanter | — |
| Vinarija Ćosić | Župsko vinogorje | mesto | — |
| Vino Budimir | Župsko vinogorje | mesto | — |
| Vinska Kuća Milinčić | — | vivino | — |
| Vinska Kuća Minića | Župsko vinogorje | mesto | — |
| Vujić | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Yotta | — | mesto | Три Моравы и Жупа |
| Zupa | Župsko vinogorje | mesto | Три Моравы и Жупа |
| Čokot | Kruševačko vinogorje | decanter | Три Моравы и Жупа |
| Žarković | Župsko vinogorje | mesto | — |
| Винарија Живковић (Vinarija Živković) | Župsko vinogorje | mesto | — |
| Манастир Студеница (Manastir Studenica) | — | vivino | — |
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
| Chardonnay | Fruškogorsko vinogorje | decanter | — |
| Chichateau | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Deurić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Do Kraja Sveta | Fruškogorsko vinogorje | vivino | — |
| Dragojlović Vinarija | Fruškogorsko vinogorje | vivino | — |
| Dulka | Fruškogorsko vinogorje | mesto | — |
| Erdevik | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Fruškogorski | Fruškogorsko vinogorje | mesto | — |
| Gora | Fruškogorsko vinogorje | decanter | — |
| Hadži Popović | Fruškogorsko vinogorje | vivino | — |
| Imperator Vino | Fruškogorsko vinogorje | vivino | — |
| Kiš | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Kovačević | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Krstašica | Fruškogorsko vinogorje | decanter+vivino | — |
| Krstašica Doo | Fruškogorsko vinogorje | decanter | — |
| La Gora | Fruškogorsko vinogorje | mesto | — |
| La Grande Bellezza | Fruškogorsko vinogorje | decanter | — |
| Mackov Podrum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Manufaktura Spasić | Fruškogorsko vinogorje | decanter | — |
| McCulloch | Fruškogorsko vinogorje | decanter+vivino | — |
| Mcculloch Wines | Fruškogorsko vinogorje | decanter | — |
| Milanović | Fruškogorsko vinogorje | mesto | — |
| Mister | Fruškogorsko vinogorje | decanter | — |
| Molovin | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Molowinery | Fruškogorsko vinogorje | decanter | — |
| Nera | Fruškogorsko vinogorje | vivino | — |
| Patkov Vinograd | Fruškogorsko vinogorje | mesto | — |
| Petković Latin | Fruškogorsko vinogorje | vivino | — |
| Podrum Probus | Fruškogorsko vinogorje | mesto | — |
| Podrum Stojković | Fruškogorsko vinogorje | mesto | — |
| Probus Vineyards | Fruškogorsko vinogorje | decanter | — |
| Probus Vineyards CCLXXX | Fruškogorsko vinogorje | decanter | — |
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
| Vinarija Mrdjanin | Fruškogorsko vinogorje | decanter | — |
| Vinarija Mrđanin | Fruškogorsko vinogorje | mesto | — |
| Vinarija Podrum Danguba | Fruškogorsko vinogorje | mesto | — |
| Vinarija Sokolov Zamak | Fruškogorsko vinogorje | mesto | — |
| Vinarija Tanasković | Fruškogorsko vinogorje | vivino | — |
| Vinarija Đurđić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Šijački | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarium | Fruškogorsko vinogorje | mesto | — |
| Vinum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinčić | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vista Hill Plus | Fruškogorsko vinogorje | decanter | — |
| Vista Hills Plus | Fruškogorsko vinogorje | decanter | — |
| Winery Djurdjic | Fruškogorsko vinogorje | decanter | — |
| Šapat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Šveljo | Fruškogorsko vinogorje | vinarijesrbije | — |
| Živanović | Fruškogorsko vinogorje | mesto | Фрушка гора |
| ВИНАРИЈА СТОЈАНОВИЋ (Vinarija Stojanović) | Fruškogorsko vinogorje | mesto | — |

### Subotički rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Bogdan | — | decanter | — |
| Dibonis Winery | — | decanter+vivino | — |
| Maurer | — | vivino | Суботичко-Хоргошская пешчара |
| Max-Ex Doo | — | decanter | — |
| Porodična Vinarija Stanimirović | — | vivino | — |
| Reljić Vinarija | — | decanter | — |
| The Collective Presents | — | vivino | — |
| Tonković | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Dragić | Riđičko vinogorje | mesto | — |
| Vinarija Petra | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Salaš Naš | Horgoško vinogorje | mesto | — |
| Vinarija Zaba | Riđičko vinogorje | decanter | — |
| Vinski Dvor | — | vivino | — |
| Zvonko Bogdan | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |

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
| Winery Aleksić Doo | — | decanter | — |
