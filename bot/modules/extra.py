# Simple dictionary module by @TheRealPhoenix  
import requests
import wikipedia
import json
import aiohttp

from pyrogram import filters # for github pyro, delete this with github pyro code

from urllib.request import urlopen
from requests import get
from telegram import Message, Update, ParseMode, Chat
from telegram.ext import CommandHandler, CallbackContext, run_async
from wikipedia.exceptions import DisambiguationError, PageError
from bot import dispatcher, IMAGE_URL

from bot import app # for github pyro, delete this with github pyro code
from bot.modules.others.errors import capture_err # for github pyro, delete this with github pyro code

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


@app.on_message(filters.command('github'))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/github Username")
        return
    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()
            try:
                url = result['html_url']
                ids = result['id']
                tipe = result['type']
                followers_url = result['followers_url']
                following_url = result['following_url']
                updated_at = result['updated_at']
                email = result['email']
                name = result['name']
                company = result['company']
                bio = result['bio']
                hireable = result['hireable']
                public_gists = result['public_gists']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']
                caption = f"""**Info Of {name}**

**Username :** `{username}`
**Account ID :** `{ids}`
**Account type :** `{tipe}`

**Bio :** `{bio}`
**Profile Link :** [Here]({url})
**Company :** `{company}`

**Hireable :** `{hireable}`
**Blog :** `{blog}`
**Location :** `{location}`
**Email :** `{email}`
**Created On :** `{created_at}`

**Public Repos :** `{repositories}`
**Public Gists :** `{public_gists}`

**[Followers]({followers_url}) :** `{followers}`
**[Following]({following_url}) :** `{following}`

**Last updated :** `{updated_at}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=avatar_url, caption=caption)

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



COVID_HANDLER = CommandHandler("covid", covid)
UD_HANDLER = CommandHandler("ud", ud)
WIKI_HANDLER = CommandHandler("wiki", wiki)

dispatcher.add_handler(COVID_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(UD_HANDLER)