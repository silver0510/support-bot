from analysis.trending import *


def ma_trending_prime_ma_for_15_1_4(symbol):
    return __ma_trending_prime_ma(symbol, current_trend_15_1_4, Client.KLINE_INTERVAL_15MINUTE)


def ma_trending_prime_ma_for_1_4_1(symbol):
    return __ma_trending_prime_ma(symbol, current_trend_1_4_1, Client.KLINE_INTERVAL_1HOUR)


def __ma_trending_prime_ma(symbol, trend_consensus_func, short_trend_interval):
    trend_consensus = trend_consensus_func(symbol)
    ema, current_value, percent, trend = prime_ema_interval(
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
