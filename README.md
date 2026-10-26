# 7th & Hill · email templates for Klaviyo

Стиль Collector's Edition (за макетом YAKO Digital Studio): кремова сторінка, темно-зелені смуги, Bodoni Moda + Jost, фото в білих «паспарту», підпис Sally.
Відправник: **Sally at 7th & Hill** &lt;hello@7thandhilljewelry.ca&gt; · сайт: https://www.7thandhilljewelry.ca

```
templates/              6 готових шаблонів (кожен — самодостатній HTML)
  welcome-1.html        Welcome 1/3 · привітання, Sally, історія назви
  welcome-2.html        Welcome 2/3 · філософія і матеріали (solid gold, made to order, book box)
  welcome-3.html        Welcome 3/3 · як обрати прикрасу
  campaign-master.html  базовий шаблон розсилки (заголовок, банер, текст, 2–4 картки, кнопка)
  thank-you.html        після покупки + догляд за прикрасами
  abandoned-cart.html   м'яке нагадування про кошик
blocks/cards-3-up.html  блок «3 картки в ряд» для campaign-master
assets/images/          лого і фото, підготовлені з ваших файлів
preview.html            усі шаблони поруч (desktop / mobile / dark mode / з іменем і без)
klaviyo/               ті самі шаблони, готові до вставки в Klaviyo
scripts/build.py        оновлює preview.html і klaviyo/
```

Вихідні файли, з яких узято лого, фото і факти (`7th & Hill Launch Emails.zip`, PDF-каталог, PNG), лежать у корені репозиторію.

## Як переглянути
Відкрийте `preview.html` у браузері (на GitHub: файл → кнопка «Download raw file» → відкрити завантажений файл).

## Як вставити в Klaviyo
Готові до вставки файли лежать у папці **`klaviyo/`**. Картинки в них підтягуються з цього репозиторію (гілка `main`) через jsDelivr, тож нічого окремо завантажувати не треба.

1. Відкрийте потрібний файл у `klaviyo/` на GitHub і натисніть **Copy raw file** (значок копіювання над кодом).
2. Klaviyo → **Content → Templates → Create template → HTML** (або *Code your own*).
3. Виділіть увесь стартовий код у редакторі, вставте скопійоване, натисніть **Save**, назвіть шаблон.
4. У флоу або кампанії: відкрийте лист → **Change template / Select template** → **Saved templates** → виберіть свій.

Після правок у `templates/` оновіть і `preview.html`, і `klaviyo/` однією командою:

```
python3 scripts/build.py
```

Якщо картинки колись переїдуть на інший хостинг (наприклад, Shopify Files): `python3 scripts/build.py --base-url https://…/files/`.

## Що де міняти
Кожен шаблон починається з коментаря з **Subject**, **Preheader**, **From** і рекомендованим тригером флоу. Блоки позначені коментарями `BLOCK: …` і є цілими рядками `<tr>…</tr>`: їх можна дублювати, переставляти й видаляти цілком.

| Що | Де |
|---|---|
| Прехедер | перший `<div style="display:none…">` після `<body>` |
| Лого | `assets/images/logo.png` — кругле чорне лого з білим написом, показується 66×66. Читається і на світлому, і на темному фоні, тому темна тема його не ламає |
| Фото | блоки `PHOTO · …` / `BANNER` — фото в білій рамці. При заміні оновіть `width`/`height` під пропорції (вказані в атрибутах) |
| Заголовок / текст | блоки `INTRO`, `TEXT`, теги `<h1>`, `<p>` |
| Кнопка | коментар `BUTTON` — текст у `<span>`, посилання в `href` |
| Картки (campaign) | `CARDS · ROW A` і `ROW B`, по 2 картки, квадратні фото. 2 картки — видаліть ROW B; 3 — замініть обидва рядки на `blocks/cards-3-up.html`. Посилання карток зараз ведуть на `/collections` — підставте потрібні колекції |
| Зелена смуга | блоки `… (green band)` — список з римськими цифрами або три «обіцянки» (Solid gold · Book box · Duties) |
| Підпис | блок `SIGNATURE · Sally` |
| Футер | `BLOCK: FOOTER` — меню, email, адреса, відписка |
| Кольори | #ECE8E0 сторінка · #DEDAD2 фон · #1A1816 заголовки · #2C2925 текст · #7A5E30 золото · #1F3A30 зелений · #CDAA6D світле золото |

## Змінні Klaviyo
- `{{ first_name|default:'' }}` — у привітаннях, обгорнуто в `{% if first_name %}…{% else %}…{% endif %}`, щоб без імені текст лишався правильним.
- `{{ event.extra.checkout_url|default:'…/cart' }}` — кнопка в abandoned-cart (подія Shopify *Started Checkout*).
- Футер (обов'язково для CASL): «7th & Hill Jewelry», `{{ organization.full_address }}`, email для зв'язку, `{% unsubscribe %}` і `{% manage_preferences %}`. Адресу (190 Roslin Avenue, Toronto, Ontario M4N 1Z6) задайте в Klaviyo → Settings → Organization.

## Факти, використані в текстах
Узяті з погодженого документа YAKO: Sally Brooks, founder & designer; Modern Heirlooms. Timeless Classics.; назва від перехрестя 7th & Hill у Лос-Анджелесі (батько — gold leaf letterer у St. Vincent's Jewelry Center); браслет бабусі Lily 1913–2013; solid gold, не тьмяніє; made to order у Торонто, Лос-Анджелесі та Італії; зелена book box з оксамитом; in stock — 1–2 робочі дні; безкоштовний resize кілець; доставка по світу, мита покриваються.
Поради з догляду в `thank-you.html` загальні — звірте з вашою сторінкою Jewelry Care.

## Сумісність
- Таблична верстка, інлайн-стилі, контейнер 600px, гібридні колонки (картки складаються в стовпчик на мобільному навіть без media queries).
- Outlook (Windows): ghost-таблиці `<!--[if mso]>`, шрифти примусово Georgia/Arial, кнопка з відступами через `mso-text-raise`. Тіні рамок Outlook не показує — це нормально.
- Шрифти: Bodoni Moda → Didot / Bodoni 72 → Georgia; Jost → Helvetica Neue → Arial; Pinyon Script (підпис) → Snell Roundhand → Georgia italic.
- Темна тема: стилі для Apple Mail і Outlook.com; зелені смуги і лого лишаються як є.
- Кожен шаблон < 26 KB (Gmail обрізає листи від 102 KB).

## Перед запуском
- Перевірте посилання (`/collections`, `/collections/design-your-own-jewelry`, `/pages/about-salt`, `/pages/jewelry-care`, `/pages/contact`).
- Надішліть тестові листи в Gmail, Apple Mail, Outlook (Klaviyo → Preview & test).
