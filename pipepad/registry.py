import hashlib
import logging
from dataclasses import dataclass
from datetime import date, datetime
from os import PathLike

from pipepad.pipepad_lib import PipePad


logger = logging.getLogger(__name__)


@dataclass
class PadRecord(object):
    pad_name: str
    date_added: date
    pad: PipePad

    # def __repr__(self):
    #     return f"PadRecord(pad_name={self.pad_name}, " \
    #            f"pad_hash={self.pad.hash}, " \
    #            f"date_added={self.date_added}, " \
    #            f"pad_contents={self.pad.short_contents})"


@dataclass
class PadRegistry:
    repo_name: str
    storage_path: PathLike

    def _load_registry(self):
        pass

    def register_pad(self, name: str, pad: PipePad):
        dt = datetime.now()
        logger.debug("Registering pad with name %s at time %s", name, dt)

        record = PadRecord(name, dt, pad)
        print(repr(record))



        raise
        pass


m = hashlib.sha256()
print(type(m))