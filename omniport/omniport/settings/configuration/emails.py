"""
This settings file exposes critical configurations for email service.
"""

from omniport.settings.configuration.base import CONFIGURATION as _CONF

EMAIL_BACKEND = _CONF.emails.email_backend
EMAIL_HOST = _CONF.emails.email_host
EMAIL_USE_TLS = _CONF.emails.email_use_tls
EMAIL_PORT  = _CONF.emails.email_port
EMAIL_HOST_USER = _CONF.emails.email_host_user
EMAIL_HOST_PASSWORD = _CONF.emails.email_host_password
