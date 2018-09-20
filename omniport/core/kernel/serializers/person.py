import swapper

from kernel.serializers.root import ModelSerializer


class PersonSerializer(ModelSerializer):
    """
    Serializer for Person objects
    """

    class Meta:
        """
        Meta class for PersonSerializer
        """

        model = swapper.load_model('kernel', 'Person')
        fields = '__all__'


class ProfileSerializer(ModelSerializer):
    """
    Serializer for the entire profile of a person
    """

    class Meta:
        """
        Meta class for ProfileSerializer
        """

        model = swapper.load_model('kernel', 'Person')
        exclude = (
            'datetime_modified',
            'removed',
        )


class AvatarSerializer(ModelSerializer):
    """
    Serializer for minimal information of a person
    """

    class Meta:
        """
        Meta class for AvatarSerializer
        """

        model = swapper.load_model('kernel', 'Person')
        fields = (
            'short_name',
            'full_name',
            'display_picture',
        )

