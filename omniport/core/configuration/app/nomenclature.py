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
