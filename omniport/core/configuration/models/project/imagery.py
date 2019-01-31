import os
import mimetypes

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

        self.logo = file_search(
            files=contents,
            name='logo',
            extensions=['.svg', '.png', '.jpg']
        )
        self.logo_mime, _ = mimetypes.guess_type(self.logo)

        self.wordmark = file_search(
            files=contents,
            name='wordmark',
            extensions=['.svg', '.png', '.jpg']
        )
        self.wordmark_mime, _ = mimetypes.guess_type(self.wordmark)

        self.favicon = file_search(
            files=contents,
            name='favicon',
            extensions=['.ico']
        )

        self.logo_192 = file_search(
            files=contents,
            name='logo_192',
            extensions=['.png']
        )
        self.logo_512 = file_search(
            files=contents,
            name='logo_512',
            extensions=['.png']
        )

        self.logo_apple = file_search(
            files=contents,
            name='logo_apple',
            extensions=['.png']
        )
