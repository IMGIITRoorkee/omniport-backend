"""
WSGI config for Omniport.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the Django environment with the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omniport.settings")

# Return the WSGI application
application = get_wsgi_application()
