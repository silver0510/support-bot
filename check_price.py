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


def get_and_check_alert(id):
    '''
        Get data from database by id and check the price change
        return True if need to alert, False otherwise
    '''

    alert = get_alert_by_id(id)
    if alert:
        price, change = check_symbol_change(
            alert.symbol, alert.screener, alert.exchange)
        if not change:
            return price, change, False
        else:
            return price, change, change > alert.percent


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
        return 0, 0


if __name__ == '__main__':
    print(validate_symbol_data('TSLA', 'america', 'NASDAQ'))
