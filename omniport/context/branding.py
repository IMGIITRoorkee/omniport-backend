import os

from django.conf import settings
from django.contrib.staticfiles import finders


def unique_logo(name, extension):
    """
    Check if a logo with the given name exists
    :param name: the name of the logo to check for existence
    :param extension: the extension of the logo to check for existence
    :return: the relative path to the logo if found, None otherwise
    """

    logo_relative_path = os.path.join(
        'omniport',
        'logos',
        f'{name}{extension}',
    )
    if finders.find(logo_relative_path) is not None:
        return logo_relative_path
    else:
        return None


def indexed_logo(name, extension, preferred_index):
    """
    Check if a logo with the given name, and preferably index, exists
    :param name: the name of the logo to check for existence
    :param extension: the extension of the logo to check for existence
    :param preferred_index: the preferred index of the logo
    :return: the relative path to the logo if found, None otherwise
    """

    logo_relative_path = os.path.join(
        'omniport',
        'logos',
        f'{name}_{preferred_index}{extension}',
    )
    if finders.find(logo_relative_path) is not None:
        return logo_relative_path
    else:
        return unique_logo(name, extension)


def logos(_):
    """
    Add the logos of the institute, maintainer and project to the context
    :param _: the request being served
    :return: the data to add to the context
    """

    data = dict()
    data['INSTITUTE_LOGO'] = unique_logo('institute', '.png')
    data['MAINTAINERS_LOGO'] = unique_logo('maintainers', '.png')
    data['PORTAL_LOGO'] = indexed_logo('portal', '.png', settings.SITE_ID)
    return data


def branding_text(_):
    """
    Add the brand text of the institute, maintainer and project to the context
    :param _: the request being served
    :return: the data to add to the context
    """

    data = dict()
    data['INSTITUTE'] = settings.INSTITUTE
    data['MAINTAINERS'] = settings.MAINTAINERS
    return data
