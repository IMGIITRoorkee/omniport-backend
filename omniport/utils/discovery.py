import json
import os

import inflection


def discover(app_group_info):
    """
    Load apps belonging to the given app group
    :param app_group_info: the information about the app group being scanned
    """

    group_directory = app_group_info.get('directory')
    app_group_info['apps'] = [
        {
            'name': directory,
            'directory': os.path.join(group_directory, directory),
            'isAllowed': True,
        }
        for directory in os.listdir(path=group_directory)
        if os.path.isdir(os.path.join(group_directory, directory))
    ]
    for app in app_group_info.get('apps'):
        configuration = config(app.get('directory'))
        app['config'] = configuration
        name = app.get('name')
        listing = f'{name}.apps.{inflection.camelize(name)}Config'
        app['listing'] = listing


def config(directory):
    """
    Get the configuration from the folder name of an app
    :param directory: the directory from which to extract the
    :return: the configuration of every app being scanned
    """

    config_file = open(os.path.join(directory, 'config.json'))
    configuration = json.load(config_file)
    return configuration
