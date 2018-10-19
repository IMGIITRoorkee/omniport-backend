"""
Omniport serves two application entry points namely a WSGI entry point served
by Gunicorn and an ASGI entry point served by Daphne.

This setting file exposes these two application paths.
"""

# WSGI application served by Gunicorn
WSGI_APPLICATION = 'omniport.wsgi.application'

# ASGI application served by Daphne
ASGI_APPLICATION = 'omniport.routing.application'
