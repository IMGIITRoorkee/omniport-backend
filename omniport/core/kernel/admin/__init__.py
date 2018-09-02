import swapper
from django.contrib.auth.models import Group

from kernel.admin.site import omnipotence
from kernel.models import (
    User,
    ContactInformation,
    LocationInformation,
)

# Load all swappable models

Person = swapper.load_model('kernel', 'Person')

BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')
FinancialInformation = swapper.load_model('kernel', 'FinancialInformation')
PoliticalInformation = swapper.load_model('kernel', 'PoliticalInformation')

Department = swapper.load_model('kernel', 'Department')
Centre = swapper.load_model('kernel', 'Centre')
Branch = swapper.load_model('kernel', 'Branch')
Course = swapper.load_model('kernel', 'Course')

Student = swapper.load_model('kernel', 'Student')
FacultyMember = swapper.load_model('kernel', 'FacultyMember')
Maintainer = swapper.load_model('kernel', 'Maintainer')

# Register all models
# If any are being overridden, they will show up separately in the Django admin

omnipotence.register(User)
omnipotence.register(ContactInformation)
omnipotence.register(LocationInformation)

omnipotence.register(Person)

omnipotence.register(BiologicalInformation)
omnipotence.register(FinancialInformation)
omnipotence.register(PoliticalInformation)

omnipotence.register(Department)
omnipotence.register(Centre)
omnipotence.register(Branch)
omnipotence.register(Course)

omnipotence.register(Student)
omnipotence.register(FacultyMember)
omnipotence.register(Maintainer)
