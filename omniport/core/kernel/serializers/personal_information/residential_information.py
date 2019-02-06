import swapper
from django.db import ProgrammingError
from rest_framework import serializers

from kernel.serializers.root import ModelSerializer
from omniport.utils import switcher

ResidentialInformation = swapper.load_model('kernel', 'ResidentialInformation')
Residence = swapper.load_model('kernel', 'Residence')

ResidenceSerializer = switcher.load_serializer('kernel', 'Residence')


class ResidentialInformationSerializer(ModelSerializer):
    """
    Serializer for ResidentialInformation objects
    """

    def __init__(self, *args, **kwargs):
        """
        Add the residence ChoiceField on the serializer based on the existence
        of Residence models
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)

        try:
            residences = Residence.objects.all()
        except ProgrammingError:
            residences = list()

        self.fields['residence'] = serializers.ChoiceField(
            choices=[
                (residence.id, residence.name)
                for residence in residences
            ],
            write_only=True,
        )

    def to_representation(self, instance):
        """
        Insert the ID of the related residence instance into the representation
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        representation['residence'] = instance.residence.id

        return representation

    def update(self, instance, validated_data):
        """

        :param instance: the instance being updated
        :param validated_data: the new data for the instance
        :return: the updated instance
        """

        residence = validated_data['residence']
        residence = Residence.objects.get(pk=residence)
        validated_data['residence'] = residence

        return super().update(instance, validated_data)

    class Meta:
        """
        Meta class for ResidentialInformationSerializer
        """

        model = ResidentialInformation
        exclude = [
            'person',
            'id',
            'datetime_created',
            'datetime_modified',
        ]
