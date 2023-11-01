import swapper

from formula_one.serializers.base import ModelSerializer
from omniport.utils import switcher

DepartmentSerializer = switcher.load_serializer('kernel', 'Department')


class CourseSerializer(ModelSerializer):
    """
    Serializer for Course objects
    """

    department = DepartmentSerializer(
        read_only=True,
    )

    class Meta:
        """
        Meta class for CourseSerializer
        """

        model = swapper.load_model('kernel', 'Course')

        fields = [
            'id',
            'code',
            'name',
            'credits',
            'department',
        ]
