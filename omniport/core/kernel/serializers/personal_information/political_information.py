import swapper

from formula_one.serializers.base import ModelSerializer

PoliticalInformation = swapper.load_model('kernel', 'PoliticalInformation')


class PoliticalInformationSerializer(ModelSerializer):
    """
    Serializer for PoliticalInformation objects

    Since political fields are delicate, it is important to be able to make
    fields editable explicitly, rather than read-only explicitly.
    """

    # All fields other than these will be read-only
    editable_fields = [
        'religion',
    ]

    class Meta:
        """
        Meta class for PoliticalInformationSerializer
        """

        model = PoliticalInformation
        exclude = [
            'person',
            'id',
            'datetime_created',
            'datetime_modified',
        ]

    def __init__(self, *args, **kwargs):
        """
        Delegate to superclass but alter the editability of the fields based on
        whether they appear in the editable_fields property
        :param args: arguments
        :param kwargs: keyword arguments
        """

        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field not in self.editable_fields:
                self.fields[field].read_only = True

    def to_representation(self, instance):
        """
        Replace the country code of the nationality with a prettier string
        containing the flag and the country name
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        if 'nationality' in representation:
            del representation['nationality']

        nationality = instance.nationality
        nationality_string = f'{nationality.unicode_flag} {nationality.name}'
        representation['nationality'] = nationality_string

        return representation
