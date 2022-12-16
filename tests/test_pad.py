from pipepad.pad import PadID


class TestPadID:
    def test_file_path(self):
        pad_id = PadID.from_str("file://./samples/sum_ints.pad.py")