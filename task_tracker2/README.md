# Трекінг завдань (Django)

Система управління завданнями: створення, редагування, видалення та коментування
завдань, з автентифікацією, дозволами та фільтрацією.

## Технології
- Python 3.x, Django (5.x)
- SQLite (розробка) / PostgreSQL (продакшн)
- HTML + Bootstrap 5

## Швидкий старт

```bash
# 1. Створити та активувати віртуальне середовище
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Встановити залежності
pip install -r requirements.txt

# 3. Застосувати міграції
python manage.py migrate

# 4. Створити суперкористувача (для доступу до /admin/)
python manage.py createsuperuser

# 5. Запустити сервер розробки
python manage.py runserver
```

Далі відкрийте http://127.0.0.1:8000/

## Структура проекту

```
task_tracker/
├── manage.py
├── task_tracker/        # налаштування проекту (settings, urls, wsgi)
└── tasks/                # основний застосунок
    ├── models.py         # Task, Comment
    ├── forms.py          # TaskForm, TaskFilterForm, CommentForm, RegisterForm
    ├── views.py          # Class-Based Views
    ├── permissions.py    # OwnerRequiredMixin — дозволи на edit/delete
    ├── urls.py
    ├── admin.py
    └── templates/
```

## Реалізований функціонал

- **Реєстрація / вхід / вихід** — `RegisterView`, вбудовані `django.contrib.auth.urls`.
- **CRUD завдань** — `TaskCreateView`, `TaskDetailView`, `TaskUpdateView`, `TaskDeleteView`.
- **Коментарі** — додавання прямо на сторінці завдання, видалення автором коментаря
  або власником завдання.
- **Фільтрація** — за статусом, пріоритетом, датою терміну та пошуком за назвою
  (`TaskFilterForm`, GET-параметри).
- **Дозволи** — `OwnerRequiredMixin` дозволяє редагувати/видаляти завдання лише
  власнику (або персоналу).

## Перемикання на PostgreSQL (продакшн)

Встановіть змінні оточення:

```bash
export DJANGO_USE_POSTGRES=True
export POSTGRES_DB=task_tracker
export POSTGRES_USER=task_tracker_user
export POSTGRES_PASSWORD=your_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="згенеруйте_свій_ключ"
```

## Можливі напрямки розвитку (масштабованість)

- Призначення завдань іншим користувачам (поле `assigned_to`).
- REST API (Django REST Framework) для мобільного клієнта.
- Сповіщення про наближення терміну виконання (Celery + email).
- Docker/docker-compose для ізоляції середовища.
