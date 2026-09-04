# Отсев: о ком есть что сказать

В сборе 454 хозяйства — все сербские винарии, каких удалось найти. Это не
значит, что каждая заслуживает строки в справочнике: у части нет ни одной
оценки, у части оценка есть, но ниже сербской нормы, а две строки — вовсе
не хозяйства, а ошибка ввода у Decanter.

**Отсутствие оценки — это отсутствие данных, а не приговор вину.**
Маленькое хозяйство может делать прекрасное вино, которого просто никто
не оценил: на конкурс оно не выходило, а на Vivino у него три отзыва.
Поэтому ступени ниже названы по признаку, а не по качеству, и последняя
ступень читается как «сказать нечего», а не как «вино плохое».

## Четыре ступени

1. **Оценка критика или медаль** — 202 хозяйства. Есть балл Decanter или
   Falstaff, или медаль конкурса. О таком хозяйстве справочник может
   сказать что-то проверяемое.
2. **Только Vivino, выборка набрана** — 85 хозяйств. Оценки критиков нет,
   но хотя бы одно вино держит 25 отзывов и больше. Порог тот же, что
   у пятёрок: ниже него средняя ничего не значит.
3. **Вина есть, оценок нет** — 165 хозяйств. Vivino знает их вина, но
   оценку не показывает: отзывов слишком мало. На конкурсы они не выходили.
4. **Ни вин, ни оценок** — таких не осталось.

Ступени 1 и 2 — 287 хозяйств — и есть тот круг, о котором справочник
рейтингов может говорить.

## Что из третьей ступени всё же стоит внимания

Сто шестьдесят пять «немых» хозяйств — не мусор. Восемьдесят четыре
нашлись в Винарском регистру, то есть это действующие производители
с лицензией, и у восьмидесяти девяти известен рејон. В книге из них назван
один — Драгојловић с Фрушке горе.

Вывод простой: **третья ступень — это не «недостойные», а «неизмеренные»**.
Исключать их из книги по этому признаку нельзя; исключать из **рейтинговой
части** — можно и нужно, потому что рейтинга у них нет.

## Какие фильтры применены

**Порог выборки — 25 отзывов.** Тот же, что у пятёрок. Оценка 4,6 по трём
отзывам не значит ничего.

**Нижняя десятая часть оценок Vivino.** Лучшее вино хозяйства держится
на 3,4 и ниже при набранной выборке, и при этом ни медали, ни балла
критика. Средняя сербская оценка Vivino — 3,85, медиана 3,90; 3,4 — это
десятый процентиль. Таких хозяйств девять, и среди них Navip: шесть вин,
479 отзывов, лучшее 3,4. Это уже не отсутствие данных, а данные.

**Строки, которые не хозяйства.** «Marselan» и «Prokupac» — ошибка ввода
у Decanter: в поле производителя стоит название сорта. Отсеяны.

## Какие фильтры рассмотрены и отвергнуты

**«Нет в Винарском регистру».** В регистре нашлись 300 хозяйств из 454.
Остальные — не обязательно незарегистрированные: регистр пишет
юридическое имя, и марка в нём может не встретиться вовсе. Признак
ненадёжный, фильтром не годится.

**«Мало вин».** Petica — два вина, 163 отзыва, лучшее 4,4. Tri Oraha —
восемь вин, 909 отзывов, лучшее 4,5. Размер ассортимента о качестве
не говорит.

**«Награда старая».** Медаль DWWA 2017 остаётся медалью. Год стоит
в таблице отдельным столбцом — пусть решает читатель, а не отсев.

**«Хозяйства нет в книге».** Это перевёрнутый вопрос: справочник рейтингов
затевался в том числе чтобы показать, кого в книге не хватает.

## Что осталось решать автору

Ступени 1 и 2 разделены порогом отзывов, а не качеством. Нужно ли
показывать в книге хозяйство, у которого есть только оценка покупателей
и ни одной оценки критика, — вопрос об устройстве книги, а не о данных.
То же и с девятью хозяйствами ниже нормы: сказать «Navip держит 3,4»
можно, и это честно, но нужно ли — решать автору.

**Пересобрать файл:**

    python3 _rabota/rejtingi/svesti-otsev.py --otchet


## Что получилось

| Ступень | Всего | Из них без рејона | Из них в книге |
|---|---|---|---|
| оценка критика или медаль | 216 | 15 | 61 |
| только Vivino, выборка набрана | 72 | 21 | 2 |
| вина есть, оценок нет | 163 | 75 | 1 |
| **всего** | **451** | **111** | **64** |

## Сказать есть что, а где стоит — неизвестно

Именно эти и стоят руки. У остальных без рејона нет ни одной оценки, и место им ничего не добавит.

| Хозяйство | Лучший балл критика | Медалей | Лучшая Vivino | Вин с выборкой | Отзывов | Последний год |
|---|---|---|---|---|---|---|
| Josic Winery | 92 | — | — | — | 0 | 2020 |
| AURUS Winery & Distillery | 90 | 5 | — | — | 0 | 2026 |
| Николић Неyзински (Nikolićh Neuzinsky) | 90 | 3 | — | — | 0 | 2025 |
| Lakićević | 89 | 32 | 4.2 | 8 | 774 | 2025 |
| Vinarija Tasa | 89 | 2 | — | — | 0 | 2026 |
| Gardijan | 86 | 1 | — | — | 0 | 2026 |
| Winery ŠKRBIĆ | 85 | 1 | 4 | 3 | 126 | 2018 |
| Damalis | 85 | 1 | — | — | 0 | 2026 |
| Kuća Vina Jokić | 85 | 1 | — | — | 0 | 2020 |
| Robert Rudinski | — | 2 | 3.6 | 1 | 62 | 2022 |
| Miletić | — | 1 | 4.2 | 4 | 155 | 2021 |
| Vinarija Bela Kula | — | 1 | 3.9 | 2 | 51 | 2021 |
| In | — | 1 | — | — | 0 | 2023 |
| Probus Vineyard | — | 1 | — | — | 0 | 2023 |
| Милица (Milica) | — | 1 | — | — | 0 | 2023 |
| Petica | — | — | 4.4 | 2 | 163 | — |
| Брояница (Brojanica) | — | — | 4.1 | 7 | 6170 | — |
| Intuicija | — | — | 4.1 | 1 | 32 | — |
| Serbika Wine | — | — | 4 | 4 | 262 | — |
| Podrum Panajotovic | — | — | 4 | 1 | 47 | — |
| Vinarija Bogunovic | — | — | 4 | 1 | 44 | — |
| Vinarija Vojnović | — | — | 3.9 | 1 | 27 | — |
| Vinogradi Nikolic | — | — | 3.8 | 1 | 70 | — |
| Nelt | — | — | 3.8 | 1 | 40 | — |
| M. Dubrana - N. Scheidt | — | — | 3.8 | 1 | 27 | — |
| Boemi | — | — | 3.6 | 2 | 208 | — |
| Ukusi Moga Kraja | — | — | 3.6 | 2 | 91 | — |
| Moderato | — | — | 3.6 | 1 | 38 | — |
| Perun Wine | — | — | 3.5 | 2 | 511 | — |
| Enigma | — | — | 3.5 | 3 | 141 | — |
| ODPF-Radmilovac | — | — | 3.5 | 1 | 47 | — |
| Vinokratija | — | — | 3.5 | 1 | 32 | — |
| WinEco | — | — | 3.5 | 1 | 29 | — |
| Sava Minić | — | — | 3.4 | 2 | 171 | — |
| Vina Pešić | — | — | 3.4 | 2 | 62 | — |
| Sunčani Breg | — | — | 3.4 | 1 | 26 | — |

## Оценка набрана, но ниже сербской нормы

Лучшее вино хозяйства держится на 3,4 и ниже при выборке от 25 отзывов — это нижняя десятая часть всех сербских оценок Vivino (средняя 3,85, медиана 3,90). Ни медалей, ни оценок критиков у этих хозяйств нет.

| Хозяйство | Лучшая Vivino | Вин с выборкой | Отзывов | Рејон |
|---|---|---|---|---|
| Vinex Grozd | 2.9 | 2 | 146 | Rejon Tri Morave |
| Vinarija Selecta | 3.2 | 1 | 28 | Južnobanatski rejon |
| Vinarija Vojinović | 3.3 | 1 | 27 | Beogradski rejon |
| Navip | 3.4 | 6 | 479 | Vranjski rejon |
| Agrina | 3.4 | 1 | 225 | Sremski rejon |
| Nikolas | 3.4 | 2 | 175 | Knjaževački rejon |
| Sava Minić | 3.4 | 2 | 171 | — |
| Vina Pešić | 3.4 | 2 | 62 | — |
| Sunčani Breg | 3.4 | 1 | 26 | — |

## Ни одной оценки и ни одной награды

163 хозяйств. Вина у них в сборе есть, но Vivino не показывает оценку — отзывов слишком мало, — и ни на один конкурс они не выходили. Справочнику рейтингов сказать о них нечего: не потому, что вино плохое, а потому, что его никто не оценил.

| Хозяйство | Вин в сборе | В Винарском регистру | Рејон |
|---|---|---|---|
| Винарија Живковић (Vinarija Živković) | 9 | да | Rejon Tri Morave |
| Vinarija Brestovački | 8 | да | Sremski rejon |
| Vinarija Brindza | 8 | да | — |
| Vinarija Levač | 8 | да | Rejon Tri Morave |
| World Of Wine | 8 | не нашлось | — |
| Podrum Palić | 7 | да | Subotički rejon |
| Porodična Vinarija Stanimirović | 7 | да | Južnobanatski rejon |
| Lagum | 6 | не нашлось | — |
| Podrum Ljubisavljević | 6 | да | Niški rejon |
| Radošević | 6 | да | Sremski rejon |
| Radu Group Vinarija | 6 | да | Rejon Negotinska Krajina |
| Rajacke Pimnice Vinarija Vukašinovi | 6 | не нашлось | — |
| Saboss | 6 | да | Rejon Tri Morave |
| Vinarija Agatija | 6 | да | Rejon Tri Morave |
| Vinarija Kurjak | 6 | да | Sremski rejon |
| Vinarija Milojević | 6 | да | Beogradski rejon |
| Vinarija Ćosić | 6 | да | Rejon Tri Morave |
| Vinik | 6 | да | Južnobanatski rejon |
| Виногради Гроцка (Vinogradi Grocka) | 6 | да | Beogradski rejon |
| Bahus | 5 | да | Južnobanatski rejon |
| Kepul | 5 | да | Banatski rejon |
| Majetić | 5 | не нашлось | — |
| Pimnica Perić | 5 | не нашлось | — |
| Podrum Jovanovic | 5 | да | — |
| Soul Wine | 5 | да | Južnobanatski rejon |
| Vinarija Pantić | 5 | не нашлось | Beogradski rejon |
| Vinarija Sinjac | 5 | не нашлось | — |
| Weingut Jović | 5 | да | — |
| Полрум Вина Тодор (Podrum Vina Todor) | 5 | да | Rejon Tri Morave |
| 45. Paralela | 4 | да | Sremski rejon |
| Antonijević Family Winery | 4 | да | Sremski rejon |
| Conte Vallonne | 4 | не нашлось | — |
| Crmničko Vino | 4 | не нашлось | — |
| Dealul Tirolului | 4 | не нашлось | — |
| Milić | 4 | да | Rejon Tri Morave |
| Molin Winery | 4 | да | — |
| Nikodijević | 4 | не нашлось | — |
| Podrum Krička | 4 | не нашлось | — |
| Podrum Lukic | 4 | да | Pocersko Valjevski Rejon |
| Stari Oplenac | 4 | да | Šumadijski rejon |
| Vinarija Boierescu | 4 | да | Rejon Negotinska Krajina |
| Vinarija Milovanovic | 4 | да | Rejon Tri Morave |
| Vinarija Rajić | 4 | да | Rejon Tri Morave |
| Vinarska Kuća Miljković | 4 | да | Rejon Tri Morave |
| Vinski Podrum Mirjana | 4 | да | Rejon Negotinska Krajina |
| Ačanski | 3 | да | Sremski rejon |
| Bogdanovic | 3 | да | — |
| Cvetković Vinarija | 3 | да | Rejon Tri Morave |
| Dukay | 3 | да | Sremski rejon |
| Mali Šareni Podrum | 3 | не нашлось | — |
| Marinković | 3 | да | — |
| Orvin | 3 | не нашлось | — |
| Podrum Milošević | 3 | да | — |
| Podrum Pića Maric | 3 | не нашлось | — |
| Podrum Zagorac | 3 | не нашлось | — |
| Puce | 3 | да | Pocersko Valjevski Rejon |
| Radosavljevic | 3 | да | Rejon Tri Morave |
| Rittium | 3 | не нашлось | Sremski rejon |
| Srodne Duše | 3 | не нашлось | — |
| Tica Winery | 3 | не нашлось | — |
| Vina Mives | 3 | да | Šumadijski rejon |
| Vinarija Aquila | 3 | да | Leskovački rejon |
| Vinarija Bononia | 3 | не нашлось | — |
| Vinarija Dosen | 3 | не нашлось | Sremski rejon |
| Vinarija Krajina Rajac | 3 | не нашлось | — |
| Vinarija Lalić | 3 | да | Južnobanatski rejon |
| Vinarija Mišić | 3 | да | — |
| Vinarija Nedin | 3 | да | Južnobanatski rejon |
| Vinarija Okrug | 3 | не нашлось | — |
| Vinarija S. Milošević | 3 | да | Čačansko–kraljevački rejon |
| Vinarija Smiljković 90 | 3 | да | Rejon Tri Morave |
| Vinartos Vinarija | 3 | да | Potiski rejon |
| Vinska Kuća Milić - Geci M | 3 | да | — |
| Аранђеловић 1920 (Aranđelović 1920) | 3 | не нашлось | Toplički rejon |
| Патријаршија (Patriarchate) | 3 | не нашлось | — |
| Фенек (Fenek Monastery) | 3 | да | Beogradski rejon |
| Чаша Вина и Прича (Čaša Vina i Priča) | 3 | да | — |
| Benišek Veselinović | 2 | не нашлось | Sremski rejon |
| Cubra | 2 | да | Rejon Negotinska Krajina |
| Dragojlović Vinarija | 2 | не нашлось | Sremski rejon |
| Hadži Popović | 2 | да | Sremski rejon |
| Jagodinska | 2 | не нашлось | — |
| Jevremović | 2 | не нашлось | — |
| Kutinska Vinarija | 2 | не нашлось | — |
| Kuća Vina Popović | 2 | да | Mlavski rejon |
| Mali Podrum Stamenković | 2 | не нашлось | — |
| Nera | 2 | не нашлось | Sremski rejon |
| Pannonian | 2 | не нашлось | — |
| Petković Latin | 2 | да | Sremski rejon |
| Podrum Stojković | 2 | да | Sremski rejon |
| Savković | 2 | да | Rejon Tri Morave |
| Terra Balkanika | 2 | не нашлось | — |
| Tri Puške | 2 | не нашлось | — |
| Victory | 2 | не нашлось | — |
| Vinarija A. Rajković | 2 | да | Rejon Tri Morave |
| Vinarija Apatović | 2 | да | Sremski rejon |
| Vinarija Bada | 2 | да | Rejon Tri Morave |
| Vinarija Burcel Todorov | 2 | не нашлось | — |
| Vinarija Mozaik Milan | 2 | не нашлось | Rejon Tri Morave |
| Vinarija Porta | 2 | не нашлось | Rejon Negotinska Krajina |
| Vinarija Vilotijević | 2 | не нашлось | — |
| Vinarija Vino Grade | 2 | не нашлось | — |
| Vinska Kuća Milinčić | 2 | да | Rejon Tri Morave |
| Vučurević | 2 | да | Sremski rejon |
| Zlatar | 2 | не нашлось | — |
| Ćirić | 2 | да | Rejon Tri Morave |
| Манастир Жича (Monastery of Licha) | 2 | не нашлось | — |
| 117 Wine | 1 | не нашлось | Rejon Bačka |
| Alaska Barka | 1 | не нашлось | — |
| Alchemy Winery | 1 | не нашлось | Sremski rejon |
| Amstadt Winery | 1 | не нашлось | — |
| Arhangel | 1 | не нашлось | — |
| Belgrade | 1 | не нашлось | — |
| Enellion | 1 | не нашлось | Rejon Telečka |
| Fekete | 1 | не нашлось | Rejon Bačka |
| Janek Wineyard | 1 | не нашлось | — |
| K-ing | 1 | не нашлось | — |
| Koreni | 1 | да | — |
| Krug Vinarija | 1 | не нашлось | — |
| Mihajlovacko | 1 | не нашлось | — |
| Moravski Val | 1 | да | — |
| Perla | 1 | не нашлось | — |
| Podrum Gvozdanović | 1 | не нашлось | — |
| Podrum Stričević | 1 | не нашлось | — |
| Podrum Tosic | 1 | не нашлось | — |
| Prima | 1 | не нашлось | Leskovački rejon |
| Rajačke Pimnice Podrum Prvulović | 1 | не нашлось | — |
| Rujevica | 1 | не нашлось | — |
| Sila | 1 | не нашлось | Rejon Bačka |
| Teodora | 1 | не нашлось | Sremski rejon |
| Uns Petra | 1 | не нашлось | — |
| Uziwa Winery | 1 | да | Rejon Tri Morave |
| Vina Jelenković | 1 | да | Rejon Tri Morave |
| Vinarija Aleksandar | 1 | да | Južnobanatski rejon |
| Vinarija Gvožđan | 1 | не нашлось | — |
| Vinarija Mihailović | 1 | да | Šumadijski rejon |
| Vinarija Necak | 1 | да | Mlavski rejon |
| Vinarija Rudež | 1 | не нашлось | — |
| Vinarija Tana | 1 | да | Rejon Negotinska Krajina |
| Vinarija Tanasković | 1 | да | Sremski rejon |
| Vinarija Timahus | 1 | не нашлось | Rejon Negotinska Krajina |
| Vinarija Tomić - Rošci | 1 | да | Čačansko–kraljevački rejon |
| Vinarija Val d'Ov | 1 | да | — |
| Vinarija VinoIlić | 1 | да | Šumadijski rejon |
| Vinarija Vulovic | 1 | не нашлось | — |
| Vinarija Čolaković | 1 | да | Čačansko–kraljevački rejon |
| Vinarija Žir | 1 | не нашлось | Šumadijski rejon |
| Vinska Kuća Djordjevic | 1 | да | — |
| Vinska Kuća Rakićević | 1 | да | Rejon Tri Morave |
| Vinum Lódi | 1 | не нашлось | — |
| Vladavina | 1 | да | Rejon Tri Morave |
| Vukman | 1 | не нашлось | — |
| Walc & Grozd | 1 | не нашлось | — |
| Zvezda | 1 | не нашлось | — |
| Šumadija | 1 | не нашлось | — |
| Živač | 1 | не нашлось | — |
| Винарија Королија | 1 | да | Rejon Negotinska Krajina |
| Винарија Мицић | 1 | не нашлось | — |
| Виница Грковић (Vinica Grković) | 1 | не нашлось | Niški rejon |
| Дика Винарија | 1 | да | Šumadijski rejon |
| Подрум Берлин | 1 | не нашлось | — |
| Подрум Вина Лазаревић | 1 | да | Rejon Tri Morave |
| Фенечко Вино | 1 | не нашлось | — |

## Строки, которые не хозяйства

Ошибки ввода у Decanter: в поле производителя стоит название сорта. В отсчёт выше они не входят.

- **Marselan** — Ошибка ввода у Decanter, DWWA 2023: в поле производителя стоит название сорта, вино тоже «Marselan». Марселан в Сербии делают десятки хозяйств — привязать не к кому.
- **Prokupac** — То же, DWWA 2021. Прокупац делают почти все — привязать не к кому.

