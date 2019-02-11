from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import logging
from tasks import find_artist_info, send_message, download_voice, recognize_speech
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    send_message.delay(token=settings.tg_token, chat_id=update.message.chat_id, msg="test hello")


def search(bot, update):
    logging.debug("start searching...")
    query = ' '.join(update.message.text.split()[1:])
    ct = find_artist_info.s(query) | send_message.s(token=settings.tg_token, chat_id=update.message.chat_id)
    ct()


def voice_search(bot, update):
    logging.debug("start searching voice...")
    ct = download_voice.s(settings.tg_token, update.message.voice.file_id) | \
         recognize_speech.s() | \
         find_artist_info.s() | \
         send_message.s(token=settings.tg_token, chat_id=update.message.chat_id)
    ct()


updater = Updater(settings.tg_token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.voice, voice_search))
updater.start_polling()