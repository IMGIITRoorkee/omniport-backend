"""
This settings file exposes settings for CORS headers
"""

from omniport.settings.configuration.base import configuration as _conf

CORS_ALLOW_CREDENTIALS = _conf.cors.allow_credentials
CORS_ORIGIN_WHITELIST = _conf.cors.origin_whitelist
CORS_ORIGIN_ALLOW_ALL = _conf.cors.origin_allow_all
