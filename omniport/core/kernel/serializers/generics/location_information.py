from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from kernel.models import LocationInformation


class CountryDetailSerializer(serializers.Serializer):
    """
    Serializer for django_countries.Country objects
    """

    code = serializers.CharField()
    name = serializers.CharField()
    flag = serializers.CharField()
    unicode_flag = serializers.CharField()


class LocationInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for LocationInformation objects
    """

    country_detail = CountryDetailSerializer(
        source='country',
        read_only=True,
    )
    country = CountryField(
        write_only=True,
    )

    class Meta:
        """
        Meta class for LocationInformationSerializer
        """

        model = LocationInformation

        exclude = [
            'datetime_created',
            'datetime_modified',
            'entity_content_type',
            'entity_object_id',
        ]
