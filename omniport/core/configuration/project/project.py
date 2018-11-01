from configuration.project.allowances import IpAddressRing, Allowances
from configuration.project.branding import Branding
from configuration.project.i18n import I18n
from configuration.project.secrets import Secrets
from configuration.project.services import Services
from configuration.project.site import Site


class ProjectConfiguration:
    """
    This class stores configuration for the base project in the form of an
    object, encapsulating load-time checks
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
        self.ip_address_rings = [
            IpAddressRing(
                dictionary=ip_address_ring
            )
            for ip_address_ring in dictionary.get('ipAddressRings')
        ]
        self.allowances = Allowances(
            dictionary=dictionary.get('allowances')
        )
        self.branding = Branding(
            dictionary=dictionary.get('branding')
        )
        self.i18n = I18n(
            dictionary=dictionary.get('i18n')
        )
        self.secrets = Secrets(
            dictionary=dictionary.get('secrets')
        )
        self.services = Services(
            dictionary=dictionary.get('services')
        )
        self.site = Site(
            dictionary=dictionary.get('site')
        )
