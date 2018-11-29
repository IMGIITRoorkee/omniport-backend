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
