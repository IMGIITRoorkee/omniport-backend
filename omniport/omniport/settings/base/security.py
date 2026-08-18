"""
This file defines the security options for Omniport
"""

import os

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Response headers, which NGINX must not add a second time
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# getCookie in formula_one rewrites 'csrftoken' to a deployment-specific name,
# so Django has to write the same one or every POST is rejected. The default
# here matches the bundle deployed on stage and belongs back at 'csrftoken'
# before this goes upstream, with the real value coming from the environment.
CSRF_COOKIE_NAME = os.getenv(
    'OMNIPORT_CSRF_COOKIE_NAME', 'omniport_stage_csrftoken'
)
