from rest_framework import serializers


class BaseUrlsSerializer(serializers.Serializer):
    """
    Serializer for BaseUrls objects
    """

    http = serializers.CharField()
    ws = serializers.CharField()
    static = serializers.CharField()
