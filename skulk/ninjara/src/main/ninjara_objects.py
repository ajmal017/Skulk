import os
from configparser import ConfigParser

import sys
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])
import pandas as pd


class NinjaraObjects:
    # General config to set config file
    parser = ConfigParser()
    os.environ['NINJARA_CONFIG'] = os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")]+'/config/ninjara/config.ini'
    parser.read(os.getenv("NINJARA_CONFIG"))
    log = None
    # All this below variable got assigned by main method through cmd line arguments
    topic = ""
    kafka = ""
    symbol = ""
    market_date = ""
    prev_market_date = ""
    backtest = None
    order_sheet = None
    # all below used in fast min data frame
    start_sapm = True
    fast_min_ticks = []
    fast_min = int(parser.get('dataframes', 'fast_df'))
    cur_fast_min = 0
    fast_min_pd_DF = pd.DataFrame([])

    # all below used in slow min data frame
    slow_min_ticks = []
    slow_min = int(parser.get('dataframes', 'slow_df'))
    cur_slow_min = 0
    slow_min_pd_DF = pd.DataFrame([])
    # end

    # General flags
    long_flags = {'FA_SAPM': 0, 'FA_MAEMA': 0, 'FA_ADX': 0, 'FA_MACD': 0, 'FA_RSI': 0,
                  'SL_SAPM': 0, 'SL_MAEMA': 0, 'SL_ADX': 0, 'SL_MACD': 0, 'SL_RSI': 0}

    short_flags = {'FA_SAPM': 0, 'FA_MAEMA': 0, 'FA_ADX': 0, 'FA_MACD': 0, 'FA_RSI': 0,
                   'SL_SAPM': 0, 'SL_MAEMA': 0, 'SL_ADX': 0, 'SL_MACD': 0, 'SL_RSI': 0}


    @staticmethod
    def get_with_base_path(head, key):
        return os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent/")] + NinjaraObjects.parser.get(head, key)

    @staticmethod
    def get_value(head, key):
        return NinjaraObjects.parser.get(head, key)

    @staticmethod
    def update_config_values(section, key, value):
        NinjaraObjects.parser.set(section, key, value)