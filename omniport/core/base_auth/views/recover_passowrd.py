from rest_framework import generics, response, status

from base_auth.models import User
from omniport.utils import switcher
from formula_one.utils.create_token import create_token_send_mail, verify_access_token
from session_auth.models import SessionMap
from categories.models import Category

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class RecoverPassword(generics.GenericAPIView):
    """
    This view when responding to a GET request, generates password recovery token
    and sends mail to the concerned user. and when responding to a POST request
    changes the password of the user.
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

        user = User.objects.get(username=username)
        person = user.person

        url = f"http://localhost.com/"
        subject = "Channel-i account password reset"
        body = f'For changing your account password please visit: '
        category = Category.objects.get(name="testCat")

        create_token_send_mail(user_id=user.id,
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

        if not user or \
                ("RECOVERY_TOKEN" != token_data['token_type']):
            return response.Response(
                data="Incorrect Token Type",
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

        token_data = args[0]
        username = request.data.get('username', None)
        new_password = request.data.get('new_password', None)
        checked = request.data.get('checked', True)

        user = User.objects.get(id=token_data['user_id'])

        if not user or \
                ("RECOVERY_TOKEN" != token_data['token_type']):
            return response.Response(
                data="This recovery token is  wrong",
                status=status.HTTP_404_NOT_FOUND,
            )
        if username != user.username:
            return response.Response(
                data="The username provided is incorrect",
                status=status.HTTP_403_FORBIDDEN,
            )
        if not new_password:
            return response.Response(
                data="Please provide new Password",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        #        delete(recovery_token)

        if checked:
            SessionMap.objects.filter(user=user).delete()

        return response.Response(
            data="Successfully reset password.",
            status=status.HTTP_200_OK,
        )