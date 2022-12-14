from abc import abstractmethod
from dataclasses import dataclass


class UnknownLanguage(Exception):
    pass


@dataclass
class PadLanguage(object):
    name: str
    extension: str

    @abstractmethod
    def comment_block(self, txt: str):
        raise

    @classmethod
    def from_string(cls, s: str):
        if s == "python":
            return PythonLanguage()
        # elif s == "bash":
        #     pass
        # elif s == "txt":
        #     pass
        else:
            raise UnknownLanguage(s)



class PythonLanguage(PadLanguage):
    def __init__(self):
        super().__init__(name="python", extension="py")

    def comment_block(self, txt: str):
        out_str = '"""\n'
        out_str += txt
        out_str += '"""\n'
        return out_str


PYTHON = PythonLanguage()

