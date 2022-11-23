from tradingview_ta import TA_Handler, Interval, Exchange
from database.utils import *
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


def get_and_check_alert(id):
    '''
        Get data from database by id and check the price change
        return True if need to alert, False otherwise
    '''

    alert = get_alert_by_id(id)
    if alert:
        return check_alert(alert)


def check_alert(alert):
    price, change = check_symbol_change(
        alert.symbol, alert.screener, alert.exchange)
    if not change:
        return price, change, False
    else:
        if alert.percent < 0:
            '''
                Alert when change drop below the percent when
                the alert percent is negative.
            '''
            return price, change, change < alert.percent
        else:
            '''
                Alert when change increase above the percent when
                the alert percent is positive.
            '''
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
        write_log(
            f"Check price for {symbol} - {screener} - {exchange} error: {e}")
        if str(e) == "Exchange or symbol not found.":
            delete_percent_alerts_by_symbol_screener_exchange(
                symbol, screener, exchange)
            write_log(
                f"Delete all alerts of {symbol} - {screener} - {exchange}")

        return 0, 0


if __name__ == '__main__':
    print(validate_symbol_data('TSLA', 'america', 'NASDAQ'))
