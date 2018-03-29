# Blood groups
O_POSITIVE = 'O+'
O_NEGATIVE = 'O-'
A_POSITIVE = 'A+'
A_NEGATIVE = 'A-'
B_POSITIVE = 'B+'
B_NEGATIVE = 'B-'
AB_POSITIVE = 'AB+'
AB_NEGATIVE = 'AB-'

BLOOD_GROUPS = (
    (O_POSITIVE, O_POSITIVE),
    (O_NEGATIVE, O_NEGATIVE),
    (A_POSITIVE, A_POSITIVE),
    (A_NEGATIVE, A_NEGATIVE),
    (B_POSITIVE, B_POSITIVE),
    (B_NEGATIVE, B_NEGATIVE),
    (AB_POSITIVE, AB_POSITIVE),
    (AB_NEGATIVE, AB_NEGATIVE),
)

# Genders
MAN = 'man'
WOMAN = 'woman'
NON_BINARY = 'n-bin'
NON_DISCLOSURE = 'n-dis'

GENDERS = (
    (MAN, 'Man'),
    (WOMAN, 'Woman'),
    (NON_BINARY, 'Non-binary/Other'),
    (NON_DISCLOSURE, 'Prefer not to disclose'),
)

# Sexes
MALE = 'male'
FEMALE = 'female'
NON_BINARY = 'n-bin'
NON_DISCLOSURE = 'n-dis'

SEXES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (NON_BINARY, 'Non-binary/Other'),
    (NON_DISCLOSURE, 'Prefer not to disclose'),
)

# Pronouns
HE = 'h'
SHE = 's'
THEY = 't'

PRONOUNS = (
    (HE, 'He/him/his'),
    (SHE, 'She/her/her'),
    (THEY, 'They/them/their'),
)

# Impairments
ORTHOPAEDICALLY_IMPAIRED = 'o'
VISUALLY_IMPAIRED = 'v'
HEARING_IMPAIRED = 'h'
SPEECH_IMPAIRED = 's'
NO_IMPAIRMENT = 'n'

IMPAIRMENTS = (
    (ORTHOPAEDICALLY_IMPAIRED, 'Orthopaedically impaired'),
    (VISUALLY_IMPAIRED, 'Visually impaired'),
    (HEARING_IMPAIRED, 'Hearing impaired'),
    (SPEECH_IMPAIRED, 'Speech impaired'),
    (NO_IMPAIRMENT, 'No impairment'),
)
