"""
Middleware that keeps an audit trail of the security relevant requests
"""

from core.utils.logs import get_logging_function

auth_security_log = get_logging_function('auth_security')

# The suffix shared by the URL namespaces of the authentication apps, every one
# of which is worth an audit record. Matching on the namespace rather than on
# the path keeps this working as apps are added and as they are mounted
# elsewhere, which the admin site in particular is
AUTHENTICATION_NAMESPACE_SUFFIX = '_auth'
ADMIN_NAMESPACE = 'admin'


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
