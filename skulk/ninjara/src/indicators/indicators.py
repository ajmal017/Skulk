import os
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
import traceback
from concurrent.futures import ThreadPoolExecutor
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from base_utils.error_book.errorbook import ErrorBook
from skulk.ninjara.src.pandaframe.slow_df import SlowDF as SLDF
from skulk.ninjara.src.pandaframe.fast_df import FastDF as FADF
from skulk.ninjara.src.algos.sapm import Sapm as Sapm

error = None

class Indicators(object):
    sapm_obj_one = None

    def __init__(self):
        global error
        error = ErrorBook(ninjaraObj.log)
        self.sapm_obj_one = Sapm()

    def data_frame(self, ticks):
        SLDF.generate_slow_min_df(ticks)
        FADF.generate_fast_min_df(ticks)

    def exe_sapm(self, ticks):
        self.sapm_obj_one.do_samp(ticks)

    def algo(self, ticks):
        try:
            executors_list = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                if ticks.get('Price') is not None:
                    executors_list.append(executor.submit(self.data_frame(ticks)))
                    executors_list.append(executor.submit(self.exe_sapm(ticks)))

        except Exception as ex:
            error.handle(ex,traceback.format_exc(), ticks)


if __name__ == '__main__':
    a = Indicators()
    a.algo("[[2123123, 12]]")

