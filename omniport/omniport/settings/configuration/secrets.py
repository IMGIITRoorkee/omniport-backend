"""
This settings file exposes critical secrets of the instance.
"""

from omniport.settings.configuration.base import configuration as _conf

# This key, as implied by the name, should be a well-protected secret
SECRET_KEY = _conf.secrets.secret_key
