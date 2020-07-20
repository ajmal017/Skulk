import sys
import os
import datetime
import json
import traceback
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])
from base_utils.error_book.errorbook import ErrorBook
from base_utils.common.skulk_objects import SkulkObjects as sb
from base_utils.gcloud.gstorage import GStorage
log = None
error = None
class Functions:
    datefrmt = "%Y%m%d"

    def __init__(self, logger):
        global log, error
        log = logger
        error = ErrorBook(logger)
        self.gstore = GStorage(log)

    def getTradedays(self, startdate, enddate, excluded=(6, 7)):
        try:
            if type(startdate) is str:
                startdate = datetime.datetime.strptime(self.getPrevTradeday(startdate), self.datefrmt)
            if type(enddate) is str:
                enddate = datetime.datetime.strptime(enddate, self.datefrmt)
            days = []
            log.info("Getting trade day in between {} to {}".format(startdate, enddate))
            while startdate.date() <= enddate.date():
                if startdate.isoweekday() not in excluded:
                    if self.isValidtradeday(startdate):
                        days.append(startdate.strftime(self.datefrmt))
                startdate += datetime.timedelta(days=1)
            log.info(days)
            return days
        except Exception as e:
            error.handle(e, traceback.format_exc(), startdate, enddate)

    def isValidtradeday(self, tdate, excluded=(6, 7)):
        try:
            if type(tdate) is str:
                tdate = datetime.datetime.strptime(tdate, self.datefrmt)
            if tdate.isoweekday() not in excluded:
                if tdate.strftime(self.datefrmt) not in json.loads(
                    sb.get_value("nse_holiday_list", "trading_holiday_" + str(tdate.year))):
                    log.debug("Given date %s is valid trade date" % tdate)
                    return True
            log.debug("Given date %s is not a valid trade date might be weekend or holiday" % tdate)
            log.debug("Holiday list :" + sb.get_value("nse_holiday_list", "trading_holiday_" + str(tdate.year)))
            return False
        except Exception as e:
            error.handle(e, traceback.format_exc(), tdate)

    def getPrevTradeday(self, tdate):
        try:
            if type(tdate) is str:
                tdate = datetime.datetime.strptime(tdate, self.datefrmt)
            while True:
                offset = max(1, (tdate.weekday() + 6) % 7 - 3)
                timedelta = datetime.timedelta(offset)
                prvtradedate = tdate - timedelta
                if self.isValidtradeday(prvtradedate):
                    return prvtradedate.strftime(self.datefrmt)
                else:
                    log.debug(
                        str(prvtradedate) + "is not a valid trade date looping back to get next prev valid trade date.")
                    tdate = prvtradedate
        except Exception as e:
            error.handle(e, traceback.format_exc(), tdate)

    def getBacktestlist(self, nse_symbols_file=None):
        if nse_symbols_file is None:
            nse_symbols_path = sb.backtest_list_path
        else:
            nse_symbols_path = os.path.join(sb.master_path,nse_symbols_file)
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
            error.handle(ex,traceback.format_exc(),  nse_symbols_file)

    def isHrhdInLocal(self, tdate, symbol, contract_type="STK"):
        try:
            path = os.path.join(sb.get_with_base_path("common", "hrhd_local_path"), contract_type, tdate,
                                symbol + ".csv")
            if os.path.exists(path):
                log.info("HRHD exist in local for {} - {} - {}".format(tdate, symbol, path))
                return path
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(), tdate, symbol)

    def isHrhdPresent(self, tdate, symbol):
        try:
            lpath = self.isHrhdInLocal(tdate, symbol)
            if lpath is not None:
                return lpath
            else:
                gblob = self.ishrhdInGstore(tdate, symbol)
                if gblob is not None:
                    return gblob
                return None
        except Exception as e:
            error.handle(e, traceback.format_exc(), tdate, symbol)

    def ishrhdInGstore(self, tdate, symbol, contract_type="STK"):
        try:
            blob_name = os.path.join(contract_type, tdate, symbol + ".csv")
            file_path = self.gstore.downloadBlob(sb.hrhd_bucket, blob_name, sb.hrhd_local_path)
            if file_path is not None:
                log.info(
                    "HRHD Blob downloaded to {} for {} - {}".format(
                        file_path, tdate, symbol)
                )
                return file_path
            return None
        except Exception as e:
            error.handle(e, traceback.format_exc(), tdate, symbol, type)
            return None