import re

from django.conf import settings
from django.http import Http404

from base_auth.managers.get_user import get_user
from discovery.available import from_acceptable_person

class RoutesControlRoles:
    """
    Handles the routing of apps for the guest role and restricts
    the guest user to the allowed urls of an app only
    """
    def __init__(self, get_response):
        """
        __init__function exactly as the Django documentation says for
        a custom middleware
        """
        self.get_response = get_response

    def __call__(self, request):

        source_user = request.user
        
        try:
            guest_user = get_user(settings.GUEST_USERNAME)
        except User.DoesNotExist:
            guest_user = None

        if source_user == guest_user:
            """
            Perform actual processing on the request before it goes to the view
            and on response returned by the view
            :param request: the request being processed
            :return: the processed response
            """
            if request.method == 'GET':
                DISCOVERY = settings.DISCOVERY

                all_apps = DISCOVERY.apps

                for app, app_configuration in all_apps:
                    base_url = app_configuration.base_urls.http.strip('/')
                    if (app_configuration.guest_allowed or
                    from_acceptable_person(request.roles, 
                    app_configuration.acceptables.roles)):
                        excluded_paths = app_configuration.excluded_paths
                        for excluded_path in excluded_paths:
                            if re.match(f'^/{base_url}/{excluded_path}/', request.path):
                                raise Http404
                    else:
                        if re.match(f'^/{base_url}/', request.path):
                            raise Http404
            else:
                raise Http404
        response = self.get_response(request)

        return response
