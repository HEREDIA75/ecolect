import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. DIRETÓRIOS BASE E AMBIENTE
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# -----------------------------------------------------------------------------
# 2. SEGURANÇA E HOSTS (CORRIGIDO PARA RAILWAY)
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-fallback-key-change-in-production"
)

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Garante a aceitação do domínio exato da Railway, wildcard e localhost
DEFAULT_HOSTS = (
    "ecolect-production.up.railway.app, .up.railway.app, localhost, 127.0.0.1, *"
)
ENV_HOSTS = os.getenv("ALLOWED_HOSTS", DEFAULT_HOSTS)

# Trata a lista para o ALLOWED_HOSTS
ALLOWED_HOSTS = [host.strip() for host in ENV_HOSTS.split(",") if host.strip()]

# Gera a lista CSRF_TRUSTED_ORIGINS ignorando '*' e prefixando 'https://'
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    if host in ("*", "localhost", "127.0.0.1"):
        continue
    # Se o host começa com ponto (.up.railway.app), adiciona com wildcard (*.up.railway.app)
    clean_host = host.lstrip(".")
    if host.startswith("."):
        CSRF_TRUSTED_ORIGINS.append(f"https://*.{clean_host}")
    else:
        CSRF_TRUSTED_ORIGINS.append(f"https://{clean_host}")

# Adiciona o domínio explícito caso não tenha sido incluído
if "https://ecolect-production.up.railway.app" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("https://ecolect-production.up.railway.app")

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
    "django_htmx",
    # Apps do Projeto
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve estáticos no ambiente de produção
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
# 5. BANCO DE DADOS (DATABASE_URL / MYSQL / SQLITE FALLBACK)
# -----------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Produção (Railway com MySQL provisionado)
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
elif os.getenv("DB_NAME"):
    # Desenvolvimento Local (MySQL via .env)
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.mysql"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
        }
    }
else:
    # Fallback SQLite
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
# 8. ARQUIVOS ESTÁTITCOS E MÍDIA
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

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
