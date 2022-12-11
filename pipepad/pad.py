import hashlib
from dataclasses import dataclass

from pipepad.language import PadLanguage


@dataclass
class PipePad:
    """Pad object containing the contents of a pad"""
    contents: str
    language: PadLanguage

    def __repr__(self):
        return f"PipePad(hash={self.get_hash()}, contents={self.short_contents})"

    def get_hash(self):
        return hashlib.sha256(self.contents.encode("utf-8")).hexdigest()

    @property
    def short_contents(self):
        return self.contents.split("\n")[10]

    @property
    def extension(self):
        return self.language.extension
