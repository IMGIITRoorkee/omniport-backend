import swapper
import random
import string

from django.conf import settings
from datetime import date

from base_auth.models import User

def create_guest(password):
    person = swapper.load_model('kernel', 'person')
    password = ''.join(random.choice(string.ascii_letters) for i in range(10))

    guest_user = User.objects.create_user(username=settings.GUEST_USERNAME, password=password)

    guest_person = person.objects.get_or_create(user=guest_user, short_name=settings.GUEST_USERNAME, full_name = settings.GUEST_USERNAME)[0]

    guest = swapper.load_model('kernel', 'Guest')

    guest.objects.get_or_create(person= guest_person, start_date=date.today())

    return guest_user
