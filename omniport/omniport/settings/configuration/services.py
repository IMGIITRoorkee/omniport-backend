"""
This settings files exposes configurations for various services that run
alongside Django such as databases and message brokers.
"""

from omniport.settings.configuration.base import configuration as _conf

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': _conf.services.database.name,
        'HOST': _conf.services.database.host,
        'PORT': _conf.services.database.port,
        'USER': _conf.services.database.user,
        'PASSWORD': _conf.services.database.password,
    },
}

# Channel layer
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    _conf.services.channel_layer.host,
                    _conf.services.channel_layer.port,
                )
            ],
        },
    },
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': (f'{_conf.services.cache.host}'
                     f':{_conf.services.cache.port}'),
    },
    'notification': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': (
            'redis://'
            f'{_conf.services.notification_store.host}'
            f':{_conf.services.notification_store.port}'
            '/0'
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': (
            'redis://'
            f'{_conf.services.session_store.host}'
            f':{_conf.services.session_store.port}'
            f'/0'
        ),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
    }
}
