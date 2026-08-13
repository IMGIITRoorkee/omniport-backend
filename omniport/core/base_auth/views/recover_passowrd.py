import swapper
from django.core.cache import cache
from rest_framework import generics, response, status

from base_auth.constants.password_recovery import (
    ACCOUNT_RATE_LIMIT,
    ACCOUNT_RATE_LIMIT_KEY_PREFIX,
    ACCOUNT_RATE_LIMIT_WINDOW,
    GENERIC_RECOVERY_MESSAGE,
    IP_RATE_LIMIT,
    IP_RATE_LIMIT_KEY_PREFIX,
    IP_RATE_LIMIT_WINDOW,
    MINIMUM_USERNAME_LENGTH,
    RECOVERY_TOKEN_TYPE,
)
from base_auth.models import User
from base_auth.managers.get_user import get_user
from core.utils.logs import get_logging_function
from omniport.utils import switcher
from omniport.settings.configuration.base import CONFIGURATION
from formula_one.utils.verification_token import send_token, verify_access_token, delete
from session_auth.models import SessionMap
from categories.models import Category

base_auth_log = get_logging_function('base_auth')
AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


def rate_limit_check(key, limit=IP_RATE_LIMIT, window=IP_RATE_LIMIT_WINDOW):
    """
    Fixed window counter, allowing `limit` hits on `key` per `window` seconds
    """

    current = cache.get(key, 0)
    if current >= limit:
        return False
    cache.set(key, current + 1, timeout=window)
    return True


class RecoverPassword(generics.GenericAPIView):
    """
    Password recovery endpoint, rate limited per IP and per account, which
    responds identically whether or not the account exists
    """

    def get(self, request):
        """
        View to serve GET requests, deprecated in favour of POST and retained
        only until the frontends have moved off it
        """

        base_auth_log(
            'Password recovery requested over the deprecated GET route',
            'warning'
        )

        return self.recover(request, request.GET.get('username'))

    def post(self, request):
        """
        View to serve POST requests
        """

        return self.recover(request, request.data.get('username'))

    def recover(self, request, username):
        """
        Send a recovery token to the named account, if it exists
        """

        username = (username or '').strip()

        # Get client IP for rate limiting
        ip_address = request.source_ip_address

        # Rate limit by IP
        ip_key = f'{IP_RATE_LIMIT_KEY_PREFIX}:{ip_address}'
        if not rate_limit_check(ip_key, IP_RATE_LIMIT, IP_RATE_LIMIT_WINDOW):
            base_auth_log(
                f'Password recovery rate limit exceeded by IP {ip_address}',
                'warning'
            )
            return response.Response(
                data={'message': GENERIC_RECOVERY_MESSAGE},
                status=status.HTTP_200_OK
            )

        # Validate input
        if not username or len(username) < MINIMUM_USERNAME_LENGTH:
            base_auth_log(
                'Password recovery attempted with a malformed username',
                'warning'
            )
            return response.Response(
                data={'message': GENERIC_RECOVERY_MESSAGE},
                status=status.HTTP_200_OK
            )

        # Try to find user
        user = None
        try:
            user = get_user(username)
        except User.DoesNotExist:
            pass

        if user:
            # Rate limit by account
            account_key = f'{ACCOUNT_RATE_LIMIT_KEY_PREFIX}:{user.id}'
            if not rate_limit_check(
                account_key, ACCOUNT_RATE_LIMIT, ACCOUNT_RATE_LIMIT_WINDOW
            ):
                base_auth_log(
                    'Password recovery rate limit exceeded on the account',
                    'warning',
                    user
                )
                return response.Response(
                    data={'message': GENERIC_RECOVERY_MESSAGE},
                    status=status.HTTP_200_OK
                )

            try:
                person = user.person
                site_name = CONFIGURATION.site.nomenclature.verbose_name
                site_url = CONFIGURATION.allowances.hosts[0]

                token_type = RECOVERY_TOKEN_TYPE
                url = f'https://{site_url}/auth/reset_password/?token={token_type}'
                subject = f'{site_name} account password reset'
                body = f'To reset your {site_name} account password, please visit url'
                category, _ = Category.objects.get_or_create(name="Auth", slug="auth")

                send_token(
                    user_id=user.id,
                    person_id=person.id,
                    token_type=token_type,
                    email_body=body,
                    email_subject=subject,
                    url=url,
                    category=category
                )

                base_auth_log('Password recovery email sent', 'info', user)

            except Exception as e:
                base_auth_log(
                    f'Could not send the password recovery email: {e}',
                    'error',
                    user
                )

        # The same response either way, so that accounts cannot be enumerated
        return response.Response(
            data={'message': GENERIC_RECOVERY_MESSAGE},
            status=status.HTTP_200_OK,
        )


class VerifyRecoveryToken(generics.GenericAPIView):

    @verify_access_token
    def get(self, request, *args):
        """
        This view serves GET request, and returns the username of the user
        if recovery token exists and error otherwise.
        :param request: the request that is being responded to
        :return: the response to the request.
        """

        token_data = args[0]
        user = User.objects.get(id=token_data['user_id'])

        if not user or (RECOVERY_TOKEN_TYPE != token_data['token_type']):
            return response.Response(
                data="Incorrect token type",
                status=status.HTTP_404_NOT_FOUND,
            )

        person = user.person
        response_data = AvatarSerializer(person).data

        return response.Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )

    @verify_access_token
    def post(self, request, *args):
        """
        View to serve POST requests
        :param request: the request this is to be responded to
        :return: the response for request
        """

        token_data, recovery_token = args[:2]
        person_id = request.data.get('person_id', None)
        new_password = request.data.get('new_password', None)
        remove_all_sessions = request.data.get('remove_all_sessions', False)

        Person = swapper.load_model('kernel', 'Person')
        try:
            person = Person.objects.get(id=person_id)
            user = User.objects.get(id=token_data['user_id'])
        except (User.DoesNotExist, Person.DoesNotExist):
            return response.Response(
                data='User corresponding to this token does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if person.user.id != user.id:
            return response.Response(
                data='The username provided is incorrect',
                status=status.HTTP_403_FORBIDDEN,
            )
        if not new_password:
            return response.Response(
                data='Please provide new password',
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        # Delete the recovery token once it is used.
        delete(recovery_token)

        if remove_all_sessions:
            SessionMap.objects.filter(user=user).delete()

        return response.Response(
            data='Successfully reset password.',
            status=status.HTTP_200_OK,
        )
