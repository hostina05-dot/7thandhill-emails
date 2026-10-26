# 7th & Hill · email templates for Klaviyo

Дизайн: современный, с нотками мистики, по макету K2 / 01.1. Белая страница в тёмно-зелёной «ночной» рамке, чёрная полоса 7 T H & H I L L, фото во всю ширину с круглым лого на нижнем краю, изделия на светлом «лунном» градиенте, тёмные ночные блоки с золотыми звёздочками ✦. Шрифты: Cormorant Garamond и Jost.
Отправитель: **Sally at 7th & Hill** &lt;hello@7thandhilljewelry.ca&gt; · сайт: https://www.7thandhilljewelry.ca

```
templates/               7 шаблонов (исходники)
  welcome-1.html         Welcome 1/3 · приветствие Sally, подборка, история названия
  welcome-2.html         Welcome 2/3 · философия и материалы, персонализированные изделия
  welcome-3.html         Welcome 3/3 · как выбрать, «Six pieces I'd start with»
  campaign-master.html   базовая рассылка (баннер, заголовок, текст, коллаж изделий, кнопка)
  thank-you.html         после покупки: уход за украшениями + шармы «в пару»
  abandoned-cart.html    мягкое напоминание о корзине + несколько любимых изделий
  salt-welcome.html      приветствие для контактов SALT (макет K2, «Sally's edit»)
klaviyo/                 те же шаблоны, готовые к вставке в Klaviyo
blocks/                  готовые блоки: collage, pieces-with-names, three-pieces, night-quote, find-your-piece
blocks/catalog.md        все 32 изделия из каталога со ссылками
assets/images/           фото с лого (hero-*), изделия (product-01…32), фото для коллажей (feature-*)
preview.html             все шаблоны рядом (desktop / mobile, с именем и без)
scripts/build.py         обновляет preview.html и klaviyo/
```

## Как посмотреть
https://raw.githack.com/hostina05-dot/7thandhill-emails/main/preview.html
или скачайте `preview.html` с GitHub (Download raw file) и откройте в браузере.

## Как вставить в Klaviyo
Готовые к вставке файлы лежат в папке **`klaviyo/`**. Картинки подгружаются из этого репозитория (ветка `main`) через jsDelivr, отдельно ничего загружать не нужно.

1. Откройте нужный файл в `klaviyo/` на GitHub и нажмите **Copy raw file** (значок копирования над кодом).
2. Klaviyo → **Content → Templates → Create template → HTML** (или *Code your own*).
3. Выделите весь стартовый код в редакторе, вставьте скопированный, нажмите **Save**, назовите шаблон.
4. Во флоу или кампании: откройте письмо → **Change template / Select template** → **Saved templates** → выберите свой.

После правок в `templates/` обновите `preview.html` и `klaviyo/` одной командой:

```
python3 scripts/build.py
```

Если картинки когда-нибудь переедут на другой хостинг (например, Shopify Files): `python3 scripts/build.py --base-url https://…/files/`.

## Что где менять
Каждый шаблон начинается с комментария: **Subject**, **Preheader**, **From** и когда отправлять. Блоки подписаны `BLOCK: …` и являются целыми строками `<tr>…</tr>`: их можно копировать, переставлять и удалять целиком. Готовые блоки для вставки лежат в `blocks/`.

| Что | Где |
|---|---|
| Прехедер | первый `<div style="display:none…">` после `<body>` |
| Главное фото с лого | `BLOCK: HERO`. Лого «впечатано» в картинку `hero-*.jpg`, поэтому никакой почтовый клиент его не сдвинет и не перекрасит. Новое фото с лого: пришлите фото, я подготовлю, или сделайте сами: 1200 px шириной, снизу белая полоса 80 px, лого 128 px по центру на границе фото и полосы |
| Заголовок и текст | `BLOCK: TITLE` |
| Изделия | `BLOCK: … collage` и `… pieces with names`. У каждого изделия: картинка `product-NN.jpg`, название и ссылка. Номера и ссылки всех 32 изделий: `blocks/catalog.md`, картинки всех 32 уже лежат в `assets/images/` |
| Анимированные ячейки | `anim-rings.gif`, `anim-charms.gif`, `anim-pendants.gif`, `anim-earrings.gif`: 1–2 ячейки коллажа плавно перебирают 3 изделия. Работает в Gmail, Apple Mail и на телефонах; Outlook для Windows показывает первый кадр. Новый набор изделий для такой ячейки: напишите, какие номера из `blocks/catalog.md`, я соберу GIF (150–290 КБ) |
| Фото для оформления | оригиналы в `assets/photos/`, оттуда делаются кадрировки для писем |
| Кнопка | комментарий `BUTTON`: текст в `<span>`, ссылка в `href` |
| Тёмный блок | `… (night band)`: цитата, список с ✦ |
| Подвал | `BLOCK: FOOTER`: сайт, Instagram, TikTok, адрес, отписка |

## Переменные Klaviyo
- `{{ first_name|default:'' }}` в приветствиях, обёрнуто в `{% if first_name %}…{% else %}…{% endif %}`.
- `{{ event.extra.checkout_url|default:'…/cart' }}` в abandoned-cart (событие Shopify *Started Checkout*).
- Подвал (обязательно для CASL): «7th & Hill Jewelry», `{{ organization.full_address }}`, email, `{% unsubscribe %}` и `{% manage_preferences %}`. Адрес (190 Roslin Avenue, Toronto, Ontario M4N 1Z6) укажите один раз в Klaviyo → Settings → Organization.

## Список SALT
`salt-welcome.html` для контактов, перенесённых из SALT Fine Jewelry. Отправляйте волнами по 200–300 и следите за жалобами на спам (держите их ниже 0,1%).
По CASL согласие, полученное другой компанией, не всегда переходит к новой. Надёжнее всего попросить подтверждение: добавить кнопку «Yes, keep me posted» и дальше писать только тем, кто нажал (как в письмах T1–T3 из документа YAKO). Проверьте это до запуска.

## Темная тема
Шаблоны объявлены как светлые (`color-scheme: light`): Apple Mail показывает их как есть. Gmail и Outlook в тёмной теме могут затемнить белый фон, но фото, лого и изделия — это картинки, они не меняются.

## Совместимость
- Таблицы, инлайн-стили, 600 px. Коллажи и ряды изделий в процентах, поэтому на телефоне просто уменьшаются, ничего не разваливается.
- Outlook (Windows): ghost-таблицы, шрифты Georgia/Arial, кнопка с отступами через `mso-text-raise`.
- Шрифты: Cormorant Garamond → Georgia; Jost → Helvetica Neue → Arial.
- Каждый шаблон меньше 25 KB (Gmail обрезает письма от 102 KB).

## Перед запуском
- Проверьте ссылки на Instagram (`instagram.com/7thandhilljewelry`) и TikTok (`tiktok.com/@7thandhilljewelry`): я поставил их наугад.
- Кнопки категорий ведут на поиск по сайту (`/search?q=rings` и т. п.). Если есть отдельные страницы коллекций, подставьте их адреса.
- Советы по уходу в `thank-you.html` сверьте со страницей Jewelry Care.
- Отправьте тестовые письма в Gmail, Apple Mail, Outlook (Klaviyo → Preview & test).
