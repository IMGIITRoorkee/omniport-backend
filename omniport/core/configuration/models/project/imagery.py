import os

from configuration.utils.file_search import file_search


class Imagery:
    """
    This class stores information about a entity's imagery, namely the path to
    various image files
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Imagery from a directory
        :param args: arguments
        :param kwargs: keyword arguments, includes 'directory'
        """

        self.directory = kwargs.get('directory')
        self.url = kwargs.get('url')
        contents = os.listdir(self.directory)

        self.favicon = file_search(contents,
                                   'favicon', ['.ico'])
        self.logo = file_search(contents,
                                'logo', ['.svg', '.png', '.jpg'])
        self.wordmark = file_search(contents,
                                    'wordmark', ['.svg', '.png', '.jpg'])
