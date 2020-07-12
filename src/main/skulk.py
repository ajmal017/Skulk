import sys
from src.main.skulk_objects import SkulkObject as sb
sys.path.append(sb.skulk_path)
import traceback
import argparse
import traceback
from src.loghandler.log_handler import LogHandler
from src.utils.trade_days.trading_day import TradingDates

log = None
class Skulk:
    def __init__(self, startdate=None, enddate=None, ins_list=None):
        global log
        LogHandler().set_logger()
        log = sb.log
        log.info("hi")

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
    # Enable to execute vis command promp
    # sysArghandler()
    skObj = Skulk(None, None, None)
    td = TradingDates()

    td.getTradedays("20200103", "20201007")


