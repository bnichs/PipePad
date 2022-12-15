import logging
import os

from pipepad.config_old import DEFAULT_REPO

logger = logging.getLogger(__name__)

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


def register(name: str, repo: str=DEFAULT_REPO):
    pass


def save(fname: str):
    pass
