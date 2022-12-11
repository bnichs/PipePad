import os
import tempfile
from pathlib import Path
from unittest import TestCase
from uuid import uuid4

from pipepad.pipepad_lib import get_template_pad
from pipepad.registry import PadRegistry


TEST_DIR = tempfile.gettempdir()


def get_test_pad():
    pad = get_template_pad()
    return pad
    pass


class TestRegistry(TestCase):
    def setup_method(self, method):
        self.test_id = str(uuid4())
        self.test_dir = os.path.join(TEST_DIR, self.test_id)
        os.makedirs(self.test_dir, exist_ok=True)
        self.pad = get_test_pad()

    def test_create_registry(self):
        r = PadRegistry("test-reg", storage_path=Path(self.test_dir))

    def test_add_one_pad(self):
        r = PadRegistry("test-reg", storage_path=Path(self.test_dir))
        r.register_pad("test-add-one", self.pad)
        pass

    pass