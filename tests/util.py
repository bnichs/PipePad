from uuid import uuid4

from pipepad.language import PLAINTEXT
from pipepad.pad import PipePad


def dummy_str(prefix="", suffix=""):
    s = str(uuid4())
    s = prefix + s + suffix
    return s



# def get_test_dir()
def get_test_pad(contents=None):
    contents = contents or dummy_str(prefix="pad-contents-")
    pad = PipePad(contents=contents, language=PLAINTEXT)
    return pad
