"""
Centres of IIT Roorkee
"""

# Academic centres
ALTERNATE_HYDRO_ENERGY_CENTRE = 'ahec'
CENTRE_FOR_NANOTECHNOLOGY = 'cnt'

ACADEMIC_CENTRES = (
    (
        ALTERNATE_HYDRO_ENERGY_CENTRE,
        'Alternate Hydro Energy Centre'
    ),
    (
        CENTRE_FOR_NANOTECHNOLOGY,
        'Centre for Nanotechnology'
    ),
)

# Centres of excellence
CENTRE_OF_EXCELLENCE_IN_DISASTER_MITIGATION_AND_MANAGEMENT = 'cedmm'
CENTRE_FOR_TRANSPORTATION_SYSTEMS = 'cts'
CENTRE_FOR_HIMALAYAN_STUDIES = 'chs'
CENTRE_OF_EXCELLENCE_IN_URBAN_DESIGN_AND_MANAGEMENT = 'ceudm'

CENTRES_OF_EXCELLENCE = (
    (
        CENTRE_OF_EXCELLENCE_IN_DISASTER_MITIGATION_AND_MANAGEMENT,
        'Centre of Excellence in Disaster Mitigation and Management'
    ),
    (
        CENTRE_FOR_TRANSPORTATION_SYSTEMS,
        'Centre for Transportation Systems'
    ),
    (
        CENTRE_FOR_HIMALAYAN_STUDIES,
        'Centre for Himalayan Studies'
    ),
    (
        CENTRE_OF_EXCELLENCE_IN_URBAN_DESIGN_AND_MANAGEMENT,
        'Centre of Excellence in Urban Design and Management'
    )
)

# Academic service centres
MAHATMA_GANDHI_CENTRAL_LIBRARY = 'mgcl'
CONTINUING_EDUCATION_CENTRE = 'cec'
INSTITUTE_COMPUTER_CENTRE = 'icc'
INSTITUTE_INSTRUMENTATION_CENTRE = 'iic'

ACADEMIC_SERVICE_CENTRES = (
    (
        MAHATMA_GANDHI_CENTRAL_LIBRARY,
        'Mahatma Gandhi Central Library'
    ),
    (
        CONTINUING_EDUCATION_CENTRE,
        'Continuing Education Centre'
    ),
    (
        INSTITUTE_COMPUTER_CENTRE,
        'Institute Computer Centre'
    ),
    (
        INSTITUTE_INSTRUMENTATION_CENTRE,
        'Institute Instrumentation Centre'
    ),
)

# Other supporting units
INTELLECTUAL_PROPERTY_RIGHTS_CELL = 'iprc'
EDUCATION_TECHNOLOGY_CELL = 'etc'
INSTITUTE_HOSPITAL = 'ih'
TIDES_INCUBATION_CENTRE = 'tides'

OTHER_SUPPORTING_UNITS = (
    (
        INTELLECTUAL_PROPERTY_RIGHTS_CELL,
        'Intellectual Property Rights Cell'
    ),
    (
        EDUCATION_TECHNOLOGY_CELL,
        'Education Technology Cell'
    ),
    (
        INSTITUTE_HOSPITAL,
        'Institute Hospital'
    ),
    (
        TIDES_INCUBATION_CENTRE,
        'Tides Incubation Centre'
    ),
)

CENTRES = (
        ACADEMIC_CENTRES
        + CENTRES_OF_EXCELLENCE
        + ACADEMIC_SERVICE_CENTRES
        + OTHER_SUPPORTING_UNITS
)
