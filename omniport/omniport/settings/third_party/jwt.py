"""
This settings file exposes settings for Simple JWT
"""

import datetime as _datetime

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': _datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': _datetime.timedelta(weeks=26),
}
