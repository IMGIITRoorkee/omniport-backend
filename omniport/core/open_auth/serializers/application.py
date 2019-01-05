import pydash as _
from django.core.validators import URLValidator
from oauth2_provider.models import AbstractApplication
from rest_framework import serializers

from kernel.admin import Person
from kernel.relations.person import PersonRelatedField
from kernel.serializers.person import AvatarSerializer
from open_auth.models import Application


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
            'client_secret',
            'authorization_grant_type',
        ]
        exclude = [
            'datetime_created',
            'datetime_modified',
            'skip_authorization',
            'user',
        ]

    def validate_description(self, value):
        """
        Validate the value submitted for the field 'description'
        :param value: the value submitted by the user
        :return: the value, if validation passes
        :raise: ValidationError, if validation fails
        """

        word_count = len(_.strings.words(value))

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

        validator = URLValidator()

        redirect_urls = value.split(' ')
        for url in redirect_urls:
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
        validated_data['user'] = user

        validated_data['authorization_grant_type'] = (
            AbstractApplication.GRANT_AUTHORIZATION_CODE
        )

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

        if 'agrees_to_terms' in validated_data:
            del validated_data['agrees_to_terms']

        if 'data_points' in validated_data:
            del validated_data['data_points']

        return super().update(instance, validated_data)
