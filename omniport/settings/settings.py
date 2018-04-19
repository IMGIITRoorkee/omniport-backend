from omniport.settings.base import *

# Institute

INSTITUTE = os.getenv('INSTITUTE', 'Institute')
INSTITUTE_HOME_PAGE = os.getenv(
    'INSTITUTE_HOME_PAGE',
    'https://dhruvkb.github.io/'
)

MAINTAINERS = os.getenv('MAINTAINERS', 'Dhruv Bhanushali')
MAINTAINERS_HOME_PAGE = os.getenv(
    'MAINTAINERS_HOME_PAGE',
    'https://dhruvkb.github.io/'
)

# Site

SITE_ID = int(os.getenv('SITE_ID', 0))

SITE_NAME = os.getenv('SITE_NAME', f'site_{SITE_ID}')

SITE_VERBOSE_NAME = os.getenv('SITE_VERBOSE_NAME', f'Omniport Site {SITE_ID}')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'omniport_database'),
        'USER': os.getenv('DATABASE_USER', 'omniport_user'),
        'HOST': os.getenv('DATABASE_HOST', 'database'),
        'PORT': int(os.getenv('DATABASE_PORT', '5432')),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'omniport_password'),
    },
}

# Internationalisation and localisation

LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-gb')

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Kolkata')

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    # For the love of all that is holy, change this in production
    'placeholder_19kbufifr&(r5i8qv&i-e^d08ma#1s0kgdi(_lce9r301teck-'
)

# This variable should be True in testing environments and False otherwise
DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False

if DEBUG is True:
    # The list of hosts to which this application will respond
    ALLOWED_HOSTS = ['*']
    # The list of apps whose URLs will be loaded in this app
    ALLOWED_APPS = '__all__'
else:
    hostnames = os.getenv('HOSTNAMES', '*')
    ALLOWED_HOSTS = hostnames.split(',')

    allowed_apps = os.getenv('ALLOWED_APPS', None)
    if allowed_apps is None:
        ALLOWED_APPS = '__all__'
    else:
        ALLOWED_APPS = allowed_apps.split(',')
