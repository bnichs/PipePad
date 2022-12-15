#!/usr/bin/env python
"""
Updates everything in the template folder and makes sure the headers and hashes are good.
"""
import logging
import os

from pipepad.config_old import TEMPLATE_DIR
from pipepad.record import PadRecord


logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def update_template(fpath: str):
    fil = os.path.basename(fpath)
    logger.debug("Updating template %s at %s", fil, fpath)
    record = PadRecord.load_from_file(fpath, ignore_hash_mismatch=True)

    if record.differs_from_file(fpath):
        # save the differences
        logger.info("Template %s has changes, save them?", fpath)
        yes_or_no = input("Template has changes, save them? (y/n)")

        if yes_or_no in ["y", 'Y']:
            logger.debug("User says save")
            record.save_to_file(fpath=fpath)
        else:
            logger.info("Nothing to do")
    else:
        logger.info("No updates needed for %s", fpath)


def update_templates():
    for fil in os.listdir(TEMPLATE_DIR):
        fpath = os.path.join(TEMPLATE_DIR, fil)
        if fil.startswith("template."):
            update_template(fpath)


if __name__ == '__main__':
    update_templates()
