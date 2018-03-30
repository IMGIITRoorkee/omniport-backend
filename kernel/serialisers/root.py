from rest_framework import serializers


class ModelSerialiser(serializers.ModelSerializer):
    """
    This model serialiser should be inherited by all model serialisers
    Allows you to specify fields via a keyword argument
    Do not inherit from serializers.ModelSerializer!
    """

    def __init__(self, *args, **kwargs):
        """
        Delegate to superclass but alter the fields based on a keyword
        argument. The list of fields to keep from the existing fields is
        specified in the fields keyword argument
        :param args: arguments
        :param kwargs: keyword arguments
        """

        fields = kwargs.pop('fields', None)

        super(ModelSerialiser, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed_fields = set(fields)
            existing_fields = set(self.fields)
            for field in existing_fields - allowed_fields:
                self.fields.pop(field)
