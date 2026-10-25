# 7th&Hill · email templates for Klaviyo

Відправник: hello@7thandhilljewelry.ca · сайт: https://7thandhilljewelry.ca

```
templates/            6 готових шаблонів (кожен — самодостатній HTML)
  welcome-1.html      Welcome 1/3 · привітання та історія бренду
  welcome-2.html      Welcome 2/3 · філософія і матеріали
  welcome-3.html      Welcome 3/3 · як обрати прикрасу
  campaign-master.html базовий шаблон розсилки (банер, текст, 2–4 картки, кнопка)
  thank-you.html      після покупки + догляд за прикрасами
  abandoned-cart.html м'яке нагадування про кошик
blocks/cards-3-up.html  блок «3 картки в ряд» для campaign-master
assets/images/        лого і фото (зараз — плейсхолдери, замініть файлами з тими ж іменами)
preview.html          усі шаблони поруч (desktop / mobile / dark mode / з іменем і без)
scripts/build.py      оновлює preview.html і збирає dist/ для Klaviyo
```

## Як переглянути
Відкрийте `preview.html` у браузері. Після будь-яких змін у шаблонах або фото:

```
python3 scripts/build.py
```

## Як завантажити в Klaviyo
1. Завантажте файли з `assets/images/` на хостинг зображень (Shopify → Content → Files, або Klaviyo → Content → Images). Імена файлів не міняйте.
2. Зберіть версії з абсолютними шляхами:
   ```
   python3 scripts/build.py --base-url https://cdn.shopify.com/s/files/XXXX/files/
   ```
   (`--base-url` — адреса папки, де лежать файли; у Shopify Files усі файли мають спільний префікс.)
3. Klaviyo → Content → Templates → Create template → **HTML** → вставте вміст файлу з `dist/`.

Без кроку 2 картинки в Klaviyo не відобразяться: у `templates/` шляхи відносні (`../assets/images/…`) — лише для локального перегляду.

## Що де міняти
Кожен шаблон починається з коментаря з **Subject**, **Preheader** і рекомендованим тригером флоу. Блоки позначені коментарями `BLOCK: …` і є цілими рядками `<tr>…</tr>`: їх можна дублювати, переставляти й видаляти цілком.

| Що | Де |
|---|---|
| Прехедер (сірий рядок у списку листів) | перший `<div style="display:none…">` після `<body>` |
| Лого | `assets/images/logo.png` (440×80, показується 220×40) і `logo-footer.png` (280×52). **Світле лого на суцільному фоні #131210, без прозорості** — так його не «з'їсть» темна тема |
| Головне фото | `BLOCK: HERO IMAGE` — файл 1200×800 (у campaign 1200×900, thank-you / cart 1200×700). При зміні пропорцій оновіть `height` |
| Заголовок / текст | `BLOCK: INTRO…`, теги `<h1>`, `<p>` |
| Кнопка | коментар `BUTTON` — текст у `<span>`, посилання в `href` |
| Картки (campaign) | `CARDS · ROW A` і `ROW B`, по 2 картки. 2 картки — видаліть ROW B; 3 — замініть обидва рядки на `blocks/cards-3-up.html`. Фото 520×640 |
| Посилання футера | `BLOCK: FOOTER` (Shop / About / Contact) — перевірте, що `/pages/about` і `/pages/contact` існують на сайті |
| Кольори | у `<style>` у `<head>` і в інлайн-стилях: #131210 (ніч), #F6F3EE (сторінка), #1F1D1A (текст), #5E584F (другорядний текст), #8F7A52 (акцент) |

## Змінні Klaviyo
- `{{ first_name|default:'' }}` — у привітаннях, обгорнуто в `{% if first_name %}…{% else %}…{% endif %}`, щоб без імені не було «, you've found us».
- `{{ event.extra.checkout_url|default:'…/cart' }}` — кнопка в abandoned-cart (подія Shopify *Started Checkout*). Поза флоу веде на `/cart`.
- Футер (обов'язково для CASL): назва відправника, `{{ organization.full_address }}`, email для зв'язку, `{% unsubscribe %}`. Адресу задайте в Klaviyo → Settings → Organization.

## Сумісність
- Таблична верстка, інлайн-стилі, контейнер 600px, гібридні колонки (картки самі складаються в стовпчик на мобільному навіть без media queries).
- Outlook (Windows): ghost-таблиці `<!--[if mso]>`, шрифти примусово Georgia/Arial, кнопка з відступами через `mso-text-raise`.
- Шрифти: Cormorant Garamond (Apple Mail, iOS) → Georgia / Times New Roman; текст — Helvetica Neue → Helvetica → Arial.
- Темна тема: шапка і футер уже темні, тому лого не міняється; для Apple Mail і Outlook.com є окремі темні стилі світлої частини.
- Кожен шаблон < 25 KB (Gmail обрізає листи від 102 KB).

## Перед запуском
- Замініть плейсхолдери в `assets/images/` справжніми лого і фото.
- Звірте тексти з фактами бренду (матеріали, походження) і посилання на сторінки сайту.
- Надішліть тестовий лист у Gmail, Apple Mail, Outlook (Klaviyo → Preview & test).
