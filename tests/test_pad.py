from pipepad.pad import PadID




class TestPadID:
    # def test_file_path(self):
    #     pad_id = PadID.from_str("file://./samples/sum_ints.pad.py")

    def test_simple_pad_id(self):
        pad_id = "samples/sum_ints"
        pad_id_out = PadID.from_str(pad_id)

    def test_simple_pad_id_with_version(self):
        pad_id = "samples/sum_ints:5"
        pad_id_out = PadID.from_str(pad_id)

    def test_file_pad_id(self):
        pad_id = "./samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)

    def test_file_pad_id_with_schema(self):
        pad_id = "file://./samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)

    def test_remote_repo_with_file(self):
        pad_id = "git@github.com:bnichs/pad_repo/samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)

    def test_remote_repo_with_pad(self):
        pad_id = "git@github.com:bnichs/pad_repo/samples/sum_ints"
        pad_id_out = PadID.from_str(pad_id)

    def test_remote_repo_with_pad_and_version(self):
        pad_id = "https://github.com/bnichs/pad_repo/samples/sum_ints:5"
        pad_id_out = PadID.from_str(pad_id)
