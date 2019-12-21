import swapper

from kernel.serializers.roles.base import RoleSerializer

class GuestSerializer(RoleSerializer):
    """
    Serializer for Guest Object
    """

    class Meta:
        """
        Meta class for guests
        """

        model = swapper.load_model('kernel', 'Guest')

        fields = [
            'id',
            'person',
        ]
