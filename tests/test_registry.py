import os
import tempfile
from pathlib import Path
from unittest import TestCase
from uuid import uuid4

import pytest

from pipepad.pipepad_lib import get_template_pad, get_template_pad_record
from pipepad.record import PadHeader, MisssingHeaderField
from pipepad.registry import PadRegistry


TEST_DIR = tempfile.gettempdir()


def get_test_pad():
    pad = get_template_pad()
    return pad
    pass


class TestPadHeader(TestCase):
    def test_create_header(self):
        pad = get_template_pad_record()
        header = pad.get_pad_header()

        print(header)

    def test_ensure_fields(self):
        full_dict = {field: "foo" for field in PadHeader.REQUIRED_FIELDS}
        header = PadHeader.from_data(full_dict)

        while len(full_dict):
            el = list(full_dict.keys())[0]
            full_dict.pop(el)

            with pytest.raises(MisssingHeaderField):
                print(full_dict)
                header = PadHeader.from_data(full_dict)
                print(header)



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