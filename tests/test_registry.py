import os
import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from pipepad.registry import LocalPadRepo, NoPadByThatName
from tests.util import get_test_pad, dummy_str

TEST_DIR = tempfile.gettempdir()
NUM_VERSIONS = 10


class TestRegistry():
    def setup_method(self, method):
        self.test_id = str(uuid4())
        self.test_dir = os.path.join(TEST_DIR, self.test_id)
        os.makedirs(self.test_dir, exist_ok=True)
        self.pad = get_test_pad()

    def test_create_registry(self):
        r = LocalPadRepo("test-reg", path=Path(self.test_dir))

    def test_list_no_pads(self):
        r = LocalPadRepo("test-reg", path=Path(self.test_dir))
        assert r.list_pads() == []

    def test_list_pads_type_correct(self, request):
        pad_name = request.node.name
        r = LocalPadRepo("test-reg", path=Path(self.test_dir))
        r.register_pad(pad_name, self.pad)

        pads = r.list_pads()
        for pad in pads:
            assert isinstance(pad, str)

    def test_get_no_pads(self):
        r = LocalPadRepo("test-reg", path=Path(self.test_dir))
        with pytest.raises(NoPadByThatName):
            r.get_pad_by_name("not-a-real-pad")

    def test_add_one_pad(self):
        pad_name = "test-add-one"
        r = LocalPadRepo("test-reg", path=Path(self.test_dir))
        r.register_pad(pad_name, self.pad)

        assert r.list_pads()
        record_from_req = r.get_pad_by_name(pad_name)
        pad_from_reg = record_from_req.pad
        assert pad_from_reg
        assert pad_from_reg == self.pad
        assert pad_from_reg.get_hash() == self.pad.get_hash()

    def test_get_latest(self, request, tmp_path):
        reg_name = request.node.name
        r = LocalPadRepo(reg_name, path=tmp_path)

        pad, pad_name = get_test_pad(), "pad"

        for i in range(NUM_VERSIONS):
            r.register_pad(pad_name, pad)
            assert r.get_latest(pad_name=pad_name).pad == pad

            pad.contents += dummy_str()

    def test_multiple_puts(self, request, tmp_path):
        reg_name = request.node.name
        r = LocalPadRepo(reg_name, path=tmp_path)

        pad1, pad1_name = get_test_pad(), "pad1"
        pad2, pad2_name = get_test_pad(), "pad2"

        print(repr(pad1))

        r.register_pad(pad1_name, pad1)
        r.register_pad(pad2_name, pad2)

        assert r.get_latest(pad1_name).pad == pad1
        assert r.get_latest(pad2_name).pad == pad2

