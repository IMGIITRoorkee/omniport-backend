"""
This file extends the base settings with settings loaded from the YAML
configuration files.
"""

import yaml

from configuration.project_configuration import ProjectConfiguration
# Import base settings to override or extend them
from omniport.settings.base import *

# Site ID helps in loading site-specific configuration
SITE_ID = int(os.getenv('SITE_ID', '0'))

# Read the configuration files from the ``configuration`` directory

base_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'base.yml'
))
base_configuration = yaml.load(base_config_file)

site_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'sites',
    f'site_{SITE_ID}.yml'
))
site_configuration = yaml.load(site_config_file)

# Note that site_configuration overrides base_configuration
configuration = {**base_configuration, **site_configuration}

configuration = ProjectConfiguration(dictionary=configuration)

# Branding

INSTITUTE_NAME = configuration.branding.institute.name

INSTITUTE_HOME_PAGE = configuration.branding.institute.home_page

MAINTAINERS_NAME = configuration.branding.maintainers.name

MAINTAINERS_HOME_PAGE = configuration.branding.maintainers.home_page

# Site

SITE_NAME = configuration.site.name

SITE_VERBOSE_NAME = configuration.site.verbose_name

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': configuration.services.database.name,
        'HOST': configuration.services.database.host,
        'PORT': configuration.services.database.port,
        'USER': configuration.services.database.user,
        'PASSWORD': configuration.services.database.password,
    },
}

# Channel layer
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    configuration.services.channel_layer.host,
                    configuration.services.channel_layer.port,
                )
            ],
        },
    },
}

# CORS configuration

CORS_ALLOW_CREDENTIALS = configuration.cors.allow_credentials

CORS_ORIGIN_WHITELIST = configuration.cors.origin_whitelist

CORS_ORIGIN_ALLOW_ALL = configuration.cors.origin_allow_all

# Network rings

IP_ADDRESS_RINGS = dict()

ip_address_rings = configuration.ip_address_rings
for ip_address_ring in ip_address_rings:
    name = ip_address_ring.name
    patterns = ip_address_ring.patterns
    IP_ADDRESS_RINGS[name] = patterns

# Internationalisation and localisation

LANGUAGE_CODE = configuration.i18n.language_code

TIME_ZONE = configuration.i18n.time_zone

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = configuration.secret_key

# This variable should be True in testing environments and False otherwise
DEBUG = configuration.debug

# The list of hosts to which this site will respond
ALLOWED_HOSTS = configuration.allowances.hosts

# The list of apps whose URLs will be loaded in this site

ALLOWED_APPS = configuration.allowances.apps

for (app, app_configuration) in DISCOVERY.services:
    app_configuration.is_allowed = True  # Hack to allow all services
for (app, app_configuration) in DISCOVERY.apps:
    if (
            ALLOWED_APPS == '__all__'
            or app_configuration.nomenclature.name in ALLOWED_APPS
    ):
        app_configuration.is_allowed = True
    else:
        app_configuration.is_allowed = False

# The list of IP address rings which this site will service

ALLOWED_IP_ADDRESS_RINGS = configuration.allowances.ip_address_rings

if ALLOWED_IP_ADDRESS_RINGS == '__all__':
    ALLOWED_IP_ADDRESS_RINGS = list(IP_ADDRESS_RINGS.keys())
