import importlib
import json
import os

from channels.routing import URLRouter
from django.conf import settings
from django.urls import path, include


def populate_base_urls_map(apps_dir, app_dirs, app_base_urls_map):
    """
    Pick up apps from the given directory and map them with their base URLs
    :param apps_dir: the directory containing various Django apps
    :param app_dirs: the individual app directories inside apps_dir
    :param app_base_urls_map: the dictionary of apps and their base URLs
    """

    for app in app_dirs:
        config_file = os.path.join(
            apps_dir,
            app,
            'config.json'
        )
        with open(config_file) as config_file:
            config = json.load(config_file)
            base_urls = config['baseUrls']
            app_base_urls_map[app] = base_urls


def get_http_urlpatterns(app_base_urls_map, allowed_apps='__all__'):
    """
    Get the URL pattern list corresponding to the hypertext protocol
    :param app_base_urls_map: the dictionary of apps and their base URLs
    :param allowed_apps: the list of apps to allow in the URLs, or __all__
    :return: the URL pattern list corresponding to the hypertext protocol
    """

    urlpatterns = list()

    for app, base_urls in app_base_urls_map.items():
        if allowed_apps == '__all__' or app in allowed_apps:
            if 'http' in base_urls:
                base_url = base_urls.get('http')
                urlpatterns.append(
                    path(f'{base_url}', include(f'{app}.http_urls'))
                )

    return urlpatterns


def get_ws_urlpatterns(app_base_urls_map, allowed_apps='__all__'):
    """
    Get the URL pattern list corresponding to the websocket protocol
    :param app_base_urls_map: the dictionary of apps and their base URLs
    :param allowed_apps: the list of apps to allow in the URLs, or __all__
    :return: the URL pattern list corresponding to the websocket protocol
    """

    urlpatterns = list()

    for app, base_urls in app_base_urls_map.items():
        if allowed_apps == '__all__' or app in allowed_apps:
            if 'ws' in base_urls:
                base_url = base_urls.get('ws')
                module = importlib.import_module(f'{app}.ws_urls')
                dict = module.__dict__
                app_urlpatterns = dict['urlpatterns']
                url_router = URLRouter(app_urlpatterns)
                urlpatterns.append(
                    path(f'{base_url}', url_router)
                )

    return urlpatterns


def get_core_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of a core app to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of a core app to its dispatcher
    """

    if protocol == 'http':
        return get_http_urlpatterns(settings.CORE_APP_BASE_URLS_MAP)

    if protocol == 'ws':
        return get_ws_urlpatterns(settings.CORE_APP_BASE_URLS_MAP)


def get_service_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of a service to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of a service to its dispatcher
    """

    if protocol == 'http':
        return get_http_urlpatterns(settings.SERVICE_BASE_URLS_MAP)

    if protocol == 'ws':
        return get_ws_urlpatterns(settings.SERVICE_BASE_URLS_MAP)


def get_app_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of an app to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of an app to its dispatcher
    """

    if protocol == 'http':
        return get_http_urlpatterns(
            settings.APP_BASE_URLS_MAP,
            settings.ALLOWED_APPS
        )

    if protocol == 'ws':
        return get_ws_urlpatterns(
            settings.APP_BASE_URLS_MAP,
            settings.ALLOWED_APPS
        )
