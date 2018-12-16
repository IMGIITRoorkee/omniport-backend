import datetime

from session_auth.models import SessionMap


class LastSeen:
    """
    Set the datetime_modified attribute of the SessionMap object if request is
    authenticated
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
            try:
                session_key = request.session.session_key
                if session_key is not None and not session_key == '':
                    try:
                        session_map = SessionMap.objects.get(
                            session_key=session_key
                        )
                        session_map.datetime_modified = datetime.datetime.now()
                        session_map.save()
                    except SessionMap.DoesNotExist:
                        SessionMap.create_session_map(request)
            except AttributeError:
                pass

        response = self.get_response(request)

        return response
