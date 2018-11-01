class IpAddressRing:
    """
    This class stores information about an IP address ring, namely the name and
    patterns
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of IpAddressRing from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')
        self.patterns = dictionary.get('patterns')


class Allowances:
    """
    This class stores information about a site's allowances, namely the hosts,
    apps and IP address rings
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Allowances from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.hosts = dictionary.get('hosts') or ['*']
        self.apps = dictionary.get('apps') or '__all__'
        self.ip_address_rings = dictionary.get('ipAddressRings') or '__all__'
