# Design

## Context

Баннер рендерится в шапке сайта через `layouts/partials/header.html` (блок `.banner-section` с `.banner`, `.banner-image`, `.banner-overlay`, `.banner-role`). Этот partial подключается из `layouts/_default/baseof.html` и因此 отображается на каждой странице. Ссылка на баннер также используется для `og:image` и `twitter:image` в `layouts/partials/head.html`. Стили баннера описаны в `assets/main.css` (классы `.banner-section`, `.banner`, `.banner-image`, `.banner-overlay`, `.banner-role`). Файл изображения `static/images/banner.jpg` остаётся на месте — он просто перестанет использоваться.

## Goals / Non-Goals

**Goals:**
- Баннер не рендерится ни на одной странице сайта (главная, разделы, отдельные материалы).
- Файл изображения `static/images/banner.jpg` удаляется из репозитория.
- Удалены неиспользуемые CSS-классы баннера из `assets/main.css`.
- Ссылки `og:image`/`twitter-image` на баннер убраны из `head.html` (или заменены на подходящую заглушку).
- Сайт собирается через `hugo` без ошибок.

**Non-Goals:**
- Изменение логотипа/фото терапевта (`/images/photo.png`).
- Переделка навигации или шапки сайта за пределами удаления баннера.

## Decisions

1. **Удалить блок `.banner-section` из `layouts/partials/header.html`** (строки 1–12). Альтернаativa — закомментировать, но полное удаление чище, так как баннер больше не нужен ни на одной странице.
2. **Убрать `og:image`/`twitter-image` на баннер из `layouts/partials/head.html`** — заменить на отсутствие мета-тегов изображения (или оставить без картинки), так как баннер больше не является 대표тельным изображением сайта.
3. **Удалить стили баннера из `assets/main.css`** — классы `.banner-section`, `.banner`, `.banner-image`, `.banner-overlay`, `.banner-role` и связанные с ними правила, так как после удаления HTML они не используются.
4. **Удалить `static/images/banner.jpg` из репозитория** — файл больше не нужен ни в шаблонах, ни в CSS, ни в мета-тегах.

## Risks / Trade-offs

- [Risk] Отсутствие `og:image`/`twitter:image` может ослабить превью при шаринге ссылок в соцсетях → Mitigation: добавить отдельное `og:image` с фото терапевта (`/images/photo.png`) при необходимости позже.
- [Risk] Удаление CSS может оставить неиспользуемые правила, если где-то ещё ссылаются на классы баннера → Mitigation: после удаления проверить сборку и отсутствие ссылок на классы баннера в коде.

## Migration Plan

1. Удалить блок `.banner-section` из `layouts/partials/header.html`.
2. Убрать ссылки на баннер из `layouts/partials/head.html`.
3. Удалить стили баннера из `assets/main.css`.
4. Удалить файл `static/images/banner.jpg` из репозитория.
5. Запустить `hugo` и проверить отсутствие ошибок сборки и отсутствия баннера на страницах.
5. Закоммитить и запушить — GitHub Actions пересоберёт сайт на GitHub Pages.

## Open Questions

—