import swapper
from django.contrib.admin.sites import AlreadyRegistered

from omniport.admin.site import omnipotence

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
Guest = swapper.load_model('kernel', 'Guest')

models = [
    Person,
    BiologicalInformation,
    FinancialInformation,
    PoliticalInformation,
    ResidentialInformation,
    Department,
    Centre,
    Branch,
    Course,
    Degree,
    Residence,
    Student,
    FacultyMember,
    Maintainer,
    Guest,
]

# Register all models
# If any are being swapped, they will show up separately in the Django admin

for model in models:
    try:
        omnipotence.register(model)
    except AlreadyRegistered:
        # A custom ModelAdmin has already registered it
        pass
