import swapper
from rest_framework import serializers

from kernel.serializers.roles.base import RoleSerializer
from omniport.utils import switcher

DepartmentSerializer = switcher.load_serializer('kernel', 'Department')


class JointFacultyMembershipSerializer(serializers.Serializer):
    """
    Serializer for JointFacultyMembership objects
    """

    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for JointFacultyMembershipSerializer
        """

        model = swapper.load_model('kernel', 'JointFacultyMembership')

        fields = [
            'department',
            'designation',
        ]


class JointFacultySerializer(RoleSerializer):
    """
    Serializer for JointFaculty objects
    """

    memberships = JointFacultyMembershipSerializer(many=True)


    class Meta:
        """
        Meta class for JointFacultySerializer
        """

        model = swapper.load_model('kernel', 'JointFaculty')

        fields = [
            'id',
            'person',
            'memberships',
        ]
