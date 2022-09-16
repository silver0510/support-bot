from tradingview_ta import TA_Handler, Interval, Exchange
from database.utils import *


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
        print(str(e))
        return False


def get_and_check_alert(chat_id):
    alerts = get_alert_by_chat_id(chat_id)


def check_symbol_change(symbol, screener, exchange):
    symbol_info = TA_Handler(
        symbol=symbol,
        screener=screener,
        exchange=exchange,
        interval=Interval.INTERVAL_1_DAY,
    )
    try:
        return symbol_info.get_analysis().indicators['close'], symbol_info.get_analysis().indicators['change']
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    print(validate_symbol_data('TSLA', 'america', 'NASDAQ'))
