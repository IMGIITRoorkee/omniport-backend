from rest_framework import serializers

from configuration.serializers.project.imagery import ImagerySerializer
from configuration.serializers.project.nomenclature import (
    NomenclatureSerializer,
)


class SiteSerializer(serializers.Serializer):
    """
    Serializer for Site objects
    """

    id = serializers.IntegerField()
    nomenclature = NomenclatureSerializer()
    imagery = ImagerySerializer()
