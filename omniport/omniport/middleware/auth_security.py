"""
Security middleware for authentication and authorization.

Fixes:
- CWE-602: Client-side role enforcement
- CWE-284: Improper access control (Guest sessions)
- CWE-639: Missing authorization checks
"""

import logging
from django.http import JsonResponse

logger = logging.getLogger('security')

# Endpoints that require authentication (not accessible to Guest)
PROTECTED_ENDPOINTS = [
    '/api/people/',
    '/api/stats/',
    '/api/filemanager/',
    '/api/marketplace/',
    '/api/noticeboard/new/',
    '/api/lectures/',
    '/api/groups/',
    '/api/lost_and_found/',
]

# Endpoints accessible to unauthenticated users
PUBLIC_ENDPOINTS = [
    '/api/auth/',
    '/api/base_auth/',
    '/api/public/',
]


class SecurityHeadersMiddleware:
    """Add HSTS and other security headers to all responses"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # HSTS (fix ATO via network interception)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        # Prevent MIME sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'

        # XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response


class GuestSessionBlockerMiddleware:
    """
    Block Guest sessions from accessing protected endpoints.
    Fixes CWE-284: Improper Access Control
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is Guest
        if self.is_guest_user(request):
            # Check if trying to access protected endpoint
            if self.is_protected_endpoint(request.path):
                logger.warning(
                    f"[SECURITY] Guest access blocked: path={request.path} ip={request.source_ip_address}"
                )
                return JsonResponse(
                    {'error': 'Authentication required'},
                    status=401
                )

        response = self.get_response(request)
        return response

    @staticmethod
    def is_guest_user(request):
        """Check if user is Guest"""
        if request.user.is_anonymous:
            return True
        # Check if this is a guest session
        is_guest = getattr(request.user, 'is_guest', False)
        username_is_guest = request.user.username == 'Guest User'
        return is_guest or username_is_guest

    @staticmethod
    def is_protected_endpoint(path):
        """Check if path requires authentication"""
        # Check protected list first
        for protected in PROTECTED_ENDPOINTS:
            if path.startswith(protected):
                return True

        # Override: some protected paths are public
        for public in PUBLIC_ENDPOINTS:
            if path.startswith(public):
                return False

        return path.startswith('/api/') and '/auth/' not in path and '/public/' not in path


class AuditLoggingMiddleware:
    """Log all security-relevant actions"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log auth failures
        if response.status_code in [401, 403]:
            user_id = request.user.id if not request.user.is_anonymous else 'anonymous'
            logger.warning(
                f"[AUDIT] Authorization failed: "
                f"user={user_id} path={request.path} method={request.method} status={response.status_code}"
            )

        # Log sensitive operations
        if any(x in request.path for x in ['/password', '/auth/', '/admin']):
            user_id = request.user.id if not request.user.is_anonymous else 'anonymous'
            logger.info(
                f"[AUDIT] Sensitive operation: "
                f"user={user_id} path={request.path} method={request.method} status={response.status_code}"
            )

        return response
