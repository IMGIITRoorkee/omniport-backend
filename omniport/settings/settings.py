import json

from omniport.settings.base import *

# Site ID helps in loading site-specific configuration
SITE_ID = int(os.getenv('SITE_ID', '0'))

# Read the configuration files from the ``configuration`` directory

base_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'base.json'
))
base_configuration = json.load(base_config_file)

site_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'sites',
    f'site_{SITE_ID}.json'
))
site_configuration = json.load(site_config_file)

# Note that site_configuration overrides base_configuration
configuration = {**base_configuration, **site_configuration}

# Branding

BRANDING = configuration.get('branding', {})

INSTITUTE = BRANDING.get('institute', {})
INSTITUTE_NAME = INSTITUTE.get('name', 'Institute')
INSTITUTE_HOME_PAGE = INSTITUTE.get('homePage',
                                    'https://dhruvkb.github.io/')

MAINTAINERS = BRANDING.get('maintainers', {})
MAINTAINERS_NAME = MAINTAINERS.get('name', 'Dhruv Bhanushali')
MAINTAINERS_HOME_PAGE = MAINTAINERS.get('homePage',
                                        'https://dhruvkb.github.io/')

# Site

SITE = configuration.get('site', {})

SITE_NAME = SITE.get('name', f'site_{SITE_ID}')

SITE_VERBOSE_NAME = SITE.get('verboseName', f'Omniport Site {SITE_ID}')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE = configuration.get('database', {})

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': DATABASE.get('host', 'database'),
        'NAME': DATABASE.get('name', 'omniport_database'),
        'USER': DATABASE.get('user', 'omniport_user'),
        'PASSWORD': DATABASE.get('password', 'omniport_password'),
        'PORT': DATABASE.get('port', 5432),
    },
}

# Channel layer
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYER = configuration.get('channelLayer', {})

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    CHANNEL_LAYER.get('host', 'channel-layer'),
                    CHANNEL_LAYER.get('port', 6379),
                )
            ],
        },
    },
}

# Internationalisation and localisation

I18N = configuration.get('i18n', {})

LANGUAGE_CODE = I18N.get('languageCode', 'en-gb')

TIME_ZONE = I18N.get('timeZone', 'Asia/Kolkata')

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = configuration.get(
    'secretKey',
    # For the love of all that is holy, change this in production
    'placeholder_19kbufifr&(r5i8qv&i-e^d08ma#1s0kgdi(_lce9r301teck-'
)

# This variable should be True in testing environments and False otherwise
DEBUG = configuration.get('debug', False)

if DEBUG:
    # The list of hosts to which this application will respond
    ALLOWED_HOSTS = ['*']
    # The list of apps whose URLs will be loaded in this app
    ALLOWED_APPS = '__all__'
else:
    # The list of hosts to which this application will respond
    ALLOWED_HOSTS = configuration.get('allowedHosts', [])
    # The list of apps whose URLs will be loaded in this app
    ALLOWED_APPS = configuration.get('allowedApps', '__all__')
