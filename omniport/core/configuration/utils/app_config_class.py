import os

from django.apps import AppConfig
from django.conf import settings


def get_app_config_class(path):
    """
    Return a subclass of AppConfig to configure the app
    :param path: the path to the apps.py file, can be accessed as __file__
    :return: a subclass of AppConfig that configures the given app
    """

    file_path = os.path.abspath(path)
    app_directory = os.path.dirname(file_path)
    app_directory_name = os.path.basename(app_directory)
    conf = settings.DISCOVERY.get_app_configuration(app_directory_name)

    class Config(AppConfig):
        name = app_directory_name
        label = conf.nomenclature.name
        verbose_name = conf.nomenclature.verbose_name
        configuration = conf

    return Config
