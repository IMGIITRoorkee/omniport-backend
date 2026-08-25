"""
Middleware that keeps an audit trail of the security relevant requests
"""

from django.conf import settings
from django.utils import timezone

from core.utils.logs import get_logging_function
from omniport.constants import (
    ADMIN_NAMESPACE,
    APP_ENTRY_SESSION_KEY,
    AUTHENTICATION_NAMESPACE_SUFFIX,
)

auth_security_log = get_logging_function('auth_security')


class AuditLoggingMiddleware:
    """Log all security-relevant actions"""

    def __init__(self, get_response):
        self.get_response = get_response
        self.namespaces = frozenset(
            configuration.nomenclature.name
            for _, configuration in settings.DISCOVERY.apps
            + settings.DISCOVERY.services
        )

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

        app_name = self.discovered_namespace(request)
        if app_name is not None:
            auth_security_log(
                f'{request.method} {request.get_full_path()} '
                f'returned status {response.status_code}',
                'info',
                user
            )
            if user is not None:
                self.log_app_entry(request, app_name, user)

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

    def discovered_namespace(self, request):
        """
        The discovered app or service that served the request, if any.
        Authentication namespaces are refused because these lines keep the
        query string, which for them carries OAuth codes and tokens
        """

        name = getattr(request.resolver_match, 'app_name', None)
        if name is None or name.endswith(AUTHENTICATION_NAMESPACE_SUFFIX):
            return None
        return name if name in self.namespaces else None

    @staticmethod
    def first_entry_of_the_day(opened, app_name, today):
        """
        Whether this is the session's first request to the app today, which is
        what turns a stream of requests into one record of the app being used
        """

        return opened.get(app_name) != today

    def log_app_entry(self, request, app_name, user):
        """
        Record a session opening an app, skipping the request-per-request
        repetition that would otherwise bury the record it is kept for
        """

        session = getattr(request, 'session', None)
        if session is None or not session.session_key:
            return

        today = timezone.localdate().isoformat()
        opened = session.get(APP_ENTRY_SESSION_KEY, {})
        if not self.first_entry_of_the_day(opened, app_name, today):
            return

        opened[app_name] = today
        session[APP_ENTRY_SESSION_KEY] = opened
        auth_security_log(f'Opened {app_name}', 'info', user)
