import curses
import fileinput
import logging
import shutil
import subprocess
import sys, tempfile, os
import threading
import tty
from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
from subprocess import call
from typing import TextIO

import editor

logger = logging.getLogger(__name__)

logging.basicConfig()
logger.setLevel(logging.DEBUG)



EDITOR = os.environ.get('EDITOR', 'vim')  # that easy!
EDITOR = "vim -n -E"
EDITOR = "vim "



def setup_help_file():
    pass


# initial_message = 'hello there'  # if you want to set up the file somehow
#
#
# def run_editor(py_file):
#     # with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
#     py_file.write(initial_message.encode('utf-8'))
#     py_file.flush()
#
#
#     use_tty = sys.stdin.isatty() and not sys.stdout.isatty()
#     if use_tty:
#         stdout = open("/dev/tty", 'wb')
#     else:
#         stdout = sys.stdout
#
#     log_stty()
#
#     args = EDITOR.split() + [py_file.name]
#     print(args)
#     with tempfile.NamedTemporaryFile(suffix=".tmp") as stdout_tmp:
#         proc = subprocess.run(args, shell=False, text=True, stdin=subprocess.PIPE, close_fds=True)
#         # print(proc.stdout)
#         # print(proc.stderr)
#
#
#     log_stty()
#
#     # do the parsing with `tf` using regular File operations.
#     # for instance:
#     py_file.seek(0)
#     edited_message = py_file.read()
#
#
#     log_stty()
#
#     # curses.setupterm()
#     # sys.stdout.write(curses.tigetstr('sgr0').decode("utf-8"))
#
#     # os.system('stty')
#     # os.system('reset')
#     # tty.setcbreak()
#     # os.system('tty.setcbreak()')
#
#
#     log_stty()
#
#     # subprocess.run(["clear"], shell=True)
#     # os.system("stty sane")
#
#     print("Output:")
#     print(edited_message)
#     for i in range(6):
#         print(i)
#
#
# def run_editor2():
#     # https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python
#     import os
#     import sys
#     import select
#     import termios
#     import tty
#     import pty
#     from subprocess import Popen
#
#     command = 'bash'
#     # command = 'docker run -it --rm centos /bin/bash'.split()
#
#     # save original tty setting then set it to raw mode
#     # old_tty = termios.tcgetattr(sys.stdin)
#     tty.setraw(sys.stdin.fileno())
#
#     # open pseudo-terminal to interact with subprocess
#     master_fd, slave_fd = pty.openpty()
#
#
#     try:
#         # use os.setsid() make it run in a new process group, or bash job control will not be enabled
#         p = Popen(command,
#                   preexec_fn=os.setsid,
#                   stdin=slave_fd,
#                   stdout=slave_fd,
#                   stderr=slave_fd,
#                   universal_newlines=True)
#
#         while p.poll() is None:
#             r, w, e = select.select([sys.stdin, master_fd], [], [])
#             if sys.stdin in r:
#                 d = os.read(sys.stdin.fileno(), 10240)
#                 os.write(master_fd, d)
#             elif master_fd in r:
#                 o = os.read(master_fd, 10240)
#                 if o:
#                     os.write(sys.stdout.fileno(), o)
#     finally:
#         # restore tty settings back
#         # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
#         pass


class PadRegistry:
    """Persists pads to be used later"""
    pass


@dataclass
class PipePad:
    """Pad object containing the contents of a pad"""
    contents: str

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as f:
            contents = f.read().decode("utf-8")
            return cls(contents)



class Processor:
    """Processes inputs using a given Pipepad"""


def get_pad_from_user():

    # with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    #     editor.edit(filename=tf.name, use_tty=True)

    template_pad = PipePad.load_from_file(TEMPLATE_FILE)

    with tempfile.NamedTemporaryFile(suffix=".py") as tf:
        logger.debug("Using tempfile %s", tf.name)
        tf.write(template_pad.contents.encode("utf-8"))
        tf.flush()

        # https://stackoverflow.com/questions/25496295/running-vi-from-python-script
        os.system('vim' + ' "' + tf.name + '" </dev/tty >/dev/tty 2>&1')

        tf.seek(0)

        print("File writen:")
        pad_contents = tf.read()

        user_pad = PipePad(pad_contents.decode("utf-8"))
        print(user_pad)
        # return
        # log_stty()
        # run_editor(tf)
        # log_stty()
        logger.debug("Editor saved file %s", tf.name)

        return user_pad




TEMPLATE_FILE = "./template.py"


# In pad functions
def line_generator():
    pass



class PadProcessor:
    def run_cmd(self):
        pass

    def process_pad(self, pad, fifo):
        with tempfile.NamedTemporaryFile(suffix=".py") as tf:
            logger.info("Running pad %s", tf.name)
            tf.write(pad.contents.encode("utf-8"))
            tf.flush()

            # subprocess.run(["python", tf.name], stdout=sys.stdout)

            print(sys.path)
            os.system(f"./run_pad.sh {tf.name} {fifo} '{sys.path}'")

        logger.debug("Done running pad")
        pass



APP_NAME = "pipepad"


@dataclass
class StdinProcessor:
    stdin: TextIO
    fifo: str = None
    """
    Used to process lines in the backgroundby pushing them onto a fifo
    """

    # def __post_init__(self):
    #     if not self.fifo:
    #         fifo = ""
    #         pass

    def start(self):
        # logger.debug("fooo")
        # path = "test.fifo"
        # os.remove(path)
        # logger.debug("removed")
        os.mkfifo(self.fifo, mode=0o600)
        logger.debug("Made fifo at %s", self.fifo)

        with open(self.fifo, "w") as fifo:
            logger.debug("Starting write to fifo")
            for el in self.stdin:
                logger.debug("Writing %s", el)
                fifo.write(el)

        return self.fifo




def gen_run_id():
    return f"{APP_NAME}.{datetime.now().isoformat()}"


def main():
    run_id = gen_run_id()
    logger.debug("Running %s", run_id)

    fifo_name = f".{run_id}.fifo"

    stdin_proc = StdinProcessor(sys.stdin, fifo=fifo_name)
    # fifo = stdin_proc.fifo
    # fifo = stdin_proc.start()
    stdin_thread = threading.Thread(target=stdin_proc.start, name="stdin_thread")
    stdin_thread.start()
    print(stdin_thread)

    # sys.exit()
    pad = get_pad_from_user()

    print(pad)

    proc = PadProcessor()
    proc.process_pad(pad, fifo=stdin_proc.fifo)


    # Should read this in another thread and pass it to the pad when ready
    # print("From stdin")
    # for el in sys.stdin:
    #     print(el)


if __name__ == "__main__":
    main()
