"""
This setting file imports all settings from various setting files and then some.
"""

from omniport.settings.base import *  # Hardcoded settings
from omniport.settings.configuration import *  # Settings parsed from YAML files
from omniport.settings.third_party import *  # Settings for PyPI packages

# Import shell models to replace swappable models from other apps
if SHELL_PRESENT:
    from shell.swapper import *

if not DEBUG:
    SESSION_COOKIE_SECURE = True

# Primary URLconf served by Gunicorn and Daphne
ROOT_URLCONF = 'omniport.urls'

# Roles
ROLES = list()
