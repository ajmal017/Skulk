import gspread
import os
import traceback

# don't remove this unused import ist initialize google cred key
from base_utils.common.skulk_objects import SkulkObjects as sb
from base_utils.error_book.errorbook import ErrorBook

log = None
error = None

class GSheet:
    def __init__(self, logger, workbook="Vulpix-Results"):
        global log, error
        log = logger
        error = ErrorBook(log)
        self.gc = gspread.service_account(filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        self.wb = self.gc.open(workbook)


    def appendRow(self, sheet_name, row):
        try:
            ws = self.wb.worksheet(sheet_name)
            ws.append_row(row, table_range='A1')
        except Exception as ex:
            error.handle(ex, traceback.format_exc(),self.wb.title, sheet_name, row)

    def deletesheet(self, sheet_name):
        try:
            ws = self.wb.worksheet(sheet_name)
            if ws is not None:
                self.wb.del_worksheet(ws)
        except Exception as ex:
            error.handle(ex, traceback.format_exc(), self.wb.title, sheet_name)

if __name__ == "__main__":
    gs = GSheet()
