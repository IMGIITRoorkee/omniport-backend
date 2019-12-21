import swapper
from django.contrib import admin

from formula_one.admin.model_admins.base import ModelAdmin
from omniport.admin.site import omnipotence

FacultyMember = swapper.load_model('kernel', 'FacultyMember')


@admin.register(FacultyMember, site=omnipotence)
class FacultyMemberAdmin(ModelAdmin):
    """
    This class controls the behaviour of FacultyMember in Omnipotence
    """

    search_fields = [
        'employee_id',
        'person__full_name'
    ]
