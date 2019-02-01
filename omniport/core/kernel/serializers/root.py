from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    """
    This model serializer should be inherited by all model serializers
    Allows you to specify fields via a keyword argument
    Such a feature may be a nifty little addition to the existing
    ModelSerializer functionality
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
        excluded_fields = kwargs.pop('excluded_fields', None)

        super(ModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None and excluded_fields is not None:
            raise ValueError('Cannot specify both included and excluded fields')

        if fields is not None:
            allowed_fields = set(fields)
            existing_fields = set(self.fields)
            for field in existing_fields - allowed_fields:
                self.fields.pop(field)

        if excluded_fields is not None:
            disallowed_fields = set(excluded_fields)
            for field in disallowed_fields:
                self.fields.pop(field)
