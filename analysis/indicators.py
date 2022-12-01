import pandas as pd
import pandas_ta as ta
from binance.client import Client

from apis.binance_api.custom_api import *


def calc_current_ema(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=34, data=None):
    try:
        if data is None:
            data = get_kline_prop(symbol, kline_interval)

        ret = ta.ema(data, length=length)
        return round(ret[len(ret) - 1], 2)
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def calc_1000_ema(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=34, data=None):
    try:
        if data is None:
            data = get_kline_prop(symbol, kline_interval)

        ret = ta.ema(data, length=length)
        return data, ret
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def calc_current_rsi(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, data=None):
    try:
        if data is None:
            data = get_kline_prop(symbol, kline_interval)
        ret = ta.rsi(data, length=length)
        return round(ret[len(ret) - 1], 2)
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def calc_1000_rsi(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, data=None):
    try:
        if data is None:
            data = get_kline_prop(symbol, kline_interval)
        ret = ta.rsi(data, length=length)
        return data, ret
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def calc_current_atr(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=14, mamode='rma', data=None):
    try:
        if data_frame is None:
            data_frame = get_kline_data(symbol, kline_interval)
        ret = ta.atr(pd.to_numeric(
            data_frame["high_price"], downcast="float"), pd.to_numeric(
            data_frame["low_price"], downcast="float"), pd.to_numeric(
            data_frame["close_price"], downcast="float"), length=length, mamode=mamode)
        return round(ret[len(ret) - 1], 2)
    except Exception as e:
        print(f"There's a error with {symbol}: {e}")


def get_long_medium_short_rsi(symbol, short_interval, medium_interval, long_interval):
    short_rsi = calc_current_rsi(symbol, short_interval)
    medium_rsi = calc_current_rsi(symbol, medium_interval)
    long_rsi = calc_current_rsi(symbol, long_interval)
    return short_rsi, medium_rsi, long_rsi
