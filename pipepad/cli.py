import logging

import click

from pipepad.config_old import APP_NAME
from pipepad.language import PYTHON, PadLanguage, ALL_LANGUAGES
from pipepad.pipepad_lib import PadMaker, PadProcessor
from pipepad.util import detect_stdin


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def get_default_language():
    ## TODO use configs
    return PYTHON


@click.group(invoke_without_command=True )
@click.option("-l", "--language", type=str, default=get_default_language().name)
@click.option('--debug/--no-debug', default=False)
def cli(language: PadLanguage, debug: bool):
    has_stdin = detect_stdin()
    logger.debug("Starting with stdin=%s", has_stdin)



### Create


# @cli.group(help="Create a thing")
# def create():
#     pass


def get_language_strings():
    return [l.name for l in ALL_LANGUAGES]


@cli.command(name="create", help="Create a new pad")
@click.option("-l", "--language", type=click.Choice(get_language_strings()), default=get_default_language().name)
def create_pad(language: str):
    language = PadLanguage.from_string(language)
    logger.debug("Creating pad with lang=%s....", language)

    has_stdin = detect_stdin()
    logger.debug("Starting with stdin=%s", has_stdin)

    maker = PadMaker(process_stdin=has_stdin, language=language)
    maker.run()


### Run
@cli.command(name="run", help="Run pads")
@click.argument("PAD_ID", type=str, required=True)
def run_pad(pad_id: str):
    logger.debug("Trying to run %s", pad_id)

    # TODO handle stdin or not

    pad_id = PadID.from_str(pad_id)
    pad = ...  # Get from registry

    proc = PadProcessor()
    proc.process_pad(pad, fifo=...)


### List


@cli.group(name="list", help="List things")
def list_things():
    pass


@list_things.command(help="List the pads")
def list_pads():
    pass

#
# @cli.group(help="Manage repos")
# def repo():
#     pass


### Configuration

@cli.group(help=f"Configuration for {APP_NAME}")
def config():
    pass
