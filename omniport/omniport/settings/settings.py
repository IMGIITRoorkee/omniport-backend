"""
This setting file imports all settings from various setting files and then some.
"""

from omniport.settings.base import *  # Hardcoded settings
from omniport.settings.configuration import *  # Settings parsed from YAML files
from omniport.settings.third_party import *  # Settings for PyPI packages

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
else:
    SESSION_COOKIE_SECURE = True

# Import shell models to replace swappable models from other apps
if SHELL_PRESENT:
    from shell.swapper_replacements import *

# Roles
ROLES = list()

# Serializers
from kernel.serializers.registration import *

if SHELL_PRESENT:
    from shell.serializers.registration import *
