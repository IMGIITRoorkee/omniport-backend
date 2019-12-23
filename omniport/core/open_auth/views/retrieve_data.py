from rest_framework import status, generics
from rest_framework.response import Response

from oauth2_provider.models import AccessToken

from open_auth.models import Application
from open_auth.utils import get_field_data, get_roles

model_regex = ['person', 'student', 'faculty_member', 'biological_information', 'contact_information']
model_strings = ['person', 'person.student', 'person.facultymember', 'person.biologicalinformation', 'person.contact_information.first()']

class GetUserData(generics.GenericAPIView):
    """
    View to retrieve data for oauth
    based applications.
    """

    def post(self, request, *args, **kwargs):
        """
        View to serve POST requests
        :param request: the request that is to be responded to
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the response for request
        """

        client_id = request.POST['client_id']
        token = request.POST['token']

        try:
            application = Application.objects.get(client_id=client_id)
            access_token = AccessToken.objects.get(token=token)
        except:
            return Response(
                data="Invalid Client Id or access token",
                status=status.HTTP_400_BAD_REQUEST
            )
        

        if not access_token.is_valid():
            return Response(
                data="Token entered is invalid",
                status=status.HTTP_400_BAD_REQUEST
            )
        
        elif access_token.is_expired():
            return Response(
                data="This token has expired",
                status=status.HTTP_401_UNAUTHORIZED
            )

        app_data_points = application.data_points
        user = access_token.user
        response_data = {}

        try:
            person = user.person
        except:
            response_data['username'] = user.username
            return Response(
                data=response_data,
                status=status.HTTP_200_OK
            )

        response_data['username'] = user.username

        for i in range(len(model_regex)):
            model_data_points = [x.split('.', 1)[1] for x in app_data_points if model_regex[i] in x and 'roles' not in x]
            try:
                if len(model_data_points) !=0:
                    response_data[model_regex[i]] = get_field_data(person, model_data_points, model_strings[i])
            except:
                response_data[model_regex[i]] = {}

        if 'person.roles' in app_data_points:
            response_data['person']['roles'] = get_roles(person)

        if 'social_information.links' in app_data_points:
            data = {}
            social_info = person.social_information.first()
            if social_info is not None:
                for link in social_info.links.all():
                    data[link.site] = link.url
            response_data['social_information'] = data

        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
