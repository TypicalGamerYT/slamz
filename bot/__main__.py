import shutil, psutil
import signal
import pickle
from pyrogram import idle
import platform
from platform import python_version
from bot import app
from os import execl, kill, path, remove
from sys import executable
from datetime import datetime
import pytz
import datetime
from datetime import datetime
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, __version__
from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime, AUTHORIZED_CHATS, IMAGE_URL
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize, list, cancel_mirror, mirror_status, mirror, clone, watch, shell, eval, anime, stickers, search, delete, speedtest, usage, gtranslator, paste

now=datetime.now(pytz.timezone('Asia/Jakarta'))


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    current = now.strftime('%Y/%m/%d %I:%M:%S %p')
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    stats = f'======[ SYSTEM STATUS ]======\n' \
            f'<b>Bot Uptime ⌚:</b> {currentTime}\n' \
            f'<b>Total Space 🗄️:</b> {total}\n' \
            f'<b>Used Space 🗃️:</b> {used}  ' \
            f'<b>Free Space 🗃️:</b> {free}\n' \
            f'<b>Bot First Boot 👨‍💻:</b> {current}\n\n' \
            f'📇<b>Pengunaan data bot</b>📇\n<b>Total Upload :</b> {sent}\n' \
            f'<b>Total Download:</b> {recv}\n\n' \
            f'<b>CPU 🖥️:</b> {cpuUsage}% ' \
            f'<b>RAM ⛏️:</b> {memory}% ' \
            f'<b>DISK 🗄️:</b> {disk}%'
    update.effective_message.reply_photo(IMAGE_URL, stats, parse_mode=ParseMode.HTML)


@run_async
def start(update, context):
    start_string = f'''
This bot can mirror all your links to Google drive!
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
    update.effective_message.reply_photo(IMAGE_URL, start_string, parse_mode=ParseMode.MARKDOWN)


@run_async
def chat_list(update, context):
    chatlist =''
    chatlist += '\n'.join(str(id) for id in AUTHORIZED_CHATS)
    sendMessage(f'<b>======[ AUTHORIZED LIST ]======</b>\n<code>{chatlist}</code>\n', context.bot, update)


@run_async
def repo(update, context):
    repo_string = '''
𝙒𝙚 𝘾𝙪𝙧𝙧𝙚𝙣𝙩𝙡𝙮 𝙃𝙖𝙙 𝙂𝙧𝙤𝙪𝙥𝙨 
𝙃𝙚𝙧𝙚 𝙄𝙛 𝙔𝙤𝙪 𝙒𝙖𝙣𝙩 𝙏𝙤 𝙅𝙤𝙞𝙣 😎?
𝘿𝙤𝙣'𝙩 𝙛𝙤𝙧𝙜𝙚𝙩 𝙩𝙤 𝙛𝙤𝙡𝙡𝙤𝙬 𝙤𝙪𝙧 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 💢

- 𝙊𝙬𝙣𝙚𝙧
'''
    button = [
    [InlineKeyboardButton("🔱 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 🔱", url=f"https://t.me/Jusidama")],
    [InlineKeyboardButton("🔱 𝙂𝙧𝙤𝙪𝙥 1 🔱", url=f"https://t.me/joinchat/SNDQh7vYDkr5q1H5")],
    [InlineKeyboardButton("🔱 𝙂𝙧𝙤𝙪𝙥 2 🔱", url=f"https://t.me/joinchat/Ml7dMhQ9xTTOKbbwL6FiEg")]]
    reply_markup = InlineKeyboardMarkup(button)
    update.effective_message.reply_photo(IMAGE_URL, repo_string, parse_mode=ParseMode.HTML, reply_markup=reply_markup)


@run_async
def restart(update, context):
    restart_message = sendMessage("Restarting, Please wait!", context.bot, update)
    LOGGER.info(f'Restarting the Bot...')
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log(update, context):
    sendLogFile(context.bot, update)

@run_async
def systemstats(update, context):
    uname = platform.uname()
    system = platform.system()
    
    code = f'<b>======[ SYSTEM INFO ]======</b>\n\n' \
             f'<b>System:</b> <code>' + str(uname.system) + '</code>\n' \
             f'<b>Node name:</b> <code>' + str(uname.node) + '</code>\n' \
             f'<b>Release:</b> <code>' + str(uname.release) + '</code>\n' \
             f'<b>Version:</b> <code>' + str(uname.version) + '</code>\n' \
             f'<b>Machine:</b> <code>' + str(uname.machine) + '</code>\n' \
             f'<b>Processor:</b> <code>' + str(uname.processor) + '</code>\n' \
             f'<b>Python version:</b> <code>' + python_version() + '</code>\n' \
             f'<b>Library version:</b> <code>' + str(__version__) + '</code>\n'
    context.bot.sendMessage(
        update.effective_chat.id, code, parse_mode=ParseMode.HTML
       )
    update.effective_message.reply_photo(IMAGE_URL, code, parse_mode=ParseMode.HTML)
    
@run_async
def bot_help(update, context):
    help_string = f'''
/{BotCommands.HelpCommand}: To get this message

/{BotCommands.MirrorCommand} [download_url][magnet_link]: Start mirroring the link to google drive

/{BotCommands.UnzipMirrorCommand} [download_url][magnet_link]: Starts mirroring and if downloaded file is any archive, extracts it to google drive

/{BotCommands.TarMirrorCommand} [download_url][magnet_link]: Start mirroring and upload the archived (.tar) version of the download

/{BotCommands.CloneCommand}: Copy file/folder to google drive

/{BotCommands.WatchCommand} [youtube-dl supported link]: Mirror through youtube-dl. Click /{BotCommands.WatchCommand} for more help.

/{BotCommands.TarWatchCommand} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.CancelMirror}: Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.StatusCommand}: Shows a status of all the downloads

/{BotCommands.ListCommand} [search term]: Searches the search term in the Google drive, if found replies with the link

/{BotCommands.StatsCommand}: Show Stats of the machine the bot is hosted on

/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Can only be invoked by owner of the bot)

/{BotCommands.AuthListCommand}: See Authorized list (Can only be invoked by owner of the bot)

/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports

/{BotCommands.UsageCommand}: To see Heroku Dyno Stats (Owner only).

/{BotCommands.SpeedCommand}: Check Internet Speed of the Host

/{BotCommands.RepoCommand}: Get the bot repo.

/{BotCommands.SystemstatsCommand} : Get system information for this bot.

/{BotCommands.TotranslateCommand} : Translating message with listed code.

/{BotCommands.PasteCommand} : Paste a word to neko.bin from message.

/tshelp: Get help for torrent search module.

/weebhelp: Get help for anime, manga and character module.

/stickerhelp: Get help for stickers module.
'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        LOGGER.info('Restarted Successfully!')
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    repo_handler = CommandHandler(BotCommands.RepoCommand, repo,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    authlist_handler = CommandHandler(BotCommands.AuthListCommand, chat_list, filters=CustomFilters.owner_filter)
    system_handler = CommandHandler(BotCommands.SystemstatsCommand, systemstats,
                                    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(repo_handler)
    dispatcher.add_handler(authlist_handler)
    dispatcher.add_handler(system_handler)
    
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
