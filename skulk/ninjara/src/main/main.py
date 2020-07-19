import datetime
import os
from datetime import timezone
import time
import pytz

# time.tzset()
# tz = pytz.timezone('Asia/Kolkata')

import os
import traceback
import argparse
import sys
# sys.path.append(os.getcwd()[:os.getcwd().find("TickAlgoAgent")+len("TickAlgoAgent")])
from kafka import KafkaConsumer
import pandas as pd
from skulk.ninjara.src.loghandler.log_handler import LogHandler
from base_utils.error_book.errorbook import ErrorBook
from skulk.ninjara.src.main.ninjara_objects import NinjaraObjects as ninjaraObj
from skulk.ninjara.src.pandaframe.prev_indicators import prevIndicators
from skulk.ninjara.src.indicators.indicators import Indicators
from base_utils.gcloud.gstorage import GStorage
from base_utils.common.common_fuctions import Functions
from json import loads
log = None
error = None
class ConsumerAgent(object):

    ohlc_consumer = None
    indicator_obj = None
    exit_algo = None
    exit_algo_315pm = None
    tick_df = None

    def __init__(self, args_topic, args_symbol, args_marketdate, args_kafkadetails="127.0.0.1:9092",
                 args_backtest=False, args_backttest_result = None):
        ninjaraObj.log = LogHandler.set_logger(args_topic)
        global log, error
        log = ninjaraObj.log
        error = ErrorBook(log)
        ninjaraObj.backtest = bool(args_backtest)
        ninjaraObj.backtest_result_sheet = args_backttest_result
        self.gstore = GStorage(log)
        self.comfunc = Functions(log)
        arg_prevdate = self.comfunc.getPrevTradeday(args_marketdate)
        ninjaraObj.topic = args_topic
        ninjaraObj.kafka = args_kafkadetails
        ninjaraObj.market_date = args_marketdate
        ninjaraObj.symbol = args_symbol
        ninjaraObj.prev_market_date = arg_prevdate
        if ninjaraObj.backtest is False:
            self.exit_algo = datetime.datetime.strptime(ninjaraObj.market_date + ' 09:45:00', '%Y%m%d %H:%M:%S')
            self.exit_algo_315pm = self.exit_algo.timestamp()
        else:
            self.exit_algo = datetime.datetime.strptime(ninjaraObj.market_date + ' 15:15:00', '%Y%m%d %H:%M:%S')
            self.exit_algo_315pm = self.exit_algo.timestamp()
        self.tick_df = pd.DataFrame(None, columns=['Timestamp', 'Price'])
        self.ohlc_consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                      auto_offset_reset='earliest',
                      enable_auto_commit=True,
                      value_deserializer=lambda x: loads(x.decode('utf-8')))

    def export_dataframe(self, message):
        try:
            if not os.path.exists(os.path.join("/tmp", ninjaraObj.market_date)):
                os.makedirs(os.path.join("/tmp", ninjaraObj.market_date))
            dfs_path = os.path.join("/tmp", ninjaraObj.market_date)
            ninjaraObj.fast_min_pd_DF.to_csv(os.path.join(dfs_path, ninjaraObj.symbol+"_fast_data_frames.csv"), header=True)
            ninjaraObj.slow_min_pd_DF.to_csv(os.path.join(dfs_path, ninjaraObj.symbol+"_slow_data_frames.csv"), header=True)
            self.tick_df.to_csv(os.path.join(dfs_path, ninjaraObj.symbol + "_ticks.csv"), header=True)
            sys.exit()
        except Exception as ex:
            error.handle(ex,traceback.format_exc(),message)
            sys.exit()

    def startlisten(self):
        indicator_obj = Indicators()
        ninjaraObj.log.info("Algo Agent Started Listening ticks for " + ninjaraObj.symbol + ", Topic Id:"+ninjaraObj.topic)
        print("In Liostening")
        self.ohlc_consumer.subscribe([str(ninjaraObj.topic)])
        try:
            for message in self.ohlc_consumer:
                # print(message.value)
                message = message.value
                if (message.get('Timestamp') is not None) and (message.get('Price') is not None):
                    self.tick_df.loc[len(self.tick_df)] = [message.get('Timestamp'), message.get('Price')]
                    if float(message.get('Timestamp')) < self.exit_algo_315pm:
                        indicator_obj.algo(message)
                    else:
                        self.export_dataframe(message)
        except Exception as ex:
            error.handle(ex,traceback.format_exc())

    def startLocalLoop(self, path):
        try:
            indicator_obj = Indicators()
            ninjaraObj.log.info(
                "Algo Agent Started Listening ticks for " + ninjaraObj.symbol + ", Topic Id:" + ninjaraObj.topic)
            print("In looping")
            loop_ohlc = pd.read_csv(path)
            for ind in loop_ohlc.index:
                message = {
                        "topicId": ninjaraObj.symbol,
                        "Price": float(loop_ohlc['price'][ind]),
                        "Timestamp": str(loop_ohlc['time'][ind])
                }
                if (message.get('Timestamp') is not None) and (message.get('Price') is not None):
                    self.tick_df.loc[len(self.tick_df)] = [message.get('Timestamp'), message.get('Price')]
                    if float(message.get('Timestamp')) < self.exit_algo_315pm:
                        indicator_obj.algo(message)
                    else:
                        self.export_dataframe(message)

        except Exception as ex:
            error.handle(ex,traceback.format_exc())

    def loadDFs_with_prev_data(self, date, symbol, contract_type="STK"):
        try:
            ninjaraObj.log.info("Trying to get previous day bar data from firebase")
            csv_path = self.comfunc.isHrhdPresent(date,symbol)
            # csv_path = fbobj.get_file_from_firebaseStorage(fbobj.get_blob_path(date,symbol,contract_type))
            ninjaraObj.log.info("CSV downloaded from firebase and saved in "+csv_path)
            data = pd.read_csv(csv_path)
            data['time'] = pd.to_datetime(data['time'], unit='s', utc=True)
            data = data.set_index('time')
            data = data.tz_convert(tz='Asia/Kolkata')
            ti = data.loc[:, ['price']]
            ninjaraObj.fast_min_pd_DF = ti.price.resample(str(ninjaraObj.fast_min) + 'min').ohlc()
            ninjaraObj.slow_min_pd_DF = ti.price.resample(str(ninjaraObj.slow_min) + 'min').ohlc()
            ninjaraObj.log.info("Panda dataframe resampled for fast and slow prev day data")
            pindi = prevIndicators()
            ninjaraObj.log.info("Generating indicators for data frames")
            pindi.generate_indicator_serious()
            ninjaraObj.log.info("All indicators gensrated sucessfull for previous day data")
            ninjaraObj.log.info("**Fast dataframe with indicators")
            ninjaraObj.fast_min_pd_DF = ninjaraObj.fast_min_pd_DF[:-1]
            ninjaraObj.log.info(ninjaraObj.fast_min_pd_DF)
            ninjaraObj.log.info("**Fast dataframe with indicators")
            ninjaraObj.slow_min_pd_DF = ninjaraObj.slow_min_pd_DF[:-1]
            ninjaraObj.log.info(ninjaraObj.slow_min_pd_DF)

        except Exception as ex:
            error.handle(ex, traceback.format_exc())


    def startAgentEngine(self):
        try:
            ninjaraObj.log.info("Algo Agent Preparing to Start")
            self.loadDFs_with_prev_data(ninjaraObj.prev_market_date, ninjaraObj.symbol, "STK")
            if ninjaraObj.backtest:
                pass
            else:
                self.startlisten()
        except Exception as ex:
            error.handle(ex, traceback.format_exc())


def cmd_param_handlers():
    try:
        # ninjaraObj.log.info("Tick Algo Agent - command param handlers")
        cmdLineParser = argparse.ArgumentParser("Tick Algo Agent :")
        cmdLineParser.add_argument("-k", "--kafka", action="store", type=str, dest="kafka",
                                   default="127.0.0.1:9092", help="Kafka server IP eg: 127.0.0.1:9092")
        cmdLineParser.add_argument("-t", "--topic", action="store", type=str, dest="topic",
                                   default="CIPLA", help="Kafka Producer Topic Name eg: 0")
        cmdLineParser.add_argument("-md", "--marketdate", action="store", type=str, dest="marketdate",
                                   default="20200424", help="Market Date eg: 20191025")
        # cmdLineParser.add_argument("-pd", "--prevdate", action="store", type=str, dest="prevdate",
        #                            default="20200423", help="Previous Market date eg: 20191025")
        cmdLineParser.add_argument("-s", "--symbol", action="store", type=str, dest="symbol",
                                   default="CIPLA", help="IB Symbol eg: INFY")
        cmdLineParser.add_argument("-bt", "--backtest", action="store", type=bool, dest="backtest",
                                   default=False, help="Back Test eg : True or False")

        args = cmdLineParser.parse_args()
        # ninjaraObj.backtest = bool(args.backtest)
        consObj = ConsumerAgent(args_topic=str(args.topic),
                                args_symbol=str(args.symbol),
                                args_marketdate=str(args.marketdate),
                                args_kafkadetails=str(args.kafka),
                                args_backtest=bool(args.backtest))
        consObj.startAgentEngine()


    except Exception as ex:
        error.handle(ex, traceback.format_exc())




if __name__ == '__main__':
    # ninjaraObj.log.info("** Algo Agent Initiated Succesfully")
    cmd_param_handlers()

    # # Below commands to execute individually
    # consobj = ConsumerAgent(
    #     args_topic=str("ADANIPORT"),
    #     args_kafkadetails=str("localhost:9092"),
    #     args_symbol=str("ADANIPORT"),
    #     args_marketdate=str("20200417"),
    #     arg_prevdate=str("20200416")
    # )
    # consobj.startAgentEngine()
