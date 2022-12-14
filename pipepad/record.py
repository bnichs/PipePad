import io
import logging
import os.path
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

#
# class UnsortableList(list):
#     def sort(self, *args, **kwargs):
#         pass
#
#
# class UnsortableOrderedDict(OrderedDict):
#     def items(self, *args, **kwargs):
#         return UnsortableList(OrderedDict.items(self, *args, **kwargs))
#
#
# yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)

class MisssingHeaderField(Exception):
    pass


class NoHeaderFound(Exception):
    pass


class HashMismatch(Exception):
    pass


class PadHeader(object):
    HEADER_VERSION = "v1"
    REQUIRED_FIELDS = [
        # HEADER_VERSION_KEY,
        HEADER_DATE_KEY,
        HEADER_NAME_KEY,
        HEADER_LANG_KEY,
        HEADER_HASH_KEY
    ]

    def __init__(self):
        self._store = {} #UnsortableOrderedDict()
        self._store[HEADER_VERSION_KEY] = self.HEADER_VERSION

    def __repr__(self):
        els = ', '.join(f"{name}={val}" for name, val in self)
        return f"PadHeader({els})"

    def __iter__(self):
        yield from self._store.items()

    def add(self, name: str, val: Any):
        self._store[name] = val

    def add_data(self, data: Dict[str, Any]):
        for name, val in data.items():
            self.add(name, val)

    def ensure_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if field not in self._store:
                raise MisssingHeaderField(field)

    def encode(self):
        """Encode this header using whatever format"""
        self.ensure_required_fields()
        with io.StringIO() as stream:
            yaml.dump(self._store, stream, sort_keys=False)
            txt = stream.getvalue()
            return txt

    def get_text(self):
        txt = f"{HEADER_START_STRING}\n"
        txt += self.encode()
        txt += f"{HEADER_END_STRING}\n"
        return txt

    @classmethod
    def extract_header(cls, contents: str) -> Tuple["PadHeader", str]:
        start_loc = contents.find(HEADER_START_STRING)
        if start_loc == -1:
            raise NoHeaderFound()
        start_loc = start_loc + len(HEADER_START_STRING) + 1

        end_loc = contents.find(HEADER_END_STRING)
        if end_loc == -1:
            raise NoHeaderFound()
        header_str = contents[start_loc:end_loc]

        # Now, scan for the next newline after our comment block
        start_of_content = contents.find("\n", end_loc) + 1
        start_of_content = contents.find("\n", start_of_content) + 1

        remaining = contents[start_of_content:]
        return PadHeader.from_string(header_str), remaining

    @classmethod
    def from_string(cls, header_str: str) -> "PadHeader":
        logger.debug("Loading header from string")

        with io.StringIO() as stream:
            stream.write(header_str)
            stream.seek(0)
            data = yaml.safe_load(stream)

            header = cls.from_data(data)
            logger.debug("Got header %s", header)
            return header

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> "PadHeader":
        header = PadHeader()
        header.add_data(data)
        header.ensure_required_fields()
        return header

    def get_language(self) -> PadLanguage:
        return PadLanguage.from_string(self._store[HEADER_LANG_KEY])

    def get_date(self) -> datetime:
        return self._store[HEADER_DATE_KEY]

    def get_hash(self) -> str:
        return self._store[HEADER_HASH_KEY]

    def get_name(self) -> str:
        return self._store[HEADER_NAME_KEY]


@dataclass
class PadRecord(object):
    """A pad that can be saved"""
    pad_name: str
    pad: PipePad
    date_added: date = None

    def __post_init__(self):
        self.date_added = self.date_added or datetime.now()

    def get_pad_name(self):
        logger.debug("Getting pad file name for %s", self)
        return Path(f"foo.{PAD_EXTENSION}.{self.pad.language.extension}")

    # def pad_header(self):
    #     """The header at the beginning of pad text with all the info about the pad
    #
    #     Full output Depends on the language the pad is in, the comment function takes care of that
    #
    #     """

    def get_pad_header(self) -> str:
        header = PadHeader()
        header.add(HEADER_NAME_KEY, self.pad_name)
        header.add(HEADER_DATE_KEY, self.date_added)
        header.add(HEADER_HASH_KEY, self.pad.get_hash())
        header.add(HEADER_LANG_KEY, self.pad.language.name)

        txt = header.get_text()
        txt = self.pad.language.comment_block(txt)

        return txt

    @classmethod
    def load_from_file(cls, filename, ignore_hash_mismatch=False):
        logger.debug("Loading pad from file %s", filename)
        with open(filename, 'rb') as f:
            contents = f.read().decode("utf-8")

            header, contents = PadHeader.extract_header(contents)

            dt = header.get_date()
            lang = header.get_language()
            name = header.get_name()
            header_hash = header.get_hash()
            pad = PipePad(contents=contents, language=lang)
            pad_hash = pad.get_hash()

            if header_hash != pad_hash:
                args = ("Hash mismatch, header=%s pad=%s", header_hash, pad_hash)
                if ignore_hash_mismatch:
                    print(logger.level)
                    logger.debug(*args)
                else:
                    logger.error(*args)
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

    def differs_from_file(self, fpath: PathLike):
        """Determine if the text version of this records differs from a given file"""
        txt = self.get_full_text()

        with open(fpath) as f:
            fil_txt = f.read()

            return fil_txt != txt


    # def __repr__(self):
    #     return f"PadRecord(pad_name={self.pad_name}, " \
    #            f"pad_hash={self.pad.hash}, " \
    #            f"date_added={self.date_added}, " \
    #            f"pad_contents={self.pad.short_contents})"
