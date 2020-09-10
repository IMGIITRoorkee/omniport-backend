from configuration.models.project.allowances import Allowances
from configuration.models.project.branding import Branding
from configuration.models.project.i18n import I18n
from configuration.models.project.ip_address_ring import IpAddressRing
from configuration.models.project.secrets import Secrets
from configuration.models.project.emails import Emails
from configuration.models.project.services import Services
from configuration.models.project.site import Site

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
        server = kwargs.get('server') or 'server'

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
        self.emails = Emails(
            dictionary=dictionary.get('emails')
        )
        self.services = Services(
            dictionary=dictionary.get('services')
        )
        self.site = Site(
            dictionary=dictionary.get('site')
        )
        self.integrations = dictionary.get('integrations')
        self.server = server
