#!/usr/bin/env python
import os
import ast
import dj_database_url

DEBUG = ast.literal_eval(os.environ['DEBUG_STATE'])

# Begin environ variables

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

# End environ variables


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
    'storages',
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



DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_QUERYSTRING_AUTH = False # This will make sure that the file URL does not have unnecessary parameters like your access key.
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'

#static media settings
MEDIA_STATIC_URL = 'https://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'
MEDIA_URL = STATIC_URL + 'media/'


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Server place staticfiles
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'statics'),)

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
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
