"""
Internationalisation i18n (lowercase i to differentiate it from 1) and
localisation L10n (uppercase L to differentiate it from 1) are used to open
the app to a broader global audience.

Omniport supports and enables both i18n and L10n by default.

This settings file exposes the variables for enabling i18n and L10n.
"""

from omniport.settings.configuration.base import configuration as _conf

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = _conf.i18n.language_code
TIME_ZONE = _conf.i18n.time_zone
