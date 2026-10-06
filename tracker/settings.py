"""Настройки Django-проекта tracker.

Документация: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Каталог с JSON-файлами предметной области (ПР1–ПР3).
DATA_DIR = BASE_DIR / "data"

# Ключ только для учебной разработки, в продакшене его нужно заменить.
SECRET_KEY = (
    "django-insecure-"
    "+gku)q38mc-h9*9)9=_-t%^mzk60sj5u4&_t=-7nk$q1&ot@*("
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "accounts",
    "catalog",
    "progress",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tracker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tracker.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


_VALIDATORS = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_VALIDATORS}.UserAttributeSimilarityValidator"},
    {"NAME": f"{_VALIDATORS}.MinimumLengthValidator"},
    {"NAME": f"{_VALIDATORS}.CommonPasswordValidator"},
    {"NAME": f"{_VALIDATORS}.NumericPasswordValidator"},
]


LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Сессия хранится в подписанной cookie: вход по имени работает без БД.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
