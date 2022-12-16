import atexit
import logging
import os
import sys
import tempfile
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO

from pipepad.config_old import APP_NAME, PY_TEMPLATE_PATH, RUN_PAD_PATH
from pipepad.language import PYTHON, PadLanguage
from pipepad.pad import PipePad
from pipepad.record import PadRecord
from pipepad.util import get_template_path

logger = logging.getLogger()


def get_template_pad_record(language=PYTHON, **kwargs):
    pad_record = PadRecord.load_from_file(get_template_path(language=language), **kwargs)
    return pad_record


def get_template_pad(language=PYTHON, **kwargs):
    pad_record = get_template_pad_record(language=language, **kwargs)
    template_pad = pad_record.pad
    return template_pad


class PadProcessor:
    """Used to run a pad against stdin using whatever language the pad is in"""
    def run_cmd(self):
        pass

    def process_pad(self, pad, fifo):
        with tempfile.NamedTemporaryFile(suffix=".py") as tf:
            logger.info("Running pad %s", tf.name)
            tf.write(pad.contents.encode("utf-8"))
            tf.flush()

            os.system(f"{RUN_PAD_PATH} {tf.name} {fifo} '{sys.path}'")

        logger.debug("Done running pad")


@dataclass
class StdinProcessor:
    stdin: TextIO
    fifo: str
    """
    Used to process lines in the background by pushing them onto a fifo
    """

    def start(self):
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


@dataclass
class PadMaker:
    """Used to make pads before they are executed"""
    process_stdin: bool
    language: PadLanguage

    def __post_init__(self):
        logger.debug("Making pad with %s", self)

    def get_pad_from_user(self):
        # TODO lang
        template_pad = get_template_pad(language=self.language)

        with tempfile.NamedTemporaryFile(suffix=f".{self.language.extension}") as tf:
            logger.debug("Using tempfile %s", tf.name)
            tf.write(template_pad.contents.encode("utf-8"))
            tf.flush()

            # https://stackoverflow.com/questions/25496295/running-vi-from-python-script
            os.system('vim' + ' "' + tf.name + '" </dev/tty >/dev/tty 2>&1')

            tf.seek(0)

            print("File writen:")
            pad_contents = tf.read()

            user_pad = PipePad(pad_contents.decode("utf-8"), language=self.language)
            logger.debug("Editor saved file %s", tf.name)

            return user_pad

    def run(self) -> PipePad:
        run_id = gen_run_id()
        logger.debug("Running %s", run_id)

        if self.process_stdin:
            fifo_name = f".{run_id}.fifo"
            atexit.register(lambda: os.remove(fifo_name))

            # Start processing stdin
            stdin_proc = StdinProcessor(sys.stdin, fifo=fifo_name)
            stdin_thread = threading.Thread(target=stdin_proc.start, name="stdin_thread")
            stdin_thread.start()

        # Now get code from user
        pad = self.get_pad_from_user()

        if self.process_stdin:
            proc = PadProcessor()
            proc.process_pad(pad, fifo=stdin_proc.fifo)
            stdin_thread.join()
