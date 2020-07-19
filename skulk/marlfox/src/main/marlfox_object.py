import os
from configparser import ConfigParser
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")])


class Marlfox_Objects:
    log = None
    parser = ConfigParser()
    os.environ['MARLFOX_CONFIG'] = str(
        os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]) + "/config/marlfox/config.ini"
    parser.read(os.getenv("MARLFOX_CONFIG"))
    os.environ['HRHD'] = str(
        os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]) + "/skulk/marlfox/src/hrhd"


    @staticmethod
    def get_with_base_path(head, key):
        return str(os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]) + Marlfox_Objects.parser.get(head, key)

    @staticmethod
    def get_value(head, key):
        return Marlfox_Objects.parser.get(head, key)