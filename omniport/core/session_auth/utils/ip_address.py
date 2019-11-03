import requests


def get_location(ip_address):
    """
    Get the location of an IP address
    :param ip_address: the IP address to geo-locate
    :return: the approximate location of the IP address
    """
    try:

        fields = ','.join([
            'status',
            'message',
            'city',
            'country',
            'countryCode',
        ])
        response = requests.get(
            url=f'http://ip-api.com/json/{ip_address}',
            params={'fields': fields},
        )
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
        location = 'The Void'


    return location
