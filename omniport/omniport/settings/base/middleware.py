"""
Omniport relies on a whole bunch of middleware for pre- and post-view
processing, including Django middleware, third-party middleware and self-written
middleware.

This settings file exposes the middleware employed in the project.
"""

MIDDLEWARE = [
    # Outermost, so that the headers are set on every response, including the
    # ones the middleware below return without ever reaching a view
    'omniport.middleware.auth_security.SecurityHeadersMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'omniport.middleware.drf_auth.DrfAuth',

    # Below DrfAuth, so that the user is known, and above the middleware that
    # deny requests outright, so that their denials are audited
    'omniport.middleware.auth_security.AuditLoggingMiddleware',

    'omniport.middleware.ip_address_rings.IpAddressRings',
    'omniport.middleware.routes_control.RoutesControl',
    'omniport.middleware.person_roles.PersonRoles',
    'omniport.middleware.last_seen.LastSeen',
    'omniport.middleware.routes_control_roles.RoutesControlRoles',

    'omniport.middleware.auth_security.GuestSessionBlockerMiddleware',
]
