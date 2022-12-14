import logging
from abc import abstractmethod
from dataclasses import dataclass


logger = logging.getLogger(__name__)


class UnknownLanguage(Exception):
    pass


@dataclass
class PadLanguage(object):
    name: str
    extension: str

    def __hash__(self):
        return hash((self.name, self.extension))

    @abstractmethod
    def comment_block(self, txt: str):
        raise

    @classmethod
    def from_string(cls, s: str):
        if s == "python":
            return PYTHON
        # elif s == "bash":
        #     pass
        elif s == "plaintext":
            return PLAINTEXT
        else:
            raise UnknownLanguage(s)

    def get_contents(self, txt: str, end_of_header: int):
        """
        :param txt: The full text of a pad file
        :param end_of_header: THe index of where we know the header ends
        :return:
        """
        logger.debug("Extracting contents for %s", self)
        start_of_content = txt.find("\n", end_of_header) + 1
        return txt[start_of_content:]


class PythonLanguage(PadLanguage):
    def __init__(self):
        super().__init__(name="python", extension="py")

    def comment_block(self, txt: str):
        out_str = '"""\n'
        out_str += txt
        out_str += '"""\n'
        return out_str

    def get_contents(self, txt: str, end_of_header: int):
        logger.debug("Extracting contents for %s", self)
        start_of_content = txt.find("\n", end_of_header) + 1

        # Skip past the comment part of the header
        start_of_content = txt.find("\n", start_of_content) + 1
        return txt[start_of_content:]


PYTHON = PythonLanguage()


class PlainTextLanguage(PadLanguage):
    def __init__(self):
        super().__init__(name="plaintext", extension="txt")

    def comment_block(self, txt: str):
        return txt


PLAINTEXT = PlainTextLanguage()


ALL_LANGUAGES = [
    PLAINTEXT,
    PYTHON
]