"""
This settings file exposes the configuration settings for templates.
"""

import os

from omniport.settings.base.directories import PROJECT_DIR, OMNIPORT_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
            os.path.join(OMNIPORT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'omniport.context.branding.branding_imagery',
                'omniport.context.branding.branding_text',
                'omniport.context.site.site_information',
            ],
        },
    },
]

__all__ = [
    'TEMPLATES',
]
