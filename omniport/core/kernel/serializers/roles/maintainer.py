import swapper

from formula_one.serializers.base import ModelSerializer
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

        fields = [
            'id',
            'person',
            'role',
            'designation',
            'post',
        ]
