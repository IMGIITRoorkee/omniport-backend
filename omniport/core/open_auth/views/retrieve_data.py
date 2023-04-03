from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import AccessToken

from kernel.models import Person
from open_auth.utils import (
    get_field_data,
    get_roles,
    get_custom_roles,
    get_display_picture,
)

MODEL_REGEX = [
    'person',
    'student',
    'faculty_member',
    'biological_information',
    'contact_information',
    'residential_information'
]
MODEL_STRINGS = [
    'person',
    'person.student',
    'person.facultymember',
    'person.biologicalinformation',
    'person.contact_information.first()',
    'person.residentialinformation'
]


class GetUserData(generics.GenericAPIView):
    """
    View to retrieve data for OAuth based applications
    """

    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        View to serve GET requests
        :param request: the request that is to be responded to
        :return: the response for request
        """

        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        if token == '':
            return Response(
                data="Please prvide the access\
                 token in the Authorization header",
                status=status.HTTP_400_BAD_REQUEST
            )

        access_token = AccessToken.objects.get(token=token)
        application = access_token.application

        if application is None:
            return Response(
                data="Associated application not found",
                status=status.HTTP_404_NOT_FOUND
            )

        app_data_points = application.data_points
        user = request.user
        response_data = dict()

        try:
            person = user.person
        except Person.DoesNotExist:
            response_data['user_id'] = user.id
            return Response(
                data=response_data,
                status=status.HTTP_200_OK
            )

        response_data['user_id'] = user.id

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
            try:
                response_data['person']['roles'] = get_roles(person)
            except KeyError:
                response_data['person'] = dict()
                response_data['person']['roles'] = get_roles(person)

        if 'person.custom_roles' in app_data_points:
            response_data['person']['custom_roles'] = get_custom_roles(person)

        if 'person.display_picture' in app_data_points:
            try:
                response_data['person']['display_picture'] = \
                    get_display_picture(person)
            except KeyError:
                response_data['person'] = dict()
                response_data['person']['display_picture'] = get_display_picture(person)

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
