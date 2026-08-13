"""
This file defines the security options for Omniport
"""

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Response headers, which SecurityMiddleware and XFrameOptionsMiddleware emit,
# and which NGINX must therefore not add a second time, add_header appending to
# what the portal already sent rather than replacing it
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
