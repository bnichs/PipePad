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

    def test_save_load_identical_txt(self, tmp_path):
        pad = PipePad(contents=self.id, language=PLAINTEXT)
        record = PadRecord(f"test-pad-{self.id}", pad=pad)

        out_path = record.save_to_file(save_dir=tmp_path)
        assert os.path.exists(out_path)

        print(repr(record.pad.contents))
        new_record = PadRecord.load_from_file(out_path, ignore_hash_mismatch=False)
        print(repr(new_record.pad.contents))

        assert new_record == record
        assert new_record.pad == record.pad

        assert new_record.date_added
        assert new_record.pad.get_hash()
        assert new_record.pad.contents


class TestHeader():

    def test_extract_header_py(self):
        tpath = get_template_path(PYTHON)
        with open(tpath) as f:
            fil_contents = f.read()

        header, extracted_contents = PadHeader.extract_header(fil_contents)
        print(header)

        assert header.get_language() == PYTHON

        print(extracted_contents)
        assert HEADER_END_STRING not in extracted_contents and HEADER_START_STRING not in extracted_contents
        assert extracted_contents.startswith('"""\n# Welcome To Pypad!!!')

    def test_extract_header_txt(self):
        tpath = get_template_path(PLAINTEXT)
        with open(tpath) as f:
            fil_contents = f.read()

        header, extracted_contents = PadHeader.extract_header(fil_contents)
        print(header)
        assert header.get_hash()
        assert header.get_language() == PLAINTEXT

        print(extracted_contents)
        assert HEADER_END_STRING not in extracted_contents and HEADER_START_STRING not in extracted_contents
        assert extracted_contents.startswith('hello')

    def test_create_header(self):
        for lang in ALL_LANGUAGES:
            pad = get_template_pad_record(language=lang, ignore_hash_mismatch=True)
            header = pad.generate_pad_header()
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
        # raise


