class Secrets:
    """
    This class stores the secret information related to the project, namely
    the Django secret key
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Secrets from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, includes 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.secret_key = dictionary.get('secretKey')
