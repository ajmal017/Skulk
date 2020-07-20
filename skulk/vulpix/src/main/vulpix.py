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
from base_utils.gcloud.gsheet import GSheet
from skulk.marlfox.src.main.marlfox import Marlfox

log = None
error = None

class Skulk:

    def __init__(self, startdate=None, enddate=None, ins_list="ind_nifty2.json"):
        global log, error
        LogHandler().set_logger()
        log = vo.log
        error = ErrorBook(log)
        self.start_date = startdate
        self.end_date = enddate
        self.instrument_list = ins_list
        self.comfunc = Functions(log)
        self.gheet = GSheet(log)
        self.marlfox = Marlfox()


    def readinessProcess(self):
        try:
            # Getting valid trading days
            from skulk.ninjara.src.main.ninjara import NinjaraAgent
            trading_dates = self.comfunc.getTradedays(self.start_date, self.end_date)
            log.info(trading_dates)
            instruments = self.comfunc.getBacktestlist(self.instrument_list)
            log.info(instruments)
            order_sheet = self.gheet.newRandomResultSheet()
            i=0
            for dt in trading_dates:
                for inst in instruments:
                    if self.comfunc.isHrhdPresent(dt,inst) is None:
                        self.marlfox.worker_as_process_ohlc_data(inst,dt,random.randint(1,3))
                    if i > 0:
                        ninjaagent = NinjaraAgent(args_topic = inst,args_symbol = inst,
                                                  args_marketdate = dt,args_backtest=True,
                                                  args_order_sheet = order_sheet)
                        ninjaagent.startLocalLoop(self.comfunc.isHrhdInLocal(dt,inst))
                        del ninjaagent
                i +=1

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
    skObj = Skulk("20200706", "20200707", "ind_nifty2.json")
    skObj.readinessProcess()




