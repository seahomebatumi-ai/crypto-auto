# SYSTEM_MAP — Pro Crypto Tool

Единый источник правды. Сверяться ПЕРЕД любой правкой кода и при интерпретации метрик.
Актуально на 19.08.2026 (движок направления §3.12 + третья редакция отображения: рейтинг на каждой карточке, глиф состояния, инв. 33–34); прежняя опора — 14.08.2026 (аналитический слой ЗАКРЫТ §10 + §3.10b «потолок разрешения» + §3.10c «следующие ворота»; `--verify` §3.10; чистка мёртвого CSS §9; блок «ЗАЩИТА ПОЗИЦИИ» §3.11); прежняя редакция — (жёсткий потолок риска маржи §3.4, доска CRYPTO FUTURE, движок плеча на трёх потолках, размер в монетах, якорь прокрутки, «ШОРТ СОЗРЕЕТ, КОГДА», остаток к BTC `res7`).

> **Language rule (project instructions V9, in force from 11.08.2026):** new
> sections of this map and new code comments are written in ENGLISH. Sections
> written earlier stay in Russian — retranslating them would be an unsolicited
> rewrite of a validated document, and the mixture is deliberate, not drift.
> Only chat with the Boss is in Russian; UI strings stay Russian by definition.

## 1. Поток данных
iPhone Shortcuts → `workflow_dispatch` → GitHub Actions → Python-бот → CoinGecko `/market_chart` (90 дней, hourly; BTC + 28 альтов = 29 вызовов) + `/coins/markets` (ранги, 1 вызов) = 30 вызовов/прогон → расчёт метрик → PATCH Gist → WebApp (iPhone).

**Расписание — НЕ cron.** Cron жил в `main.yml` с 12.06 по 15.06.2026 (последняя
редакция — дважды в час, «чтобы гарантировать выполнение») и снят Боссом
сознательно 16.06 в `acd4315`. Единственный регулярный триггер — Shortcuts на
телефоне Босса: **раз в час с 09:00 до 01:50 локального времени = 17 плановых
прогонов в сутки ≈ 15.3k вызовов CoinGecko в месяц**, плюс редкие прогоны по
`push` в `main.py` / `main.yml`. Возврат cron 20.08 (ТЗ-02, на ложной находке
отчёта-2) давал ДВА источника обновления вместо одного и снят обратно в PR #2.
Автоматизация вне репозитория не дублируется и не выключается — она принадлежит
Боссу.

**Ночная пауза 7 ч 10 мин — часть проекта, а не сбой.** С 01:50 до 09:00 прогонов
нет, `coeffs.json` штатно стареет до ~7 часов, и `STALE_CRIT` (130 мин) загорается
КАЖДУЮ ночь при полностью исправной системе. Отсюда инв. 4: «расписание спит» и
«обновление не пришло» — разные состояния, и путать их нельзя.

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

### 3.12 Direction engine — veto cascade (19.08.2026)

<!-- EDIT-MARKER 2026-08-19-DIRECTION-ENGINE -->

**Why this exists.** On 18.08 the system produced two opposite conclusions on
the same data: the board ranked GRAM as the #1 LONG candidate and ZEC as a
SHORT candidate, while the market analysis called GRAM a SHORT and ZEC a LONG.
Both were internally consistent and structurally incompatible: the board scores
MEAN REVERSION (proximity to the 90-day extreme), the analysis traded TREND
CONTINUATION with catalysts. Two opposite priors ran simultaneously on one
screen with nothing arbitrating between them.

The GRAM short was a real error and the system already held the evidence:
target = min90 $1.3027 against entry $1.3190 is **1.2 %**, i.e. **0.27 σ** of
the weekly noise, against a structural stop of 9.2 %. Reward/risk below 1:1 —
negative expectancy, printed on the board and never read. The ZEC long was a
different failure: the geometry was sound (R:R ≈ 1:2.5) and only the ENTRY was
undisciplined — «wait for $495–505» existed as prose, not as a system state.

**Principle: the direction is decided by a CASCADE OF VETOES, not by a sum of
weights.** Nothing below predicts anything. Each layer either asserts «the
geometry of this trade is bad» or «this prior is not admitted right now»; both
are measurable without a forecast. This is why §3.12 does NOT reopen the
predictive layer closed in §10 — no ranking factor is added, and no weight is
tuned. See «Relation to §10» at the end of this section.

```
Layer 0  REGIME     one per list      trend | range | stress
Layer 1  GEOMETRY   veto, no forecast R:R · noise floor · money · entry chase
Layer 2  CHANNEL    exactly one       mean reversion  XOR  continuation
Layer 3  CATALYSTS  veto only         manual registry, cannot raise a score
Layer 4  VERDICT    default = NO      trade | wait | watch
```

#### Layer 0 — `marketRegime(btcStats)`

```
z   = btc.r7  / (btc.volatility·√H_NOISE)          weekly move of BTC in its own σ
eff = btc.r14 / (btc.volatility·√(2·H_NOISE))      clipped to ±3
stress  if  btc.volatility ≥ VOL_HARD  or  z ≤ −REG_STRESS_Z
trend   if  |eff| ≥ EFF_TREND,  dir = sign(eff)
range   otherwise
```

`eff` is deliberately the SAME formula the bot uses for a coin's `eff14`
(`r14/(vol·√336)`, and `336 = 2·H_NOISE`), compared against the SAME
`EFF_TREND`. One threshold per system (inv. 20); a second trend constant was
rejected rather than tuned.

**Known property, measured, not hidden:** under a driftless random walk
`eff ~ N(0,1)`, so `|eff| ≥ 0.6` labels **~55 %** of pure-noise windows as
«trend». The bench confirms it (7 of 14 flat-world dates). This is the same
class of finding as inv. 23 and it is ACCEPTED, because a false trend label
cannot produce a wrong direction: it switches the channel and narrows the
admissible side to one, and on a driftless market both channels are worth
exactly zero — proven by the walk control below. `[решение принято мной]`
Discarded alternative: a dedicated `REG_TREND = 1.5`. Rejected because a second
trend threshold violates inv. 20 immediately and cannot be validated on this
sample (§3.10b). Reversal condition: the Boss reports the regime flapping
between renders; the cheap fix is hysteresis, not a new constant.

No `btcStats`, or no `volatility` → `mode = 'range'`, `known = false`. That is
EXACTLY the pre-19.08 production behaviour (mean reversion always), so an old
`coeffs.json` changes nothing (inv. 9).

#### Layer 1 — `tradeGeometry(cd, E, isLong, dec, hi24, lo24)`

Turns numbers the board ALREADY prints from advice into prohibition. Nothing is
recomputed: the target is the 90-day extremum (the same `ЕСЛИ СРАБОТАЕТ` line),
the risk is `dec.inv.dist`, the money veto is read from `dec.moneyBelowMin` so
`MAX_MARGIN_LOSS` keeps living in exactly one place (inv. 20).

| Veto | Condition | What it prevents |
|---|---|---|
| target passed | `tgt ≤ E` (long) / `tgt ≥ E` (short) | trading toward a target already behind price |
| reward/risk | `reward/risk < RR_MIN` | the GRAM short: a trade that must be right more often than wrong |
| noise floor | `reward/(vol·√H_NOISE) < TGT_SIGMA_MIN` | targets the market reaches by chop, where being right pays nothing |
| money | `dec.moneyBelowMin` | a stop that costs more than `MAX_MARGIN_LOSS` even at `L_MIN` |
| leverage | `!dec.ok` | «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» becoming a tradable card |

**Entry discipline — `wait`, not a veto.** Anchor = the 24-hour low for a long,
the 24-hour high for a short (`highPrice`/`lowPrice`, already in the Binance
ticker — zero new requests). Beyond `ENTRY_CHASE_SD` daily sigmas from that
anchor the card enters state ЖДАТЬ and prints the price to wait for. The rule
works in BOTH channels because it forbids not «buying high» but «buying AFTER
the move» — chasing, not strength. On the 19.08 ZEC data it produces ≈ $500,
which is the level that had existed only as prose.

#### Layer 2 — `momentumScore` and the ban on adding channels

`scoreCandidate` is the mean-reversion channel and is **not modified**. The
continuation channel is its mirror: trend intactness (`eff14` in the side's
direction), own strength (`res7` z in the side's direction), weekly pace vs
monthly pace, quality. The two are NEVER summed — summing opposite priors is
precisely what produced «GRAM long» and «GRAM short» at the same time. The
regime admits one; the other is not computed.

Quality and penalties are shared through `qualityScore` / `scoreFinish`, lifted
out of `scoreCandidate` **without a single arithmetic change** — proven on
200 000 random inputs, 0 mismatches. `trendPenalty = false` removes EXACTLY the
two `eff14` penalties and only those: continuation wants the trend intact,
mean reversion wants it broken.

#### Layer 3 — `CATALYSTS` / `catalystCheck`

The ONLY external input of the engine, filled by hand from market analysis.
`{ d: ISO date, dir: long|short, t: short reason }`. Events older than one day
or further than `CAT_WINDOW_D` are ignored. An unlock is always written
`dir:'short'` — it vetoes a long and does not create a short.

**Hard rule: a catalyst can only VETO a side.** It cannot raise a score and it
can never override a geometry veto. A catalyst placed above geometry is what
produced the GRAM short on the floor of its range; the ban is written against
that specific error. It also keeps external input out of the ranking, which is
what §3.10b forbids.

#### Layer 4 — `directionVerdict` and the coherence guarantee

Default is NO TRADE. A side is emitted only when everything lines up: regime
admits the prior → channel ranks the coin → geometry passes → no catalyst veto
→ the entry is not a chase.

**One coin can never receive both ЛОНГ and ШОРТ. This is structural, not
empirical:**

```
stress → neither side
trend  → only the side matching reg.dir
range  → only the side with the HIGHER mean-reversion score (tie → neither)
```

The range rule is load-bearing and was added after the bench showed that
geometry ALONE does not guarantee it: a coin sitting mid-range with a wide
90-day range can clear R:R ≥ 2 on both sides simultaneously (ZEC on 19.08:
long 1:1.6, short 1:2.9 — both would have passed). Geometry filters bad trades;
it does not arbitrate direction. The regime does.

~~Only actionable candidates are numbered (`row.no`), so `#1` is an assertion
about a trade rather than a row index.~~ — **reversed 19.08 (3):** it made the
number an assertion at the price of erasing the ranking from 74 % of the list.
`#N` is now the place in the score ranking, present on every scored card, and
the trade assertion is carried by the glyph and by `.reason-line` (see the
Display contract below and inv. 33–34). Zero new blocks, zero new CSS classes,
zero new sections, zero new API calls (inv. 15 and 18 untouched — the board's
block order and anchor keys did not move).

#### Display contract (Boss's specification, 19.08.2026 — third revision)

Two failures produced this contract, in opposite directions, one day apart.

**First failure — one word, two meanings.** The badge reused `tierOf`'s
vocabulary, so «Наблюдать» named both the 35–49 score tier (cyan, numbered)
and the «no trade» verdict (grey, unnumbered). The Boss read two live SHORT
candidates (ETH #1, SOL #2) as an empty short side.

**Second failure — the fix ate the ranking.** Separating the vocabularies by
STATE meant only tradable cards kept a number and a score; everything else
collapsed into a flat grey «НАБЛЮДАТЬ». Measured on the shipped build: **74 %
of scored cards printed no rank at all** (3538 of 4808 over 400 random lists).
The list was sorted correctly and looked random, because the evidence of the
order had been erased from four cards in five — the top-scoring coin stood
first saying «НАБЛЮДАТЬ» while the second card said «#1 Средний 53».

**Resolution — one channel, one meaning** (inv. 33):

| Channel | Carries | Values |
|---|---|---|
| number `#N` | place in the ranking | contiguous 1..N in score order |
| word + colour | quality of the score | Сильный ≥70 green · Средний ≥50 `--accent` · Кандидат ≥35 `--cyan` · Наблюдать below, grey |
| glyph (`stateMark`) | state of the entry | `` trade · `~` pullback needed, pulsing `--orange` · `✕` no trade, `--red` |
| `.reason-line` (`verdictNote`) | why, in words | «нет сделки: …» · «ждать $0.3337 — вход далеко от суточной опоры» · «катализатор: …» |

So a card reads `#3 Средний 54 ✕` with «нет сделки: риск/прибыль 1:1.0»
underneath: third by score, decent quality, not tradable, and the reason is
stated. Nothing is inferred from an absence.

The glyph vocabulary is borrowed from МДЛ (`✓ / ~ / ✕`), which already sits on
the same card — no second language is introduced. The pulse reuses the existing
`light-blink` class (the Min/Max pulse, inv. 19); no keyframe was added.

**The board speaks the same words.** `stateMark` and `verdictNote` are single
named functions used by both surfaces. Before this revision the board printed
the tier and the score and said nothing at all about the refusal — with a rank
now printed there too, silence would have read as permission.

**Ranking is strictly by score, and neither the state nor the tier may take a
number away.** `byScore` orders by score (ties within 0.05 points resolved by
market-cap rank, then by volatility); `assignRanks` numbers every scored row of
the shown list, contiguously. Rows folded away as irrelevant to the side carry
`row.off` and get no number: they are outside this side's ranking, and a
number would lie about their place.

**`directionVerdict` always computes and exposes the score,** even when the
side is refused at the regime or channel stage. A card without a score is
invisible to sorting, and the Boss's standing requirement is «calculate
accurately → rank accurately → display clearly». Invariant 30 is unaffected:
coherence is enforced by `action`, never by withholding the number.

**Validation — `bench/display_bench.py` and `bench/render_bench.py`.**
The first proves the contract on the functions (24 598 checks, 0 failures) and
carries a quantitative witness of the old defect. The second proves it on the
rendered DOM: real `update()`, real `renderBoard()`, 123 scenarios,
24 157 checks, 0 failures, including degraded rows, the expanded off-side
block, an empty bot payload and ОБЗОР. Neither copies production logic —
the `<script>` block is cut out of `index.html` and executed by node (inv. 21).

#### Constants (all new ones in one place, inv. 20)

```
RR_MIN         = 2.0     the same 2 the board already prints in ЕСЛИ СРАБОТАЕТ
TGT_SIGMA_MIN  = 1.0     target closer than one weekly σ is inside the chop
ENTRY_CHASE_SD = 0.5     distance from the 24h anchor, in daily σ, that is a chase
REG_STRESS_Z   = 2.0     BTC weekly move in its own σ that suspends new entries
CAT_WINDOW_D   = 14      catalyst horizon
```

#### Validation — `bench/direction_bench.py`, 689 786 checks, 0 failures

Inv. 21 is satisfied literally: no copy of production math anywhere. JS is cut
out of `index.html` by name with brace matching and executed by real node;
coin metrics are produced by `window_stats` / `window_vol` extracted from
`main.py` through the AST. Editing either file changes the bench automatically.

| Mode | Result |
|---|---|
| `--identity` | old vs new `scoreCandidate`: 200 000 inputs, **0** mismatches |
| `--props` | 60 000 scenarios: never both sides tradable, never a trade in stress, never a trade under an active veto, never a trade below `RR_MIN`, never a trade while the entry is a chase |
| `--fixtures` | reproduces the Boss's own board: GRAM long R:R **7.64** (board 7.7), ZEC short **2.86** (board 2.9) |
| `--display` | tier boundaries 70/50/35 inclusive, order strictly by score, contiguous numbering, no coin numbered on both sides |
| `--control` | driftless walk, untruncated barrier race: old system **−0.001** (2SE 0.080) |
| `--sim` | trend world mean R **−0.748 → −0.345**; walk −0.540 → −0.400; mean-reversion world unchanged |

**The control is the most important number in this section, and it is a
LIMIT, not a win.** With zero drift, `P(target before stop) = risk/(risk+reward)`,
so `E[R] = rr·risk/(risk+reward) − reward/(risk+reward) = 0` for ANY selection.
Geometry therefore CANNOT raise mean R on a random walk — and is not supposed
to. It works against costs and against drift. That is why the measured gain
appears in the trend world and nowhere else, and why no claim of «better
prediction» is made anywhere in this section.

**Two honest limitations, recorded so they are not rediscovered:**

1. **The live archive backtest was NOT run.** `data.binance.vision` is blocked
   by the execution environment's network policy (HTTP 403, `host_not_allowed`),
   so `backtest_bench.py --run` remains the Boss's to execute. Everything
   provable offline is proven; nothing about live data is claimed.
2. **Synthetic levels are an artefact, only differences are interpretable.**
   The 30-day barrier race truncates the winning tail (a 5σ target needs longer
   than a 2σ stop), which biases both arms negatively by the same construction.
   The first run of the simulation FAILED and the failure was in the generator,
   not the rule: BTC statistics were pinned flat, so the trend world was judged
   by the mean-reversion channel and the regime switch was never exercised at
   all; and a drift of ±0.35σ per hour produced a ~1900× move over 90 days. The
   generator was fixed; the comparison rule was not touched (inv. 23).

#### Relation to §10 — this is not a reopening of the predictive layer

§10 closes the directional layer to new RANKING FACTORS, and that closure
stands untouched. §3.12 adds none: no factor enters `scoreCandidate`, no weight
is tuned, no new metric claims predictive power. What it adds is a filter with
zero predictive content (geometry), a switch (regime), and a manual external
veto (catalysts). The operative rule of §10 — «a new ranking factor is
admissible ONLY on an external prior naming an effect size this sample could
resolve» — is unaffected and still binding.


### 3.13 Verdict journal — «вход → вердикт доски → факт» (specified 21.08.2026, TZ-05)

<!-- EDIT-MARKER 2026-08-21b-JOURNAL -->

**Status: SPECIFIED, NOT BUILT.** TZ-05 written 21.08; nothing is merged, no
file exists yet, and the calculator's behaviour is unchanged. This section is
the permanent contract — the TZ is a work order and will be archived, the schema
has to be answerable from the map in six months.

**What it is.** A daily record of what the board said about every coin — inputs,
verdict, the catalyst registry in force, the engine fingerprint — plus, 7 and 14
days later, what the price did. A measuring instrument: nothing is displayed,
nothing feeds back into any calculation (the same standing as `res7` §3.9 and
«ЗАЩИТА ПОЗИЦИИ» §3.11, inv. 27).

**Why it precedes `catalysts.json` in the §10 queue.** The verdict is not
reconstructible after the fact. `history.json` keeps betas, R² and rank only —
no price, no `min/max`, no `volatility`, no volume — and `scoreCandidate`,
`tradeGeometry` and `leverageDecision` all need exactly the fields it does not
keep. Every un-journaled day is lost permanently, which is true of no other item
in the queue.

**Layout — one file per unit of work, never reopened.**

| Path | Written | Content |
|---|---|---|
| `journal/data/YYYY-MM-DD.jsonl` | once per date | `k:"s"` snapshot line per covered coin, `k:"x"` skip line per uncovered one |
| `journal/out/YYYY-MM-DD-h7.jsonl`, `…-h14.jsonl` | once per date × horizon | `k:"oh"` BTC header, then `k:"o"` per coin |
| `journal/runs.jsonl` | appended per run | `k:"r"` run line, `k:"g"` gap line per unrecorded date |

**Snapshot fields.** `d · ts · sym · pair · gen · age · px{src,cur,p24,qv,hi,lo,cnt}
· reg · cd (analysis_data row verbatim) · btc (coeffs.btc verbatim) · rp ·
long{…} · short{…} · cat{acting,hash} · fp{script,commit}`. Side block:
`rel · score · tier · ch · action · why · note · verdict · wait · tgt ·
geo{rr,reward,risk,tgtSig} · dec{ok,L,binding,moneyBelowMin,parts} ·
inv{dist,price,dStruct,capped,floored,sd,ref,src}`. Объекты, возвращённые
продакшн-функциями, кладутся ЦЕЛИКОМ и без округления: поле, не записанное
сегодня, из годовалой записи не восстанавливается, а стоит оно байты. Outcome line: `p0 · p1 · hi · lo` plus, per side,
the ISO hour of first touch of `tgt` / `stop` / `wait` and `first ∈
tgt|stop|tie|null`. `tie` means both levels fell inside one hourly candle and
the order is genuinely unresolvable — recorded, not guessed.

**Three decisions worth keeping after the TZ is archived.**

1. **Daily, not hourly.** §3.10c measured daily resampling worth exactly 1.00×
   against weekly at a 7–14 day horizon, because consecutive dates share 6/7 of
   the forward window; hourly buys 24× the storage and zero independent
   observations. `[решение принято мной]` Discarded: hourly. Reversed if the
   Boss starts trading intraday.
2. **Coverage is 25 of 28 by construction.** `fut:true` pairs (HYPE, XMR, LIT)
   have no spot mirror, and Binance production hosts answer HTTP 451 from
   Actions (inv. 24). They are attempted on every run and recorded as explicit
   skip lines, so the gap is measured rather than assumed.
3. **`#N` is NOT recorded.** The board's number is produced inside `update()` by
   `byScore` → strip filter → `assignRanks`, which is not callable in isolation;
   recording it would mean reimplementing it, and inv. 21 forbids that. It is
   fully derivable at analysis time from the recorded `score`, `rp`, `rel`,
   `tier`. Deriving is free; duplicating is a silent divergence waiting to
   happen.

**What the journal is for, in order:** (a) an audit trail of what the Boss
actually saw; (b) the compensating control that makes `catalysts.json` safe —
once the registry is a freely editable file, the acting set and its hash sit
next to every verdict; (c) eventually, a live sample. It is NOT a backtest and
carries no predictive claim: §3.10b's resolution ceiling applies to it
unchanged, and one year of daily records is ~52 independent 7-day windows.


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

**Capital-efficiency follow-up (14.08.2026, same `run_raw.json`).** The
Boss's question — rank candidates by expected outcome for a $1–2k futures
position — reduces exactly: P&L per dollar of margin = L · move, and the
engine sets L ≈ risk_budget / dist, so P&L/margin ≈ risk_budget · move/dist
= risk_budget · R-multiple. Ranking by capital EV is therefore ranking by
expected R-multiple, nothing else. Measured (R = realized return ÷ realized
MAE inside the window, floored at 2 % and capped at ±5 — hindsight risk in
the denominator, i.e. the construction FAVOURS the hypothesis): LONG
IC(score, R) = −0.027 [−0.069; +0.015], SHORT +0.014 [−0.027; +0.057];
№1 above the list's median R on 47 % of dates on both sides; №1 R-excess
+0.08 / +0.24 with CI covering zero. Null with a handicap → null without.
The cost side is deterministic and already priced on the board: at $1.5k
margin × 4X = $6k notional, round-trip taker = $6, funding at 0.01 %/8h
≈ $12.6/week (0.05 %/8h ≈ $63) against a typical 14d absolute move of
9.5 % median / 13.9 % mean = $570–830. Cross-candidate cost SPREAD is
~6 % of a typical move whose SIGN is unpredictable (IC ≈ 0) — sorting by
it is sorting the second decimal of an unknown number. No EV ranking.

**Regime follow-up (14.08.2026) — supersedes the degenerate 13/132 split.**
The original split («trend = BTC 90d drift significant») left 13 trend
dates and was unpowered. Rebuilt look-ahead-free: BTC 14d return is exact
in the raw dump (`fwd − exc`, cross-coin sd = 0), so the TRAILING 14d BTC
return at date t is the forward return of date t−2 (weekly grid). Buckets:
trend-up > +5 % (51 dates) · range ±5 % (50) · trend-down < −5 % (41);
plus an expansion split on trailing mean |14d move| across the list, high
vs low half (70 / 72 dates). Score IC by bucket, both sides, doubled bar
(|IC| ≥ 0.10, CI99 clear of zero): every one of the ten cells is null;
the largest |IC| anywhere is 0.058 (SHORT · trend-down) with CI99 spanning
zero, and no bucket even reaches the single bar of 0.05. Powered split,
same answer → RANGE/TREND/EXPANSION conditioning is measured worthless as
a directional switch. Expansion already lives where it is defensible — in
risk, as the production caps `vol7/vol90 > 2 → 3X`, `Vol ≥ 2 %/h → 2X`,
`Vol ≥ 3 %/h → no leverage` (§3.2).

Both live directional hypotheses from §10 are now measured zeros: the
directional layer remains human (catalysts + REVIEW) by design, and the
tool's edge — risk, sizing, honesty — is confirmed as a result, not a
fallback. Re-running a lab mode requires a new external argument, not a
re-roll of the same data.

### 3.10b Resolution ceiling — what this bench can and cannot see (14.08.2026)

<!-- EDIT-MARKER 2026-08-14b-RESOLUTION-CEILING -->

A permanent property of the SAMPLE, not of any one experiment. Fixed here so
that no future proposal has to re-derive it, and so that no future null is
misread as «данных мало».

Sample: 145 weekly dates x ~24.4 coins/date. Measured block-bootstrap
SE(IC) = 0.020-0.023 (0.0215 used below); the block SE runs ~1.35x the iid
value, and that ratio is what rescales the figure to other universe widths.

| Test family | z* (FWER 5%) | true \|IC\| needed for 80% power |
|---|---|---|
| one pre-registered primary | 1.96 | 0.060 |
| ~15 cells (one experiment + its exploration) | 2.90 | 0.080 |
| 45-66 pairwise interactions | 3.21-3.31 | 0.087-0.089 |
| 66 pairs x 2 sides x 3 horizons | 3.68 | 0.097 |

Two consequences, both load-bearing:

1. **Everything measured so far sits inside the null.** ~40 cells have been
   run (score 6, res7 12, funding 9, regime 10, R-multiple 2). In a world
   with zero signal anywhere, the EXPECTED largest \|IC\| across 40
   correlated cells is 0.049, 90th pct 0.063. Observed largest: 0.058
   (SHORT · trend-down, CI99 through zero). The entire body of exploration
   is statistically indistinguishable from pure noise — which is the
   correct reading of it, and the reason nothing has ever been promoted.
2. **Universe width is the binding constraint, and it cannot be bought.**
   SE(IC) scales as 1/sqrt(n-3): at 24.4 coins/date the detectable \|IC\|
   is 0.068; at 6 coins/date, 0.181; at 4, 0.314. Calendar time helps only
   as 1/sqrt(D) — doubling to 290 weekly dates (another 2.75 years of
   waiting) moves the single-test bar from 0.060 only to 0.043. The
   standing decision «новые монеты не добавляем» (§10) therefore also
   fixes this system's measurement resolution permanently. That is a
   deliberate trade — a list the Boss can actually watch, against the
   ability to validate weak factors — and it is settled in favour of the
   watchable list.

### 3.10c Next architectural gate — what would reopen advanced ranking (14.08.2026)

<!-- EDIT-MARKER 2026-08-14c-NEXT-GATE -->

§3.10b states the resolution ceiling. This section states what would MOVE it,
what that costs, and the exact evidence that reopens the layer. Nothing here
is built. It exists so the answer is decided BEFORE the next proposal
arrives, not after.

**The binding dimension is universe width, and only universe width.**
SE(IC) = 1.198 / sqrt((n-3)*D), calibrated on the measured 0.0215 at
n = 24.4, D = 145. Moving one dimension at a time:

| Target \|IC\| | via coins alone | via history alone |
|---|---|---|
| 0.040 | n = 52 | D = 329 (6.3 years) |
| 0.030 | n = 89 | D = 585 (11.2 years) |
| 0.020 | n = 197 | D = 1315 (25.2 years) |

**Sampling more often is worth exactly zero — measured, not assumed.**
Sampling the same calendar span daily instead of weekly gives 7x the rows
and a **1.00x** improvement in SE, because consecutive daily dates share 6/7
of the same forward window (simulation, 4000 replications). Independent
periods are calendar time divided by holding horizon; that identity cannot
be worked around. Shortening the horizon to 1d would multiply periods by 7
but would validate a factor we do not trade, in the most arbitraged part of
the market. Rejected.

**Detection is not the whole bar: fitting costs signal.** Out-of-sample IC
actually delivered by a fitted cross-sectional ranker when the TRUE IC is
0.030, k = fitted parameters, 12 replications per cell:

| Configuration | detection bar | k=6 | k=15 | k=60 |
|---|---|---|---|---|
| today: 24 coins x 2.8y | 0.060 | 0.021 | 0.019 | 0.003 |
| wide bench: 120 x 2.8y | 0.026 | 0.025 | 0.019 | 0.016 |
| wide + 5.6y | 0.018 | 0.026 | 0.023 | 0.018 |
| wide + 11.1y | 0.013 | 0.032 | 0.027 | 0.021 |

A cell passes only where delivered exceeds the bar. Three tiers follow, with
different fates:

- **Tier 1 — a SINGLE pre-specified factor, nothing fitted.** Unlocked by
  universe width alone: bar 0.060 -> 0.026 at n = 120. This is the class
  every incoming proposal actually belongs to (basis, funding variants, a
  named interaction term specified in advance). Reachable today.
- **Tier 2 — a fitted multi-factor / interaction model (k >= 15).** Needs
  the wide bench AND ~5.6 years — wide bench plus 2.8 more years of
  accumulation. Reachable ~2029, not before.
- **Tier 3 — ML ranking (k ~ 60 effective parameters).** Needs the wide
  bench AND ~11 years. **ML ranking is therefore PERMANENTLY rejected for
  this system, not conditionally** — this upgrades the §8/§10 line from a
  judgement call to an arithmetic fact.

**Research-universe specification, if and when tier 1 is triggered**
`[решение принято мной]`: Binance USDS-M perpetuals, target **n = 120**
(150 buys only 0.026 -> 0.023 for 25 % more fetch; below 100 the tier-1
unlock is lost). Filters in order: (1) >= 3 years of continuous hourly
candles in `data.binance.vision`, no listing gap > 48 h — the binding
filter; (2) median 24h notional over the sample >= $30M; (3) exclude
wrapped duplicates, pegged assets and 1000X-style pairs — they inflate n
without adding independent cross-section; (4) **delisted perps MUST be
included for the period they traded.** Point 4 is not optional: today's
28-coin bench is survivorship-biased by construction (it is today's list).
At n = 24 with everything null that bias is harmless; at n = 120 with a
factor near threshold it could manufacture the result. Cost: ~120 pairs x
36 monthly ZIPs, bench-only, production untouched, no new runtime
dependency, no new failure point in the hourly bot.

**Transfer gate — a VETO, never a confirmation.** Any factor passing on the
wide universe is re-measured on the 28 traded coins; required: same sign,
and the 28-coin point estimate inside the wide-universe CI95. That test
resolves only \|IC\| >= 0.060, so it can KILL a factor (a small-cap /
illiquid effect absent from our segment — exactly the failure mode the
external literature predicts) but can never bless one. Blessing stays with
the wide-universe primary plus the standing +26-week fresh-data confirmation
run (§3.10a).

**The prize, sized honestly.** A validated IC = 0.030 factor is worth
0.57 % per selection to the top-1 pick over the list mean (cross-sectional
sd of 14d excess return 9.8 %, E[best of 24] = 1.95 sigma) — about $34 per
trade at $1.5k margin x 4X, ~$890/year at 26 selections. Real, but 17x
smaller than a typical 14d move, and it would take ~2300 live trades to
separate from luck. **Even a fully validated factor could therefore never be
confirmed by the Boss's own trading experience — using it would be an act of
trust in the bench.** That is the true size of the prize, and it is why the
gate is deliberately expensive.

**BUILD TRIGGER — the archive is not perishable.** The wide bench is NOT
built now. Waiting costs nothing in data: `data.binance.vision` is
historical, so building it in 2027 yields 2027's history including
everything back to 2023. Building it now with no hypothesis queued costs a
large fetch, CI time and a second universe to keep in sync, and buys a
fishing expedition — precisely what pre-registration exists to prevent.
Discarded alternative: build it now to «be ready»; rejected because
readiness carries no expiry advantage here.

**THE GATE, IN ONE LINE.** The wide bench is built the first time a named
tier-1 hypothesis arrives carrying an external effect size **>= 0.030 IC,
measured on a LIQUID cross-section (top-100 by volume or equivalent), at a
7-14 day horizon.** An effect size from a small-cap universe, or a claim of
predictiveness with no number attached, does not open the gate.

## 4. Инварианты — НЕ ЛОМАТЬ
1. Схема `coeffs.json` — только аддитивные изменения; `err_result` в боте синхронен по ключам с успешным результатом.
2. Новые монеты — только `TOKENS` (бот) + `tokens[]` (фронт). Проверять: id CoinGecko, спот-пару, фьюч, квоту. Нет спот-пары, есть перп → обязателен `fut:true`.
3. `history.json` ≤ 720 точек; чтение с обработкой `truncated` через `raw_url`.
4. `STALE_WARN 75` / `STALE_CRIT 130` мин ↔ ЧАСОВОЙ ТЕМП Shortcuts (cron'а нет, §1); менять только парой. **Внутри ночной паузы 02:00–09:00 локальных красный порог сам по себе НЕ означает сбоя:** возраст сравнивается с последним ПЛАНОВЫМ прогоном 01:50, допуск — один пропущенный час; два пропущенных — уже сбой.
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
33. **Один канал — один смысл, и ни один канал не спорит с глифом (ред. 19.08 (4)).** На карточке и на доске: ЧИСЛО + СЛОВО говорят о МЕСТЕ в рейтинге и СИЛЕ ВНИМАНИЯ, ГЛИФ (`stateMark`) — о СОСТОЯНИИ входа: пусто = сделка, `~` = ждать откат, `✕` = сделки нет. Одно слово в двух ролях уже заставило Босса прочитать две живые шорт-сделки как пустую сторону (19.08); попытка развести их одним цветом продержалась один день и произвела обратную ошибку — рейтинг без номеров (19.08 (3)). Различие не имеет права нестись только цветом И не имеет права стирать число. Обе поверхности обязаны брать глиф и текст вердикта из ОДНИХ функций (`stateMark`, `verdictNote`): доска, молчащая о запрете карточки, — тот же дефект.
    **Поправка 19.08 (4).** ЦВЕТ выведен из роли «качество счёта» в роль «состояние»: при `action === 'none'` бейдж гаснет до `#888`, цвет тира остаётся только на `trade` и `wait`. Причина — живая доска 19.08: на 10 из 10 карточек зелёный «#1 Сильный 90» стоял над красным `✕`, и Босс прочитал бейдж как рекомендацию. Цвет — самый громкий канал на телефоне, и он утверждал ровно обратное глифу. Это НЕ возврат к «различию одним цветом» (запрещено выше): глиф и число на месте, цвет лишь перестал их опровергать.
    **Ред. 20.08 — Босс вернул словарь сделки.** «ВНИМАНИЕ / СРЕДНЕЕ / СЛАБОЕ / ФОН» → «Сильный / Средний / Кандидат / Фон», формат бейджа «Сильный #1 — 91», цвета: зелёный / бирюза (`--cyan`) / жёлтый (`--accent`) / серый. Решение Product Owner'а, оно перекрывает правку 19.08 (4). Риск («Сильный» звучит как разрешение войти) снят ДРУГИМИ средствами того же релиза: строка плана печатает вход/цель/стоп только там, где движок сделку разрешил, счёт ниже 35 вообще не выходит на доску, а запрещённая карточка по-прежнему гаснет до `#888`. Гашение сохранено вопреки букве спецификации `[решение принято мной]` — альтернатива (красить запрещённые карточки в цвет тира) возвращает ровно тот дефект, о котором Босс написал 19.08. Отменяется, если Босс сообщит, что теряет полосу тира на отклонённых карточках.
    **Ранг капитализации потерял «#»** («кап 54↑2»): два разных «#» на одной карточке были той самой «смешанной логикой» из письма 20.08. Символ «#» теперь принадлежит только месту в рейтинге счёта.
    **Прежняя формулировка 19.08 (4):** «Сильный / Средний / Кандидат / Наблюдать» → «ВНИМАНИЕ / СРЕДНЕЕ / СЛАБОЕ / ФОН». Счёт — приор сортировки с измеренной нулевой предсказательной силой (§10, IC ≈ 0.058) и МДЛ `✕` на всех карточках; слово «Сильный» присваивало ему качество, которого у него нет. Пороги 70/50/35 и `TIER_STRONG/TIER_MID/TIER_MIN` не сдвинуты.
    **Цена отката вернулась в глиф:** `~ $1.0089` вместо голого `~` плюс «ждать $1.0089 — …» в строке причин. Это осознанная отмена части правки 19.08 (3), а не рецидив: цена по-прежнему печатается РОВНО ОДИН раз, слово «ждать» удалено как избыточное (сама цена рядом с `~` и есть рекомендация), а строка причин сохранила причину. Требование Босса от 19.08.
34. **Номер = МЕСТО В РЕЙТИНГЕ, и он есть у каждой карточки со счётом.** Порядок — строго по счёту (`byScore`, окно ничьей 0.05 разрешается рангом капитализации), нумерация сплошная 1..N по показанному списку. Состояние входа не имеет права ни переставлять список (сортировка «сначала торгуемые» уронила лучшего шорт-кандидата LIT под две слабые карточки), ни отнимать номер (нумерация «только торгуемых» стёрла номер у 74 % карточек и превратила верный порядок в видимую случайность). Номера не получают только строки без счёта и свёрнутые как нерелевантные стороне (`row.off`). `byScore`, `assignRanks`, `tierBadge`, `stateMark`, `verdictNote` — отдельные функции именно затем, чтобы стенд мог их проверять.
30. **Одна монета — ОДНА сторона.** Гарантия даётся НЕ геометрией, а слоем режима (§3.12, слой 4): стресс — ни одной, тренд — только по направлению рынка, диапазон — только сторона с большим счётом возврата. Стенд показал, что одной геометрии НЕ хватает: монета в середине широкого диапазона проходит R:R ≥ 2 С ОБЕИХ сторон (ZEC 19.08: 1:1.6 и 1:2.9). Убрать правило режима = вернуть противоречие 18.08.
31. **Катализатор умеет ТОЛЬКО ветировать.** Ни поднять счёт, ни отменить вето геометрии он не может. Именно катализатор, поставленный выше геометрии, произвёл шорт GRAM на дне диапазона 18.08. Запрет держит внешний ввод вне ранжирования — то, что требует §3.10b.
32. **Геометрия не предсказывает и не обязана.** На блуждании `E[R] = 0` при ЛЮБОМ отборе — это теорема, подтверждённая контролем `--control` (−0.001 при 2SE 0.080). Любое будущее утверждение вида «вето подняло точность» обязано сначала объяснить, откуда взялся снос или издержки.
26. **Денежный потолок не убивает сделку.** `риск маржи` участвует в `min`, но с полом `L_MIN`: `убыток/маржа = dist·L` не зависит от размера позиции, то есть это правило про ДОЛЮ СЧЁТА, а не про выживание. «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» имеют право выдавать только три первых потолка.

35. **Цену входа и цель печатает только разрешённая сделка.** `planLine` выходит пустой при `action === 'none'`: напечатать «вход/цель» там, где геометрия или режим отказали, значит выдумать рекомендацию, которой у модели нет — это ровно тот запрет, который Босс сформулировал 20.08 («Do not invent or display a price if the calculation is not sufficiently reliable»). Ни одно число строки не считается заново: цель — тот же экстремум 90д, что берёт `tradeGeometry`, стоп — тот же `dec.inv.price`, R:R — тот же `geo.rr` (инв. 20). Строка живёт только у тиров Сильный и Средний.
36. **Счёт ниже `TIER_MIN` не выходит на основную доску, но и не исчезает молча.** Такие монеты уходят в ту же раскрываемую полосу, что и монеты у нерелевантного края диапазона, с раздельными счётчиками причин. Порядок проверок фиксирован: сначала слабый счёт, потом положение — иначе одна монета попадала бы в обе группы и счётчики не сходились бы с длиной полосы. Деградированные строки (нет пары / мёртвый рынок / нет метрик) НЕ прячутся никогда: это операционные предупреждения, а не кандидаты. Если кандидатов 35+ нет вовсе, доска печатает одну нейтральную строку и остаётся пустой намеренно.

37. **Молчание обязано быть объяснено — и объяснение обязано быть машинным.** Прогон, который не записал данные, обязан вернуть НЕНУЛЕВОЙ код; каждый прогон обязан оставить одну grep-пригодную строку с `generated_at`; ночная пауза обязана отличаться от сбоя не глазом, а правилом (`freshnessState`, инв. 4). Причина не в аккуратности логов: дыра в выборке, у которой нет причины, неотличима от «событий не было», и выборка с необъяснимыми дырами не выдерживает ни одного статистического утверждения. Отсюда же правило учёта в журнале: пропущенная дата пишется строкой-пробелом, а не отсутствием строки (§3.13). **Стенд, не подключённый к `bench.yml`, не исполняется ни разу и контролем не является** — `fresh_bench.js` простоял в этом состоянии с ТЗ-04 до ТЗ-05. Родня инв. 22, 25, 29: все четыре — способы выглядеть зелёным, ничего не проверив.
38. **Журнал — прибор, и запись в нём неизменяема.** Три правила, каждое ломается молча и потому вынесено в инвариант. **(1) Вердикт производится ИСПОЛНЕНИЕМ продакшн-скрипта** — функции вырезаются из `index.html` и вызываются по имени (инв. 21). Вторая реализация любого правила, порога или формулы запрещена в любом языке и любом файле: журнал, считающий вердикт сам, документирует не систему, а свою копию системы. **(2) Файл, однажды записанный, не открывается на изменение никогда** — ни для дозаписи исхода, ни для правки. Исход живёт в отдельном файле и присоединяется ключом; повторный прогон, увидев существующий файл, пишет `dup` и выходит нулём. Неизменяемость сделана физической, а не обещанной, потому что запись, которую можно переписать, перестаёт быть свидетельством ровно в тот момент, когда результат не понравился. **(3) Рядом с вердиктом лежит то, чем его можно объяснить:** действовавший набор катализаторов и его хеш, отпечаток скрипта и коммита. Без отпечатка записи разных версий движка сливаются в одну выборку — и это ошибка, которую нельзя обнаружить постфактум.

## 5. Лимиты
- **CoinGecko: бот ходит БЕЗ КЛЮЧА.** В `main.yml` в env передаётся только
  `GIST_TOKEN`, `COINGECKO_API_KEY` не передаётся → `api_key=None` →
  публичный доступ без месячной квоты, ограничение по IP раннера, обходится
  паузой `REQUEST_GAP_SEC = 1.0` и тремя попытками. Проверено 10–11.08:
  `error = null` у всех 28 монет.
- **Бесплатный ключ Demo подключать НЕЛЬЗЯ при нынешнем расписании.** Demo
  даёт 100 вызовов/мин, но потолок 10 000/мес. Расход: 17 плановых запусков в день (Shortcuts, §1) ×
  30 вызовов ≈ 15 300/мес, плюс триггер `push` гоняет полный прогон бота на
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
| **Open Interest — ЗАКРЫТ НАВСЕГДА 14.08.2026** (и как сигнал, и как отображение) | Три независимых довода. (1) Funding — рыночная ЦЕНА того же дисбаланса, что OI измеряет количеством; z-скученность и уровень измерены нулём с узким ДИ (§3.10a), поэтому условная вероятность, что количественная мера несёт сигнал, которого нет в цене, много ниже 10 %. (2) Мощность: 145 недельных дат × 24 монеты различают \|IC\| ≳ 0.06; правдоподобный эффект OI на 7–14д лежит ниже этого порога, то есть даже честный прогон не смог бы отличить его от нуля — тест без разрешающей способности не проводят. (3) Отображение «новые деньги / закрытие позиций» держалось только на будущей направленной пользе: без неё это метрика, не меняющая решение — прямой запрет из правил. Цена отказа нулевая: 28 запросов / 5 мин и новая точка отказа не появляются. Развернёт только внешнее свидетельство, что позиционирование Binance предсказывает 7д-доходность крупных капитализаций **при размере эффекта, различимом на нашей выборке** |
| Ранжирование по ожидаемой прибыли на капитал ($1–2k) | Сводится тождеством к ранжированию по ожидаемому R-мультипликатору (движок уже выравнивает риск на маржу: P&L/маржа ≈ бюджет риска · ход/дистанция). Измерено с форой гипотезе — риск взят задним числом — IC −0.027 / +0.014, №1 выше медианы R в 47 % дат (§3.10a). Издержки (комиссия, funding) детерминированы, уже стоят на доске в USDT, и их РАЗБРОС между кандидатами ≈ 6 % типичного хода, знак которого непредсказуем. Ликвидность на размере $3–10k номинала не различает 28 перпов (та же причина, что строкой «Ликвидность фьючерсов») |
| Режим RANGE/TREND/EXPANSION как условие скоринга | Мощное деление построено 14.08 (тренд вверх 51 дата / диапазон 50 / тренд вниз 41; расширение 70 / сжатие 72, всё без взгляда в будущее) — десять ячеек из десяти нулевые, максимум \|IC\| = 0.058 при ДИ99 через ноль (§3.10a). Прежняя строка «вырожденное деление» больше не единственный довод: теперь ноль измерен на выборке, которая эффект увидела бы. Расширение уже реализовано там, где оно законно — в потолках риска §3.2 |
| **Нелинейный слой взаимодействий факторов — ОТКЛОНЁН 14.08.2026** | Три независимых довода. (1) **Сегмент не тот.** Источник (взаимодействия на 40 характеристиках, 500+ монет, 2017–2023) сам показывает сетевым анализом, что прибыль аномалий живёт в МАЛЫХ и НЕЛИКВИДНЫХ монетах, где издержки мешают арбитражу, а ведущие пары — меры ликвидности (оборот, спред) с мерами риска. Наш список — 28 топовых перпов Binance, ровно дополнение к этому сегменту. (2) **Механика не переносится.** Двойная сортировка 5×5 при 500 монетах даёт 20 монет в корзине; при наших 24.4 — ОДНУ. Сортировать нечего. (3) **Мощность.** Семейство из 45–66 парных взаимодействий требует истинного \|IC\| ≈ 0.087–0.089 (§3.10b) — в полтора раза больше максимума, когда-либо измеренного в системе (0.058), который сам равен ожидаемому максимуму ЧИСТОГО шума при нашем числе ячеек. Плюс: взаимодействие с наибольшим приором — фактор × режим — уже измерено на мощном делении, 10 ячеек из 10 нулевые |
| **Order flow / микроструктура как фактор ранжирования — ОТКЛОНЁН 14.08.2026** | Ошибка категории в самом источнике применительно к нашей задаче: предиктор там — **world order flow**, агрегат потоков в 11 фиатных валютах, то есть ОДНО число на дату, общее для всех монет. Величина, постоянная по кросс-секции, имеет кросс-секционный IC = 0 тождественно: это таймер РЫНКА, а наша задача — «какую из 28 взять». Приводимые R² 10.4 % (день) / 19.6 % (неделя) относятся к синхронной (одновременной) связи потока с доходностью, не к предсказанию. Данных нет и не будет: поток в 11 фиатах — платный агрегат по венчурам; Binance открыто отдаёт только `aggTrades` по USDT-парам одной биржи, то есть заведомо не «world». Цена — терабайты тиков и постоянный ETL против уже принятого решения по внутридневной микроструктуре (§10: масштаб времени сигнала — часы, удержание Босса 1–14 дней) |
| **Кросс-секционный базис срочных фьючерсов — ОТКЛОНЁН 14.08.2026** | Развилка из двух ветвей, обе закрыты. (а) Базис ПЕРПЕТУАЛА = премиум-индекс, из которого Binance и считает funding — та же величина в другом виде (строка «Спот/перп базис» выше), а funding измерен нулём: IC +0.003, ДИ95 [−0.030; +0.039]. (б) Базис СРОЧНОГО контракта — величина действительно независимая, но её нет на нашем списке: квартальные поставочные Binance это USDⓈ-M только BTC/ETH и COIN-M BTC/ETH/BNB/ADA/LINK/BCH/XRP/DOT/LTC; пересечение с нашими 28 — **шесть монет** (ETH, BNB, ADA, LINK, BCH, XRP), все COIN-M. Кросс-секция из шести различает только \|IC\| ≳ 0.18 (§3.10b) — теста с таким разрешением не проводят. Третий довод из самого источника: доходность базисного фактора сильна на ДНЕВНОМ шаге, СЛАБЕЕ на недельном, незначима на месячном — эффект затухает ровно на нашем горизонте 7–14д |

## 9. Журнал миграций
- 2026-08-21 (2): **ТЗ-04 в коде, ТЗ-05 написано, карта закрывает пункт 0 очереди.**
  **ТЗ-04 (достоверность свежести) — в зеркалах Проекта, слито Боссом.** Бот: `run_line()` печатает одну grep-пригодную строку на прогон (`<статус> <этап> generated_at=<iso> coins=<n> errors=<n>`) и возвращает ненулевой код на каждом пути отказа — BTC `2`, Gist `3`, исключение `4`; прежде провалившийся прогон выглядел зелёным. Фронт: `freshnessState(ageMin, now)` вынесена чистой функцией (ни DOM, ни собственных часов внутри) и внутри окна 02:00–09:00 сверяет возраст не со `STALE_*`, а с последним ПЛАНОВЫМ прогоном 01:50 — новое состояние `pause` серым вместо красного `! Молчит`; допуск прощает ровно один пропущенный час. Константы расписания `SCHED_FIRST_H/SCHED_LAST_H/SCHED_LAST_M` — по одному числу на систему (инв. 20). Математика, счёт, движок плеча, схема `coeffs.json` и CSS не тронуты.
  **Найдено при подготовке ТЗ-05 и не исправлено ТЗ-04:** `bench/fresh_bench.js` существует, но НЕ подключён к `bench.yml` — то есть не исполнялся ни разу и контролем не является. Правка входит в ТЗ-05.
  **ТЗ-05 (журнал «вход → вердикт доски → факт») написано, НЕ исполнено, НЕ слито.** Контракт — новый §3.13: суточная запись, файлы только на дозапись, вердикт исполняется из `index.html` (инв. 21), рядом кладутся действовавший набор катализаторов, его хеш и отпечаток скрипта; исход отдельным файлом на (дата × горизонт), первое касание цели/стопа/цены отката с честным `tie`; покрытие 25 из 28 (три `fut:true` без спотового зеркала, инв. 24); `#N` не записывается сознательно — выводится из `score`/`rp`/`rel` продакшн-функциями, а не дублируется. Модель исполнителя — Opus: четыре новых файла, правка CI, сетевой фолбэк и формат, ошибки которого неисправимы задним числом.
  **Новые инварианты 37–38.** 37 — молчание обязано быть объяснено машинно, и стенд без строки в `bench.yml` контролем не является. 38 — журнал неизменяем физически, вердикт не имеет права быть посчитанным второй реализацией, рядом с вердиктом обязано лежать то, чем его можно объяснить.
  **Ни одна формула, константа, схема и ни один файл кода этой правкой карты не тронуты.**
- 2026-08-21: **правка карты по факту автоматизации; кода нет, формул нет.** §1 описывал `GitHub Actions (cron ~1 раз/час)` и бюджет 21.6k/мес от 24 прогонов в сутки. Cron снят Боссом 16.06.2026 (`acd4315`), возвращён 20.08 в ТЗ-02 на ложной находке отчёта-2 (shallow-клон скрыл 39 коммитов истории `main.yml`) и снят повторно в PR #2. Реальный триггер — Shortcuts на iPhone, раз в час 09:00–01:50 = 17 плановых прогонов ≈ 15.3k/мес. §1 и §5 расходились между собой (21.6k против 16.7k) — приведены к одному числу. Инв. 4 перепривязан к темпу Shortcuts и к ночной паузе 7 ч 10 мин, внутри которой `STALE_CRIT` загорается штатно. §10: порядок работ пересмотрен — журнал ПЕРЕД `catalysts.json`, добавлен пункт 0 «достоверность свежести» (ТЗ-04). Ни одна формула, константа, схема и ни один файл кода не тронуты.
- 2026-08-20: **сверка второй живой доски + отображение по спецификации Босса. Торговая математика не тронута ни на символ.**
  **Сверка (`bench/board2_bench.js`, 129 проверок, 0 отказов; продакшн-функции исполняются из `index.html`, инв. 21).** Проверены девять карточек 02:04–02:07 и ДВА полных экрана CRYPTO FUTURE (XRP ЛОНГ 3X, UNI ШОРТ 3X). Сошлось точно: ликвидация 3X от прогноза и от входа; ликвидация после долива маржи (2X); перенос прогноза бетой; положение в диапазоне 90д; `gateState` на всех девяти (включая три новых `~`); безубыток 7д с издержками 0.31 % объёма у XRP и с ОТРИЦАТЕЛЬНЫМ costFrac у UNI (funding перекрывает комиссии); защёлка 1R; убыток по стопу и по ликвидации в деньгах и в долях маржи; размер долива; воспроизведение всех напечатанных R:R через `tradeGeometry`; непрерывность и уникальность номеров на обеих сторонах.
  **Главная находка сверки — метрики не «поплыли».** Между 01:08 и 02:04 у всех монет изменились β и R², а МДЛ у трёх переехал с `✕` на `~`. Причина одна: слайдер перешёл через ноль, прогноз BTC стал ВЫШЕ цены, и доска переключилась с `down_*`-регрессии на `up_*` (`ratio >= 0 ? cd.up_beta : cd.down_beta`). Доказательство: ρ (`corr_90`) НЕ зависит от направления и совпал во всех шести сверенных парах до второго знака, тогда как β₉₀ разошлась (BNB 0.88→0.70, UNI 1.42→1.13, SKY 0.91→0.71). Данные стабильны, переключение — по проекту.
  **Стороны не подавлены.** Счёт считается на обеих сторонах при любом исходе (проверено вызовом обоих каналов). Из шести ЛОНГ-карточек четыре закрыты вето R:R < 2.0 с напечатанной причиной, две выдали живой уровень входа (HBAR $0.0678, RENDER $1.2842). ШОРТ закрыт целиком слоем режима (инв. 30) — правило, а не сбой; строка режима над списком его называет.
  **Сделано (7 участков, только отображение):** `tierOf` — словарь и цвета по спецификации (Сильный зелёный / Средний бирюза / Кандидат жёлтый / Фон серый); `tierBadge` — формат «Сильный #1 — 91»; ранг капитализации — «кап 54↑2» без «#»; новая `planLine` — ВХОД (зелёный пульс «СЕЙЧАС» либо оранжевый пульс с ценой) · ЦЕЛЬ · СТОП · R:R для тиров Сильный и Средний и только при разрешённой сделке; счёт ниже `TIER_MIN` уходит в раскрываемую полосу; полоса печатает раздельные счётчики причин; пустая доска печатает одну нейтральную строку.
  **Не тронуто:** `scoreCandidate`, `momentumScore`, `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`, `catalystCheck`, `directionVerdict`, `byScore`, `assignRanks`, `leverageDecision`, `invalidationInfo`, `protectionPlan`, `liqPrice`, схема `coeffs.json`, бот, CSS, keyframes (инв. 1, 9, 13, 15, 18, 19). Пульс — существующий `light-blink`. Ни одна константа не изменена; diff употреблений показал только НОВЫЕ чтения `TIER_MID` (+1) и `TIER_MIN` (+4).
  **Валидация:** `bench/badge_bench.js` — 133 240 проверок, 0 отказов, прежняя и новая сборки грузятся обе и сравниваются на одних входах (числовая поверхность совпадает побитово); `bench/board2_bench.js` — 129; `bench/verify_board.js` (доска 19.08) — 108, всё ещё зелёный. `node --check` пройден. Новые инварианты 35–36, инвариант 33 переписан.
- 2026-08-19 (4): **сверка живой доски + четвёртая редакция бейджа. Торговая математика не тронута ни на символ.**
  **Повод.** Босс прислал скриншоты ЛОНГ и ШОРТ (01:08–01:09, 3X, Normal, BTC $69 727 / $69 589) и потребовал полной сверки: «почти на каждой монете красный ✕, включая Сильных; шорт-сторона особенно; и это противоречит твоему же анализу рынка».
  **Что проверено и оказалось ВЕРНЫМ (`bench/verify_board.js`, 108 проверок на десяти живых карточках, продакшн-функции исполняются из `index.html`, инв. 21):** ликвидация 3X от прогноза (`liqPrice`, все 20 значений сходятся до 5e-4); перенос прогноза BTC бетой на монету (все 10, включая три карточки, отрисованные на промежуточном тике BTC ≈ $69 518 — расхождение −0.22 %/−0.29 %/−0.03 % объясняется ОДНИМ и тем же тиком, а не ошибкой); положение в диапазоне 90д (`rangePos`, все 10); границы тиров 70/50/35; порядок списка строго невозрастающий по счёту на обеих сторонах; вето R:R — все напечатанные 1:0.9, 1:0.7, 1:1.4 действительно ниже `RR_MIN = 2.0`; `gateState` — МДЛ `✕` на 10 из 10 карточек математически верен (Conf < 40 у восьми, R²₁₄ < 0.25 у XRP и AVAX). **Арифметических дефектов не найдено.**
  **Почему шорт-сторона пуста целиком.** `marketRegime` вернул `trend`, `dir = +1` (BTC +7.9 % за сутки, eff14 выше `EFF_TREND`). Слой 4 `directionVerdict` закрывает сторону против тренда ЦЕЛИКОМ (инв. 30) — «против тренда рынка» на всех 28 карточках это работа правила, а не сбой. Дефект был в том, что режим НИГДЕ не печатался: Босс видел 28 запретов без единого объяснения.
  **Сделано (5 участков, только отображение):** `tierOf` — слова тира на «ВНИМАНИЕ / СРЕДНЕЕ / СЛАБОЕ / ФОН»; `tierBadge` — бейдж гаснет до `#888` при `action === 'none'`; `stateMark` — цена отката печатается рядом с глифом (`~ $1.0089`); `verdictNote` — «ждать $X — » удалено, причина осталась; новая `regimeBanner` — одна строка над списком называет режим и говорит, открыта ли сторона.
  **Не тронуто:** `scoreCandidate`, `momentumScore`, `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`, `catalystCheck`, `directionVerdict`, `byScore`, `assignRanks`, `leverageDecision`, `liqPrice`, схема `coeffs.json`, бот, CSS, keyframes (инв. 1, 9, 13, 15, 18, 19). Ни одна константа не изменена и не переиспользована (сверка употреблений `TIER_*`, `RR_MIN`, `EFF_TREND`, `ENTRY_CHASE_SD`, `LIQ_MMR`, `MAX_MARGIN_LOSS`, `RES_Z`, `PACE_Z`, `TGT_SIGMA_MIN` — diff пустой).
  **Валидация:** `bench/badge_bench.js` — 132 824 проверки, 0 отказов; старая и новая сборки грузятся ОБЕ и сравниваются на одних входах (40 000 вызовов `scoreCandidate`/`momentumScore`/`qualityScore`/`rangePos`/`gateState`, 6 000 вызовов `tradeGeometry`, 3 000 `marketRegime`/`liqPrice`) — числовая поверхность совпадает побитово. `node --check` пройден. Инвариант 33 переписан (поправка 19.08 (4)), новый пункт очереди в §10.
- 2026-08-19 (3): **третья редакция отображения §3.12 — рейтинг снова виден.** Причина — видео Босса ЛОНГ/ШОРТ: список был отсортирован ВЕРНО, но номер и счёт печатались только у торгуемых карточек, остальные несли глухое серое «НАБЛЮДАТЬ». Замер на прежней сборке: **74 % карточек со счётом не печатали номер вообще** (3538 из 4808 на 400 случайных списках). На экране первой стояла монета с лучшим счётом с надписью «НАБЛЮДАТЬ», второй — «#1 Средний 53»: доказательство порядка было стёрто, и рейтинг читался как случайная россыпь. Попутно слово «Наблюдать» всё ещё значило две вещи — нижний тир и вердикт (инв. 33 держался только цветом, что он сам же и запрещает).
  **Сделано:** `assignRanks` нумерует КАЖДУЮ карточку со счётом, сплошь 1..N по уже отсортированному списку; привязка номера к `TIER_MIN` и к состоянию удалена. Свёрнутые как нерелевантные стороне помечаются `row.off` и номера не получают — сквозной номер у монеты вне рейтинга стороны лгал бы о месте. Сборка бейджа вынесена из цикла отрисовки в `tierBadge(row)`, состояние — в `stateMark(row)`: бейдж стал тестируемым, а глиф — единым для карточки и доски. Вердикт словами вынесен из `verdictLine` в `verdictNote(row)` и напечатан ТЕМ ЖЕ текстом на доске, где его раньше не было вовсе. Цена отката переехала из бейджа в строку причин («ждать $0.3337 — вход далеко от суточной опоры»); попутно исправлена формулировка, верная только для лонга.
  **Словарь после правки:** число + слово + цвет = МЕСТО и КАЧЕСТВО; глиф = СОСТОЯНИЕ входа (пусто = сделка, пульсирующий `~` = ждать откат, `✕` = сделки нет). Глифы взяты у МДЛ, который уже стоит на той же карточке — второго языка не заведено. Пульс — прежний `light-blink`, новых keyframes нет (инв. 19 цел).
  **Математика, счёт, движок плеча, схема `coeffs.json`, бот, CSS, порядок блоков доски и ключи якоря не тронуты** (инв. 1, 9, 13, 15, 18). Дифф фронта: 5 участков, −33/+46 строк, из них 30 — комментарии.
  **Валидация (продакшн-код исполняется из `index.html`, инв. 21):** `bench/display_bench.py` — 24 598 проверок, 0 отказов (порядок невозрастающий по счёту с производственным окном ничьей 0.05, нумерация сплошная и согласованная с порядком, номер и счёт присутствуют при любом вердикте, глифы, границы тиров 70/50/35 без сдвига) плюс количественный свидетель дефекта на прежней сборке. `bench/render_bench.py` — 123 сценария, 24 157 проверок, 0 отказов: реальный `update()` и реальный `renderBoard()` на данных формы `coeffs.json` + тикер Binance, включая деградированные строки (нет пары / мёртвый рынок / нет метрик), развёрнутый блок нерелевантных, пустой ответ бота и режим ОБЗОР. `node --check` и `py_compile` пройдены.
- 2026-08-19 (2): **вторая редакция отображения §3.12 по спецификации Босса.** Причина — пост-деплой: слово «Наблюдать» означало и тир 35–49, и вердикт «сделки нет», из-за чего две активные шорт-сделки (ETH #1, SOL #2) были прочитаны как пустая сторона. Сделано: тиры переименованы (70+ Сильный / 50–69 Средний / 35–49 Кандидат / ниже — серый Наблюдать), границы вынесены в `TIER_STRONG/TIER_MID/TIER_MIN` (инв. 20); состояние ЖДАТЬ получило собственный цвет `--orange` и пульс через СУЩЕСТВУЮЩИЙ `light-blink` (новых keyframes нет, инв. 19 цел); сортировка переведена СТРОГО на счёт (`byScore`), нумерация — в `assignRanks`, приоритет состояния удалён вместе с `actRank`; `directionVerdict` теперь считает счёт ПРИ ЛЮБОМ исходе, чтобы ни одна карточка не выпадала из ранжирования. **Торговая математика и расчёт счёта НЕ тронуты:** тождество `scoreCandidate` снова проверено на 200 000 входах, 0 расхождений. Новый режим стенда `--display`; всего 747 447 проверок, провалов 0. Новые инварианты 33–34.
- 2026-08-19: **Движок направления — каскад вето (§3.12).** Причина: 18.08 система выдала два противоположных вывода на одних данных (GRAM доска = лонг #1 / анализ = шорт; ZEC зеркально). Добавлены пять слоёв: `marketRegime` · `tradeGeometry` · `momentumScore` · `catalystCheck` · `directionVerdict`, плюс `verdictLine`/`actRank` для рендера. **Проверенная математика не тронута ни на символ:** `leverageDecision`, `invalidationInfo`, `protectionPlan`, `liqTouchProb`, `lStruct`, `lNoise`, `advBeta`, `lBtcCheck`, `residual7`, `shortMaturity`, `tierOf` сверены побайтово. Общий хвост счёта вынесен в `qualityScore`/`scoreFinish` без изменения арифметики — 200 000 случайных входов, 0 расхождений. Новый стенд `bench/direction_bench.py` (5 режимов, 689 786 проверок, провалов 0). Дифф фронта: 13 участков, −25/+307 строк. Бот, схема `coeffs.json`, CSS, порядок блоков доски и ключи якоря не изменены (инв. 1, 9, 15, 18). Новые инварианты 30–32. Живой архивный бэктест НЕ прогнан: `data.binance.vision` закрыт сетевой политикой среды (HTTP 403), остаётся за Боссом.
- 2026-08-14c: **next architectural gate defined in numbers — §3.10c.
  Map-only diff, zero code, nothing built.** The Boss asked what would have
  to change before advanced predictive technology could responsibly reopen.
  Answer: universe width, and nothing else. Coins are elastic (n = 89
  reaches \|IC\| 0.030), history is not (the same bar needs 11.2 years);
  sampling daily instead of weekly is measured worth 1.00x because
  consecutive dates share 6/7 of the forward window. Fitting costs signal on
  top of detection, which splits the roadmap into three tiers with different
  fates: single pre-specified factors unlock on a 120-coin research bench
  today, fitted multi-factor models need ~5.6 years, ML ranking needs ~11
  and is now permanently rejected on arithmetic rather than judgement.
  Research-universe spec, transfer-gate-as-veto, and the survivorship
  requirement (delisted perps included for their live period — today's bench
  is survivorship-biased by construction) are all fixed in §3.10c. The prize
  is sized: a validated 0.030 factor is worth ~$34/trade and ~2300 live
  trades to prove, i.e. never confirmable from the Boss's own experience.
  **Nothing built:** the archive is not perishable, so deferring costs zero
  data; the build trigger is a named tier-1 hypothesis carrying an external
  effect size >= 0.030 IC on a liquid cross-section at 7-14 days.
- 2026-08-14b: **three external research directions assessed, all three
  REJECTED; the analytical layer is declared COMPLETE at the current
  evidence level. Map-only diff — zero code, zero product change.**
  (1) Nonlinear interaction layer: the source effect lives in small,
  illiquid coins by its own network analysis and needs a 500-coin
  cross-section to double-sort — our 5x5 grid would hold 1 coin per bucket,
  and an interaction search needs true |IC| ~0.087-0.089 against a system
  maximum of 0.058 that is itself the expected maximum of pure noise.
  (2) Order flow: the source predictor is WORLD order flow — one number per
  date shared by all coins, so its cross-sectional IC is zero by
  construction; the quoted R2 are contemporaneous, not predictive; the data
  is a paid 11-fiat aggregate that Binance's public API cannot reproduce;
  intraday microstructure was already out of scope on holding-period
  grounds. (3) Futures basis: perp basis is mechanically the premium index
  behind funding (measured null, tight CI); dated-futures basis exists for
  6 of our 28 coins, a cross-section resolving only |IC| >= 0.18, and the
  source's own horizon gradient has the factor dying between daily and
  weekly. New **§3.10b** records the bench's permanent resolution ceiling
  so no future proposal re-derives it; **§8** gains three rows; **§10**
  gains the admission rule for any future factor. Header date corrected
  11.08 -> 14.08 (it contradicted the migration log).
- 2026-08-14: **analytical layer CLOSED — three questions answered by
  measurement, zero code, zero product change.** (1) Capital-efficient
  ranking for a $1–2k position: proved identical to ranking by expected
  R-multiple (the engine already equalises risk per margin), measured with
  hindsight risk in the denominator as a handicap in favour of the
  hypothesis — still null on both sides, №1 above median R on 47 % of
  dates; costs are deterministic, already on the board, and their
  cross-candidate spread is ~6 % of a move whose sign is unpredictable.
  Rejected in §8. (2) OI: closed PERMANENTLY as signal and as display —
  funding is the price of the same imbalance and reads zero with a tight
  CI, our sample resolves only |IC| ≳ 0.06 so the test would have no
  power, and the display was justified solely by the directional value
  that does not exist. §10 queue item struck; yesterday's pre-gate void
  with its feature. (3) Regime RANGE/TREND/EXPANSION: the degenerate
  13/132 split replaced by a powered look-ahead-free one (51/50/41 by
  trailing BTC 14d, 70/72 by trailing expansion) — ten of ten cells null,
  max |IC| 0.058 with CI99 through zero. Expansion stays where it is
  legitimate: the §3.2 risk caps. Numbers in §3.10a.
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
- **Слой контекста: как рыночная разведка попадает в калькулятор (архитектура принята 20.08, код НЕ написан).**
  Вопрос Босса: почему прямой анализ рынка 19.08 оказался полезнее механической доски и можно ли встроить его систематически. **Ответ по существу: дело не в весах, а во входных данных.** Двигателем дня 19.08 был удвоенный выкуп длинных облигаций Минфином США — величина, которой нет ни в одном входе калькулятора. Никакая перенастройка `scoreCandidate` этого не исправляет; исправляют только новые данные. Отсюда деление на три класса и три разных режима допуска:
  1. **Датированные проверяемые события** (голосование, разлок, заседание, слушание). Машинно представимы: `{sym, date, dir, kind, text, src}`. Потребитель уже есть — `catalystCheck`, и он по инв. 31 умеет ТОЛЬКО ветировать и подписывать, никогда не двигать счёт. Первый шаг: перенести `CATALYSTS` из литерала в `catalysts.json`, который кладёт рядом с `coeffs.json` тот же workflow, что гоняет бота. Схема аддитивная: отсутствие файла не меняет ни одного числа (инв. 1, 9).
  2. **Непрерывные измеримые величины, которых бот не тянет** (нетто-приток в спот-ETF, комиссионная выручка протокола, открытый интерес, TVL, календарь разлоков как темп роста предложения). Объективны и воспроизводимы, но каждая — новый фактор, а значит §3.10 и инв. 32: сначала архивный бэктест на `data.binance.vision`, потом вход в счёт. Без бэктеста — только отображением.
  3. **Суждение аналитика** (чтение режима, тезис, «это сквиз, а не тренд»). НЕ представимо машинно и НЕ должно попадать в модель: закодированное мнение — это переобучение на одного аналитика, а не сигнал. Место суждения — чат, а не веса.
  **Порядок работ — ПЕРЕСМОТРЕН 21.08.** Было: (1) `catalysts.json` → (2) журнал → (3) бэктест. Стало:
  **(0) Достоверность свежести.** Бот обязан возвращать ненулевой код, когда запись не состоялась; `generated_at` обязан быть виден в логе прогона; ночная пауза обязана отличаться от сбоя. Без этого дыра в выборке неотличима от «событий не было», а выборка с необъяснимыми дырами не выдерживает ни одного статистического утверждения. ТЗ-04.
  **(1) Журнал** «вход → вердикт доски → факт» — **ТЗ-05 написано 21.08, §3.13; не исполнено и не слито**. Ставится ПЕРВЫМ, потому что это единственный артефакт, ценность которого строго падает со временем: каждый неотжурналированный час теряется навсегда. **Ретроспективно вердикт НЕ восстанавливается:** `history.json` хранит только беты, R² и ранг — без цены, `min/max`, `volatility` и объёма, а `scoreCandidate`, `tradeGeometry` и `leverageDecision` требуют именно их. Журнал обязан писаться ИСПОЛНЕНИЕМ продакшн-скрипта (инв. 21), а не второй реализацией вердикта, и обязан класть рядом действовавший набор катализаторов.
  **(2) `catalysts.json`** — вынос `CATALYSTS` из литерала в данные. Даёт правку катализатора без деплоя, но ОСЛАБЛЯЕТ контроль: сегодня вето проходит через ТЗ, исполнителя, PR и аудит, после — через одну правку файла. Компенсация — журнал из пункта (1), уже пишущий действовавший набор рядом с вердиктом. Поэтому (2) ПОСЛЕ (1), а не до.
  **(3)** Только когда выборка есть — бэктест одного фактора из класса 2. Пункт (3) не открывать, пока не закрыт (1).
  `[решение принято мной]` Отброшена альтернатива «сохранить прежний порядок». Причина: она производит период, в котором вердикты уже зависят от свободно правимого файла, а измерить этот эффект нечем. Разворот — если журнал окажется дороже двух ТЗ: тогда сначала дешёвый `catalysts.json`, но с обязательной фиксацией версии файла в каждом будущем журнальном рекорде.
- **Цель геометрии не зависит от канала — структурное натяжение, СОЗНАТЕЛЬНО не исправлено 19.08 (4).**
  `tradeGeometry` не принимает режим: цель всегда `cd.max_price` для лонга и `cd.min_price` для шорта, то есть экстремум 90д — цель ВОЗВРАТА. В режиме `trend` ранжирует `momentumScore` — канал ПРОДОЛЖЕНИЯ. Монета с сильным импульсом стоит близко к своему экстремуму 90д, оставшаяся до цели награда мала, и R:R разбивается о `RR_MIN = 2.0`. Живой замер 19.08: SKY счёт 90 → 1:0.9, ZEC 78 → 1:0.7, BNB 67 → 1:1.4 — ни одна карточка канала импульса не прошла ворота.
  **Почему не тронуто.** Вето по существу ВЕРНО: покупка ZEC на $577 после +13.5 % за сутки, на 74 % диапазона, со структурным стопом в 24.5 % и 17 % до цели — плохая сделка независимо от канала. Механизм натяжения доказуем по коду, но утверждение «континуационная цель дала бы лучший исход» — гипотеза без бэктеста, а §3.10/инв. 32 запрещают менять ворота сделки на гипотезе. Строгой монотонности «выше счёт → ниже R:R» на живых данных НЕТ (SKY 0.9 против ZEC 0.7), так что даже направление эффекта на трёх точках не установлено.
  **Условие открытия:** архивный бэктест на `data.binance.vision`, сравнивающий исход `RR ≥ 2` к экстремуму 90д против континуационной цели (например, `E + k·σ·√H`) на одних и тех же входах канала импульса. Без него — не трогать.
Порядок — результат аудита 10.08 (пять пунктов Босса + три идеи его ассистента). Внутри каждого пункта указана цена и что именно он меняет.

**Принято, ждёт очереди**
~~0. **Lab runs (12.08.2026)** — `--stops`, `--res7`, `--funding`, verdict rules fixed in §3.10a, awaiting a manual `workflow_dispatch` on cache key v4.~~
   — **закрыт 12.08 вечером, run №4: см. §3.10a Results и «Сделано»**
~~3. Потолок риска маржи жёстким.~~ — **закрыт 11.08, см. «Сделано»**

<!-- `MAX_MARGIN_LOSS = 0.35` сейчас справочный (§3.4). Расчёт: включённый целиком, он связывает 15 типовых комбинаций из 16 и роняет ИТОГ ниже `L_MIN` в семи. Причина — дистанция, упёршаяся в `INV_CAP_SD`: там стоп нарисованный, и денежное правило применять к нему нельзя. Версия, которую стоит обсуждать: жёсткий потолок при `inv.capped = false` И `inv.src ≠ 'вход'`, справочная строка во всех остальных случаях.
-->
~~1. **Open Interest** — отложен; показывать одним состоянием «новые деньги / закрытие позиций», не сырыми числами. Ворота-бэктест позиционирования добавлены 13.08.~~
   — **ЗАКРЫТ НАВСЕГДА 14.08.2026, см. §8.** Ворота-бэктест из записи 13.08 тем самым отменены вместе с самой фичей: измерять нечего, если показывать нечего.
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
  ~~Reversal conditions (13.08): external evidence on Binance positioning ratios, or the deferred OI feature proceeding — in which case this backtest is its mandatory pre-gate.~~
  **Superseded 14.08.2026: OI closed permanently as signal AND display (§8),
  so the pre-gate is void with its feature. Any reversal now requires an
  external effect size our sample could actually resolve (|IC| ≳ 0.06), not
  merely a claim of predictiveness.** Until then the machine owns risk,
  sizing and honesty; the human owns catalysts via REVIEW. Final.
- **ANALYTICAL LAYER — COMPLETE at the current evidence level. Verdict
  14.08.2026, after the three external directions the Boss forwarded
  (nonlinear interactions / order flow / cross-sectional futures basis)
  were assessed and all three rejected — §8.**
  <!-- EDIT-MARKER 2026-08-14b-LAYER-COMPLETE -->
  This is NOT «мы исчерпали идеи». It is a measured statement about this
  system's resolution. Three independent facts, each sufficient alone:
  (1) every directional cell ever measured here — ~40 of them — lies inside
  the null distribution for that number of tests (§3.10b);
  (2) the effect sizes in the external literature are produced on
  cross-sections of 84 to 500+ coins, 3-20x our width, and the published
  mechanisms locate the profit in small, illiquid, high-cost assets — the
  exact complement of a 28-coin top-perp list;
  (3) our detection threshold is set by universe width, which the standing
  «новые монеты не добавляем» decision fixes permanently at |IC| ~0.06-0.07
  for a single pre-registered test and ~0.09 for any search.
  **Operative rule from here:** a new ranking factor is admissible ONLY on
  an external prior that names an effect size THIS sample could resolve, on
  a cross-section shaped like ours, at a 7-14 day horizon. «Предсказывает в
  литературе» is not such a prior and never was. Absent that, additions to
  the analytical layer buy complexity and false precision, not accuracy.
  The division of labour is final: the machine owns risk, sizing, honesty
  and geometry; the human owns direction via catalysts and REVIEW.
  **Refined 14.08.2026 — §3.10c now states the NEXT GATE in numbers:** the
  only elastic dimension is universe width (n = 120 research universe moves
  the bar 0.060 -> 0.026, bench-only); daily resampling is measured worth
  exactly 1.00x; tier-1 single factors become testable at once, fitted
  multi-factor models need ~5.6 years, and ML ranking needs ~11 years and is
  therefore permanently — not conditionally — rejected. The wide bench is
  NOT built now: the archive is historical, so deferring costs nothing,
  while building it without a queued hypothesis buys a fishing expedition.
  Build trigger: a named single-factor hypothesis with an external effect
  size >= 0.030 IC on a LIQUID cross-section at 7-14 days.
- **DIRECTION ENGINE (§3.12) — built 19.08.2026, and it does NOT reopen the
  layer closed above.** The closure stands: it bans new RANKING FACTORS, and
  §3.12 adds none. No factor entered `scoreCandidate`, no weight was tuned, no
  metric claims predictive power. What was added is a filter with zero
  predictive content (geometry), a switch (regime) and a manual external veto
  (catalysts). The measured control is explicit that geometry CANNOT raise
  mean R on a driftless market — it works against costs and drift only.
  The operative rule above («a new ranking factor is admissible ONLY on an
  external prior naming an effect size this sample could resolve») is
  unchanged and still binding.
  **Open item, not built:** regime hysteresis. `EFF_TREND = 0.6` labels ~55 %
  of driftless windows as trend (measured), which is harmless for direction
  but can make the label flap between hourly renders and reshuffle the list.
  Build trigger: the Boss reports flapping. Not built pre-emptively — that
  would be a second trend constant against inv. 20 on speculation.
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
