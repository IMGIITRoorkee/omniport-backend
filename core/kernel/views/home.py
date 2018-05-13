from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class Home(APIView):
    """
    This view shows the app name and description
    """

    def get(self, request, *args, **kwargs):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        site_name = settings.SITE_VERBOSE_NAME
        response = {
            'app': 'kernel',
            'appGroup': 'core',
            'description': f'Handles the core functionality of {site_name}, '
                           'including but not limited to the management of the '
                           'core database and auth',
        }
        return Response(response)
