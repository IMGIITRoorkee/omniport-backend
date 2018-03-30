import json
import os

from django.conf import settings
from django.urls import path, include


def populate_base_url_map(apps_dir, app_dirs, app_base_url_map):
    """
    Pick up apps from the given directory and map them with their base URL
    :param apps_dir: the directory containing various Django apps
    :param app_dirs: the individual app directories inside apps_dir
    :param app_base_url_map: the dictionary of apps and their base URL
    """

    for app in app_dirs:
        config_file = os.path.join(
            apps_dir,
            app,
            'config.json'
        )
        with open(config_file) as config_file:
            config = json.load(config_file)
            base_url = config['baseUrl']
            app_base_url_map[app] = base_url


def get_service_urlpatterns():
    """
    Get the list of paths each mapping the URL of a service to its dispatcher
    :return: the list of paths mapping the URL of a service to its dispatcher
    """

    service_urlpatterns = list()

    for service, base_url in settings.SERVICE_BASE_URL_MAP.items():
        # Add the path mapping to the URL patterns
        service_urlpatterns.append(
            path(f'{base_url}', include(f'{service}.urls'))
        )

    return service_urlpatterns


def get_app_urlpatterns():
    """
    Get the list of paths each mapping the URL of an app to its dispatcher
    :return: the list of paths mapping the URL of an app to its dispatcher
    """

    app_urlpatterns = list()

    for app, base_url in settings.APP_BASE_URL_MAP.items():
        if settings.ALLOWED_APPS == '__all__' or app in settings.ALLOWED_APPS:
            # Add the path mapping to the URL patterns
            app_urlpatterns.append(
                path(f'{base_url}', include(f'{app}.urls'))
            )

    return app_urlpatterns
