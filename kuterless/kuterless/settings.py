"""
Django settings for kuterless project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+i4mx76+pi29$50gdbxh%111@it_hz=(bw39@o16uru=_-pxa+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [u'95.85.3.168', u'127.0.0.1']

SITE_ID  = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'south',
    'public_fulfillment',
    'coplay',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)




TEMPLATE_CONTEXT_PROCESSORS = (
                            "django.contrib.auth.context_processors.auth",
                            "django.core.context_processors.request",
                            "django.core.context_processors.debug",
                            "django.core.context_processors.i18n",
                            "django.core.context_processors.media",
                            "django.core.context_processors.static",
                            "django.core.context_processors.tz",
                            "django.contrib.messages.context_processors.messages"
                            )

ROOT_URLCONF = 'kuterless.urls'

WSGI_APPLICATION = 'kuterless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'kuterless',
        'USER':'kuterless',
        'PASSWORD':'kuterless',
        'HOST':'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'he'
#LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_URL = '/static/'

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}



try:
    from local_settings import *
except ImportError:
    pass
