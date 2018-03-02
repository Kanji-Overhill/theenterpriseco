#!/usr/bin/env python
import os
import ast
import dj_database_url

LOCAL_SETTINGS = ast.literal_eval(os.environ['LOCAL_SETTINGS'])

DEBUG = ast.literal_eval(os.environ['LOCAL_SETTINGS'])

if LOCAL_SETTINGS:
    from enterpriseback.local_set import *
else:
    DATABASE_URL = os.environ['DATABASE_URL']
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}
    #EMail Settings
    EMAIL_USE_TLS = ast.literal_eval(os.environ['EMAIL_USE_TLS'])
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = os.environ['EMAIL_PORT']

    TO_SEND = os.environ['TO_SEND']
    SENDER = os.environ['SENDER']
    SENDER_CONTACT = os.environ['SENDER_CONTACT']
    SENDER_CONTACT_PASS =os.environ['SENDER_CONTACT_PASS']

    #CATCHA SETTINGS
    RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
    NOCAPTCHA = ast.literal_eval(os.environ['NOCAPTCHA'])
    RECAPTCHA_USE_SSL = ast.literal_eval(os.environ['RECAPTCHA_USE_SSL'])

    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS']

    SECRET_KEY = os.environ['SECRET_KEY']


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'buildings.apps.BuildingsConfig',
    'managers.apps.ManagersConfig',
    'home.apps.HomeConfig',
    'django_cleanup',
    'captcha',
    'imagekit',
)

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'enterpriseback.urls'

WSGI_APPLICATION = 'enterpriseback.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Server place staticfiles
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'statics'),)

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Console logging for DEBUG=False - Probably should disable if DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'loggers': {
        'django_info': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}
