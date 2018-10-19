"""
This setting file maps Django's file variables and similar variables of our own
to various directories defined in the 'directories' setting file.
"""

import os

from omniport.settings.base.directories import (
    OMNIPORT_DIR,
    STATIC_DIR,
    BRANDING_DIR,
    MEDIA_DIR,
    PERSONAL_DIR,
)

# Static files
STATICFILES_DIRS = [
    os.path.join(OMNIPORT_DIR, 'static'),
]
STATIC_URL = '/static/'
STATIC_ROOT = STATIC_DIR

# Branding files
BRANDING_URL = '/branding/'
BRANDING_ROOT = BRANDING_DIR

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

# Personal files
PERSONAL_URL = '/personal/'
PERSONAL_ROOT = PERSONAL_DIR

__all__ = [
    'STATICFILES_DIRS',
    'STATIC_URL',
    'STATIC_ROOT',
    'BRANDING_URL',
    'BRANDING_ROOT',
    'MEDIA_URL',
    'MEDIA_ROOT',
    'PERSONAL_URL',
    'PERSONAL_ROOT',
]