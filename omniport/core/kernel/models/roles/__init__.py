from django.conf import settings

from kernel.models.roles.faculty_member import (
    AbstractFacultyMember,

    FacultyMember,
)
from kernel.models.roles.maintainer import (
    AbstractMaintainer,

    Maintainer,
)
from kernel.models.roles.student import (
    AbstractStudent,

    Student,
)
from kernel.models.roles.guest_role import (
    Guest,
)
from kernel.models.roles.joint_faculty import (
    AbstractJointFacultyMembership,
    AbstractJointFaculty,

    JointFacultyMembership,
    JointFaculty,
)
from kernel.models.roles.nonteaching_staff import (
    AbstractNonTeachingStaff,

    NonTeachingStaff,
)

# Add the names of roles to the list maintained in settings
settings.ROLES.extend([
    'Student',
    'FacultyMember',
    'Maintainer',
    'Guest',
    'JointFaculty',
    'NonTeachingStaff',
])
