from rest_framework import serializers


class TextSerializer(serializers.Serializer):
    """
    Serializer for Text objects
    """

    name = serializers.CharField()
    acronym = serializers.CharField()
    home_page = serializers.CharField()
