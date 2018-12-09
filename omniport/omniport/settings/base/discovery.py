"""
Omniport is equipped with Discovery. Not going into details, Discovery finds
and populates apps and services in INSTALLED_APPS and their static files in
STATICFILES_DIRS.

This settings file exposes installed apps and the discovery object.
"""

import os

from discovery.discovery import Discovery
from omniport.settings.base.directories import (
    OMNIPORT_DIR,
    APPS_DIR,
    SERVICES_DIR,
)
from omniport.settings.base.shell import SHELL_PRESENT

# Discovery
DISCOVERY = Discovery(SERVICES_DIR, APPS_DIR)
DISCOVERY.discover()

# Application declarations
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

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
    'kernel.apps.KernelConfig',
    'base_auth.apps.BaseAuthConfig',
    'session_auth.apps.SessionAuthConfig',
    'token_auth.apps.TokenAuthConfig',
]
if SHELL_PRESENT:
    INSTALLED_APPS.append('shell.apps.ShellConfig')

DISCOVERY.prepare_installed_apps()
INSTALLED_APPS += DISCOVERY.service_installed_apps
INSTALLED_APPS += DISCOVERY.app_installed_apps

# Static files directories
STATICFILES_DIRS = [
    os.path.join(OMNIPORT_DIR, 'static'),
]

DISCOVERY.prepare_staticfiles_dirs()
STATICFILES_DIRS += DISCOVERY.service_staticfiles_dirs
STATICFILES_DIRS += DISCOVERY.app_staticfiles_dirs

__all__ = [
    'DISCOVERY',
    'INSTALLED_APPS',
    'STATICFILES_DIRS',
]
