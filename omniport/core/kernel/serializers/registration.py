KERNEL_BRANCH_SERIALIZER = (
    'kernel.serializers.institute.'
    'branch.BranchSerializer'
)
KERNEL_DEGREE_SERIALIZER = (
    'kernel.serializers.institute.'
    'degree.DegreeSerializer'
)
KERNEL_DEPARTMENT_SERIALIZER = (
    'kernel.serializers.institute.'
    'department.DepartmentSerializer'
)
KERNEL_RESIDENCE_SERIALIZER = (
    'kernel.serializers.institute.'
    'residence.ResidenceSerializer'
)

KERNEL_STUDENT_SERIALIZER = (
    'kernel.serializers.roles.'
    'student.StudentSerializer'
)
KERNEL_FACULTYMEMBER_SERIALIZER = (
    'kernel.serializers.roles.'
    'faculty_member.FacultyMemberSerializer'
)
KERNEL_MAINTAINER_SERIALIZER = (
    'kernel.serializers.roles.'
    'maintainer.MaintainerSerializer'
)
KERNEL_GUEST_SERIALIZER = (
    'kernel.serializers.roles.'
    'guest.GuestSerializer'
)
KERNEL_JOINTFACULTYMEMBERSHIP_SERIALIZER = (
    'kernel.serializers.roles.'
    'joint_faculty.JointFacultyMembershipSerializer'
)
KERNEL_JOINTFACULTY_SERIALIZER = (
    'kernel.serializers.roles.'
    'joint_faculty.JointFacultySerializer'
)

KERNEL_BIOLOGICALINFORMATION_SERIALIZER = (
    'kernel.serializers.personal_information.'
    'biological_information.BiologicalInformationSerializer'
)
KERNEL_FINANCIALINFORMATION_SERIALIZER = (
    'kernel.serializers.personal_information.'
    'financial_information.FinancialInformationSerializer'
)
KERNEL_POLITICALINFORMATION_SERIALIZER = (
    'kernel.serializers.personal_information.'
    'political_information.PoliticalInformationSerializer'
)
KERNEL_RESIDENTIALINFORMATION_SERIALIZER = (
    'kernel.serializers.personal_information.'
    'residential_information.ResidentialInformationSerializer'
)

KERNEL_PERSON_PROFILE_SERIALIZER = (
    'kernel.serializers.'
    'person.ProfileSerializer'
)

KERNEL_PERSON_AVATAR_SERIALIZER = (
    'kernel.serializers.'
    'person.AvatarSerializer'
)

KERNEL_COURSE_SERIALIZER = (
    'kernel.serializers.institute.'
    'course.CourseSerializer'
)

__all__ = [
    'KERNEL_BRANCH_SERIALIZER',
    'KERNEL_DEGREE_SERIALIZER',
    'KERNEL_DEPARTMENT_SERIALIZER',
    'KERNEL_RESIDENCE_SERIALIZER',

    'KERNEL_STUDENT_SERIALIZER',
    'KERNEL_FACULTYMEMBER_SERIALIZER',
    'KERNEL_MAINTAINER_SERIALIZER',
    'KERNEL_GUEST_SERIALIZER',
    'KERNEL_JOINTFACULTYMEMBERSHIP_SERIALIZER',
    'KERNEL_JOINTFACULTY_SERIALIZER',


    'KERNEL_BIOLOGICALINFORMATION_SERIALIZER',
    'KERNEL_FINANCIALINFORMATION_SERIALIZER',
    'KERNEL_POLITICALINFORMATION_SERIALIZER',
    'KERNEL_RESIDENTIALINFORMATION_SERIALIZER',

    'KERNEL_PERSON_PROFILE_SERIALIZER',
    'KERNEL_PERSON_AVATAR_SERIALIZER',
    'KERNEL_COURSE_SERIALIZER'
]
