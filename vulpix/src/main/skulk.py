import sys
import os
import argparse
import traceback
import json
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])
from vulpix.src.main.skulk_objects import SkulkObject as sb
from vulpix.src.loghandler.log_handler import LogHandler
from vulpix.src.utils.error_book.errorbook import ErrorBook
from vulpix.src.utils.trade_days.trading_day import TradingDates
from vulpix.src.utils.common.helper import CommonHelper

log = None
error = None

class Skulk:

    def __init__(self, startdate=None, enddate=None, ins_list="other"):
        global log, error
        LogHandler().set_logger()
        log = sb.log
        error = ErrorBook()
        self.start_date = startdate
        self.end_date = enddate
        self.td = TradingDates()
        self.com = CommonHelper()


    def readinessProcess(self):
        try:
            # Getting valid trading days
            trading_dates = self.td.getTradedays(self.start_date, self.end_date)
            log.info(trading_dates)
            instruments = self.com.getBacktestlist()
            log.info(instruments)


        # Check in local data is available
        # In local if not available check in google cloud storage, if available downlaod to local
        # If not available in local and cloud storage then call hrhd and get data in local and uplod to cloud bucket
        # Complete this process for all the dates and respective companies
        except Exception as e:
            error.handle(e, traceback.format_exc())





def sysArghandler():
    try:
        # agentObj.log.info("Tick Algo Agent - command param handlers")
        cmdLineParser = argparse.ArgumentParser("Skulk Backtest :")
        cmdLineParser.add_argument("-sd", "--startdate", action="store", type=str, dest="startdate",
                                   default="20200424", help="Backtest start date, eg: 20191025")
        cmdLineParser.add_argument("-ed", "--enddate", action="store", type=str, dest="enddate",
                                   default="20200423", help="Backtest end date, eg: 20191025")
        cmdLineParser.add_argument("-l", "--list", action="store", type=str, dest="ins_list",
                                   default="nifty10", help="symbol lists")

        args = cmdLineParser.parse_args()
        skObj = Skulk(startdate=str(args.startdate),
                      enddate=str(args.enddate),
                      ins_list=str(args.ins_list))

    except Exception as ex:
        log.error(traceback.format_exc())
        log.error(ex)

if __name__ == "__main__":
    skObj = Skulk("20200713", "20200716", None)
    skObj.readinessProcess()




