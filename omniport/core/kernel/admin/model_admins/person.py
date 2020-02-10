import swapper
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from formula_one.admin.model_admins.base import ModelAdmin
from formula_one.models import (
    ContactInformation,
    LocationInformation,
    SocialInformation
)
from omniport.admin.site import omnipotence

Person = swapper.load_model('kernel', 'Person')
BiologicalInformation = swapper.load_model('kernel', 'BiologicalInformation')
FinancialInformation = swapper.load_model('kernel', 'FinancialInformation')
PoliticalInformation = swapper.load_model('kernel', 'PoliticalInformation')
ResidentialInformation = swapper.load_model('kernel', 'ResidentialInformation')


class BaseGenericRelationsInline(GenericTabularInline):
    """
    This is the base class inherited by all classes implementing
    inline generic relation in admin page
    """

    ct_field = 'entity_content_type'
    ct_fk_field = 'entity_object_id'
    fk_name = 'entity'
    max_num = 1


class ContactInformationInline(BaseGenericRelationsInline):
    """
    This class implements Contact Information Inline for Person in omnipotence
    """

    model = ContactInformation


class LocationInformationInline(BaseGenericRelationsInline):
    """
    This class implements Location Information Inline for Person in omnipotence
    """

    model = LocationInformation


class SocialInformationInline(BaseGenericRelationsInline):
    """
    This class implements Social Information Inline for Person in omnipotence
    """

    model = SocialInformation


class BiologicalInformationInline(admin.TabularInline):
    """
    This class implements Biological Information Inline for Person in
    omnipotence
    """

    model = BiologicalInformation


class FinancialInformationInline(admin.TabularInline):
    """
    This class implements Financial Information Inline for Person in omnipotence
    """

    model = FinancialInformation


class PoliticalInformationInline(admin.TabularInline):
    """
    This class implements Political Information Inline for Person in omnipotence
    """

    model = PoliticalInformation


class ResidentialInformationInline(admin.TabularInline):
    """
    This class implements Residential Information Inline for Person in
    omnipotence
    """

    model = ResidentialInformation


@admin.register(Person, site=omnipotence)
class PersonAdmin(ModelAdmin):
    """
    This class controls the behaviour of Person in Omnipotence
    """

    search_fields = [
        'full_name',
        'short_name',
    ]
    inlines = [
        ContactInformationInline,
        LocationInformationInline,
        SocialInformationInline,
        BiologicalInformationInline,
        FinancialInformationInline,
        PoliticalInformationInline,
        ResidentialInformationInline,
    ]

