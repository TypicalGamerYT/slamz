import aiohttp
import requests
import requests

from pyrogram import filters # for github pyro, delete this with github pyro code

from bot import app, AUTHORIZED_CHATS # for github pyro, delete this with github pyro code
from bot.plugins.others.errors import capture_err # for github pyro, delete this with github pyro code


@app.on_message(filters.command(['github', 'git'])  & filters.chat(AUTHORIZED_CHATS))
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