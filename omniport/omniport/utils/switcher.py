import importlib

from django.conf import settings


def load_serializer(app_name, model_name, version_name=None):
    """
    This function returns the appropriate serializer class based on the names of
    the app, model and version
    :param app_name: the name of the app whose model is being serialized
    :param model_name: the name of the model being serialized
    :param version_name: the name of the serializer if many exist
    :return: the serializer class
    """

    app_name = app_name
    model_name = model_name
    setting_name = f'{app_name}_{model_name}'
    if version_name is not None:
        setting_name = f'{setting_name}_{version_name}'
    setting_name = f'{setting_name}_SERIALIZER'.upper()

    setting = getattr(settings, setting_name, None)
    if setting is not None:
        module_name, _, class_name = setting.rpartition('.')
        module = importlib.import_module(module_name)
        dictionary = module.__dict__
        SerializerClass = dictionary[class_name]
        return SerializerClass
    else:
        return None
