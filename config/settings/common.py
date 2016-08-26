# -*- coding: utf-8 -*-
"""
Django settings for Speakeazy project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ
from django.core.exceptions import ImproperlyConfigured

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('speakeazy')

env = environ.Env()  # https://github.com/jpadilla/django-dotenv

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'flat',
    'django.contrib.admin',
    'django.contrib.admindocs',
)
THIRD_PARTY_APPS = (
    'floppyforms',

    'userena',

    'guardian',
    'easy_thumbnails',

    'rest_framework',
    'rest_framework_swagger',

    'kombu.transport.django',

    'django_js_reverse',  # https://github.com/ierror/django-js-reverse
    'easy_timezones',  # https://github.com/Miserlou/django-easy-timezones
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'speakeazy.users',  # custom users app

    # Your stuff: custom apps go here
    'speakeazy.projects',
    'speakeazy.recordings',
    'speakeazy.groups',
    'speakeazy.speakeazy',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# apps that need to be added last
INSTALLED_APPS += (
    'hijack',  # http://django-hijack.readthedocs.org/en/latest/
    'compat',
)

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    # Make sure djangosecure.middleware.SecurityMiddleware is listed first
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easy_timezones.middleware.EasyTimezoneMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'speakeazy.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
# FIXTURE_DIRS = (
#     str(APPS_DIR.path('fixtures')),
# )

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Ryan Mirman""", 'rsgm123@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# AUTHENTICATION CONFIGURATION
#
# http://docs.django-userena.org/en/latest/settings.html
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'users.UserProfile'
AUTH_USER_MODEL = 'users.User'

# USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'
USERENA_SIGNIN_REDIRECT_URL = '/dashboard'
USERENA_ACTIVATION_NOTIFY = False
USERENA_MUGSHOT_GRAVATAR = False
USERENA_DEFAULT_PRIVACY = 'closed'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_HIDE_EMAIL = True
USERENA_HTML_EMAIL = True
USERENA_REGISTER_USER = False  # override userena admin page
USERENA_REGISTER_PROFILE = False  # override userena admin page
USERENA_REDIRECT_ON_SIGNOUT = 'userena_signin'
USERENA_FORBIDDEN_USERNAMES = ('signup', 'signout', 'signin', 'activate', 'me', 'password', 'admin')

LOGIN_REDIRECT_URL = 'speakeazy:dashboard'
LOGIN_URL = 'userena_signin'
LOGOUT_URL = 'userena_signout'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# CELERY
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('speakeazy.taskapp.celery.CeleryConfig',)

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings

PASSWORD_HASHERS = (
    'speakeazy.users.bcryptHasher.Bcrypt',
)

try:
    RECORDING_ROOT_PATH = environ.Path(env("RECORDING_ROOT_PATH"))
except ImproperlyConfigured:
    RECORDING_ROOT_PATH = ROOT_DIR.path('recordings')

RECORDING_PATHS = {
    'VIDEO_PIECES': RECORDING_ROOT_PATH.path('video_pieces'),
    'AUDIO_PIECES': RECORDING_ROOT_PATH.path('audio_pieces'),
    'CONVERTED_PIECES': RECORDING_ROOT_PATH.path('converted_pieces'),
    'LISTS': RECORDING_ROOT_PATH.path('lists'),
    'THUMBNAILS': RECORDING_ROOT_PATH.path('thumbnails'),
    'FINISHED': RECORDING_ROOT_PATH.path('finished'),
    'AUDIENCE': RECORDING_ROOT_PATH.path('audience')
}

FFMPEG_LOG_LEVEL = 'quiet'

GEOIP_DATABASE = str(ROOT_DIR.path('resources/GeoLiteCity.dat'))
GEOIPV6_DATABASE = str(ROOT_DIR.path('resources/GeoLiteCityv6.dat'))

JS_REVERSE_INCLUDE_ONLY_NAMESPACES = ['recordings', 'projects', 'groups']
JS_REVERSE_OUTPUT_PATH = str(APPS_DIR.path('static/js'))

HIJACK_USE_BOOTSTRAP = False

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'PAGE_SIZE': 10
}
