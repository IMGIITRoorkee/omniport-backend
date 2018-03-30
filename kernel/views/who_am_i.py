from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kernel.serialisers.person import PersonSerialiser


class WhoAmI(APIView):
    """
    This view shows some personal information of the currently logged in user
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        person = request.user.person
        serialiser = PersonSerialiser(
            person,
            fields=[
                'full_name',
            ]
        )
        return Response(serialiser.data)
