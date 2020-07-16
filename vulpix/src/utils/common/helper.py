import sys
import os
import traceback
import json
from vulpix.src.main.skulk_objects import SkulkObject as sb
from vulpix.src.utils.error_book.errorbook import ErrorBook
from vulpix.src.utils.gcloud.gstoragehelper import StorageHelper
sys.path.append(sb.skulk_path)
log = None
error = None
class CommonHelper:
    ghelp = None
    def __init__(self):
        global log, error
        log = sb.log
        error = ErrorBook()
        self.ghelp = StorageHelper()


    def isHrhdInLocal(self, tdate , symbol, contract_type = "STK"):
        try:
            path = os.path.join(sb.get_with_base_path("common", "hrhd_local_path"),contract_type, tdate, symbol+".csv")
            if os.path.exists(path):
                log.info("HRHD exist in local for {} - {} - {}".format(tdate,symbol,path))
                return path
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(),tdate , symbol)

    def isHrhdPresent(self, tdate , symbol):
        try:
          lpath = self.isHrhdInLocal(tdate,symbol)
          if lpath is not None:
              return lpath
          else:
            gblob = self.ghelp.ishrhdPresetInGstorage(tdate,symbol)
            if gblob is not None:
                return gblob
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(),tdate , symbol)

    def getBacktestlist(self, nse_symbols_path=sb.backtest_list_path):
        try:
            nse_json = json.loads(open(str(nse_symbols_path)).read())
            map_json = json.loads(open(str(sb.ib_map_path)).read())
            instruments = list()
            for cmp in nse_json:
                instruments.append(cmp['Symbol'])
                for sym in map_json:
                    if sym['NSE_Symbol'] == cmp['Symbol']:
                        instruments[len(instruments)-1] = sym['IB_Symbol']
                        break
            return instruments
        except Exception as ex:
            log.error("No mapping value found for NSE Symbol:%s" % nse_symbols_path)
            log.error(traceback.format_exc())
