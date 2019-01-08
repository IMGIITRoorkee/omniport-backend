from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from base_auth.managers.get_user import get_user


class PersonRelatedField(serializers.PrimaryKeyRelatedField):
    """
    This field handles the proper input of related people,
    by overriding functions from PrimaryKeyRelatedField
    """

    def to_internal_value(self, data):
        try:
            if type(data) is dict:
                # Dictionary sent by API should have ID in key 'id'...
                if 'id' in data:
                    return self.queryset.get(pk=data['id'])
                # ...or username in key 'username'
                elif 'username' in data:
                    return get_user(username=data['username']).person
                else:
                    # Any other dictionary is not acceptable
                    self.fail('incorrect_type', data_type=type(data).__name__)
            elif type(data) is int:
                # Integer sent by API should be the ID
                return self.queryset.get(pk=data)
            elif type(data) is str:
                # String sent by API should be the username
                return get_user(username=data).person
            else:
                # Any other data type sent by the API is not acceptable
                self.fail('incorrect_type', data_type=type(data).__name__)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
