import importlib

from channels.routing import URLRouter
from django.conf import settings
from django.urls import path, include


def get_http_urlpatterns(app_group):
    """
    Get the URL pattern list corresponding to the hypertext protocol
    :param app_group: the group of apps whose URL patterns are to be retrieved
    :return: the URL pattern list corresponding to the hypertext protocol
    """

    urlpatterns = list()

    discovery = settings.DISCOVERY
    app_group = discovery.get(app_group)
    apps = app_group.get('apps')
    for app in apps:
        name = app.get('name')
        if app.get('isAllowed'):
            config = app.get('config')
            base_url = config.get('baseUrls', {}).get('http', None)
            if base_url is not None:
                urlpatterns.append(
                    path(f'{base_url}', include(f'{name}.http_urls'))
                )

    return urlpatterns


def get_ws_urlpatterns(app_group):
    """
    Get the URL pattern list corresponding to the websocket protocol
    :param app_group: the group of apps whose URL patterns are to be retrieved
    :return: the URL pattern list corresponding to the websocket protocol
    """

    urlpatterns = list()

    discovery = settings.DISCOVERY
    app_group = discovery.get(app_group)
    apps = app_group.get('apps')
    for app in apps:
        name = app.get('name')
        if app.get('isAllowed'):
            config = app.get('config')
            base_url = config.get('baseUrls', {}).get('ws', None)
            if base_url is not None:
                module = importlib.import_module(f'{name}.ws_urls')
                dictionary = module.__dict__
                app_urlpatterns = dictionary['urlpatterns']
                url_router = URLRouter(app_urlpatterns)
                urlpatterns.append(
                    path(f'{base_url}', url_router)
                )

    return urlpatterns


def get_urlpatterns(app_group, protocol):
    """
    Get the list of paths each mapping the URL of an app to its dispatcher
    :param app_group: the group of apps whose URL patterns are to be retrieved
    :param protocol: the protocol for which the URL patterns are to be retrieved
    :return: the list of paths mapping the URL of an app to its dispatcher
    """

    if protocol == 'http':
        return get_http_urlpatterns(app_group)

    if protocol == 'ws':
        return get_ws_urlpatterns(app_group)
