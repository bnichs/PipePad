import os

APP_NAME = "pipepad"


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_DIR = os.path.dirname(MODULE_DIR)

TEMPLATE_FILE = "template.py"
TEMPLATE_PATH = os.path.join(MODULE_DIR, TEMPLATE_FILE)

BIN_PATH = os.path.join(PACKAGE_DIR, "bin")


RUN_PAD_PATH = os.path.join(BIN_PATH, "run_pad.sh")


DEFAULT_REPO = "local"


PAD_EXTENSION = "ppad"
