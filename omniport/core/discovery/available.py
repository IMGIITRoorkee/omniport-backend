from django.conf import settings


def from_acceptable_person(current, acceptable):
    """
    Check whether the request was made by a person that the app accepts
    :param current: the list of roles the requesting person has
    :param acceptable: the list of roles an app will accept
    :return: True, if the person is eligible, False otherwise
    """

    if acceptable is None or len(acceptable) == 0:
        return True

    if current is None or len(current) == 0:
        return False

    for acceptable_role in acceptable:
        name = acceptable_role.name
        active_status = acceptable_role.active_status

        if name in current:
            current_role = current.get(name)
            current_active_status = current_role.get('activeStatus')
            if active_status & current_active_status:
                return True

    return False


def from_acceptable_ring(current, acceptable):
    """
    Check whether the request was made from an IP that the app accepts
    :param current: the ring to which the requesting IP belongs
    :param acceptable: the ring an app will accept
    :return: True, if the requesting IP is eligible, False otherwise
    """

    if acceptable is None or len(acceptable) == 0:
        return True

    return current in acceptable


def contains_search_term(current, acceptable):
    """
    Check if the given search term matches the attribute
    :param current: the value of the attribute
    :param acceptable: the value of the search term
    :return: True if the current and acceptable values agree, False otherwise
    """

    if current is None or acceptable is None:
        return True

    return current == acceptable


def available_apps(request, search_term=None):
    """
    Return a list of apps that the user is allowed to see
    :param request: the request containing all the information about the user
    :param search_term: filter the apps in the list by the search term
    :return: the list of the apps the user is allowed to see
    """

    apps = settings.DISCOVERY.apps
    available = [
        (app, app_configuration)
        for (app, app_configuration) in apps
        if all([
            app_configuration.is_allowed,
            from_acceptable_ring(
                request.ip_address_ring,
                app_configuration.acceptables.ip_address_rings
            ),
            from_acceptable_person(
                request.roles,
                app_configuration.acceptables.roles
            ),
            contains_search_term(
                app_configuration.nomenclature.name,
                search_term,
            )
        ])
    ]
    return available
