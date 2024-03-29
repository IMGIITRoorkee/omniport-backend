import re
import swapper
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from oauth2_provider.models import AbstractApplication
from pydash import py_
from rest_framework import serializers

from kernel.relations.person import PersonRelatedField
from omniport.utils import switcher
from open_auth.constants import data_points as data_point_constants
from open_auth.models import Application

Person = swapper.load_model('kernel', 'Person')

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')


class ApplicationListSerializer(serializers.ModelSerializer):
    """
    Serializer for Application objects that exposes minimal information
    """

    class Meta:
        """
        Meta class for ApplicationListSerializer
        """

        model = Application
        fields = [
            'id',
            'name',
            'logo',
            'is_approved',
        ]


class ApplicationAuthoriseSerializer(serializers.ModelSerializer):
    """
    Serializer for Application objects that exposes only the information that
    user needs to Allow or Deny an application
    """

    class Meta:
        """
        Meta class for ApplicationAuthoriseSerializer
        """

        model = Application
        fields = [
            'client_id',
            'redirect_uris',
            'name',
            'logo',
            'skip_authorization',
            'data_points',
        ]

    def to_representation(self, instance):
        """
        Replace the array of data point codes in the serialized data with a
        dictionary mapping codes to their display names
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        data_points = representation.pop('data_points')
        data_point_tuples = py_.filter(
            data_point_constants.DATA_POINTS,
            lambda tup: tup[0] in data_points
        )
        data_point_map = dict()
        for (code, name) in data_point_tuples:
            data_point_map[code] = name
        representation['data_points'] = data_point_map

        return representation


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Application objects that exposes all information
    """

    team_members = PersonRelatedField(
        queryset=Person.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        """
        Meta class for ApplicationDetailSerializer
        """

        model = Application
        read_only_fields = [
            'is_approved',
            'client_id',
            'authorization_grant_type',
            'datetime_created',
        ]
        exclude = [
            'created',
            'datetime_modified',
            'updated',
            'skip_authorization',
            'user',
            'client_secret',
        ]

    def validate_description(self, value):
        """
        Validate the value submitted for the field 'description'
        :param value: the value submitted by the user
        :return: the value, if validation passes
        :raise: ValidationError, if validation fails
        """

        word_count = len(py_.words(value))

        if word_count < 127:
            raise serializers.ValidationError('Use a minimum of 127 words.')
        if word_count > 511:
            raise serializers.ValidationError('Use a maximum of 511 words.')

        return value

    def validate_redirect_uris(self, value):
        """
        Validate the value submitted for the field 'redirect_uris'
        :param value: the value submitted by the user
        :return: the value if validation passes
        :raise: ValidationError, if validation fails
        """

        redirect_urls = value.split(' ')
        instance = self.instance

        # Use initial_data as validated_data might not be available here
        data = self.initial_data

        application_name = data.get('name', None)
        if application_name is None:
            application_name = instance.name if instance else None

        # Regex for valid characters in application_slug for custom scheme
        schema_re = '[^A-Za-z0-9]+'

        # Default schemes
        schemes = ['http', 'https', 'ftp', 'ftps']

        # Substitute all special characters in application name
        # and add it valid schemes list
        application_slug = re.sub(schema_re, '', application_name)
        schemes.append(application_slug.lower())

        for url in redirect_urls:
            validator = URLValidator(schemes=schemes)
            validator(url)

        return value

    def validate_agrees_to_terms(self, value):
        """
        Validate the value submitted for the field 'agrees_to_terms'
        :param value: the value submitted by the user
        :return: the value if validation passes
        :raise: ValidationError, if validation fails
        """

        if not value:
            raise serializers.ValidationError('Agree to terms of use.')

        return value

    def to_representation(self, instance):
        """
        Convert the team member IDs from the PersonRelatedField to their
        corresponding AvatarSerializer serialized instances
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        # Convert team_member PKs to expanded dictionaries
        team_members = [
            AvatarSerializer(Person.objects.get(pk=team_member)).data
            for team_member in representation.get('team_members')
        ]
        representation['team_members'] = team_members

        return representation

    def create(self, validated_data):
        """
        Create a new Application instance from the validated data, adding user
        and team members from the currently logged-in user
        :param validated_data: the validated data passed to the serializer
        :return: the newly-created Application instance
        """

        user = self.context.get('request').user
        authorization_grant_type = AbstractApplication.GRANT_AUTHORIZATION_CODE

        validated_data['user'] = user
        validated_data['authorization_grant_type'] = authorization_grant_type
        validated_data['agrees_to_terms'] = True
        application = super().create(validated_data)

        person = self.context.get('request').person
        application.team_members.add(person)

        return application

    def update(self, instance, validated_data):
        """
        Remove the create-only fields from the validated data and defer to the
        base implementation of the method
        :param instance: the application instance being updated
        :param validated_data: the validated data passed to the serializer
        :return: whatever super().update() returns
        """

        # Ensure that the creator of the app cannot leave the team
        if 'team_members' in validated_data:
            validated_data['team_members'].append(instance.user.person)

        validated_data['agrees_to_terms'] = True
        application = super().update(instance, validated_data)

        return application


class ApplicationHiddenDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Application objects that exposes all information
    """

    class Meta:
        """
        Meta class for ApplicationDetailSerializer
        """

        model = Application
        fields = ['client_secret']
        read_only_fields = ['client_secret']
