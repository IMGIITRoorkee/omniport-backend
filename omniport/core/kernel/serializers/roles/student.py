import swapper

from kernel.serializers.roles.base import RoleSerializer
from omniport.utils import switcher

BranchSerializer = switcher.load_serializer('kernel', 'Branch')


class StudentSerializer(RoleSerializer):
    """
    Serializer for Student objects
    """

    branch = BranchSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for StudentSerializer
        """

        model = swapper.load_model('kernel', 'Student')

        fields = [
            'id',
            'person',
            'branch',
            'current_year',
            'current_semester',
        ]
