import requests
import logging


def get_location(ip_address):
    """
    Get the location of an IP address
    :param ip_address: the IP address to geo-locate
    :return: the approximate location of the IP address
    """
    
    fields = ','.join([
        'status',
        'message',
        'city',
        'country',
        'countryCode',
    ])
    try:
        response = requests.get(
            url=f'http://ip-api.com/json/{ip_address}',
            params={'fields': fields},
        )
        response = None

        response = response.json()
        if response.pop('status') == 'success':
            location = ', '.join([
                response.get('city'),
                response.get('country'),
                response.get('countryCode'),
            ])
        else:
            if response.get('message') == 'private range':
                location = 'Intranet'
            elif response.get('message') == 'reserved range':
                location = 'Reserved'
            else:
                location = 'The Void'
    except requests.ConnectionError:
        logger = logging.getLogger('django')
        logger.error(f'Connection refused by http://ip-api.com/json/{ip_address}')
        location = 'The Void'

    return location
