import os
from pprint import pprint

import pytest

from pipepad.config import settings
from tests.util import dummy_str


def test_show():
    pprint(settings.as_dict())


def test_simple_get():
    assert settings.pipepad.default_language == "python"


def test_override(tmp_path, request):
    with pytest.raises(AttributeError):
        assert settings.foo == "baz"

    id = dummy_str()
    name = request.node.name
    fpath = os.path.join(tmp_path, f"{name}.toml")

    with open(fpath, 'w') as f:
        f.write(f'[ppad]\nfoo = "{id}"')


    settings.load_file(fpath, silent=False)

    assert settings.ppad.foo == id
