from db import *


def register_percent_alert(chat_id, symbol, screener, exchange, percent):
    try:
        alert = get_alert_by_all_information(
            chat_id, symbol, screener, exchange, percent)
        if not alert:
            alert = StockPercentAlert.create(chat_id=chat_id, symbol=symbol, percent=float(
                percent), screener=screener, exchange=exchange)
        return alert
    except Exception as e:
        print('Register alert error:', str(e))
        return None


def get_alert_by_all_information(chat_id, symbol, screener, exchange, percent):
    try:
        alert = StockPercentAlert.get(StockPercentAlert.chat_id == chat_id, StockPercentAlert.symbol == symbol, StockPercentAlert.percent == float(
            percent), StockPercentAlert.screener == screener, StockPercentAlert.exchange == exchange)
        return alert
    except Exception as e:
        print('Get alert by all information error:', str(e))
        return None


def get_alert_by_chat_id(chat_id):
    try:
        alerts = StockPercentAlert.select().where(StockPercentAlert.chat_id == chat_id)
        return alerts
    except Exception as e:
        print('Get alert by chat id error:', str(e))
        return []


if __name__ == '__main__':
    print(register_percent_alert('123456789', 'TSLA', 'america', 'NASDAQ', '5'))
    # print(get_alert_by_all_information(
    #     '123456789', 'TSLA', 'america', 'NASDAQ', '5').symbol)
