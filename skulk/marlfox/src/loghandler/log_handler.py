import logging
import os
import sys
from skulk.marlfox.src.main.marlfox_object import Marlfox_Objects as mo
# sys.path.append(so.skulk_path)
import shutil


class LogHandler:
    def set_logger(self, name="vulpix"):
        log_level = logging.INFO
        if not os.path.exists(mo.parser.get('common', 'log_path')):
            os.makedirs(mo.parser.get('common', 'log_path'))
        else:
            shutil.rmtree(mo.parser.get('common', 'log_path'))
            os.makedirs(mo.parser.get('common', 'log_path'))
        if mo.parser.get('common', 'log_level').lower() == "info":
            log_level = logging.INFO
        elif mo.parser.get('common', 'log_level').lower() == "debug":
            log_level = logging.DEBUG
        elif mo.parser.get('common', 'log_level').lower() == "error":
            log_level = logging.ERROR
        elif mo.parser.get('common', 'log_level').lower() == "warn":
            log_level = logging.WARNING
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            handlers=[
                logging.FileHandler(mo.parser.get('common', 'log_path')+os.sep+name+".log"),
                logging.StreamHandler()
            ]
        )
        mo.log = logging.getLogger()