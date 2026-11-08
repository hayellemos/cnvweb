from pathlib import Path
import os
from urllib.parse import urlparse, unquote

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-cnv-web-dev-only")
DEBUG = os.getenv("DEBUG", "True").lower() in ("1", "true", "yes", "on")
ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "usuarios",
    "feedbacks",
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

ROOT_URLCONF = "cnvweb.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "front"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "cnvweb.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada. Crie o .env na mesma pasta do manage.py.")
parsed = urlparse(DATABASE_URL)
if parsed.scheme not in ("postgres", "postgresql"):
    raise RuntimeError("DATABASE_URL deve começar com postgres:// ou postgresql://")

DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": unquote(parsed.path.lstrip("/")) or "postgres",
    "USER": unquote(parsed.username or ""),
    "PASSWORD": unquote(parsed.password or ""),
    "HOST": parsed.hostname or "",
    "PORT": str(parsed.port or 5432),
    "OPTIONS": {"sslmode": "require"},
}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Bahia"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "front"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CORS_ALLOWED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
