import importlib
import os

import inflection
import yaml
from channels.routing import URLRouter
from django.urls import path, include

from configuration.models.app.app import AppConfiguration
from configuration.models.app.assets import Assets


class Discovery:
    """
    This class stores information about the applications discovered in the
    service and app folders and their app configurations
    """

    def __init__(self, services_directory, apps_directory):
        """
        Create an instance of Discovery with the specified service and app
        directories
        :param services_directory: the directory to scan for services
        :param apps_directory: the directory to scan for apps
        """

        self.services_directory = services_directory
        self.apps_directory = apps_directory

        # App directory - configuration tuples
        self.services = list()
        self.apps = list()

        # App name - configuration maps
        self.service_configuration_map = dict()
        self.app_configuration_map = dict()

        # INSTALLED_APPS additional entries
        self.service_installed_apps = list()
        self.app_installed_apps = list()

        # STATICFILES_DIRS additional entries
        self.service_staticfiles_dirs = list()
        self.app_staticfiles_dirs = list()

        # http_urls additional entries
        self.service_http_urlpatterns = list()
        self.app_http_urlpatterns = list()

        # ws_urls additional entries
        self.service_ws_urlpatterns = list()
        self.app_ws_urlpatterns = list()

    @staticmethod
    def _prepare_app_configuration_list(directory):
        """
        Produce a list of tuples of apps and their configurations after scanning
        the specified directory
        :param directory: the directory to scan for apps
        :return: the list of tuples of apps and their configuration objects
        """

        sub_directories = [
            sub_directory
            for sub_directory in os.listdir(path=directory)
            if os.path.isdir(os.path.join(directory, sub_directory))
        ]

        apps_and_configs = list()
        for sub_directory in sub_directories:
            config_path = os.path.join(directory, sub_directory, 'config.yml')
            if os.path.isfile(config_path):
                config_dictionary = yaml.load(open(config_path))
                config_object = AppConfiguration(dictionary=config_dictionary)
                apps_and_configs.append(
                    (sub_directory, config_object,)
                )
        return apps_and_configs

    @staticmethod
    def _prepare_app_configuration_map(app_set):
        """
        Generate a dictionary for the given list of tuples of apps and
        configuration objects
        :param app_set: the given list of tuples of apps and their configuration
        objects
        :return: the dictionary version of the list of tuples
        """

        app_configuration_map = dict()
        for (app, app_configuration) in app_set:
            app_name = app_configuration.nomenclature.name
            app_configuration_map[app_name] = app_configuration
        return app_configuration_map

    def discover(self):
        """
        Populate the values of apps and their configurations for both services
        and apps
        """

        self.services = Discovery._prepare_app_configuration_list(
            self.services_directory
        )
        self.service_configuration_map = self._prepare_app_configuration_map(
            self.services
        )

        self.apps = Discovery._prepare_app_configuration_list(
            self.apps_directory
        )
        self.app_configuration_map = self._prepare_app_configuration_map(
            self.apps
        )

    @staticmethod
    def _prepare_installed_apps(app_set):
        """
        Generate INSTALLED_APPS entries for the given list of tuples of apps and
        configuration objects
        :param app_set: the given list of tuples of apps and their configuration
        objects
        :return: the INSTALLED_APPS entries
        """

        additional_installed_apps = list()
        for (app, app_configuration) in app_set:
            additional_installed_apps.append(
                f'{app}.apps.{inflection.camelize(app)}Config'
            )
        return additional_installed_apps

    def prepare_installed_apps(self):
        """
        Populate the values of INSTALLED_APPS entries in settings for both
        services and apps
        """

        self.service_installed_apps = Discovery._prepare_installed_apps(
            self.services
        )
        self.app_installed_apps = Discovery._prepare_installed_apps(
            self.apps
        )

    @staticmethod
    def _prepare_assets(directory, app_configuration):
        """
        
        :param directory: 
        :param app_configuration: 
        :return: 
        """

        assets_path = os.path.join(directory, 'assets')
        if os.path.isdir(assets_path):
            assets = Assets(directory=assets_path)
            app_configuration.assets = assets

    @staticmethod
    def _prepare_staticfiles_dirs(directory, app_set):
        """
        Generate STATICFILES_DIRS entries for the given list of tuples of apps
        and configuration objects
        :param directory: the directory to scan for apps
        :param app_set: the given list of tuples of apps and their configuration
        objects
        :return: the STATICFILES_DIRS entries
        """

        additional_staticfiles_dirs = list()
        for (app, app_configuration) in app_set:
            static_path = os.path.join(directory, app, 'static')
            if os.path.isdir(static_path):
                app_configuration.has_static = True

                # Additional files can be found at the URL
                # /<static URL>/<namespace>/<static path>
                additional_staticfiles_dirs.append(
                    (
                        app_configuration.base_urls.static[:-1],  # <namespace>
                        static_path,  # <static path>
                    )
                )

                Discovery._prepare_assets(static_path, app_configuration)
            else:
                app_configuration.has_static = False

        return additional_staticfiles_dirs

    def prepare_staticfiles_dirs(self):
        """
        Populate the values of static file directories for both services and
        apps
        """

        self.service_staticfiles_dirs = Discovery._prepare_staticfiles_dirs(
            self.services_directory,
            self.services
        )
        self.app_staticfiles_dirs = Discovery._prepare_staticfiles_dirs(
            self.apps_directory,
            self.apps
        )

    @staticmethod
    def _prepare_http_urlpatterns(app_set):
        """
        Generate HTTP URL patterns for the given list of tuples of apps and
        configuration objects
        :param app_set: the given list of tuples of apps and their configuration
        objects
        :return: the HTTP URL patterns
        """

        http_urlpatterns = list()
        for (app, app_configuration) in app_set:
            if app_configuration.is_allowed:
                url = app_configuration.base_urls.http
                if url is not None:
                    if app_configuration.is_api:
                        url = f'api/{url}'
                    http_urlpatterns.append(
                        path(url, include(f'{app}.http_urls'))
                    )
        return http_urlpatterns

    @staticmethod
    def _prepare_ws_urlpatterns(app_set):
        """
        Generate WS URL patterns for the given list of tuples of apps and
        configuration objects
        :param app_set: the given list of tuples of apps and their configuration
        objects
        :return: the WS URL patterns
        """

        ws_urlpatterns = list()
        for (app, app_configuration) in app_set:
            if app_configuration.is_allowed:
                url = app_configuration.base_urls.ws
                if url is not None:
                    module = importlib.import_module(f'{app}.ws_urls')
                    dictionary = module.__dict__
                    app_urlpatterns = dictionary['urlpatterns']
                    url_router = URLRouter(app_urlpatterns)
                    ws_urlpatterns.append(
                        path(url, url_router)
                    )
        return ws_urlpatterns

    def prepare_urlpatterns(self):
        """
        Populate the values of HTTP and WS URL patterns for both services and
        apps
        """

        self.service_http_urlpatterns = self._prepare_http_urlpatterns(
            self.services
        )
        self.service_ws_urlpatterns = self._prepare_ws_urlpatterns(
            self.services
        )

        self.app_http_urlpatterns = self._prepare_http_urlpatterns(
            self.apps
        )
        self.app_ws_urlpatterns = self._prepare_ws_urlpatterns(
            self.apps
        )

    def get_app_configuration(self, app):
        """
        Get the AppConfiguration object of the mentioned app
        :param app: the name of the app to get the AppConfiguration object for
        :return: the AppConfiguration object of the given app
        """

        try:
            return self.app_configuration_map[app]
        except KeyError:
            pass

        try:
            return self.service_configuration_map[app]
        except KeyError:
            pass

        return None
