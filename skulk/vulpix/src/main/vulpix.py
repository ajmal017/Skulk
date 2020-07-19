import sys
import os
import argparse
import traceback
import random
import pandas as pd
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])
from skulk.vulpix.src.main.vulpix_objects import VulpixObject as vo
from skulk.vulpix.src.loghandler.log_handler import LogHandler
from base_utils.error_book.errorbook import ErrorBook
from base_utils.common.common_fuctions import Functions
from skulk.marlfox.src.main.marlfox import Marlfox

log = None
error = None

class Skulk:

    def __init__(self, startdate=None, enddate=None, ins_list="ind_nifty10.json"):
        global log, error
        LogHandler().set_logger()
        log = vo.log
        error = ErrorBook(log)
        self.start_date = startdate
        self.end_date = enddate
        self.instrument_list = ins_list
        self.comfunc = Functions(log)
        self.marlfox = Marlfox()


    def readinessProcess(self):
        try:
            # Getting valid trading days
            trading_dates = self.comfunc.getTradedays(self.start_date, self.end_date)
            log.info(trading_dates)
            instruments = self.comfunc.getBacktestlist(self.instrument_list)
            log.info(instruments)
            for dt in trading_dates:
                for inst in instruments:
                    if self.comfunc.isHrhdPresent(dt,inst) is None:
                        self.marlfox.worker_as_process_ohlc_data(inst,dt,random.randint(1,3))
                    ohlc = pd.read_csv(self.comfunc.isHrhdInLocal(dt,inst))
                    for ind in ohlc.index:
                        print(ohlc['time'][ind], ohlc['price'][ind], ohlc['open'][ind], ohlc['high'][ind], ohlc['low'][ind]
                              ,ohlc['close'][ind], ohlc['volume'][ind])
        except Exception as e:
            error.handle(e, traceback.format_exc())


def sysArghandler():
    try:

        cmdLineParser = argparse.ArgumentParser("Skulk Backtest :")
        cmdLineParser.add_argument("-sd", "--startdate", action="store", type=str, dest="startdate",
                                   default="20200424", help="Backtest start date, eg: 20191025")
        cmdLineParser.add_argument("-ed", "--enddate", action="store", type=str, dest="enddate",
                                   default="20200423", help="Backtest end date, eg: 20191025")
        cmdLineParser.add_argument("-l", "--list", action="store", type=str, dest="ins_list",
                                   default="ind_nifty2.json", help="symbol lists")

        args = cmdLineParser.parse_args()
        skObj = Skulk(startdate=str(args.startdate),
                      enddate=str(args.enddate),
                      ins_list=str(args.ins_list))

    except Exception as ex:
        log.error(traceback.format_exc())
        log.error(ex)

if __name__ == "__main__":
    skObj = Skulk("20200713", "20200716", "ind_nifty10.json")
    skObj.readinessProcess()




