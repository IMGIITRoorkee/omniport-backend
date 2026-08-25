"""
This file defines the security options for Omniport
"""

import os

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Response headers, which NGINX must not add a second time
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# The frontend reads its CSRF token from a cookie whose name a deployment can
# choose, because sibling subdomains would otherwise overwrite each other's
# cookie where several Omniports share a parent domain. Django has to write the
# name the frontend reads or every POST is rejected, so both sides take it from
# the environment and the default here stays Django's own.
CSRF_COOKIE_NAME = os.getenv('OMNIPORT_CSRF_COOKIE_NAME', 'csrftoken')
