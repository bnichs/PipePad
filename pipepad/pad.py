import hashlib
from dataclasses import dataclass

from pipepad.language import PadLanguage


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

    @property
    def extension(self):
        return self.language.extension