import shutil, psutil
import signal
import importlib

from pyrogram import idle

from bot import app

from sys import executable
from datetime import datetime
import pytz
import datetime
from datetime import datetime
from telegram import ParseMode, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async
from bot import bot, dispatcher, updater, botStartTime, AUTHORIZED_CHATS, IMAGE_URL
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from bot.modules import ALL_MODULES
from bot.plugins import ALL_PLUGINS

for module in ALL_MODULES:
    imported_module = importlib.import_module("bot.modules." + module)
    importlib.reload(imported_module)

for plugins in ALL_PLUGINS:
    imported_plugins = importlib.import_module("bot.plugins." + module)
    importlib.reload(imported_plugins)

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
Hello {update.message.chat.first_name}, this bot can help you mirror all your links to Google drive!
Type /{BotCommands.HelpCommand} to get a list of available commands.
'''
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    if CustomFilters.authorized_user(update) or CustomFilters.owner_filter(update) or CustomFilters.sudo_user(update):
        if update.message.chat.type == "private" :
            sendMessage(f"Hey I'm alive :)\n\n Chat ID : <code>{update.message.chat.id}</code>", context.bot, update)
        else :
            update.effective_message.reply_photo(IMAGE_URL, start_string, parse_mode=ParseMode.MARKDOWN)
    else :
        sendMessage(f"Oops! {update.message.chat.first_name}, you are not a authorized user.", context.bot, update)

@run_async
def restart(update, context):
    LOGGER.info('UID: {} - UN: {} - MSG: {}'.format(update.message.chat.id,update.message.chat.username,update.message.text))
    restart_message = sendMessage("<b>🔁 Restarting... Please wait! 🔁</b>", context.bot, update)
    LOGGER.info(f'Restarting the Bot...')
    # Save restart message object in order to reply to it after restarting
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    fs_utils.clean_all()
    os.execl(executable, executable, "-m", "bot")


@run_async
def log(update, context):
    sendLogFile(context.bot, update)

botcmds = [
BotCommand(f'{BotCommands.MirrorCommand}', 'Start Mirroring'),
BotCommand(f'{BotCommands.TarMirrorCommand}','Upload tar (zipped) file'),
BotCommand(f'{BotCommands.UnzipMirrorCommand}','Extract files'),
BotCommand(f'{BotCommands.CloneCommand}','Copy file/folder to Drive'),
BotCommand(f'{BotCommands.WatchCommand}','Mirror YT-DL support link'),
BotCommand(f'{BotCommands.TarWatchCommand}','Mirror Youtube playlist link as tar'),
BotCommand(f'{BotCommands.CancelMirror}','Cancel a task'),
BotCommand(f'{BotCommands.CancelAllCommand}','Cancel all tasks'),
BotCommand(f'{BotCommands.DeleteCommand}','Delete file from Drive'),
BotCommand(f'{BotCommands.ListCommand}',' [query] Searches files in G-Drive'),
BotCommand(f'{BotCommands.StatusCommand}','Get Mirror Status message'),
BotCommand(f'{BotCommands.StatsCommand}','Bot Usage Stats'),
BotCommand(f'{BotCommands.HelpCommand}','Get Detailed Help'),
BotCommand(f'{BotCommands.SpeedCommand}','Check Speed of the host'),
BotCommand(f'{BotCommands.LogCommand}','Bot Log [owner only]'),
BotCommand(f'{BotCommands.RestartCommand}','Restart bot [owner only]'),
BotCommand(f'{BotCommands.RepoCommand}','Get the group info'),
BotCommand(f'{BotCommands.TotranslateCommand}','Translating message with listed code.'),
BotCommand(f'{BotCommands.PasteCommand}','Paste a word to neko.bin from message.'),
BotCommand(f'{BotCommands.SearchHelpCommand}','Get help for torrent search module.'),
BotCommand(f'{BotCommands.WeebHelpCommand}','Get help for anime, manga and character module.'),
BotCommand(f'{BotCommands.StickerHelpCommand}','Get help for stickers module.')]

def main():
    current = now.strftime('%Y/%m/%d %I:%M:%P')
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        bot.edit_message_text(f"Restarted Successfully !\n"f"\nBot Start : {current}", chat_id, msg_id)
        os.remove(".restartmsg")

    start_handler = CommandHandler(BotCommands.StartCommand, start,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)

app.start()
main()
idle()
