import swapper

from kernel.serializers.root import ModelSerializer
from kernel.serializers.person import AvatarSerializer


class MaintainerSerializer(ModelSerializer):
    """
    Serializer for Maintainer objects
    """

    person = AvatarSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for MaintainerSerializer
        """

        model = swapper.load_model('kernel', 'Maintainer')
        fields = (
            'id',
            'person',
            'role',
            'post',
        )

