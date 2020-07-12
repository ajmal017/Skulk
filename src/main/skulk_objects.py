import os
import sys
from configparser import ConfigParser
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

class SkulkObject:
    log = None
    parser = ConfigParser()
    os.environ['SKULK_CONFIG'] = os.getcwd()[:os.getcwd().find("Skulk") + len(
        "Skulk")] + '/config/config.ini'
    parser.read(os.getenv("SKULK_CONFIG"))
    skulk_path = os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")]

    @staticmethod
    def get_value(head, key):
        return SkulkObject.parser.get(head, key)