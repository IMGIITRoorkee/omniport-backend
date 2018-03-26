from django import forms as django_forms
from django.conf import settings
from django.contrib.admin import sites, forms

from kernel.utils.rights import has_omnipotence_rights


class OmniportAdminAuthenticationForm(forms.AdminAuthenticationForm):
    """
    Extends the default AdminAuthenticationForm provided by Django to modify the
    permission check method
    """

    def confirm_login_allowed(self, user):
        """
        Replace the check for is_staff with has_omnipotence_rights
        :param user: the user whose login privileges are being checked
        :raise: ValidationError if the user is not privileged enough
        """

        if not user.is_active or not has_omnipotence_rights(user):
            raise django_forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


class OmniportAdminSite(sites.AdminSite):
    """
    Extends the default AdminSite provided by Django to modify
    - the branding throughout the site
    - the authentication form used to login
    - the permission framework
    """

    site_header = f'{settings.SITE_VERBOSE_NAME} administration'
    site_title = f'{settings.SITE_VERBOSE_NAME} administration'
    index_title = f'{settings.SITE_VERBOSE_NAME} administration'

    login_form = OmniportAdminAuthenticationForm

    def has_permission(self, request):
        """
        Replace the check for is_staff with has_omnipotence_rights
        :param request: the request whose user is to be checked for permissions
        :return: True if the user of the request is active and privileged enough
        """

        return request.user.is_active and has_omnipotence_rights(request.user)


omnipotence = OmniportAdminSite(name='omniport_admin_site')
