import re

from django.conf import settings


class NetworkRings:
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

        network_rings = settings.NETWORK_RINGS
        ip_address_patterns = settings.IP_ADDRESS_PATTERNS

        for ring in network_rings:
            patterns = ip_address_patterns[ring]
            if re.search('|'.join(patterns), ip_address):
                request.network_ring = ring
                break
        else:
            request.network_ring = network_rings[-1]

        response = self.get_response(request)

        return response
