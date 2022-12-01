import pandas as pd
import pandas_ta as ta
from binance.client import Client

from apis.binance_api.configuration.constants import *
from apis.binance_api.model.kline import Kline


def current_price(symbol):
    return Kline(client.get_historical_klines(
        symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit=1)[0]).close_price


def last_close_price(symbol, kline_interval=Client.KLINE_INTERVAL_15MINUTE):
    return Kline(client.get_historical_klines(
        symbol, interval=kline_interval, limit=2)[0]).close_price


def get_kline_data(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=1000):
    return pd.DataFrame(client.get_historical_klines(
        symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)


def get_kline_prop(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, prop="close_price", length=1000, data_frame=None):
    if data_frame == None:
        data_frame = pd.DataFrame(client.get_historical_klines(
            symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)
    return pd.to_numeric(data_frame[prop], downcast="float")
