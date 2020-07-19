import os
import sys

# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from base_utils.error_book.errorbook import ErrorBook
# from src.loghandler import log
import pandas as pd
import traceback
import math

# Init Logging Facilities
# logger = ninjaraObj.log
error = ErrorBook(ninjaraObj.log)
def load_indicators():
    try:
        if len(ninjaraObj.fast_min_pd_DF) >= int(ninjaraObj.parser.get('ma', 'interval')):
            moving_average(int(ninjaraObj.parser.get('ma', 'interval')))
        if len(ninjaraObj.fast_min_pd_DF) >= int(ninjaraObj.parser.get('ema', 'interval')):
            exponential_moving_average(int(ninjaraObj.parser.get('ema', 'interval')))
        if len(ninjaraObj.fast_min_pd_DF) >= int(ninjaraObj.parser.get('macd', 'slow_interval')):
            macd(int(ninjaraObj.parser.get('macd', 'fast_interval')), int(ninjaraObj.parser.get('macd', 'slow_interval')))
        if len(ninjaraObj.fast_min_pd_DF) >= int(ninjaraObj.parser.get('adx', 'interval')):
            average_directional_movement_index(int(ninjaraObj.parser.get('adx', 'interval')),
                                               int(ninjaraObj.parser.get('adx', 'interval_ADX')))
        if len(ninjaraObj.fast_min_pd_DF) >= int(ninjaraObj.parser.get('rsi', 'interval')):
            rsi(int(ninjaraObj.parser.get('rsi', 'interval')))

        if ninjaraObj.start_sapm is True:
            flag_it()
    except Exception as ex:
        error.handle(ex,traceback.format_exc())


def flag_it():
    try:
        # Long Entry
        prev_row = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[len(ninjaraObj.fast_min_pd_DF)-2]]
        cur_row = ninjaraObj.fast_min_pd_DF.loc[ninjaraObj.fast_min_pd_DF.index[-1]]
        # MAEMA Flag Settings for long
        if cur_row['EMA'] > prev_row['EMA'] and cur_row['close'] > cur_row['EMA']\
                and prev_row['close'] > prev_row['EMA'] and cur_row['MA'] > prev_row['MA']:
            ninjaraObj.long_flags['FA_MAEMA'] = 1
        else:
            ninjaraObj.long_flags['FA_MAEMA'] = 0
        # RSI Flag Settings for long
        if int(ninjaraObj.parser.get('rsi', 'long_low')) <= cur_row['RSI'] <= int(ninjaraObj.parser.get('rsi', 'long_high')):
            ninjaraObj.long_flags['FA_RSI'] = 1
        else:
            ninjaraObj.long_flags['FA_RSI'] = 0
        # ADX Flag Settings for long
        if cur_row['PosDI'] > cur_row['NegDI'] and cur_row['ADX'] > prev_row['ADX'] and\
                cur_row['ADX'] > cur_row['NegDI']:
            # and cur_row['PosDI'] > prev_row['PosDI']\
            ninjaraObj.long_flags['FA_ADX'] = 1
        else:
            ninjaraObj.long_flags['FA_ADX'] = 0
        # MACD Flag Setting for long
        if cur_row['MACD'] > cur_row['MACDsign'] \
                and (cur_row['MACD']+prev_row['MACD']) > (cur_row['MACDsign']+prev_row['MACDsign']):
            #and cur_row['MACD'] < float(ninjaraObj.parser.get('macd', 'long_range'))\
            ninjaraObj.long_flags['FA_MACD'] = 1
        else:
            ninjaraObj.long_flags['FA_MACD'] = 0

        # Shot Entry
        # MAEMA Flag Settings for shot
        if cur_row['EMA'] < prev_row['EMA'] \
                and cur_row['close'] < cur_row['EMA'] \
                and prev_row['close'] < prev_row['EMA'] and cur_row['MA'] < prev_row['MA']:
            ninjaraObj.short_flags['FA_MAEMA'] = 1
        else:
            ninjaraObj.short_flags['FA_MAEMA'] = 0

        # RSI Flag Settings for shot
        if int(ninjaraObj.parser.get('rsi', 'shot_low')) <= cur_row['RSI'] <= int(ninjaraObj.parser.get('rsi', 'shot_high')):
            ninjaraObj.short_flags['FA_RSI'] = 1
        else:
            ninjaraObj.short_flags['FA_RSI'] = 0

        # ADX Flag Settings for short
        if cur_row['NegDI'] > cur_row['PosDI'] and cur_row['ADX'] > prev_row['ADX'] and\
                cur_row['ADX'] > cur_row['PosDI']:
                #and cur_row['NegDI'] > prev_row['NegDI'] \
            ninjaraObj.short_flags['FA_ADX'] = 1
        else:
            ninjaraObj.short_flags['FA_ADX'] = 0

        # MACD Flag Setting for shot
        if cur_row['MACD'] < cur_row['MACDsign']\
            and (cur_row['MACD'] + prev_row['MACD']) < (cur_row['MACDsign'] + prev_row['MACDsign']):
            # and cur_row['MACD'] < float(ninjaraObj.parser.get('macd', 'shot_range')) and \
            ninjaraObj.short_flags['FA_MACD'] = 1
        else:
            ninjaraObj.short_flags['FA_MACD'] = 0
        # print(cur_row.name,str(cur_row['open']),cur_row['high'],cur_row['low'],cur_row['close']
        #       ,cur_row['MA'],cur_row['EMA'],cur_row['MACD'],cur_row['ADX'],cur_row['RSI'])
        # print("*L",ninjaraObj.fast_min_long_flags)
        # print("*S",ninjaraObj.fast_min_shot_flags)

    except Exception as ex:
        error.handle(ex,traceback.format_exc())


def moving_average(n):
    try:
        MA = pd.Series(ninjaraObj.fast_min_pd_DF['close'].tail(n).rolling(n, min_periods=n).mean(), name='MA')
        if 'MA' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(MA.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(MA.tail(1).index, 'MA', MA.tail(1)[0])
    except Exception as ex:
        error.handle(ex, traceback.format_exc(), n)


def exponential_moving_average(n):
    try:
        EMA = pd.Series(ninjaraObj.fast_min_pd_DF['close'].tail(n).ewm(span=n, min_periods=n).mean(), name='EMA')
        if 'EMA' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(EMA.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(EMA.tail(1).index, 'EMA', EMA.tail(1)[0])
    except Exception as ex:
        error.handle(ex, traceback.format_exc(), n)


def macd(n_fast, n_slow):
    try:
        EMAfast = pd.Series(ninjaraObj.fast_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_fast, min_periods=n_slow).mean())
        EMAslow = pd.Series(ninjaraObj.fast_min_pd_DF['close'].tail(n_slow+10).ewm(span=n_slow, min_periods=n_slow).mean())
        MACD = pd.Series(EMAfast - EMAslow, name='MACD')
        MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name='MACDsign')
        MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff')
        if 'MACD' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(MACD.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(MACD.tail(1).index, 'MACD', MACD.tail(1)[0])

        if 'MACDsign' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(MACDsign.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(MACDsign.tail(1).index, 'MACDsign', MACDsign.tail(1)[0])

        if 'MACDdiff' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(MACDdiff.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(MACDdiff.tail(1).index, 'MACDdiff', MACDdiff.tail(1)[0])
    except Exception as ex:
        error.handle(ex, traceback.format_exc(),n_fast, n_slow)


def average_directional_movement_index(n, n_ADX):
    try:
        df = ninjaraObj.fast_min_pd_DF.tail(n+10)
        i = 0
        UpI = []
        DoI = []
        for row in df.iterrows():
            if (i != 0):
                UpMove = df.loc[df.index[i]]['high'] - df.loc[df.index[i - 1]]['high']
                DoMove = df.loc[df.index[i - 1]]['low'] - df.loc[df.index[i]]['low']
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
        for row in df.iterrows():
            if i != 0:
                TR = max(df.loc[df.index[i]]['high'], df.loc[df.index[i-1]]['close']) - min(
                    df.loc[df.index[i]]['low'], df.loc[df.index[i - 1]]['close'])
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

        if 'PosDI' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(PosDI.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(ninjaraObj.fast_min_pd_DF.tail(1).index, 'PosDI', math.ceil(PosDI.loc[PosDI.index[len(PosDI)-2]]*100))

        if 'NegDI' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(NegDI.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(ninjaraObj.fast_min_pd_DF.tail(1).index, 'NegDI', math.ceil(NegDI.loc[NegDI.index[len(NegDI)-2]]*100))

        if 'ADX' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(ADX.tail(1))
        else:
            try:
                ninjaraObj.fast_min_pd_DF._set_value(ninjaraObj.fast_min_pd_DF.tail(1).index, 'ADX', (math.ceil(ADX.tail(1).values[0]*100)))
            except:
                pass
    except Exception as ex:
        # print(traceback.format_exc())
        error.handle(ex,traceback.format_exc(), n , n_ADX)


def rsi(n):
    try:
        """Calculate Relative Strength Index(RSI) for given data.

            :param df: pandas.DataFrame
            :param n: 
            :return: pandas.DataFrame
            """
        df = ninjaraObj.fast_min_pd_DF.tail(n)
        i = 0
        UpI = [0]
        DoI = [0]
        for row in df.iterrows():
            if (i != 0):
        #while i + 1 <= df.index[-1]:
                UpMove = df.loc[df.index[i]]['high'] - df.loc[df.index[i - 1]]['high']
                DoMove = df.loc[df.index[i - 1]]['low'] - df.loc[df.index[i]]['low']
                #UpMove = df.loc[i + 1, 'High'] - df.loc[i, 'High']
                #DoMove = df.loc[i, 'Low'] - df.loc[i + 1, 'Low']
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
        if 'RSI' not in ninjaraObj.fast_min_pd_DF.columns:
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF.join(RSI.tail(1))
        else:
            ninjaraObj.fast_min_pd_DF._set_value(ninjaraObj.fast_min_pd_DF.tail(1).index, 'RSI', RSI.tail(1).values[0])
    except Exception as ex:
        error.handle(ex, traceback.format_exc(), n)
