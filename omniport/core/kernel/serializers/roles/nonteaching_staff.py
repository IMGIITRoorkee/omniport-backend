import swapper

from kernel.serializers.roles.base import RoleSerializer

class NonTeachingStaffSerializer(RoleSerializer):
    """
    Serializer for NonTeachingStaff Object
    """

    class Meta:
        """
        Meta class for non-teaching staff
        """

        model = swapper.load_model('kernel', 'NonTeachingStaff')

        fields = [
            'id',
            'person',
        ]
