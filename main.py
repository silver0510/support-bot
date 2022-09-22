from asyncio import sleep
import os
from os import path
import hashlib
import logging
import asyncio
from datetime import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, JobQueue
from dotenv import load_dotenv
from database.utils import *
from database.db import *
from check_price import *
from database.db import init_db
from database.utils import *
from write_log import write_activity_log

load_dotenv()
TOKEN = os.getenv('TOKEN')
DB_NAME = os.getenv('DB_NAME')
ALERT_INTERVAL = int(os.getenv('ALERT_INTERVAL'))
ADMINS_TELEGRAM_ID = []
for id in os.getenv('ADMINS_TELEGRAM_ID').split(','):
    ADMINS_TELEGRAM_ID.append(int(id.strip()))

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='1. Show your id: `/my_id\n2. Register a alert with format:\n `/register_alert symbol screener exchange percent`.\n\tExp: /register_alert ETHUSDT crypto BINANCE 5.\n\tYou can search on https://tvdb.brianthe.dev to see which symbol, exchange, and screener to use.\n3. Show alerts: `/show_alerts`\n4. Delete alert: `/delete_alert symbol screener exchange percent`')


async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)


async def percent_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
        command exp: /register_alert TSLA america NASDAQ 5 
        command exp: /register_alert ETHUSDT crypto BINANCE 1 
        context.args = ['TSLA', 'america, 'NASDAQ', '5'] 
    """
    chat_id = update.effective_chat.id
    if chat_id in ADMINS_TELEGRAM_ID:
        symbol, screener, exchange, percent = context.args
        alert = register_percent_alert(
            chat_id, symbol, screener, exchange, percent)
        if not alert:
            await update.effective_message.reply_text("Sorry we can not register your alert!")
            return
        job_removed = remove_job_if_exists(str(alert.id), context)
        context.job_queue.run_repeating(
            alert_callback, interval=60, first=5, chat_id=chat_id, name=str(alert.id), data=alert)
        msg = f"Registed your alert for {symbol} at {percent}% successfully."
        write_activity_log(msg)
        await context.bot.send_message(chat_id=chat_id, text=msg)
    else:
        await context.bot.send_message(chat_id=chat_id, text="You have no permission to use this feature. Please contact https://t.me/ryan_pham")


async def show_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    alerts = get_alert_by_chat_id(chat_id)
    if len(alerts):
        msg = 'List of alerts:'
        for index, alert in enumerate(alerts):
            msg += f"\n{str(index + 1)}. {alert.symbol} {alert.screener} {alert.exchange} {alert.percent}"
        await context.bot.send_message(chat_id=chat_id, text=msg)
    else:
        await context.bot.send_message(chat_id=chat_id, text="You do not have any alerts.")


async def delete_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Sorry we can not delete your alert!"
    chat_id = update.effective_chat.id
    symbol, screener, exchange, percent = context.args
    is_delete_successfuly, id = delete_percent_alert(
        chat_id, symbol, screener, exchange, percent)
    if not is_delete_successfuly:
        await update.effective_message.reply_text(msg)
        return
    else:
        if not id:
            msg = f"Delete your alert for {symbol} at {percent}% successfully."
        else:
            job_removed = remove_job_if_exists(str(id), context)
            if job_removed:
                msg = f"Delete your alert for {symbol} at {percent}% successfully."
                write_activity_log(msg)
        await context.bot.send_message(chat_id=chat_id, text=msg)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def alert_callback(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    alert = job.data
    price, change, should_alert = get_and_check_alert(alert.id)

    if should_alert:
        await context.bot.send_message(job.chat_id, text=f"{alert.symbol} has changed {round(change, 2)}%. Current price: {price}")
        job.enabled = False


async def enable_all_jobs_at_start_day_callback(context: ContextTypes.DEFAULT_TYPE):
    current_jobs = context.job_queue.jobs()
    if not current_jobs:
        return
    for job in current_jobs:
        job.enabled = True

    write_activity_log("Reset all jobs for the new day")


def remove_job_if_exists(alert_id: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    try:
        current_jobs = context.job_queue.get_jobs_by_name(alert_id)
        if not current_jobs:
            return True
        for job in current_jobs:
            job.schedule_removal()
        return True
    except Exception as e:
        write_log("Remove job error: {e}")
        return False


def load_all_alerts_and_create_job(job_queue: JobQueue):
    alerts = get_all_alerts()
    if len(alerts):
        for alert in alerts:
            job_queue.run_repeating(
                alert_callback, interval=ALERT_INTERVAL, first=5, chat_id=alert.chat_id, name=str(alert.id), data=alert)
            msg = f"Registed your alert for {alert.symbol} at {alert.percent}% successfully."
            write_activity_log(msg)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    if not path.exists(DB_NAME):
        init_db()
    else:
        load_all_alerts_and_create_job(application.job_queue)

    start_handler = CommandHandler('start', start)
    myid_handler = CommandHandler('my_id', my_id)
    percent_alert_handler = CommandHandler('register_alert', percent_alert)
    show_alerts_handler = CommandHandler('show_alerts', show_alerts)
    delete_alert_handler = CommandHandler('delete_alert', delete_alert)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(myid_handler)
    application.add_handler(percent_alert_handler)
    application.add_handler(show_alerts_handler)
    application.add_handler(delete_alert_handler)
    application.add_handler(unknown_handler)

    # add job queue handler
    job_queue = application.job_queue
    job_queue.run_daily(enable_all_jobs_at_start_day_callback,
                        time(0, 0, 0))
    application.run_polling()
