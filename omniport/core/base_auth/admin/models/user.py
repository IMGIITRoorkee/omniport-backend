from django import forms
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms

from base_auth.models import User


class UserChangeForm(forms.ModelForm):
    """
    Replicate the form shown when the user model supplied by Django is not
    replaced with our own by copying most of the code
    """

    username = auth_forms.UsernameField(
        help_text="This username is optional because authentication is "
                  "generalized to work with other attributes such as email "
                  "addresses and phone numbers.",
        required=False,
    )

    password = auth_forms.ReadOnlyPasswordHashField(
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>.",
    )
    secret_answer = auth_forms.ReadOnlyPasswordHashField(
        help_text="Raw answers are not stored, so there is no way to see "
                  "this user's answer, but you can change the answer "
                  "using the shell.",
    )

    class Meta:
        """
        Meta class for UserChangeForm
        """

        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]

    def clean_secret_answer(self):
        return self.initial["secret_answer"]


class UserAdmin(auth_admin.UserAdmin):
    """
    Customize the presentation of the model User in Omnipotence
    """

    form = UserChangeForm

    fieldsets = (
        ('Authentication', {
            'fields': (
                'username',
                'password',
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
            )
        }),
        ('Password reset', {
            'fields': (
                'secret_question',
                'secret_answer',
                'failed_reset_attempts',
                'allows_alohomora',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )
    add_fieldsets = (
        ('Authentication', {
            'fields': (
                'password1',
                'password2',
            )
        }),
    )

    list_display = (
        'username',
        'get_short_name',
        'get_full_name',
        'last_login',
        'is_superuser',
    )
    list_filter = tuple()

    search_fields = ['id', 'username', 'person__full_name', ]
