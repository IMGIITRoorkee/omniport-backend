import swapper
import random
import string
import datetime

from django.conf import settings

from base_auth.models import User


def create_guest():
    Person = swapper.load_model('kernel', 'person')
    password = ''.join(random.choice(string.ascii_letters) for i in range(10))

    guest_user = User.objects.create_user(
        username=settings.GUEST_USERNAME,
        password=password
    )
    guest_person, _ = Person.objects.get_or_create(
        user=guest_user,
        short_name=settings.GUEST_USERNAME,
        full_name=settings.GUEST_USERNAME
    )

    Guest = swapper.load_model('kernel', 'Guest')
    Guest.objects.get_or_create(person=guest_person, start_date=datetime.date.today())
    return guest_user
