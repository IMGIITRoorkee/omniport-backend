from enum import auto, Flag


class ActiveStatus(Flag):
    """
    These flags describe the active status of the model in question
    """

    # Base flags
    HAS_BEEN_ACTIVE = auto()
    IS_ACTIVE = auto()
    WILL_BE_ACTIVE = auto()

    # Aliases
    IS_INACTIVE = ~IS_ACTIVE
    ANY = HAS_BEEN_ACTIVE | IS_ACTIVE | WILL_BE_ACTIVE
    NONE = 0
