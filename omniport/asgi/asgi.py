"""
ASGI config for Omniport.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
    http://channels.readthedocs.io/en/latest/deploying.html
"""

import os

import django
from channels.routing import get_default_application

# Set the Django environment with the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "omniport.settings")

# Since this is not the Django-backed WSGI spec, we need to configure Django
django.setup()

# Return the ASGI application
application = get_default_application()
