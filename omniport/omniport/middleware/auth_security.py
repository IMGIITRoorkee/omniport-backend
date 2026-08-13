"""
Security middleware for authentication and authorization.

Fixes:
- CWE-602: Client-side role enforcement
- CWE-284: Improper access control (Guest sessions)
- CWE-639: Missing authorization checks
"""

from django.http import JsonResponse

from core.utils.logs import get_logging_function

auth_security_log = get_logging_function('auth_security')

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

# The suffix shared by the URL namespaces of the authentication apps, every one
# of which is worth an audit record. Matching on the namespace rather than on
# the path keeps this working as apps are added and as they are mounted
# elsewhere, which the admin site in particular is
AUTHENTICATION_NAMESPACE_SUFFIX = '_auth'
ADMIN_NAMESPACE = 'admin'


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
                auth_security_log(
                    f'Guest access blocked on {request.path} '
                    f'from {request.source_ip_address}',
                    'warning'
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

        user = None if request.user.is_anonymous else request.user

        # Log auth failures
        if response.status_code in [401, 403]:
            auth_security_log(
                f'Authorisation failed on {request.method} {request.path} '
                f'with status {response.status_code}',
                'warning',
                user
            )

        # Log sensitive operations
        if self.is_sensitive_operation(request):
            auth_security_log(
                f'Sensitive operation {request.method} {request.path} '
                f'returned status {response.status_code}',
                'info',
                user
            )

        return response

    @staticmethod
    def is_sensitive_operation(request):
        """
        Whether the view that served the request came from an authentication
        app or from the admin site
        """

        resolver_match = request.resolver_match
        if resolver_match is None:
            return False

        app_name = resolver_match.app_name
        return (
            app_name.endswith(AUTHENTICATION_NAMESPACE_SUFFIX)
            or app_name == ADMIN_NAMESPACE
        )
