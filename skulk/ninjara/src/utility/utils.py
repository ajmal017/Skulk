import traceback
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from base_utils.error_book.errorbook import ErrorBook
from base_utils.gcloud.gsheet import GSheet

log = None
error = None
class NinjaraUtils:
    def __init__(self, logger):
        global log, error
        log = ninjaraObj.log
        error = ErrorBook(log)
        self.gsheet = GSheet(log)

    def order_info(self, order_dict):
        try:
            log.info(order_dict)
            print("***** ORDER DETAILS ******")
            print(order_dict)
            print("***** ************* ******")
            self.gsheet.appendRow(ninjaraObj.order_sheet, list(order_dict.values()))
        except Exception as ex:
            error.handle(ex, traceback.format_exc())