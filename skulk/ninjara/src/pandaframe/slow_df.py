import os
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from skulk.ninjara.src.pandaframe import slow_indicators as indi_obj
from base_utils.error_book.errorbook import ErrorBook
# from src.loghandler import log
import traceback
import time
# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()
import pandas as pd

# logger = ninjaraObj.log

error = ErrorBook(ninjaraObj.log)
class SlowDF(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_slow_min_df(ticks):

        def get_ohlc():
            try:
                data = pd.DataFrame(ninjaraObj.slow_min_ticks, columns=['time', 'price'])
                data['time'] = pd.to_datetime(data['time'], unit='s', utc=True)
                data = data.set_index('time')
                # data = data.tz_convert(tz='Asia/Kolkata')
                ti = data.loc[:, ['price']]
                slow_min_bars = ti.price.resample(str(ninjaraObj.slow_min)+'min').ohlc()
                for index, row in slow_min_bars.iterrows():
                    # print('*', row)
                    ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.append(row, sort=False)
                    break
                indi_obj.load_indicators()
            except Exception as ex:
                error.handle(ex, traceback.format_exc())
        tick_time = ticks.get('Timestamp')
        tick_price = ticks.get('Price')
        try:
            if len(ninjaraObj.slow_min_ticks) > 0:

                if (int(str(time.strftime("%M", time.localtime(int(tick_time)))))) > ninjaraObj.cur_slow_min-1:
                    # print('@', ninjaraObj.cur_slow_min)
                    # print(ninjaraObj.slow_min_ticks[0][0], ' - ', ninjaraObj.slow_min_ticks[len(ninjaraObj.slow_min_ticks)-1][0])
                    get_ohlc()
                    ninjaraObj.slow_min_ticks.clear()
                    ninjaraObj.slow_min_ticks.append([tick_time, tick_price])
                    ninjaraObj.cur_slow_min = (int(str(time.strftime("%M", time.localtime(int(tick_time)))))) + ninjaraObj.slow_min
                else:
                    ninjaraObj.slow_min_ticks.append([tick_time, tick_price])

                if (int(str(time.strftime("%M", time.localtime(int(tick_time))))) == 0) and ninjaraObj.cur_slow_min >= 59:
                    ninjaraObj.cur_slow_min = ninjaraObj.cur_slow_min - 60
            else:
                ninjaraObj.cur_slow_min = int(str(time.strftime("%M", time.localtime(int(tick_time))))) + ninjaraObj.slow_min
                ninjaraObj.slow_min_ticks.append([tick_time, tick_price])

        except Exception as ex:
                error.handle(ex, traceback.format_exc())



