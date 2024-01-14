"""
Django settings for wishlists project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from typing import Optional

from django.core.exceptions import ImproperlyConfigured


def get_env_bool(name: str, default=False) -> bool:
    """
    Get a boolean value from an environment variable.
    """
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.lower() in ["t", "true", "y", "yes", "1"]


def get_env_int(name: str, default=None) -> Optional[int]:
    """
    Get an integer value from an environment variable.
    """
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError:
        raise ImproperlyConfigured(
            f"Expected environment variable '{name}' to be an integer, not "
            f"'{raw_value}'."
        )


def get_env_list(name: str, separator: str = ",") -> list[str]:
    """
    Get a list of string values from an environment variable.
    """
    raw_value = os.getenv(name, "")
    # An empty string would split to a one-element list containing an empty
    # string, but we want an empty list instead.
    if not raw_value:
        return []

    return raw_value.split(separator)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Development Specific Settings

DEV_LIVE_RELOAD = get_env_bool("DEV_LIVE_RELOAD")
DEV_TOOLS = get_env_bool("DEV_TOOLS")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

DEBUG = get_env_bool("DEBUG")

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: keep the secret key used in production secret!
if not SECRET_KEY and DEBUG:
    SECRET_KEY = "django-insecure-w+n*on^3a$k-7+!fnq(k-qkon(#q&8e311o7(5)*_@)8^0_k*h"


ALLOWED_HOSTS = get_env_list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = get_env_list("CSRF_TRUSTED_ORIGINS")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
    # Third party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "tailwind",
    # Custom apps
    "core",
    "theme",
]

if DEV_LIVE_RELOAD:
    INSTALLED_APPS.append("django_browser_reload")

if DEV_TOOLS:
    import socket

    INSTALLED_APPS.append("debug_toolbar")

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

MIDDLEWARE = []
if DEV_TOOLS:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

MIDDLEWARE.extend(
    [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "allauth.account.middleware.AccountMiddleware",
    ]
)

if DEV_LIVE_RELOAD:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = "wishlists.urls"

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

WSGI_APPLICATION = "wishlists.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Allow for using weak passwords in a dev environment.
if not get_env_bool("DISABLE_PASSWORD_RESTRICTIONS"):
    AUTH_PASSWORD_VALIDATORS.append(
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
    )

AUTH_USER_MODEL = "core.User"

AUTHENTICATION_BACKENDS = [
    # Needed for Django admin.
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "idea-collection-list"
LOGIN_URL = "account_login"


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = "/var/www/static"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "listgiftr@localhost")
EMAIL_HOST = os.getenv("EMAIL_HOST")

if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = get_env_int("EMAIL_PORT", 587)
    EMAIL_USE_TLS = get_env_bool("EMAIL_USE_TLS", True)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Forms

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Logging
# https://docs.djangoproject.com/en/4.1/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}


# Allauth

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False


# Tailwind Theming

TAILWIND_APP_NAME = "theme"
