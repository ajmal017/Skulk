import logging
import os
import sys
from skulk.vulpix.src.main.vulpix_objects import VulpixObject as vo
# sys.path.append(so.skulk_path)
import shutil


class LogHandler:
    def set_logger(self, name="marlfox"):
        log_level = logging.INFO
        if not os.path.exists(vo.parser.get('common', 'log_path')):
            os.makedirs(vo.parser.get('common', 'log_path'))
        else:
            shutil.rmtree(vo.parser.get('common', 'log_path'))
            os.makedirs(vo.parser.get('common', 'log_path'))
        if vo.parser.get('common', 'log_level').lower() == "info":
            log_level = logging.INFO
        elif vo.parser.get('common', 'log_level').lower() == "debug":
            log_level = logging.DEBUG
        elif vo.parser.get('common', 'log_level').lower() == "error":
            log_level = logging.ERROR
        elif vo.parser.get('common', 'log_level').lower() == "warn":
            log_level = logging.WARNING
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            handlers=[
                logging.FileHandler(vo.parser.get('common', 'log_path')+os.sep+name+".log"),
                logging.StreamHandler()
            ]
        )
        vo.log = logging.getLogger()