"""
    Base Django settings
"""

import logging
from pathlib import Path as __Path

from django.utils.translation import gettext_lazy as _


###############################################################################

# Build paths relative to the project root:
PROJECT_PATH = __Path(__file__).parent.parent.parent
print(f'PROJECT_PATH:{PROJECT_PATH}')

if __Path('/.dockerenv').is_file():
    # We are inside a docker container
    BASE_PATH = __Path('/django_volumes')
    assert BASE_PATH.is_dir()
else:
    # Build paths relative to the current working directory:
    BASE_PATH = __Path().cwd().resolve()

print(f'BASE_PATH:{BASE_PATH}')

# Paths with Django dev. server:
# BASE_PATH...: .../django-for-runners
# PROJECT_PATH: .../django-for-runners/src
#
# Paths in Docker container:
# BASE_PATH...: /for_runners_volumes
# PROJECT_PATH: /usr/local/lib/python3.9/site-packages

###############################################################################


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Serve static/media files by Django?
# In production Caddy should serve this!
SERVE_FILES = False

SECRET_KEY = 'test project without a real secret'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'deploy_django.apps.DeployDjangoConfig',
]

ROOT_URLCONF = 'deploy_django_project.urls'
WSGI_APPLICATION = 'deploy_django_project.wsgi.application'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [],
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

# _____________________________________________________________________________
# Internationalization

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Europe/Paris'
USE_TZ = True

# _____________________________________________________________________________
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(__Path(BASE_PATH, 'static'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(__Path(BASE_PATH, 'media'))

# _____________________________________________________________________________
# Django-dbbackup

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': str(__Path(BASE_PATH, 'backups'))}

# _____________________________________________________________________________
# cut 'pathname' in log output

old_factory = logging.getLogRecordFactory()


def cut_path(pathname, max_length):
    if len(pathname) <= max_length:
        return pathname
    return f'...{pathname[-(max_length - 3):]}'


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.cut_path = cut_path(record.pathname, 30)
    return record


logging.setLogRecordFactory(record_factory)

# -----------------------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'deploy_django': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
}
