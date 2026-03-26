from kernel.models.institute import (
    # Abstract models for customised implementations
    AbstractDepartment,
    AbstractCentre,
    AbstractBranch,
    AbstractCourse,
    AbstractDegree,
    AbstractResidence,

    # Concrete models for default implementation
    Department,
    Centre,
    Branch,
    Course,
    Degree,
    Residence,
)
from kernel.models.person import (
    # Abstract models for customised implementations
    AbstractPerson,

    # Concrete models for default implementation
    Person,
)
from kernel.models.personal_information import (
    # Abstract models for customised implementations
    AbstractBiologicalInformation,
    AbstractPoliticalInformation,
    AbstractFinancialInformation,
    AbstractResidentialInformation,

    # Concrete models for default implementation
    BiologicalInformation,
    FinancialInformation,
    PoliticalInformation,
    ResidentialInformation,
)
from kernel.models.roles import (
    # Abstract models for customised implementations
    AbstractStudent,
    AbstractFacultyMember,
    AbstractJointFaculty,
    AbstractJointFacultyMembership,
    AbstractNonTeachingStaff,

    # Concrete models for default implementation
    Student,
    FacultyMember,
    Guest,
    JointFaculty,
    JointFacultyMembership,
    NonTeachingStaff,
)
