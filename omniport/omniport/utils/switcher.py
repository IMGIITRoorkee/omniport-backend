import importlib

from django.conf import settings


def load_serializer(app_name, model_name):
    """

    :param app_name:
    :param model_name:
    :return:
    """

    app_name = app_name
    model_name = model_name
    setting_name = f'{app_name}_{model_name}_SERIALIZER'.upper()

    setting = getattr(settings, setting_name, None)
    if setting is not None:
        module_name, _, class_name = setting.rpartition('.')
        module = importlib.import_module(module_name)
        dictionary = module.__dict__
        SerializerClass = dictionary[class_name]
        return SerializerClass
    else:
        return None
