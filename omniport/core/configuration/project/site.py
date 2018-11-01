class Site:
    """
    This class stores information about a site, namely the ID, code name and
    verbose name
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Site from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.id = dictionary.get('id') or 0
        self.name = dictionary.get('name') or 'omniport'
        self.verbose_name = dictionary.get('verboseName') or 'Omniport'
        self.debug = dictionary.get('debug') or False
