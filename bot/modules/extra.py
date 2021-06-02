# Simple dictionary module by @TheRealPhoenix  
import requests
import wikipedia
import json
import aiohttp
import random
import re

from pyrogram import filters # for github pyro, delete this with github pyro code

from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import get, post

from telegram import Chat, ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, TelegramError, Message, Update
from telegram.ext import CommandHandler, CallbackContext, run_async
from telegram.error import BadRequest
from wikipedia.exceptions import DisambiguationError, PageError

from bot.modules.others.alternate import send_action, typing_action
from bot.helper.telegram_helper.filters import CustomFilters

from bot import dispatcher, IMAGE_URL


@run_async
def ud(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text[len("/ud ") :]
    results = requests.get(
        f"https://api.urbandictionary.com/v0/define?term={text}"
    ).json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except:
        reply_text = "No results found."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

@run_async
def wiki(update: Update, context: CallbackContext):
    msg = update.effective_message.reply_to_message if update.effective_message.reply_to_message else update.effective_message
    res = ""
    if msg == update.effective_message:
        search = msg.text.split(" ", maxsplit=1)[1]
    else:
        search = msg.text
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        update.message.reply_text(
            "Disambiguated pages found! Adjust your query accordingly.\n<i>{}</i>"
            .format(e),
            parse_mode=ParseMode.HTML)
    except PageError as e:
        update.message.reply_text(
            "<code>{}</code>".format(e), parse_mode=ParseMode.HTML)
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Read more...</a>"""
        if len(result) > 4000:
            with open("result.txt", 'w') as f:
                f.write(f"{result}\n\nUwU OwO OmO UmU")
            with open("result.txt", 'rb') as f:
                context.bot.send_document(
                    document=f,
                    filename=f.name,
                    reply_to_message_id=update.message.message_id,
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(
                result,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True)

@run_async
def covid(update: Update, context: CallbackContext):
    message = update.effective_message
    device = message.text[len('/covid '):]
    fetch = get(f'https://coronavirus-tracker-api.herokuapp.com/all')

    if fetch.status_code == 200:
        usr = fetch.json()
        data = fetch.text
        parsed = json.loads(data)
        total_confirmed_global = parsed["latest"]["confirmed"]
        total_deaths_global = parsed["latest"]["deaths"]
        total_recovered_global = parsed["latest"]["recovered"]
        active_cases_covid19 = total_confirmed_global - total_deaths_global - total_recovered_global
        reply_text = ("*Corona Status 🦠 :*\n\n"
        "*Total Confirmed :* `" + str(total_confirmed_global) + "`\n\n"
        "*Total Deaths :* `" + str(total_deaths_global) + "`\n\n"
        "*Total Recovered :* `" + str(total_recovered_global) +"`\n\n"
        "*Active Cases :* `"+ str(active_cases_covid19) + "`")
        message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

        return

    elif fetch.status_code == 404:
        reply_text = "The API is currently down."
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

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


COVID_HANDLER = CommandHandler("covid", covid)
UD_HANDLER = CommandHandler("ud", ud)
WIKI_HANDLER = CommandHandler("wiki", wiki)
APP_HANDLER = CommandHandler("app", app, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
GIFID_HANDLER = CommandHandler("gifid", gifid, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
GETLINK_HANDLER = CommandHandler("getlink", getlink, pass_args=True, filters=CustomFilters.owner_filter)
REDDIT_MEMES_HANDLER = CommandHandler("rmeme", rmemes, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)


dispatcher.add_handler(APP_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(REDDIT_MEMES_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(UD_HANDLER)