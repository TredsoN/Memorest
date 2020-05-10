"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0bw76$-yfj^v&e21fo9o&3#4ha@(dx8egq2^+*!nw3h-pi6=bh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

djcelery.setup_loader()  ###
CELERY_TIMEZONE='Asia/Shanghai'  #并没有北京时区，与下面TIME_ZONE应该一致
BROKER_URL='redis://localhost:6379'  #任何可用的redis都可以，不一定要在django server运行的主机上
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  ###
CELERYD_MAX_TASKS_PER_CHILD = 5

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user',
    'memory',

    'graphene_django',  # GraphQL
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',  # JWT
    'graphql_auth',  # GraphQL Auth
    'django_filters',
    'corsheaders',
    'djcelery',
    # 'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Memorest',
        'USER': 'root',
        'PASSWORD': '000116',
        'HOST': '106.13.41.151',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=(
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = '/home/memorest/static/'

# Auth
AUTH_USER_MODEL = 'user.User'

# GraphQL
GRAPHENE = {
    'SCHEMA': 'backend.schema.schema',  # Root schema
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": True,
    'JWT_EXPIRATION_DELTA': timedelta(minutes=3),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),

    # optional
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,

    "JWT_ALLOW_ANY_CLASSES": [
        "user.schema.Register",
        "user.schema.Login",
        "user.schema.PasswordReset",
        "user.schema.GenerateVerificationCode",
    ],
}

GRAPHQL_AUTH = {
    'UPDATE_MUTATION_FIELDS': ['username', ],

    'ALLOW_DELETE_ACCOUNT': True
}


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtpdm.aliyun.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'memorest@email.streack.cn'
EMAIL_HOST_PASSWORD = 'MEmorest123'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'fforkboat@gmail.com'

SITE_URL = '127.0.0.1:8000'

CORS_ORIGIN_ALLOW_ALL = True

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "up_img")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace("\\", "/")

# # 定时任务
# CELERY_BEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'memory.tasks.cycleprocessing',  # 任务名
#         'schedule': timedelta(seconds=1),  # 每一秒执行一次该任务
#         'args': ()  # 参数
#     },
# }
