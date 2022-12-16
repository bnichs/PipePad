import io
import logging
import os.path
from dataclasses import dataclass
from datetime import date, datetime
from os import PathLike
from pathlib import Path
from typing import Any, Tuple, Dict, Self

import yaml

from pipepad.config_old import PAD_EXTENSION, HEADER_START_STRING, HEADER_END_STRING, HEADER_VERSION_KEY, HEADER_DATE_KEY, \
    HEADER_NAME_KEY, HEADER_LANG_KEY, HEADER_HASH_KEY
from pipepad.language import PadLanguage, PythonLanguage
from pipepad.pad import PipePad

logger = logging.getLogger(__name__)


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
        # HEADER_HASH_KEY
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
        """Split the header from the contents using language specific traits"""
        start_loc = contents.find(HEADER_START_STRING)
        if start_loc == -1:
            raise NoHeaderFound()
        start_loc = start_loc + len(HEADER_START_STRING) + 1

        end_loc = contents.find(HEADER_END_STRING)
        if end_loc == -1:
            raise NoHeaderFound()
        header_str = contents[start_loc:end_loc]
        header = PadHeader.from_string(header_str)

        lang = header.get_language()
        if not lang:
            raise

        # The end of what the header is responsible for,
        # now the language decides where content starts
        end_of_header = end_loc + len(HEADER_END_STRING)

        remaining = lang.get_contents(txt=contents, end_of_header=end_of_header)

        return header, remaining

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
        return self._store.get(HEADER_HASH_KEY, None)

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

    # TODO Put in registry.py?
    def get_registry_pad_name(self):
        """
        Get a registry name for this pad

        Registry name: 2021-12-12T23-13-12.{hash}.pad.py
        """
        logger.debug("Getting pad file name for %s", self)
        return Path(f"{self.date_added.isoformat()}.{self.pad.get_short_hash()}.{PAD_EXTENSION}.{self.pad.language.extension}")

    def get_generic_pad_name(self):
        """
        Get a generic name for this pad

        Generic name: hello-foo.pad.py

        Registry name: 2021-12-12T23-13-12.{hash}.pad.py
        """
        logger.debug("Getting pad file name for %s", self)
        return Path(f"{self.pad_name}.{PAD_EXTENSION}.{self.pad.language.extension}")

    def generate_pad_header(self) -> str:
        header = PadHeader()
        header.add(HEADER_NAME_KEY, self.pad_name)
        header.add(HEADER_DATE_KEY, self.date_added)
        header.add(HEADER_HASH_KEY, self.pad.get_hash())
        header.add(HEADER_LANG_KEY, self.pad.language.name)

        txt = header.get_text()
        txt = self.pad.language.comment_block(txt)

        return txt

    def get_full_text(self):
        txt = self.generate_pad_header()
        txt += self.pad.contents
        return txt

    @classmethod
    def create_from_file(cls, filename, language: PadLanguage) -> Self:
        pad = PipePad.create_from_file(filename, language)
        raise

        record = PadRecord()
        logger.debug("Creating pad from file %s", filename)
        with open(filename, 'r') as f:
            contents = f.read()

            pad = PipePad(contents=contents, language=language)




        pass

    @classmethod
    def load_from_file(cls, filename, ignore_hash_mismatch=False) -> Self:
        logger.debug("Loading pad from file %s", filename)
        with open(filename, 'rb') as f:
            contents = f.read().decode("utf-8")

            header, contents = PadHeader.extract_header(contents)

            # TODO this isnt great but it'll have to do for now to find bad extractions
            if HEADER_START_STRING in contents or HEADER_END_STRING in contents:
                print(contents)
                raise

            dt = header.get_date()
            lang = header.get_language()
            name = header.get_name()
            header_hash = header.get_hash()
            pad = PipePad(contents=contents, language=lang)

            logger.debug("Loaded contents from file: %s", repr(pad.contents))
            pad_hash = pad.get_hash()

            if header_hash and header_hash != pad_hash:
                args = ("Hash mismatch, header=%s pad=%s", header_hash, pad_hash)
                if ignore_hash_mismatch:
                    print(logger.level)
                    logger.debug(*args)
                else:
                    logger.error(*args)
                    raise HashMismatch(header_hash, pad_hash)

            return cls(pad=pad, date_added=dt, pad_name=name)

    def save_to_file(self, fname: PathLike=None, save_dir: PathLike=None, fpath: PathLike=None) -> PathLike:
        """
        Save this pad record to a file
        """
        if fpath:
            fname = os.path.basename(fpath)
            save_dir = os.path.dirname(fpath)

        # TODO: Remember how to boolean logic
        if save_dir and fname:
            fpath = os.path.join(save_dir, fname)
        elif save_dir:
            fname = self.get_generic_pad_name()
            fpath = os.path.join(save_dir, fname)
        elif fname:
            fpath = os.path.abspath(fname)
        else:
            fname = self.get_generic_pad_name()
            fpath = os.path.abspath(fname)

        with open(fpath, 'w') as f:
            txt = self.get_full_text()
            f.write(txt)
        logger.debug("Saved pad %s to %s", self.pad_name, fpath)

        return fpath

    def differs_from_file(self, fpath: PathLike):
        """Determine if the text version of this records differs from a given file"""
        txt = self.get_full_text()

        with open(fpath) as f:
            fil_txt = f.read()

            return fil_txt != txt
