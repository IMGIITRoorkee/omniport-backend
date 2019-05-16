import swapper
from django.contrib import admin

from formula_one.admin.model_admins.base import ModelAdmin
from omniport.admin.site import omnipotence

Person = swapper.load_model('kernel', 'Person')


@admin.register(Person, site=omnipotence)
class PersonAdmin(ModelAdmin):
    """
    This class controls the behaviour of Person in Omnipotence
    """

    search_fields = [
        'full_name',
        'short_name',
    ]
