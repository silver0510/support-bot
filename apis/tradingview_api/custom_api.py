from tradingview_ta import TA_Handler, Interval, Exchange
from write_log import write_log


def validate_symbol_data(symbol, screener, exchange):
    symbol_info = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=Interval.INTERVAL_1_DAY,
    )
    try:
        symbol_info.get_analysis()
        return True
    except Exception as e:
        write_log(f"Validation symbol error: {e}")
        return False


def get_symbol_data(symbol, screener, exchange, interval=Interval.INTERVAL_1_DAY):
    return TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval
    ).get_analysis().indicators


def get_symbol_indicator(symbol, screener, exchange, prop="close", interval=Interval.INTERVAL_1_DAY):
    symbol_info = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=interval
    )
    return symbol_info.get_analysis().indicators[prop]
