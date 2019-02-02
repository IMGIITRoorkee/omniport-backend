import os

from django.conf import settings
from rest_framework import serializers


class ImagerySerializer(serializers.Serializer):
    """
    Serializer for Imagery objects
    """

    favicon = serializers.SerializerMethodField()
    favicon_mime = serializers.CharField()

    logo = serializers.SerializerMethodField()
    logo_mime = serializers.CharField()

    wordmark = serializers.SerializerMethodField()
    wordmark_mime = serializers.CharField()

    @staticmethod
    def get_url(directory, item):
        """
        Get the URL to the given imagery item
        :param directory: the directory in which the imagery resides
        :param item: the item whose URL is to be determined
        :return: the URL to the item
        """

        return os.path.join(
            directory,
            item
        ).replace(
            f'{settings.BRANDING_ROOT}/',
            settings.BRANDING_URL
        )

    def get_favicon(self, instance):
        """
        Get the URL to the favicon of the imagery instance
        :param instance: the instance whose favicon is requested
        :return: the URL to the favicon
        """

        if instance.favicon is not None:
            return self.get_url(instance.directory, instance.favicon)

    def get_logo(self, instance):
        """
        Get the URL to the logo of the imagery instance
        :param instance: the instance whose logo is requested
        :return: the URL to the logo
        """

        if instance.logo is not None:
            return self.get_url(instance.directory, instance.logo)

    def get_wordmark(self, instance):
        """
        Get the URL to the wordmark of the imagery instance
        :param instance: the instance whose wordmark is requested
        :return: the URL to the wordmark
        """

        if instance.wordmark is not None:
            return self.get_url(instance.directory, instance.wordmark)
