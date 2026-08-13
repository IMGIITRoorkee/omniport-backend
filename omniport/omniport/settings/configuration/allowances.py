"""
Omniport allows configuring the allowed hosts, apps and IP addresses via
external YAML files.

This settings file exposes settings pertaining to allowances.
"""

from omniport.settings.base.discovery import DISCOVERY as _DISCOVERY
from omniport.settings.configuration.base import CONFIGURATION as _CONF

# Allowed hosts
ALLOWED_HOSTS = _CONF.allowances.hosts

# Allowed apps
ALLOWED_APPS = _CONF.allowances.apps

for (_app, _app_configuration) in _DISCOVERY.services:
    _app_configuration.is_allowed = True  # Hack to allow all services

for (_app, _app_configuration) in _DISCOVERY.apps:
    if (
            ALLOWED_APPS == '__all__'
            or _app_configuration.nomenclature.name in ALLOWED_APPS
    ):
        _app_configuration.is_allowed = True
    else:
        _app_configuration.is_allowed = False

# IP address rings
IP_ADDRESS_RINGS = dict()
_ip_address_rings = _CONF.ip_address_rings

for _ip_address_ring in _ip_address_rings:
    _name = _ip_address_ring.name
    _patterns = _ip_address_ring.patterns
    IP_ADDRESS_RINGS[_name] = _patterns

ALLOWED_IP_ADDRESS_RINGS = _CONF.allowances.ip_address_rings
if ALLOWED_IP_ADDRESS_RINGS == '__all__':
    ALLOWED_IP_ADDRESS_RINGS = list(IP_ADDRESS_RINGS.keys())
