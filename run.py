from telegram.ext import Updater, CommandHandler
import settings
import logging
from tasks import find_artist_info
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="test hello")




def search(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="start searching...")
    query = ' '.join(update.message.text.split()[1:])
    ct = find_artist_info.delay(query)
    bot.send_message(chat_id=update.message.chat_id, text=ct.get())


updater = Updater(settings.tg_token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))

updater.start_polling()