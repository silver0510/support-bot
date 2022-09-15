from lib2to3.pgen2 import grammar
from peewee import *
from datetime import date
import click

db = SqliteDatabase('support-bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class StockPercentAlert(BaseModel):
    name = CharField()
    screener = CharField()
    exchange = CharField()
    percent = FloatField()


@click.command()
def init_db():
    list_tables = [StockPercentAlert]
    db.connect()
    db.drop_tables(list_tables)
    db.create_tables(list_tables)
    db.close()

    click.echo('Initialized the database.')


if __name__ == '__main__':
    init_db()
