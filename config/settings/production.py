# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from django.utils import six
from .common import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")

# This ensures that Django will be able to detect a secure connection on reverse proxies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# django-secure
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("djangosecure",)

SECURITY_MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
)

MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + MIDDLEWARE_CLASSES

# set this to 60 seconds and then to 518400 when you can prove it works
# SECURE_HSTS_SECONDS = 60 # done in nginx
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# SECURE_FRAME_DENY = env.bool("DJANGO_SECURE_FRAME_DENY", default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
# SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
CSRF_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
# END SITE CONFIGURATION

INSTALLED_APPS += ("gunicorn",)

# set default redis variable
os.environ.setdefault("REDIS_URL",
                      'redis://%s:%s/0' % (env("REDIS_PORT_6379_TCP_ADDR"), env("REDIS_PORT_6379_TCP_PORT")))

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'

GS_ACCESS_KEY_ID = env('GCLOUD_KEY')
GS_SECRET_ACCESS_KEY = env('GCLOUD_KEY_SECRET')
GS_BUCKET_NAME = env('GCLOUD_BUCKET')
GS_AUTO_CREATE_BUCKET = True
GS_QUERYSTRING_AUTH = True
GS_QUERYSTRING_EXPIRE = 60

# STATICFILES_STORAGE = 'storages.backends.gs.GSBotoStorage'

# AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
# AWS_AUTO_CREATE_BUCKET = True
# AWS_QUERYSTRING_AUTH = True
# AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
# AWS_HEADERS = {
#     'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY))
# }

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_ROOT = '/media/'
MEDIA_URL = 'https://s3.amazonaws.com/%s/%s' % (GS_BUCKET_NAME, MEDIA_ROOT)

# Static Assets
# ------------------------
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# STATIC_HOST = env('DJANGO_STATIC_HOST')
STATIC_URL = '/static/'  # STATIC_HOST + '/static/'

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'speakeazy',
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_URL"),  # Or an IP Address that your DB is hosted on
        'PORT': env("DATABASE_PORT"),
        'ATOMIC_REQUESTS': True,
    }
}

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%s/%s" % (env('REDIS_PORT_6379_TCP_ADDR'), env('REDIS_PORT_6379_TCP_PORT'), 0),
        # "LOCATION": "{0}/{1}".format(env.cache_url('REDIS_URL', default="redis://127.0.0.1:6379"), 0),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,  # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    }
}

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['file', 'mail_admins'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': '/app/django.log'
        }
    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'handlers': ['file', 'mail_admins'],
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'level': 'ERROR',
        #     'handlers': ['file', 'mail_admins'],
        #     'propagate': False,
        # },
        # 'django.request': {
        #     'level': 'ERROR',
        #     'handlers': ['file', 'mail_admins'],
        #     'propagate': False,
        # },
        'django.security': {
            'level': 'info',
            'handlers': ['file', 'mail_admins'],
            'propagate': False,
        },
    },
}

#
# INSTALLED_APPS += (
#     'opbeat.contrib.django',
# )
# OPBEAT = {
#     'ORGANIZATION_ID': env('OPBEAT_ORGANIZATION_ID'),
#     'APP_ID': env('OPBEAT_APP_ID'),
#     'SECRET_TOKEN': env('OPBEAT_SECRET_TOKEN'),
# }
# MIDDLEWARE_CLASSES = ('opbeat.contrib.django.middleware.OpbeatAPMMiddleware',) + MIDDLEWARE_CLASSES

# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = env('DJANGO_ADMIN_URL', default=r'^admin/')

# Your production stuff: Below this line define 3rd party library settings
BCRYPT_ROUNDS = env('BCRYPT_ROUNDS', default=12)

# Set production celery url
BROKER_URL = env("REDIS_URL")
