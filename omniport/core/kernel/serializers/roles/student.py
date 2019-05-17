import swapper

from kernel.serializers.institute.branch import BranchSerializer
from kernel.serializers.roles.base import RoleSerializer


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
