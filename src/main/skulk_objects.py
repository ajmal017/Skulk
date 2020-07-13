import os
import sys
from configparser import ConfigParser
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

class SkulkObject:
    log = None
    parser = ConfigParser()
    skulk_path = os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]
    os.environ['SKULK_CONFIG'] = skulk_path + '/config/config.ini'
    parser.read(os.getenv("SKULK_CONFIG"))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(str(skulk_path),parser.get("common", "gkey"))

    hrhd_bucket = "hrhd"

    @staticmethod
    def get_value(head, key):
        return SkulkObject.parser.get(head, key)

    @staticmethod
    def get_with_base_path(head, key):
        return os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")] + SkulkObject.parser.get(
            head, key)
