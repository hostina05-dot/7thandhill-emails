# 7th & Hill · launch letters for Klaviyo

Отправитель: **Sally at 7th & Hill** &lt;hello@7thandhilljewelry.ca&gt;, ответы на hello@7thandhilljewelry.ca · сайт: https://www.7thandhilljewelry.ca

Дизайн: белая страница в тёмно-зелёной рамке, чёрная полоса 7 T H & H I L L, фото во всю ширину с круглой печатью на нижнем краю, изделия на светлом «лунном» фоне, тёмные блоки с золотым санберстом. Шрифты: Italiana (заголовки) и Jost (текст), в Gmail/Outlook запасные Georgia и Arial.

## Где что лежит

```
templates/        34 письма в трёх группах: flow-, salt-, camp- (исходники, их пишет scripts/compose.py)
klaviyo/          те же письма, готовые к вставке в Klaviyo (картинки с хостинга)
preview.html      все письма в трёх группах (Flows, SALT consent, Campaigns) с коротким описанием каждой
blocks/           готовые блоки для вставки + catalog.md (все изделия с номерами и ссылками)
assets/photos/    оригиналы фото и видео
assets/images/    готовые картинки для писем (после цветокоррекции)
assets/catalog.json  изделия: название, картинка, ссылка
scripts/compose.py   тексты Sally и сборка всех писем из общих блоков
scripts/photos.py    цветокоррекция, кадрирование, печать на фото, GIF из видео
scripts/build.py     preview.html и klaviyo/
```

Имя файла = группа и код письма: `flow-w1-welcome.html`, `salt-t1-note-from-sally.html`, `camp-k3-holiday-deadline.html`. Первая строка комментария в каждом файле: группа, флоу, код, место в серии, триггер и задержка (для кампаний дата). Ниже: метка карточки, тема, прехедер, отправитель, логика флоу.

Всё запускается во вторник, 27 октября, тремя группами:

| Группа | Когда | Письма |
|---|---|---|
| `flow-` · Flows | автоматически с Tue Oct 27 | P0 попап · Welcome 01 (W1 to W5) · Cart 06 (C1, C2) · Checkout 07 (CO1 to CO3, консьерж CC1, CC2 от $5,500) · Browse 05 (B1, B2) · After purchase 10 (PP1 to PP3) · Anniversary 15 (AN1) |
| `salt-` · SALT consent | с Tue Oct 27 | T1 ежедневными волнами по 200 to 300 · T2 и T3 автоматически через 7 и 14 дней |
| `camp-` · Campaigns | по датам | K2 Sally’s Edit Tue Oct 27 11:00 · K3 Tue Nov 3 · K1 Tue Nov 10 · DYO Tue Nov 17 · S1 Wed Nov 25 18:00 · S2 Fri Nov 27 08:00 · S3 Mon Nov 30 · K4 Thu Dec 3 · K2 Tue Dec 8 · LC Tue Dec 15 · HN Thu Dec 24 (+ запасной макет K2 без даты) |

## Как посмотреть
https://raw.githack.com/hostina05-dot/7thandhill-emails/main/preview.html (после слияния в `main`).
Переключатели вверху: Desktop / Mobile, With name / No name, масштаб.

## Как вставить в Klaviyo
1. Откройте файл в `klaviyo/` на GitHub, нажмите **Copy raw file**.
2. Klaviyo → **Content → Templates → Create template → HTML**, замените стартовый код, **Save**.
3. Во флоу или кампании: письмо → **Change template → Saved templates**.
4. Тему, прехедер и отправителя возьмите из комментария в начале файла.

Картинки в `klaviyo/` грузятся из ветки `main` этого репозитория через jsDelivr.

## Настройки в Klaviyo
- **Купон VAULT15**: уникальные коды, одно использование, 30 дней, не суммируется со скидками (в том числе с Black Friday 20%). В письмах стоит тег `{% coupon_code 'VAULT15' %}`, код вручную нигде не прописан.
- **Адрес** в подвале: Settings → Organization (190 Roslin Avenue, Toronto, Ontario M4N 1Z6).
- **SALT · said yes**: флоу по Clicked Email на кнопку Yes в T1 или T2 → `consent_source = SALT T1/T2`, `vault_member = true` → W1 с купоном сразу, W2 to W5 по дням флоу 01. Кто нажал Yes, выходит из SALT-флоу. Включите фильтр бот-кликов. Аудитория кампаний: Vault + `consent_source` начинается с SALT.
- **Динамические блоки**: корзина (C1) берёт `event.Items`, браузинг (B1) берёт `event.ProductName/ImageURL/URL`, checkout (CO1 to CO3, CC1, CC2) ведёт на `event.extra.checkout_url`. Проверьте в Preview & test на реальном профиле.

## Как менять
Тексты и состав писем меняются в `scripts/compose.py`, затем:

```
python3 scripts/compose.py && python3 scripts/build.py
```

Новое фото или видео: положите оригинал в `assets/photos/`, впишите в `SHOTS`, `CLIPS` или `SLIDES` в `scripts/photos.py`, запустите `python3 scripts/photos.py`. Изделие в сетке = номер из `blocks/catalog.md`.

## Правила текста (из брифа)
Без тире, без «Shop now», без «we love» и «stack»; мягкие кнопки (Step inside, Start a gift, Return to your bag). «Solid gold» вместо 14k. Ни слова о бесплатном ресайзе, вместо этого: «Not sure about size? Send me a photo of what you already wear, and I'll help you choose.» Праздники нейтрально: holiday, без ёлок. Слова Sally остаются как она написала.

## Waiting for Sally
1. Бесплатный ресайз колец: есть или нет.
2. Какие изделия только для подписчиков Vault.
3. Даты заказа к праздникам для K3 (предложены Nov 6, Nov 30, Dec 17).
4. Девять изделий для W3 (до Oct 29).
5. Шесть плиток коллекций в W1.
6. 14k или «Solid gold».
7. Бесплатная чистка в GTA как привилегия Vault.
