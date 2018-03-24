import json
import os

from django.conf import settings
from django.urls import path, include


def get_site_urlpatterns():
    """
    Get the list of paths each mapping the URL of an app to its dispatcher
    :return: the list of paths each mapping the URL of an app to its dispatcher
    """

    site_urlpatterns = list()

    for app in settings.DJANGO_APP_FOLDERS:
        if settings.ALLOWED_APPS == '__all__' or app in settings.ALLOWED_APPS:
            config_file = os.path.join(
                settings.DJANGO_APPS_DIR,
                app,
                'config.json'
            )
            with open(config_file) as config_file:
                config = json.load(config_file)
                base_url = config['baseUrl']

                # Add the app-base URL entry to the map stored in settings
                settings.APP_BASE_URL_MAP[app] = base_url

                # Add the path mapping to the URL patterns
                site_urlpatterns.append(
                    path(f'{base_url}', include(f'{app}.urls'))
                )

    return site_urlpatterns
