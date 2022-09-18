import os
import hashlib
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler, filters, CallbackContext
from dotenv import load_dotenv
from database.utils import *
from database.db import *

load_dotenv()
TOKEN = os.getenv('TOKEN')

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def percent_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
        command exp: /percent_alert TSLA america NASDAQ 5 
        context.args = ['TSLA', 'america, 'NASDAQ', '5'] 
    """
    symbol, screener, exchange, percent = context.args
    chat_id = update.effective_chat.id
    alert = register_percent_alert(
        chat_id, symbol, screener, exchange, percent)
    if not alert:
        await update.effective_message.reply_text("Sorry we can not register your command!")
        return
    alert_id = hash_alert_info(
        str(chat_id), symbol, screener, exchange, percent)
    job_removed = remove_job_if_exists(alert_id, context)
    context.job_queue.run_repeating(
        alert_callback, interval=300, first=5, chat_id=chat_id, name=alert_id, data=alert)
    await context.bot.send_message(chat_id=chat_id, text=f"Registed your alert for {symbol} at {percent}% successfully.")


async def alert_callback(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    alert = job.data
    print(alert.chat_id)
    # await context.bot.send_message(job.chat_id, text=f"Beep! {alert.chat_id}!")


def remove_job_if_exists(alert_id: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(alert_id)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def hash_alert_info(chat_id, symbol, screener, exchange, percent):
    return hashlib.md5((chat_id + symbol + screener + exchange + percent).encode()).hexdigest()


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    percent_alert_handler = CommandHandler('percent_alert', percent_alert)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(percent_alert_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
