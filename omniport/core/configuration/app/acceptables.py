class Acceptables:
    """
    This class stores information about an app's acceptables, namely the
    acceptable roles and the acceptable IP address rings
    """

    def __init__(self, *args, **kwargs):
        """
        Create an Acceptables instance from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.roles = dictionary.get('roles')
        self.ip_address_rings = dictionary.get('ipAddressRings')
