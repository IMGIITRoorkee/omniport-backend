# Hosts from which a password recovery request is honoured
ALLOWED_PASSWORD_RESET_HOSTS = [
    'channel.iitr.ac.in',
]

# Rate limits, expressed as the number of requests allowed in the window
IP_RATE_LIMIT = 3
ACCOUNT_RATE_LIMIT = 1
RATE_LIMIT_WINDOW = 3600

# Prefixes of the cache keys holding the rate limit counters
IP_RATE_LIMIT_KEY_PREFIX = 'password_reset:ip'
ACCOUNT_RATE_LIMIT_KEY_PREFIX = 'password_reset:account'

# The shortest username that is worth looking up
MINIMUM_USERNAME_LENGTH = 2

# The type of the token sent out in the password recovery email
RECOVERY_TOKEN_TYPE = 'RECOVERY_TOKEN'

# The only message the endpoint ever returns, so that the existence of an
# account cannot be inferred from the response
GENERIC_RECOVERY_MESSAGE = (
    'If an account exists with that username, you will receive a password '
    'recovery email shortly.'
)
