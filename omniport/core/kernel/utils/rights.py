"""
These functions are an essential part of the rights framework used by Omniport.
They determine which users have access to the administrative features of the
project, which are:

- omnipotence
    The admin interface of the project which is a heavily customised
    implementation of the default Django administration view

- alohomora
    The impersonation ability of maintainers to access the account of any user
    with their explicit permission, to be used strictly for debugging purposes
    under a strict oath of ethical behaviour

- lockpicking
    The no-questions-asked password reset ability which is used by maintainers
    to reset the password of forgetful people upon request after verifying the
    identity of the requester

- helpcentre
    The ability to access and answer user queries using the special Helpcentre
    service, which is also a bug tracker and ticketing system

These can, and most probably should, be overridden in shell.utils.rights
"""

from kernel.permissions.omnipotence import has_omnipotence_rights
from kernel.permissions.polyjuice import has_polyjuice_rights
from kernel.permissions.alohomora import has_alohomora_rights
from kernel.permissions.helpcentre import has_helpcentre_rights
