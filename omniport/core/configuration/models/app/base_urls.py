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
        self.static = dictionary.get('static')
