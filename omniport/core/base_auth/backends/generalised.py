from django.contrib.auth.backends import ModelBackend

from base_auth.managers.get_user import get_user
from base_auth.models import User
from kernel.utils.rights import has_alohomora_rights


class GeneralisedAuthBackend(ModelBackend):
    """
    This auth backend authenticates users via a complex relation for username,
    wherein the User instance is searched by the get_user function defined in
    the kernel.utils file.

    This auth backend also has Alohomora support baked right in, so that
    debugging and helping users is easy. This backend allows
    accessor-authenticated Alohomora, which is more secure than shared password
    Alohomora which requires big changes if that password gets leaked. Also this
    method restricts Alohomora access to users explicitly granted that right.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        if '_alohomora_' in username:
            (account_holder, account_accessor) = username.split('_alohomora_')
        else:
            (account_holder, account_accessor) = (username, username)

        try:
            account_holder = get_user(username=account_holder)
            account_accessor = get_user(username=account_accessor)
        except User.DoesNotExist:
            return None

        if (
                '_alohomora_' in username
                and not has_alohomora_rights(account_accessor)
        ):
            return None

        if account_accessor.check_password(password):
            return account_holder
