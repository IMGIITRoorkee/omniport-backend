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
