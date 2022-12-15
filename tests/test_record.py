import os
from unittest import TestCase

import pytest

from pipepad.config import HEADER_START_STRING, HEADER_END_STRING
from pipepad.language import PythonLanguage, PYTHON, PLAINTEXT, ALL_LANGUAGES
from pipepad.pad import PipePad
from pipepad.pipepad_lib import get_template_pad_record
from pipepad.record import PadRecord, PadHeader, MisssingHeaderField
from pipepad.util import get_template_path
from tests.util import dummy_str


class TestRecord():
    def setup_method(self, method):
        self.id = dummy_str()
        self.pad = PipePad(contents=self.id, language=PYTHON)

    def test_save_load_identical_py(self, tmp_path):
        record = PadRecord(f"test-pad-{self.id}", pad=self.pad)

        out_path = record.save_to_file(save_dir=tmp_path)
        assert os.path.exists(out_path)

        print(repr(record.pad.contents))
        new_record = PadRecord.load_from_file(out_path)

        assert new_record == record
        assert new_record.pad == record.pad

        assert new_record.date_added
        assert new_record.pad.get_hash()
        assert new_record.pad.contents

        # raise


