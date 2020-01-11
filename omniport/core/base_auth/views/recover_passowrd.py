from rest_framework import generics, response, status

from base_auth.models import User
from base_auth.managers.get_user import get_user
from omniport.utils import switcher
from omniport.settings.configuration.base import CONFIGURATION
from formula_one.utils.verification_token import send_token, verify_access_token, delete
from session_auth.models import SessionMap
from categories.models import Category

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class RecoverPassword(generics.GenericAPIView):
    """
    This view when responding to a GET request, generates password recovery token
    and sends mail to the concerned user.
    """

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request this is to be responded to
        :return: the response for request
        """

        username = request.GET.get('username', None)

        if not username:
            return response.Response(
                data="Please provide the username",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = get_user(username)
        except User.DoesNotExist:
            return response.Response(
                data="The username provided is incorrect",
                status=status.HTTP_400_BAD_REQUEST
            )
        person = user.person

        site_name = CONFIGURATION.site.nomenclature.verbose_name
        site_url = CONFIGURATION.allowances.hosts[0]

        url = f'https://{site_url}/auth/reset_password/?token=recovery_token'
        subject = f'{site_name} account password reset'
        body = f'To reset your {site_name} account password, please visit url'
        category, _ = Category.objects.get_or_create(name="Auth", slug="auth")

        send_token(
            user_id=user.id,
            person_id=person.id,
            token_type="RECOVERY_TOKEN",
            email_body=body,
            email_subject=subject,
            url=url,
            category=category
        )

        return response.Response(
            data="Email sent successfully",
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

        if not user or ("RECOVERY_TOKEN" != token_data['token_type']):
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
        username = request.data.get('username', None)
        new_password = request.data.get('new_password', None)
        remove_all_sessions = request.data.get('remove_all_sessions', False)

        try:
            user = User.objects.get(id=token_data['user_id'])
        except User.DoesNotExist:
            return response.Response(
                data='User corresponding to this token does not exist',
                status=status.HTTP_400_BAD_REQUEST,
            )

        if username != user.username:
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
            data="Successfully reset password.",
            status=status.HTTP_200_OK,
        )
