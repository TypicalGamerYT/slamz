import html
import requests

from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *

from bot import app
from bot import dispatcher, updater, IMAGE_URL

from bot import BLOCK_MEGA_LINKS, TORRENT_DIRECT_LIMIT, CLONE_LIMIT
from bot.modules import ALL_MODULES
from bot.plugins import ALL_PLUGINS

from telegram import Bot, Message, Update, ParseMode, Chat, InlineKeyboardMarkup
from bot.helper.telegram_helper import button_build
from telegram.ext import CommandHandler, run_async

@run_async
def configinfo(update, context):
    configinfo_string = f'''
╭────「 *BOT CONFIG* 」───────╮
│ 
├ • *🛑 Mega Block Link is :* `{BLOCK_MEGA_LINKS}`
│ 
├ • *🔒 Max Clone Size Limit is :* `{CLONE_LIMIT}`
│ 
├ • *🌀 Then Torrent Size Limit :* `{TORRENT_DIRECT_LIMIT}`
│
╰────「 *BOT CONFIG* 」───────╯

╭────「 *MODULE LIST* 」───────╮

`{ALL_MODULES}`

╭────「 *PLUGIN LIST* 」───────╮

`{ALL_PLUGINS}`
'''
    update.effective_message.reply_text(configinfo_string, parse_mode=ParseMode.MARKDOWN)


@run_async
def bot_help(update, context):
    help_string = f'''
╭────「 *BOT COMMAND LIST* 」───────╮
│ 
├ • `/{BotCommands.HelpCommand}` *: To get this message.*
│
├── *Along with [Download_Url] or [Magnet_Link]* ──╮
│
├ • `/{BotCommands.MirrorCommand}` *: Start mirroring*
│   *the link to google drive.*
│ 
├ • `/{BotCommands.UnzipMirrorCommand}` *: Starts mirroring*
│   *and if downloaded file is any archive, extracts it to google drive.*
│ 
├ • `/{BotCommands.TarMirrorCommand}` *: Start mirroring*
│   *and upload the archived (.tar) version of the download.*
│
├── *Along with [Download_Url] or [Magnet_Link]* ──╯
│ 
├ • `/{BotCommands.CloneCommand}` *: Copy file/folder to google drive.*
│
├ • `/{BotCommands.CountCommand}` *:  files/folders of G-Drive Links*
│
├── *Along with [Youtube-DL Supported Link]* ──╮
│
├ • `/{BotCommands.WatchCommand}` *: Mirror through YT-DL Click /ytdl for help.*
│ 
├ • `/{BotCommands.TarWatchCommand}` *: Mirror through  YT-DL then upload it .tar*
│
├── *Along with [Youtube-DL Supported Link]* ──╯
│
├ • `/{BotCommands.CancelMirror}` *: Reply to the message by which the download *
│   *was initiated and that download will be cancelled.*
│ 
├ • `/{BotCommands.StatusCommand}` *: Shows a status of all the downloads.*
│ 
├ • `/{BotCommands.ListCommand}` *[search term] : Searches the search term.*
│   *in the Google drive, if found replies with the link.*
│ 
├ • `/{BotCommands.StatsCommand}` *: Show Stats of the Bot machine is hosted on.*
│ 
├ • `/index` *: To get this group Index Drives link, user and pass.*
│ 
├ • `/drive` *: To get this group Shared Drives link.*
│ 
├ • `/admin` *: Command list for Owner & Sudo User only.*
│ 
├ • `/next` *: Show next command list available in this bot.*
│
╰────「 *BOT COMMAND LIST* 」───────╯
'''
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Custom Name", "https://telegra.ph/Magneto-Python-Aria---Custom-Filename-Examples-01-20")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    update.effective_message.reply_text(help_string, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

@run_async
def nexthelp(update, context):
    nexthelp_string = f'''
╭────「 *OTHERS COMMAND LIST* 」───────╮
│ 
├ • `/{BotCommands.RepoCommand}` *: Get the group info.*
│ 
├ • `/{BotCommands.SpeedCommand}` *: Check Internet Speed of the Host.*
│
├ • `/{BotCommands.TotranslateCommand}` *: Translating message with listed code.*
│
├ • `/{BotCommands.PasteCommand}` *: Paste a word to neko.bin from message.*
│
├ • `/{BotCommands.SearchHelpCommand}` *: Get help for torrent search module.*
│
├ • `/{BotCommands.WeebHelpCommand}` *: Get help for anime and manga module.*
│
├ • `/{BotCommands.StickerHelpCommand}` *: Get help for stickers module.*
│
├ • `/ud` *<word> : Searches Urban Dictionary For The Query.*
│
├ • `/wiki` *<word> : Returns some article from Wikipedia.*
│
├ • `/mediainfo` *: Get detailed info about replied media.*
│
├ • `/mathhelp` *: Get help for math stuff module.*
│
├ • `/dicthelp` *: Get help for dictionary stuff module.*
│
├ • `/lewdhelp` *: Get help for lewd stuff module.*
│
├ • `/extra` *: Get help for more command module.*
│
╰────「 *OTHERS COMMAND LIST* 」───────╯
'''
    update.effective_message.reply_text(nexthelp_string, parse_mode=ParseMode.MARKDOWN)

@run_async
def shellhelp(update, context):
    shellhelp_string = f'''
╭────「 *SHELL COMMAND LIST* 」───────╮
│
├ • `/term` *: Run a shell or terminal command with :*
│   *(*'`sh`', '`shell`', '`term`', '`terminal`'*), use slash (`/`) before command like* `/sh`*.*
│
├ • `/eval` *: Eval a python code line with : *
│   *(*'`e`', '`ev`', '`eva`', '`eval`'*), use slash (`/`) before command like* `/e`*.*
│
├ • `/exec` *: Execute a python command with : *
│   *(*'`x`', '`ex`', '`exe`', '`exec`', '`py`'*), use slash (`/`) before command like* `/x`*.*
│
├ • `/clearlocals` *: Clear local, idk what this command. U can try ur self.*
│
╰────「 *ONLY OWNER & SUDO* 」───────╯
'''
    update.effective_message.reply_text(shellhelp_string, parse_mode=ParseMode.MARKDOWN)

@run_async
def index(update, context):
    index_string = f'''
<b>Hello {update.message.chat.first_name},</b>
<b>We Had 4 Index, Open Link in Button Below</b>

🚧 <b>For Multi-Index You Need To Register Your Account</b>
🚧 <b>And Follow Tutorial In <i>Register Button</i></b>

╭─ <b>Security Login Here 🚧</b>
├ Username : <code>index</code>
├ Password : <code>dbs</code>
╰─ <b>For Database-Index 🚧</b>

╭─ <b>Security Login Here 🚧</b>
├ Username : <code>md</code>
├ Password : <code>555</code>
╰─ <b>For MainData-Index </b>

╭─ <b>Security Login Here 🚧</b>
├ Username : <code>movie</code>
├ Password : <code>play</code>
╰─ <b>For Movie-Index</b>

<b>⚡️ Multi-Index ⚡️</b>
<b>⚡️ DB-Index ⚡️</b>
<b>⚡️ Movie-Index ⚡️</b>
<b>⚡️ MD5-Index ⚡️</b>

<b>Don't Misuse The Index Link </b>
<b>Else I Will Remove Support For It 👍</b>
'''
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Multi-Index 🚧", "https://index.juicedama.workers.dev")
    buttons.buildbutton("DB-Index 🚧", "https://is.gd/john_db")
    buttons.buildbutton("Movie-Index 🚧", "http://bit.ly/jusimovie")
    buttons.buildbutton("MD5-Index 🚧", "https://md5.juicedama.workers.dev")
    buttons.buildbutton("💢 Register 💢", "https://telegra.ph/How-To-Regiter-In-Jusidama-Multi-Index-05-20")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    update.effective_message.reply_photo(IMAGE_URL, index_string, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

@run_async
def drives(update, context):
    drives_string = f'''
<b>Hello {update.message.chat.first_name},</b>
<b>Hi there fellow members, here group drive :</b>

<b>We Had 3 Shared Drive, Open Our GDrive in Button Below </b>

<b>If you don't have access, you need to join our groups</b>
<b>and don't spamming request access</b>
<b>and you only can join 1 email tho, thanks have a nice day 😁</b>

<b>⚡️ Transfer Gate 1 ⚡️</b>
<b>⚡️ Transfer Gate 2 ⚡️</b>
<b>⚡️ Transfer Gate 3 ⚡️</b>
'''
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("Transfer Gate 1 👇🏻🏻", "https://drive.google.com/drive/u/0/folders/0AKsMNMRrF9NgUk9PVA")
    buttons.buildbutton("Transfer Gate 2 👇🏻🏻", "https://drive.google.com/drive/u/0/folders/0APWyZJWQRZ87Uk9PVA")
    buttons.buildbutton("Transfer Gate 3 👇🏻🏻", "https://drive.google.com/drive/u/0/folders/0AFVhE30K7gpWUk9PVA")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(1))
    update.effective_message.reply_photo(IMAGE_URL, drives_string, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

@run_async
def repo(update, context):
    repo_string = '''
𝙒𝙚 𝘾𝙪𝙧𝙧𝙚𝙣𝙩𝙡𝙮 𝙃𝙖𝙙 𝙂𝙧𝙤𝙪𝙥𝙨 
𝙃𝙚𝙧𝙚 𝙄𝙛 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙅𝙤𝙞𝙣 😎?
𝘿𝙤𝙣'𝙩 𝙛𝙤𝙧𝙜𝙚𝙩 𝙩𝙤 𝙛𝙤𝙡𝙡𝙤𝙬 𝙤𝙪𝙧 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 💢

- 𝙊𝙬𝙣𝙚𝙧
'''
    buttons = button_build.ButtonMaker()
    buttons.buildbutton("🔱 𝙂𝙧𝙤𝙪𝙥 1 🔱", "https://t.me/joinchat/SNDQh7vYDkr5q1H5")
    buttons.buildbutton("🔱 𝙂𝙧𝙤𝙪𝙥 2 🔱", "https://t.me/joinchat/Ml7dMhQ9xTTOKbbwL6FiEg")
    buttons.buildbutton("🔱 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 🔱", "https://t.me/Jusidama")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    update.effective_message.reply_photo(IMAGE_URL, repo_string, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


@run_async
def owner(update, context):
    owner_string = f'''
╭────「 *ADMIN COMMAND LIST* 」───────╮
│
├ • `/{BotCommands.UsageCommand}` *: To see Heroku Dyno Stats.*
│
├ • `/{BotCommands.LogCommand}` *: Get a Bot log file. Handy for crash reports.*
│
├ • `/{BotCommands.AuthorizeCommand}` *: Authorize a chat or a user to bot.*
│
├ • `/{BotCommands.UnAuthorizeCommand}` *: Unauthorize a chat or a user to bot.*
│
├ • `/{BotCommands.AuthorizedUsersCommand}` *: See Authorized list & Sudo User*
│
├ • `/{BotCommands.AddSudoCommand}` *: Add sudo user .*
│
├ • `/{BotCommands.RmSudoCommand}` *: Remove sudo users.*
│
├ • `/{BotCommands.RestartCommand}` *: Restart bot.*
│
├ • `/{BotCommands.DeleteCommand}` *[Link] : Delete file from Google Drive.*
│
├ • `/shellhelp` *: Get help for shell and eval stuff module.*
│
├ • `/system` *: Get system information for this bot.*
│
├ • `/getsize` *: Get drive size with rclone.*
│
├ • `/leave` *: Make bot leave provided group id.*
│
╰────「 *ONLY OWNER & SUDO* 」───────╯
'''
    update.effective_message.reply_text(owner_string, parse_mode=ParseMode.MARKDOWN)


@run_async
def extrahelp(update, context):
    extrahelp_string = '''
╭────「 *EXTRA COMMAND LIST* 」───────╮
│
├ • `/gr` *: Reply a message for a corrected grammar*
│
├ • `/covid` *: Get worldwide corona status.*
│
├ • `/aq` *: Give you random anime quotes.*
│
├ • `/truth` *: Give you a truth option challenge option*
│
├ • `/dare` *: Give you a dare challenge option*
│
├ • `/react` *: Reacting to a message mentioned.*
│
├ • `/git` *<user> : Returns GitHub info from username*
│
├ • `/rmbg` *: Returns picture with removed background*
│
├ • `/weather` *: Gets weather info from provided city!*
│
├ • `/cash` *: To convert realtime currency, ex. 10 usd idr.*
│
╰ • `/time` *<tz> : Gives information about a timezone.*
'''
    update.effective_message.reply_text(extrahelp_string, parse_mode=ParseMode.MARKDOWN)

help_handler = CommandHandler(BotCommands.HelpCommand, bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
extra_handler = CommandHandler("extra", extrahelp, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
next_handler = CommandHandler("next", nexthelp, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
index_handler = CommandHandler("index", index, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
drives_handler = CommandHandler("drive", drives, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
shellhelp_handler = CommandHandler("shellhelp", shellhelp, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
owner_handler = CommandHandler("admin", owner, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
repo_handler = CommandHandler(BotCommands.RepoCommand, repo, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
configinfo_handler = CommandHandler("config", configinfo, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)


dispatcher.add_handler(configinfo_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(extra_handler)
dispatcher.add_handler(drives_handler)
dispatcher.add_handler(owner_handler)
dispatcher.add_handler(index_handler)
dispatcher.add_handler(next_handler)
dispatcher.add_handler(shellhelp_handler)
dispatcher.add_handler(repo_handler)
