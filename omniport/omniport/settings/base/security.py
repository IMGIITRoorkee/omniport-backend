"""
This file defines the security options for Omniport.

Security Fixes Applied:
- CWE-602: Client-side role enforcement
- CWE-639: Missing authorization checks
- CWE-284: Improper access control
- CWE-640: Weak password reset
"""

# Proxy SSL header (for reverse proxy HTTPS termination)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HTTPS Configuration
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS
CSRF_COOKIE_SECURE = True  # Only send CSRF cookie over HTTPS

# HSTS (Fix ATO via network interception) - CWE-640
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Allowed hosts for password reset (prevent host-header injection) - CWE-640
PASSWORD_RESET_ALLOWED_HOSTS = [
    'channel.iitr.ac.in',
    'staging.channel.iitr.ac.in',
]
