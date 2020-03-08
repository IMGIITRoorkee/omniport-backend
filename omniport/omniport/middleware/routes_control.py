import re

from django.conf import settings
from django.http import Http404, HttpResponseForbidden

from discovery.available import from_acceptable_ring


class RoutesControl:
    """
    Handle routing of specialised internal features that are to be
    restricted under certain IP rings
    """

    def __init__(self, get_response):
        """
        __init__ function exactly as the Django documentations says for
        a custom middleware
        """
        self.get_response = get_response

        default_restrictions = [
            (settings.ADMIN_SITE_URL, 'administrator'),
        ]

        self.restrictions = default_restrictions

    def __call__(self, request):
        """
        Perform the actual processing on the request before it goes to the view
        and on the response returned by the view
        :param request: the request being processed
        :return: the processed response
        """

        source_address = request.source_ip_address
        DISCOVERY = settings.DISCOVERY

        for site_path, ip_address_ring_name in self.restrictions:
            ip_patterns = settings.IP_ADDRESS_RINGS.get(ip_address_ring_name)
            base = site_path.strip('/')
            if re.match(f'^/{base}/', request.path) and \
                    not re.search('|'.join(ip_patterns), source_address):
                raise Http404

        response = self.get_response(request)


        for app, app_configuration in DISCOVERY.apps:
            base_url  = app_configuration.base_urls.http.strip('/')
            if not re.math(f'^/{base_url}/', request.path):
                continue
            if not from_acceptable_ring(
                    source_address,
                    app_configuration.acceptables.ip_address_rings
                ):
                return HttpResponseForbidden()

        return response
