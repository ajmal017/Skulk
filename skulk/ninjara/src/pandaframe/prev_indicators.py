import sys,os
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from base_utils.error_book.errorbook import ErrorBook
# from src.loghandler import log
import pandas as pd
import traceback

# logger = ninjaraObj.log
error = ErrorBook(ninjaraObj.log)

class prevIndicators(object):

    def moving_average(self):
        try:
            n = int(ninjaraObj.get_value("ma", "interval"))
            FMA = pd.Series(ninjaraObj.fast_min_pd_DF['close'].rolling(n, min_periods=n).mean(), name='MA')
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(FMA)
            SMA = pd.Series(ninjaraObj.slow_min_pd_DF['close'].rolling(n, min_periods=n).mean(), name='MA')
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.join(SMA)

        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def exponential_moving_average(self):
        try:
            n = int(ninjaraObj.get_value("ema", "interval"))
            FEMA = pd.Series(ninjaraObj.fast_min_pd_DF['close'].ewm(span=n, min_periods=n).mean(), name='EMA')
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(FEMA)
            SEMA = pd.Series(ninjaraObj.slow_min_pd_DF['close'].ewm(span=n, min_periods=n).mean(), name='EMA')
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.join(SEMA)

        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def macd(self):
        try:
            n_fast = int(ninjaraObj.get_value("macd", "fast_interval"))
            n_slow = int(ninjaraObj.get_value("macd", "slow_interval"))
            macdsign_n = int(ninjaraObj.get_value("macd", "MACDsign_n"))

            FEMAfast = pd.Series(ninjaraObj.fast_min_pd_DF['close'].ewm(span=n_fast, min_periods=n_slow).mean())
            FEMAslow = pd.Series(ninjaraObj.fast_min_pd_DF['close'].ewm(span=n_slow, min_periods=n_slow).mean())
            FMACD = pd.Series(FEMAfast - FEMAslow, name='MACD')
            FMACDsign = pd.Series(FMACD.ewm(span=macdsign_n, min_periods=macdsign_n).mean(), name='MACDsign')
            FMACDdiff = pd.Series(FMACD - FMACDsign, name='MACDdiff')
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(FMACD)
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(FMACDsign)
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(FMACDdiff)

            SEMAfast = pd.Series(ninjaraObj.slow_min_pd_DF['close'].ewm(span=n_fast, min_periods=n_slow).mean())
            SEMAslow = pd.Series(ninjaraObj.slow_min_pd_DF['close'].ewm(span=n_slow, min_periods=n_slow).mean())
            SMACD = pd.Series(SEMAfast - SEMAslow, name='MACD')
            SMACDsign = pd.Series(SMACD.ewm(span=macdsign_n, min_periods=macdsign_n).mean(), name='MACDsign')
            SMACDdiff = pd.Series(SMACD - SMACDsign, name='MACDdiff')
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.join(SMACD)
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.join(SMACDsign)
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF.join(SMACDdiff)

        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def average_directional_movement_index_fastDF(self):
        try:
            n = int(ninjaraObj.get_value("adx", "interval"))
            n_ADX = int(ninjaraObj.get_value("adx", "interval_ADX"))
            i = 0
            UpI = []
            DoI = []
            for row in ninjaraObj.fast_min_pd_DF.iterrows():
                if i != 0:
                    UpMove = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['high'] - ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['high']
                    DoMove = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['low'] - ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['low']
                    if UpMove > DoMove and UpMove > 0:
                        UpD = UpMove
                    else:
                        UpD = 0
                    UpI.append(UpD)
                    if DoMove > UpMove and DoMove > 0:
                        DoD = DoMove
                    else:
                        DoD = 0
                    DoI.append(DoD)
                i = i + 1
            i = 0
            TR_l = [0]
            for row in ninjaraObj.fast_min_pd_DF.iterrows():
                if i != 0:
                    TR = max(ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['high'], ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['close']) - min(
                        ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['low'], ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['close'])
                    TR_l.append(TR)
                i = i + 1
            TR_s = pd.Series(TR_l)
            ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
            UpI = pd.Series(UpI)
            DoI = pd.Series(DoI)
            PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR, name='PosDI')
            NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR, name='NegDI')
            ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(),
                            name='ADX')
            ninjaraObj.fast_min_pd_DF['ADX'] = ADX.tolist()
            ninjaraObj.fast_min_pd_DF['PosDI'] = PosDI.tolist()
            ninjaraObj.fast_min_pd_DF['NegDI'] = NegDI.tolist()

        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def average_directional_movement_index_slowDF(self):
        try:
            n = int(ninjaraObj.get_value("adx", "interval"))
            n_ADX = int(ninjaraObj.get_value("adx", "interval_ADX"))
            i = 0
            UpI = []
            DoI = []
            for row in ninjaraObj.slow_min_pd_DF.iterrows():
                if i != 0:
                    UpMove = ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['high'] - ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['high']
                    DoMove = ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['low'] - ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['low']
                    if UpMove > DoMove and UpMove > 0:
                        UpD = UpMove
                    else:
                        UpD = 0
                    UpI.append(UpD)
                    if DoMove > UpMove and DoMove > 0:
                        DoD = DoMove
                    else:
                        DoD = 0
                    DoI.append(DoD)
                i = i + 1
            i = 0
            TR_l = [0]
            for row in ninjaraObj.slow_min_pd_DF.iterrows():
                if i != 0:
                    TR = max(ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['high'], ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['close']) - min(
                        ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['low'], ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['close'])
                    TR_l.append(TR)
                i = i + 1
            TR_s = pd.Series(TR_l)
            ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
            UpI = pd.Series(UpI)
            DoI = pd.Series(DoI)
            PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR, name='PosDI')
            NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR, name='NegDI')
            ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(),
                            name='ADX')
            ninjaraObj.slow_min_pd_DF['ADX'] = ADX.tolist()
            ninjaraObj.slow_min_pd_DF['PosDI'] = PosDI.tolist()
            ninjaraObj.slow_min_pd_DF['NegDI'] = NegDI.tolist()
        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def relative_strength_index_fastDF(self):
        try:
            n = int(ninjaraObj.get_value("rsi", "interval"))
            i = 0
            UpI = [0]
            DoI = [0]
            for row in ninjaraObj.fast_min_pd_DF.iterrows():
                if (i != 0):
                    UpMove = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['high'] - ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['high']
                    DoMove = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i - 1]]['low'] - ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[i]]['low']
                    if UpMove > DoMove and UpMove > 0:
                        UpD = UpMove
                    else:
                        UpD = 0
                    UpI.append(UpD)
                    if DoMove > UpMove and DoMove > 0:
                        DoD = DoMove
                    else:
                        DoD = 0
                    DoI.append(DoD)
                i = i + 1
            UpI = pd.Series(UpI)
            DoI = pd.Series(DoI)
            PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
            NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
            RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI')
            ninjaraObj.fast_min_pd_DF['RSI'] = RSI.tolist()
        except Exception as ex:
            error.handle(ex, traceback.format_exc())

    def relative_strength_index_slowDF(self):
        try:
            n = int(ninjaraObj.get_value("rsi", "interval"))
            i = 0
            UpI = [0]
            DoI = [0]
            for row in ninjaraObj.slow_min_pd_DF.iterrows():
                if (i != 0):
                    UpMove = ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['high'] - \
                             ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['high']
                    DoMove = ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i - 1]]['low'] - \
                             ninjaraObj.slow_min_pd_DF.loc[ninjaraObj.slow_min_pd_DF.index[i]]['low']
                    if UpMove > DoMove and UpMove > 0:
                        UpD = UpMove
                    else:
                        UpD = 0
                    UpI.append(UpD)
                    if DoMove > UpMove and DoMove > 0:
                        DoD = DoMove
                    else:
                        DoD = 0
                    DoI.append(DoD)
                i = i + 1
            UpI = pd.Series(UpI)
            DoI = pd.Series(DoI)
            PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
            NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
            RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI')
            ninjaraObj.slow_min_pd_DF['RSI'] = RSI.tolist()
        except Exception as ex:
            error.handle(ex, traceback.format_exc())


    def generate_indicator_serious(self):
        try:
            self.moving_average()
            self.exponential_moving_average()
            self.macd()
            self.average_directional_movement_index_fastDF()
            self.average_directional_movement_index_slowDF()
            self.relative_strength_index_fastDF()
            self.relative_strength_index_slowDF()

        except Exception as ex:
            error.handle(ex, traceback.format_exc())
