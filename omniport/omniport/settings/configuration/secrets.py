"""
This settings file exposes critical secrets of the instance.
"""

from omniport.settings.configuration.base import CONFIGURATION as _CONF

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = _CONF.secrets.secret_key
