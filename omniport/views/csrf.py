from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator([ensure_csrf_cookie], name='get')
class EnsureCsrf(APIView):
    """
    This view forcefully sets or resets the CSRF cookie on the browser
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
            'data': {
                'type': 'message',
                'attributes': {
                    'text': 'Successfully set CSRF token',
                },
            },
        }
        return Response(response)
