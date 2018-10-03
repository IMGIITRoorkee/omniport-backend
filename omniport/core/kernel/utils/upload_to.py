import mimetypes
import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """

    """

    def __init__(self, app_name, folder_name, file_manager=False):
        """

        :param app_name:
        :param folder_name:
        :param file_manager:
        """

        self.app_name = app_name
        self.folder_name = folder_name
        self.file_manager = file_manager

    def __call__(self, instance, filename):
        """
        Compute the location of where to store the file, removing any
        existing file with the same name
        :param instance: the instance to which file is being uploaded
        :param filename: the original name of the file, not used
        :return: the path to the uploaded image
        """
        if self.file_manager:
            folder_name = str(instance.folder.folder_name())
        else:
            folder_name = self.folder_name

        extension = filename.split('.')[-1]
        extension = f'.{extension}'
        if extension not in mimetypes.types_map.keys():
            extension = ''
        uuid_key = uuid.uuid4()
        destination = os.path.join(
            self.app_name,
            folder_name,
            f'{uuid_key}{extension}',
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
