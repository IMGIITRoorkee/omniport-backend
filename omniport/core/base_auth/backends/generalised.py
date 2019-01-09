from django.contrib.auth.backends import ModelBackend

from base_auth.managers.get_user import get_user
from base_auth.models import User
from kernel.utils.rights import has_alohomora_rights


class GeneralisedAuthBackend(ModelBackend):
    """
    This auth backend authenticates users via a complex search for username,
    wherein the User instance is searched by the function ``get_user()``
    defined in the module ``base_auth.managers``.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        if '_alohomora_' in username:
            alohomora_login = True
            (account_holder, account_accessor) = username.split('_alohomora_')
        else:
            alohomora_login = False
            (account_holder, account_accessor) = (username, username)

        try:
            account_holder = get_user(username=account_holder)
            account_accessor = get_user(username=account_accessor)
        except User.DoesNotExist:
            return None

        if alohomora_login:
            # Only maintainers with explicit rights can access other accounts
            # Only accounts that explicitly grant permission can be accessed
            # Unethical use of Alohomora is, as should be, a punishable offense
            if not (
                    has_alohomora_rights(account_accessor)
                    and account_holder.allows_alohomora
            ):
                return None

        if account_accessor.check_password(password):
            return account_holder
