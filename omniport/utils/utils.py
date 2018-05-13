import json
import os

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


def get_core_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of a core app to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of a core app to its dispatcher
    """

    core_urlpatterns = list()

    for core_app, base_urls in settings.CORE_APP_BASE_URLS_MAP.items():
        # Add the path mapping to the URL patterns
        base_url = base_urls.get(protocol, None)
        if base_url is not None:
            core_urlpatterns.append(
                path(f'{base_url}', include(f'{core_app}.{protocol}_urls'))
            )

    return core_urlpatterns


def get_service_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of a service to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of a service to its dispatcher
    """

    service_urlpatterns = list()

    for service, base_urls in settings.SERVICE_BASE_URLS_MAP.items():
        # Add the path mapping to the URL patterns
        base_url = base_urls.get(protocol, None)
        if base_url is not None:
            service_urlpatterns.append(
                path(f'{base_url}', include(f'{service}.{protocol}_urls'))
            )

    return service_urlpatterns


def get_app_urlpatterns(protocol):
    """
    Get the list of paths each mapping the URL of an app to its dispatcher
    :param protocol: the protocol for which the base URL is to be retrieved
    :return: the list of paths mapping the URL of an app to its dispatcher
    """

    app_urlpatterns = list()

    for app, base_urls in settings.APP_BASE_URLS_MAP.items():
        if settings.ALLOWED_APPS == '__all__' or app in settings.ALLOWED_APPS:
            # Add the path mapping to the URL patterns
            base_url = base_urls.get(protocol, None)
            if base_url is not None:
                app_urlpatterns.append(
                    path(f'{base_url}', include(f'{app}.{protocol}_urls'))
                )

    return app_urlpatterns
