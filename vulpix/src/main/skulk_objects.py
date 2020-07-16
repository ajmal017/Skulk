import os
import sys
from configparser import ConfigParser
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

class SkulkObject:
    log = None
    parser = ConfigParser()
    skulk_path = os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")]
    os.environ['SKULK_CONFIG'] = skulk_path + '/config/vulpix/config.ini'
    parser.read(os.getenv("SKULK_CONFIG"))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(str(skulk_path),parser.get("common", "gkey"))
    master_path = os.path.join(skulk_path,parser.get("common", "master_path"))
    ib_map_path =  os.path.join(master_path,"IB_NSE_Map.json")
    backtest_list_path = os.path.join(master_path, parser.get("common", "backtest_list"))
    hrhd_bucket = parser.get("common", "hrhd_bucket")
    hrhd_local_path = os.path.join(skulk_path,"hrhd_bank")


    @staticmethod
    def get_value(head, key):
        return SkulkObject.parser.get(head, key)

    @staticmethod
    def get_with_base_path(head, key):
        return os.getcwd()[:os.getcwd().find("Skulk") + len("Skulk")] + SkulkObject.parser.get(
            head, key)
