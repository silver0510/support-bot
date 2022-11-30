from binance.client import Client

from crypto.constants import *
from analysis.indicators import *


SHORT_LENGTH = 34
MEDIUM_LENGTH = 89
LONG_LENGTH = 200
UP_TREND = 'UP TREND'
SIDE_WAY = 'SIDE WAY'
DOWN_TREND = 'DOWN TREND'


def detect_trend_interval(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY):
    price = current_price(symbol)
    ema_short = calc_current_ema(
        symbol, kline_interval, SHORT_LENGTH)
    ema_medium = calc_current_ema(
        symbol, kline_interval, MEDIUM_LENGTH)
    # ema_long = calc_current_ema(
    #     symbol, kline_interval, LONG_LENGTH)

    if (price >= ema_short) and (price >= ema_medium):
        return UP_TREND
    if (price <= ema_short) and (price <= ema_medium):
        return DOWN_TREND

    return SIDE_WAY


'''
    Trending for 15min - 1h - 4h
'''


def current_trend_15_1_4(symbol='BTCBUSD'):
    return __trend_short_medium_long_consensus(symbol, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_4HOUR)


'''
    Trending for 1h - 4h - 1day
'''


def current_trend_1_4_1(symbol='BTCBUSD'):
    return __trend_short_medium_long_consensus(symbol, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_4HOUR, Client.KLINE_INTERVAL_1DAY)


def __trend_short_medium_long_consensus(symbol, short_interval, medium_interval, long_interval):
    short_trend = detect_trend_interval(
        symbol, short_interval)

    medium_trend = detect_trend_interval(
        symbol, medium_interval)
    long_trend = detect_trend_interval(
        symbol, long_interval)

    conclusion = SIDE_WAY
    if (short_trend == UP_TREND) and (medium_trend == UP_TREND) and (long_trend == UP_TREND):
        conclusion = UP_TREND

    if (short_trend == DOWN_TREND) and (medium_trend == DOWN_TREND) and (long_trend == DOWN_TREND):
        conclusion = DOWN_TREND

    return {
        "short_trend": short_trend,
        "medium_trend": medium_trend,
        "long_trend": long_trend,
        "conclusion": conclusion
    }


def prime_ema_interval(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY):
    ema_lengths = [20, 34, 55, 89, 200]
    for ema_length in ema_lengths:
        ema, current_value, is_important, percent, trend = __is_ema_important(
            symbol, kline_interval, ema_length)
        if is_important:
            return ema, current_value, percent, trend
    return None, None, None, None


def __is_ema_important(symbol='BTCBUSD', kline_interval=Client.KLINE_INTERVAL_1DAY, length=34):
    CHECKING_LENGTH = 60
    THRESHOLD = 0.8
    prices, emas = calc_1000_ema(symbol, kline_interval, length)
    current_value = round(emas[len(prices)-1], 2)
    above_ema = []
    below_ema = []
    for i in range(1, CHECKING_LENGTH + 1):
        if prices[len(prices)-i] >= emas[len(prices)-i]:
            above_ema.append((prices[len(prices)-i], emas[len(prices)-i]))
        else:
            below_ema.append((prices[len(prices)-i], emas[len(prices)-i]))
    percents_of_above_ema = round(len(above_ema)/CHECKING_LENGTH, 2)
    percents_of_below_ema = round(len(below_ema)/CHECKING_LENGTH, 2)
    if percents_of_above_ema > THRESHOLD:
        return length, current_value, True, percents_of_above_ema, "Above EMA"

    if percents_of_below_ema > THRESHOLD:
        return length, current_value, True, percents_of_below_ema, "Below EMA"

    return length, current_value, False, max(percents_of_above_ema, percents_of_below_ema), "Sideway"


def detect_long_short_by_rsi(symbol, short_interval, medium_interval, long_interval):
    short_rsi, medium_rsi, long_rsi = get_long_medium_short_rsi(
        symbol, short_interval, medium_interval, long_interval)
    if (short_rsi > 19 and medium_rsi > 39 and long_rsi > 60) or (short_rsi > 39 and medium_rsi > 59 and long_rsi > 79):
        return {
            "short_rsi": short_rsi,
            "medium_rsi": medium_rsi,
            "long_rsi": long_rsi,
            "conclusion": "LONG"
        }

    if (short_rsi < 61 and medium_rsi < 41 and long_rsi < 21) or (short_rsi < 81 and medium_rsi < 61 and long_rsi < 41):
        return {
            "short_rsi": short_rsi,
            "medium_rsi": medium_rsi,
            "long_rsi": long_rsi,
            "conclusion": "SHORT"
        }

    return {
        "short_rsi": short_rsi,
        "medium_rsi": medium_rsi,
        "long_rsi": long_rsi,
        "conclusion": "SIDE_WAY"
    }
