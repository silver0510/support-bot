from binance.client import Client

from crypto.indicators import *
from crypto.trending import Trending
from crypto.util import *


def ma_trending_prime_ma_for_15_1_4(symbol):
    return __ma_trending_prime_ma(symbol, Trending.current_trend_15_1_4, Client.KLINE_INTERVAL_15MINUTE)


def ma_trending_prime_ma_for_1_4_1(symbol):
    return __ma_trending_prime_ma(symbol, Trending.current_trend_1_4_1, Client.KLINE_INTERVAL_1HOUR)


def __ma_trending_prime_ma(symbol, trend_consensus_func, short_trend_interval):
    trend_consensus = trend_consensus_func(symbol)
    ema, current_value, percent, trend = Trending.prime_ema_interval(
        symbol, short_trend_interval)
    rsi = calc_current_rsi(symbol, short_trend_interval)
    atr = calc_current_atr(symbol, short_trend_interval)
    return {
        "trend_consensus": trend_consensus,
        "prime_ema": {
            "ema": ema,
            "current_value": current_value,
            "percent": percent,
            "trend": trend
        },
        "rsi": rsi,
        "atr": atr
    }


def rsi_divergence(symbol, interval):
    detect_length = 34
    pivot_checking_period = 3
    divergence_threshold = 3
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
            if p_change > divergence_threshold and rsi_change > divergence_threshold:
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
            if p_change > divergence_threshold and rsi_change > divergence_threshold:
                divergences.append({
                    "price1": price1,
                    "price2": price2,
                    "rsi1": rsi1,
                    "rsi2": rsi2,
                    "location1": len(rsi_pivot_highs) - i - 1,
                    "location2": len(rsi_pivot_highs) - j - 1
                })

    return divergences
