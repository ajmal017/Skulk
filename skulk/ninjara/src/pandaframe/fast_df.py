import os
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from skulk.ninjara.src.pandaframe import fast_indicators as indi_obj
from base_utils.error_book.errorbook import ErrorBook
import traceback
# from src.loghandler import log
import time
# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()
import pandas as pd

# logger = ninjaraObj.log

log = None
error = None
class FastDF(object):
    def __init__(self):
        global log, error
        log = ninjaraObj.log
        error = ErrorBook(log)
        pass

    @staticmethod
    def generate_fast_min_df(ticks):

        def get_ohlc():
            try:
                data = pd.DataFrame(ninjaraObj.fast_min_ticks, columns=['time', 'price'])
                data['time'] = pd.to_datetime(data['time'], unit='s', utc=True)
                data = data.set_index('time')
                data = data.tz_convert(tz='Asia/Kolkata')
                ti = data.loc[:, ['price']]
                fast_min_bars = ti.price.resample(str(ninjaraObj.fast_min)+'min').ohlc()
                for index, row in fast_min_bars.iterrows():
                    ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.append(row, sort=False)
                    break
                indi_obj.load_indicators()
            except Exception as ex:
                # print(traceback.format_exc())
                error.handle(ex, traceback.format_exc())

        tick_time = ticks.get('Timestamp')
        tick_price = ticks.get('Price')
        try:
            if len(ninjaraObj.fast_min_ticks) > 0:
                if int(str(time.strftime("%M", time.localtime(int(tick_time))))) > ninjaraObj.cur_fast_min - 1:
                    get_ohlc()
                    ninjaraObj.fast_min_ticks.clear()
                    ninjaraObj.fast_min_ticks.append([tick_time, tick_price])
                    ninjaraObj.cur_fast_min = int(str(time.strftime("%M", time.localtime(int(tick_time))))) + ninjaraObj.fast_min
                else:
                    ninjaraObj.fast_min_ticks.append([tick_time, tick_price])
                if (int(str(time.strftime("%M", time.localtime(int(tick_time))))) == 0) and ninjaraObj.cur_fast_min >= 59:
                    ninjaraObj.cur_fast_min = ninjaraObj.cur_fast_min - 60
            else:
                ninjaraObj.cur_fast_min = int(str(time.strftime("%M", time.localtime(int(tick_time))))) + ninjaraObj.fast_min
                ninjaraObj.fast_min_ticks.append([tick_time, tick_price])
        except Exception as ex:
            error.handle(ex, traceback.format_exc())

