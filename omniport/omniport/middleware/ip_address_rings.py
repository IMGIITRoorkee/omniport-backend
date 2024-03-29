import re

from django.conf import settings
from django.http import HttpResponseForbidden


class IpAddressRings:
    """
    Set the network_ring attribute on the request object based on the IP from
    which the request was made
    """

    def __init__(self, get_response):
        """
        Write the __init__ function exactly as the Django documentations says
        """

        self.get_response = get_response

    def __call__(self, request):
        """
        Perform the actual processing on the request before it goes to the view
        and on the response returned by the view
        :param request: the request being processed
        :return: the processed response
        """

        # The headers to read in order of preference
        real_ip_header = 'HTTP_X_REAL_IP'
        forwarded_for_header = 'HTTP_X_FORWARDED_FOR'
        remote_addr = 'REMOTE_ADDR'

        # The IP address is extracted from the right header
        # The right header depends on whether the request was proxied by NGINX
        ip_address = request.META.get(
            real_ip_header,
            request.META.get(
                forwarded_for_header,
                request.META.get(
                    remote_addr,
                    'Not Found'
                )
            )
        )
        request.source_ip_address = ip_address

        ip_address_rings = settings.IP_ADDRESS_RINGS
        allowed_ip_address_rings = settings.ALLOWED_IP_ADDRESS_RINGS

        request.ip_address_rings = list()
        for ring in allowed_ip_address_rings:
            patterns = ip_address_rings[ring]
            if re.fullmatch('|'.join(patterns), ip_address):
                request.ip_address_rings.append(ring)
        if not len(request.ip_address_rings):
            return HttpResponseForbidden()

        response = self.get_response(request)

        return response
