import hashlib
import logging
from dataclasses import dataclass

from pipepad.config_old import SHORT_HASH_LENGTH
from pipepad.language import PadLanguage


logger = logging.getLogger(__name__)


@dataclass
class PadID:

    @classmethod
    def from_str(cls, s: str):
        logger.debug("Making PadID from %s", s)
        pass



@dataclass
class PipePad:
    """Pad object containing the contents of a pad"""
    contents: str
    language: PadLanguage

    def __repr__(self):
        return f"PipePad(hash={self.get_hash()}, " \
               f"contents={self.short_contents}," \
               f"language={self.language})"

    def get_hash(self):
        return hashlib.sha256(self.contents.encode("utf-8")).hexdigest()

    @property
    def short_contents(self):
        lines = self.contents.splitlines()
        num = 10
        num = num if len(lines) > num else len(lines) - 1

        return self.contents.split("\n")[num]

    def get_short_hash(self) -> str:
        h = self.get_hash()
        print(h)
        return h[:SHORT_HASH_LENGTH]

    @property
    def extension(self):
        return self.language.extension

    @classmethod
    def create_from_file(cls, filename, language: PadLanguage) -> Self:
        logger.debug("Creating pad from file %s", filename)
        with open(filename, 'r') as f:
            contents = f.read()

            pad = PipePad(contents=contents, language=language)
            return pad


