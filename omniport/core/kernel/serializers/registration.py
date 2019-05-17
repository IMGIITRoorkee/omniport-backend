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

__all__ = [
    'KERNEL_RESIDENCE_SERIALIZER',

    'KERNEL_STUDENT_SERIALIZER',
    'KERNEL_FACULTYMEMBER_SERIALIZER',
    'KERNEL_MAINTAINER_SERIALIZER',

    'KERNEL_BIOLOGICALINFORMATION_SERIALIZER',
    'KERNEL_FINANCIALINFORMATION_SERIALIZER',
    'KERNEL_POLITICALINFORMATION_SERIALIZER',
    'KERNEL_RESIDENTIALINFORMATION_SERIALIZER',

    'KERNEL_PERSON_PROFILE_SERIALIZER',
    'KERNEL_PERSON_AVATAR_SERIALIZER',
]
