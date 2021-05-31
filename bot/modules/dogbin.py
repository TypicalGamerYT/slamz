import html
import json
import random

from typing import Optional, List

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity, ParseMode
from telegram.ext import CommandHandler, run_async, CallbackContext
from telegram.utils.helpers import escape_markdown

from bot import dispatcher

BASE_URL = 'https://del.dog'

@run_async
def dogbin(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?!")
        return

    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text('Failed to reach dogbin')
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL : {BASE_URL}/{key}\n\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'Shortened Dogbin [URL]({BASE_URL}/{key})'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

@run_async
def get_dogbin_content(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    if len(args) >= 1:
        key = args[0]
    else:
        message.reply_text("Please supply a paste key!")
        return

    format_normal = f'{BASE_URL}/'
    format_view = f'{BASE_URL}/v/'

    if key.startswith(format_view):
        key = key[len(format_view):]
    elif key.startswith(format_normal):
        key = key[len(format_normal):]

    r = requests.get(f'{BASE_URL}/raw/{key}')

    if r.status_code != 200:
        try:
            res = r.json()
            update.effective_message.reply_text(res['message'])
        except Exception:
            if r.status_code == 404:
                update.effective_message.reply_text('Failed to reach dogbin')
            else:
                update.effective_message.reply_text('Unknown error occured')
        r.raise_for_status()

    update.effective_message.reply_text('```' + escape_markdown(r.text) + '```', parse_mode=ParseMode.MARKDOWN)


#__help__ = """
# - /paste: Create a paste or a shortened url using [dogbin](https://del.dog)
# - /getpaste: Get the content of a paste or shortened url from [dogbin](https://del.dog)
# - /pastestats: Get stats of a paste or shortened url from [dogbin](https://del.dog)
#"""

#__mod_name__ = "DOG BIN"

PASTE_HANDLER = CommandHandler("dogbin", dogbin, pass_args=True)
GET_PASTE_HANDLER = CommandHandler("getdog", get_dogbin_content, pass_args=True)

dispatcher.add_handler(PASTE_HANDLER)
dispatcher.add_handler(GET_PASTE_HANDLER)