import logging
import os
import sys
from src.main.skulk_objects import SkulkObject as so
sys.path.append(so.skulk_path)
import shutil


class LogHandler:
    def set_logger(self, name="skulk"):
        log_level = logging.INFO
        if not os.path.exists(so.parser.get('common', 'log_path')):
            os.makedirs(so.parser.get('common', 'log_path'))
        else:
            shutil.rmtree(so.parser.get('common', 'log_path'))
            os.makedirs(so.parser.get('common', 'log_path'))
        if so.parser.get('common', 'log_level').lower() == "info":
            log_level = logging.INFO
        elif so.parser.get('common', 'log_level').lower() == "debug":
            log_level = logging.DEBUG
        elif so.parser.get('common', 'log_level').lower() == "error":
            log_level = logging.ERROR
        elif so.parser.get('common', 'log_level').lower() == "warn":
            log_level = logging.WARNING
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            handlers=[
                logging.FileHandler(so.parser.get('common', 'log_path')+os.sep+name+".log"),
                logging.StreamHandler()
            ]
        )
        so.log = logging.getLogger()