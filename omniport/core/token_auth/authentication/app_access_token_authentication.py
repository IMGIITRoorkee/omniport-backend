import re

from rest_framework import authentication
from rest_framework import exceptions

from token_auth.models import AppAccessToken
from token_auth.constants import HTTP_X_ACCESS_TOKEN

class AppAccessTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get(HTTP_X_ACCESS_TOKEN)
        ip_address = request.source_ip_address

        if access_token and ip_address:
            try:
                app_access_token = AppAccessToken.objects.get(
                    access_token=access_token
                )
                allowed_ip_address_regex = app_access_token.ip_address_regex
                if re.search(allowed_ip_address_regex, ip_address):
                    return (app_access_token, None)
                else:
                    raise exceptions.AuthenticationFailed('Request not allowed from' \
                       ' this IP address. This event will be logged.'
                    )
            except AppAccessToken.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such app access token')
            except Exception as exception:
                raise exception

        return None
