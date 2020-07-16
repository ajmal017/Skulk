import sys
import datetime
import json
import traceback
from vulpix.src.main.skulk_objects import SkulkObject as sb
from vulpix.src.utils.error_book.errorbook import ErrorBook
sys.path.append(sb.skulk_path)
log = None
error = None
class TradingDates:
    datefrmt = "%Y%m%d"
    def __init__(self):
        global log, error
        log = sb.log
        error = ErrorBook()

    def getTradedays(self, startdate, enddate, excluded=(6, 7)):
        try:
            if type(startdate) is str:
                startdate = datetime.datetime.strptime(self.getPrevTradeday(startdate), self.datefrmt)
            if type(enddate) is str:
                enddate = datetime.datetime.strptime(enddate, self.datefrmt)
            days = []
            log.info("Getting trade daye in between {} to {}".format(startdate, enddate))
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
               if tdate.strftime(self.datefrmt) not in json.loads(sb.get_value("nse_holiday_list","trading_holiday_"+str(tdate.year))):
                   log.debug("Given date %s is valid trade date" % tdate)
                   return True
            log.debug("Given date %s is not a valid trade date might be weekend or holiday" % tdate)
            log.debug("Holiday list :" + sb.get_value("nse_holiday_list","trading_holiday_"+str(tdate.year)))
            return False
        except Exception as e:
            error.handle(e,traceback.format_exc(), tdate)

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
                    log.debug(str(prvtradedate)+ "is not a valid trade date looping back to get next prev valid trade date.")
                    tdate = prvtradedate
        except Exception as e:
            error.handle(e,traceback.format_exc(),tdate)
