# Рейтинги вин: по стране и по главам

Четыре способа спросить «какое вино лучше», и они дают разные ответы.
Это проверено, а не предположено: в сильных главах пятнадцать мест трёх
пятёрок занимают тринадцать-пятнадцать **разных** вин, пересечения — ноль
или одно вино.

| Дорожка | Что ранжирует | Чему верить |
|---|---|---|
| **олимпиадный зачёт** | очки медалей: строгость конкурса × ступень | постоянству: вино, берущее серебро четыре года подряд |
| **мнение экспертов** | лучший балл по стобалльной шкале | одному дегустатору в один день |
| **vox populi** | оценка Vivino при выборке от 25 отзывов | тому, что бутылку купили и допили |
| **согласие трёх** | худший из трёх процентилей главы | только тому, с чем согласны все трое |

**Почему у сводной худший процентиль, а не средний.** «И жюри, и критик,
и покупатель хороши» — утверждение о согласии. Вино, стоящее первым
у критиков и сороковым у покупателей, согласием не является, а среднее
это прячет. В сводную идут только вина, у которых есть все три сигнала;
где такого нет, дорожки нет — и это тоже сведение о районе.

**Веса конкурсов измерены, а не назначены** — по доле золота и выше среди
их собственных наград: у Decanter 4%, у венского AWC 17%, у софийского
BIWC 31%, у Berliner и Asia Wine Trophy 86%. Отсюда Decanter ×3,
AWC, IWC и Concours Mondial ×2, BIWC и Wine Trophy ×1. Ступени: Best in
Show 6, платина и гран-золото 5, золото 4, серебро 2, бронза 1,
«отмечено» 0,5.

**Шкалы не смешиваются.** Первая редакция этого отчёта переводила оценку
Vivino в стобалльную, когда балла критика не было, — и ставила вино,
которого не судил никто, выше золота Decanter. Пересчёт убран: у критиков
свой ряд, у покупателей свой.

**«За свои деньги» — это не «дёшево и хорошо».** Первая редакция этого
отчёта считала так и звала список «топ за свои деньги», а на деле там
стояли просто лучшие из тех, кто дешевле двух тысяч. Теперь цена
переводится в ожидаемый балл, и вино оценивается превышением над
ожиданием — «дороже своей цены». Отдельно осталась и таблица по потолку:
это ответ на другой вопрос, «что взять сегодня на две тысячи».

**Потолок — два вина на хозяйство.** Без него пятёрка района становится
витриной одного дома: у Александровића хватит вин на всю Шумадију.

**Печатается десятка, а не пятёрка.** Первые пять — сама пятёрка,
остальные скамейка: фактчек выбивает вино, следующее поднимается,
и видно, сколько запаса осталось на самом деле.

## Главы

Главы — по действующей рејонизацији, а слабые рејоны собраны под
географическим зонтиком. Приём не выдуман: книга уже так устроена —
восемь её глав из десяти это ровно один рејон, а «Банат» и «Юго-восток»
как раз зонтики. Разбор и числа — в `perestrojka-glav.md`.

Чачанско-краљевачки рејон стоит в Трем Моравама: Западна Морава — одна
из трёх Морава, и Трстеник с Краљевом лежат на ней же.

Тройка по цвету печатается там, где она есть. Розе набирается не везде,
и выдумывать его для полноты таблицы незачем: отсутствие — тоже ответ.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-rejtingi.py --otchet

<!-- Собрано скриптом svesti-rejtingi.py. Руками не править. -->

# По стране целиком

Здесь районы соревнуются друг с другом, а не каждый сам с собой.


## Супервина: десятка лучших без оглядки на цену

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 97 | — | 15 | — |
| Deurić · La Rem Chardonnay | 97 | — | 21 | 4025 |
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 | 4550 |
| Matalj · Kremen Kamen | 97 | — | 54 | 9191 |
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 | — |
| Vinčić · Grašac | 97 | 4.3 | 38 | 17385 |
| Arsenijević · Kaberne | 96 | — | 5 | — |
| Bikicki · Uncensored | 96 | 4.0 | 54 | 2871 |
| Ivanović · Prokupac Gaga | 96 | — | — | — |
| La Gora · Aria | 96 | — | 5 | — |

## Красные: пятёрка страны

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 97 | — | 15 | — |
| Matalj · Kremen Kamen | 97 | — | 54 | 9191 |
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 | — |
| Arsenijević · Kaberne | 96 | — | 5 | — |
| Aleksandrović · Regent Reserve | 95 | 4.2 | 72 | 2158 |

## Белые: пятёрка страны

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Deurić · La Rem Chardonnay | 97 | — | 21 | 4025 |
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 | 4550 |
| Vinčić · Grašac | 97 | 4.3 | 38 | 17385 |
| Bikicki · Uncensored | 96 | 4.0 | 54 | 2871 |
| La Gora · Aria | 96 | — | 5 | — |

## Розе: пятёрка страны

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Budimir · Svb Rosa | 94 | 4.2 | — | 4410 |
| Zvonko Bogdan · Rosé Sec | 92 | 4.0 | 44 | 1680 |
| Doja · Rose | 91 | 3.5 | 5 | 1070 |
| Verkat · Roze | 91 | 3.9 | 8 | — |
| Vinska Kuća Rajić · Rosé | 91 | — | 9 | — |

## Vox populi: десятка по оценке покупателей

Шкала Vivino своя и в стобалльную не переводится, поэтому покупательский ряд стоит отдельно, а не подмешан к баллам критиков.

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Vinis · Crveno Vino | 84 | 4.6 | 2 | — |
| Aleksandrović · Vožd Cabernet Sauvignon | 95 | 4.5 | 18 | — |
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 | — |
| Stemina winery · Draga | 94 | 4.5 | 6 | — |
| Tri Oraha · 750 Barrique Barrels | — | 4.5 | — | 7365 |
| Aleksandrović · Rodoslov Grand Reserve | 94 | 4.4 | 64 | 4642 |
| Atelje vina Šapat · Àkcent Réserve | — | 4.4 | — | — |
| Bjelica · Babaroga Chardonnay | — | 4.4 | — | 5016 |
| Bjelica · Babaroga Crvena | — | 4.4 | — | 6750 |
| Braća Rajković · 33 Red | — | 4.4 | — | — |

## Лучше, чем за них просят

Здесь не «дёшево и хорошо», а «дороже своей цены». Цена переводится в ожидаемый балл, и вино оценивается превышением над ожиданием. Ожидание плоское: удвоение цены обещает всего 1.0 балла, связь слабая (коэффициент 0.28 по 290 винам, разброс остатка 2.8 балла). Это и есть главный вывод: **в Сербии цена почти не предсказывает качество**, и покупать по ценнику здесь бессмысленнее, чем где-либо.

Второй голос здесь — сам `vino.rs`: у него есть своя категория «за свои деньги», и её отметка вино в ряду поднимает. Столбец «vino.rs» показывает лучшее место и год; в порядке ряда отметка стоит +2.0 балла остатка за первую тройку и +1.0 за прочие места десятки — ровно столько, на сколько такие вина в среднем и превышают ожидание по цене. Столбец «сверх ожидания» при этом остаётся чистым измерением, без надбавки.

| Вино | Сверх ожидания | vino.rs | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|---|---|
| Doja · Prokupac | +5.4 | 1-е, 2024 | 95 | 3.9 | 70 | 1460 |
| Vinum · Grašac Beli | +5.2 | 1-е, 2020 | 95 | 3.9 | 48 | 1630 |
| Jović · Vranac Potrkanjski | +4.2 | 1-е, 2025 | 94 | — | 24 | 1635 |
| Erdevik · Trianon | +4.1 | 2-е, 2023 | 94 | 4.1 | 12 | 1774 |
| Deurić · La Rem Chardonnay | +5.9 | — | 97 | — | 21 | 4025 |
| Aleksandrović · Regent Reserve | +4.8 | 4-е, 2019 | 95 | 4.2 | 72 | 2158 |
| Erdevik · Omnibus Lector Chardonnay | +5.7 | — | 97 | 4.3 | 66 | 4550 |
| Virtus · Morava | +5.6 | — | 95 | 3.9 | 16 | 1310 |
| Virtus · Pinot Grigio | +3.5 | 3-е, 2022 | 93 | 3.8 | 33 | 1360 |
| Bikicki · Uncensored | +5.4 | — | 96 | 4.0 | 54 | 2871 |

Хвост того же ряда — вино, которое просит больше, чем даёт:

| Вино | Сверх ожидания | vino.rs | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|---|---|
| Fruškogorski · Tri Sunca Traminac Kasna Berba | -8.8 | — | 84 | — | 2 | 13005 |
| Lakićević · Upupa | -8.3 | — | 82 | — | 4 | 2282 |
| Lakićević · Merula | -7.0 | — | 84 | — | 14 | 3762 |
| Arsenijević · Starosedelac | -6.7 | — | 83 | — | 1 | 1619 |
| Lakićević · Solaris | -6.6 | — | 84 | 4.2 | 5 | 2952 |

## Если в кармане 2000 динаров

Другой вопрос и другой ответ: не «что выгодно», а «что взять сегодня». Цена известна у 290 отобранных вин, медиана 1834 динара.

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Doja · Prokupac | 95 | 3.9 | 70 | 1460 |
| Vinum · Grašac Beli | 95 | 3.9 | 48 | 1630 |
| Virtus · Morava | 95 | 3.9 | 16 | 1310 |
| Zvonko Bogdan · Chardonnay | 95 | 4.0 | 58 | 2000 |
| Erdevik · Trianon | 94 | 4.1 | 12 | 1774 |
| Ivanović · Prokupac | 94 | 3.9 | 38 | 1640 |
| Jović · Vranac Potrkanjski | 94 | — | 24 | 1635 |
| Verkat · Malvazija | 94 | 3.8 | 16 | 1606 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 | 1399 |
| Deurić · Aksiom | 93 | 4.1 | 39 | 1920 |

## Что взять в супермаркете

Полка супермаркета — не полка винотеки. Медиана бутылки 0,75 на полках Idea и Maxi — 1350 динаров против 1782 у винотек. Из 887 обычных бутылок с нашими таблицами сошлись 130, и 53 из этих 130 в винотеке нет вовсе. Вот те, о которых есть что сказать.

Дешевле там, однако, не то же вино, а другое. Из 77 вин, которые продаются и в супермаркете, и в винотеке, дешевле в супермаркете 4: одна и та же бутылка на полке стоит в среднем на 19% дороже. В супермаркет идут не за скидкой на знакомое вино, а за тем, чего в винотеке нет.

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Doja · Prokupac | 95 | 3.9 | 70 | 1579 |
| Zvonko Bogdan · Chardonnay | 95 | 4.0 | 58 | 2470 |
| Matijašević Vinogradi · SoviNoa | 95 | — | 15 | 2769 |
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 | 3800 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 | 1399 |
| Verkat · Malvazija | 94 | 3.8 | 16 | 1450 |
| Ivanović · Prokupac | 94 | 3.9 | 38 | 1999 |
| Erdevik · Trianon | 94 | 4.1 | 12 | 2459 |
| Ivanović · No 1/2 | 94 | 4.3 | 46 | 4369 |
| Temet · Ergo | 94 | — | 70 | 4369 |
| Deurić · Severna Morava | 93 | 3.9 | 38 | 1699 |
| Matijašević Vinogradi · Belina | 93 | 3.9 | 34 | 1919 |

## То же, по мнению покупателей

Тот же потолок, но ряд строит выборка Vivino. Ряд нужен отдельно: дешёвое вино на конкурс возят редко, и таблица выше молчит как раз о самых ходовых бутылках.

| Вино | Критик | Vivino | Медали | Динаров |
|---|---|---|---|---|
| Aleksandrović · Prokupac | 92 | 4.2 | 24 | 1770 |
| Draganić · Silueta Sauvignon Blanc | — | 4.2 | — | 1667 |
| Lastar · Tamjanika | 90 | 4.2 | 32 | 1740 |
| MV Vinarija · Tamjanika | — | 4.2 | 18 | 1730 |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 90 | 4.2 | 9 | 1910 |
| Manastir Bukovo · Filigran Merlot | 87 | 4.2 | 3 | 1500 |
| Vinarija 100 Žena · Monsieur Merlot Premium | — | 4.2 | — | 1440 |
| Vinarija DeLena · 70/30 Sauvignon Blanc - Sémillon | 90 | 4.2 | — | 1775 |
| Aleksić · Žuti Cvet | 87 | 4.1 | 14 | 1187 |
| Arsenijević · Merlot | — | 4.1 | — | 1707 |

# По главам


## Фрушка гора (Срем)

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 |
| Bikicki · Uncensored | 96 | 4.0 | 54 |
| Vinum · Grašac 26a | 94 | 4.0 | 50 |
| Vinum · Grašac Beli | 95 | 3.9 | 48 |
| Erdevik · Stifler's Mom Shiraz | 95 | 4.3 | 42 |
| Vinarija Dumo · Pinot Noir | 90 | 3.9 | 40 |
| Deurić · Aksiom | 93 | 4.1 | 39 |
| Vinčić · Grašac | 97 | 4.3 | 38 |
| Deurić · Severna Morava | 93 | 3.9 | 38 |
| Veritas Ćuković · Momentum Cabernet Sauvignon | 95 | 4.4 | 36 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Deurić · La Rem Chardonnay | 97 | — | 21 |
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 |
| Vinčić · Grašac | 97 | 4.3 | 38 |
| Bikicki · Uncensored | 96 | 4.0 | 54 |
| La Gora · Aria | 96 | — | 5 |
| Atelje vina Šapat · Atila Chardonnay | 95 | 4.3 | 35 |
| BT Winery · King Supreme Limited Edition Marselan | 95 | 4.3 | 12 |
| BT Winery · Mister Marselan | 95 | 4.1 | 22 |
| Chichateau · Chi Chardonnay | 95 | 4.2 | 6 |
| Erdevik · Marlon Delon Cabernet Sauvignon - Merlot | 95 | 4.3 | 24 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Atelje vina Šapat · Àkcent Réserve | — | 4.4 | — |
| Bjelica · Babaroga Chardonnay | — | 4.4 | — |
| Bjelica · Babaroga Crvena | — | 4.4 | — |
| Veritas Ćuković · Momentum Cabernet Sauvignon | 95 | 4.4 | 36 |
| Atelje vina Šapat · Atila Chardonnay | 95 | 4.3 | 35 |
| BT Winery · King Supreme Limited Edition Marselan | 95 | 4.3 | 12 |
| Dukay-Sagmeister · ZZ Zero | — | 4.3 | — |
| Erdevik · Grand Trianon | 93 | 4.3 | 20 |
| Erdevik · Marlon Delon Cabernet Sauvignon - Merlot | 95 | 4.3 | 24 |
| Manufaktura Spasić · Tamjanika | — | 4.3 | — |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 |
| Erdevik · Stifler's Mom Shiraz | 95 | 4.3 | 42 |
| Vinčić · Grašac | 97 | 4.3 | 38 |
| Veritas Ćuković · Momentum Cabernet Sauvignon | 95 | 4.4 | 36 |
| Atelje vina Šapat · Atila Chardonnay | 95 | 4.3 | 35 |
| Deurić · Aksiom | 93 | 4.1 | 39 |
| Vinarija Frug · Chardonnay Signum | 92 | 4.3 | 31 |
| BT Winery · Mister Marselan | 95 | 4.1 | 22 |
| Veritas Ćuković · Momentum | 95 | 4.3 | 21 |
| Bikicki · Uncensored | 96 | 4.0 | 54 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| BT Winery · King Supreme Limited Edition Marselan | 95 | 4.3 | 12 |
| BT Winery · Mister Marselan | 95 | 4.1 | 22 |
| Erdevik · Marlon Delon Cabernet Sauvignon - Merlot | 95 | 4.3 | 24 |
| Erdevik · Stifler's Mom Shiraz | 95 | 4.3 | 42 |
| Veritas Ćuković · Momentum | 95 | 4.3 | 21 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Deurić · La Rem Chardonnay | 97 | — | 21 |
| Erdevik · Omnibus Lector Chardonnay | 97 | 4.3 | 66 |
| Vinčić · Grašac | 97 | 4.3 | 38 |
| Bikicki · Uncensored | 96 | 4.0 | 54 |
| La Gora · Aria | 96 | — | 5 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Verkat · Roze | 91 | 3.9 | 8 |
| Atelje vina Šapat · šU-šU Blaufrankisch | 90 | — | 6 |
| Erdevik · Nostra | 90 | — | 6 |
| Vinarija Ilić-Nijemčević · IG | 90 | — | 13 |
| Vinarium winery · Pinoranž | 89 | 3.7 | 20 |


## Суботичко-хоргошка пешчара

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 |
| Zvonko Bogdan · Icon Campana Rubimus | 95 | 4.3 | 68 |
| Драгић Винарија (Vina Dragic) · Carski Drum Manzoni | 90 | — | 21 |
| Драгић Винарија (Vina Dragic) · Crni Biser | 94 | — | 21 |
| Maurer · Kadarka 1880 | — | — | 20 |
| DiBonis Winery · Di Icewine | 94 | — | 20 |
| Tonković · Fantazija | 91 | — | 19 |
| Maurer · Orion | — | 4.0 | 18 |
| Tonković · Rapsodija | 92 | — | 16 |
| Vinarija VRT · Pesak Sivi | 85 | 3.6 | 13 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Maurer · Kadarka 1880 (натуральное) | 95 | — | — |
| Reljić Vinarija · Rebus Merlot-Cabernet Sauvignon-Probus | 95 | — | 12 |
| Zvonko Bogdan · Chardonnay | 95 | 4.0 | 58 |
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 |
| DiBonis Winery · Di Icewine | 94 | — | 20 |
| Драгић Винарија (Vina Dragic) · Crni Biser | 94 | — | 21 |
| Tonković · Rapsodija | 92 | — | 16 |
| Vinarija Petra · Pinot Grigio Orange | 92 | — | — |
| Vinarija Petra · Pinot Noir Barrique | 92 | 3.9 | — |
| Reljić Vinarija · Rebus Reserve | 91 | — | 6 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Petra · Traminac Late Harvest | — | 4.4 | — |
| Maurer · Kadarka Gravitation | — | 4.3 | — |
| Zvonko Bogdan · Icon Campana Rubimus | 95 | 4.3 | 68 |
| DiBonis Winery · 1697 | — | 4.2 | — |
| DiBonis Winery · Di Cabernet Sauvignon | — | 4.2 | — |
| Maurer · Kadarka Nagy-Krisztus | — | 4.2 | — |
| Reljić Vinarija · Rebus Crveno | 90 | 4.2 | 9 |
| Vinarija Petra · Cuvée | — | 4.2 | — |
| The Collective Presents · Kadarka 1880 | — | 4.1 | — |
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Zvonko Bogdan · Icon Campana Rubimus | 95 | 4.3 | 68 |
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 |
| Tonković · Rapsodija Kadarka | 90 | 3.9 | 12 |
| Tonković · Fantazija Kadarka | 91 | 3.8 | 10 |
| Reljić Vinarija · Rebus Crveno | 90 | 4.2 | 9 |
| Vinarija VRT · Pesak Plavi | 88 | 3.9 | 8 |
| Vinarija Petra · Pinot Noir | 90 | 3.7 | 2 |
| Vinarija Petra · Rose & Co | 90 | 3.7 | 2 |
| Vinarija VRT · Pesak Sivi | 85 | 3.6 | 13 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Reljić Vinarija · Rebus Merlot-Cabernet Sauvignon-Probus | 95 | — | 12 |
| Zvonko Bogdan · Cuvée No.1 | 95 | 4.1 | 100 |
| Zvonko Bogdan · Icon Campana Rubimus | 95 | 4.3 | 68 |
| Драгић Винарија (Vina Dragic) · Crni Biser | 94 | — | 21 |
| Tonković · Rapsodija | 92 | — | 16 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Zvonko Bogdan · Chardonnay | 95 | 4.0 | 58 |
| Zvonko Bogdan · Eclater Blanc De Blancs Extra Brut | 95 | — | 21 |
| DiBonis Winery · Di Icewine | 94 | — | 20 |
| Драгић Винарија (Vina Dragic) · Beli Biser | 91 | — | 6 |
| Vinarija Petra · Traminac | 90 | 4.0 | — |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Zvonko Bogdan · Rosé Sec | 92 | 4.0 | 44 |
| Драгић Винарија (Vina Dragic) · Mitra | 91 | — | 6 |
| Vinarija Petra · Rose | 89 | — | 2 |
| Vinarija VRT · ROSSE | 89 | — | 6 |
| Драгић Винарија (Vina Dragic) · Carski Drum | 84 | — | 2 |


## Банат

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Gnezdo · Belo | 90 | — | 21 |
| Rnjak · Chardonnay | 89 | 3.7 | 17 |
| Vinarija Drašković · Beli Pinot | 90 | 3.6 | 17 |
| Rnjak · Pinot Noir | 89 | 4.0 | 16 |
| Vinska Kuća Rajić · Tamjanika | 89 | 4.0 | 11 |
| Vinarija Coka · Grof Lederer Merlot | 85 | — | 11 |
| Vinarija Drašković · Mahago | 90 | 3.7 | 10 |
| Galot · Gala | — | — | 9 |
| Vinska Kuća Rajić · Rosé | 91 | — | 9 |
| Vinarija Sočanski · Classique Spiritoso Rizling Rajnski | 84 | — | 8 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Gnezdo · Sovinjon Kis | 94 | — | 5 |
| Vinarija Drašković · Mahago Frankovka | 92 | — | 7 |
| Vinarija Tri Tachke · Rezonanca | 91 | — | 4 |
| Vinska Kuća Rajić · Rosé | 91 | — | 9 |
| Vinarija Fleur D'Oranger · Grof Muskat Krokan | 91 | — | 6 |
| Rnjak · CUVEE DE RGNAC | 90 | — | 6 |
| Vinarija Drašković · Beli Pinot | 90 | 3.6 | 17 |
| Vinarija Gnezdo · Belo | 90 | — | 21 |
| Драгић Винарија (Vina Dragic) · Nemirac | 90 | — | 6 |
| Rnjak · Chardonnay | 89 | 3.7 | 17 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Rnjak · Merlot Limited Edition | — | 4.2 | — |
| Galot · Balerina | — | 4.1 | — |
| Vinarija Drašković · Muskat Otonel | 90 | 4.1 | 6 |
| Galot · Chardonnay | 87 | 4.0 | 2 |
| Rnjak · Pinot Noir | 89 | 4.0 | 16 |
| Vinska Kuća Rajić · Tamjanika | 89 | 4.0 | 11 |
| Vršački Vinogradi · Kvalitetno Muskat Ottonel | — | 4.0 | — |
| Vršački Vinogradi · Вршачкн Брег Вранац | — | 4.0 | — |
| Vinarija Coka · Kupianovo Vino | — | 4.0 | — |
| Vinarija Coka · Ždrepčeva Krv Forever | — | 4.0 | — |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Rnjak · Pinot Noir | 89 | 4.0 | 16 |
| Vinska Kuća Rajić · Tamjanika | 89 | 4.0 | 11 |
| Vinarija Drašković · Muskat Otonel | 90 | 4.1 | 6 |
| Rnjak · Chardonnay | 89 | 3.7 | 17 |
| Vinarija Drašković · Mahago | 90 | 3.7 | 10 |
| Vinarija ĐORĐE · Freska Bela | 89 | 3.7 | 6 |
| Драгић Винарија (Vina Dragic) · Aurora | 88 | 3.8 | 3 |
| Galot · Chardonnay | 87 | 4.0 | 2 |
| Vinarija Coka · Muštuluk Crveni | 86 | 3.5 | 5 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Drašković · Mahago Frankovka | 92 | — | 7 |
| Vinarija Tri Tachke · Rezonanca | 91 | — | 4 |
| Rnjak · CUVEE DE RGNAC | 90 | — | 6 |
| Vinarija Drašković · Frankovka Rezerva | 90 | — | 8 |
| Vinarija Gnezdo · Kadarka | 90 | — | 7 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Gnezdo · Sovinjon Kis | 94 | — | 5 |
| Vinarija Fleur D'Oranger · Grof Muskat Krokan | 91 | — | 6 |
| Vinarija Drašković · Beli Pinot | 90 | 3.6 | 17 |
| Vinarija Drašković · Muskat Otonel | 90 | 4.1 | 6 |
| Vinarija Gnezdo · Belo | 90 | — | 21 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinska Kuća Rajić · Rosé | 91 | — | 9 |
| Драгић Винарија (Vina Dragic) · Randes | 89 | — | 6 |
| Vinarija ĐORĐE · Freska Rose | 88 | — | 6 |
| Vinarija Gnezdo · Roze | 84 | — | 2 |


## Бачка

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vindulo d.o.o. · Mirna Bačka | 84 | — | 4 |
| Vinarija Baza · Barre | 88 | — | 2 |
| Vinarija Ždrnja · Grašac | 87 | — | 2 |
| Dimalis · Rosé | 85 | — | 2 |
| Dimalis · Sauvignon Blanc | 85 | — | 2 |
| Vinarija Baza · Baza-proseko | 81 | — | 1 |
| Vindulo d.o.o. · Eureka | — | — | 1 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Baza · Barre | 88 | — | 2 |
| Vinarija Ždrnja · Grašac | 87 | — | 2 |
| Dimalis · Rosé | 85 | — | 2 |
| Dimalis · Sauvignon Blanc | 85 | — | 2 |
| Vinarija Baza · Talični | 84 | — | 1 |
| Vindulo d.o.o. · Mirna Bačka | 84 | — | 4 |

**Vox populi** — не набирается: подходящих вин 2.

**Согласие трёх** — не набирается: подходящих вин 0.


## Три Мораве и Жупа

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Temet · Ergo | 94 | — | 70 |
| Temet · Tri Morave | 90 | 4.0 | 54 |
| Lastar · Chardonnay | 89 | 3.8 | 46 |
| Ivanović · No 1/2 | 94 | 4.3 | 46 |
| Ivanović · Prokupac | 94 | 3.9 | 38 |
| Jovac · Stella Noir | 95 | — | 36 |
| Grabak · Prokupac | 94 | — | 34 |
| Lastar · Tamjanika | 90 | 4.2 | 32 |
| Nikad Nije Kasno · Signature | 90 | 4.3 | 31 |
| Fragaria · Red | 91 | 4.4 | 24 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Ivanović · Prokupac Gaga | 96 | — | — |
| Grabak · Vivak Prokupac | 95 | 4.1 | 17 |
| Jovac · Stella Noir | 95 | — | 36 |
| Ralević · RaRa Tamjanika PETNAT | 95 | — | 7 |
| Temet · Tamjanika | 95 | — | — |
| Temet · Tri Morave Belo Reserve | 95 | — | — |
| Budimir · Svb Rosa | 94 | 4.2 | — |
| Grabak · Prokupac | 94 | — | 34 |
| Ivanović · No 1/2 | 94 | 4.3 | 46 |
| Podrum Pevac · GUŠT BARIK | 94 | — | 6 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinis · Crveno Vino | 84 | 4.6 | 2 |
| Stemina winery · Draga | 94 | 4.5 | 6 |
| Braća Rajković · 33 Red | — | 4.4 | — |
| Cilić · Merlot Manifest Grand Cur | — | 4.4 | — |
| Fragaria · Jagoda | 87 | 4.4 | 3 |
| Fragaria · Red | 91 | 4.4 | 24 |
| Stemina winery · Stephanos Cabernet Sauvignon | — | 4.4 | — |
| Temet · Three Morave Rezerva (Три Mораве Резерва) | — | 4.4 | — |
| Aleksandar Todorović · Ibis Crveni | — | 4.3 | 7 |
| Ivanović · No 1/2 | 94 | 4.3 | 46 |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Ivanović · No 1/2 | 94 | 4.3 | 46 |
| Fragaria · Red | 91 | 4.4 | 24 |
| Lastar · Tamjanika | 90 | 4.2 | 32 |
| Nikad Nije Kasno · Signature | 90 | 4.3 | 31 |
| Grabak · Vivak Prokupac | 95 | 4.1 | 17 |
| Lastar · Triangl Chardonnay | 90 | 4.0 | 28 |
| Temet · Tri Morave | 90 | 4.0 | 54 |
| Vinarija Radovan · Experiment Tamjanika | 92 | 4.0 | 11 |
| Temet · Ergo White | 89 | 4.0 | 32 |
| Ivanović · Prokupac | 94 | 3.9 | 38 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Grabak · Vivak Prokupac | 95 | 4.1 | 17 |
| Jovac · Stella Noir | 95 | — | 36 |
| Temet · Tri Morave Reserve | 95 | — | 54 |
| Grabak · Prokupac | 94 | — | 34 |
| Ivanović · No 1/2 | 94 | 4.3 | 46 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Podrum Pevac · GUŠT BARIK | 94 | — | 6 |
| Ralević · Virgo | 94 | — | 5 |
| Cilić · Onyx Blanc | 92 | 4.2 | — |
| Ivanović · No 3/4 Tamjanika | 92 | 4.2 | — |
| Ivanović · Tamjanika | 92 | 3.9 | 28 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Budimir · Svb Rosa | 94 | 4.2 | — |
| Temet · Ergo Rosé | 90 | — | 24 |
| Temet · Rose | 90 | — | 5 |
| Grabak · Prva Lasta Prokupac | 88 | — | 3 |
| Lastar · Rose | 86 | 3.8 | 11 |


## Шумадија

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksandrović · Regent Reserve | 95 | 4.2 | 72 |
| Aleksandrović · Rodoslov Grand Reserve | 94 | 4.4 | 64 |
| Despotika · Morava | 91 | — | 58 |
| Despotika · Beskraj | 90 | — | 48 |
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 96 | 4.3 | 40 |
| Matijašević Vinogradi · Belina | 93 | 3.9 | 34 |
| Tarpoš · Tamjanika | 90 | 3.9 | 23 |
| Tarpoš · Cabernet Sauvignon | 90 | 4.1 | 22 |
| Podrum Stari Hrast · Sauvignon Blanc | 90 | 3.8 | 20 |
| Radovanović · Rèserve Cabernet Sauvignon | 91 | 4.3 | 17 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 97 | — | 15 |
| Arsenijević · Kaberne | 96 | — | 5 |
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 96 | 4.3 | 40 |
| Aleksandrović · Regent Reserve | 95 | 4.2 | 72 |
| Despotika · Krunski Dokaz | 95 | — | 18 |
| Matijašević Vinogradi · SoviNoa | 95 | — | 15 |
| Tarpoš · Chardonnay Extra Brut | 95 | — | 15 |
| Tarpoš · Merlot | 95 | 4.0 | 17 |
| Despotika · Krunski Dokas (The Key Evidence) Grand Reserve | 93 | — | — |
| Eden · Velvet | 93 | 4.0 | 6 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksandrović · Vožd Cabernet Sauvignon | 95 | 4.5 | 18 |
| Aleksandrović · Rodoslov Grand Reserve | 94 | 4.4 | 64 |
| Draganić · Miracolo Sangiovese Superiore | — | 4.4 | — |
| Radovanović · Réserve Special Cabernet Sauvignon | — | 4.4 | — |
| Vinarija DeLena · 1903 Merlot | 92 | 4.4 | 3 |
| Vinarija DeLena · Kota 376 Malbec | — | 4.4 | — |
| Vinarija Vladimir · 1 Hektar | — | 4.4 | — |
| Despotika · Krunski Dokaz Grand Reserve | — | 4.3 | — |
| Despotika · Додир Мускат Отонел - Тамјаника (Dodir Muscat Ottonel - Тamjanika) | — | 4.3 | — |
| Draganić · Cavalier Cuvée | — | 4.3 | — |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksandrović · Rodoslov Grand Reserve | 94 | 4.4 | 64 |
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 96 | 4.3 | 40 |
| Aleksandrović · Regent Reserve | 95 | 4.2 | 72 |
| Matijašević Vinogradi · Sovinoa Sauvignon Blanc | 93 | 4.1 | 12 |
| Radovanović · Rèserve Cabernet Sauvignon | 91 | 4.3 | 17 |
| Château Prince · Velika Morava | 90 | 4.1 | 16 |
| Tarpoš · Cabernet Sauvignon | 90 | 4.1 | 22 |
| Tarpoš · Sauvignon Blanc | 90 | 4.1 | 11 |
| Vinarija Zmajevac · Cuvée | 90 | 4.3 | 9 |
| Vinarija Zmajevac · Prokupac | 90 | 4.1 | 9 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksandrović · Kameničarka Prokupac | 97 | — | 15 |
| Arsenijević · Kaberne | 96 | — | 5 |
| Aleksandrović · Regent Reserve | 95 | 4.2 | 72 |
| Despotika · Krunski Dokaz | 95 | — | 18 |
| Matijašević Vinogradi · Tri Doline | 95 | — | 16 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matijašević Vinogradi · Sovinoa Fumé Blanc | 96 | 4.3 | 40 |
| Matijašević Vinogradi · SoviNoa | 95 | — | 15 |
| Tarpoš · Chardonnay Extra Brut | 95 | — | 15 |
| Aleksandrović · Trijumf Gold | 94 | 4.2 | 60 |
| Aleksandrović · Trijumf Selection | 93 | 4.1 | 29 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Despotika · Nemir | 89 | — | 36 |
| PIK OPLENAC · Constanta Muse Rosé | 89 | 3.9 | — |
| Radovanović · Rosé | 89 | 3.9 | 4 |
| Djordjevic Estate Winery · Rosé | 88 | — | 2 |
| Matijašević Vinogradi · Rock & Rose | 87 | 4.0 | 7 |


## Неготинска Крајина

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Kremen Kamen | 97 | — | 54 |
| Matalj · Kremen | 92 | — | 52 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 |
| Vimmid · Cabernet Sauvignon | 89 | 3.9 | 10 |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 90 | 4.2 | 9 |
| Manastir Bukovo · Filigran Гаме | 92 | — | 9 |
| Traško Vinarija · Fabulous Cabernet Franc | 90 | 4.1 | 9 |
| Mikić · Chardonnay | 89 | — | 8 |
| Mikić · Crna Tamjanika | 88 | — | 8 |
| Traško Vinarija · Bagrina Edición Limitada | 92 | 3.9 | 6 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Kremen Kamen | 97 | — | 54 |
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 |
| Manastir Bukovo · Chardonnay Oaked | 92 | — | — |
| Manastir Bukovo · Filigran Гаме | 92 | — | 9 |
| Traško Vinarija · Bagrina Edición Limitada | 92 | 3.9 | 6 |
| Vimmid · Dentelle | 92 | — | 6 |
| Mikić · Crveno vino | 91 | — | 8 |
| Traško Vinarija · Fabulous Cabernet Franc | 90 | 4.1 | 9 |
| Mikić · Chardonnay | 89 | — | 8 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 |
| Tri Oraha · 750 Barrique Barrels | — | 4.5 | — |
| Tri Oraha · 500 Barrique Barrels | — | 4.4 | — |
| Vinarija Dajic · Gamay Barrique | — | 4.4 | — |
| Manastir Bukovo · Вез | 90 | 4.3 | — |
| Vimmid · Аглаjа Dentelle Cabernet Sauvignon | — | 4.3 | — |
| Manastir Bukovo · Chardonnay | 85 | 4.2 | 2 |
| Matalj · Zemna Reserva | 92 | 4.2 | 16 |
| Raj · Plot | — | 4.1 | 1 |
| Traško Vinarija · Fabulous Cabernet Franc | 90 | 4.1 | 9 |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 |
| Matalj · Zemna Reserva | 92 | 4.2 | 16 |
| Manastir Bukovo · Filigran Cabernet Sauvignon | 90 | 4.2 | 9 |
| Traško Vinarija · Fabulous Cabernet Franc | 90 | 4.1 | 9 |
| Traško Vinarija · Bagrina Edición Limitada | 92 | 3.9 | 6 |
| Vimmid · Cabernet Sauvignon | 89 | 3.9 | 10 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 |
| Vinarija Gamanović · Cabernet Sauvignon | 87 | 3.9 | 4 |
| Manastir Bukovo · Filigran Merlot | 87 | 4.2 | 3 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Kremen Kamen | 97 | — | 54 |
| Matalj · Kremen Kamen Cabernet Sauvignon | 97 | 4.5 | 33 |
| Manastir Bukovo · Filigran Гаме | 92 | — | 9 |
| Vimmid · Dentelle | 92 | — | 6 |
| Manastir Bukovo · Filigran Reserve Cabernet Sauvignon | 91 | — | — |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Matalj · Bagrina Bukovska | 94 | 3.9 | 2 |
| Vinarija Gamanović · Grašac Beli | 94 | 3.9 | 16 |
| Matalj · Terasa Chardonnay | 92 | — | 42 |
| Traško Vinarija · Bagrina Edición Limitada | 92 | 3.9 | 6 |
| Manastir Bukovo · Filigran Chardonnay | 90 | — | 3 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Manastir Bukovo · Filigran Roze | 89 | — | 2 |
| Matalj · Dušica Rose | 89 | 3.8 | 6 |
| Mikić · Rosé | 84 | — | 2 |


## Подунавље и Београд

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Janko · Stari Zavet | 92 | — | 70 |
| Virtus · Credo | 92 | — | 56 |
| Virtus · Prokupac | 91 | 3.8 | 51 |
| Janko · Vrtlog | 90 | — | 28 |
| VINARIJA STANKOVIĆ · Chardonnay | 91 | — | 24 |
| VINARIJA STANKOVIĆ · Cabernet Sauvignon | 91 | — | 22 |
| Despotika · Nebo | 90 | — | 18 |
| Plavinci · Selena | — | — | 17 |
| Vinarija Milićević · Vladavina Icone Merlot | 90 | — | 14 |
| Plavinci · Ćilibar | 86 | 3.9 | 12 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Virtus · Morava | 95 | 3.9 | 16 |
| Винарија Тришић (Vinarija Trišić) · Dimasid | 94 | — | 9 |
| Virtus · Pinot Grigio | 93 | 3.8 | 33 |
| Janko · Stari Zavet | 92 | — | 70 |
| Jeremić · Kanon Merlot - Cabernet Sauvignon | 92 | 4.1 | — |
| Plavinac · Rebo | 92 | — | 8 |
| Vinarija Milićević · VLADAVINA Merlot | 92 | — | 8 |
| Janko · Zapis Crveni | 91 | — | 14 |
| Jeremić · Sonata Sauvignon Blanc | 91 | 3.8 | — |
| VINARIJA STANKOVIĆ · Cabernet Sauvignon | 91 | — | 22 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Janko · Zlatno Runo Cabernet Sauvignon | 87 | 4.4 | 3 |
| Janko · Запис Тестамент (Crveni Zapis Testament) | — | 4.4 | — |
| Jeremić · Kanon Superior Merlot - Cabernet Sauvignon | — | 4.3 | — |
| Virtus · Cuvée Virtus Credo | — | 4.3 | — |
| Virtus · Prokupac 733 | 90 | 4.3 | 12 |
| Jeremić · Sonata Icon Sauvignon Blanc | — | 4.2 | — |
| Plavinci · Good Boy Bruno! Pét Nat | — | 4.2 | — |
| Pruna · Cabernet Sauvignon | — | 4.2 | — |
| Pruna · Umbra Tamjanika | — | 4.1 | — |
| Винарија Тришић (Vinarija Trišić) · Тришино (Triša's) | — | 4.0 | — |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Virtus · Credo Beli | 92 | 4.2 | 32 |
| Virtus · Marselan | 91 | 4.0 | 50 |
| Janko · Bifora | 90 | 4.3 | 16 |
| Janko · Zavet | 89 | 3.9 | 9 |
| Plavinci · Ćilibar | 86 | 3.9 | 12 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Винарија Тришић (Vinarija Trišić) · Dimasid | 94 | — | 9 |
| Janko · Stari Zavet | 92 | — | 70 |
| Jeremić · Kanon Merlot - Cabernet Sauvignon | 92 | 4.1 | — |
| Plavinac · Rebo | 92 | — | 8 |
| Virtus · Credo | 92 | — | 56 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Virtus · Morava | 95 | 3.9 | 16 |
| Virtus · Pinot Grigio | 93 | 3.8 | 33 |
| Jeremić · Sonata Sauvignon Blanc | 91 | 3.8 | — |
| VINARIJA STANKOVIĆ · Chardonnay | 91 | — | 24 |
| Despotika · Nebo | 90 | — | 18 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Virtus · Rosé | 89 | 3.6 | 10 |
| Virtus · W | 89 | — | 3 |
| Vinarija Milićević · rose | 84 | — | 1 |


## Подриње и Колубара

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Pusula Winery · Traminac | 90 | 4.0 | 20 |
| Milijan Jelić · Kameničanka | — | — | 12 |
| Pusula Winery · Sauvignon Blanc | 88 | 3.6 | 12 |
| Milijan Jelić · Morava | — | 3.8 | 9 |
| Karić Vinarija · Adria | 90 | — | 6 |
| Vinarija Đurđevića Legat · Otisak Vremena | 90 | — | 6 |
| HUP MIHAJLOVAC · Djurdjevica Legat - Otisak | 89 | — | 4 |
| HUP MIHAJLOVAC · Djurdjevica Legat - Otisak vremena | 87 | — | 4 |
| Vinarija Đurđevića Legat · Sanivale | — | — | 4 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Karić Vinarija · Adria | 90 | — | 6 |
| Pusula Winery · Traminac | 90 | 4.0 | 20 |
| Vinarija Đurđevića Legat · Otisak Vremena | 90 | — | 6 |
| HUP MIHAJLOVAC · Djurdjevica Legat - Otisak | 89 | — | 4 |
| Pusula Winery · Cabernet Sauvignon | 89 | 3.4 | 8 |
| HUP MIHAJLOVAC · Djurdjevica Legat - Do neba i nazad | 87 | — | 2 |
| Vinarija Đurđevića Legat · Otisak | 86 | — | 3 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Đurđevića Legat · Otisak Merlot - Cabernet Sauvignon Crveno | — | 4.2 | — |
| Milijan Jelić · Millennium | — | 4.1 | 4 |
| Milijan Jelić · Millennium Barrique | — | 4.1 | 2 |
| Pusula Winery · Traminac | 90 | 4.0 | 20 |
| Vinarija Đurđevića Legat · Do Neba i Nazad Belo | — | 4.0 | — |
| Pusula Winery · Cabernet Cuvee | — | 3.8 | — |
| Andrića Vinograd · Consul Prokupac - Merlot | — | 3.7 | — |

**Согласие трёх** — не набирается: подходящих вин 2.

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Vinarija Đurđevića Legat · Otisak Vremena | 90 | — | 6 |
| Pusula Winery · Cabernet Sauvignon | 89 | 3.4 | 8 |
| Pusula Winery · Cabernet | 86 | — | 6 |
| Vinarija Đurđevića Legat · Otisak | 86 | — | 3 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Karić Vinarija · Adria | 90 | — | 6 |
| Pusula Winery · Traminac | 90 | 4.0 | 20 |
| Pusula Winery · Chardonnay | 88 | 3.7 | 10 |


## Топлица

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Doja · Prokupac | 95 | 3.9 | 70 |
| Doja · Breg Prokupac | 95 | 4.1 | 64 |
| Toplički vinogradi · Epigenia Prokupac | 92 | 3.8 | 26 |
| Kostić · Prokupac | — | — | 12 |
| Toplički vinogradi · Vranac Barrique | 90 | — | 12 |
| Kostić · Tamjanika Oranž | — | — | 6 |
| Tody · Doja Belo | 83 | — | 2 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Doja · Breg Prokupac | 95 | 4.1 | 64 |
| Doja · Prokupac | 95 | 3.9 | 70 |
| Toplički vinogradi · Epigenia Prokupac | 92 | 3.8 | 26 |
| Toplički vinogradi · President Vranac | 90 | — | 4 |
| Tody · Doja Belo | 83 | — | 2 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Toplički vinogradi · Гвоздени Пук Ирьено (Gvozdeni Puk Ryeno) | — | 4.4 | — |
| Doja · Breg Cabernet Sauvignon | 94 | 4.3 | 34 |
| Kostić · Prokupac Barrique | — | 4.2 | 4 |
| Doja · Breg Prokupac | 95 | 4.1 | 64 |
| Kostić · Cuvée | — | 4.0 | — |
| Toplički vinogradi · Epigenia Cabernet Sauvignon | — | 3.8 | 9 |

**Согласие трёх** — только 4 вина вместо пяти

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Doja · Breg Prokupac | 95 | 4.1 | 64 |
| Doja · Breg Cabernet Sauvignon | 94 | 4.3 | 34 |
| Toplički vinogradi · Epigenia Prokupac | 92 | 3.8 | 26 |
| Toplički vinogradi · Tribus Villa Prokupac | 88 | 3.5 | 4 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Doja · Breg Prokupac | 95 | 4.1 | 64 |
| Doja · Prokupac | 95 | 3.9 | 70 |
| Toplički vinogradi · Epigenia Prokupac | 92 | 3.8 | 26 |
| Toplički vinogradi · Tribus Villa Prokupac | 88 | 3.5 | 4 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Doja · Chardonnay Barrique | 91 | 3.7 | 2 |
| Doja · Chardonnay-Pinot Grigio | 90 | — | 11 |
| Tody · Doja Belo | 83 | — | 2 |


## Југоисток

**Олимпиадный зачёт**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksić · Amanet Vranac | 95 | 4.0 | 36 |
| Aleksić · Žuti Cvet Tamjanika | 91 | — | 32 |
| Jović · Vranac Potrkanjski | 94 | — | 24 |
| Džervin · Sauvignon | 89 | 3.9 | 16 |
| Vinarija Todorović · Merlot | 89 | 4.0 | 13 |
| Džervin · Trifun Grand Cabernet Sauvignon | 91 | — | 12 |
| Jović · Chardonnay Potrkanjski | — | — | 10 |
| Vinarija Todorović · Cabernet Sauvignon | — | 3.9 | 8 |
| Vinarija 100 Žena · 100 žena-100 women-Monsieur Merlot | 90 | — | 8 |
| Vinarija 100 Žena · Veliki Dečko | 89 | 3.8 | 8 |

**Мнение экспертов**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksić · Amanet Vranac | 95 | 4.0 | 36 |
| Aleksić · Biser Smederevka Extra Brut | 95 | — | 12 |
| Džervin · Lozana | 94 | — | 7 |
| Jović · Vranac Potrkanjski | 94 | — | 24 |
| Džervin · Trifun Grand Cabernet Sauvignon | 91 | — | 12 |
| Vinarija 100 Žena · 100 žena-100 women-Monsieur Merlot | 90 | — | 8 |
| Jović · Rose Dionizije | 89 | 3.5 | 8 |
| Vinarija Todorović · Merlot | 89 | 4.0 | 13 |
| Vinarija 100 Žena · Veliki Dečko | 89 | 3.8 | 8 |
| Hrusija d.o.o. Leskovac · Simfonija - Prokupac 65%, Kaberne sovinjon 20%, Merlot 15% | 87 | — | 2 |

**Vox populi**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Изба Јовановић (Izba Jovanovic) · Žetva | — | 4.3 | — |
| Vinarija 100 Žena · Monsieur Merlot Premium | — | 4.2 | — |
| Изба Јовановић (Izba Jovanovic) · Merlot | — | 4.2 | 8 |
| Vinarija 100 Žena · Rosé | — | 4.1 | 6 |
| Митровиђ Винарија · Monogram | — | 4.1 | — |
| Aleksić · Limited Bonaca Chardonnay | 87 | 4.1 | 6 |
| Aleksić · Žuti Cvet | 87 | 4.1 | 14 |
| Jović · Petrkanjski Roze | — | 4.0 | — |
| Jović · Vranac | — | 4.0 | — |
| Vinarija Todorović · Merlot | 89 | 4.0 | 13 |

**Согласие трёх**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksić · Amanet Vranac | 95 | 4.0 | 36 |
| Aleksić · Limited Kardaš Cabernet Sauvignon | 90 | 4.0 | 15 |
| Vinarija Todorović · Merlot | 89 | 4.0 | 13 |
| Džervin · Sauvignon | 89 | 3.9 | 16 |
| Vinarija 100 Žena · Veliki Dečko | 89 | 3.8 | 8 |
| Vinarija 100 Žena · Tamjanika | 88 | 4.1 | 6 |
| Jović · Rose Dionizije | 89 | 3.5 | 8 |
| Podrum Malča · Anonymous Grašac | 85 | 3.8 | 2 |

**Красные: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksić · Amanet Vranac | 95 | 4.0 | 36 |
| Jović · Vranac Potrkanjski | 94 | — | 24 |
| Aleksić · Kardaš Cabernet Sauvignon | 92 | 3.8 | 9 |
| Džervin · Trifun Grand Cabernet Sauvignon | 91 | — | 12 |
| Džervin · Cuvee 69 | 89 | — | 6 |

**Белые: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Aleksić · Biser Smederevka Extra Brut | 95 | — | 12 |
| Aleksić · Žuti Cvet Penuśavo Tamnjanika Sec | 95 | — | 12 |
| Džervin · Lozana | 94 | — | 7 |
| Džervin · Dubravka Gold | 89 | — | 5 |
| Jović · Rizling Rajnski Potrkanjski | 88 | — | 10 |

**Розе: тройка и запас**

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Jović · Rose Dionizije | 89 | 3.5 | 8 |
| Džervin · Nijansa | 87 | — | 5 |
| Vinarija 100 Žena · Roze | 87 | — | 2 |


## Косово и Метохија

**Олимпиадный зачёт** — не набирается: подходящих вин 2.

**Мнение экспертов** — не набирается: подходящих вин 2.

**Vox populi** — только 4 вина вместо пяти

| Вино | Критик | Vivino | Медали |
|---|---|---|---|
| Monastery Visoki Decani  (Манастирско Дечанско) · Cabernet Sauvignon Barrique | — | 4.2 | — |
| Lakićević · Cuvée Alcedo | — | 4.2 | — |
| Lakićević · Cuvée No.5 Merula | — | 4.2 | — |
| Monastery Visoki Decani  (Манастирско Дечанско) · Red (Црвени) | — | 3.8 | — |

**Согласие трёх** — не набирается: подходящих вин 0.

