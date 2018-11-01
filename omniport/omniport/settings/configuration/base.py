"""
Omniport settings are cascaded in two layers, base and site. Both layers are
read from YAML files and combined.

This settings file exposes the entire configuration from the YAML files as a
Python object of class ProjectConfiguration.
"""

import os

import yaml

from configuration.project.project import ProjectConfiguration
from omniport.settings.base.directories import CONFIGURATION_DIR

# Site ID helps in loading site-specific configuration
site_id = int(os.getenv('SITE_ID', '0'))

# Read the configuration files from the ``configuration`` directory
base_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'base.yml'
))
base_configuration = yaml.load(base_config_file)
site_config_file = open(os.path.join(
    CONFIGURATION_DIR,
    'sites',
    f'site_{site_id}.yml'
))
site_configuration = yaml.load(site_config_file)

# Note that site_configuration overrides base_configuration
configuration = {**base_configuration, **site_configuration}
configuration = ProjectConfiguration(dictionary=configuration)
