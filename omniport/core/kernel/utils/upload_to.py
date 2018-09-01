import mimetypes
import os

from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """

    """

    def __init__(self, app_name, folder_name):
        """

        :param app_name:
        :param folder_name:
        """

        self.app_name = app_name
        self.folder_name = folder_name

    def __call__(self, instance, filename):
        """
        Compute the location of where to store the file, removing any
        existing file with the same name
        :param instance: the instance to which file is being uploaded
        :param filename: the original name of the file, not used
        :return: the path to the uploaded image
        """

        extension = filename.split('.')[-1]
        extension = f'.{extension}'
        if extension not in mimetypes.types_map.keys():
            extension = ''

        destination = os.path.join(
            self.app_name,
            self.folder_name,
            f'{instance.id}{extension}',
        )

        try:
            path = os.path.join(
                settings.MEDIA_ROOT,
                destination,
            )
            os.remove(path)
        except FileNotFoundError:
            pass

        return destination
