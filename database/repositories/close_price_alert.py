from database.db import ClosePricetAlert
from write_log import write_log

ABOVE = "above"
BELOW = "below"


def register_alert(chat_id, symbol, kline, price, trend):
    try:
        alert = get_alert_by_all_information(
            str(chat_id), symbol, kline, price, trend)
        if not alert:
            alert = ClosePricetAlert.create(chat_id=chat_id, symbol=symbol, kline=kline, price=float(
                price), trend=trend)
        return alert
    except Exception as e:
        write_log(
            f"Register alert for {symbol} - {kline} - {price} - {trend} error: {e}")
        return None


def delete_alert(id):
    try:
        alert = get_alert_by_id(id)
        if not alert:
            return True, None
        alert.delete_instance()
        return True, id
    except Exception as e:
        write_log(
            f"Delete alert by id error: {e}")
        return False, None


def delete_price_alerts_by_id(symbol):
    try:
        alerts = get_alert_by_symbol(symbol)
        if len(alerts) == 0:
            return True
        else:
            for alert in alerts:
                alert.delete_instance()
            return True
    except Exception as e:
        write_log(
            f"Delete alert for {symbol} error: {e}")
        return False, None


def get_alert_by_id(id):
    try:
        alert = ClosePricetAlert.get(ClosePricetAlert.id == id)
        return alert
    except Exception as e:
        return None


def get_alert_by_symbol(symbol):
    try:
        alerts = ClosePricetAlert.select().where(ClosePricetAlert.symbol == symbol)
        return alerts
    except Exception as e:
        return None


def get_alert_by_all_information(chat_id, symbol, kline, price, trend):
    try:
        alert = ClosePricetAlert.get(ClosePricetAlert.chat_id == chat_id, ClosePricetAlert.symbol == symbol,
                                     ClosePricetAlert.kline == kline, ClosePricetAlert.price == price, ClosePricetAlert.trend == trend)
        return alert
    except Exception as e:
        return None


def get_all_alerts():
    try:
        alerts = ClosePricetAlert.select()
        return alerts
    except Exception as e:
        print(e)
        return []


def get_alert_by_chat_id(chat_id):
    try:
        alerts = ClosePricetAlert.select().where(ClosePricetAlert.chat_id == chat_id)
        return alerts
    except Exception as e:
        return []


def get_alert_by_id(id):
    try:
        alert = ClosePricetAlert.get_by_id(id)
        return alert
    except Exception as e:
        return None


# if __name__ == '__main__':
    #     register_percent_alert('123456789', 'TSLA', 'america', 'NASDAQ', '5')
    #     for i in get_all_alerts():
    #         print(i.symbol)
    #     print(get_alert_by_all_information(
    #         '123456789', 'TSLA', 'america', 'NASDAQ', '5').symbol)
    # for alert in get_alerts_by_symbol_screener_exchange(
    #         'FTTUSDT', 'crypto', 'BINANCE'):
    #     print(alert.symbol)
    #     alert.delete_instance()

    # print(len(get_alerts_by_symbol_screener_exchange(
    #     'FTTUSDT', 'crypto', 'BINANCE')))
