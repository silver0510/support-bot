from os import path
import json

from dotenv import load_dotenv

from analysis.indicators import *
from analysis.util import *

load_dotenv()
RSI_DIVERGENCE_RANGE = os.getenv('RSI_DIVERGENCE_RANGE')
RSI_DIVERGENCE_PIVOT_CHECKING_PERIOD = os.getenv(
    'RSI_DIVERGENCE_PIVOT_CHECKING_PERIOD')


def rsi_divergence(symbol, interval):
    detect_length = int(RSI_DIVERGENCE_RANGE)
    pivot_checking_period = int(RSI_DIVERGENCE_PIVOT_CHECKING_PERIOD)
    divergence_percent_threshold = 3
    prices, rsis = calc_1000_rsi(symbol, interval)
    price_pivot_highs, price_pivot_lows = get_pivot_low_high(
        prices, pivot_checking_period)
    rsi_pivot_highs, rsi_pivot_lows = get_pivot_low_high(
        rsis, pivot_checking_period)
    divergences = []

    for i in range(len(rsi_pivot_highs) - detect_length, len(rsi_pivot_highs)):
        rsi1 = rsi_pivot_highs[i]
        price1 = price_pivot_highs[i]
        if rsi1 < 60 or price1 == 0:
            continue
        for j in range(i + 1, len(rsi_pivot_highs)):
            rsi2 = rsi_pivot_highs[j]
            price2 = price_pivot_highs[j]
            if rsi2 < 60 or price2 == 0:
                continue
            p_change = (price2 - price1) * 100 / price2
            rsi_change = (rsi1 - rsi2) * 100 / rsi1
            if p_change > divergence_percent_threshold and rsi_change > divergence_percent_threshold:
                divergences.append({
                    "price1": price1,
                    "price2": price2,
                    "rsi1": rsi1,
                    "rsi2": rsi2,
                    "location1": len(rsi_pivot_highs) - i - 1,
                    "location2": len(rsi_pivot_highs) - j - 1
                })
    for i in range(len(rsi_pivot_lows) - detect_length, len(rsi_pivot_lows)):
        rsi1 = rsi_pivot_lows[i]
        price1 = price_pivot_lows[i]
        if (rsi1 == 0 or rsi1 > 40) or (price1 == 0):
            continue
        for j in range(i + 1, len(rsi_pivot_lows)):
            rsi2 = rsi_pivot_lows[j]
            price2 = price_pivot_lows[j]
            if (rsi2 == 0 or rsi2 > 40) or (price2 == 0):
                continue
            p_change = (price1 - price2) * 100 / price1
            rsi_change = (rsi2 - rsi1) * 100 / rsi2
            if p_change > divergence_percent_threshold and rsi_change > divergence_percent_threshold:
                divergences.append({
                    "price1": price1,
                    "price2": price2,
                    "rsi1": rsi1,
                    "rsi2": rsi2,
                    "location1": len(rsi_pivot_highs) - i - 1,
                    "location2": len(rsi_pivot_highs) - j - 1
                })

    return divergences


def make_rsi_divergence_alert_msg(symbol, kline_interval):
    divergences = rsi_divergence(
        symbol, kline_interval)
    msgs = []
    for divergence in divergences:
        if divergence["location2"] < 6:
            suggestion = "LONG" if divergence["price2"] < divergence["price1"] else "SHORT"
            msgs.append(
                f"{symbol} {kline_interval.upper()} rsi divergence - {suggestion}:\n{json.dumps(divergence, indent=2)}")
    return msgs
