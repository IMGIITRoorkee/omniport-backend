"""
Omniport overrides the default Django user with a custom user defined in the
kernel. This also implies the use of a generalised authentication backend for
said user.

This setting file exposes variables pertaining to authentication.
"""

AUTH_USER_MODEL = 'base_auth.User'

GUEST_USERNAME = 'Guest User'

AUTHENTICATION_BACKENDS = [
    'base_auth.backends.generalised.GeneralisedAuthBackend',  # Custom backend
    'guardian.backends.ObjectPermissionBackend',  # Django Guardian
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'

SESSION_COOKIE_NAME = 'omniport_session'

OAUTH2_PROVIDER_APPLICATION_MODEL = 'open_auth.Application'
OAUTH2_PROVIDER={
        'REQUEST_APPROVAL_PROMPT':'auto_even_if_expired',
        }
