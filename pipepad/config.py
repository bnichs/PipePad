import os

# Primitives
APP_NAME = "pipepad"
PAD_EXTENSION = "ppad"


# Package locations
MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_DIR = os.path.dirname(MODULE_DIR)
BIN_PATH = os.path.join(PACKAGE_DIR, "bin")


# Templates
TEMPLATE_DIR = os.path.join(PACKAGE_DIR, "pipepad", "templates")
TEMPLATE_FILE = "template"

# TODO for python only
TEMPLATE_FILE_PY = "template.ppad.py"
PY_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, TEMPLATE_FILE_PY)


# Todo lang agnostic
RUN_PAD_PATH = os.path.join(BIN_PATH, "run_pad.sh")


DEFAULT_REPO = "local"



# Headers
# We use tokens because not every language has the same comments so we need to know where to find the data
HEADER_START_STRING = "START_HEADER"
HEADER_END_STRING = "END_HEADER"

HEADER_VERSION_KEY = "pipepad-version"
HEADER_DATE_KEY = "date"
HEADER_NAME_KEY = "name"
HEADER_LANG_KEY = "language"
HEADER_HASH_KEY = "hash"


# Pads
# How many characters for a short hash
SHORT_HASH_LENGTH = 8


LATEST_PAD_NAME = "latest"