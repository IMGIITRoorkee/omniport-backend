from kernel.managers.get_role import get_all_roles


class PersonRoles:
    """
    Set the person attribute on the request object pointing to the person
    attached to the user and the roles attribute on the request object
    containing a list of all roles the person has been assigned
    """

    def __init__(self, get_response):
        """
        Write the __init__ function exactly as the Django documentations says
        """

        self.get_response = get_response

    def __call__(self, request):
        """
        Perform the actual processing on the request before it goes to the view
        and on the response returned by the view
        :param request: the request being processed
        :return: the processed response
        """

        if request.user and request.user.is_authenticated:
            person = request.user.person
            request.person = person
            request.roles = get_all_roles(person)
        else:
            request.person = None
            request.roles = None

        response = self.get_response(request)

        return response
