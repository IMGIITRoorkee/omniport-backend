import swapper
from django.db.models import Q

from kernel.models import User, ContactInformation


def get_user(username):
    """
    Get the user corresponding to the given username

    This method is different from User.objects.get(username=username) because
    it looks at a spectrum of other fields in related models to identify the
    user. These fields are:

    User
    - username

    Student
    - enrolment_number

    ContactInformation
    - primary_phone_number
    - secondary_phone_number
    - email_address
    - institute_webmail_address

    :param username: the username provided to identify the user
    :return: the user, if a user with the given username is found
    :raise: User.DoesNotExist, if no user with the given username is found
    """

    Person = swapper.load_model('kernel', 'Person')
    Student = swapper.load_model('kernel', 'Student')

    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        pass

    try:
        student = Student.objects.get(enrolment_number=username)
        person = student.person
        if person is not None:
            user = person.user
            if user is not None:
                return user
    except Student.DoesNotExist:
        pass

    try:
        q_primary_phone_number = Q(primary_phone_number=username)
        q_secondary_phone_number = Q(secondary_phone_number=username)
        q_email_address = Q(email_address=username)
        q_institute_webmail_address = Q(institute_webmail_address=username)
        q = (
                q_primary_phone_number
                | q_secondary_phone_number
                | q_email_address
                | q_institute_webmail_address
        )
        contact_information = ContactInformation.objects.get(q)
        entity = contact_information.entity
        if type(entity) is Person:
            user = entity.user
            if user is not None:
                return user
    except (
            ContactInformation.DoesNotExist,
            User.DoesNotExist
    ):
        pass

    raise User.DoesNotExist
