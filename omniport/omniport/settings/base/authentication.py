"""
Omniport overrides the default Django user with a custom user defined in the
kernel. This also implies the use of a generalised authentication backend for
said user.

This setting file exposes variables pertaining to authentication.
"""

AUTH_USER_MODEL = 'kernel.User'

AUTHENTICATION_BACKENDS = [
    'kernel.auth_backends.generalised.GeneralisedAuthBackend',
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

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'session'

SESSION_COOKIE_NAME = 'omniport_session'
