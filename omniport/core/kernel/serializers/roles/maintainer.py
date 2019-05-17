import swapper

from kernel.serializers.roles.base import RoleSerializer


class MaintainerSerializer(RoleSerializer):
    """
    Serializer for Maintainer objects
    """

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
