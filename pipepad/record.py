import io
import logging
from dataclasses import dataclass
from datetime import date, datetime
from os import PathLike
from pathlib import Path
from typing import Any, Tuple, Dict

import yaml

from pipepad.config import PAD_EXTENSION, HEADER_START_STRING, HEADER_END_STRING, HEADER_VERSION_KEY, HEADER_DATE_KEY, \
    HEADER_NAME_KEY, HEADER_LANG_KEY, HEADER_HASH_KEY
from pipepad.language import PadLanguage, PythonLanguage
from pipepad.pad import PipePad

logger = logging.getLogger(__name__)


from collections import OrderedDict


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


class UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))


class HashMismatch(Exception):
    pass


class PadHeader(object):
    HEADER_VERSION = "v1"

    def __init__(self):
        self._store = {} #UnsortableOrderedDict()
        self._store["pipepad-version"] = self.HEADER_VERSION

    def add(self, name: str, val: Any):
        self._store[name] = val

    def encode(self):
        """Encode this header using whatever format"""

        with io.StringIO() as stream:
            yaml.dump(self._store, stream, sort_keys=False)
            txt = stream.getvalue()
            return txt

    def get_text(self):
        return self.encode()
        pass





@dataclass
class PadRecord(object):
    """A pad that can be saved"""
    pad_name: str
    date_added: date
    pad: PipePad



    def get_pad_name(self):
        return Path(f"foo.{PAD_EXTENSION}.{self.pad.extension}")

    def pad_header(self):
        """The header at the beginning of pad text with all the info about the pad

        Full output Depends on the language the pad is in, the comment function takes care of that

        """

    def get_pad_header(self) -> str:
        header = PadHeader()
        header.add("name", self.pad_name)
        header.add("date", self.date_added)
        header.add("hash-sha256", self.pad.get_hash())
        header.add("language", self.pad.language.name)

        txt = header.get_text()
        print(txt)

        txt = self.pad.language.comment_block(txt)
        return txt

    @classmethod
    def load_from_file(cls, filename):
        logger.debug("Loading pad from file %s", filename)
        with open(filename, 'rb') as f:
            contents = f.read().decode("utf-8")

            # TODO
            dt = datetime.now()
            lang = PythonLanguage()
            pad = PipePad(contents=contents, language=lang)
            return cls(pad=pad, date_added=dt, pad_name="foo")

            dt = header.get_date()
            lang = header.get_language()
            name = header.get_name()
            header_hash = header.get_hash()
            pad = PipePad(contents=contents, language=lang)
            pad_hash = pad.get_hash()

            if header_hash != pad_hash:
                print(repr(pad.contents))

                raise HashMismatch(header_hash, pad_hash)

            return cls(pad=pad, date_added=dt, pad_name=name)

    def save_to_file(self, fname: PathLike=None, save_dir: PathLike=None) -> PathLike:
        if save_dir and fname:
            fpath = os.path.join(save_dir, fname)
        elif save_dir:
            fname = self.get_pad_name()
            fpath = os.path.join(save_dir, fname)
        elif fname:
            fpath = os.path.abspath(fname)
        else:
            fname = self.get_pad_name()
            fpath = os.path.abspath(fname)

        with open(fpath, 'w') as f:
            txt = self.get_pad_header()
            txt += self.pad.contents
            f.write(txt)
        logger.debug("Saved pad %s to %s", self.pad_name, fpath)

        return fpath

    # def __repr__(self):
    #     return f"PadRecord(pad_name={self.pad_name}, " \
    #            f"pad_hash={self.pad.hash}, " \
    #            f"date_added={self.date_added}, " \
    #            f"pad_contents={self.pad.short_contents})"
