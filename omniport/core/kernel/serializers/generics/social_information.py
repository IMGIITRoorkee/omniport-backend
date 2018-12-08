import swapper
from rest_framework import serializers

from kernel.serializers.root import ModelSerializer


class SocialLinkSerializer(ModelSerializer):
    """
    Serializer for SocialLink objects
    """

    site_name = serializers.SerializerMethodField()

    def get_site_name(self, instance):
        """
        Return the display name of the site that can be used for tooltips
        :param instance: the SocialLink model being serialized
        :return: the display name of the site in the link
        """

        return instance.get_site_display()

    class Meta:
        """
        Meta class for SocialLinkSerializer
        """

        model = swapper.load_model('kernel', 'SocialLink')

        fields = [
            'site_name',
            'url',
            'site_logo',
        ]


class SocialInformationSerializer(ModelSerializer):
    """
    Serializer for SocialInformation objects
    """

    links = SocialLinkSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        """
        Meta class for SocialInformationSerializer
        """

        model = swapper.load_model('kernel', 'SocialInformation')

        fields = [
            'links',
        ]
