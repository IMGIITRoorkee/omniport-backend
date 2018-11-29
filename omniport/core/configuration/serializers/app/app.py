from rest_framework import serializers

from configuration.serializers.app.assets import AssetsSerializer
from configuration.serializers.app.base_urls import BaseUrlsSerializer
from configuration.serializers.app.nomenclature import NomenclatureSerializer


class AppSerializer(serializers.Serializer):
    """
    Serializer for AppConfiguration objects
    """

    nomenclature = NomenclatureSerializer()
    base_urls = BaseUrlsSerializer()
    assets = AssetsSerializer()
    description = serializers.CharField()
