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


class CommunicationStore(Service):
    """
    This class stores information about the notification store service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)

class VerificationStore(Service):
    """
    This class stores information about the notification store service
    """

    def __init__(self, *args, **kwargs):
        """
        Defer to the base class to populate the data points
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)

class Cache(Service):
    """
    This class stores information about the cache service
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
        self.communication_store = CommunicationStore(
            dictionary=dictionary.get('communicationStore')
        )
        self.verification_store = VerificationStore(
            dictionary=dictionary.get('verificationStore')
        )
        self.cache = Cache(
            dictionary=dictionary.get('cache')
        )
        self.message_broker = MessageBroker(
            dictionary=dictionary.get('messageBroker')
        )
