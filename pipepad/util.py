import os
import sys

from pipepad.config_old import TEMPLATE_FILE, PAD_EXTENSION, TEMPLATE_DIR
from pipepad.language import PadLanguage


def get_template_path(language: PadLanguage) -> str:
    """Get the path for a given lanuages template"""
    fname = f"{TEMPLATE_FILE}.{PAD_EXTENSION}.{language.extension}"

    path = os.path.join(TEMPLATE_DIR, fname)
    return path


def detect_stdin():
    """
    Determine if this program was run with or without anything in stdin
    :return: True if stdin has elements
    """
    return not sys.stdin.isatty()
