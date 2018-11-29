import os

from configuration.utils.file_search import file_search


class Assets:
    """
    This class stores information about an app's assets, namely the the path to
    various image files
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Assets from a directory
        :param args: arguments
        :param kwargs: keyword arguments, includes 'directory'
        """

        super().__init__()

        directory = kwargs.get('directory')
        contents = os.listdir(directory)

        self.favicon = file_search(contents,
                                   'favicon', ['.ico'])
        self.icon = file_search(contents,
                                'icon', ['.svg', '.png', '.jpg'])
        self.logo = file_search(contents,
                                'logo', ['.svg', '.png', '.jpg'])
