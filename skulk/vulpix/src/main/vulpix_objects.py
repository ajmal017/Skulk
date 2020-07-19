import os
import sys
from configparser import ConfigParser
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

class VulpixObject:
    log = None
    parser = ConfigParser()
    skulk_path = os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]
    os.environ['VULPIX_CONFIG'] = skulk_path + '/config/vulpix/config.ini'
    parser.read(os.getenv("VULPIX_CONFIG"))

    @staticmethod
    def get_value(head, key):
        return VulpixObject.parser.get(head, key)

    @staticmethod
    def get_with_base_path(head, key):
        return os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")] + VulpixObject.parser.get(
            head, key)
