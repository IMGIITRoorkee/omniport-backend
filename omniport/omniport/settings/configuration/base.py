"""
Omniport settings are cascaded in two layers, base and site. Both layers are
read from YAML files and combined.

This settings file exposes the entire configuration from the YAML files as a
Python object of class ProjectConfiguration.
"""

import os

import yaml

from configuration.models.project.imagery import Imagery, SiteImagery
from configuration.models.project.project import ProjectConfiguration
from omniport.settings.base.directories import CONFIGURATION_DIR, BRANDING_DIR
from omniport.settings.base.files import BRANDING_URL

# Site ID helps in loading site-specific configuration
site_id = int(os.getenv('SITE_ID', '0'))

# Read the configuration files from the ``configuration`` directory
base_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'base.yml'
))
base_configuration = yaml.safe_load(base_config_file)
site_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'sites',
    f'site_{site_id}.yml'
))
site_configuration = yaml.safe_load(site_config_file)

# Note that site_configuration overrides base_configuration
configuration = {**base_configuration, **site_configuration}
CONFIGURATION = ProjectConfiguration(dictionary=configuration)

# Imagery
site_imagery_directory = os.path.join(BRANDING_DIR, f'site_{site_id}')
if not os.path.isdir(site_imagery_directory):
    site_imagery_directory = os.path.join(BRANDING_DIR, 'site')

CONFIGURATION.site.imagery = SiteImagery(
    directory=os.path.join(BRANDING_DIR, site_imagery_directory),
    url=BRANDING_URL,
)
CONFIGURATION.branding.institute.imagery = Imagery(
    directory=os.path.join(BRANDING_DIR, 'institute'),
    url=BRANDING_URL,
)
CONFIGURATION.branding.maintainers.imagery = Imagery(
    directory=os.path.join(BRANDING_DIR, 'maintainers'),
    url=BRANDING_URL,
)

__all__ = [
    'CONFIGURATION',
]
