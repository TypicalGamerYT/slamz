# Written by MaskedVirus | github.com/swatv3nub for William and SupMeta_bot
# Kang with Proper Credits
# Part of Pull Req #2 by @MaskedVirus | github.com/swatv3nub

import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from telegraph import upload_file

from bot import app
from bot.plugins.others.errors import capture_err


@app.on_message(filters.command("tgphoto"))
@capture_err
async def tgphoto(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a photo.")
        return
    if not message.reply_to_message.photo:
        await message.reply_text("Works only for Photos")
        return
    dwn = await message.reply_text("Downloading to my server...", True)
    userid = str(message.chat.id)
    path = f"./DOWNLOADS/{userid}.jpg"
    path = await client.download_media(message=message.reply_to_message, file_name=path)
    await dwn.edit_text("Uploading as telegra.ph link...")
    try:
        tlink = upload_file(path)
    except Exception as error:
        await dwn.edit_text(f"Oops something went wrong\n{error}")
        return
    await dwn.edit_text(text=f"<b>Link :-</b> <code>https://telegra.ph{tlink[0]}</code>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{tlink[0]}"), InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{tlink[0]}")]]))
    os.remove(path)


@app.on_message(filters.command("tgvideo"))
@capture_err
async def tgvideo(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a Video and Size Should Be Less Than 5 mb.")
        return
    if not message.reply_to_message.video:
        await message.reply_text("Works only for Videos")
        return
    if message.reply_to_message.video.file_size < 5242880:
        dwn = await message.reply_text("Downloading to my server...", True)
        userid = str(message.chat.id)
        vid_path = f"./DOWNLOADS/{userid}.mp4"
        vid_path = await client.download_media(message=message.reply_to_message, file_name=vid_path)
        await dwn.edit_text("Uploading as telegra.ph link...")
        try:
            tlink = upload_file(vid_path)
        except Exception as error:
            await dwn.edit_text(f"Oops something went wrong\n{error}")
            return
        await dwn.edit_text(text=f"<b>Link :-</b> <code>https://telegra.ph{tlink[0]}</code>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{tlink[0]}"), InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{tlink[0]}")]]))
        os.remove(vid_path)
