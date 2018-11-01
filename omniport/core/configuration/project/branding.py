class Brand:
    """
    This class stores information about a brand, namely the name and home page
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Brand from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.acronym = dictionary.get('acronym')
        self.name = dictionary.get('name')
        self.home_page = dictionary.get('homePage')


class Institute(Brand):
    """
    This class stores information about the institute brand
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)


class Maintainers(Brand):
    """
    This class stores information about the maintainers brand
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)


class Branding:
    """
    This class stores the Branding objects for all the brands involved
    """

    def __init__(self, *args, **kwargs):
        """
        Create instances of individual brand classes
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.institute = Institute(
            dictionary=dictionary.get('institute')
        )
        self.maintainers = Maintainers(
            dictionary=dictionary.get('maintainers')
        )
