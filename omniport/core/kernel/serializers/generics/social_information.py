from rest_framework import serializers

from kernel.models import SocialLink, SocialInformation


class SocialLinkSerializer(serializers.ModelSerializer):
    """
    Serializer for SocialLink objects
    """

    site_name = serializers.ReadOnlyField()
    site_logo = serializers.ReadOnlyField()

    class Meta:
        """
        Meta class for SocialLinkSerializer
        """

        model = SocialLink

        exclude = [
            'datetime_created',
            'datetime_modified',
        ]


class SocialInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for SocialInformation objects
    """

    links = SocialLinkSerializer(
        many=True,
    )

    class Meta:
        """
        Meta class for SocialInformationSerializer
        """

        model = SocialInformation

        exclude = [
            'datetime_created',
            'datetime_modified',
            'entity_content_type',
            'entity_object_id',
        ]
