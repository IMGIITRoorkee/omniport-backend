from omniport.settings.base import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'omniport_database'),
        'USER': os.getenv('DATABASE_USER', 'omniport_user'),
        'HOST': os.getenv('DATABASE_HOST', 'postgresql'),
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
DEBUG = True

if DEBUG is True:
    ALLOWED_HOSTS = ['*']
else:
    hostnames = os.getenv('HOSTNAMES', '')
    ALLOWED_HOSTS = hostnames.split(',')