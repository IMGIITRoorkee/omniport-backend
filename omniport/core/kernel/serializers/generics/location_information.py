import swapper

from rest_framework import serializers
from kernel.serializers.root import ModelSerializer


class CountrySerializer(serializers.Serializer):
    """
    Serializer for django_countries.Country objects
    """

    code = serializers.CharField()
    name = serializers.CharField()
    flag = serializers.CharField()
    unicode_flag = serializers.CharField()


class LocationInformationSerializer(ModelSerializer):
    """
    Serializer for LocationInformation objects
    """

    country = CountrySerializer()

    class Meta:
        """
        Meta class for LocationInformationSerializer
        """

        model = swapper.load_model('kernel', 'LocationInformation')

        fields = [
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            'latitude',
            'longitude',
        ]
