import swapper

from kernel.admin.site import omnipotence
from kernel.models import (
    ContactInformation,
    LocationInformation,
    SocialInformation,
    SocialLink,
)

# Load all swappable models

Person = swapper.load_model('kernel', 'Person')

BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')
FinancialInformation = swapper.load_model('kernel', 'FinancialInformation')
PoliticalInformation = swapper.load_model('kernel', 'PoliticalInformation')
ResidentialInformation = swapper.load_model('kernel', 'ResidentialInformation')

Department = swapper.load_model('kernel', 'Department')
Centre = swapper.load_model('kernel', 'Centre')
Branch = swapper.load_model('kernel', 'Branch')
Course = swapper.load_model('kernel', 'Course')
Degree = swapper.load_model('kernel', 'Degree')
Residence = swapper.load_model('kernel', 'Residence')

Student = swapper.load_model('kernel', 'Student')
FacultyMember = swapper.load_model('kernel', 'FacultyMember')
Maintainer = swapper.load_model('kernel', 'Maintainer')

# Register all models
# If any are being overridden, they will show up separately in the Django admin

omnipotence.register(ContactInformation)
omnipotence.register(LocationInformation)
omnipotence.register(SocialInformation)
omnipotence.register(SocialLink)

omnipotence.register(Person)

omnipotence.register(BiologicalInformation)
omnipotence.register(FinancialInformation)
omnipotence.register(PoliticalInformation)
omnipotence.register(ResidentialInformation)

omnipotence.register(Department)
omnipotence.register(Centre)
omnipotence.register(Branch)
omnipotence.register(Course)
omnipotence.register(Degree)
omnipotence.register(Residence)

omnipotence.register(Student)
omnipotence.register(FacultyMember)
omnipotence.register(Maintainer)
