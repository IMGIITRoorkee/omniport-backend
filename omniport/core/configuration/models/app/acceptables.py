from formula_one.enums.active_status import ActiveStatus


class Role:
    """
    This class stores information about the roles acceptable to an app, namely
    the role name and the active statuses of the said role
    """

    def __init__(self, *args, **kwargs):
        """
        Create a Role instance from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.name = dictionary.get('name')

        active_statuses = dictionary.get('activeStatuses')
        if active_statuses is None:
            self.active_status = ActiveStatus.ANY
        else:
            self.active_status = ActiveStatus.NONE
            for active_status in active_statuses:
                self.active_status |= ActiveStatus[active_status]  # Enum OR


class Acceptables:
    """
    This class stores information about an app's acceptables, namely the
    acceptable roles and the acceptable IP address rings
    """

    def __init__(self, *args, **kwargs):
        """
        Create an Acceptables instance from a dictionary
        :param args: arguments
        :param kwargs: keyword arguments, including 'dictionary'
        """

        super().__init__()

        dictionary = kwargs.get('dictionary') or dict()
        self.roles = [
            Role(
                dictionary=role
            )
            for role in dictionary.get('roles') or []
        ]
        self.ip_address_rings = dictionary.get('ipAddressRings')
