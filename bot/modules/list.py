from telegram.ext import CommandHandler, run_async
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.drive_utils.recursive import  GoogleDriveHelper as Recursive
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
import threading
from bot.helper.telegram_helper.bot_commands import BotCommands

@run_async
def list_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        if "'"in search:
            search = search.replace("'", "\\'")
        LOGGER.info(f"Searching: {search}")
        reply = sendMessage('Searching..... Please wait!', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
        else:
            editMessage('No result found', reply, button)

    except IndexError:
        sendMessage('Send a search key along with command', context.bot, update)


@run_async
def search_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
    except IndexError:
        sendMessage('Send a search key along with command', context.bot, update)
        return
        
    reply = sendMessage('Searching...', context.bot, update)

    LOGGER.info(f"Searching: {search}")
        
    gdrive = Recursive(None)
    msg, button = gdrive.drive_list(search)

    editMessage(msg,reply,button)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
search_handler = CommandHandler("list", search_drive, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)

dispatcher.add_handler(search_handler)
dispatcher.add_handler(list_handler)
