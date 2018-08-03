class Nomenclature:
    """
    This class stores information about an app's nomenclature, namely the code
    name and verbose name
    """

    def __init__(self, *args, **kwargs):
        """
        Create a Nomenclature instance, from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')
        self.verbose_name = dictionary.get('verboseName')


class BaseUrls:
    """
    This class stores information about an app's URL dispatcher configuration,
    namely the base URLs for http and ws protocols
    """

    def __init__(self, *args, **kwargs):
        """
        Create a BaseUrls instance from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.http = dictionary.get('http')
        self.ws = dictionary.get('ws')
        self.is_api = dictionary.get('isApi') or False


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


class AppConfiguration:
    """
    This class stores configuration for an app in the form of an object,
    encapsulating load-time checks
    """

    def __init__(self, *args, **kwargs):
        """
        Parse the dictionaries generated from YAML files into a class-object
        representation
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.is_allowed = None
        self.nomenclature = Nomenclature(
            dictionary=dictionary.get('nomenclature')
        )
        self.base_urls = BaseUrls(
            dictionary=dictionary.get('baseUrls')
        )
        self.acceptables = Acceptables(
            dictionary=dictionary.get('acceptables')
        )
