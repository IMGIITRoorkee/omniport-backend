"""
This setting file names all directories of relevance in the entire filesystem
containing and surrounding the project.
"""

import os as _os

# The location of this file
FILE_PATH = _os.path.abspath(__file__)

# The 'base' package, inside the 'settings' directory
BASE_DIR = _os.path.dirname(FILE_PATH)

# The 'settings' package, inside the 'omniport' directory
SETTINGS_DIR = _os.path.dirname(BASE_DIR)

# The 'omniport' package, inside the base directory
OMNIPORT_DIR = _os.path.dirname(SETTINGS_DIR)

# The project directory, inside which the project code rests
PROJECT_DIR = _os.path.dirname(OMNIPORT_DIR)

# The parent directory inside which the project directory rests
PARENT_DIR = _os.path.dirname(PROJECT_DIR)

# Parent level directories
# The 'configuration' directory where all settings will be loaded from
# The 'branding' directory where all branding imagery will be loaded from
# The 'static' directory where all static files will be collected into
# The 'media' directory where all uploaded media will be stored in
# The 'personal' directory where all uploaded personal files will be stored in
# The 'certificates' directory where third-party services' certificates will be stored in
# The 'supervisor.d' directory where all supervisor daemon scripts will be stored in

CONFIGURATION_DIR = _os.path.join(PARENT_DIR, 'configuration')
BRANDING_DIR = _os.path.join(PARENT_DIR, 'branding')
STATIC_DIR = _os.path.join(PARENT_DIR, 'static_files')
MEDIA_DIR = _os.path.join(PARENT_DIR, 'media_files')
PERSONAL_DIR = _os.path.join(PARENT_DIR, 'personal_files')
CERTIFICATES_DIR = _os.path.join(PARENT_DIR, 'certificates')
SUPERVISORD_DIR = _os.path.join(PARENT_DIR, 'supervisor.d')

# Project level directories
# The 'core' directory where all Omniport core apps will be loaded from
# The 'services' directory where all Omniport service apps will be loaded from
# The 'apps' directory where all Omniport drop-in apps will be loaded from

CORE_DIR = _os.path.join(PROJECT_DIR, 'core')
SERVICES_DIR = _os.path.join(PROJECT_DIR, 'services')
APPS_DIR = _os.path.join(PROJECT_DIR, 'apps')

APP_SUPERVISORD_DIR = 'supervisor.d'
