from peewee import *
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')

db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class StockPercentAlert(BaseModel):
    chat_id = CharField()
    symbol = CharField()
    screener = CharField()
    exchange = CharField()
    percent = FloatField()
    is_alert_today = BooleanField(default=False)


class ClosePricetAlert(BaseModel):
    chat_id = CharField()
    symbol = CharField()
    kline = CharField()
    price = FloatField()
    trend = CharField()


def init_db():
    list_tables = [StockPercentAlert, ClosePricetAlert]
    db.connect()
    db.drop_tables(list_tables)
    db.create_tables(list_tables)
    db.close()

    print('Initialized the database.')


if __name__ == '__main__':
    init_db()
