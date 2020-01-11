from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.response import Response
from oauth2_provider.models import AccessToken

from kernel.models import Person
from open_auth.utils import get_field_data, get_roles, get_display_picture

MODEL_REGEX = [
    'person',
    'student',
    'faculty_member',
    'biological_information',
    'contact_information'
]
MODEL_STRINGS = [
    'person',
    'person.student',
    'person.facultymember',
    'person.biologicalinformation',
    'person.contact_information.first()'
]


class GetUserData(generics.GenericAPIView):
    """
    View to retrieve data for OAuth based applications
    """

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :return: the response for request
        """

        token = request.headers['Authorization'].replace('OAUTH_TOKEN ', '')

        try:
            access_token = AccessToken.objects.get(token=token)
            application = access_token.application
        except AccessToken.DoesNotExist:
            return Response(
                data="Please provide access token in the headers",
                status=status.HTTP_400_BAD_REQUEST
            )

        if not access_token.is_valid():
            return Response(
                data="Token entered is invalid",
                status=status.HTTP_400_BAD_REQUEST
            )

        if access_token.is_expired():
            return Response(
                data="This token has expired",
                status=status.HTTP_401_UNAUTHORIZED
            )

        app_data_points = application.data_points
        user = access_token.user
        response_data = dict()

        try:
            person = user.person
        except Person.DoesNotExist:
            response_data['username'] = user.username
            return Response(
                data=response_data,
                status=status.HTTP_200_OK
            )

        response_data['username'] = user.username

        for model_name, object_string in zip(MODEL_REGEX, MODEL_STRINGS):
            model_data_points = [
                data_point.split('.', 1)[1] for data_point in app_data_points
                if (
                        model_name in data_point and
                        'roles' not in data_point and
                        'display_picture' not in data_point
                )
            ]
            try:
                if model_data_points:
                    response_data[model_name] = \
                        get_field_data(
                        person,
                        model_data_points,
                        object_string
                    )
            except (ObjectDoesNotExist, AttributeError):
                response_data[model_name] = dict()

        if 'person.roles' in app_data_points:
            response_data['person']['roles'] = get_roles(person)

        if 'person.display_picture' in app_data_points:
            response_data['person']['display_picture'] = \
                get_display_picture(person)

        if 'social_information.links' in app_data_points:
            data = dict()
            social_info = person.social_information.first()
            if social_info is not None:
                for link in social_info.links.all():
                    data[link.site] = link.url
            response_data['social_information'] = data

        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
