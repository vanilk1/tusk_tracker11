"""
Django settings for task_tracker project.

Проект "Трекінг завдань" — система управління завданнями.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# БАЗОВЫЕ НАСТРОЙКИ / БЕЗОПАСНОСТЬ
# --------------------------------------------------------------------------

# В продакшене ОБЯЗАТЕЛЬНО задайте свой SECRET_KEY через переменную окружения!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-CHANGE-ME-IN-PRODUCTION-xxxxxxxxxxxxxxxxxxxxxxxx'
)

# DEBUG=True только для разработки. В продакшене — False.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# --------------------------------------------------------------------------
# ПРИЛОЖЕНИЯ
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Наше приложение трекинга задач
    'tasks.apps.TasksConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_tracker.wsgi.application'
ASGI_APPLICATION = 'task_tracker.asgi.application'


# --------------------------------------------------------------------------
# БАЗА ДАННЫХ
# По умолчанию — SQLite (разработка).
# Для продакшена задайте переменную окружения DJANGO_USE_POSTGRES=True
# и параметры подключения (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD,
# POSTGRES_HOST, POSTGRES_PORT).
# --------------------------------------------------------------------------

if os.environ.get('DJANGO_USE_POSTGRES', 'False') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'task_tracker'),
            'USER': os.environ.get('POSTGRES_USER', 'task_tracker_user'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# --------------------------------------------------------------------------
# ВАЛИДАЦИЯ ПАРОЛЕЙ
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------------------------------
# ЛОКАЛИЗАЦИЯ
# --------------------------------------------------------------------------

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------
# СТАТИКА
# --------------------------------------------------------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'tasks' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------------------------------
# АУТЕНТИФИКАЦИЯ
# --------------------------------------------------------------------------

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'task_list'
LOGOUT_REDIRECT_URL = 'login'
