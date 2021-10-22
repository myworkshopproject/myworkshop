"""
Django base settings.
"""

import os
import sys
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from .allauth import *  # noqa F401 F403
from .auth import *  # noqa F401 F403
from .logging import *  # noqa F401 F403

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
APPS_DIR = BASE_DIR / "apps"
sys.path.append(str(APPS_DIR))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ["DJANGO_SECRET_KEY"])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ["DEBUG"]) == "True"
MESSAGE_LEVEL = 10  # DEBUG

# Allowed hosts
ALLOWED_HOSTS = str(os.environ["ALLOWED_HOSTS"]).split(" ")

# Application definition
INSTALLED_APPS = [
    # before "accounts" to override SiteAdmin  # `allauth` needs this from django:
    "django.contrib.sites",
    # before "django.contrib.auth" to override templates,
    "accounts.apps.AccountsConfig",
    "modeltranslation",  # before "django.contrib.admin" to use the admin integration
    "django.contrib.admin",
    "django.contrib.auth",  # `allauth` needs this from django
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",  # `allauth` needs this from django
    "django.contrib.staticfiles",
    "allauth",  # <- django-allauth
    "allauth.account",  # <- django-allauth
    "allauth.socialaccount",  # <- django-allauth
    "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.openid",
    "core.apps.CoreConfig",
    "simple_history",
    "widget_tweaks",
    "django_celery_results",
    "rest_framework",
    "django_filters",
    "webpack_loader",
]

# Middewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # after "SessionMiddleware" and "CacheMiddleware" ; before "CommonMiddleware":
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

# Root urls
ROOT_URLCONF = "myapp.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                # `allauth` needs this from django:
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "myapp.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.environ["POSTGRES_DB"]),
        "USER": str(os.environ["POSTGRES_USER"]),
        "PASSWORD": str(os.environ["POSTGRES_PASSWORD"]),
        "HOST": str(os.environ["POSTGRES_HOST"]),
        "PORT": str(os.environ["POSTGRES_PORT"]),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa E501
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

# Internationalization
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = "en"
LANGUAGES = (
    ("fr", _("French")),
    ("en", _("English")),
)
MODELTRANSLATION_FALLBACK_LANGUAGES = ("fr",)

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = str(os.environ["MEDIA_ROOT"])

# django-webpack-loader
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "dist/",  # must end with slash
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        # "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email
EMAIL_HOST_USER = str(os.environ["EMAIL_HOST_USER"])
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = str(os.environ["EMAIL_HOST"])
    EMAIL_PORT = str(os.environ["EMAIL_PORT"])
    EMAIL_HOST_PASSWORD = str(os.environ["EMAIL_HOST_PASSWORD"])
    EMAIL_USE_TLS = str(os.environ["EMAIL_USE_TLS"]) == "True"
    EMAIL_USE_SSL = str(os.environ["EMAIL_USE_SSL"]) == "True"

# django-simple-history
# SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = False
SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True  # Default: False
SIMPLE_HISTORY_FILEFIELD_TO_CHARFIELD = True  # Default: False
# SIMPLE_HISTORY_REVERT_DISABLED = False

# Celery Configuration Options
CELERY_BROKER_URL = "amqp://{user}:{password}@{host}:{port}/{vhost}".format(
    host=str(os.environ["RABBITMQ_HOST"]),
    port=str(os.environ["RABBITMQ_PORT"]),
    user=str(os.environ["RABBITMQ_DEFAULT_USER"]),
    password=str(os.environ["RABBITMQ_DEFAULT_PASS"]),
    vhost=str(os.environ["RABBITMQ_DEFAULT_VHOST"]),
)
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# Configure Celery to use the django-celery-results backend:
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
    "SEARCH_PARAM": "search",  # Default: "search"
    "ORDERING_PARAM": "ordering",  # Default: "ordering"
}

# Core App
CORE_DEFAULT_SITE_NAME = str(os.environ["SITE_NAME"])
