"""
Security hardening middleware.

Provides response security headers (HSTS, anti-sniff, anti-clickjacking) and
audit logging of authentication/authorization events. Access control itself is
enforced by DRF's default IsAuthenticated permission and per-view permission
classes, not by URL-prefix matching in middleware.
"""

import logging

logger = logging.getLogger('security')


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
