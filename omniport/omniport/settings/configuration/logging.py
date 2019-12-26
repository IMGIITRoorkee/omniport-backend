from omniport.settings.base.discovery import DISCOVERY
from omniport.settings.configuration.base import CONFIGURATION

site_id = CONFIGURATION.site.id
server = CONFIGURATION.server

DISCOVERY.prepare_logging(server, site_id)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Filters based on Django DEBUG
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    # Formatters
    'formatters': {
        'loquacious': {
            'format': (
                '{levelname:>8} {asctime} {process:d} | '
                '{module:>16} ❯ {message}'
            ),
            'datefmt': '%a %d/%b/%y %H:%M:%S',  # e.g. Mon 01/Apr/19 13:26:39
            'style': '{',
        },
        'succinct': {
            'format': (
                '{levelname:>8} | '
                '{message}'
            ),
            'datefmt': '%a %d/%b/%y %H:%M:%S',  # e.g. Mon 01/Apr/19 13:26:39
            'style': '{',
        },
    },

    # Handlers
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true', ],
            'formatter': 'succinct',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false', ],
            'formatter': 'loquacious',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'/web_server_logs/{server}_logs/{site_id}-django.log',
            'when': 'midnight',
            'backupCount': 32,
        },
        # App-level handlers
        **DISCOVERY.app_logging_handlers,
        **DISCOVERY.service_logging_handlers,
    },

    # Loggers
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': [
                'console',
                'file',
            ],
            'propagate': False,
        },
        # App-level loggers
        **DISCOVERY.app_logging_loggers,
        **DISCOVERY.service_logging_loggers,
    },
}

__all__ = [
    'LOGGING',
]
