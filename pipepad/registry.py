import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime
from os import PathLike

from pipepad.pad import PipePad
from pipepad.record import PadRecord

logger = logging.getLogger(__name__)


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

        record.save_to_file()
        print(repr(record))

        raise
        pass


m = hashlib.sha256()
print(type(m))