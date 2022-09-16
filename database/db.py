from peewee import *

db = SqliteDatabase('support-bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class StockPercentAlert(BaseModel):
    chat_id = CharField()
    symbol = CharField()
    screener = CharField()
    exchange = CharField()
    percent = FloatField()


def init_db():
    list_tables = [StockPercentAlert]
    db.connect()
    db.drop_tables(list_tables)
    db.create_tables(list_tables)
    db.close()

    print('Initialized the database.')


if __name__ == '__main__':
    init_db()
