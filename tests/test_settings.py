from pprint import pprint

from pipepad.config import settings


def test_show():
    pprint(settings.as_dict())

    raise


def test_simple_get():
    assert settings.pipepad.default_language == "python"


def test_override():
    settings.configure()
    pass