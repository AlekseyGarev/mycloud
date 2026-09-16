import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() in {"1", "true", "yes", "on"}
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "users.apps.UsersConfig",
    "storage.apps.StorageConfig",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

FRONTEND_DIST = BASE_DIR / "frontend_dist"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIST],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

if os.getenv("DB_ENGINE", "postgresql").lower() == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "mycloud_db"),
            "USER": os.getenv("DB_USER", "mycloud_user"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [FRONTEND_DIST] if FRONTEND_DIST.exists() else []
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))

# Ограничения загрузки защищают сервер от случайного/намеренного заполнения диска.
MAX_UPLOAD_FILE_SIZE = int(os.getenv("MAX_UPLOAD_FILE_SIZE", str(100 * 1024 * 1024)))
MAX_FILES_PER_UPLOAD = int(os.getenv("MAX_FILES_PER_UPLOAD", "20"))

# CORS нужен только при локальной разработке, когда Vite работает отдельным процессом.
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # React читает csrftoken и отправляет X-CSRFToken.
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", str(not DEBUG)).lower() in {
    "1",
    "true",
    "yes",
    "on",
}

CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", str(not DEBUG)).lower() in {
    "1",
    "true",
    "yes",
    "on",
}
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_THROTTLE_RATES": {
        "login": os.getenv("LOGIN_THROTTLE_RATE", "10/min"),
        "register": os.getenv("REGISTER_THROTTLE_RATE", "10/hour"),
        "public_download": os.getenv("PUBLIC_DOWNLOAD_THROTTLE_RATE", "120/hour"),
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] [{name}:{lineno}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "users": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
        "storage": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
}
