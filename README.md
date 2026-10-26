# 7th & Hill · launch letters for Klaviyo

Отправитель: **Sally at 7th & Hill** &lt;hello@7thandhilljewelry.ca&gt;, ответы на hello@7thandhilljewelry.ca · сайт: https://www.7thandhilljewelry.ca

Дизайн: белая страница в тёмно-зелёной рамке, чёрная полоса 7 T H & H I L L, фото во всю ширину с круглой печатью на нижнем краю, изделия на светлом «лунном» фоне, тёмные блоки с золотым санберстом. Шрифты: Italiana (заголовки) и Jost (текст), в Gmail/Outlook запасные Georgia и Arial.

## Где что лежит

```
templates/        34 письма по этапам запуска (исходники, их пишет scripts/compose.py)
klaviyo/          те же письма, готовые к вставке в Klaviyo (картинки с хостинга)
preview.html      все письма, сгруппированные по этапам, с метками, статусами и списком «Waiting for Sally»
blocks/           готовые блоки для вставки + catalog.md (все изделия с номерами и ссылками)
assets/photos/    оригиналы фото и видео
assets/images/    готовые картинки для писем (после цветокоррекции)
assets/catalog.json  изделия: название, картинка, ссылка
scripts/compose.py   тексты Sally и сборка всех писем из общих блоков
scripts/photos.py    цветокоррекция, кадрирование, печать на фото, GIF из видео
scripts/build.py     preview.html и klaviyo/
```

Имя файла = этап и код письма: `s1-w1-welcome.html`, `s2-k3-holiday-deadline.html` и т. д. Первая строка комментария в каждом файле: этап, дата запуска, флоу, код, место в серии, когда уходит. Ниже: метка карточки, статус, тема, прехедер, отправитель, логика флоу.

| Этап | Запуск | Письма |
|---|---|---|
| 1 | Tue Oct 27 | P0 попап Vault (макет и спецификация, сам попап собирается в Klaviyo Forms) · W1 to W5 welcome · T1 to T3 SALT |
| 2 | Mon Nov 2 (K3 Tue Nov 3, 10:00) | K3 holiday deadline · C1, C2 cart · CO1 to CO3 checkout · CC1, CC2 concierge ($5,500+) |
| 3 | Mon Nov 9 | B1, B2 browse · PP1 to PP3 after purchase · AN1 anniversary · K1 weekly skeleton |
| 4 | by Tue Nov 24 | S1 to S3 sale · DYO · K4 gift guide · K2 Sally's edit (3 layouts) · LC last call · HN holiday note |

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
