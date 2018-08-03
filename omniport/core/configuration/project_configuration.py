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


class I18n:
    """
    This class stores the information about the internationalisation of the
    project, namely the language code and time zone
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of I18n from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.language_code = dictionary.get('languageCode') or 'en-gb'
        self.time_zone = dictionary.get('timeZone') or 'Asia/Kolkata'


class Service:
    """
    This class stores information about a service, namely the host and port
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Service from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.host = dictionary.get('host')
        self.port = dictionary.get('port')


class AuthenticationMixin:
    """
    This mixin stores information about the authentication credentials of a
    service, namely the username and password
    """

    def __init__(self, *args, **kwargs):
        """
        Populate the user and password from the dictionary, and then defer to
        the parent class
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__(*args, **kwargs)

        dictionary = kwargs.get('dictionary') or dict()
        self.user = dictionary.get('user')
        self.password = dictionary.get('password')


class Database(AuthenticationMixin, Service):
    """
    This class stores information about the database service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base classes to populate the data points and then populate
        the name
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__(*args, **kwargs)

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')


class MessageBroker(AuthenticationMixin, Service):
    """
    This class stores information about the message broker service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)


class ChannelLayer(Service):
    """
    This class stores information about the channel layer service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)


class SessionStore(Service):
    """
    This class stores information about the session store service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)


class Services:
    """
    This class stores the Service objects for all the services involved
    """

    def __init__(self, *args, **kwargs):
        """
        Create instances of individual service objects
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.database = Database(
            dictionary=dictionary.get('database')
        )
        self.channel_layer = ChannelLayer(
            dictionary=dictionary.get('channelLayer')
        )
        self.session_store = SessionStore(
            dictionary=dictionary.get('sessionStore')
        )
        self.message_broker = MessageBroker(
            dictionary=dictionary.get('messageBroker')
        )


class IpAddressRing:
    """
    This class stores information about an IP address ring, namely the name and
    patterns
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of IpAddressRing from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')
        self.patterns = dictionary.get('patterns')


class Cors:
    """
    This class stores information about CORS, namely origin whitelist,
    whether credentials are allowed and whether all origins are allowed
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Cors from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.allow_credentials = dictionary.get('allowCredentials') or False
        self.origin_whitelist = dictionary.get('originWhitelist') or list()
        self.origin_allow_all = dictionary.get('originAllowAll') or False


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


class Allowances:
    """
    This class stores information about a site's allowances, namely the hosts,
    apps and IP address rings
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Allowances from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.hosts = dictionary.get('hosts') or ['*']
        self.apps = dictionary.get('apps') or '__all__'
        self.ip_address_rings = dictionary.get('ipAddressRings') or '__all__'


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
        self.branding = Branding(
            dictionary=dictionary.get('branding')
        )
        self.i18n = I18n(
            dictionary=dictionary.get('i18n')
        )
        self.secret_key = dictionary.get('secretKey')
        self.services = Services(
            dictionary=dictionary.get('services')
        )
        self.ip_address_rings = [
            IpAddressRing(dictionary=ip_address_ring)
            for ip_address_ring in dictionary.get('ipAddressRings')
        ]
        self.site = Site(
            dictionary=dictionary.get('site')
        )
        self.cors = Cors(
            dictionary=dictionary.get('cors')
        )
        self.debug = dictionary.get('debug') or False
        self.allowances = Allowances(
            dictionary=dictionary.get('allowances')
        )
