from configuration.models.app.acceptables import Acceptables
from configuration.models.app.base_urls import BaseUrls
from configuration.models.app.nomenclature import Nomenclature


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

        self.nomenclature = Nomenclature(
            dictionary=dictionary.get('nomenclature')
        )
        self.is_api = dictionary.get('isApi') or False
        self.description = dictionary.get('description')
        self.base_urls = BaseUrls(
            dictionary=dictionary.get('baseUrls')
        )
        self.acceptables = Acceptables(
            dictionary=dictionary.get('acceptables')
        )

        # Processed variables
        self.is_allowed = None
        self.has_static = None
        self.assets = None
