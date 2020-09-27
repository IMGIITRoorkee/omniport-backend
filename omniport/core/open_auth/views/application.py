from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action

from django.http import HttpResponse
from open_auth.models import Application
from open_auth.serializers.application import ApplicationAuthoriseSerializer
from oauth2_provider.exceptions import OAuthToolkitError
from oauth2_provider.models import get_application_model,get_access_token_model
from oauth2_provider.scopes import get_scopes_backend
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views import AuthorizationView

class ApplicationViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for R operations on Application
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ApplicationAuthoriseSerializer
    queryset = Application.objects.filter(is_approved=True)
    lookup_field = 'client_id'
    pagination_class = None

    """
    Action view for getting the availabilty of token 
    for a particular view in order to skip authorization
    after first consent
    """
    @action(methods=['get'], detail=False, url_name="get_token", url_path="get_token")
    def get_token(self, request):
        
        token=get_access_token_model().objects.filter(
            user=request.user,
            application=request.GET.get('id')   
        ).exists()

        
        return HttpResponse(token)




class OmniportAuthorizationView(AuthorizationView):
    """
    Overrided the default implementation
    of get method of AuthorizationView in order
    to skip authorization even after the access
    token has expired.
    """
    def get(self, request, *args, **kwargs):
        
        """
        The code is similar to https://github.com/jazzband/django-oauth-toolkit/blob/master/oauth2_provider/views/base.py
        Significant Changes marked with *** in the code
         
        """
        try:
            require_approval = request.GET.get(
                "approval_prompt",
                oauth2_settings.REQUEST_APPROVAL_PROMPT,
            )
            
            if require_approval != 'auto_even_if_expired':
                return super(OmniportAuthorizationView, self).get(request, *args, **kwargs)

            scopes, credentials = self.validate_authorization_request(request)
            all_scopes = get_scopes_backend().get_all_scopes()
            kwargs["scopes_descriptions"] = [all_scopes[scope] for scope in scopes]
            kwargs['scopes'] = scopes

            # at this point we know an Application instance with such client_id exists in the database
            application = get_application_model().objects.get(client_id=credentials['client_id'])
            kwargs['application'] = application
            kwargs['client_id'] = credentials['client_id']
            kwargs['redirect_uri'] = credentials['redirect_uri']
            kwargs['response_type'] = credentials['response_type']
            kwargs['state'] = credentials['state']

            self.oauth2_data = kwargs
            # following two loc are here only because of https://code.djangoproject.com/ticket/17795
            form = self.get_form(self.get_form_class())
            kwargs['form'] = form
            
            """
             If skip_authorization field is True, skip the authorization screen even
             if this is the first use of the application and there was no previous authorization.
             This is useful for in-house applications-> assume an in-house applications
             are already approved.
            """
            
            if application.skip_authorization:
                uri, headers, body, status = self.create_authorization_response(
                    request=self.request, scopes=" ".join(scopes),
                    credentials=credentials, allow=True)
                return self.redirect(uri, application)

            #check for require_approval

            assert require_approval == 'auto_even_if_expired'
            tokens = (
                    get_access_token_model()
                    .objects.filter(
                        user=request.user,
                        application=kwargs["application"],
                        #expires__gt=timezone.now(),  ***
                    )
                    .all()
                )

            # check past authorizations regarded the same scopes as the current one
            for token in tokens:
                if token.allow_scopes(scopes):
                    uri, headers, body, status = self.create_authorization_response(
                        request=self.request, scopes=" ".join(scopes),
                        credentials=credentials, allow=True)
                    return self.redirect(uri, application)

            # render an authorization prompt so the user can approve
            # the application's requested scopes
            return self.render_to_response(self.get_context_data(**kwargs))

        except OAuthToolkitError as error:
            return self.error_response(error)