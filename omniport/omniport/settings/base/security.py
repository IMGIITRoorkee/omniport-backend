"""
This file defines the security options for Omniport
"""

import os

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Response headers, which NGINX must not add a second time
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# getCookie in formula_one rewrites 'csrftoken' to a deployment-specific name
# on deployments that run more than one Omniport under one parent domain, since
# sibling subdomains would otherwise overwrite each other's cookie. Django has
# to write whichever name the frontend reads or every POST is rejected, so both
# sides take it from the environment and the default stays Django's own.
CSRF_COOKIE_NAME = os.getenv('OMNIPORT_CSRF_COOKIE_NAME', 'csrftoken')
