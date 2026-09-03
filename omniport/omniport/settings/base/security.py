"""
This file defines the security options for Omniport
"""

import os

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Response headers, which NGINX must not add a second time
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Named per deployment, so sibling subdomains sharing a parent domain do not
# overwrite each other's. The frontend must read the same variable
CSRF_COOKIE_NAME = os.getenv('OMNIPORT_CSRF_COOKIE_NAME', 'csrftoken')
