import mimetypes
import os
import uuid

from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadTo:
    """
    This utility provides a cross-application, cross-model generalised way for
    storing files based on a UUID naming scheme
    """

    def __init__(self, app_name, folder_name, file_manager=False):
        """
        Initialise a callable instance of the class with the given parameters
        :param app_name: the name of the app using this utility
        :param folder_name: the name of the folder where to write the file
        :param file_manager: whether the app using this utility is File Manager
        """

        self.app_name = app_name
        self.folder_name = folder_name
        self.file_manager = file_manager

    def __call__(self, instance, filename):
        """
        Compute the location of where to store the file, removing any
        existing file with the same name
        :param instance: the instance to which file is being uploaded
        :param filename: the original name of the file, used for the extension
        :return: the path to the uploaded image
        """

        # Path upto the file
        if self.file_manager:
            folder_name = str(instance.folder.folder_name())
        else:
            folder_name = self.folder_name

        # Name of the file
        uuid_key = uuid.uuid4()

        # Extension of the file
        extension = filename.split('.')[-1]
        extension = extension.lower()
        extension = f'.{extension}'
        if extension not in mimetypes.types_map.keys():
            extension = ''

        # Full path to the file
        destination = os.path.join(
            self.app_name,
            folder_name,
            f'{uuid_key}{extension}',
        )

        # Delete any existing file at the destination location
        # This is highly unlikely because of the use of UUIDs
        try:
            path = os.path.join(
                settings.MEDIA_ROOT,
                destination,
            )
            os.remove(path)
        except FileNotFoundError:
            pass

        return destination
