"""
Omniport is equipped with Discovery. Not going into details, Discovery finds
and populates services in INSTALLED_APPS.

This settings file exposes installed apps and the discovery object.
"""

from discovery.discovery import Discovery
from omniport.settings.base.directories import APPS_DIR, SERVICES_DIR
from omniport.settings.base.shell import SHELL_PRESENT

# Application declarations
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # PyPI packages
    'channels',  # HTTP/2.0 and sockets support

    'rest_framework',  # JSON-based APIs in Django
    'crispy_forms',  # Reusable forms used by DRF
    'guardian',  # Object permissions for DRF
    'django_filters',  # Dynamic queryset filtering in DRF

    'corsheaders',  # Handles CORS headers on responses
    'django_countries',  # Country fields and widgets (with little flags!)
    'mptt',  # Infinite nesting of objects of the same model
    'tinymce',  # Rich text editor

    # Core apps
    'kernel',
    'session_auth',
    'token_auth',
]

# If shell is present, add to INSTALLED_APPS
if SHELL_PRESENT:
    INSTALLED_APPS.append(
        'shell.apps.ShellConfig',
    )

# Discovery
DISCOVERY = Discovery(SERVICES_DIR, APPS_DIR)
DISCOVERY.discover()

DISCOVERY.prepare_installed_apps()
INSTALLED_APPS += DISCOVERY.service_installed_apps
INSTALLED_APPS += DISCOVERY.app_installed_apps

__all__ = [
    'INSTALLED_APPS',
    'DISCOVERY',
]
