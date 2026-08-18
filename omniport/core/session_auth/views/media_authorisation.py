from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView


class MediaAuthorisation(APIView):
    """
    Authorisation endpoint for nginx ``auth_request``. It gates protected static
    files (media, personal files) that nginx would otherwise serve directly with
    no access control, exposing institute PII to unauthenticated callers.

    nginx issues an internal sub-request here before serving a protected file
    and serves the file only on a 2xx response. Authenticated callers receive
    200; unauthenticated callers are rejected by the IsAuthenticated permission,
    so nginx denies the file.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'media_authorisation'

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: an empty 200 response for authenticated callers
        """

        return Response(status=HTTP_200_OK)
