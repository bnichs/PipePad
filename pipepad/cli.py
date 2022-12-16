import logging

import click

from pipepad.config_old import APP_NAME
from pipepad.language import PYTHON, PadLanguage, ALL_LANGUAGES
from pipepad.pad import PadID
from pipepad.pipepad_lib import PadMaker, PadProcessor
from pipepad.record import PadRecord
from pipepad.registry import PadRegistry, DEFAULT_FMT
from pipepad.util import detect_stdin


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)



def get_default_language():
    ## TODO use configs
    return PYTHON


@click.group(invoke_without_command=True )
@click.option("-l", "--language", type=str, default=get_default_language().name)
# @click.option("-c", "--config-file", type=str, default=...)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, language: PadLanguage, debug: bool):
    has_stdin = detect_stdin()
    logger.debug("Starting with stdin=%s", has_stdin)

    # ctx.invoke(create_pad, language=language)


### Create


# @cli.group(help="Create a thing")
# def create():
#     pass


def get_language_strings():
    return [l.name for l in ALL_LANGUAGES]


@cli.command(name="create", help="Create a new pad")
@click.option("-l", "--language", type=click.Choice(get_language_strings()), default=get_default_language().name)
@click.argument("FILENAME", default=None)
@click.option("-n", "--name", default="new-pad")
def create_pad(language: str, filename: str, name):
    language = PadLanguage.from_string(language)
    logger.debug("Creating pad with lang=%s....", language)

    has_stdin = detect_stdin()
    logger.debug("Starting with stdin=%s", has_stdin)

    maker = PadMaker(process_stdin=has_stdin, language=language)
    pad = maker.run()

    if filename:
        record = PadRecord(pad_name=name, pad=pad)
        record.save_to_file(filename)



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


@list_things.command(name="repos", help="List the repos available")
@click.option("-f", "--format", default=DEFAULT_FMT)
def list_repos(format: str):
    reg = PadRegistry.from_settings()
    reg.pprint(fmt=format)


# @list_things.command(name="pads", help="List the pads available")
# def list_pads(format: str):
#     reg = PadRegistry.from_settings()
#
#     reg.pprint(fmt=format)


@list_things.command(name="pads", help="List the pads")
@click.option("-f", "--format", default=DEFAULT_FMT)
@click.argument("repo", type=str)
def list_pads(repo: str, format: str):
    reg = PadRegistry.from_settings()
    repo = reg.get_repo_by_name(repo)
    repo.pprint(fmt=format)


#
# @cli.group(help="Manage repos")
# def repo():
#     pass


### Configuration

@cli.group(help=f"Configuration for {APP_NAME}")
def config():
    pass
