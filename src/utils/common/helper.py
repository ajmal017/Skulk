import sys
import os
import traceback
from src.main.skulk_objects import SkulkObject as sb
from src.utils.error_book.errorbook import ErrorBook
from src.utils.gcloud.gstoragehelper import StorageHelper
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


    def isHrhdInLocal(self, tdate , symbol):
        try:
            path = os.path.join(sb.get_with_base_path("common", "hrhd_local_path"), tdate, symbol+".csv")
            if os.path.exists(path):
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


