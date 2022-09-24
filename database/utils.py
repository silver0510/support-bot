from database.db import StockPercentAlert
from write_log import write_log


def register_percent_alert(chat_id, symbol, screener, exchange, percent):
    try:
        alert = get_alert_by_all_information(
            str(chat_id), symbol, screener, exchange, percent)
        if not alert:
            alert = StockPercentAlert.create(chat_id=chat_id, symbol=symbol, percent=float(
                percent), screener=screener, exchange=exchange)
        return alert
    except Exception as e:
        write_log(f"Register alert error: {e}")
        return None


def delete_percent_alert(chat_id, symbol, screener, exchange, percent):
    try:
        alert = get_alert_by_all_information(
            str(chat_id), symbol, screener, exchange, percent)
        if not alert:
            return True, None
        else:
            id = alert.id
            alert.delete_instance()
            return True, id
    except Exception as e:
        write_log(f"Delete alert error: {e}")
        return False, None


def get_alert_by_all_information(chat_id, symbol, screener, exchange, percent):
    try:
        alert = StockPercentAlert.get(StockPercentAlert.chat_id == chat_id, StockPercentAlert.symbol == symbol, StockPercentAlert.percent == float(
            percent), StockPercentAlert.screener == screener, StockPercentAlert.exchange == exchange)
        return alert
    except Exception as e:
        return None


def get_all_alerts():
    try:
        alerts = StockPercentAlert.select()
        return alerts
    except Exception as e:
        print(e)
        return []


def get_alert_by_chat_id(chat_id):
    try:
        alerts = StockPercentAlert.select().where(StockPercentAlert.chat_id == chat_id)
        return alerts
    except Exception as e:
        return []


def get_today_alerts():
    try:
        alerts = StockPercentAlert.select().where(
            StockPercentAlert.is_alert_today == False)
        return alerts
    except Exception as e:
        return []


def get_alert_by_id(id):
    try:
        alert = StockPercentAlert.get_by_id(id)
        return alert
    except Exception as e:
        return None


def reset_all_today_alerts():
    try:
        alerts = get_all_alerts()
        if alerts:
            for alert in alerts:
                alert.is_alert_today = False
                alert.save()
        return True
    except Exception as e:
        print(e)
        return False

# if __name__ == '__main__':
#     register_percent_alert('123456789', 'TSLA', 'america', 'NASDAQ', '5')
#     for i in get_all_alerts():
#         print(i.symbol)
#     print(get_alert_by_all_information(
#         '123456789', 'TSLA', 'america', 'NASDAQ', '5').symbol)
