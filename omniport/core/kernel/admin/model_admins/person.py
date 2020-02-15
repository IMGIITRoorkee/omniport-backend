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
    This class implements ContactInformation inline for Person in Omnipotence
    """

    model = ContactInformation


class LocationInformationInline(BaseGenericRelationsInline):
    """
    This class implements LocationInformation inline for Person in Omnipotence
    """

    model = LocationInformation


class SocialInformationInline(BaseGenericRelationsInline):
    """
    This class implements SocialInformation inline for Person in Omnipotence
    """

    model = SocialInformation


class BiologicalInformationInline(admin.TabularInline):
    """
    This class implements BiologicalInformation inline for Person in
    Omnipotence
    """

    model = BiologicalInformation


class FinancialInformationInline(admin.TabularInline):
    """
    This class implements FinancialInformation inline for Person in Omnipotence
    """

    model = FinancialInformation


class PoliticalInformationInline(admin.TabularInline):
    """
    This class implements PoliticalInformation inline for Person in Omnipotence
    """

    model = PoliticalInformation


class ResidentialInformationInline(admin.TabularInline):
    """
    This class implements ResidentialInformation inline for Person in
    Omnipotence
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

