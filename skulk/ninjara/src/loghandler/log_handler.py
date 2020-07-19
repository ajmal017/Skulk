import logging
import os
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as no
import shutil


class LogHandler:
    def set_logger(self, name="ninjara"):
        log_level = logging.INFO
        if not os.path.exists(no.parser.get('common', 'log_path')):
            os.makedirs(no.parser.get('common', 'log_path'))
        else:
            shutil.rmtree(no.parser.get('common', 'log_path'))
            os.makedirs(no.parser.get('common', 'log_path'))
        if no.parser.get('common', 'log_level').lower() == "info":
            log_level = logging.INFO
        elif no.parser.get('common', 'log_level').lower() == "debug":
            log_level = logging.DEBUG
        elif no.parser.get('common', 'log_level').lower() == "error":
            log_level = logging.ERROR
        elif no.parser.get('common', 'log_level').lower() == "warn":
            log_level = logging.WARNING
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            handlers=[
                logging.FileHandler(no.parser.get('common', 'log_path')+os.sep+name+".log"),
                logging.StreamHandler()
            ]
        )
        no.log = logging.getLogger()