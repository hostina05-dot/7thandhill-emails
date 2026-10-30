# 7th & Hill · launch letters for Klaviyo

Отправитель: **Sally at 7th & Hill** &lt;hello@7thandhilljewelry.ca&gt;, ответы на hello@7thandhilljewelry.ca · сайт: https://www.7thandhilljewelry.ca

Дизайн: белая страница в тёмно-зелёной рамке, чёрная полоса 7 T H & H I L L, фото во всю ширину с круглой печатью на нижнем краю, изделия на светлом «лунном» фоне, тёмные блоки с золотым санберстом. Шрифты как на сайте: Cormorant (заголовки), Inter (текст), Montserrat Medium (строка 7 T H & H I L L); в Gmail/Outlook запасные Georgia и Arial. Зелёный Sally: #58744E.

## Где что лежит

```
templates/        32 письма в трёх группах: flow-, salt-, camp- (исходники, их пишет scripts/compose.py)
klaviyo/          те же письма, готовые к вставке в Klaviyo (картинки с хостинга)
preview.html      все письма в трёх группах (Flows, SALT list, Campaigns) с коротким описанием каждой
blocks/           готовые блоки для вставки + catalog.md (все изделия с номерами и ссылками)
assets/photos/    оригиналы фото и видео
assets/images/    готовые картинки для писем (после цветокоррекции)
assets/catalog.json  изделия: название, картинка, ссылка
assets/products/  все изделия с сайта на «лунном» фоне (600x600) + index.csv: код, название, тип, ссылка, файл
products.html     галерея всех изделий с сайта: код на каждой плитке, поиск по коду или названию
blocks/site-products.md  та же таблица кодов текстом
scripts/compose.py   тексты Sally и сборка всех писем из общих блоков
scripts/photos.py    цветокоррекция, кадрирование, печать на фото, GIF из видео
scripts/build.py     preview.html и klaviyo/
```

Имя файла = группа и код письма: `flow-w1-welcome.html`, `salt-t1-note-from-sally.html`, `camp-k3-holiday-deadline.html`. Первая строка комментария в каждом файле: группа, флоу, код, место в серии, триггер и задержка (для кампаний дата). Ниже: метка карточки, тема, прехедер, отправитель, логика флоу.

Всё запускается во вторник, 27 октября, тремя группами:

| Группа | Когда | Письма |
|---|---|---|
| `flow-` · Flows | автоматически с Fri Oct 30 | P0 попап · Welcome 01 (W1 to W5) · Cart 06 (C1, C2) · Checkout 07 (CO1 to CO3, консьерж CC1, CC2 от $5,500) · Browse 05 (B1, B2) · After purchase 10 (PP1 to PP3) · Anniversary 15 (AN1) |
| `salt-` · SALT list | с Fri Oct 30 | только T1, ежедневными волнами 200, 400, 800, затем по 1,500 в день, пока жалобы ниже 0.1% и отказы ниже 2% · дальше SALT получает кампании с K3 (Tue Nov 3), без welcome-флоу · кто не открыл и не кликнул за 30 дней, исключается (sunset) |
| `camp-` · Campaigns | по датам | K2 Sally’s Edit Fri Oct 30 · K3 Tue Nov 3 · K1 Tue Nov 10 · DYO Tue Nov 17 · S1 Wed Nov 25 18:00 · S2 Fri Nov 27 08:00 · S3 Mon Nov 30 · K4 Thu Dec 3 · K2 Tue Dec 8 · LC Tue Dec 15 · HN Thu Dec 24 (+ запасной макет K2 без даты) |

## Как посмотреть
https://raw.githack.com/hostina05-dot/7thandhill-emails/main/preview.html (после слияния в `main`).
Переключатели вверху: Desktop / Mobile, With name / No name, масштаб.

## Как вставить в Klaviyo
1. Откройте файл в `klaviyo/` на GitHub, нажмите **Copy raw file**.
2. Klaviyo → **Content → Templates → Create template → HTML**, замените стартовый код, **Save**.
3. Во флоу или кампании: письмо → **Change template → Saved templates**.
4. Тему, прехедер и отправителя возьмите из комментария в начале файла.

Картинки в `klaviyo/` грузятся через jsDelivr из конкретного коммита этого репозитория (адрес вида `…@<коммит>/assets/images/`). Так Klaviyo всегда показывает именно те фото, что в превью, без задержки кэша jsDelivr для ветки `main`. После замены фото: закоммитить и запушить картинки, затем пересобрать письма с новым коммитом:

```
python3 scripts/build.py --base-url https://cdn.jsdelivr.net/gh/hostina05-dot/7thandhill-emails@$(git rev-parse HEAD)/assets/images/
```

## Настройки в Klaviyo
- **Купон VAULT15**: уникальные коды, одно использование, 30 дней, не суммируется со скидками (в том числе с Black Friday 20%). В письмах стоит тег `{% coupon_code 'VAULT15' %}`, код вручную нигде не прописан.
- **Адрес** в подвале: «Toronto, ON M4N 3N1, Canada» (офисное здание рядом с мастерской Sally, где сдают помещения). Вписан прямо в подвал (`footer()` в `scripts/compose.py`), не через `{{ organization.full_address }}`: в настройках Klaviyo стоит домашний адрес. Когда будет номер дома и офиса, дописать их туда же.
- **SALT**: шага согласия нет, только T1 с купоном VAULT15 в P.S. Ссылка отписки в подвале. Аудитория кампаний с K3: Vault + SALT. Sunset: SALT-контакты без открытий и кликов за 30 дней исключаются.
- **Динамические блоки**: корзина (C1) берёт `event.Items`, браузинг (B1) берёт `event.ProductName/ImageURL/URL`, checkout (CO1 to CO3, CC1, CC2) ведёт на `event.extra.checkout_url`. Проверьте в Preview & test на реальном профиле.

## Как менять
Тексты и состав писем меняются в `scripts/compose.py`, затем:

```
python3 scripts/compose.py && python3 scripts/build.py
```

Новое фото или видео: положите оригинал в `assets/photos/`, впишите в `SHOTS`, `CLIPS` или `SLIDES` в `scripts/photos.py`, запустите `python3 scripts/photos.py`. Изделие в сетке = номер из `blocks/catalog.md`.

## Все изделия с сайта
`assets/products/` = все товары с www.7thandhilljewelry.ca на том же «лунном» фоне, что плитки в письмах: первое фото товара на белом, белый выровнен, изделие по центру с одинаковым воздухом (если на исходном фото оно обрезано краем кадра, этот край остаётся на краю плитки). У каждого изделия свой код по типу: **C** шарм, **R** кольцо, **E** серьги, **N** колье, **CH** цепочка, **B** браслет, **CN** коннектор, **L** замок, **O** другое. R012 = кольцо № 12. Файл: `R012-<адрес товара>.jpg`. Коды не меняются при обновлении, новые товары получают следующий свободный номер своего типа.

Чтобы поставить изделие в письмо, назовите код: в `scripts/compose.py` код работает как номер из каталога, например `grid("…", ["R012", "E005", "N031"])` или `("R012", "Своё название")`. Плитка сама копируется в `assets/images/site-R012.jpg`, название берётся с сайта без «14k Gold». Посмотреть: https://raw.githack.com/hostina05-dot/7thandhill-emails/claude/friendly-newton-8qmg2v/products.html

Обновить после новых товаров на сайте: скачать `products.json?limit=250&page=1..3` и фото товаров в одну папку (`img/<id товара>_<номер фото>.jpg`), затем `python3 scripts/site_products.py <папка>`.

## Правила текста (из брифа)
Без тире (кроме слов Sally, где тире её: W1 «…personalized jewelry—one piece, one story at a time»), без «Shop now», без «we love» и «stack»; мягкие кнопки (Step inside, Start a gift, Return to your bag). «Solid gold» вместо 14k. Ни слова о бесплатном ресайзе, вместо этого: «Not sure about size? Send me a photo of what you already wear, and I'll help you choose.» Праздники нейтрально: holiday, без ёлок. Слова Sally остаются как она написала.

## Waiting for Sally
1. Бесплатный ресайз колец: есть или нет.
2. Какие изделия только для подписчиков Vault.
3. Даты заказа к праздникам для K3 (предложены Nov 6, Nov 30, Dec 17).
4. Девять изделий для W3 (до Oct 29).
5. Шесть плиток коллекций в W1.
6. 14k или «Solid gold».
7. Бесплатная чистка в GTA как привилегия Vault.
