"""
This settings file connects Django to various integrations for various purposes
such as Sentry for error-logging or Grafana for monitoring, to name a few.
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from omniport.settings.configuration.base import CONFIGURATION as _CONF

# Sentry
if 'sentry' in _CONF.integrations:
    sentry_sdk.init(
        dsn=_CONF.integrations.get('sentry').get('dsn'),
        integrations=[
            DjangoIntegration(),
        ],
    )
