from django.utils.translation import gettext_lazy as _

from pathlib import Path
from decouple import config

import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "import_export",
    # local apps
    "app_user",
    "app_education",
    "app_application",
    "app_occupation",
    "app_frequently_question",
    "app_notification",
    "app_chat",
    "app_admin",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # multi language
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # cors-headers
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # custom middlewares
    "utils.middleware.TransactionMiddleware",
    # "utils.middleware.LanguageMiddleware",
]

ROOT_URLCONF = "Abrat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Abrat.wsgi.application"

# Database
SQL_LITE_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if config("USE_MYSQL", default=False, cast=bool):
    MYSQL_DATABASE = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_NAME"),
        "USER": config("MYSQL_USER"),
        "PASSWORD": config("MYSQL_PASS"),
        "HOST": config("MYSQL_HOST"),
        "PORT": config("MYSQL_PORT", cast=int),
    }

if config("USE_POSTGRES", default=False, cast=bool):
    POSTGRE_SQL_DATABASE = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_NAME"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASS"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", cast=int),
    }

DEFAULT_DATABASE = config("DEFAULT_DATABASE_NAME", default="")

DATABASES = {
    "default": SQL_LITE_DATABASE
    if DEBUG
    else MYSQL_DATABASE
    if DEFAULT_DATABASE.upper() == "MYSQL"
    else POSTGRE_SQL_DATABASE
    if DEFAULT_DATABASE.upper() == "POSTGRESQL"
    else SQL_LITE_DATABASE
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ___django settings___ #
AUTH_USER_MODEL = "app_user.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# Media files (Images, Files)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Internationalization
LANGUAGES = [
    ("en", _("English")),
    ("fa", _("Persian")),
    ("ar", _("Arabic")),
]
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
# File
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

# ___django rest framework settings___ #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ___Redis settings___ #
Redis_host = config("REDIS_HOST", default="localhost")
Redis_port = config("REDIS_PORT", default=6379, cast=int)
Redis_db = config("REDIS_DB", default=0, cast=int)

# ___Request Api Options___ #
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = config(
    "CORS_ORIGIN_REGEX_WHITELIST", cast=lambda v: [s.strip() for s in v.split(",")]
)

# __django multi language settings__ #
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

# __Email Settings__ #
DEPENDENT_EMAIL_ON_DEBUG = config("DEPENDENT_EMAIL_ON_DEBUG", cast=bool, default=True)
if DEBUG is True and DEPENDENT_EMAIL_ON_DEBUG is True:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST_USER = ""
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# __Custom Settings__ #
DATE_INPUT_FORMATS = "%Y-%m-%d"
TIME_INPUT_FORMATS = "%H:%M:%S"
MAX_DOCUMENTS_SIZE = 3 * 1024 * 1024
