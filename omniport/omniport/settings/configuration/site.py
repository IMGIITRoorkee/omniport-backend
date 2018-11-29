"""
This settings file exposes variables pertaining to the current site such as
codename and verbose name.
"""

from omniport.settings.configuration.base import CONFIGURATION as _CONF

SITE = _CONF.site

# Should be True in testing environments and False otherwise
DEBUG = _CONF.site.debug
