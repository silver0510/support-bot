from playhouse.migrate import *
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')

db = SqliteDatabase(DB_NAME)
migrator = SqliteMigrator(db)

is_alert_today = BooleanField(null=False, default=False)

migrate(
    migrator.add_column('stockpercentalert', 'is_alert_today', is_alert_today)
)
