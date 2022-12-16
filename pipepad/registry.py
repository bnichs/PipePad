import logging
import os
from abc import abstractmethod
from dataclasses import dataclass, asdict
from os import PathLike
from pathlib import Path
from typing import List, Self

from pipepad.config_old import LATEST_PAD_NAME
from pipepad.language import PadLanguage, ALL_LANGUAGES
from pipepad.pad import PipePad
from pipepad.record import PadRecord

logger = logging.getLogger(__name__)


LATEST = -1


class NoPadByThatName(Exception):
    pass


@dataclass
class PadRepo():
    name: str
    # a single source of pads
    @classmethod
    def from_settings(cls, d: dict):
        logger.debug("Making pad repo from settings")

        rtype = d.get("type", None)

        if not rtype:
            return LocalPadRepo(**d)
        elif rtype == "git":
            raise
            pass

    def as_dict(self):
        raise

    @abstractmethod
    def register_pad(self, name: str, pad: PipePad, **kwargs):
        pass

    @abstractmethod
    def list_pads(self) -> List[str]:
        pass

    @abstractmethod
    def get_latest(self, name: str) -> PipePad:
        pass

    def list_latest_pads(self) -> List[Self]:
        pads = []
        for pname in self.list_pads():
            pad = self.get_latest(pname)
            pads.append(pad)
        return pads

    def pprint(self, **kwargs):
        print(self.pformat(**kwargs))

    def pformat(self, fmt: str = DEFAULT_FMT):
        if fmt == "table":
            data = []
            for pad in self.list_latest_pads():
                d = {
                    "name": pad
                }
                data.append(d)
                pass
            return tabulate(data, headers="keys")
        elif fmt == "plain":
            for pad in self.list_pads():
                print(pad)

    def get_latest_pad_name(self, language: PadLanguage) -> str:
        return f"{LATEST_PAD_NAME}.{language.extension}"


@dataclass
class LocalPadRepo(PadRepo):
    """
    Used to persist pads in an easy to use format.

    All pads are within a given storage_path, with each pad at its own folder.

    storage_path:
        - pad1
            - pad1.pad.py
            - {date1}.pad.py
            - {date2}.pad.py
            - {date3}.pad.py
        - pad2
            ...
        - pad3
            ...

    New pads registered which match the contents of latest will not be saved
    New pads registered will have latest pointed to them
    """
    path: PathLike

    def as_dict(self):
        return asdict(self)

    def __post_init__(self):
        logger.debug("Setting up registry %s at %s", self.name, self.path)

    def _load_registry(self):
        # TODO
        pass

    def get_pad_dir(self, pad_name: str) -> PathLike:
        """Given a pad_name, find the directorry it should be in """
        pad_dir = os.path.join(self.path, pad_name)
        return Path(pad_dir)


    def get_latest_pad_path(self, pad_name: str, language: PadLanguage=None):
        def get_fil(lang):
            latest_name = self.get_latest_pad_name(lang)
            return os.path.join(self.get_pad_dir(pad_name), latest_name)
        if not language:
            # Looks for a latest in every language
            for lang in ALL_LANGUAGES:
                fil = get_fil(lang)
                if os.path.exists(fil):
                    return fil
            raise
        else:
            return get_fil(language)

    def get_pad_path(self, pad_record: PadRecord, get_generic=False) -> PathLike:
        """

        :param pad_record:
        :param get_generic: If set, get a generic name instead of the registry name
        :return:
        """
        pad_dir = self.get_pad_dir(pad_record.pad_name)

        if get_generic:
            fil_name = pad_record.get_generic_pad_name()
        else:
            fil_name = pad_record.get_registry_pad_name()

        pad_path = os.path.join(pad_dir, fil_name)

        return Path(pad_path)

    def ensure_dir(self, fpath):
        d = os.path.dirname(fpath)
        os.makedirs(d, exist_ok=True)

    def link_latest(self, pad_record: PadRecord, pad_path: PathLike, overwrite_latest=True):
        """Link the latest pad to pad_path."""
        logger.debug("Setting up latest pad to be %s", pad_path)

        latest_pad_path = self.get_latest_pad_path(pad_record.pad_name, pad_record.pad.language)
        # logger.debug("Latest is at %s", pad_path)

        logger.debug("Linking %s to %s", latest_pad_path, pad_path)
        print(latest_pad_path)
        if os.path.islink(latest_pad_path):
            pointing_to = os.path.realpath(latest_pad_path)
            logger.debug("Latest pad already exists at %s pointing to %s. Overwriting...", latest_pad_path, pointing_to)

            if not overwrite_latest:
                raise
            os.remove(latest_pad_path)
        os.symlink(os.path.abspath(pad_path), latest_pad_path)
        # os.symlink(latest_pad_path, pad_path)

    def register_pad(self, name: str, pad: PipePad, makedirs=True):
        # TODO handle dupe pad hashes
        logger.debug("Registering pad with name %s", name)
        record = PadRecord(pad_name=name, pad=pad)

        pad_path = self.get_pad_path(record)

        if makedirs:
            self.ensure_dir(pad_path)

        out = record.save_to_file(fpath=pad_path)

        self.link_latest(pad_record=record, pad_path=out)

        print(out)
        print(repr(record))

        # TODO return (?)

    def list_pads(self) -> List[str]:
        # TODO metadata handling, need date, latest, hashes(?)
        pads = []
        for fil in os.listdir(self.storage_path):
            print(fil)
            pads.append(fil)
        return pads

    def list_pad_dir(self, pad_name: str):
        pad_dir = self.get_pad_dir(pad_name)
        logger.debug("Looking in %s", pad_dir)

        pads = os.listdir(pad_dir)
        return pads

    def get_latest(self, pad_name: str) -> PadRecord:
        logger.debug("Getting latest pad with name %s", pad_name)

        pad_path = self.get_latest_pad_path(pad_name)

        print(pad_path)
        try:
            record = PadRecord.load_from_file(pad_path)
        except FileNotFoundError as e:
            logger.error(e)
            raise NoPadByThatName(pad_name)
        return record

    def get_pad(self, pad_name: str, version=LATEST) -> PadRecord:
        logger.debug("Getting pad with name %s", pad_name)

        if version == LATEST:
            return self.get_latest(pad_name)


        pads = self.list_pads()
        if pad_name not in pads:
            raise NoPadByThatName(pad_name)

        pads_in_dir = self.list_pad_dir(pad_name)

        logger.debug("Found pads %s", pads_in_dir)

        raise



class PadRepo():
    # a single source of pads
    pass


class RemotePadRepo():
    pass


class LocalPadRepo():
    pass


class LocalPadRegistry(PadRegistry):
    #  a source of many repos
    pass


class RemotePadRegistry(PadRegistry):
    # Needed?
    pass