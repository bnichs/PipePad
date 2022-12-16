import logging
import os
import shutil
from pathlib import Path

from pipepad.config import settings
from pipepad.config_old import DEFAULT_REPO


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!
EDITOR = "vim -n -E"
EDITOR = "vim "


# In pad functions


def line_generator():
    print(os.environ['PIPEPAD_FIFO'])
    fifo = os.environ.get('PIPEPAD_FIFO', None)

    if not fifo:
        raise

    with open(fifo) as f:
        yield from f


def all_lines():
    pass


def process_line(line):
    pass

def _get_pad_path() -> os.PathLike:
    env_var = settings.pipepad.env_vars.cur_path
    pad_path = os.environ[env_var]
    return Path(pad_path)



def register(name: str, repo: str=DEFAULT_REPO):
    pass


def save(fname: str):
    pad_path = _get_pad_path()

    shutil.copy(pad_path, fname)
    logger.info("Saved pad to %s", fname)
