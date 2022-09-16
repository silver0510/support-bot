import os
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler, filters, CallbackContext
from dotenv import load_dotenv
from database.utils import *

load_dotenv()
TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def percent_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # command exp: /percent_alert TSLA 5 america NASDAQ
    # context.args = ['TSLA', 'america, 'NASDAQ', '5']
    symbol, screener, exchange, percent = context.args
    chat_id = update.effective_chat.id
    # alert = register_percent_alert(
    #     chat_id, symbol, screener, exchange, percent)
    context.job
    await context.bot.send_message(chat_id=chat_id, text=f"Registed your alert for {alert.symbol} at {alert.percent}%")


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
