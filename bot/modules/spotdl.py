import logging
import os
import subprocess
import uuid
from typing import List

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, run_async

from bot import dispatcher
from bot.helper.telegram_helper.filters import CustomFilters

def downspotify(download_path: str, link: List[str]):
    os.mkdir(download_path)
    os.chdir(download_path)
    os.system(f'spotifydl {link} -o download_path')
    os.chdir("..")


def sendspotify(download_path: str, update: Update, context: CallbackContext):
    directory = os.listdir(download_path)
    for file in directory:
        if not file.endswith(".mp3"):
            continue
        result = context.bot.send_audio(
            caption=("แ๐ซ0แน๐ฅ @Jusidama"),
            chat_id=update.effective_chat.id,
            audio=open(f'{download_path}/{file}', 'rb')
        )

    subprocess.run(['rm', '-r', download_path])

@run_async
def botify(update: Update, context: CallbackContext):
    song_link = context.args
    download_path = os.getcwd() + "/" + str(uuid.uuid4())

    context.bot.sendChatAction(chat_id =update.effective_chat.id,  action = "typing")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"๐ฅ๐๐จ๐ฐ๐ง๐ฅ๐จ๐๐๐ข๐ง๐ ๐ค")
    

    context.bot.sendChatAction(chat_id =update.effective_chat.id,  action = "record_video")
    spotifydl.downspotify(download_path, song_link)
    
    context.bot.sendChatAction(chat_id =update.effective_chat.id,  action = "record_audio")
    sendspotify(download_path, update, context)



SPOTDL_HANDLER = CommandHandler('spotdl', botify, pass_args=True, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)

dispatcher.add_handler(SPOTDL_HANDLER)
