# Описание кода для разработчиков

## Модели

### Category (категория)
- `user` – `ForeignKey` на `User` (владелец категории).
- `name` – `CharField`, название категории.
- `description` – `TextField`, описание (необязательное).
- `created_at` – `DateTimeField`, дата создания.

**Методы:**
- `__str__()` – возвращает название категории.

### Entry (запись/карточка)
- `category` – `ForeignKey` на `Category` (связь с категорией, `related_name='entries'`).
- `term` – `CharField`, термин.
- `definition` – `TextField`, определение.
- `created_at` – `DateTimeField`, дата создания.
- `correct_count` – `IntegerField`, количество правильных ответов (по умолчанию 0).
- `wrong_count` – `IntegerField`, количество неправильных ответов (по умолчанию 0).

**Методы:**
- `__str__()` – возвращает термин.

## Представления (views)

### Аутентификация
- `register` – регистрация нового пользователя.
- `login_view` – вход.
- `logout_view` – выход.

### Категории
- `category_list` – список категорий текущего пользователя.
- `category_detail` – детальный просмотр категории со списком записей.
- `category_create` – создание новой категории.
- `category_update` – редактирование категории.
- `category_delete` – удаление категории.

### Записи
- `entry_create` – создание записи в указанной категории.
- `entry_update` – редактирование записи.
- `entry_delete` – удаление записи.

### Режимы изучения и тестирования
- `study` – режим изучения (переворот карточек, GET-параметры index и show).
- `test_mode` – режим тестирования (ввод ответа, POST-запрос, обновление статистики).

## Маршруты (urls)
Все маршруты находятся в файле `flashcards/urls.py`. Основные:
- `/` – список категорий (`category_list`)
- `/category/new/` – создание категории
- `/category/<int:pk>/` – детальная страница категории
- `/category/<int:pk>/edit/` – редактирование категории
- `/category/<int:pk>/delete/` – удаление категории
- `/category/<int:category_id>/entry/new/` – создание записи
- `/entry/<int:pk>/edit/` – редактирование записи
- `/entry/<int:pk>/delete/` – удаление записи
- `/category/<int:category_id>/study/` – режим изучения
- `/category/<int:category_id>/test/` – режим тестирования
- `/register/` – регистрация
- `/login/` – вход
- `/logout/` – выход

## Шаблоны
Все шаблоны находятся в `flashcards/templates/flashcards/`. Базовый шаблон – `base.html`. Остальные наследуются от него.

## Настройки аутентификации
В `flashcard_project/settings.py` добавлены:
- `LOGIN_URL = 'login'`
- `LOGIN_REDIRECT_URL = 'category_list'`