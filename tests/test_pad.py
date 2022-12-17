from pipepad.config_old import LATEST_VERSION
from pipepad.pad import PadID




class TestPadID:
    def test_simple_pad_id(self):
        pad_id = "samples:sum_ints"
        pad_id_out = PadID.from_str(pad_id)

        assert pad_id_out.pad_name == "sum_ints"
        assert pad_id_out.repo == "samples"
        assert pad_id_out.version == LATEST_VERSION

    def test_simple_pad_id_with_version(self):
        pad_id = "samples:sum_ints:5"
        pad_id_out = PadID.from_str(pad_id)
        print(pad_id_out)

        assert pad_id_out.pad_name == "sum_ints"
        assert pad_id_out.repo == "samples"
        assert pad_id_out.version == 5

    def test_simple_pad_id_with_version_str(self):
        pad_id = "samples:sum_ints:latest"
        pad_id_out = PadID.from_str(pad_id)
        print(pad_id_out)

        assert pad_id_out.pad_name == "sum_ints"
        assert pad_id_out.repo == "samples"
        assert pad_id_out.version == LATEST_VERSION

    def test_file_pad_id(self):
        pad_id = "./samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)
        assert pad_id_out.is_file()
        assert pad_id_out.file_exists()
        print(pad_id_out)

    def test_file_pad_id_with_schema(self):
        pad_id = "file://./samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)
        assert pad_id_out.is_file()
        assert pad_id_out.file_exists()
        print(pad_id_out)

    def test_remote_repo_with_file(self):
        pad_id = "git://git@github.com:bnichs/pad_repo/samples/sample_repo/sum_ints/latest.py"
        pad_id_out = PadID.from_str(pad_id)

        assert pad_id_out.is_remote()

        assert pad_id_out.repo.scheme == "git"
        assert pad_id_out.repo.netloc == "git@github.com:bnichs"
        assert pad_id_out.path == "/pad_repo/samples/sample_repo/sum_ints/latest.py"

    def test_remote_repo_with_pad(self):
        pad_id = "git://git@github.com:bnichs/pad_repo/samples:sum_ints"
        pad_id_out = PadID.from_str(pad_id)
        assert pad_id_out.name == "sum_ints"

        assert pad_id_out.repo.scheme == "git"
        assert pad_id_out.repo.netloc == "git@github.com:bnichs"
        assert pad_id_out.repo.path == "/pad_repo/samples"

    def test_remote_repo_with_pad_and_version(self):
        pad_id = "https://github.com/bnichs/pad_repo/samples:sum_ints:5"
        pad_id_out = PadID.from_str(pad_id)
        assert pad_id_out.name == "sum_ints"

        assert pad_id_out.repo.scheme == "https"
        assert pad_id_out.repo.netloc == "github.com"
        assert pad_id_out.repo.path == "/bnichs/pad_repo/samples"

        print(pad_id_out)

    # @classmethod
    # def teardown_class(cls):
    #     raise