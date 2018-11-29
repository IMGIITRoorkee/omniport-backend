import os

from rest_framework import serializers


class AssetsSerializer(serializers.Serializer):
    """
    Serializer for Assets objects
    """

    favicon = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    def get_favicon(self, instance):
        """
        Get the URL to the favicon of the imagery instance
        :param instance: the instance whose favicon is requested
        :return: the URL to the favicon
        """

        if instance.favicon is not None:
            return os.path.join('assets', instance.favicon)

    def get_icon(self, instance):
        """
        Get the URL to the icon of the imagery instance
        :param instance: the instance whose icon is requested
        :return: the URL to the icon
        """

        if instance.icon is not None:
            return os.path.join('assets', instance.icon)

    def get_logo(self, instance):
        """
        Get the URL to the logo of the imagery instance
        :param instance: the instance whose logo is requested
        :return: the URL to the logo
        """

        if instance.logo is not None:
            return os.path.join('assets', instance.logo)
