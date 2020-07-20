import os

import sys
from datetime import timezone
# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from skulk.ninjara.src.algos.sapm_objects import SapmObjects as so
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from skulk.ninjara.src.utility.utils import NinjaraUtils
from base_utils.error_book.errorbook import ErrorBook

import time, traceback, datetime
# os.environ['TZ'] = 'Asia/Kolkata'
# time.tzset()

log = None
error = None
class Sapm(object):
    entime = None
    ent930am = None
    extime = None
    exit320pm = None
    exit_algo = None
    exit_algo_325pm = None

    def __init__(self):
        global log, error
        log = ninjaraObj.log
        error = ErrorBook(log)
        self.util = NinjaraUtils(log)

        if ninjaraObj.backtest is False:
            self.entime = datetime.datetime.strptime(ninjaraObj.market_date + ' 04:00:00', '%Y%m%d %H:%M:%S')
            self.ent930am = self.entime.timestamp()
            # time.mktime(self.entime.timetuple())
            self.extime = datetime.datetime.strptime(ninjaraObj.market_date + ' 09:40:00', '%Y%m%d %H:%M:%S')
            self.exit320pm = self.extime.timestamp()
            # time.mktime(self.extime.timetuple()) # self.extime.replace(tzinfo=timezone.utc)
        else:
            self.entime = datetime.datetime.strptime(ninjaraObj.market_date + ' 09:30:00', '%Y%m%d %H:%M:%S')
            self.ent930am = self.entime.timestamp()
            # time.mktime(self.entime.timetuple())
            self.extime = datetime.datetime.strptime(ninjaraObj.market_date + ' 15:10:00', '%Y%m%d %H:%M:%S')
            self.exit320pm = self.extime.timestamp()
            # time.mktime(self.extime.timetuple()) # self.extime.replace(tzinfo=timezone.utc)

    def reset_sapm_object(self):
        so.SYMBOL = ninjaraObj.symbol
        so.TI = int(so.check_get_sapm_config('TI'))
        so.DTH = float(so.check_get_sapm_config('DTH'))
        so.TSL = 0.0
        so.SL = 0.0
        so.titicks = []
        so.avgs = []
        so.LBuy_Position = False
        so.SSell_Position = False
        so.LSL_Price = 0
        so.SSL_Price = 0
        so.LB_Price = 0
        so.SS_Price = 0
        so.No_Trades = 0
        so.LSL_Price = 0
        so.SSL_Price = 0
        so.TI_SAPM_LONG = 0
        so.TI_SAPM_SHORT = 0
        so.net_profit = []

    def time_converter(self, utc_ticktime):
        # time.localtime(int(ticktime))))
        if ninjaraObj.backtest is False:
            print("UTC_Tick : " + str(utc_ticktime))
            return time.localtime(int(utc_ticktime + 19800))
        else:
            return time.localtime(int(utc_ticktime))

    def do_samp(self, ticks):
        if ninjaraObj.start_sapm is True:
            self.algo(float(ticks.get('Timestamp')), float(ticks.get('Price')))
            if so.SL == 0.0:
                so.SL = round(ticks.get('Price') * (float(so.check_get_sapm_config('SL')) / 100), 1)
                so.TSL = round(ticks.get('Price') * (float(so.check_get_sapm_config('TSL')) / 100), 1)
                print("STOP LOSS", str(so.SL), " TRAILING STOP LOSS", so.TSL)

    def algo(self, ticktime, tickprice):
        try:
            if ticktime > self.exit320pm:
                if so.LBuy_Position is True:
                    # print("*** LONG EXIT ," + str(
                    #     time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(tickprice))
                    # print("LONG position :" + str(tickprice - so.LB_Price))
                    so.net_profit.append(tickprice - so.LB_Price)
                    so.LBuy_Position = False
                    so.LB_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    # print("NET :" + str(sum(so.net_profit)))
                    # print("Number of TRADES :" + str(so.No_Trades))
                    dt = {"algo": "SAPM",
                          "symbol": ninjaraObj.symbol, "condition": "* LONG EXIT *",
                          "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                          "price": str(tickprice),
                          "position": str(tickprice - so.LB_Price),
                          "net": str(sum(so.net_profit)),
                          "trades": str(so.No_Trades)
                    }
                    self.util.order_info(dt)

                if so.SSell_Position is True:
                    # print("*** SHORT EXIT ," + str(
                    #     time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(tickprice))
                    # print("SHORT position :" + str(so.SS_Price - tickprice))
                    so.net_profit.append(so.SS_Price - tickprice)
                    so.SSell_Position = False
                    so.SS_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    # print("NET :" + str(sum(so.net_profit)))
                    # print("Number of TRADES :" + str(so.No_Trades))
                    dt = {"algo": "SAPM",
                          "symbol": ninjaraObj.symbol, "condition": "* SHORT EXIT *",
                          "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                          "price": str(tickprice),
                          "position": str(so.SS_Price - tickprice), "net": str(sum(so.net_profit)),
                          "trades": str(so.No_Trades)}
                    self.util.order_info(dt)

            if so.LBuy_Position is True:
                if tickprice >= (so.LSL_Price + so.SL + so.TSL):
                    so.LSL_Price = so.LSL_Price + so.TSL
                elif (tickprice <= so.LSL_Price) or\
                    (ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[-1]]['ADX']
                     < ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[len(ninjaraObj.slow_min_pd_DF) - 2]]['ADX']):
                    # print(
                    #     "* LONG EXIT ," + str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(
                    #         tickprice))
                    # print("LONG position :" + str(tickprice - so.LB_Price))
                    so.net_profit.append(tickprice - so.LB_Price)
                    so.LBuy_Position = False
                    so.LB_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    # print("NET :" + str(sum(so.net_profit)))
                    # print("Number of TRADES :" + str(so.No_Trades))
                    dt = {"algo": "SAPM",
                          "symbol": ninjaraObj.symbol, "condition": "* LONG EXIT *",
                          "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                          "price": str(tickprice),
                          "position":str(tickprice - so.LB_Price),
                          "net": str(sum(so.net_profit)),
                          "trades": str(so.No_Trades)}
                    self.util.order_info(dt)

            if so.SSell_Position is True:
                if tickprice <= (so.SSL_Price - so.SL - so.TSL):
                    so.SSL_Price = so.SSL_Price - so.TSL
                elif (tickprice >= so.SSL_Price)or\
                    (ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[-1]]['ADX']
                     < ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[len(ninjaraObj.slow_min_pd_DF) - 2]]['ADX']):
                    # print(
                    #     "* SHORT EXIT ," + str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(
                    #         tickprice))
                    # print("SHORT position :" + str(so.SS_Price - tickprice))
                    so.net_profit.append(so.SS_Price - tickprice)
                    so.SSell_Position = False
                    so.SS_Price = 0
                    so.No_Trades = so.No_Trades + 1
                    # print("NET :" + str(sum(so.net_profit)))
                    # print("Number of TRADES :" + str(so.No_Trades))
                    dt = {"algo": "SAPM",
                          "symbol": ninjaraObj.symbol, "condition": "* SHORT EXIT *",
                          "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                          "price": str(tickprice),
                          "position": str(so.SS_Price - tickprice), "net": str(sum(so.net_profit)),
                          "trades": str(so.No_Trades)}
                    self.util.order_info(dt)

            if (ticktime < self.exit320pm) and (ticktime > self.ent930am):
                if len(so.titicks) > 0:
                    if (float(ticktime) - float(so.titicks[0][0])) >= so.TI:
                        so.titicks.append([ticktime, tickprice])
                        sum_value = 0.0
                        for i in so.titicks:
                            sum_value = sum_value + i[1]
                        if len(so.avgs) < 3:
                            so.avgs.append(sum_value / len(so.titicks))
                        else:
                            so.avgs[0] = so.avgs[1]
                            so.avgs[1] = so.avgs[2]
                            so.avgs[2] = (sum_value / len(so.titicks))
                        if len(so.avgs) == 3:
                            pv_delta = (so.avgs[2] - so.avgs[0]) / so.avgs[2] * 100
                            if pv_delta >= so.DTH:
                                ninjaraObj.long_flags['SL_SAPM'] = 1
                                so.TI_SAPM_LONG = ticktime + 120
                            if ninjaraObj.long_flags['SL_SAPM'] == 1 and ninjaraObj.long_flags['SL_MAEMA'] == 1\
                                    and ninjaraObj.long_flags['SL_ADX'] == 1 and ninjaraObj.long_flags['SL_MACD'] == 1\
                                    and so.LBuy_Position is False:
                                # print("LONG ENTRY ," + str(
                                #     time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(tickprice))
                                so.LB_Price = tickprice
                                so.LBuy_Position = True
                                so.LSL_Price = tickprice - so.SL
                                dt = {"algo": "SAPM",
                                      "symbol": ninjaraObj.symbol, "condition": "* LONG ENTRY *",
                                      "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                                      "price": str(tickprice)
                                      }
                                self.util.order_info(dt)
                            elif ticktime > so.TI_SAPM_LONG:
                                ninjaraObj.long_flags['SL_SAPM'] = 0

                            if pv_delta <= (so.DTH * -1):
                                ninjaraObj.short_flags['SL_SAPM'] = 1
                                so.TI_SAPM_SHORT = ticktime + 120
                            if ninjaraObj.short_flags['SL_SAPM'] == 1 and ninjaraObj.short_flags['SL_MAEMA'] == 1\
                                    and ninjaraObj.short_flags['SL_ADX'] == 1 and ninjaraObj.short_flags['SL_MACD'] == 1\
                                    and so.SSell_Position is False:
                                # print("SHORT ENTRY ," + str(
                                #     time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))) + "," + str(tickprice))
                                so.SS_Price = tickprice
                                so.SSell_Position = True
                                so.SSL_Price = tickprice + so.SL
                                dt = {"algo": "SAPM",
                                      "symbol": ninjaraObj.symbol, "condition": "* SHORT ENTRY *",
                                      "time": str(time.strftime("%D %H:%M:%S", self.time_converter(int(ticktime)))),
                                      "price": str(tickprice)
                                      }
                                self.util.order_info(dt)
                            elif ticktime > so.TI_SAPM_SHORT:
                                ninjaraObj.short_flags['SL_SAPM'] = 0
                        so.titicks.clear()
                    else:
                        so.titicks.append([ticktime, tickprice])
                else:
                    so.titicks.append([ticktime, tickprice])

        except Exception as ex:
            # print(str(ex))
            error.handle(ex,traceback.format_exc())

## this is unit test
if __name__ == '__main__':
    sobj = Sapm()
    testlist = [[1548906300, 165.0], [1548906303, 165.25], [1548906309, 165.15]]
    for item in testlist:
        sobj.algo(item[0], item[1])
    print(so.titicks)
