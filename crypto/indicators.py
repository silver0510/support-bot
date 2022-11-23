import pandas as pd
import pandas_ta as ta
from binance.client import Client

from crypto.constants import *
from crypto.model.kline import Kline


def calc_current_ema(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=34, data_frame=None):
    if data_frame is None:
        data_frame = pd.DataFrame(client.get_historical_klines(
            symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)

    ret = ta.ema(pd.to_numeric(
        data_frame["close_price"], downcast="float"), length=length)
    return round(ret[len(ret) - 1], 2)


def calc_1000_ema(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=34, data_frame=None):
    if data_frame is None:
        data_frame = pd.DataFrame(client.get_historical_klines(
            symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)
    ret = ta.ema(pd.to_numeric(
        data_frame["close_price"], downcast="float"), length=length)
    return pd.to_numeric(data_frame["close_price"]), ret


def calc_current_rsi(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, data_frame=None):
    if data_frame is None:
        data_frame = pd.DataFrame(client.get_historical_klines(
            symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)
    ret = ta.rsi(pd.to_numeric(
        data_frame["close_price"], downcast="float"), length=length)
    return round(ret[len(ret) - 1], 2)


def calc_1000_rsi(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, data_frame=None):
    try:
        if data_frame is None:
            data_frame = pd.DataFrame(client.get_historical_klines(
                symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)
        ret = ta.rsi(pd.to_numeric(
            data_frame["close_price"], downcast="float"), length=length)
        return pd.to_numeric(data_frame["close_price"]), ret
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def calc_current_atr(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, mamode='rma', data_frame=None):
    if data_frame is None:
        data_frame = pd.DataFrame(client.get_historical_klines(
            symbol, kline_interval, limit=1000), columns=KLINE_FORMAT)
    ret = ta.atr(pd.to_numeric(
        data_frame["high_price"], downcast="float"), pd.to_numeric(
        data_frame["low_price"], downcast="float"), pd.to_numeric(
        data_frame["close_price"], downcast="float"), length=length, mamode=mamode)
    return round(ret[len(ret) - 1], 2)


def current_price(symbol):
    return Kline(client.get_historical_klines(
        symbol, interval=Client.KLINE_INTERVAL_30MINUTE, limit=1)[0]).close_price


def get_long_medium_short_rsi(symbol, short_interval, medium_interval, long_interval):
    short_rsi = calc_current_rsi(symbol, short_interval)
    medium_rsi = calc_current_rsi(symbol, medium_interval)
    long_rsi = calc_current_rsi(symbol, long_interval)
    return short_rsi, medium_rsi, long_rsi
