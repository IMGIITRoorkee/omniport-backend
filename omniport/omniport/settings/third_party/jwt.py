"""
This settings file exposes settings for Simple JWT
"""

import datetime as _datetime

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': _datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': _datetime.timedelta(weeks=26),
}
