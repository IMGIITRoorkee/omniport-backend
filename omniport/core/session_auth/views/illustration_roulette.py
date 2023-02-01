from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class IllustrationRoulette(GenericAPIView):
    """
    Return the number of available illustrations to choose from
    """

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        response = {
            'count': 5
        }

        return Response(response, status=HTTP_200_OK)
