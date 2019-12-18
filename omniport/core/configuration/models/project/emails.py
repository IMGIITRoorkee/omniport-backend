class Emails:
    """
    This class stores the configuration requirements for the email service to work
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Secrets from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.email_backend = dictionary.get('emailBackend')
	self.email_host = dictionary.get('emailHost')
	self.email_use_tls = dictionary.get('emailUseTls')
	self.email_port = dictionary.get('emailPort')
	self.email_host_user = dictionary.get('emailHostUser')
	self.email_host_password = dictionary.get('emailHostPassword')
