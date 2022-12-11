import atexit
import logging
import os
import sys
import tempfile
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO

from pipepad.config import APP_NAME, TEMPLATE_PATH, RUN_PAD_PATH

logger = logging.getLogger()


class PadRegistry:
    """Persists pads to be used later"""
    pass


@dataclass
class PipePad:
    """Pad object containing the contents of a pad"""
    contents: str

    def __repr__(self):
        return f"PipePad(hash={self.hash()}, contents={self.short_contents})"

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as f:
            contents = f.read().decode("utf-8")
            return cls(contents)

    def hash(self):
        return hashlib.sha256(self.contents.encode("utf-8")).hexdigest()

    @property
    def short_contents(self):
        return self.contents.split("\n")[10]



class Processor:
    """Processes inputs using a given Pipepad"""


def get_template_pad():
    pad_record = PadRecord.load_from_file(TEMPLATE_PATH)
    template_pad = pad_record.pad
    return template_pad


def get_pad_from_user():

    # with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    #     editor.edit(filename=tf.name, use_tty=True)

    template_pad = get_template_pad()

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




class PadProcessor:
    def run_cmd(self):
        pass

    def process_pad(self, pad, fifo):
        with tempfile.NamedTemporaryFile(suffix=".py") as tf:
            logger.info("Running pad %s", tf.name)
            tf.write(pad.contents.encode("utf-8"))
            tf.flush()

            print(sys.path)
            os.system(f"{RUN_PAD_PATH} {tf.name} {fifo} '{sys.path}'")

        logger.debug("Done running pad")


@dataclass
class StdinProcessor:
    stdin: TextIO
    fifo: str
    """
    Used to process lines in the backgroundby pushing them onto a fifo
    """

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
    atexit.register(lambda: os.remove(fifo_name))

    # Start processing stdin
    stdin_proc = StdinProcessor(sys.stdin, fifo=fifo_name)
    stdin_thread = threading.Thread(target=stdin_proc.start, name="stdin_thread")
    stdin_thread.start()


    # Now get code from user
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
