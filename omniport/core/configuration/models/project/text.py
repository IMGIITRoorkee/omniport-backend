class Text:
    """
    This class stores information about a brand, namely the name, home page and
    acronym
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Text from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')
        self.acronym = dictionary.get('acronym')
        self.home_page = dictionary.get('homePage')
