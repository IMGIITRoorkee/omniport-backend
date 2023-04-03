# Person data points
SHORT_NAME = 'person.short_name'
FULL_NAME = 'person.full_name'
DISPLAY_PICTURE = 'person.display_picture'
ROLES = 'person.roles'
CUSTOM_ROLES = 'person.custom_roles'
PERSON_DATA_POINTS = (
    (SHORT_NAME, 'Short name'),
    (FULL_NAME, 'Full name'),
    (DISPLAY_PICTURE, 'Display picture'),
    (ROLES, 'Roles'),
    (CUSTOM_ROLES, 'Custom Roles'),
)

# Student data points
JOINING_DATE = 'student.start_date'
GRADUATION_DATE = 'student.end_date'
ENROLMENT_NUMBER = 'student.enrolment_number'
BRANCH = 'student.branch.name'
DEGREE = 'student.branch.degree.name'
DEPARTMENT = 'student.branch.department.name'
CURRENT_YEAR = 'student.current_year'
CURRENT_SEMESTER = 'student.current_semester'
STUDENT_DATA_POINTS = (
    (JOINING_DATE, 'Joining date'),
    (GRADUATION_DATE, 'Graduation date'),
    (ENROLMENT_NUMBER, 'Enrolment number'),
    (BRANCH, 'Branch'),
    (DEGREE, 'Degree'),
    (CURRENT_YEAR, 'Current year'),
    (CURRENT_SEMESTER, 'Current semester'),
    (DEPARTMENT, 'Department'),
)

# Faculty member data points
JOINING_DATE = 'faculty_member.start_date'
LEAVING_DATE = 'faculty_member.end_date'
DESIGNATION = 'faculty_member.designation'
DEPARTMENT = 'faculty_member.department.name'
EMPLOYEE_ID = 'faculty_member.employee_id'
FACULTY_MEMBER_DATA_POINTS = (
    (JOINING_DATE, 'Joining date'),
    (LEAVING_DATE, 'Leaving date'),
    (DESIGNATION, 'Designation'),
    (DEPARTMENT, 'Department'),
    (EMPLOYEE_ID, 'Employee id'),
)

# Biological information data points
DATE_OF_BIRTH = 'biological_information.date_of_birth'
BLOOD_GROUP = 'biological_information.blood_group'
SEX = 'biological_information.sex'
GENDER = 'biological_information.gender'
BIOLOGICAL_INFORMATION_DATA_POINTS = (
    (DATE_OF_BIRTH, 'Date of birth'),
    (BLOOD_GROUP, 'Blood group'),
    (SEX, 'Sex'),
    (GENDER, 'Gender'),
)

# Contact information data points
EMAIL_ADDRESS = 'contact_information.email_address'
EMAIL_ADDRESS_VERIFIED = 'contact_information.email_address_verified'
INSTITUTE_WEBMAIL_ADDRESS = 'contact_information.institute_webmail_address'
PRIMARY_PHONE_NUMBER = 'contact_information.primary_phone_number'
SECONDARY_PHONE_NUMBER = 'contact_information.secondary_phone_number'
CONTACT_INFORMATION_DATA_POINTS = (
    (EMAIL_ADDRESS, 'Email address'),
    (EMAIL_ADDRESS_VERIFIED, 'Email address verified'),
    (INSTITUTE_WEBMAIL_ADDRESS, 'Institute webmail address'),
    (PRIMARY_PHONE_NUMBER, 'Primary phone number'),
    (SECONDARY_PHONE_NUMBER, 'Secondary phone number'),
)

# Residential information data points
RESIDENCE = 'residential_information.residence.name'
ROOM_NUMBER = 'residential_information.room_number'
RESIDENTIAL_INFORMATION_DATA_POINTS = (
    (RESIDENCE, 'Residence'),
    (ROOM_NUMBER, 'Room Number'),
)

# Social information data points
LINKS = 'social_information.links'
SOCIAL_INFORMATION_DATA_POINTS = (
    (LINKS, 'Links'),
)

DATA_POINTS = (
        PERSON_DATA_POINTS
        + STUDENT_DATA_POINTS
        + FACULTY_MEMBER_DATA_POINTS
        + BIOLOGICAL_INFORMATION_DATA_POINTS
        + CONTACT_INFORMATION_DATA_POINTS
        + RESIDENTIAL_INFORMATION_DATA_POINTS
        + SOCIAL_INFORMATION_DATA_POINTS
)
