

import string

import random

import datetime

import swapper

import django

import os



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omniport.settings")

django.setup()

from base_auth.models import User


Branch = swapper.load_model('kernel', 'Branch')

Person = swapper.load_model('kernel', 'Person')

Student = swapper.load_model('kernel', 'Student')

FacultyMember = swapper.load_model('kernel', 'FacultyMember')

Maintainer = swapper.load_model('kernel', 'Maintainer')


# generate the random string that is used in faculty employee id


def randomString(stringLength=6):

    """Generate a random string of fixed length """

    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(stringLength))



# Increase the value of n to make more users

n = 5


# For generating unique enrolment numbers

count = 0

# Create a branch from omnipotence

branch_id = Branch.objects.all().first().id


for x in range(n):


    student_user = User()

    student_user_name = f"stu{x+1}"

    student_user.username = student_user_name

    student_user.set_password("pass")

    student_user.save()


    person = Person()

    person.user = student_user

    person.full_name = f'student{x+1}'

    person.save()


    student = Student()

    student.start_date = datetime.date.today()

    student.person = person

    student.branch_id = branch_id

    student.current_year = 2

    student.current_semester = 4

    student.enrolment_number = 14000000 + count

    count = count + 1

    student.save()


    # faculty_user = User()

    # faculty_user_name = f"fac{x+1}"

    # faculty_user.username = faculty_user_name

    # faculty_user.set_password("pass")

    # faculty_user.save()


    # person = Person()

    # person.user = faculty_user

    # person.full_name = f'faculty{x+1}'

    # person.save()


    # faculty = FacultyMember()

    # faculty.start_date = datetime.date.today()

    # faculty.person = person

    # faculty.department_id = 1

    # faculty.designation = "ap"

    # faculty.employee_id = randomString(6)

    # faculty.save()


    maintainer_user = User()

    maintainer_user_name = f"main{x+1}"

    maintainer_user.username = maintainer_user_name

    maintainer_user.set_password("pass")

    maintainer_user.is_superuser = True

    maintainer_user.save()


    person = Person()

    person.user = maintainer_user

    person.full_name = f'maintainer{x+1}'

    person.save()


    maintainer = Maintainer()

    maintainer.start_date = datetime.date.today()

    maintainer.person = person

    if count % 2 == 0:

        maintainer.role = 'dev'

    else:

        maintainer.role = 'des'

    maintainer.designation = 'hub'

    maintainer.save()


for x in range(n):

    user = User()

    user_name = f"img{x+1}"

    user.username = user_name

    user.set_password("pass")

    user.is_superuser = True

    user.save()


    person = Person()

    person.user = user

    person.full_name = f'imgian{x+1}'

    person.save()


    maintainer = Maintainer()

    maintainer.start_date = datetime.date.today()

    maintainer.person = person

    if count % 2 == 0:

        maintainer.role = 'dev'

    else:

        maintainer.role = 'des'

    maintainer.designation = 'hub'

    maintainer.save()


    student = Student()

    student.start_date = datetime.date.today()

    student.person = person

    student.branch_id = branch_id

    student.current_year = 2

    student.current_semester = 4

    student.enrolment_number = 18000000 + count

    student.current_cgpa = 9.5

    count = count + 1

    student.save()

