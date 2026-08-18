from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ThrottledOAuthLibView(APIView):
    """
    View that runs the DRF throttle stack in front of a django-oauth-toolkit
    view, which is a plain Django view and is otherwise reached without one
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    oauthlib_view = None
    throttle_scope = 'open_auth'

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: whatever the wrapped django-oauth-toolkit view returns
        """

        # The toolkit view reads the form body itself, and nothing above has
        # consumed the stream, so hand it the untouched Django request
        return self.oauthlib_view(request._request, *args, **kwargs)
