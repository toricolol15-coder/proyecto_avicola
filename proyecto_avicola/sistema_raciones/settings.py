"""
Django settings for sistema_raciones project.
"""

import pymysql
pymysql.install_as_MySQLdb()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_%#e3b(ycv7m!zg)8bua@xnz$26=b8wq-%toqb6p6s^su(i!3x'

DEBUG = True

ALLOWED_HOSTS = []


# ------------------------
#   APLICACIONES
# ------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # TU APP
    'panel',
]


# ------------------------
#   MIDDLEWARE
# ------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'sistema_raciones.urls'


# ------------------------
#   TEMPLATES
# ------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",   # Carpeta de templates global
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'panel.context_processors.stock_summary',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'sistema_raciones.wsgi.application'


# ------------------------
#   BASE DE DATOS - MYSQL
# ------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'avicoladb',           # NOMBRE DE TU BASE DE DATOS
        'USER': 'tori',              # Tu usuario de MySQL
        'PASSWORD': '123456',          # Tu contraseña de MySQL (cámbiala por la tuya)
        'HOST': '127.0.0.1',         # Localhost
        'PORT': '3306',              # Puerto por defecto de MySQL
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# ------------------------
#   VALIDACIÓN PASSWORD
# ------------------------

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


# ------------------------
#   IDIOMA Y TIEMPO
# ------------------------

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True



# ------------------------
#   ARCHIVOS STATIC
# ------------------------

STATIC_URL = 'static/'

# Carpeta donde Django buscará tus imágenes, CSS, JS
STATICFILES_DIRS = [
    BASE_DIR / "panel" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"



# ------------------------
#   LOGIN
# ------------------------

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
