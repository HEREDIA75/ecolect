import os
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. DIRETÓRIOS BASE E AMBIENTE
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# -----------------------------------------------------------------------------
# 2. SEGURANÇA E HOSTS
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-fallback-key-change-in-production"
)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Garante suporte a domínios da Railway e ambiente local
DEFAULT_HOSTS = "localhost,127.0.0.1,.up.railway.app"
ENV_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_HOSTS)
ALLOWED_HOSTS = [host.strip() for host in ENV_HOSTS.split(",") if host.strip()]

# Requisitado pelo Django 4+ ao usar HTTPS na Railway
CSRF_TRUSTED_ORIGINS = [
    f"https://{host}" if not host.startswith("https://") else host
    for host in ALLOWED_HOSTS
    if host not in ("localhost", "127.0.0.1")
]

# -----------------------------------------------------------------------------
# 3. APLICAÇÕES E MIDDLEWARES
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceiros
    "django_htmx",
    # Apps do Projeto
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve os estáticos na Railway
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "setup.urls"

# -----------------------------------------------------------------------------
# 4. TEMPLATES E WSGI
# -----------------------------------------------------------------------------
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

WSGI_APPLICATION = "setup.wsgi.application"

# -----------------------------------------------------------------------------
# 5. BANCO DE DADOS (MYSQL / SQLITE FALLBACK)
# -----------------------------------------------------------------------------
DB_ENGINE = os.getenv("DB_ENGINE", "django.db.backends.mysql")

if os.getenv("DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }
else:
    # Fallback para SQLite local caso as variáveis do MySQL não estejam definidas
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------------------------------------------------------------
# 6. VALIDAÇÃO DE SENHAS
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# 7. INTERNACIONALIZAÇÃO
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# 8. ARQUIVOS ESTÁTICOS E MÍDIA
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

# Compressão e cache dos estáticos no ambiente de produção com WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------------------------------------------------------
# 9. DIVERSOS
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
