import swapper

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

# Register all models
# If any are being overridden, they will show up separately in the Django admin
omnipotence.register(User)

omnipotence.register(Person)
omnipotence.register(BiologicalInformation)
omnipotence.register(FinancialInformation)
omnipotence.register(PoliticalInformation)

omnipotence.register(ContactInformation)
omnipotence.register(LocationInformation)
