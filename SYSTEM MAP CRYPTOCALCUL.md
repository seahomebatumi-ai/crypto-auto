# SYSTEM_MAP — Pro Crypto Tool

Единый источник правды. Сверяться ПЕРЕД любой правкой кода и при интерпретации метрик.
Актуально на 11.08.2026 (`--verify` §3.10; чистка мёртвого CSS §9; блок «ЗАЩИТА ПОЗИЦИИ» §3.11); прежняя редакция — (жёсткий потолок риска маржи §3.4, доска CRYPTO FUTURE, движок плеча на трёх потолках, размер в монетах, якорь прокрутки, «ШОРТ СОЗРЕЕТ, КОГДА», остаток к BTC `res7`).

> **Language rule (project instructions V9, in force from 11.08.2026):** new
> sections of this map and new code comments are written in ENGLISH. Sections
> written earlier stay in Russian — retranslating them would be an unsolicited
> rewrite of a validated document, and the mixture is deliberate, not drift.
> Only chat with the Boss is in Russian; UI strings stay Russian by definition.

## 1. Поток данных
GitHub Actions (cron ~1 раз/час) → Python-бот → CoinGecko `/market_chart` (90 дней, hourly; BTC + 28 альтов = 29 вызовов) + `/coins/markets` (ранги, 1 вызов) = 30 вызовов/прогон ≈ 21.6k/мес → расчёт метрик → PATCH Gist → WebApp (iPhone).

Файлы Gist:
- `coeffs.json` — generated_at + `btc` (min/max/price_pos/volatility + **r7/r14/r30**) + analysis_data[] (в т.ч. `rank`, `rank_prev`, `fdv_mc`)
- `debug.json` — по монетам: candles_total, matched_90d/14d, returns_90d/14d, error, ranks_fetched, fdv_fetched
- `history.json` — до 720 точек (~30 дней): ub/ur/db/dr/ub90/db90 + ранг `r`

Фронт дополнительно (три независимых источника Binance):
- спот-тикер `api/v3/ticker/24hr?symbols=` — 30 с, только пары БЕЗ `fut:true`;
- фьюч-тикер `fapi/v1/ticker/24hr?symbol=` — 30 с, по одному запросу на каждый `fut:true`-токен;
- funding `fapi/v1/premiumIndex` — 5 мин.

## 2. Математика — бот
- Бакетирование: `floor(ts_ms / 3.6e6)` → часовые бакеты; общие ключи BTC ∩ монета.
- Возвраты: **только между соседними бакетами**; возвраты через дыры отбрасываются.
- Беты: OLS с интерсептом, раздельно up (BTC-час > 0) и down (< 0); окна 14д и 90д. Минимумы: 24 matched (14d), 120 (90d); < 5 возвратов в направлении → None. Интерсепт (альфа) сознательно НЕ используется: на 14д его стандартная ошибка сопоставима с самим значением.
- `up_beta_90`/`up_r2_90` и `down_*` всегда парны: `fit_stats` возвращает либо (float,float), либо (None,None).
- `corr_90`: Пирсон по всем 90д-возвратам. `volatility`: std часовых возвратов за 90д. `min/max/price_pos`: за 90д.
- `btc.volatility` — часовая волатильность самого BTC за 90д. **С 08.08.2026 используется фронтом** — задаёт величину просадки в авто-стрессе (§3.2).
- `btc.r7` / `btc.r14` / `btc.r30` (10.08.2026) — доходность самого BTC за 7/14/30 дней. Та же `window_stats`, что и у альтов, по уже скачанному ряду BTC: **ноль новых вызовов API**. Нужны фронту для остаточной доходности `res7 = r7 − β₉₀·r7_BTC` (§3.9). `null` штатен (ряд короче окна или битая первая цена) — фронт обязан пережить (инв. 9). Окна режутся от ПОСЛЕДНЕЙ точки своего ряда: метка времени BTC и альта может отличаться на минуты, на горизонте 7 суток это ниже шума.
- `fdv_mc` = fully_diluted_valuation / market_cap из того же вызова `/coins/markets`, что и ранги (ноль новых запросов). Отсеиваются значения <0.95 и >100 (мусор данных о supply). `None` штатен: у монет без max supply (ETH, XMR) CoinGecko отдаёт FDV = null.
- `error=true` ⇔ мало 14d-точек или сбой запроса → фронт рисует NO DATA.
- Бот НЕ зависит от наличия спот-пары: беты считаются по CoinGecko.

**Перекрёстная проверка целостности (08.08.2026):** из тождества однофакторной регрессии `σ_BTC = σ_alt·√R²/|β|` восстановлена часовая волатильность BTC по пяти независимым карточкам: 0.316–0.393 %/час, среднее 0.367 %, разброс ±11 %. Согласованность подтверждает корректность расчёта бет и R².

## 3. Математика — фронт
- `ratio = (target − btc)/btc`; `1+ratio = target/btc > 0` всегда.
- `rawBeta` = up_beta | down_beta по знаку ratio; null/не-число → карточка **NO BETA**.
- `beta = rawBeta × stress` (normal 1.0 / panic 1.3 / crash 1.8).
- Прогноз: `growth = (1+ratio)^beta`; `pPct = (growth−1)·100`; `pred = cur·growth`.
- Ликвидация от `pred`, isolated, `LIQ_MMR = 0.0125`: LONG `pred·(1−1/L+MMR)`, SHORT `pred·(1+1/L−MMR)`. Комиссии/funding не учтены. **База на карточке — `pred`; на доске — цена входа `E`.**
- **`LIQ_MMR = 0.0125` (было 0.01 до 09.08.2026).** Восстановлено обратным счётом по трём реальным позициям Босса: XMR 1.28 %, YFI 1.25 %, LIT 1.13 %. Прежний 0.01 ставил ликвидацию ДАЛЬШЕ реальной — ошибка в опасную сторону.
- Confidence (0–100): `0.45·R²₁₄ + 0.25·R²₉₀ + 0.20·(1−min(div90,1)) + 0.10·(1−min(vol%/3,1))`; отсутствующие компоненты выпадают с перенормировкой. Цвета: ≥70 зелёный, 40–69 жёлтый, <40 красный.
- **R² в обеих строках (14d и 90d) — одна шкала:** <0.30 красный, 0.30–0.60 жёлтый, ≥0.60 зелёный. До 08.08.2026 цвет 90d был захардкожен жёлтым при уже вычисленной переменной — исправлено.
- ρ (corr_90): ≥0.75 зел., 0.5–0.75 жёлт., <0.5 красн. Отдельного значка расхождения бет 14д/90д НЕТ — оно входит в Conf.
- **Гейт MDL** (`gateState`, чистое отображение): красный при `Conf < 40` ИЛИ `R²₁₄ < 0.25` ИЛИ (`corr_90` есть И `|ρ| < 0.5`); зелёный при `Conf ≥ 70` и остальных условиях; иначе жёлтый.

### 3.1 Сторона сделки — явный вход
`currentSide` ∈ {`long`,`short`}, по умолчанию `long`, задаётся кнопками ЛОНГ/ШОРТ, в localStorage не пишется.

**Направление слайдера ≠ сторона позиции.** Слайдер задаёт сценарий BTC; надпись в шапке — `BTC ВВЕРХ` / `BTC ВНИЗ` (переименована из LONG/SHORT 08.08.2026, старое название смешивало понятия).

От `currentSide` зависят: формула плеча (§3.2) и цвет Funding. От знака `ratio` зависят: выбор беты, цвет слайдера/кнопок/стрелок, обе строки ликвидации.

**Funding:** цвет = экономический эффект для НАЖАТОЙ стороны — зелёный «мне платят», красный «я плачу». До 08.08.2026 сторона выводилась из знака `ratio`, из-за чего цвет инвертировался ровно при замере риска (слайдер смотрит против сделки) — исправлено.

### 3.2 Движок плеча — три независимых потолка (переписан 09.08.2026)
Прежняя схема (фиксация входа `pinned`, режим АВТО-СТРЕСС, формула `L_max = 1/(1.01 − 0.87·k)`) **удалена целиком**. Причина: она отвечала на вопрос «переживёт ли позиция названный сценарий BTC», тогда как реально позицию убивают три разные вещи, и сценарий BTC — самая редкая из них.

Все три потолка считаются на **горизонте 7 суток** (`H_NOISE = H_BTC = 168`), действует минимум, округление вниз.

```
Уровень инвалидации (invalidationInfo):
  опора  = мин30 / макс30  (нет -> мин90 / макс90, инвариант 9)
  опора за входом -> src = 'вход'         структуры нет, останется только шум
  structPrice = опора ∓ ½σ_дн
  dist = clamp(dStruct, 2σ_дн, 6σ_дн)      INV_FLOOR_SD=2, INV_CAP_SD=6

1. СТРУКТУРА   L = 1/(dist + 1.645·Vol·√12 + MMR)      H_REACT = 12 ч
2. ШУМ 7д      need = ЛОНГ 1−e^(−q), ШОРТ e^q−1,  q = 1.645·Vol·√168
               L = 1/(need + MMR)
3. ОБВАЛ BTC   D = 2·btc.volatility·√168
               move = |(1 ∓ D)^β_adv − 1|            L = 1/(move + MMR)
               β_adv = |β90 противоположного направления|, ужесточается
               хвостовой бетой только при tail_r2 ≥ 0.10

ИТОГ = floor( min(три потолка, cap) ),  cap: L_CAP=7 · vol7/vol90 > 2 -> 3X · Vol ≥ 2%/ч -> 2X
Vol ≥ 3%/ч -> плечо не выдаётся вовсе.  ИТОГ < L_MIN=2 -> «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» + fixHint.
```

**Почему потолков именно три.** Структура — «успею ли выйти по своему уровню раньше биржи, если идея сломается, плюс 12 часов на реакцию (сон, работа)». Шум — «выбьет ли просто болтанкой за неделю, если не выходить вовсе». Обвал BTC — «переживу ли системное движение рынка». Они опираются на разные величины (расстояние до опоры / Vol / β), поэтому связывающий потолок у разных монет разный, и доска показывает КАКОЙ (`dec.binding`).

**Потолок дистанции 6σ обязателен.** Без него вход в середине диапазона давал «БЕЗ ПЛЕЧА»: далёкая опора трактовалась как огромный риск вместо отсутствия ориентира. При `capped` карточка честно пишет, что опоры рядом нет и стоп надо держать вручную.

**Пол дистанции 2σ обязателен.** Движение меньше двух дневных сигм — шум, а не поломка идеи; обещать выход по такому уровню нельзя.

**Горизонт 7 суток, а не 30.** Прежние 30 суток были самым чувствительным параметром системы: в одиночку двигали вердикт на две ступени плеча, не будучи связанными ни с одним решением Босса. 7 дней — верхняя граница его типичного удержания.

### 3.3 Вероятность касания ликвидации (`liqTouchProb`)
```
d = 1/L − MMR;   ЛОНГ b = −ln(1−d)   ШОРТ b = ln(1+d)
P(касание за H) = 2·(1 − Φ( b / (Vol·√H) ))        принцип отражения, снос = 0
```
Показывается лестницей 7д / 14д / 30д от **нажатой** кнопки плеча (`currentLev`), не от ИТОГА.

**Ликвидация — событие КАСАНИЯ, а не конечного значения:** принцип отражения удваивает вероятность против наивной оценки. Риск сильно back-loaded: при Vol 1 %/ч и 3X это ~0 % за 7д, 3 % за 14д, 15 % за 30д.

**Формула касания вынесена в `touchProb(vol, b, hours)` (11.08).** `liqTouchProb` стал её вызывающим: ту же меру использует стоп-в-безубыток (§3.11), и две копии принципа отражения неизбежно разошлись бы. Проверено: 1716 комбинаций (Vol × плечо × горизонт × сторона), максимальное расхождение со старым кодом = 0.

**R² сюда сознательно НЕ входит.** Позиция не захеджирована против BTC, значит ликвидацию вызывает полное движение монеты, а не только идиосинкратическая часть.

Асимметрия сторон встроена: вверх цена не ограничена, поэтому при равном плече шорт всегда рискованнее лонга (Vol 1.0 %/ч, 3X: лонг 14.6 %, шорт 29.6 %).

### 3.4 Риск маржи — четвёртый потолок, ЖЁСТКИЙ с 11.08.2026
`MAX_MARGIN_LOSS = 0.35`: выход по структурному стопу не должен стоить больше 35 % маржи. Профессиональная замена правилу «стоп не дальше 10 %»: расстояние до стопа задаёт структура монеты, ограничивается не стоп, а ПЛЕЧО.

Деление `MAX_MARGIN_LOSS / dist` живёт в единственной функции `lMoney(dist)` (инв. 20). До 11.08 оно было продублировано в карточке и на доске — прямое нарушение инварианта, устранено вместе с этой правкой.

```
жёсткий режим  ⇔  inv.capped === false
вклад в ИТОГ   =  max( lMoney(dist), L_MIN )
поля решения   =  parts.money · moneyHard · moneyBelowMin
```

**Условие ровно одно — `capped`.** Исходная формулировка §10 п.1 требовала ещё и `src ≠ 'вход'`. Проверка на живом XRP 11.08 показала, что эта клауза — произвол: при входе $1.0066 `src = мин30`, при входе $0.9700 `src = вход`, а `dist` в обоих случаях упирается в один и тот же пол 2σ = 5.29 %. Стоп математически тождественный — значит и правило обязано вести себя одинаково. С клаузой получалось, что вход НИЖЕ пробитого минимума СНИМАЕТ ограничение, то есть более рискованный вход даёт больше плеча.

**Пол 2σ входит в жёсткий режим, потолок 6σ — нет.** Тише шума стоп поставить нельзя, поэтому 2σ — честная минимальная дистанция, и считать по ней деньги законно. Уровень, обрезанный потолком 6σ, нарисованный: по нему выйти невозможно, денежное правило к нему неприменимо, строка остаётся справочной.

**Пол `L_MIN` обязателен (инв. 26).** Отношение `убыток/маржа = dist·L` не зависит от размера позиции, поэтому денежное правило говорит о ДОЛЕ СЧЁТА, а не о выживании позиции. Без пола оно превращалось в запрет торговать: в контрольной сетке из 1230 сетапов 538 получали «БЕЗ БЕЗОПАСНОГО ПЛЕЧА»; с полом — ни одного. Когда стоп не укладывается даже на `L_MIN`, поднимается `moneyBelowMin`, и доска пишет прямо: брать меньшую долю счёта, плечо тут не поможет.

**Цена включения, измеренная:** 22 % сетапов контрольной сетки получают плечо ниже; на 3243 сравнимых сетапах обеих сторон нет ни одного случая роста плеча. На XRP 11.08 ИТОГ 7X → 6X, связывающий потолок сменился с «обвал BTC» на «риск маржи».

### 3.5 FDV
`fdv_mc` в бейдже слева сверху рядом с рангом. Пороги: серый <1.5, жёлтый 1.5–3, красный >3. **Контекст риска разлоков, НЕ самостоятельный триггер лонг/шорт** — высокий FDV означает лишь, что будущая эмиссия велика относительно обращающейся, и говорит, какие монеты проверять руками на графики разлоков. Поле опционально (инв. 9); нет max supply -> не рисуется.

### 3.6 Полоса неопределённости прогноза — НЕ РЕАЛИЗОВАНО, обоснование зафиксировано
Прогноз `pred` — условное среднее только той части движения, которую объясняет BTC. Идиосинкратическая часть по построению не прогнозируется:
```
σ_idio(час) = Vol·√(1−R²)      отношение сигнал/шум = √(R²/(1−R²))
```
При типичных R² = 0.15–0.36 сигнал/шум = 0.42–0.75, то есть **собственное движение монеты превышает объяснённое BTC**. Расхождение симуляции с фактом на 5–15 % — ожидаемая ширина распределения, а не дефект модели.

Следствие: **отдельная метрика «сигнал/шум» бессмысленна — она тождественна R², который уже на карточке.** Практический ответ на этот риск дан не полосой на прогнозе, а вероятностью ликвидации (§3.3).

### 3.7 Доска CRYPTO FUTURE — рабочий стол (09–10.08.2026)
Полноэкранный оверлей (`#board`, z-index 5000), открывается кнопкой `CRYPTO FUTURE ЛОНГ/ШОРТ` с карточки. Карточка осталась витриной, доска — рабочим столом; дублирования нет по построению. Одна монета за раз, состояние сессионное.

**Порядок блоков задан Боссом 10.08 и живёт ТОЛЬКО в склейке в конце `boardHtml`.** Сами блоки считаются выше в прежнем порядке — зависимости по переменным не тронуты, переставляется только конкатенация строк. Менять порядок = переставить 12 строк.

```
1 ИТОГ·СТОРОНА·ПОТОЛОК   2 ПОЧЕМУ ЭТА МОНЕТА   3 ДИАПАЗОН 90 ДНЕЙ   4 ТОЧКА ВХОДА
5 ВЫБОР ПЛЕЧА   6 РАЗМЕР ПОЗИЦИИ   7 ГРАНИЦЫ СДЕЛКИ   8 ЦЕНА ВРЕМЕНИ
9 ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ   10 ЕСЛИ СРАБОТАЕТ   11 ЗАЩИТА ПОЗИЦИИ (11.08, §3.11)
12 ОТКУДА ПЛЕЧО   13 ДОВЕРИЕ К МОДЕЛИ
```
Блоков стало 13. «ЗАЩИТА ПОЗИЦИИ» встала одиннадцатой сознательно: 9 и 10 — это исходы (потеря / прибыль), 11 — единственное действие, которое переводит незакрытую прибыль в невозможность потерять, а 12–13 остаются методикой и диагностикой, то есть хвостом.
«СТОРОНА ПРОТИВ СТРУКТУРЫ» и «ВНИМАНИЕ» идут сразу за вердиктом: это тревоги, а не разделы, и появляются редко.

**Размер позиции — две единицы ввода (10.08).** `sizeMode ∈ {usdt, coin}`, задаётся кнопками `МОНЕТЫ · ✎ · USDT` (сетка `1fr / 62px / 1fr`, карандаш геометрически по центру). Быстрые суммы 50/100/250/500 удалены: они были жёстко привязаны к USDT.
```
Тождество: notional = qty·E = mrg·L.  Задаётся ОДНО число, второе выводится.
usdt: mrg = posMargin;  notional = mrg·L;  qty = notional/E
coin: qty = posQty;     notional = qty·E;  mrg = notional/L
```
Следствия: переключение единицы НЕ двигает объём позиции (пересчёт по тождеству в `setSizeMode`, цена входа берётся точной из `entryState`, не через округлённый атрибут). В монетном режиме смена плеча оставляет количество и меняет маржу — это правильный порядок для «хочу купить 1000 UNI».

`mrg` — действующая маржа в обоих режимах; в usdt-режиме `mrg === posMargin`, поэтому все расчёты ниже (потери, цель, funding) при старом поведении дают те же числа.

**Подсветка нажатой кнопки — единый закон доски (10.08).** Ровно одна кнопка в каждой группе горит акцентом: сторона, плечо, единица размера и **точка входа**. У точки входа горит та готовая цена, что совпала с текущей, допуск 0.25 % = половина шага кнопок −/+ (мелкий тик биржи подсветку не гасит, собственный сдвиг — гасит); ни одна не совпала → горит карандаш, это и есть «своя цена».

**Funding в деньгах (10.08).** `costUsd = |fr|·21·notional` (21 = 3 выплаты/сутки × 7 дней), что тождественно `cost% = |fr|·21·L·100` от маржи. Показываются оба: сумма крупно, процент маржи мелко под ней. Цвет всего блока = экономический эффект для НАЖАТОЙ стороны: зелёный «платят мне», красный «плачу я».

**Якорь прокрутки — обязателен (10.08).** Доска перерисовывается целиком через `innerHTML` при КАЖДОМ действии и каждые 30 с вместе с тикером. Восстановление абсолютного `scrollTop` давало «прыжок экрана»: между рендерами высота блоков ВЫШЕ точки чтения меняется — появляется/исчезает «ВНИМАНИЕ», вердикт переключается между `ИТОГ NX` и «БЕЗ БЕЗОПАСНОГО ПЛЕЧА», в «ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ» всплывает предупреждение о пороге маржи. Тот же пиксель после этого показывает другое место.

Запоминается не пиксель, а **секция под верхом экрана и смещение внутри неё**; ключ секции — текст её `.bd-h`. После перерисовки та же секция ставится на то же место. Секция исчезла → откат на прежнее поведение. `scrollTop < 4` → якоря нет, верх остаётся верхом.

**Металл на рамках (10.08).** Контур `#2a2a33` на тёмном фоне был визуально невидим. Кольцо рисуется ВТОРЫМ слоем фона: заливка блока клипуется по `padding-box`, металл по `border-box`, и в щель шириной border попадает градиент `linear-gradient(148deg, …)`. Так скругления сохраняются точно (`border-image` их ломает), а новых узлов, псевдоэлементов и масок не появляется вовсе — на доске, которая целиком перерисовывается каждые 30 с, это принципиально. Толщина линии не изменилась: 1px.

Блики почти белые (`#eef2fa`, `#e8edf7`) намеренно. Мягкий градиент на 1px при DPR 3 сливается в одну серую линию — первая, деликатная версия была отвергнута Боссом как «еле заметно». Металл читается только внутренним контрастом бликов и провалов, а не средним тоном.

**Выключатель — `:not([style])`.** Инлайновый `style` на `.bd-sec` стоит ровно у двух блоков: тревог «СТОРОНА ПРОТИВ СТРУКТУРЫ» (красная рамка) и «ВНИМАНИЕ» (янтарная). У них цвет рамки НЕСЁТ СМЫСЛ, металл бы его размыл, поэтому селектор читается как «блок без собственного цвета рамки». **Ловушка:** любая новая инлайновая правка стиля на `.bd-sec` погасит на нём металл; нужен инлайн без потери металла — вешать класс. У `.bd-hero` инлайнового стиля нет никогда (он несёт `s-pass` / `s-stop`), поэтому кольцо задано ему напрямую.

### 3.8 «ШОРТ СОЗРЕЕТ, КОГДА» (10.08.2026)
Живёт ВНУТРИ блока 2 «ПОЧЕМУ ЭТА МОНЕТА», отдельной секции нет: порядок 12 блоков и ключи якоря прокрутки (инв. 15 и 18) не тронуты. Рисуется только при `boardSide = short` и только если бот дал хотя бы одно из двух чисел.

Два условия ТЕМПА — ровно те, что прямо сейчас режут счёт шорт-кандидата в `scoreCandidate`. Раньше Босс проверял их глазами.
```
1. eff14 <= EFF_TREND (0.60)          выше -> рост шёл прямой линией, счёт x0.5
2. r7   <= r30*(7/30) - PACE_Z*sd_дн*sqrt(7)      PACE_Z = 0.25
                                      тот же порог, с которого карточка уже
                                      пишет «рост выдыхается»
```
**Пороги вынесены в константы `EFF_TREND` и `PACE_Z` и читаются обоими местами** — блоком и счётом. Захардкоженные заново, они разъехались бы, и блок начал бы показывать не тот порог, по которому реально штрафуется счёт (инв. 20).

Счётчик `N / M` в шапке: `M` — сколько условий вообще удалось проверить (нет `eff14` → `M = 1`, отдельная формулировка сводки). Цвет: зелёный при `done = known`, янтарный при частичном, серый при нуле. **Красный не используется намеренно** — «ещё не созрел» это ожидание, а не опасность.

Ограничение зафиксировано прямо в подписи блока: это условия **темпа, а не цены**. Монета, рухнувшая к минимуму 90д, честно даёт 2/2 — за цену отвечают блок ДИАПАЗОН 90 ДНЕЙ и тревога «СТОРОНА ПРОТИВ СТРУКТУРЫ»; дублировать их здесь нельзя.

Ноль новых запросов, ноль новых CSS-классов, ноль новых секций.

### 3.9 Остаток к BTC — `res7` (10.08.2026)
Недельный ход монеты раскладывается ТОЧНО на две части, без остатка:
```
r7 = mkt + own      mkt = β₉₀·btc.r7 (рыночная часть)    own = res7 (своя)
```
Зачем: счёт сравнивал монету только с ней самой (`r7` против темпа `r30`) — сравнения с рынком не было нигде. Для контр-трендового лонга у минимума «упала вместе с BTC» и «упала сама» — две разные сделки.

**Бета — по знаку РЕАЛИЗОВАННОГО `btc.r7`**, а не по слайдеру: `up_beta_90` при `btc.r7 ≥ 0`, `down_beta_90` при `btc.r7 < 0`. Слайдер задаёт гипотетический сценарий будущего, а `res7` — замер прошедших 7 суток; влиять на замер прошлого сценарий права не имеет. Разрыва в нуле не возникает: там сам множитель `β·btc.r7 → 0`.

**Следствие: на карточке эта бета может НЕ совпадать с `b=` в строке `90d:`** — та выбрана по знаку `ratio` слайдера (§3). Расхождение штатно и названо вслух прямо на доске, отдельной подписью под блоком.

Разложение пути (`up_β` по плюсовым часам BTC + `dn_β` по минусовым) отклонено (§8): на флэтовом BTC оно даёт фиктивный дрейф из асимметрии бет.

**Мера — сигма ОСТАТКА, не полная сигма монеты.**
```
σ_ост(час) = Vol·√(1−R²)                    тождество однофакторной регрессии (§3.6)
z = own / ( Vol·√H_NOISE·√(1−R²) )          H_NOISE = 168 ч — та же неделя, что у плеча
R² — ПАРНЫЙ к использованной бете: up_r2_90 / down_r2_90 (по §2 они всегда парны)
R² клипуется в [0, RES_R2_CAP],  RES_R2_CAP = 0.90 — защита от деления на почти ноль
```
Полная сигма систематически занижала бы `|z|` и глушила реальные идиосинкратические ходы: при R² = 0.42 — на 24 %. Потолок 0.90 в живых данных не срабатывает (R²₉₀ альтов к BTC = 0.2–0.6). Нет R² → откат на полную сигму: оценка выходит консервативной, ложных «своим ходом» не добавляет. Нет `volatility` → `z = null`, число показывается сырым и так и называется.

**Порог `RES_Z = 1.0`** — остаток ровно в одну свою недельную сигму. Срабатывает примерно в 32 % недель случайно: подсвеченных монет хватает для сортировки внимания, но не все подряд. Порог 0.5 отвергнут — 62 % недель, то есть не говорил бы ничего.

Четыре состояния (`cls`); подпись каждого обязана быть верной при ЛЮБЫХ знаках `own` и `mkt`:
- `own` — `abs(z) ≥ RES_Z`: ход крупнее обычного недельного разброса монеты. Это её история, а не рынка. Цвет: зелёный при `own ≥ 0`, красный при `own < 0`.
- `market` — остаток мелкий И `abs(own) < abs(mkt)`: ход недели объясняет BTC. Серый.
- `quiet` — остаток мелкий, но и рыночной части почти нет: BTC стоял, монета тоже. Серый.
- `unknown` — `z = null`: бот не дал волатильность, размер остатка не с чем сравнить. Серый.

Разделение `own`/`market` по одной лишь ДОЛЕ остатка отвергнуто: на флэтовом BTC доля вырождается в 100 % у любой монеты. **Цвет = значимость, а не сторона сделки** — серый означает «своего хода нет», а не «плохо для лонга».

**Где показывается.**
- Карточка — одна витринная строка `Своё 7д: +X.X% · Zσ` под строкой `90d:`. Видна во ВСЕХ режимах экрана, включая ОБЗОР: величина от стороны сделки не зависит (в отличие от Funding, §3.1). Разложение на карточке сознательно НЕ выводится: `btc.r7` одинаков для всех 28 карточек — это шум, а не информация; а частичные слагаемые рядом с `90d: b=` провоцировали бы сверку с ЧУЖОЙ бетой и давали расхождение на ровном месте.
- Доска — блок «СВОЁ ДВИЖЕНИЕ ЗА 7 ДНЕЙ» ВНУТРИ блока 2 «ПОЧЕМУ ЭТА МОНЕТА», выше «ШОРТ СОЗРЕЕТ, КОГДА». Своей секции нет: порядок 12 блоков и ключи якоря прокрутки (инв. 15 и 18) не тронуты. Там же полный аудит — сумма разложения, использованная бета с направлением BTC, `Zσ` и словесный вердикт.

**В `scoreCandidate` НЕ входит** — чистое отображение, на счёт, плечо и ранжирование не влияет. До стенда бэктеста (§10 п.1) это был бы ещё один непроверенный приор поверх непроверенных весов — ровно та ошибка, от которой отложен режим рынка.

Нет `r7`, нет `btc.r7` или нет нужной беты → `null` → блок не рисуется, остальная карточка живёт (инв. 9). Ноль новых запросов, ноль новых CSS-классов, ноль новых секций доски.

`RES_Z` и `RES_R2_CAP` читаются РОВНО в одном месте — `residual7()`; карточка и доска берут готовый вердикт (инв. 20).

*Историческая пометка:* в комментариях фронта функция помечена «§10 п.1» — номер пункта очереди, под которым она жила до 10.08. Пункт закрыт, **номер 1 в §10 перешёл к бэктесту** — ссылка в коде историческая и по ней теперь ведёт не туда. Чистить комментарии отдельным диффом смысла нет, но при чтении кода это надо помнить.

### 3.11 Position protection — «ЗАЩИТА ПОЗИЦИИ» (11.08.2026)

The other twelve blocks answer *"may I open this, and how big"*. This one
answers the question that only exists once the position does: **when can the
trade stop being able to lose money, and what does that cost.**

```
break-even   BE  = E·(1 ± c),   c = 2·FEE_TAKER + f,   f = ±|fr|·FUND_PAY_7D
                   sign of f = economic direction for THIS side (funding rule, §3.1)
                   c clamped to [−0.9, +0.9] — pathological-rate guard only
arm price    ARM = E·(1 ± ARM_R·dist),  dist from invalidationInfo (§3.2)
                   never closer than BE — below BE a "break-even stop" locks a loss
scratch      P   = touchProb(|ln(ARM/BE)|, H_NOISE)        reflection principle, §3.3
                   armed → the row switches to |ln(cur/BE)|: the question is "from here"
top-up       add = notional/L_ceiling − mrg → liquidation moves to liqPrice(E, L_ceiling)
```

`FEE_TAKER = 0.0005` · `FUND_PAY_7D = 21` · `ARM_R = 1.0`.

**Why 1R and nothing else.** R — the distance from entry to the structural stop
— is the only risk unit this system actually measures. Any other trigger
(a fixed %, a fixed σ multiple, a "trailing" rule) would be a new invented
constant. 1R is also the classic break-even rule, so it costs no novelty.

**Taker on both legs.** A stop exit is a stop-MARKET order, i.e. taker by
construction; charging the entry as taker as well errs to the safe side of
break-even. Round trip = 0.10 % of notional = 0.10 %·L of margin.

**Seven days everywhere.** Funding is extrapolated over the same horizon the
leverage engine and the funding block already use, so the three blocks cannot
disagree. Holding longer moves break-even further; the block says so in words
rather than inventing a second horizon (the 7д/30д switch stays rejected, §10).

**No threshold on the scratch probability — deliberately.** Whether a 47 %
chance of scratching is worth removing the stop risk depends on the Boss's own
hit rate, which the system has never measured (§8, «Вероятность TP раньше SL»).
A traffic light here would look like a measured verdict without being one, so
the block prints the price and leaves the decision. This is the same restraint
that keeps `res7` out of `scoreCandidate` (§3.9).

**The scratch number is the point of the block.** Moving a stop to break-even
is normally believed free. It is not: on XRP-like inputs (Vol 0.9 %/h, 1R =
9.1 %) noise drags price back to break-even within 7 days in **47 %** of weeks.
The system could always compute this; nothing on the board ever said it.

**No money figure is repeated.** The dollar loss at the structural stop belongs
to «ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ»; here it appears only as a share of margin inside
one sentence. Funding in dollars belongs to «ЦЕНА ВРЕМЕНИ»; here it is folded
into break-even and named, not restated (§3.7, no duplication by construction).

**Margin top-up is the only lever an open position still has.** Leverage is
fixed at entry; effective leverage is not. The line appears only when the
pressed leverage exceeds the ceiling, and it is phrased conditionally («если
позиция уже открыта») because the board is also a planner.

**Degenerate cases are named, not hidden.**
- `inv.capped` (6σ) → the arm inherits a drawn stop; the sub-line says so, same
  honesty as §3.4 refusing money rules on a drawn level.
- costs ≥ 1R → the arm collapses onto break-even, the probability row is
  dropped (a 100 % touch of the level you are standing on is not information),
  and the sub-line states that 1R does not cover costs.
- no `volatility` → probabilities disappear, break-even survives.
- no invalidation level → break-even alone; the status line says the arm has
  nothing to be measured from (invariant 9).
- funding rate absent → break-even carries fees only, and says so.

**Exactly one probability on screen at any time.** Before the arm price the row
shows the plan (`pArm`); once armed it shows the situation (`pNow`). Two
near-identical percentages side by side read as a contradiction, not as detail.

Zero new API calls · zero new CSS classes · zero new state · `scoreCandidate`,
the leverage engine and the ranking are untouched: pure display over
measurements the system already had.

## 3.10 Стенд бэктеста скоринга — `bench/backtest_bench.py`

Отдельный файл, продакшн не трогает. Отвечает на один вопрос: сортирует ли
`scoreCandidate` монеты лучше жребия.

**Устройство.** Ноль копий продакшн-математики. При каждом запуске стенд
вырезает `scoreCandidate` + `has/clamp01/sigmaDay/volRegime` + `EFF_TREND/
PACE_Z/VOL_ABNORMAL` прямо из `index.html` и исполняет настоящим node; поля
`cur/min/max/volatility/r7/r14/r30/vol7/eff14/vol_ratio` считает блоком,
вырезанным через AST из `get_token_betas` в `main.py`, вместе с
`window_stats/window_vol/volume_expansion`. Правка любого из двух файлов
меняет стенд автоматически.

**Данные.** Архив `data.binance.vision` (месячные ZIP, 3 года часовых свечей),
хвост добирается зеркалом `data-api.binance.vision`. Список пар — из
`tokens[]` фронта, разбирается через node.

**Метрика.** Цель — избыточная доходность к среднему по списку: счёт решает
«какую из 28 взять», а не «куда пойдёт рынок». IC = ранговая связь счёта с
будущим по каждой дате, среднее по датам, ДИ блочным бутстрапом. Плюс ТОП-3
против среднего, худшая просадка внутри окна по третям счёта и три контроля:
перемешанный счёт, «только близость к мин90», «только r7».

**Режимы запуска:** `--probe` (доступность источников, 20 с) · `--selftest`
(офлайн, синтетика с известным ответом) · `--fetch` · `--verify` (сверка с
живым `coeffs.json`) · `--run` · `--regimes`.

**`--verify` — единственный режим, способный ошибиться в ОПАСНУЮ сторону**, то
есть напечатать «совпадает» там, где не совпало или не сверялось. Правила
режима, закрытые тестами (`bench/verify_bench.py`, 29 проверок, сеть не нужна):

| Правило | Зачем |
|---|---|
| Мера выбирается по ТИПУ поля: уровни `rel` (%), доходности `pp` (проц. пункты), `eff14` `abs` | относительная ошибка на поле, пересекающем ноль, бессмысленна: `r14` = 0.001 против 0.0155 печаталось как 1449 % при реальном расхождении 1.4 пункта |
| Код возврата ненулевой при любом провале | прежде был всегда 0: `verify_against_live` ничего не возвращала, и `sys.exit(main() or 0)` давал ноль даже под надписью «ВЫШЛИ ЗА ПОРОГ». В шаге workflow упавшая сверка выглядела зелёной — тот же класс, что инв. 25 |
| Считаются сверки ПО КАЖДОМУ ПОЛЮ, не только монеты | поле, которого нет в живом `coeffs.json` ни у одной монеты, сравнивалось ноль раз, оставляло `worst = 0.0` и проходило порог. Инвариант 22 на уровень ниже: сначала посчитать сравнения, потом судить |
| Поля, не сравнимые из-за разрыва во времени, названы в вердикте | «совпадает» без оговорки печаталось и тогда, когда четыре поля из одиннадцати не сверялись вовсе. Разрыв — штатное состояние архива (он отстаёт ~сутки), поэтому шаг не падает, но и полного согласия не заявляет |
| Файлы кэша с `_` в начале пропускаются | `--run --quality-const` штатно хранит `_quality_today.json` в том же каталоге; чтение `["prices"]` из него роняло всю сверку с `KeyError` |

**`--selftest` ниже десяти посевов даёт ЛОЖНУЮ тревогу** и это ожидаемо:
нулевой мир признаётся чистым по условию `|IC| < SE` одного прогона, а на
двух посевах среднее ещё не устоялось. Ошибка направлена в безопасную
сторону (стенд объявляет себя неисправным, а не здоровым). Судить по
десяти посевам, как и заложено по умолчанию.

**Самопроверка обязательна перед доверием к цифрам.** Три мира: чистое
блуждание (эталонный фактор обязан дать 0), возврат к среднему (+), импульс
(−); по 10 посевов, потому что при SE(IC) ≈ 0.03 один посев уходит на 2 SE
примерно в каждом двадцатом прогоне. Плюс проверка на отсутствие взгляда в
будущее: запись на дату t из полного ряда обязана побайтово совпасть с
записью из ряда, обрезанного по t.



### 3.10a Experiment lab — three pre-registered measurements (12.08.2026)

Additive modes of `bench/backtest_bench.py`; production untouched. Rules
registered BEFORE any real data (inv. 23). One PRIMARY claim per experiment;
every other cell is exploration at the doubled bar the regime study set
(|IC| >= 0.10, CI99). Multiplicity is named: three primaries in one session,
so any single positive at 0.05 carries a family-wise caveat in its verdict
line. **A positive primary wires NOTHING into the product by itself: the
standing gate is a fresh confirmation run after +26 weeks of new data.**

**A. `--stops` — honesty of the invalidation layer.** Per (weekly date, coin,
side): production `invalidationInfo` gives the stop; the next 7d of exchange
high/low decide whether it was TOUCHED; production `touchProb` gives the model
figure for the same barrier. PRIMARY: pooled per-side calibration ratio
measured/model. CI95 contains 1.0 → normal model honest at 7d; lower bound
> 1.0 → tails heavier, board probabilities understate — record the multiplier
in §7; upper bound < 1.0 → model errs safe, no action. Hit and whipsaw rates
(touched, then back at entry within 7d AFTER the touch) are DESCRIPTIVE — no
auto-thresholds; acting on them is a separate, separately-argued change.
Requires high/low in cache → cache format extended additively (`hl` key),
workflow cache key v3 → v4. CoinGecko-sourced cache has no OHLC and is
refused with an explicit message (inv. 22 direction).

**B. `--res7` — residual-vs-BTC as a ranking factor.** Rolling 90d up/down
betas+R² are built from the SAME bot functions (`bucket_prices`,
`paired_hourly_returns`, `fit_stats`, `asymmetric_beta`, AST-cut; the ≥120
matched-hours guard restated from §2 because it lives in request plumbing);
`residual7()` itself is executed from `index.html` (inv. 21 both sides).
PRIMARY: LONG · 7d · contrarian orientation (factor = −z: fell on its own →
long candidate), bar identical to the scoring study — IC ≥ +0.05, CI95 clear
of zero. Momentum orientation, short side, 3/14d and the r30 factor are
exploration.

**C. `--funding` — crowding as a directional factor.** Data: monthly
`fundingRate` ZIPs from `data.binance.vision` (futures/um), ~36 files × pair,
cached as `_fund_SYM.json` (the `_` prefix keeps them out of `load_cache`,
same convention as `_quality_today.json`). Factor (registered): z of the
3-day mean funding (9 prints) within its trailing 30-day distribution.
PRIMARY: SHORT · 7d — crowded longs → future underperformance; IC ≥ +0.05,
CI95 clear of zero. Raw-level variant, long mirror, 3/14d are exploration.
Archive lags ~1 day and the current month has no monthly file; the trailing
window at the newest dates is marginally short — measured, not modelled.

**Lab selftest (`--lab-selftest`) — known-answer worlds, offline:**
flat-vol GBM with substep-built high/low → stops ratio must read 1 (reads
0.93–0.98, CI covers 1); wick world (one-sided intra-hour spikes invisible to
close-based σ — the stop-hunt error class) → ratio must exceed 1 (reads
1.45–1.63, lower CI > 1); resnull/resrev worlds → res7 must read 0 / strongly
positive (−0.013 / +0.345), synthetic β = 0.7 recovered as 0.67; uncoupled /
coupled funding worlds → 0 / +0.24…0.27. Two lessons recorded during control
construction, before real data: (1) volatility clustering at the 2σ floor
pushes the stops ratio BELOW 1 (touch prob is concave in σ near 40–55 %), so
a real ratio < 1 is explainable by clustering and errs safe; (2) symmetric
diffusive jumps land inside the estimated σ — the barrier scales with it and
the ratio stays ≈ 1; only wick-like moves the close never sees can push it
above 1, which is exactly what the primary exists to catch.

**Results (12.08.2026, run №4 — first clean pass through all three).**
Basis: 145 weekly dates (144 where the window shortens), ~24.4 coins/date,
3y hourly candles with exchange high/low (cache v4); funding 27/28 (GRAM
excluded, 178 payments); 12 setups excluded for dist ≥ 100 % (the 12d
counter printing its real population). Selftest 10 seeds green, lab
selftest green, verify green with the fut basis lane informative.

- **A. `--stops` PRIMARY: normal model HONEST at 7d, both sides.**
  LONG n=3492 (med dist 15.1 %): hit 17.7 % vs model 20.2 %, ratio
  0.88 [0.68; 1.07]. SHORT n=3504 (med dist 19.3 %): hit 18.3 % vs
  model 20.7 %, ratio 0.88 [0.74; 1.03]. Both CI95 contain 1.0 → no §7
  multiplier. The sub-1 direction matches recorded lesson 1 (volatility
  clustering; errs safe). Descriptive, no action per registration:
  whipsaw 35 % / 42 % of stopped setups back at entry within 7d; the
  only cell where measured exceeds model is the 6σ-capped LONG bucket
  (3.5 % vs 0.9 %, n=681) — far tail, absolute gap 2.6 pp, consistent
  with the fat-tail prior in §7; SHORT capped bucket aligned (4.6/4.8).
- **B. `--res7` PRIMARY: NULL.** LONG·7d·contrarian IC −0.009
  [−0.048; +0.030], shuffled control −0.002. Fails IC ≥ +0.05. All 11
  exploration cells (3/14d, momentum, short, r30) fail the doubled bar;
  largest |IC| = 0.032. Consequence: `residual7` stays display-only
  (§3.9, inv. 27 class) — never enters `scoreCandidate`. Measured zero.
- **C. `--funding` PRIMARY: NULL.** SHORT·7d crowding-z IC +0.003
  [−0.030; +0.039], control −0.017. Fails the bar. All 8 exploration
  cells fail; largest |IC| = 0.030. Consequence: no crowding factor in
  the product; funding remains a cost (ЦЕНА ВРЕМЕНИ, безубыток) plus
  the existing ×1.05 short-score touch — unchanged.

Three primaries, all null → the registered family-wise caveat (for
positives) is moot; the +26-week confirmation gate has nothing queued.

**Rank-1 follow-up (13.08.2026, computed from `run_raw.json` of the same
run — the Boss's candidate-selection question asked directly).** 14d
horizon (the raw dump's horizon; IC verdicts at 3/7/14d are all null in
the main report, so the conclusion is horizon-independent), 144 weekly
dates. LONG: №1 excess over list mean +0.59 % [−1.83; +3.08], №2–3
+1.24 % [−1.31; +4.17]; №1 beats list median 50 % of dates; №1 lands in
the top quartile of realized outcomes 20 % (base 25 %); the best
realized mover sat in the BOTTOM half of the ranking 51 % of dates
(base 50 %). SHORT: №1 excess +0.70 % [−2.46; +3.93], №2–3 −0.51 %;
beats median 48 %; top quartile 33 %; best mover in bottom half 43 %.
Every cell is a coin flip; №2–3 above №1 on the long side is noise
demonstrating the same thing. **The ordering carries no information —
the ranking is a geometry/risk shortlist, not an opportunity detector,
and №1 does not deserve directional trust over №5.**

Both live directional hypotheses from §10 are now measured zeros: the
directional layer remains human (catalysts + REVIEW) by design, and the
tool's edge — risk, sizing, honesty — is confirmed as a result, not a
fallback. Re-running a lab mode requires a new external argument, not a
re-roll of the same data.

## 4. Инварианты — НЕ ЛОМАТЬ
1. Схема `coeffs.json` — только аддитивные изменения; `err_result` в боте синхронен по ключам с успешным результатом.
2. Новые монеты — только `TOKENS` (бот) + `tokens[]` (фронт). Проверять: id CoinGecko, спот-пару, фьюч, квоту. Нет спот-пары, есть перп → обязателен `fut:true`.
3. `history.json` ≤ 720 точек; чтение с обработкой `truncated` через `raw_url`.
4. `STALE_WARN 75` / `STALE_CRIT 130` мин ↔ часовой cron; менять только парой.
5. Тикер `?symbols=`: HTTP 400 → залипание на полном тикере 1.2 МБ до перезагрузки. Делистнутые чистить, futures-native помечать `fut:true`.
6. `applySavedOrder`: новые монеты встают в конец сохранённого порядка.
7. Пароль на клиенте — декорация. Секреты — только env GitHub Actions.
8. Все `requests` бота — `timeout=30`.
9. Фронт обязан переживать отсутствие любых новых полей coeffs (обе комбинации бот↔фронт рабочие).
10. Ребрендинг монеты: менять display-имя и пару Binance; **CoinGecko id СОХРАНЯТЬ** (id постоянные, новый id = потеря 90д-истории).
11. Три защитных состояния карточки: «НЕТ ПАРЫ» · «ТОРГИ ОСТАНОВЛЕНЫ» (count=0 или пустой стакан → расчёты отключены) · жёлтое «Расхождение источников» (цена вне 0.5×min…1.5×max).
12. `fut:true`-токены: цена только из `cachedFutTickers`, исключены из спот-`?symbols=`; детектор мёртвого рынка работает только по `count`.
13. **Расчёт плеча — валидированная математика, менять только с полным пересчётом стенда.** Три потолка (§3.2), горизонт 7 суток у всех трёх, минимум, округление ВНИЗ. Риск маржи — четвёртый, справочный, в ИТОГ не входит (§3.4).
14. **Всё, чем управляет Босс, обязано идти от `currentLev`.** Баг 09.08: блок ЦЕНА ВРЕМЕНИ считал от ИТОГА, игнорируя нажатую кнопку — цена ликвидации менялась, а вероятности и funding оставались от прежнего плеча.
15. Порядок блоков доски живёт ТОЛЬКО в склейке в конце `boardHtml` (§3.7). Блоки считаются в прежнем порядке — переставлять код блоков нельзя, там зависимости по переменным (`notional`, `qty`, `mrg`, `qtyTxt` объявлены в блоке размера и используются ниже).
16. **Единица размера — тождество `qty·E = mrg·L`.** Задаётся одно число, второе выводится; переключение `sizeMode` не меняет объём позиции. Цена входа для пересчёта берётся из `entryState`, не из округлённого HTML-атрибута.
17. **Ровно одна кнопка в группе горит акцентом** (сторона, плечо, единица размера, точка входа). Допуск подсветки входа 0.25 % привязан к шагу кнопок −/+ 0.5 %: менять только парой.
18. **Прокрутка доски восстанавливается ЯКОРЕМ по секции, не абсолютным `scrollTop`.** Любая правка, меняющая высоту блоков выше точки чтения, без якоря вернёт «прыжок экрана». Ключ якоря — текст `.bd-h`: он обязан оставаться уникальным в пределах доски.
19. Мигание Min/Max и бегущие рамки краёв — Боссом одобрены, не удалять; логику можно только предлагать улучшить.
20. **Пороги — по одному числу на систему.** `EFF_TREND` и `PACE_Z` читают и `scoreCandidate`, и блок «ШОРТ СОЗРЕЕТ, КОГДА» (§3.8); `RES_Z` и `RES_R2_CAP` читаются ровно в одном месте — `residual7()` (§3.9), а карточка и доска берут готовый вердикт. Порог, захардкоженный во втором месте, рано или поздно разойдётся с первым, и экран начнёт объяснять счёт неверным числом.
    С 11.08 сюда же: `FUND_PAY_7D` (21 выплата за 7 дней — читают «ЦЕНА ВРЕМЕНИ» и безубыток §3.11; до правки литерал `21` стоял в двух строках подряд), `FEE_TAKER`, `ARM_R`, а также функции `touchProb()` (одна формула касания на систему) и `probTxt()` (одно округление вероятности в текст).

21. **Стенд не содержит копий продакшн-математики.** Формулы вырезаются из
    `index.html` и `main.py` при каждом запуске. Копия, вставленная в стенд
    руками, разойдётся с продакшном молча, и бэктест начнёт проверять код,
    которого нет в проде.
22. **Проверка, проходящая при отсутствии данных, запрещена.** `--verify`
    при пустом кэше печатал «расхождение 0.00% → совпадает с продакшном»,
    не сверив ничего. Любой валидатор обязан считать число сверенных
    объектов и падать на нуле. Тот же класс, что «показывает ≠ применяет».
23. **Правила эксперимента фиксируются ДО данных, реализация правила
    проверяется контролем с известным ответом ДО реальных данных.** Наивная
    регрессия уровня цены по времени называла трендом 70 % чистых случайных
    блужданий — правило Босса было верным, сломана была реализация. Поймано
    синтетикой до прогона; замена после результата была бы подгонкой.
24. **Боевые хосты Binance из GitHub Actions недоступны — HTTP 451**
    (раннеры в США, США в списке ограниченных территорий). Работают только
    архив `data.binance.vision` и зеркало `data-api.binance.vision`. Любой
    новый код, ходящий на `api.binance.com` из Actions, отвалится.
25. **`| tee` в шаге workflow возвращает код `tee`, а не Python.** Без
    `set -o pipefail` упавший шаг выглядит зелёным, а отчёт уезжает пустым.
    Во всех шагах стенда стоит `shell: bash -euo pipefail`.
29. **Проверяющий режим обязан возвращать код выхода.** Функция без `return` даёт `None`, `sys.exit(main() or 0)` превращает его в ноль, и провалившаяся сверка выглядит успешной — при этом на экране честно напечатано «ВЫШЛИ ЗА ПОРОГ». Печать не является кодом возврата. Родственник инв. 25 (`| tee` съедал код Python) и инв. 22 (проверка без данных): все три — один и тот же способ соврать зелёным.
28. **Класс, собираемый конкатенацией, невидим для текстового поиска.** В `renderButtons` живут ровно два таких места: `'side-btn' + ' a-' + mode` (mode = long/none/short) и `'stress-btn' + ' s-' + mode` (mode = normal/panic/crash). Поиск по файлу строк `a-long` или `s-panic` не находит НИЧЕГО — при чистке 11.08 они попали в список «мёртвых» и были бы удалены вместе с подсветкой нажатой стороны и режима стресса. Любая будущая чистка CSS обязана разрешать такие сайты по перечислению ИХ СОБСТВЕННОГО цикла: объединение двух перечислений в одно даёт обратную ошибку — выдумывает `s-long`/`s-short` и прячет настоящих сирот. Проверка автоматизирована в `bench/clean_bench.py`.
27. **«ЗАЩИТА ПОЗИЦИИ» — чистое отображение.** Ни один её выход не входит в плечо, счёт, ранжирование и уровень инвалидации: она только читает уже посчитанное. Тот же класс, что `res7` (§3.9). Если когда-нибудь понадобится, чтобы защёлка влияла на решение — это отдельная правка с отдельным обоснованием, а не расширение блока.
26. **Денежный потолок не убивает сделку.** `риск маржи` участвует в `min`, но с полом `L_MIN`: `убыток/маржа = dist·L` не зависит от размера позиции, то есть это правило про ДОЛЮ СЧЁТА, а не про выживание. «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» имеют право выдавать только три первых потолка.

## 5. Лимиты
- **CoinGecko: бот ходит БЕЗ КЛЮЧА.** В `main.yml` в env передаётся только
  `GIST_TOKEN`, `COINGECKO_API_KEY` не передаётся → `api_key=None` →
  публичный доступ без месячной квоты, ограничение по IP раннера, обходится
  паузой `REQUEST_GAP_SEC = 1.0` и тремя попытками. Проверено 10–11.08:
  `error = null` у всех 28 монет.
- **Бесплатный ключ Demo подключать НЕЛЬЗЯ при нынешнем расписании.** Demo
  даёт 100 вызовов/мин, но потолок 10 000/мес. Расход: 18 запусков в день ×
  30 вызовов ≈ 16 700/мес, плюс триггер `push` гоняет полный прогон бота на
  каждый коммит. Ключ Demo СОЗДАСТ обрыв около 19–20 числа, которого сейчас
  нет. Подключать только вместе с сокращением до ≤ 10 запусков в день.
- Binance спот-тикер с symbols: weight 40, ~12 КБ (полный: weight 80, ~1.2 МБ).
- Binance fapi `ticker/24hr?symbol=`: weight 1 × число `fut:true`-токенов каждые 30 с.
- Gist API: файлы > 1 МБ — truncated (решено через raw_url).

## 6. Чек-лист релиза
1. `python3 -m py_compile` бота; `node --check` извлечённого `<script>`.
2. `debug.json`: у всех монет `matched_90d > 120`, `returns_14d ≳ 300`, `error = null`.
3. Фронт: карточки без NO DATA / NO BETA; Conf, ρ, MDL и оба R² с цветом; края слайдера → `pred > 0`.
4. `fut:true`-карточки: цена приходит, спот-список их не содержит (тикер ~12 КБ, не 1.2 МБ).
5. Доска: порядок 12 блоков (§3.7); в каждой группе горит ровно одна кнопка; `notional` не меняется при переключении МОНЕТЫ/USDT; смена плеча в монетном режиме двигает маржу, а не количество; funding показывает и сумму, и процент маржи; ЦЕНА ВРЕМЕНИ считает от нажатой кнопки, а не от ИТОГА (инв. 14).
   Эталон стенда 10.08 (UNI, E = $10.00, 4X): 1 000 USDT → объём $4 000, 400 UNI. Переключение в монеты → 400 UNI, маржа $1 000, объём тот же. `qty = 1 000` → объём $10 000, маржа $2 500; на 2X маржа $5 000, объём прежний. Funding +0.0100 %/8ч при объёме $11 110 → $23.33 за 7 дней.
6. Доска в режиме ШОРТ: блок «ШОРТ СОЗРЕЕТ, КОГДА» показывает счётчик `N / M` и оба порога; в режиме ЛОНГ его нет вовсе; на `coeffs.json` без `eff14`/`r7`/`r30` блок исчезает целиком, остальная карточка живёт.
7. Совместимость в обе стороны (инвариант 9).
8. `coeffs.json`: у объекта `btc` присутствуют `r7/r14/r30` и они не `null`; фронт на СТАРОМ `coeffs.json` без этих полей работает без ошибок (инв. 9).
9. Доска, рамки (§3.7): у всех 12 блоков и у героя виден металлический контур; у тревог «СТОРОНА ПРОТИВ СТРУКТУРЫ» и «ВНИМАНИЕ» рамка остаётся красной и янтарной БЕЗ металла; скругления углов целы.
10. Остаток к BTC (§3.9): на карточке строка `Своё 7д` с сигмой, видна и в ОБЗОРЕ; на доске блок «СВОЁ ДВИЖЕНИЕ ЗА 7 ДНЕЙ» внутри «ПОЧЕМУ ЭТА МОНЕТА»; `рынок + своё` сходится с `r7` до отображаемого знака; на монете без `up_beta_90`/`down_beta_90` блок исчезает, остальная карточка жива; при `sc = null` секция «ПОЧЕМУ ЭТА МОНЕТА» остаётся и прямо пишет, что счёт не посчитан.

- При правке `verify_against_live` — прогнать `bench/verify_bench.py`
  (офлайн, сеть не нужна, ~20 с). Стенд обязан давать 0 отказов; на файле
  до правки 11.08 он даёт 8 — это его собственная проверка на пригодность.
- При правке `scoreCandidate`, `window_stats`, `window_vol` или
  `volume_expansion` — прогнать `bench/backtest_bench.py --selftest`.
  Стенд вырезает эти функции из продакшна; если самопроверка перестала
  проходить, сломана продакшн-математика, а не стенд.
13. **Защита позиции (§3.11):** блок стоит одиннадцатым, между «ЕСЛИ СРАБОТАЕТ» и «ОТКУДА ПЛЕЧО»; безубыток дальше входа при funding «плачу я» и ближе входа при «платят мне»; при цене на входе строка статуса пишет «цена на входе»; на монете без `volatility` исчезают только вероятности; на `coeffs.json` без `min30/max30` защёлка считается от 90д-опоры, при обрезке 6σ подписана как нарисованная; металлический контур у блока есть (инлайнового `style` на его `.bd-sec` нет).
12. **Жёсткий потолок риска маржи (§3.4):** при `capped = true` четвёртая строка ОСТАЁТСЯ справочной и маркера «← ограничитель» не получает, подпись — «Три независимых потолка…»; при `capped = false` она стоит в общем списке, способна связать ИТОГ, подпись — «Четыре…». Ни при каких данных она не даёт «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» (инв. 26).

## 7. Осознанные упрощения
- Бета на simple-returns ≈ log-returns на часовом шаге.
- Ликвидация: один MMR = **1.25 %** для всех, без тиров/комиссий/funding. (До 10.08 в этой строке стояло 1 % — расхождение с §3 и кодом, где `LIQ_MMR = 0.0125` с 09.08. Исправлено.)
- ~~Буфер 13 % (0.87/1.13)~~ — **упразднён 09.08.2026** вместе со старым движком. Заменён явным запасом на реакцию `1.645·Vol·√12` внутри структурного потолка: та же идея, но выраженная в измеренной волатильности монеты, а не в выбранной константе.
- Запас на реакцию 12 ч — оценка «сколько позиция может стоять без присмотра» (сон, работа). Не измерена, выбрана. Прямо задаёт структурный потолок: удвоение H_REACT режет плечо примерно на четверть.
- Диапазон min/max на карточке — 90д; опора инвалидации — 30д (мин30/макс30) с откатом на 90д.
- Funding в деньгах считается по ТЕКУЩЕЙ ставке, экстраполированной на `FUND_PAY_7D` = 21 выплату. Ставка плавающая — это оценка, а не обязательство биржи. То же допущение переносится в безубыток (§3.11).
- Комиссия одна для всех: `FEE_TAKER` = 0.05 % за ногу, обе ноги тейкером, без VIP-уровней, скидки за BNB и без проскальзывания. Ошибка направлена в безопасную сторону (реальный безубыток ближе, а не дальше). Тот же принцип, что один `LIQ_MMR` на все монеты.
- Lag BTC→alt не моделируется: часовые бары грубее реального лага; вернуться при переходе на минутные данные.
- Альфа (интерсепт регрессии) не экстраполируется — на 14д не отличима от нуля.
- Разлоки НЕ автоматизированы сознательно.
- Вероятность ликвидации (§3.3): нормальное распределение и постоянная волатильность. Хвосты крипты толще нормальных, кластеризация волатильности не моделируется -> **истинная вероятность выше расчётной**, оценка на 10 % — нижняя граница риска. Снос принят нулевым (для 30д при этих Vol он мал против σ√H).
  **Измерено 12.08.2026 (§3.10a Results):** на 7д и типовых дистанциях инвалидации (2σ–6σ) та же формула касания откалибрована честно и даже консервативно (факт/модель 0.88, ДИ95 накрывает 1 на обеих сторонах — кластеризация давит вниз, ошибка в безопасную сторону); дальний хвост за обрезкой 6σ подтверждает прежний вывод — факт 3.5 % против модели 0.9 % на лонге. Формула нижней границы остаётся нижней границей именно там, где стоят стопы дальше 6σ.
  **Кредитовать 0.88 в расчёты — ОТКЛОНЕНО 13.08.2026.** Три причины, любой одной достаточно: (1) ДИ95 накрывает 1 — статистического основания нет; (2) занижение объясняется кластеризацией волатильности, то есть поправка ломалась бы ровно в режиме расширения — когда риск и важен; (3) `touchProb` не входит в плечо вовсе (все четыре потолка — дистанционные, §3.2/§3.4), а на показ вероятностей полный кредит 0.88 сдвинул бы эквивалент плеча меньше чем на 3 % — внутри округления вниз. Модель остаётся некорректированной сознательно.
- Оценка Vol по 90д очень точна (SE ≈ 1.5 % при 2160 точках), но это оценка ПРОШЛОГО. Ошибка прогноза Vol на следующие 30 дней ±30 % даёт ±20…35 % по плечу: различие 2X и 3X лежит внутри шума, поэтому округление ВНИЗ обязательно.

- **Стенд восстанавливает 82.5 % веса лонга и 86 % шорта.** Ранг
  капитализации и оборот Binance исторически недоступны, поэтому блок
  качества считается по одному `vol_ratio` из трёх компонент — штатным путём
  продакшна (инв. 9), а не заглушкой. Ранг и оборот меняются по списку
  медленно, их вклад — почти постоянный наклон, на порядок монет во времени
  влияет слабо.
- **Сверка с продакшном сходится на 25 монетах из 28.** При выровненных
  метках времени (разрыв −0.6 ч) медиана расхождения: цены 0.06–0.12 %,
  `r7` 0.32 пп, `r14` 0.26 пп, `r30` 0.31 пп, `eff14` 0.02.
  **Расходятся ровно три монеты — HYPE, XMR, LIT, то есть все `fut:true`:**
  стенд берёт цену перпетуала Binance, CoinGecko — спотовый индекс, и базис
  даёт до 7–9 пп на доходностях. Это ожидаемое свойство источника, не ошибка
  расчёта. Отдельный выброс — `volatility` XLM 12.4 % при медиане 0.97 %.
  На вывод бэктеста не влияет: внутри прогона вход, выход и метрики берутся
  из одного ряда, а доминирующая компонента счёта `pPos` (вес 0.50) стоит на
  уровнях и волатильности, которые сошлись.

## 8. Отклонённые идеи — не предлагать повторно без новых аргументов
| Идея | Причина отказа |
|---|---|
| 5д-бета/R² | SE(β) на 5д = ±17…31 % против ±10…18 % на 14д: добавляет дисперсию, а не информацию. Ошибка прогноза определяется идиосинкратической частью (§3.3), а не точностью беты |
| Метрика «сигнал/шум» отдельным числом | тождественна √(R²/(1−R²)) — дубль уже показанного R² |
| Автоматизация разлоков | нет надёжного бесплатного источника, даты плавают, касается ~5 монет |
| TVL | применим к четверти списка, меняет убеждение за недели — материал для REVIEW, не для карточки |
| Ликвидность фьючерсов | на топ-перпах Binance размер Босса не двигает стакан; мёртвый рынок ловит детектор |
| Token Identity Layer | over-engineering |
| Аврора (анимация при входе в ЛОНГ/ШОРТ) | реализована и **удалена 10.08 по решению Босса**. `mix-blend-mode: screen` поверх тёмной темы поднимал не цвет, а серый: получалась молочная дымка на верхней половине экрана вместо цветного сияния. Плюс два размытых слоя 200%x220% при DPR 3 — десятки МБ текстур на GPU. Возвращаться только с полноэкранной версией без blend-mode и без гигантского blur |
| Подсветка «рекомендуемой» кнопки плеча глобально | рекомендация индивидуальна для каждой монеты; глобальная кнопка не может её отражать |
| Карта ликвидаций (кластеры + OI + цена) | Бесплатного источника нет: тепловые карты Coinglass и аналогов — модель, восстановленная из OI и цены, а не данные биржи; Binance по `forceOrder` отдаёт не более одной ликвидации в секунду на символ, то есть заведомо неполную выборку. Второе и главное: сквизы живут часы, удержание Босса 1–14 дней — масштаб времени не совпадает. Полезный остаток («новые деньги / закрытие позиций») уже стоит в §10 как Open Interest |
| Вероятность «TP раньше SL» | Без сноса вероятность коснуться цели раньше стопа равна `b/(a+b)` — тождественна отношению риск/прибыль из блока ГРАНИЦЫ СДЕЛКИ. Снос система оценить не может (§3.6): при R² 0.15–0.36 сигнал/шум 0.42–0.75. Число выглядело бы измеренным преимуществом, не будучи им. Единственная новая величина — `P(за 7д не задета ни одна граница)`, стыкуется с ценой funding; опционально, низкий приоритет |
| Спот/перп базис | `premiumIndex` уже отдаёт `markPrice` и `indexPrice` — ноль новых запросов. Но mark price на Binance считается из того же премиум-индекса, что и funding: базис и funding механически одна величина в двух видах, а funding уже на доске |
| Подгонка весов `scoreCandidate` | Измеренный ноль на 3 годах и 28 монетах при достаточной мощности (§10, «Сделано»). Крутить веса под нулевой результат — чистое переобучение. Правило «не трогать веса ни при каком исходе» было зарегистрировано ДО прогона и соблюдено |
| Режим рынка как выключатель скоринга | Правило «тренд = снос BTC за 90д значим» даёт вырожденное деление: 13 трендовых дат против 132 диапазонных за 2.75 года. По корректно сформулированному критерию крипта почти всегда в диапазоне. Другое определение, выбранное ПОСЛЕ этого результата, было бы подгонкой под выборку |
| CoinGecko как источник для стенда | Бесплатный тариф: 365 дней истории → 39 дат → различимо только \|IC\| ≳ 0.060. Годится для сверки, не для теста |

## 9. Журнал миграций
- 2026-08-13: **directional-intelligence audit — layer CLOSED; leverage
  calibration — leave unchanged. Map-only diff, zero code.** (1) Rank-1
  follow-up computed from run №4's own `run_raw.json` answers the Boss's
  candidate-selection question directly: №1 vs №2–3 vs the list is a coin
  flip on every metric, both sides (numbers in §3.10a Results) — the
  ranking is a geometry/risk shortlist and its ordering carries no
  directional information. (2) Full technology landscape reviewed; nothing
  clears the evidence bar for this system; positioning/OI backtest decided
  NOT run now (conditional prior < 10 % after funding-zero) but recorded as
  the mandatory pre-gate if the deferred OI feature ever proceeds — §10.
  (3) Crediting the 0.88 stop-touch calibration into anything — rejected,
  three independent reasons in §7; `touchProb` is not a leverage input
  (verified in code: `leverageDecision` contains none), so the effect on
  recommendations is zero by construction; the felt restrictiveness of
  recent verdicts is the deliberate §3.4 money cap (22 % of grid setups
  lower), not touch-model miscalibration.
- 2026-08-12e: **lab run №4 — first clean pass; all three verdicts
  rendered, ZERO product changes.** Verdicts per the pre-registered
  rules, read verbatim, numbers in §3.10a Results: `--stops` — normal
  touch model HONEST at 7d on both sides (ratio 0.88, CI95 covers 1;
  sub-1 direction = clustering, errs safe; no §7 multiplier);
  `--res7` — primary NULL (IC −0.009), all exploration null →
  `residual7` confirmed display-only; `--funding` — primary NULL
  (IC +0.003), all exploration null → no crowding factor. §10 item 0
  closed; the directional-layer standing decision resolved by
  measurement (both live hypotheses zero → directional stays human).
  §7 liquidation bullet gains its first measured anchor. No code
  touched in this step — map-only diff.
- 2026-08-12d: **--stops survived its data, not its printer.** Run №3 (#12)
  cleared verify's old traps, computed 140+ dates of the invalidation study,
  then crashed in `report_stops`: a handful of setups carried a model touch
  probability of None/NaN (production `touchProb` returns null on its guard
  rails), old code let them into the aggregation, the pooled model mean went
  NaN, the calibration ratio became None and `"%.2f" % None` threw. The exact
  real-data combination is not reproducible offline; it is closed as a CLASS:
  the JS driver now nulls any non-finite model value, Python counts such
  setups out loudly («исключено сетапов с dist >= 100% …»: the counter will
  print the real population next run), the aggregation admits only finite
  model values, and the report prints «не считается / вердикт не выносится»
  instead of assuming floats — hit and whipsaw rates, which need no model,
  still print in full. Validation: a poison unit test feeding None/NaN through
  summary+report passes; full lab selftest and verify_bench (35/0) unchanged.
  Bench-only diff, one file.
- 2026-08-12c: **verify semantics v3 + workflow reorder after run №2 died on
  the step again.** Run №2 (commit 93de3b5) executed the new code correctly —
  fut return gaps routed to the basis lane as designed — but HYPE breached
  min_price by 6.1 % (perp liquidation wick vs CoinGecko composite spot low)
  and the single-coin ≥3× tripwire I had added killed the pipeline before the
  experiments a second time. Two lessons, both mine to own: (1) limiting the
  basis lane to return fields was a scale error — fut:true coins are two
  different instruments on EVERY field, so with --html all their gaps are now
  informative; (2) the 3× single-coin rule is gone on principle, not tuned:
  reconstruction defects are systemic by construction (window logic, time
  semantics and units hit all coins equally), so a field fails only on ≥3
  coins or all compared; any lone outlier warns loudly and never blocks.
  Workflow: the three experiment steps now run BEFORE verify, so no future
  source-noise vector can eat the lab again; verify stays a hard gate at the
  end for visibility. `verify_bench.py`: 35 checks / 0 fails, including the
  literal HYPE case (fut level gap → basis, exit 0) and systemic detection
  power (all coins breached → still fails).
- 2026-08-12b: **verify hardened after the first v4 run died on it.** The run
  fetched cleanly (28/29 in cache; GRAM has only 976 archive hours — stays
  excluded, as documented; XMR/HYPE/LIT correctly came as vision-perp) and
  funding landed for 27/28, but `--verify` exited non-zero — XMR r30 gap of
  6.7 pp vs live coeffs — and pipefail killed the workflow BEFORE the three
  experiments. Root cause is not a defect: fut-only coins have no Binance
  spot, the bot's CoinGecko composite vs the bench's perp candles differ by
  basis (§7), and one XLM volatility outlier (12.4 % vs 10 % bar) was source
  noise. Fix, argued from the check's purpose: a reconstruction defect is
  systemic or huge, so a field now FAILS only if ≥3 coins breach, or all
  compared breach, or any single coin is ≥3× the bar; lone sub-3× outliers
  print a named warning and do not stop the pipeline. With `--html` passed,
  return-family gaps (r7/r14/r30/eff14) on fut:true coins go to an
  informative «базис перп/спот» lane and never fail. `verify_bench.py`
  extended for the new semantics: 34 checks / 0 fails; lab selftest untouched
  and still green on the runner (artifact lab.txt).
- 2026-08-12: **experiment lab in the bench** (§3.10a) — three additive modes
  (`--stops`, `--res7`, `--funding` + `--fetch-funding`, `--lab-selftest`),
  answering the 12.08 audit's two measurements and the Boss's directional-
  capability question. Production files untouched; bench-only diff. Fetch now
  stores exchange high/low additively (`hl`; touch is a WICK event — close-only
  series undercount in the dangerous direction), workflow cache key v3 → v4.
  Whipsaw defined as «back at entry within 7d AFTER the touch». Funding parsed
  from monthly archive ZIPs by content (column layout drifted over the years).
  **Validation:** `py_compile` clean; JS bridges `node --check` clean and
  reproduce the live GRAM board stop (dist 9.7 %, price 1.2019, floored) and
  `residual7` to the digit; lab selftest green on known-answer worlds (see
  §3.10a for the numbers and the two recorded lessons); `verify_bench.py`
  29 checks / 0 fails after the fetch-format change; original `--selftest`
  still passes (extraction of `scoreCandidate` unaffected). Registered rules:
  one primary per experiment, family-wise caveat named, +26-week confirmation
  gate before any product change.
- 2026-08-11 (5): **`--verify` больше не умеет соврать в опасную сторону** (§3.10). Четыре дефекта, каждый воспроизведён тестом ДО правки и закрыт после: (1) код возврата всегда 0 — упавшая сверка зелёная в workflow; (2) поле, отсутствующее в живом `coeffs.json` у всех монет, проходило порог с нулём сравнений; (3) вердикт «совпадает с продакшном» печатался и тогда, когда доходности не сверялись из-за разрыва во времени; (4) `_quality_today.json` в каталоге кэша ронял сверку `KeyError: 'prices'`. Выбор меры по типу поля (`rel`/`pp`/`abs`) уже был в коде, но нигде не был записан — теперь в §3.10.
  **Валидация:** новый офлайн-стенд `bench/verify_bench.py` — 29 проверок, сеть заглушена, кэш синтетический, «живой» `coeffs.json` строится тем же `CdBuilder`, поэтому чистый прогон совпадает точно, а каждый провал внесён намеренно. На старом файле стенд даёт 8 отказов, на новом — 0. Правка затрагивает РОВНО одну функцию: сравнение AST показывает 33 определения до и после, изменено одно (`verify_against_live`), модульные операторы идентичны.
  **Сверх того:** `--selftest --seeds 10` на текущих продакшн-файлах — «стенд измеряет то, что должен», код возврата 0. Это подтверждает, что правки `index.html` от 11.08 (блок защиты, чистка CSS) не сломали вырезку `scoreCandidate` из HTML.
- 2026-08-11 (4): **чистка мёртвого CSS** (§10 п.2). Удалены 33 правила / 28 классов, осиротевшие после переезда блока входа на доску: `ent-*` (12), `lev-block`/`lev-head`/`lev-sub`/`lev-res`, `liq-row`/`liq-cell`/`liq-cell.pick`, `pin-btn` (+`.armed`, `.auto-on`, `.btn-row2`), `rec-line`, `diag-line`, `dist-line`, `qrow`, `side-container`, `s-long`/`s-short`, `bd-rpos`, `icon-warn`/`icon-ok` вместе с их анимациями `blinkRed`/`blinkGreen`. Плюс глобальные `L_BASE`, `SHOW_LEVS`, `STRESS_NAME` — по одному упоминанию на весь документ. Итого −4576 символов (−2.6 %).
  **Почему `icon-warn`/`icon-ok` мертвы:** МДЛ выводится текстом `MDL ✓/~/✕` с инлайновым цветом, мигающих иконок-дублёров нет с тех пор, как Босс запретил дублирующие значки; классы остались от прежней разметки.
  **Мигание Min/Max и бегущие рамки краёв не тронуты** (инв. 19): живут `light-blink`, `blink-text`, `edge-min`/`edge-max` с анимациями `lightBlink`, `blink`, `runBorderRed`, `runBorderGreen` — все четыре проверены как используемые.
  **Валидация (`bench/clean_bench.py`):** `<script>` отличается РОВНО тремя удалёнными объявлениями и ничем больше (построчный diff, список объявлений задан явно); разметка `<body>` побайтово идентична; все 156 оставшихся правил побайтово идентичны и в прежнем порядке; ни одного удалённого селектора не достижимо из живого документа, включая имена, собираемые конкатенацией (инв. 28); ни одного комментария, ссылающегося на удалённое имя; ни одной осиротевшей `@keyframes` и ни одной неиспользуемой CSS-переменной. Дополнительно: `node --check` пройден, вывод `boardHtml` побайтово совпал с прежним на 1500 случайных сценариях, стенд `prot_bench.js` — 1890 проверок, 0 отказов.
- 2026-08-11 (3): **блок «ЗАЩИТА ПОЗИЦИИ»** (§3.11) — тринадцатый блок доски, одиннадцатый по порядку чтения. Добавлены `protectionPlan()`, `touchProb()`, `probTxt()`, константы `FEE_TAKER`, `FUND_PAY_7D`, `ARM_R`. Два литерала `21` в блоке «ЦЕНА ВРЕМЕНИ» заменены на `FUND_PAY_7D` (нарушение инв. 20, устранено попутно), формула касания вынесена из `liqTouchProb`, форматирование вероятности — из `probRow`. Бот не менялся, схема не тронута, новых запросов, CSS-классов и состояний нет.
  **Валидация (`bench/prot_bench.js`, продакшн-код исполняется из `index.html`, инв. 21):** 1890 проверок, 0 отказов. `node --check` пройден. Тождество `touchProb`/`liqTouchProb` — 1716 комбинаций, максимальное расхождение 0. Остальная доска побайтово идентична прежней на 6 сценариях (новая секция вырезается из вывода и сравнивается остаток). 19 деградированных входов × 2 стороны — без исключений. Фаззинг 4000 случайных досок — ни одного `undefined`, `NaN` или `Infinity`.
- 2026-08-11 (2): **§10 п.1 — жёсткий потолок риска маржи** (§3.4). Добавлена `lMoney(dist)` — единственное место деления `MAX_MARGIN_LOSS / dist` (было два дубля, нарушение инв. 20). В `leverageDecision` четвёртый кандидат с полом `L_MIN`; новые поля `parts.money`, `moneyHard`, `moneyBelowMin`. На доске строка переехала в общий цикл и получает маркер «← ограничитель»; подпись блока переключается «Три…» / «Четыре…». Бот не менялся, новых запросов, CSS-классов и секций доски нет, схема не тронута.
  **Клауза `src ≠ 'вход'` из исходной формулировки отклонена** — обоснование в §3.4.
  **Валидация:** `node --check` пройден; 635 `capped`-случаев — 0 расхождений со старым кодом; 3243 сравнимых сетапа на обеих сторонах — ни одного роста плеча и ни одной потерянной сделки; шесть крайних случаев (нет `volatility`, `volatility = 0`, 3.5 %/ч, нет `min30`/`min90`, нет бет, `min > E`) — без исключений, сообщения прежние. Сверка с экраном XRP 11.08 14:52: структура 10.4X, шум 8.2X, риск маржи 6.6X, ликвидация 3X $0.6836 — сошлось до знака.
- 2026-08-11 (1): **блоки B–H слиты в тело карты.** До этого §5 противоречил сам себе («нужен платный тариф» против «бот ходит без ключа»), а §10 держал в очереди два уже закрытых пункта. Правка кода против самопротиворечивой карты — прямой риск, поэтому слияние сделано шагом 0.
- 2026-08-10 (6): **металл на рамках доски** (§3.7). Только CSS: два правила, `.bd-sec:not([style])` и `.bd-hero`. Разметка, JS и расчёты не тронуты ни на символ — `<script>` побайтово идентичен прежнему. Ноль новых узлов, псевдоэлементов и масок: кольцо — второй слой фона через `background-clip: border-box`. Тревоги (красная и янтарная) металла не получают, их инлайновый `border-color` остаётся единственным цветом рамки. Толщина линии прежняя, 1px. Отвергнуты: `border-image` (ломает `border-radius`), псевдоэлемент с `mask-composite` (13 масок на доске с перерисовкой каждые 30 с — цена без выгоды), фаска через `border-*-color` (Босс отверг как невидимую).
- 2026-08-10 (5): **`res7` на фронте + гард секции «ПОЧЕМУ ЭТА МОНЕТА»** (§3.9). Добавлены `residual7()` и `residColor()`, константы `RES_Z = 1.0` и `RES_R2_CAP = 0.90`; строка `Своё 7д` на карточке и блок «СВОЁ ДВИЖЕНИЕ ЗА 7 ДНЕЙ» на доске внутри блока 2. Бета берётся по знаку `btc.r7`, мера — сигма остатка `σ√(1−R²)` с парным R². Ноль новых запросов, CSS-классов и секций доски; `scoreCandidate`, движок плеча и ранжирование не тронуты — остаток только показывается. Бот не менялся (его половина закрыта записью (4)).
  **Попутно исправлен гард секции.** Было `if (sc)`: при `sc === null` — а `scoreCandidate` штатно возвращает `null` при отсутствующей `volatility` или битом диапазоне 90д, и это возможно при `error = false` — секция исчезала ЦЕЛИКОМ и МОЛЧА, унося с собой и остаток к BTC, и «ШОРТ СОЗРЕЕТ, КОГДА», хотя оба считаются НЕ через счёт и от него не зависят. Стало `if (sc || rb7 || mat)`: секция рисуется, если есть что сказать, каждый кусок отвечает за себя, а пропавший счёт называется вслух отдельной строкой вместо тихой пустоты. `mat` вычисляется до секции, тело блока «ШОРТ СОЗРЕЕТ» не тронуто ни на символ. Ключ якоря прокрутки (`.bd-h` = «ПОЧЕМУ ЭТА МОНЕТА») не изменился — инв. 18 цел.
- 2026-08-10 (4): **`btc.r7/r14/r30` в `coeffs.json`** — бот-половина остаточной доходности к BTC (§3.9; на тот момент — §10 п.1 очереди). Три вызова уже написанной `window_stats` по уже скачанному ряду BTC: ноль новых запросов, ~+60 Б к `coeffs.json`, схема аддитивна (инв. 1, 9), ключи монет и `err_result` не тронуты. Стенд: на 90д часовом ряду r7/r14/r30 совпали с прямым расчётом до 1e-12; восемь крайних случаев (пустой ряд, одна точка, нулевая и отрицательная цена, история < 30д, дыра 20 ч, плоский ряд) — без исключений, только `None`; сквозной прогон `main()` с заглушками сети — 28 монет, набор ключей карточки не изменился. **Фронт не менялся:** `res7` решено считать на фронте — там же, где живут `scoreCandidate` и выбор `rawBeta`; бот везёт только замеры.
- 2026-08-10 (3): **«ШОРТ СОЗРЕЕТ, КОГДА»** внутри блока ПОЧЕМУ ЭТА МОНЕТА (§3.8). Пороги вынесены в `EFF_TREND` / `PACE_Z`; `scoreCandidate` переведён на них **без изменения поведения** — стенд прогнал 40 000 входов (обе стороны, пропуски полей, крайние значения), расхождений 0, макс |Δсчёт| = 0. Новых запросов, CSS-классов и секций доски нет. Бот не менялся.
- 2026-08-10 (2): **якорь прокрутки доски** — устранён прыжок экрана при нажатии любой кнопки. Аврора удалена целиком (CSS, разметка, вызовы) по решению Босса.
- 2026-08-10 (1): подсветка нажатой кнопки в ТОЧКЕ ВХОДА (пять кнопок, ровно одна горит, карандаш = «своя цена») · funding показан суммой в USDT за 7 дней рядом с процентом маржи · волосяные разделители `.bd-msep` между b= / R² / ρ в блоке ДОВЕРИЕ К МОДЕЛИ.
- 2026-08-09 (3): порядок 12 блоков доски по спецификации Босса; порядок вынесен в склейку. Размер позиции: две единицы ввода (МОНЕТЫ / USDT), быстрые суммы 50/100/250/500 удалены.
- 2026-08-09 (2): движок плеча переписан на три независимых потолка с горизонтом 7 суток; `pinned` / АВТО-СТРЕСС / формула 0.87–1.13 удалены. Введены `MAX_MARGIN_LOSS`, `INV_FLOOR_SD`, `INV_CAP_SD`, `H_REACT`.
- 2026-08-09 (1): `LIQ_MMR` 0.01 → 0.0125 по обратному счёту трёх реальных позиций. Доска CRYPTO FUTURE заменила блок входа внутри карточки.
- 2026-07-17: TON → GRAM (ребрендинг). CoinGecko id сохранён `the-open-network`.
- 2026-07-29: добавлен BNB; HYPE переведён на `fut:true` (+ `cachedFutTickers`); добавлен гейт MDL.
- 2026-08-07: добавлены ZEC, XMR (`fut:true`), UNI, LIT (`fut:true`); ранг капитализации с дельтой 24ч.
- 2026-08-08 (1): исправлен цвет R² 90d — вычисленная переменная не была подключена к разметке.
- 2026-08-08 (2): этап 1 — кнопки ЛОНГ/ШОРТ, автоматический расчёт плеча, `BTC ВВЕРХ/ВНИЗ` в шапке, Funding по стороне сделки.
- 2026-08-08 (5): по итогам видео-прогона 16:54 — единый вердикт `ИТОГ = min(МАКС, РЕК)` вместо двух конфликтующих светофоров; лестница риска 7д/14д/30д вместо одной цифры; блок плеча поднят над диагностикой и строка `90d:` скрыта в режиме позиции; подпись кнопки фиксации `Вход $60 000 ✕` без слова Normal; строка сценария переименована в `(вход, без стресса)`; подсказка «нажми АВТО-СТРЕСС» при несдвинутом слайдере.
- 2026-08-08 (4): этап 2 — АВТО-СТРЕСС (2σ BTC от уровня входа, первое использование `btc.volatility`), FDV/MC в бейдже ранга, РЕКОМЕНДУЕМОЕ плечо с вероятностью касания ликвидации за 30д. Исправлена асимметрия `liqLogDist`: ограничение d<1 применялось к обеим сторонам, ломая шорт при L<1.
- 2026-08-08 (3): по итогам видео-валидации — вход всегда Normal, строка сценариев с уровнями BTC, маркеры «слайдер не сдвинут» / «сценарий мягкий», кнопки плеча сокращены до 2X–7X.

## 10. На горизонте
Порядок — результат аудита 10.08 (пять пунктов Босса + три идеи его ассистента). Внутри каждого пункта указана цена и что именно он меняет.

**Принято, ждёт очереди**
~~0. **Lab runs (12.08.2026)** — `--stops`, `--res7`, `--funding` delivered with
   green lab selftest, `verify_bench` 29/0 and the original `--selftest`
   passing; awaits a manual `workflow_dispatch` (cache key v4 forces a refetch
   that now carries high/low). Verdict rules are fixed in §3.10a; results are
   to be read against them verbatim, no post-hoc re-framing.~~
   — **закрыт 12.08 вечером, run №4: см. §3.10a Results и «Сделано»**
~~3. Потолок риска маржи жёстким.~~ — **закрыт 11.08, см. «Сделано»**

<!-- `MAX_MARGIN_LOSS = 0.35` сейчас справочный (§3.4). Расчёт: включённый целиком, он связывает 15 типовых комбинаций из 16 и роняет ИТОГ ниже `L_MIN` в семи. Причина — дистанция, упёршаяся в `INV_CAP_SD`: там стоп нарисованный, и денежное правило применять к нему нельзя. Версия, которую стоит обсуждать: жёсткий потолок при `inv.capped = false` И `inv.src ≠ 'вход'`, справочная строка во всех остальных случаях.
-->
1. **Open Interest** — отложен до недели стабильной работы расчёта плеча; цена 28 запросов/5 мин и новая точка отказа; показывать одним состоянием («новые деньги» / «закрытие позиций»), не сырыми числами. **С 13.08: перед реализацией ОБЯЗАТЕЛЕН бэктест позиционирования из архива метрик vision (см. решение в «Directional layer CLOSED» ниже) — сначала измерить, потом показывать.**
~~2. **Мёртвый CSS**~~ — **закрыт 11.08, см. «Сделано»**

**Решения, которые не пересматриваем без новых аргументов**
- **Directional prediction (Boss's point 3, 12.08.2026): the only justified
  path is pre-registered factor tests on the bench.** The composite score, the
  pure contrarian factor and the regime split are measured zeros (§3.10 «Сделано»);
  ML rankers (28 coins × ~145 dates → guaranteed overfit), GARCH (±30 % vol
  forecast error sits inside one leverage step, absorbed by rounding down),
  on-chain/TVL (weekly-scale, quarter of the list) stay rejected per §8. The
  two live hypotheses with documented priors — funding crowding and the res7
  residual — are exactly what the lab now tests. If both return null, the
  directional layer remains human (catalysts + REVIEW) by design, and the
  tool's edge remains risk, sizing and honesty — that division of labour is a
  result, not a failure. **Resolved 12.08.2026, run №4: both returned null at
  the pre-registered bars (§3.10a Results). The division of labour is now
  measured, not assumed; a new directional test needs a new external prior,
  not a re-roll of the same data.**
  **Directional layer CLOSED — audit 13.08.2026.** Full landscape reviewed
  against the evidence bar, on top of the measured zeros (score at 3/7/14d,
  both sides, both regimes; res7; funding; rank-1 follow-up in §3.10a):
  on-chain/TVL, ML rankers and GARCH stay rejected per §8 with nothing new;
  unlock automation stays consciously manual (REVIEW's job); intraday
  microstructure (orderbook, liquidation cascades) holds real edge but is
  structurally incompatible with a PWA + hourly bot + 1–14d holding — out of
  scope by design; BTC lead-lag needs minute data (§7). The one untested
  hypothesis with a data path — positioning/OI (taker and top-trader
  long/short ratios, `data.binance.vision` futures metrics archive, daily
  files since ~12.2021; availability «может быть устаревшим», verify at
  need) — is NOT run now `[решение принято мной]`: funding-z is the market-
  clearing PRICE of the same imbalance and measured zero with a tight CI, so
  the conditional prior for the quantity measure is well under 10 %, against
  a ~30k-file fetch. Discarded alternative: run it anyway for completeness.
  Reversal conditions: external evidence that Binance positioning ratios
  predict 7d large-cap returns, or the OI display feature graduating from
  the deferred queue — in which case this backtest becomes its mandatory
  PRE-GATE (measure first, display second). Until then the machine owns
  risk, sizing and honesty; the human owns catalysts via REVIEW. Final.**
- **Новые монеты — НЕ добавляем** (решение Босса 10.08). Работаем со списком из 28 пар.
- **Переключатель горизонта 7д/30д** — не реализован намеренно: масштабирование ручное (√H), лишний орган управления даёт соблазн подкрутить горизонт под желаемое плечо. Вернуться, если срок удержания начнёт меняться систематически.
- Карта ликвидаций, вероятность «TP раньше SL», спот/перп базис — отклонены, причины в §8.
- Funding уже участвует в счёте (шорт ×1.05 при ставке > 0.05 %/8ч) — это единственное место, где деривативы влияют на ранжирование.

**Заделы**
- Beta history в `history.json` (720 точек) — под будущий анализ стабильности бет и калибровку горизонта.

**Сделано**
- ~~**Lab runs**~~ — **12.08.2026, run №4**, см. §3.10a Results. Три
  вердикта по правилам, зарегистрированным до данных: `--stops` — модель
  касания ЧЕСТНА на 7д (0.88, ДИ95 накрывает 1, обе стороны, множитель в
  §7 не нужен); `--res7` — НОЛЬ (первичный IC −0.009, вся разведка ноль,
  `residual7` остаётся чистым отображением); `--funding` — НОЛЬ
  (первичный IC +0.003, вся разведка ноль, фактор скученности в продукт
  не входит). Продукт не изменён ни на символ.
- ~~**Мёртвый CSS**~~ — **11.08.2026**, см. журнал миграций. Оценка в очереди («27 классов / 33 правила / ~3.9 КБ») заменена измерением: **28 классов, 33 правила, включая 2 осиротевшие анимации `blinkRed`/`blinkGreen`, и 4576 символов (−2.6 % файла)**. Плюс три неиспользуемых глобальных переменных. Логика не тронута ни на байт.
- ~~**Защита позиции**~~ — **11.08.2026**, см. §3.11. Безубыток с издержками, цена переноса стопа в безубыток (1R) и измеренная цена этого решения — вероятность, что шум вернёт цену к безубытку за 7 дней. Плюс долив маржи как единственный рычаг уже открытой позиции. В расчёты не входит (инв. 27).
- ~~**Потолок риска маржи жёстким**~~ — **11.08.2026**, см. §3.4. Условие упрощено до `!capped`: клауза `src ≠ вход` из исходной формулировки ОТКЛОНЕНА как произвол (доказательство на живом XRP — в §3.4). Добавлен пол `L_MIN` (инв. 26), которого в исходной формулировке не было.
- ~~**Бэктест модели скоринга**~~ — **11.08.2026**, см. §3.10.
  **Вердикт: `scoreCandidate` — шум.** Правило вердикта зарегистрировано до
  прогона: IC ≥ +0.05 и ДИ мимо нуля → работает; IC ≤ −0.02 и ДИ мимо нуля →
  инвертирован; иначе шум. Веса не трогаем ни при каком исходе.

  **Выборка:** 28 монет из 29 (GRAM не набрался), 3 года часовых свечей
  (30.10.2023 – 11.08.2026), 143–145 дат, 24.3 монеты на дату.
  **Мощность достаточна:** SE(IC) = 0.020–0.023, различимо \|IC\| от 0.041
  при заявленном пороге 0.05. Это измеренный ноль, а не «данных мало».

  | Сторона · горизонт | IC | ДИ95 |
  |---|---|---|
  | Лонг 3д | +0.014 | −0.027…+0.055 |
  | Шорт 3д | +0.017 | −0.022…+0.058 |
  | Лонг 7д | −0.006 | −0.050…+0.037 |
  | Шорт 7д | +0.026 | −0.019…+0.070 |
  | Лонг 14д | −0.006 | −0.056…+0.044 |
  | Шорт 14д | +0.025 | −0.025…+0.078 |

  **Контроли пройдены:** перемешанный счёт −0.033…+0.000; разброс счёта
  внутри дня по 24 монетам 9.7 пункта при шкале 1…88 (ранжировать было что);
  медиана \|избыточной доходности\| за 14д 6.6 % (предсказывать было что).

  **Риск счёт тоже не отбирает.** Медиана худшей просадки внутри окна, лонг
  7д: верхняя треть −6.2 %, средняя −6.2 %, нижняя −6.6 %.

  **Гипотеза «штрафы душат сигнал» — проверена и отклонена.** Штрафы
  «падает прямой линией» и «нож ещё летит» операционно мощные: срабатывают в
  24 % случаев, роняют счёт в 1.67 раза, меняют состав ТОП-3 на 45 % дат. Но
  версия без них даёт IC +0.004 против −0.006 — разницы нет, потому что и
  голый контр-трендовый фактор на реальных данных ноль: «у мин90» дал
  +0.003 / −0.011 / −0.026 на трёх горизонтах (на синтетике давал +0.25).
  Душить было нечего.

- ~~**Определение режима рынка**~~ — **11.08.2026**, закрыт отрицательно.
  Правило (одобрено Боссом до прогона): тренд = наклон 90-дневной регрессии
  BTC значимо отличен от нуля, иначе диапазон. Реализация: снос по 90
  дневным доходностям, t = μ·√n/σ, \|t\| > 1.96. Контроль: 3 % ложных
  срабатываний на чистом блуждании, 92 % распознавания при +150 % за 90 дней.
  Планка вердикта поднята вдвое (\|IC\| ≥ 0.10, ДИ 99 %) — поправка на две
  проверки; главная проверка одна: лонг, 7 дней.

  **Результат: деление вырожденное — 13 трендовых дат против 132
  диапазонных** (все 13 — тренд вверх).
  · Диапазон, 132 даты, мощность хорошая (различимо от 0.043): IC = −0.019,
  ДИ99 [−0.072; +0.035] → шум.
  · Тренд, 13 дат: IC = +0.119, SE 0.081, различимо только от 0.163 →
  сказать нечего. Точечная оценка меньше полутора стандартных ошибок; это
  ровно тот случай, который соблазняет и ничего не доказывает.

  **Вывод:** по корректно сформулированному критерию значимости крипта почти
  всегда в диапазоне, и режимного выключателя из этого правила не выходит. В
  диапазоне, где данных достаточно, скоринг определённо шум. **Тема скоринга
  закрыта** — как и договаривались до прогона.
- ~~Остаточная доходность к BTC (`res7`)~~ — **10.08.2026**, см. §3.9. Закрыты обе половины: бот (`btc.r7/r14/r30`, §2) и фронт (`residual7()`, карточка + доска). Оба открытых вопроса пункта решены так, как рекомендовалось: бета по знаку `btc.r7`, разложение пути отклонено. В `scoreCandidate` не входит — до п.1 это был бы непроверенный приор. В комментариях кода функция всё ещё названа «§10 п.1» — ссылка историческая.
- ~~«ШОРТ СОЗРЕЕТ, КОГДА»~~ — **10.08.2026**, см. §3.8.
- ~~FDV~~ — **08.08.2026**, см. §3.5.
- ~~Рекомендуемое плечо~~ — **08.08.2026**, см. §3.3.
