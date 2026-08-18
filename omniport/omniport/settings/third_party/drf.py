"""
This settings file exposes settings for Django REST framework
"""

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.PageNumberPagination'  # No commas
    ),
    'PAGE_SIZE': 10,
    # ScopedRateThrottle only applies to views that declare a throttle_scope
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        # A floor above real browsing, which costs 23 requests per page mount.
        # Views serving bulk personal data need their own throttle_scope
        'anon': '2000/hour',
        'user': '5000/hour',
        'login': '300/hour',
        'reset_password': '5/hour',
        'verify_secret_answer': '5/hour',
        'verify_recovery_token': '10/hour',
    },
    # NGINX appends the peer address to X-Forwarded-For, making the last entry
    # the only one a client cannot forge to mint itself a fresh throttle bucket
    'NUM_PROXIES': 1,
}
