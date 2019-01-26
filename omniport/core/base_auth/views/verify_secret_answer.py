from rest_framework import status, generics, response

from base_auth.serializers.retrieve_user import (
    RetrieveUserSerializer,
)
from base_auth.serializers.verify_secret_answer import (
    VerifySecretAnswerSerializer,
)


class VerifySecretAnswer(generics.GenericAPIView):
    """
    This view, when responding to a GET request, shows the secret question for
    the user in question and, when responding to a POST request, takes the
    username, the secret_answer and the new password to reset it
    """

    serializer_class = VerifySecretAnswerSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = RetrieveUserSerializer(data=request.query_params)
        if serializer.is_valid():
            user = serializer.user
            secret_question = user.secret_question
            response_data = {
                'secret_question': secret_question,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response_data = {
                'status': 'Correct answer submitted.',
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_200_OK
            )
        else:
            response_data = {
                'errors': serializer.errors,
            }
            return response.Response(
                data=response_data,
                status=status.HTTP_400_BAD_REQUEST
            )
