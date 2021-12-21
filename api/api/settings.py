"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

with open('../config.json') as fd:
    CONF = json.load(fd)

# ------------------------------------------------------------ #
# Standard Django Settings
# ------------------------------------------------------------ #

ACCOUNT_UNIQUE_EMAIL = False

ALLOWED_HOSTS = [
    CONF['ibis']['endpoints']['api'],
    CONF['ibis']['endpoints']['app'],
    CONF['ibis']['endpoints']['app'],
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ibis',
        'USER': 'ibis',
        'PASSWORD': CONF['postgres']['password'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

GRAPHENE = {'SCHEMA': 'api.schema.schema'}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'annoying',
    'crispy_forms',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.microsoft',
    'rest_auth',
    'rest_auth.registration',
    'corsheaders',
    'graphene_django',
    'api',
    'users',
    'ibis',
    'distribution',
    'notifications',
    'tracker',
    'gifts',
]

LANGUAGE_CODE = 'en-us'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO'
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

if 'authenticate_as' in CONF['ibis']:
    MIDDLEWARE += ['api.middleware.AuthenticateAllMiddleware']
    AUTHENTICATE_AS = CONF['ibis']['authenticate_as']

MIDDLEWARE += [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'tracker.middleware.TrackerMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

ROOT_URLCONF = 'api.urls'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONF['ibis']['secret_key']

STATIC_URL = '/static/'

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

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True

WSGI_APPLICATION = 'api.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# ------------------------------------------------------------ #
# Additional Library/App/Middleware Settings
# ------------------------------------------------------------ #

AUTH_USER_MODEL = 'users.GeneralUser'

# TODO: change to https when ready to launch from server
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'pwa-standalone',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ORIGIN_WHITELIST = (
    'https://{}'.format(CONF['ibis']['endpoints']['app']),
    'https://{}'.format(CONF['ibis']['endpoints']['info']),
    'http://localhost:3000',
)

CSRF_TRUSTED_ORIGINS = [
    CONF['ibis']['endpoints']['api'],
    CONF['ibis']['endpoints']['app'],
    CONF['ibis']['endpoints']['dash'],
]

CSRF_COOKIE_DOMAIN = 'tokenibis.org'

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

MEDIA_URL = os.path.join(BASE_DIR, "/media/")

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

SITE_ID = 1

SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_QUERY_EMAIL = True

# ------------------------------------------------------------ #
# Custom Ibis Settings
# ------------------------------------------------------------ #


def APP_LINK_RESOLVER(reference=None):
    lookup = {
        'Organization': '/organization?id={}',
        'News': '/news?id={}',
        'Event': '/event?id={}',
        'Person': '/person?id={}',
        'Donation': '/donation?id={}',
        'Post': '/post?id={}',
        'Bot': '/bot?id={}',
        'Reward': '/reward?id={}',
        'Activity': '/activity?id={}',
        'Grant': '/grant?id={}',
        'Withdrawal': '/withdrawal?id={}',
        'MessageDirect': '/message-direct-list?id={}',
        'MessageChannel': '/message-channel-list?id={}',
    }

    if not reference:
        return 'https://{}/#/'.format(CONF['ibis']['endpoints']['app'])

    return 'https://{}/#{}'.format(
        CONF['ibis']['endpoints']['app'],
        lookup[reference.split(':')[0]].format(reference.split(':')[1]),
    )


API_ROOT_PATH = 'https://{}'.format(CONF['ibis']['endpoints']['api'])

APP_ROOT_PATH = 'https://{}'.format(CONF['ibis']['endpoints']['app'])

AVATAR_BUCKET = 'https://s3.us-east-2.amazonaws.com/app.tokenibis.org/birds/{}.jpg'

AVATAR_BUCKET_LEN = 233

AWS_REGION_NAME = CONF['aws']['region_name']

AWS_ACCESS_KEY = CONF['aws']['access_key']

AWS_SECRET_ACCESS_KEY = CONF['aws']['secret_access_key']

BOT_GAS_INITIAL = 10000000

BOT_GAS_MUTATION = {
    'createDeposit': 100,
    'createReward': 100,
    'createActivity': 100,
    'createComment': 100,
    'createFollow': 100,
    'createLike': 100,
    'createBookmark': 100,
    'createRSVP': 100,
    'updateBot': 100,
    'updateNotifier': 100,
    'updateNotification': 100,
    'updateActivity': 100,
    'deleteFollow': 100,
    'deleteLike': 100,
    'deleteBookmark': 100,
    'deleteRSVP': 100,
}

BOT_GAS_EXCHANGE = 1000  # gas units per cent

BOT_GAS_QUERY_FIXED = 10

BOT_GAS_QUERY_VARIABLE = 1

DISTRIBUTION_DAY = CONF['ibis']['distribution']['day']

DISTRIBUTION_HORIZON = 3

DISTRIBUTION_CONTROLLER_KP = 0.25

DISTRIBUTION_CONTROLLER_TI = 1

DISTRIBUTION_CONTROLLER_TD = 0.5

DONATE_LINK = CONF['ibis']['endpoints']['donate']

EMAIL_ACTIVE = CONF['email']['active']

EMAIL_HOST = CONF['email']['host']

EMAIL_HOST_PASSWORD = CONF['email']['password']

EMAIL_HOST_USER = CONF['email']['user']

EMAIL_PORT = CONF['email']['port']

EMAIL_DELAY = 1  # minutes

EMAIL_USE_TLS = True

FACEBOOK_AVATAR = 'https://graph.facebook.com/v4.0/{}/picture?type=large'

GIFT_AMOUNT = CONF['ibis']['gifts']['amount']

GIFT_CHOICE_NUMBER = 10

GIFT_CHOICE_MIN = 4

GIFT_HORIZON_DAYS = 14

GIFT_PROBABILITY_HOURLY = CONF['ibis']['gifts']['weekly'] / 7 / 24

GIFT_EXCHANGE_CATEGORY = 'gift'

IBIS_USERNAME_ROOT = 'tokenibis'

IBIS_CATEGORY_UBP = 'ubp'

MAX_EXCHANGE = 100000

MAX_GRANT_TIME = 52

MAX_GRANT_WEEKLY = 10000

MAX_TRANSFER = 10000

PAYPAL_USE_SANDBOX = CONF['payment']['paypal']['use_sandbox']

PAYPAL_SANDBOX_CLIENT_ID = CONF['payment']['paypal']['sandbox']['client_id']

PAYPAL_SANDBOX_SECRET_KEY = CONF['payment']['paypal']['sandbox']['secret_key']

PAYPAL_LIVE_CLIENT_ID = CONF['payment']['paypal']['live']['client_id']

PAYPAL_LIVE_SECRET_KEY = CONF['payment']['paypal']['live']['secret_key']

if 'public_read' in CONF['ibis'] and CONF['ibis']['public_read']:
    PUBLIC_READ = True
else:
    PUBLIC_READ = False

QUOTE_URL = 'https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=jsonp&jsonp=?'

REDIRECT_URL_FACEBOOK = 'https://{}/redirect/facebook/'.format(
    CONF['ibis']['endpoints']['app'])

REDIRECT_URL_GOOGLE = 'https://{}/redirect/google/'.format(
    CONF['ibis']['endpoints']['app'])

REDIRECT_URL_MICROSOFT = 'https://{}/redirect/microsoft/'.format(
    CONF['ibis']['endpoints']['app'])

REDIRECT_URL_NOTIFICATIONS = 'https://{}/#/_/Settings'.format(
    CONF['ibis']['endpoints']['app'])

RESERVED_USERNAMES = ['admin', 'anonymous', 'dashboard']

SETTLE_BALANCE_MIN = 10000

SORT_ORGANIZATION_WINDOW_ENTRY = 4

SORT_ORGANIZATION_WINDOW_FUNDRAISED = 8

SORT_ORGANIZATION_WINDOW_JOINED = 2

SORT_ORGANIZATION_WINDOW_RESPONSE = 8

UNSUBSCRIBE_EMAIL = 'unsubscribe@tokenibis.org?subject=unsubscribe'
