# Spec Delta

## Purpose

Определяет правила отображения элементов заголовка сайта, включая баннер, чтобы посетители сайта гештальт-терапевта фокусировались на текстовом контенте без отвлекающего графического баннера.

## ADDED Requirements

### Requirement: Banner not rendered on any page

Система НЕ ДОЛЖНА рендерировать баннер (`banner.jpg`) ни на одной странице сайта, включая главную, страницы разделов и отдельные материалы.

#### Scenario: Banner absent on homepage

- **WHEN** пользователь открывает главную страницу сайта
- **THEN** на странице отсутствует элемент баннера и связанные с ним CSS-классы (`.banner-section`, `.banner`, `.banner-image`, `.banner-overlay`, `.banner-role`)

#### Scenario: Banner absent on section page

- **WHEN** пользователь открывает страницу любого раздела (например, статьи, случаи из практики, читательский дневник)
- **THEN** на странице отсутствует элемент баннера

#### Scenario: Banner absent on single content page

- **WHEN** пользователь открывает отдельную страницу материала (статью, случай, вопрос, запись дневника)
- **THEN** на странице отсутствует элемент баннера

### Requirement: Banner image file removed from repository

Система НЕ ДОЛЖНА содержать файл изображения баннера `static/images/banner.jpg` в репозитории.

#### Scenario: Banner image file deleted

- **WHEN** разработчик проверяет содержимое директории `static/images/`
- **THEN** файла `banner.jpg` в этой директории нет