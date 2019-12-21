import swapper
from django.contrib import admin

from formula_one.admin.model_admins.base import ModelAdmin
from omniport.admin.site import omnipotence

Branch = swapper.load_model('kernel', 'Branch')


@admin.register(Branch, site=omnipotence)
class BranchAdmin(ModelAdmin):
    """
    This class controls the behaviour of Branch in Omnipotence
    """

    search_fields = [
        'name'
    ]
