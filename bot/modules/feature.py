import random
import re

import requests

from bs4 import BeautifulSoup
from requests import get, post
from telegram import Chat, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, TelegramError, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.ext.dispatcher import run_async

from bot import dispatcher
from bot.modules.others.alternate import send_action, typing_action
from bot.helper.telegram_helper.filters import CustomFilters


@run_async
def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")


@run_async
def repo(update: Update, context: CallbackContext):
    context.args
    message = update.effective_message
    text = message.text[len("/repo ") :]
    usr = get(f"https://api.github.com/users/{text}/repos?per_page=40").json()
    reply_text = "*Repositorys*\n"
    for i in range(len(usr)):
        reply_text += f"[{usr[i]['name']}]({usr[i]['html_url']})\n"
    message.reply_text(
        reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


@run_async
@typing_action
def getlink(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    if args:
        pattern = re.compile(r"-\d+")
    else:
        message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = context.bot.getChat(chat_id)
            bot_member = chat.get_member(context.bot.id)
            if bot_member.can_invite_users:
                invitelink = context.bot.exportChatInviteLink(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += (
                    str(chat_id) + ":\nI don't have access to the invite link." + "\n"
                )
        except BadRequest as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"
        except TelegramError as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"

    message.reply_text(links)


@run_async
@typing_action
def app(update: Update, _):
    message = update.effective_message
    try:
        progress_message = update.effective_message.reply_text(
            "Searching In Play-Store.... "
        )
        app_name = message.text[len("/app ") :]
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            f"https://play.google.com/store/search?q={final_name}&c=apps"
        )
        soup = BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += "\n\n<i>Developer :</i> <a href='" + app_dev_link + "'>"
        app_details += app_dev + "</a>"
        app_details += "\n<i>Rating :</i> " + app_rating.replace(
            "Rated ", "⭐️ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐️"
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<i>Features :</i> <a href='" + app_link + "'>View in Play Store</a>"
        )
        message.reply_text(
            app_details, disable_web_page_preview=False, parse_mode="html"
        )
    except IndexError:
        message.reply_text("No Result Found In Search. Please Enter **Valid App Name**")
    except Exception as err:
        message.reply_text(err)
    progress_message.delete()


@run_async
@send_action(ChatAction.UPLOAD_PHOTO)
def rmemes(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat

    SUBREDS = [
        "meirl",
        "dankmemes",
        "AdviceAnimals",
        "memes",
        "meme",
        "memes_of_the_dank",
        "PornhubComments",
        "teenagers",
        "memesIRL",
        "insanepeoplefacebook",
        "terriblefacebookmemes",
    ]

    subreddit = random.choice(SUBREDS)
    res = requests.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")

    if res.status_code != 200:  # Like if api is down?
        msg.reply_text("Sorry some error occurred :(")
        return
    else:
        res = res.json()

    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))

    caps = f"- <b>Title</b>: {title}\n"
    caps += f"- <b>Subreddit:</b> <pre>r/{rpage}</pre>"

    keyb = [[InlineKeyboardButton(text="Subreddit Postlink 🔗", url=plink)]]
    try:
        context.bot.send_photo(
            chat.id,
            photo=memeu,
            caption=(caps),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
            parse_mode=ParseMode.HTML,
        )

    except BadRequest as excp:
        return msg.reply_text(f"Error! {excp.message}")


APP_HANDLER = CommandHandler("app", app, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
GIFID_HANDLER = CommandHandler("gifid", gifid, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
GETLINK_HANDLER = CommandHandler("getlink", getlink, pass_args=True, filters=CustomFilters.owner_filter)
REDDIT_MEMES_HANDLER = CommandHandler("rmeme", rmemes, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)


dispatcher.add_handler(APP_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(REDDIT_MEMES_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)