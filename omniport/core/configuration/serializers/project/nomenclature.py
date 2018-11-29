from rest_framework import serializers


class NomenclatureSerializer(serializers.Serializer):
    """
    Serializer for Nomenclature objects
    """

    name = serializers.CharField()
    verbose_name = serializers.CharField()
