import base64

from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import AllowAny
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView


class OAuthClientThrottle(SimpleRateThrottle):
    """
    Throttle that counts requests against the client that sends them, and not
    the address, which every user of an application shares
    """

    scope = 'open_auth'

    def get_client_id(self, request):
        header = get_authorization_header(request).split()
        if len(header) == 2 and header[0].lower() == b'basic':
            try:
                return base64.b64decode(header[1]).split(b':')[0].decode()
            except (ValueError, UnicodeDecodeError):
                pass

        # Django caches the form it parses, so the view below still reads it
        return request._request.POST.get('client_id') or self.get_ident(request)

    def get_key(self, request):
        window = int(self.timer()) // self.duration
        return f'throttle_{self.scope}_{self.get_client_id(request)}_{window}'

    def count(self, request):
        # A counter, since the inherited history is read-modify-write and
        # loses increments when workers run concurrently
        key = self.get_key(request)
        try:
            return self.cache.incr(key)
        except ValueError:
            self.cache.add(key, 1, self.duration)
            return 1

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        return self.count(request) <= self.num_requests

    def wait(self):
        return self.duration - (self.timer() % self.duration)


class OAuthFailureThrottle(OAuthClientThrottle):
    """
    Throttle that counts only the requests the wrapped view rejected, so that
    the rate allowed does not have to accommodate how popular a client is
    """

    scope = 'open_auth_failures'

    def allow_request(self, request, view):
        if self.rate is None:
            return True

        # Read only, since the view counts a request once it knows the
        # outcome, which is after every throttle has run
        return (self.cache.get(self.get_key(request)) or 0) < self.num_requests


class ThrottledOAuthLibView(APIView):
    """
    View that runs the DRF throttle stack in front of a django-oauth-toolkit
    view, which is a plain Django view and is otherwise reached without one
    """

    authentication_classes = []
    permission_classes = [AllowAny]
    oauthlib_view = None
    throttle_classes = [OAuthClientThrottle, OAuthFailureThrottle]

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
        response = self.oauthlib_view(request._request, *args, **kwargs)
        if response.status_code >= 400:
            OAuthFailureThrottle().count(request)

        return response
