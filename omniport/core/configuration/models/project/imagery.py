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
        if self.logo is not None:
            self.logo_mime, _ = mimetypes.guess_type(self.logo)
        else:
            self.logo_mime = None

        self.wordmark = file_search(
            files=contents,
            name='wordmark',
            extensions=['.svg', '.png', '.jpg']
        )
        if self.wordmark is not None:
            self.wordmark_mime, _ = mimetypes.guess_type(self.wordmark)
        else:
            self.wordmark_mime = None

        self.giftbox = file_search(
            files=contents,
            name='giftbox',
            extensions=['.svg', '.png', '.jpg']
        )
        if self.giftbox is not None:
            self.giftbox_mime, _ = mimetypes.guess_type(self.giftbox)
        else:
            self.giftbox_mime = None

        self.favicon = file_search(
            files=contents,
            name='favicon',
            extensions=['.ico']
        )
        if self.favicon is not None:
            self.favicon_mime, _ = mimetypes.guess_type(self.favicon)
        else:
            self.favicon_mime = None


class SiteImagery(Imagery):
    """
    This class stores information about a site's imagery, namely the path to
    various image files
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance of Imagery from a directory
        :param args: arguments
        :param kwargs: keyword arguments, includes 'directory'
        """

        super().__init__(self, *args, **kwargs)

        self.directory = kwargs.get('directory')
        self.url = kwargs.get('url')
        contents = os.listdir(self.directory)

        self.logo_192 = file_search(
            files=contents,
            name='logo_192',
            extensions=['.png']
        )
        self.logo_192_mime, _ = mimetypes.guess_type(self.logo_192)
        self.logo_512 = file_search(
            files=contents,
            name='logo_512',
            extensions=['.png']
        )
        self.logo_512_mime, _ = mimetypes.guess_type(self.logo_512)

        self.logo_apple = file_search(
            files=contents,
            name='logo_apple',
            extensions=['.png']
        )
        self.logo_apple_mime, _ = mimetypes.guess_type(self.logo_apple)
