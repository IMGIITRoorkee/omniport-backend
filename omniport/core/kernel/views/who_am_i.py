from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kernel.serializers.person import PersonSerializer


class WhoAmI(GenericAPIView):
    """
    This view shows some personal information of the currently logged in user
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        person = request.person
        serializer = self.get_serializer_class()(
            person,
            fields=[
                'full_name',
            ]
        )
        return Response(serializer.data)
