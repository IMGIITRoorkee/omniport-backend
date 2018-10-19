"""
This settings file exposes variables pertaining to the current site such as
codename and verbose name.
"""

from omniport.settings.configuration.base import configuration as _conf

# The ID for the site is a number used to identify the correct YAML files
SITE_ID = _conf.site.id

# A codename for the site, just in case
SITE_NAME = _conf.site.name

# The public name of the site that is shown everywhere
SITE_VERBOSE_NAME = _conf.site.verbose_name

# Should be True in testing environments and False otherwise
DEBUG = _conf.site.debug
