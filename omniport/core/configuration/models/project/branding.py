from configuration.models.project.text import Text


class Brand:
    """
    This class stores information about a brand
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Brand from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        dictionary = kwargs.get('dictionary') or dict()
        self.text = Text(
            dictionary=dictionary
        )

        # Processed variables
        self.imagery = None


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

        dictionary = kwargs.get('dictionary') or dict()
        self.institute = Institute(
            dictionary=dictionary.get('institute')
        )
        self.maintainers = Maintainers(
            dictionary=dictionary.get('maintainers')
        )
