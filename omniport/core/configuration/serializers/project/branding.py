from rest_framework import serializers

from configuration.serializers.project.imagery import ImagerySerializer
from configuration.serializers.project.text import TextSerializer


class BrandSerializer(serializers.Serializer):
    """
    Serializer for Brand objects
    """

    text = TextSerializer()
    imagery = ImagerySerializer()
