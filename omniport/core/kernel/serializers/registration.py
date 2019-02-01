KERNEL_RESIDENCE_SERIALIZER = (
    'kernel.serializers.institute.'
    'residence.ResidenceSerializer'
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

__all__ = [
    'KERNEL_RESIDENCE_SERIALIZER',
    'KERNEL_BIOLOGICALINFORMATION_SERIALIZER',
    'KERNEL_FINANCIALINFORMATION_SERIALIZER',
    'KERNEL_POLITICALINFORMATION_SERIALIZER',
    'KERNEL_RESIDENTIALINFORMATION_SERIALIZER',
]
