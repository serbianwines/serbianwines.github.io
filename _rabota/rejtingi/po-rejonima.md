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
| Vojvodina | Rejon Bačka | 8 | 12 | 0 | 1 |
| Vojvodina | Banatski rejon | 4 | 6 | 7 | 7 |
| Centralna Srbija | Beogradski rejon | 8 | 29 | 24 | 26 |
| Centralna Srbija | Čačansko–kraljevački rejon | 2 | 1 | 1 | 1 |
| Vojvodina | Južnobanatski rejon | 6 | 17 | 13 | 13 |
| Kosovo i Metohija | Južnometohijski rejon | 1 | 0 | 0 | 0 |
| Centralna Srbija | Knjaževački rejon | 4 | 20 | 4 | 5 |
| Centralna Srbija | Leskovački rejon | 4 | 3 | 0 | 0 |
| Centralna Srbija | Mlavski rejon | 3 | 14 | 46 | 44 |
| Centralna Srbija | Nišavski rejon | 1 | 2 | 1 | 1 |
| Centralna Srbija | Niški rejon | 3 | 10 | 0 | 0 |
| Centralna Srbija | Pocersko Valjevski Rejon | 3 | 21 | 4 | 4 |
| Vojvodina | Potiski rejon | 2 | 19 | 0 | 0 |
| Centralna Srbija | Rejon Negotinska Krajina | 17 | 52 | 79 | 59 |
| Vojvodina | Rejon Telečka | 1 | 2 | 0 | 0 |
| Centralna Srbija | Rejon Tri Morave | 36 | 157 | 149 | 140 |
| Vojvodina | Sremski rejon | 82 | 304 | 270 | 270 |
| Vojvodina | Subotički rejon | 14 | 90 | 116 | 96 |
| Centralna Srbija | Šumadijski rejon | 15 | 137 | 166 | 120 |
| Centralna Srbija | Toplički rejon | 4 | 22 | 33 | 25 |
| Centralna Srbija | Vranjski rejon | 2 | 16 | 39 | 40 |
| — | **рејон не установлен** | 254 | 255 | 45 | 57 |

**Рејоны, из которых не собралось ни одного хозяйства:** Severnometohijski rejon.


## Главы книги и рејоны

Столбец слева — глава книги, справа — в какие рејоны попадают её хозяйства по действующей рејонизацији.

| Глава книги | Рејоны её хозяйств |
|---|---|
| Фрушка гора | Sremski rejon — 20; не установлен — 2 |
| Суботичко-Хоргошская пешчара | Subotički rejon — 4 |
| Банат | Južnobanatski rejon — 1; Potiski rejon — 1; не установлен — 1 |
| Шумадия | Šumadijski rejon — 6; не установлен — 1; Rejon Tri Morave — 1 |
| Три Моравы и Жупа | Rejon Tri Morave — 9; не установлен — 2; Sremski rejon — 1 |
| Неготинска Крайина | Rejon Negotinska Krajina — 3 |
| Топлица | Toplički rejon — 2 |
| Юго-восток | Knjaževački rejon — 2; Vranjski rejon — 1; Niški rejon — 1 |
| Подунавье и Белградский район | не установлен — 1; Beogradski rejon — 1 |
| Косово и Метохия | не установлен — 1 |

**Рејоны, где хозяйства есть, а в книге их нет:**

- **Rejon Bačka** (Vojvodina) — 117 Wine, Dimalis, Fekete, Sila, Tri Međe I Oblak, Vinarija Baza, Vinarija Mrđanin, Vindulo
- **Banatski rejon** (Vojvodina) — Galot, Salaš Gnezdo Doo Bečej, Vinarija Sočanski, Драгић Винарија (Vina Dragic)
- **Čačansko–kraljevački rejon** (Centralna Srbija) — Vinarija Tomić - Rošci, Винарија Ступови (Vinarija Stupovi)
- **Južnometohijski rejon** (Kosovo i Metohija) — Podrum Lukic
- **Leskovački rejon** (Centralna Srbija) — Prima, Vinarija Aquila, Козарак, Митровиђ Винарија
- **Mlavski rejon** (Centralna Srbija) — Pruna, Virtus, Virtus W
- **Nišavski rejon** (Centralna Srbija) — Vinarija Savic
- **Pocersko Valjevski Rejon** (Centralna Srbija) — Andrića Vinograd, Milijan Jelić, Pusula
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
| Vinarija Mrđanin | — | vivino | — |
| Vindulo | — | vinarijesrbije+vivino | — |

### Banatski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Galot | — | mesto | — |
| Salaš Gnezdo Doo Bečej | — | decanter | — |
| Vinarija Sočanski | — | vinarijesrbije | — |
| Драгић Винарија (Vina Dragic) | — | decanter | — |

### Beogradski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Plavinci | Gročansko vinogorje | mesto | — |
| Podrum Janko | Smederevsko vinogorje | mesto | — |
| Vinarija Jeremic | — | decanter+vinarijesrbije | — |
| Vinarija Milićević | Avalsko-kosmajsko vinogorje | mesto | — |
| Vinarija Milojević | Lazarevačko vinogorje | mesto | — |
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
| Rnjak | Vršačko vinogorje | mesto | — |
| Vinarija Aleksandar | — | vinarijesrbije | — |
| Vinarija Nedin | Vršačko vinogorje | mesto | — |
| Vinarija Rajić | — | decanter | — |
| Vinik | — | vinarijesrbije | — |

### Južnometohijski rejon — Kosovo i Metohija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Podrum Lukic | — | vinarijesrbije | — |

### Knjaževački rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dzervin | — | vivino | Юго-восток |
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
| Virtus | — | bolshinstvo | — |
| Virtus W | — | decanter | — |

### Nišavski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Savic | — | bolshinstvo | — |

### Niški rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Podrum Malča | Čegarsko vinogorje | mesto | Юго-восток |
| Vinarija 100 Žena | Čegarsko vinogorje | mesto | — |
| Виница Грковић (Vinica Grković) | — | vivino | — |

### Pocersko Valjevski Rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Andrića Vinograd | — | vivino | — |
| Milijan Jelić | — | vinarijesrbije+vivino | — |
| Pusula | Podgorsko vinogorje | mesto | — |

### Potiski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Vinarija Coka | Severnopotisko vinogorje | mesto | Банат |
| Vinartos Vinarija | — | vivino | — |

### Rejon Negotinska Krajina — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Dalia | — | vivino | — |
| Francuska Vinarija - Estelle et Cyrille Bongiraud | — | vivino | — |
| Manastir Bukovo | — | decanter | Неготинска Крайина |
| Manastira Bukovo | — | decanter | — |
| Matalj | Negotinsko vinogorje | mesto | Неготинска Крайина |
| Matalj Vainarija | — | decanter | — |
| Tenuta Est Winery | — | vivino | — |
| Traško Vinarija | — | decanter+vivino | — |
| Vinarija Frunza Aglaja | — | decanter | — |
| Vinarija Gamanović | — | decanter+vivino | — |
| Vinarija Janucic | — | decanter+vivino | — |
| Vinarija Novak (Новак) | — | vivino | — |
| Vinarija Porta | — | vivino | — |
| Vinarija Raj | Negotinsko vinogorje | mesto | Неготинска Крайина |
| Vinarija Timahus | — | vivino | — |
| ΒИММИД ΒИΗΑΡИЈΑ (Vimmid Winery) | — | decanter+vivino | — |
| Винарија Манастира Буково | — | vivino | — |

### Rejon Telečka — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Milisavljević | — | vinarijesrbije | — |

### Rejon Tri Morave — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Adora | Jagodinsko vinogorje | decanter | — |
| Aleksandar Todorović | — | vivino | — |
| Bacina Vino | Kruševačko vinogorje | decanter | — |
| Botunjac | — | vivino | — |
| Cilić | — | vivino | Три Моравы и Жупа |
| Cvetković Vinarija | — | mesto | — |
| Grabak | Kruševačko vinogorje | decanter | — |
| Ivanović | Kruševačko vinogorje | decanter+vinarijesrbije+vivino | Три Моравы и Жупа |
| Marko | Trsteničko vinogorje | mesto | Шумадия |
| Milan Nikolić | Jagodinsko vinogorje | decanter | — |
| Pet Hrastova | — | mesto | — |
| Podrum Bačina | Kruševačko vinogorje | decanter | — |
| Podrum Pevac | Jagodinsko vinogorje | decanter | — |
| Radovan | — | vinarijesrbije | — |
| Ralević | — | mesto | Три Моравы и Жупа |
| Rubin | Kruševačko vinogorje | mesto | Три Моравы и Жупа |
| Stemina | Kruševačko vinogorje | decanter+vivino | — |
| Temet | Jagodinsko vinogorje | decanter+vivino | Три Моравы и Жупа |
| Varina | — | vivino | — |
| Vert | — | vivino | — |
| Vila Vina | — | vivino | — |
| Vinarija Bora | — | vivino | — |
| Vinarija Fragaria | Župsko vinogorje | mesto | — |
| Vinarija Jovac | Jagodinsko vinogorje | decanter+vivino | Три Моравы и Жупа |
| Vinarija Lastar | Jagodinsko vinogorje | decanter | — |
| Vinarija Manastira Studenica | Kruševačko vinogorje | decanter | — |
| Vinarija Mozaik Milan | — | vivino | — |
| Vinarija Smiljković 90 | — | vivino | — |
| Vinarija Venčac | Jagodinsko vinogorje | decanter | — |
| Vinarija Vinis | Jagodinsko vinogorje | decanter | — |
| Vino Budimir | — | vivino | — |
| Vinska Kuća Milinčić | — | vivino | — |
| Vujić | — | vinarijesrbije | Три Моравы и Жупа |
| Yotta | — | mesto | Три Моравы и Жупа |
| Čokot | Kruševačko vinogorje | decanter | Три Моравы и Жупа |
| Манастир Студеница (Manastir Studenica) | — | vivino | — |

### Sremski rejon — Vojvodina

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| 45. Paralela | Fruškogorsko vinogorje | mesto | — |
| Alchemy Winery | Fruškogorsko vinogorje | vivino | — |
| Art Et Vinum | Fruškogorsko vinogorje | mesto | — |
| Atelje Vina Šapat | Fruškogorsko vinogorje | vivino | — |
| Atos-Fructum | Fruškogorsko vinogorje | decanter | — |
| BT Winery | Fruškogorsko vinogorje | decanter | — |
| Bajilo | Fruškogorsko vinogorje | mesto | — |
| Belo Brdo | Fruškogorsko vinogorje | decanter+vinarijesrbije+vivino | Фрушка гора |
| Benišek Veselinović | Fruškogorsko vinogorje | mesto | — |
| Bikicki | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Bjelica | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Breg | Fruškogorsko vinogorje | mesto | — |
| Budimir | Fruškogorsko vinogorje | vinarijesrbije | Три Моравы и Жупа |
| Chardonnay | Fruškogorsko vinogorje | decanter | — |
| Chichateau | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Deurić | Fruškogorsko vinogorje | bolshinstvo | Фрушка гора |
| Do Kraja Sveta | Fruškogorsko vinogorje | vivino | — |
| Dragojlović Vinarija | Fruškogorsko vinogorje | vivino | — |
| Erdevik | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Fruškogorski | Fruškogorsko vinogorje | decanter | — |
| Gora | Fruškogorsko vinogorje | decanter | — |
| Hadži Popović | Fruškogorsko vinogorje | vivino | — |
| Imperator Vino | Fruškogorsko vinogorje | vivino | — |
| Kiš | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Kovačević | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Krstašica | Fruškogorsko vinogorje | decanter+vivino | — |
| Krstašica Doo | Fruškogorsko vinogorje | decanter | — |
| La Gora | Fruškogorsko vinogorje | decanter+vinarijesrbije+vivino | — |
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
| Patkov Vinograd | Fruškogorsko vinogorje | vivino | — |
| Petković Latin | Fruškogorsko vinogorje | vivino | — |
| Probus Vineyards | Fruškogorsko vinogorje | decanter | — |
| Probus Vineyards CCLXXX | Fruškogorsko vinogorje | decanter | — |
| Quet | Fruškogorsko vinogorje | decanter | — |
| Rittium | Fruškogorsko vinogorje | vivino | — |
| Salaxia | Fruškogorsko vinogorje | vivino | — |
| Teodora | Fruškogorsko vinogorje | vivino | — |
| The Sparkling Winery | Fruškogorsko vinogorje | decanter | — |
| Tri Medje I Oblak | Fruškogorsko vinogorje | decanter | — |
| Trivanović | Fruškogorsko vinogorje | decanter+vinarijesrbije+vivino | Фрушка гора |
| Veritas | Fruškogorsko vinogorje | mesto | — |
| Veritas Ćuković | Fruškogorsko vinogorje | decanter+vinarijesrbije+vivino | Фрушка гора |
| Verkat | Fruškogorsko vinogorje | decanter | Фрушка гора |
| Vinarija Acumincum | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarija Aven | Fruškogorsko vinogorje | bolshinstvo | — |
| Vinarija Brestovački | Fruškogorsko vinogorje | vivino | — |
| Vinarija Burma Fruška Gora | Fruškogorsko vinogorje | vivino | — |
| Vinarija Dosen | Fruškogorsko vinogorje | mesto | — |
| Vinarija Dumo | Fruškogorsko vinogorje | decanter | — |
| Vinarija Frug | Fruškogorsko vinogorje | decanter | — |
| Vinarija Grumen | Fruškogorsko vinogorje | vivino | — |
| Vinarija Imperator | Fruškogorsko vinogorje | decanter | — |
| Vinarija Komazec | Fruškogorsko vinogorje | decanter+vivino | — |
| Vinarija Komuna | Fruškogorsko vinogorje | mesto | — |
| Vinarija Kurjak | Fruškogorsko vinogorje | mesto | — |
| Vinarija MK Kosović | Fruškogorsko vinogorje | vivino | — |
| Vinarija Mrdjanin | Fruškogorsko vinogorje | decanter | — |
| Vinarija Podrum Danguba | Fruškogorsko vinogorje | mesto | — |
| Vinarija Sokolov Zamak | Fruškogorsko vinogorje | decanter | — |
| Vinarija Tanasković | Fruškogorsko vinogorje | vivino | — |
| Vinarija Đurđić | Fruškogorsko vinogorje | vivino | Фрушка гора |
| Vinarija Šijački | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Vinarium | Fruškogorsko vinogorje | mesto | — |
| Vinum | Fruškogorsko vinogorje | decanter+vivino | Фрушка гора |
| Vinčić | Fruškogorsko vinogorje | bolshinstvo | Фрушка гора |
| Vista Hill Plus | Fruškogorsko vinogorje | decanter | — |
| Vista Hills Plus | Fruškogorsko vinogorje | decanter | — |
| Winery Djurdjic | Fruškogorsko vinogorje | decanter | — |
| Šapat | Fruškogorsko vinogorje | mesto | Фрушка гора |
| Šveljo | Fruškogorsko vinogorje | vinarijesrbije | — |
| šApat Wine Atelier | Fruškogorsko vinogorje | decanter | — |
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
| Tonković | — | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Dragić | Riđičko vinogorje | mesto | — |
| Vinarija Petra | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |
| Vinarija Salaš Naš | — | vivino | — |
| Vinarija Zaba | Riđičko vinogorje | decanter | — |
| Vinski Dvor | — | vivino | — |
| Zvonko Bogdan | Palićko vinogorje | mesto | Суботичко-Хоргошская пешчара |

### Šumadijski rejon — Centralna Srbija

| Хозяйство | Виногорје | Откуда рејон | В книге |
|---|---|---|---|
| Aleksandrović | Oplenačko vinogorje | mesto | Шумадия |
| Château Prince | Oplenačko vinogorje | decanter | — |
| Despotika | Oplenačko vinogorje | bolshinstvo | Шумадия |
| Draganić | — | vinarijesrbije | Шумадия |
| Matijašević | Oplenačko vinogorje | mesto | Шумадия |
| PIK Oplenac | Oplenačko vinogorje | decanter | — |
| Podrum Stari Hrast | Oplenačko vinogorje | decanter | — |
| Radovanović | Krnjevačko vinogorje | mesto | Шумадия |
| Tarpoš | Oplenačko vinogorje | mesto | Шумадия |
| Tref Line | Oplenačko vinogorje | decanter | — |
| Vinarija DeLena | Oplenačko vinogorje | decanter | — |
| Vinarija Eden | Oplenačko vinogorje | mesto | — |
| Vinarija Žir | Krnjevačko vinogorje | mesto | — |
| Vinogradi Veličković Vinarija | Oplenačko vinogorje | decanter | — |
| Zmajevac | Oplenačko vinogorje | decanter | — |

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
