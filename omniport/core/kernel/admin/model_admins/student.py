import swapper
from django.contrib import admin

from formula_one.admin.model_admins.base import ModelAdmin
from omniport.admin.site import omnipotence

Student = swapper.load_model('kernel', 'Student')


@admin.register(Student, site=omnipotence)
class StudentAdmin(ModelAdmin):
    """
    This class controls the behaviour of Student in Omnipotence
    """

    search_fields = [
        'enrolment_number',
        'person__full_name'
    ]
