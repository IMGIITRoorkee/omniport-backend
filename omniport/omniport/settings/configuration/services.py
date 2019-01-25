"""
This settings files exposes configurations for various services that run
alongside Django such as databases and message brokers.
"""

from omniport.settings.configuration.base import CONFIGURATION as _CONF

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': _CONF.services.database.name,
        'HOST': _CONF.services.database.host,
        'PORT': _CONF.services.database.port,
        'USER': _CONF.services.database.user,
        'PASSWORD': _CONF.services.database.password,
    },
}

# Channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    _CONF.services.channel_layer.host,
                    _CONF.services.channel_layer.port,
                )
            ],
        },
    },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': (f'{_CONF.services.cache.host}'
                     f':{_CONF.services.cache.port}'),
    },
    'notification': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': (
            'redis://'
            f'{_CONF.services.notification_store.host}'
            f':{_CONF.services.notification_store.port}'
            '/0'
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            'REDIS_CLIENT_KWARGS': {
                'encoding': 'utf-8',
                'decode_responses': True,
            },
        },
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': (
            'redis://'
            f'{_CONF.services.session_store.host}'
            f':{_CONF.services.session_store.port}'
            f'/0'
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
    }
}
