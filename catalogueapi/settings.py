"""
Django settings for catalogueapi project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

from .secrets import Config
from .environments import ALLOWED_ENVS, ENV_LOCAL, ENV_PROD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)fnl#4^%6ghbt+mq$i32n56=9a)%=xe9(1zhohi)uvb=nvxa#3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Current ENVIRONMENT config
ARHOLDINGSAPI_ENV= os.environ.get('ARHOLDINGSAPI_ENV', ENV_LOCAL)
if ARHOLDINGSAPI_ENV == ENV_PROD:
    DEBUG = False
if ARHOLDINGSAPI_ENV not in ALLOWED_ENVS:
    raise Exception('ARHOLDINGSAPI_ENV must be on of ({})'.format(ALLOWED_ENVS))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'catalogueapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'catalogueapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

Config.set_database_credentials(env=ARHOLDINGSAPI_ENV)

if not Config.DATABASE_CRED:
    raise Exception("Can not setup database configuration for {} not defined".format(ARHOLDINGSAPI_ENV))

if ARHOLDINGSAPI_ENV in ALLOWED_ENVS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': Config.DATABASE_CRED['NAME'],
            'USER': Config.DATABASE_CRED['USER'],
            'PASSWORD': Config.DATABASE_CRED['PASSWORD'],
            'HOST': Config.DATABASE_CRED['HOST'],
            'PORT': Config.DATABASE_CRED['PORT'],
            'ATOMIC_REQUESTS': True
        }
    }
else:
    raise Exception("Database configuration for {} not defined".format(ARHOLDINGSAPI_ENV))



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'