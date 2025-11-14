"""
Django settings for mi_sitio_venta project.
"""

from pathlib import Path
import os  

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Seguridad
SECRET_KEY = 'django-insecure-t5(_&i4s-$%)*zks4qx$wei_3wyk$a-n^d^jxww5y1u)4olbi*'
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'crochetcoco.azurewebsites.net',
    'uni-coco-mante.azurewebsites.net',
    'localhost',
    '127.0.0.1',
    '.azurewebsites.net',
]

# -------------------------------------------------------------
# DETECCIÓN DE ENTORNO
# -------------------------------------------------------------
def get_environment():
    if os.getenv('WEBSITE_SITE_NAME'):
        return 'azure'
    return 'local'

environment = get_environment()

# -------------------------------------------------------------
# BASE DE DATOS
# -------------------------------------------------------------
if environment == 'azure':
    print("🚀 Ejecutando en Azure - Usando Azure MySQL")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'proyecto_crochet',
            'USER': 'coco_adminmante',
            'PASSWORD': 'dTlF6s@z',
            'HOST': 'uni-coco-mante.mysql.database.azure.com',
            'PORT': '3306',
            'OPTIONS': {
                'ssl': {'ssl-mode': 'require'},
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }

else:
    print("💻 Ejecutando en local - MySQL Local")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '34.63.75.254',
            'NAME': 'bd_cococrochet',
            'USER': 'coco_app',
            'PASSWORD': 'CocoApp2025!Segura',
            'PORT': '3306',
        }
    }

# -------------------------------------------------------------
# APLICACIONES
# -------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
]

# -------------------------------------------------------------
# MIDDLEWARE (WhiteNoise activado)
# -------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise (archivos estáticos en Azure)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_sitio_venta.urls'

# -------------------------------------------------------------
# TEMPLATES (tu carpeta /templates funcionando)
# -------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # <<<<<<<< AQUÍ
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

WSGI_APPLICATION = 'mi_sitio_venta.wsgi.application'

# -------------------------------------------------------------
# VALIDADORES
# -------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -------------------------------------------------------------
# INTERNACIONALIZACIÓN
# -------------------------------------------------------------
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------
# ARCHIVOS ESTÁTICOS
# -------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   # Para Azure

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------------------------------------
# MEDIA
# -------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------------------------------------------
# CSRF
# -------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://crochetcoco.azurewebsites.net',
    'https://uni-coco-mante.azurewebsites.net',
    'https://*.azurewebsites.net',
]

# -------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------
# EMAIL
# -------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = "webmaster@localhost"
