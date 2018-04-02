"""
Degrees offered by IIT Roorkee
"""

BACHELOR_OF_TECHNOLOGY = 'B.Tech. - Bachelor of Technology'
MASTER_OF_TECHNOLOGY = 'M.Tech. - Master of Technology'
INTEGRATED_DUAL_DEGREE = 'Int. M.Tech. - Integrated Dual Degree'

BACHELOR_OF_SCIENCE = 'B.Sc. - Bachelor of Science'
MASTER_OF_SCIENCES = 'M.Sc. - Master of Science'
INTEGRATED_MASTER_OF_SCIENCE = 'Int. M.Sc. - Integrated Master of Science'

BACHELOR_OF_ARCHITECTURE = 'B.Arch. - Bachelor of Architecture'
MASTER_OF_ARCHITECTURE = 'M.Arch. - Master of Architecture'
MASTER_OF_URBAN_AND_REGIONAL_PLANNING = ('M.U.R.P - Master of Urban and '
                                         'Regional Planning')

DOCTOR_OF_PHILOSOPHY = 'Ph.D. - Doctor of Philosophy'
POST_DOCTORATE = 'Post Doc. - Post-doctorate'

MASTER_OF_BUSINESS_ADMINISTRATION = 'M.B.A. - Master of Business Administration'
MASTER_OF_COMPUTER_APPLICATIONS = 'M.C.A. - Master of Computer Applications'

POSTGRADUATE_DIPLOMA_COURSE = 'P.G. Dip. - Post-graduate Diploma'

UNDERGRADUATE_DEGREES = (
    ('btech', BACHELOR_OF_TECHNOLOGY),
    ('idd', INTEGRATED_DUAL_DEGREE),
    ('bsc', BACHELOR_OF_SCIENCE),
    ('imsc', INTEGRATED_MASTER_OF_SCIENCE),
    ('barch', BACHELOR_OF_ARCHITECTURE),
)

POSTGRADUATE_DEGREES = (
    ('mtech', MASTER_OF_TECHNOLOGY),
    ('msc', MASTER_OF_SCIENCES),
    ('march', MASTER_OF_ARCHITECTURE),
    ('murp', MASTER_OF_URBAN_AND_REGIONAL_PLANNING),
    ('pgdip', POSTGRADUATE_DIPLOMA_COURSE),
    ('mba', MASTER_OF_BUSINESS_ADMINISTRATION),
    ('mca', MASTER_OF_COMPUTER_APPLICATIONS),
)

DOCTORATE_DEGREES = (
    ('phd', DOCTOR_OF_PHILOSOPHY),
    ('pdoc', POST_DOCTORATE),
)

DEGREES = (
        UNDERGRADUATE_DEGREES
        + POSTGRADUATE_DEGREES
        + DOCTORATE_DEGREES
)
