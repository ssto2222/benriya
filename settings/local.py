"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
# from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

NUMBER_GROUPING = 3

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


try:
    import yaml
    with open(os.path.join(BASE_DIR,'secrets','secret.yaml')) as f:
        objs = yaml.safe_load(f)
        for obj in objs['env_variables']:
            os.environ[obj] = objs['env_variables'][obj]
except:
    print('no yaml files')


SECRET_KEY = os.environ['SECRET_KEY']
#stripe設定
STRIPE_SECRET_KEY=os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHED_KEY=os.environ['STRIPE_PUBLISHED_KEY']

#load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']
#stripe設定
STRIPE_SECRET_KEY=os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHED_KEY=os.environ['STRIPE_PUBLISHED_KEY']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mainapp',
    'blog',
    'store',
    'basket',
    'payment',
    'orders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

LIVERELOAD_PORT = '8080'

ROOT_URLCONF = 'config.urls'

#AUTH_USER_MODEL = 'mainapp.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'basket.context_processors.basket',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
   os.path.join(BASE_DIR,'static')
]

# # Following settings only make sense on production and may break development environments.
# if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
#     # in your application directory on Render.
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#     # Turn on WhiteNoise storage backend that takes care of compressing static files
#     # and creating unique names for each version so they can safely be cached forever.
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

AUTH_USER_MODEL = 'mainapp.User'

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_URL = '/logout/'

LOGOUT_REDIRECT_URL = '/login/'

from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: "rounded-0 alert alert-danger",
    messages.WARNING: "rounded-0 alert alert-warning",
    messages.SUCCESS: "rounded-0 alert alert-success",
    messages.INFO: "rounded-0 alert alert-info",
    messages.DEBUG: "rounded-0 alert alert-secondary",
}        

#---Gmail 送信設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587   
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']