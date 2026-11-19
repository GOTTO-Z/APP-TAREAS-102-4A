"""
Django settings for tareas project.
"""

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SEGURIDAD
# =====================================================

SECRET_KEY = "django-insecure--bfc@h#-)w(0g(1p!7nvqikz_gp&t_(2s4u48c@0a_g2t79vmc"

DEBUG = True

ALLOWED_HOSTS = []


# =====================================================
# APLICACIONES
# =====================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    # Lista negra para revocar Refresh Tokens
    "rest_framework_simplejwt.token_blacklist",
    "tareasapp",
]


# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "tareas.urls"


# =====================================================
# PLANTILLAS
# =====================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


WSGI_APPLICATION = "tareas.wsgi.application"


# =====================================================
# BASE DE DATOS
# =====================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "tareasdb25",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
#User: Gotoh
#Password: root123

# =====================================================
# VALIDACION DE CONTRASEÑAS
# =====================================================

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


# =====================================================
# INTERNACIONALIZACION
# =====================================================

LANGUAGE_CODE = "es-cl"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# =====================================================
# ARCHIVOS ESTATICOS
# =====================================================

STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================================
# CONFIGURACION REST FRAMEWORK
# =====================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}


# =====================================================
# CONFIGURACION JWT
# =====================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    # Revocar el Refresh anterior al renovarlo
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# =====================================================
# SESIONES DJANGO
# =====================================================

# Sesiones almacenadas en la base de datos
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Duración de la sesión: 30 minutos
SESSION_COOKIE_AGE = 1800

# Cookie no accesible desde JavaScript
SESSION_COOKIE_HTTPONLY = True

# Protección contra solicitudes externas
SESSION_COOKIE_SAMESITE = "Lax"

# En desarrollo local utilizamos HTTP
SESSION_COOKIE_SECURE = False

# Renovación de la cookie desactivada por petición
SESSION_SAVE_EVERY_REQUEST = False


# =====================================================
# PROTECCION CSRF
# =====================================================

CSRF_COOKIE_HTTPONLY = True

CSRF_COOKIE_SAMESITE = "Lax"

# En producción con HTTPS debe configurarse como True
CSRF_COOKIE_SECURE = False
