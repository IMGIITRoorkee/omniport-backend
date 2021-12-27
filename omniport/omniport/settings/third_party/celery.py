from omniport.settings.configuration.base import CONFIGURATION as _CONF

# Celery configuration

CELERY_BROKER_URL = (
    f'amqp://'
    f'{_CONF.services.message_broker.user}'
    f':{_CONF.services.message_broker.password}'
    f'@{_CONF.services.message_broker.host}'
    f':{_CONF.services.message_broker.port}'
)

# CELERY_RESULT_BACKEND = 'django-cache'

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = _CONF.i18n.time_zone

CELERY_RESULT_BACKEND = 'django-cache'

CELERY_TASK_TIME_LIMIT = 15*60

