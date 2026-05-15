# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 4.2 веб-приложение — рейтинг HR-агентств Москвы 2026. Проект называется `hrrating`, Django-приложение — `agencies`. База данных — SQLite (`db.sqlite3`). Статичный прототип сохранён отдельно в [hr-rating-moscow.html](hr-rating-moscow.html).

## Structure

```
hrrating/          — Django project (settings, root urls, wsgi/asgi)
agencies/          — основное приложение
  models.py        — модели Category, Agency, Review
  views.py         — единственная view: index()
  admin.py         — AdminSite: CategoryAdmin, AgencyAdmin (+ ReviewInline), ReviewAdmin
  urls.py          — одна маршрут: "" → index
  migrations/      — 0001_initial.py
  fixtures/        — initial_data.json
templates/
  agencies/
    index.html     — главная страница (все CSS + HTML + JS inline)
    _crit_bar.html — partial для одной строки критерия
manage.py
db.sqlite3
hr-rating-moscow.html  — статичный HTML-прототип (не используется приложением)
```

## Models

**`Category`** — справочник специализаций
- `name` CharField(100)
- `slug` SlugField(unique) — используется в URL-параметре `spec` и CSS-классах `.tag-{slug}`

**`Agency`** — агентство
- `name`, `description`, `city` (default «Москва»), `address`, `phone`, `website` (URLField), `founded_year`
- `is_verified` BooleanField
- `categories` ManyToMany → Category
- `specializations` TextField — список через запятую, парсится методом `get_specializations_list()`
- `criteria_quality`, `criteria_speed`, `criteria_price`, `criteria_support` FloatField 0–5
- `speed_score` FloatField 0–10
- `created_at` auto_now_add
- **Properties**: `avg_rating` (Avg отзывов, округлённый), `review_count`
- **Ordering**: `-created_at`

**`Review`** — отзыв
- `agency` FK → Agency (related_name `reviews`)
- `rating` PositiveSmallIntegerField 1–5 (validators Min/Max)
- `text`, `author`, `created_at`

## Views

**`agencies/views.py` → `index(request)`**

GET-параметры: `spec` (slug категории или `all`), `q` (поиск), `sort` (`rating`/`reviews`/`speed`/`name`).

Логика:
1. QuerySet с `prefetch_related("categories","reviews")` и `annotate(annotated_rating=Avg, annotated_reviews=Count)`.
2. Фильтр по `categories__slug` если `spec != all`.
3. Поиск по `name__icontains` или `specializations__icontains` (union двух QS — есть баг дублирования при одновременном поиске + фильтре по категории).
4. Сортировка через `sort_map`.
5. Список `agency_list` — dicts с ключами `obj`, `rank`, `rating`, `review_count`, `specializations`.

Контекст шаблона: `agency_list`, `categories`, `current_spec`, `search`, `sort`, `count_label`.

## Templates

**`templates/agencies/index.html`** — самодостаточный файл со всем CSS (inline `<style>`), HTML и JS (`<script>`). Внешняя зависимость только Google Fonts Inter.

Фильтры — `<a>`-ссылки с GET-параметрами (не кнопки), поиск и сортировка сабмитят форму через JS `submitForm()`.

SVG-звёзды рендерятся на клиенте через `renderStars()` по значению из `.rating-num`.

**`templates/agencies/_crit_bar.html`** — partial критерия. Принимает `label` и `value` (0–5). Цветовая логика: ≥4.5 → `#10b981`, ≥4.0 → `#2563eb`, ≥3.5 → `#f59e0b`, <3.5 → `#ef4444`. Использует `{% widthratio %}` для процентов.

## Admin

URL: `/admin/` (стандартный Django admin).

- **CategoryAdmin**: list + search по name, prepopulated slug.
- **AgencyAdmin**: list с вычисляемым рейтингом и кол-вом отзывов, фильтры по is_verified/categories/city, `filter_horizontal` для категорий, `ReviewInline` (TabularInline).
- **ReviewAdmin**: фильтры по rating/agency, `raw_id_fields=["agency"]`.

Создать суперпользователя: `python manage.py createsuperuser`

## URL Routes

| URL | View | Name |
|-----|------|------|
| `/` | `agencies.views.index` | `index` |
| `/admin/` | Django admin | — |

## Development

```bash
# Запуск сервера
python manage.py runserver

# Применить миграции (уже применены)
python manage.py migrate

# Загрузить начальные данные
python manage.py loaddata agencies/fixtures/initial_data.json

# Создать суперпользователя для /admin/
python manage.py createsuperuser
```

Настройки: `hrrating/settings.py`. `DEBUG=True`, `SECRET_KEY` захардкожен — не деплоить в продакшн без замены. `TEMPLATES['DIRS']` включает корневой `templates/`.

## CSS Custom Properties (в index.html)

```
--primary: #4f46e5    --primary-dark: #3730a3    --primary-light: #818cf8
--accent:  #f59e0b    --success: #10b981          --danger: #ef4444
--bg:      #f0f2f8    --card: #ffffff             --border: #e2e8f0
--text:    #0f172a    --muted: #64748b
--shadow / --shadow-hover / --radius: 18px
```

## Responsive Breakpoints

- `≤ 900px` — SEO-сетка 2 колонки
- `≤ 768px` — карточка 2 колонки, `.agency-right` горизонтально, `expanded-grid` 2 колонки
- `≤ 560px` — карточка 1 колонка, `expanded-grid` 1 колонка, скрыт адрес в мета, SEO/FAQ 1 колонка
- `≤ 400px` — `.filter-tabs` горизонтальный скролл

## How to extend

**Добавить агентство**: через `/admin/` → Агентства → Добавить. Рейтинг считается автоматически из отзывов.

**Добавить категорию**: через `/admin/` → Категории → Добавить (slug станет частью CSS-класса `.tag-{slug}` и GET-параметра). Добавить CSS-стиль `.tag-{slug}` в `index.html`.

**Добавить поле к Agency**: создать поле в `models.py` → `python manage.py makemigrations` → `python manage.py migrate` → обновить `admin.py` fieldsets и шаблон.
