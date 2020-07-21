import sys
import os
import argparse
import random
import subprocess
import traceback
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

from skulk.marlfox.src.main.marlfox_object import Marlfox_Objects as marlfoxObj
from skulk.marlfox.src.loghandler.log_handler import LogHandler
from base_utils.error_book.errorbook import ErrorBook
from base_utils.common.common_fuctions import Functions

log = None
error = None

class Marlfox:

    def __init__(self ):
        global log, error
        LogHandler().set_logger()
        log = marlfoxObj.log
        error = ErrorBook(log)
        self.com_func = Functions(log)


    def  worker_as_process_ohlc_data(self, symbol, date, cid, gateway_ip="127.0.0.1",):
        try:
            print("-------------------------------------------")
            print("Data Recordings started for -", symbol)
            hrhd_path=os.getenv("HRHD")
            print(hrhd_path)
            proc = subprocess.call(["python3 "+hrhd_path+"/ib_ohlc.py -cid " +
                             str(cid) + " -ip " + gateway_ip + " -p 4002 -s " + symbol + " -d " + date + " -st STK" +
                             " -ds " + " '30 secs' " + " -edt " + " '1 D' "], shell=True)
            print("-------------------------------------------")

        except Exception as ex:
            error.handle(traceback.format_exc(),gateway_ip, symbol, date, cid)


def main_tick_data():
    cmdLineParser = argparse.ArgumentParser("Vuk History Data Bot :")
    cmdLineParser.add_argument("-ip", "--ip", action="store", type=str,
                               dest="ip", default=marlfoxObj.get_value("common","gateway_ip"), help="The IP to get IB Gateway connection")
    cmdLineParser.add_argument("-d", "--date", action="store", type=str,
                               dest="date", default=marlfoxObj.get_value("common","hrhd_date"),
                               help="Date (yyyymmdd) For eg: 20190131")
    cmdLineParser.add_argument("-cid", "--cid", action="store", type=int,
                               dest="cid", default=random.randint(1,10), help="Unique client id do request")
    cmdLineParser.add_argument("-list", "--list", action="store", type=str,
                               dest="list", default='ind_nifty2.json', help="nifty list 50 or 200")
    args = cmdLineParser.parse_args()
    hrhd_obj = Marlfox()
    log.info("**HRHD Worker Initiated")
    back_test_instruments = hrhd_obj.com_func.getBacktestlist(args.list)
    log.info("Read Nifty instruments")
    i = 1
    # print(len(args.))
    if args.ip is not None:
        gateway_ip = args.ip
        hdate = args.date
        cid = args.cid
    else:
        gateway_ip = marlfoxObj.get_value('common', 'gateway_ip')
        hdate = marlfoxObj.get_value('common', 'hrhd_date')
        cid = 1
    for ins in back_test_instruments:
        log.info(str(i)+" Of Nifty list "+"("+ins+")")
        hrhd_obj.worker_as_process_ohlc_data(ins, hdate, random.randint(1,3), gateway_ip)
        # hrhd_obj.ohlcRun(gateway_ip, ins, hdate, random.randint(1,3))
        i = i+1


if __name__ == '__main__':
    import sys
    main_tick_data()