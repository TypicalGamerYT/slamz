import logging
import os
import threading
import time
import random
import string
import aiohttp
import asyncio

import aria2p
import telegram.ext as tg

from dotenv import load_dotenv
from pyrogram import Client
from telegraph import Telegraph

from Python_ARQ import ARQ

import psycopg2
from psycopg2 import Error

import socket
import faulthandler
faulthandler.enable()
from megasdkrestclient import MegaSdkRestClient, errors as mega_err
import subprocess

socket.setdefaulttimeout(600)

botStartTime = time.time()
if os.path.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)

load_dotenv('config.env')

Interval = []

ARQ_API_URL = "https://thearq.tech" #Default URL.
ARQ_API_KEY = "MUTWXW-IOSFCI-AYCOHO-KXJNLI-ARQ" #Get this from @ARQRobot.

#### FOR NON RECURSIVE SEARCH

DRIVE_NAMES = [
    "Current Drive",
    "Main Data 0",  # folder 1 name
    "Main Data 1",  # folder 2 name
    "Main Data 2",  # folder 3 name
    "Main Data 3",  # ....
    "Main Data 4",  # ......
    "Main Data 5",
    "Aulia Index"  # and soo onnnn folder n names
]

DRIVE_IDS = [
    "0AEi4wTsML7qxUk9PVA",
    "1sQOTUg0OrRh-WY8JoLNgYmdePE0oLjSN",  # folder 1 id
    "1uODcU-1OWCmKZ40XxNkzeJvR3VlVtoSY",  # folder 2 id
    "10Mujqdc8qdVW1JYpv7zIDkFvrn3-X2Vr",  # and so onn... folder n id
    "18p8QAbCfqNPXNGkyWqOP2IsI31Q5y5Hi",
    "1vgabcaxjP96H87v12HOg3iFCP-ioN6wb",
    "1ya7SyXL1yjXltR-B8BPAw8YBNywnCE1h",
    "13k-FjJJvfR_Btcwd10zEOmqMEUl5bVlw"
]

INDEX_URLS = [
    "https://database.juicedama.workers.dev/7:",
    "https://md5.juicedama.workers.dev/0:",  # folder 1 index link
    "https://md5.juicedama.workers.dev/1:",  # folder 2 index link
    "https://md5.juicedama.workers.dev/2:",  # and soo on folder n link
    "https://md5.juicedama.workers.dev/3:",
    "https://md5.juicedama.workers.dev/4:",
    "https://md5.juicedama.workers.dev/5:",
    "https://auliachan.crysriski12.workers.dev/0:"
]

if os.path.exists('drive_folders'):
    with open('drive_folders', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip().split()
            DRIVE_NAMES.append(temp[0].replace("_", " "))
            DRIVE_IDS.append(temp[1])
            try:
                INDEX_URLS.append(temp[2])
            except IndexError as e:
                INDEX_URLS.append(None)

if DRIVE_IDS :
    pass

#### FOR NON RECURSIVE SEARCH

#### FOR RECURSIVE SEARCH

R_DRIVE_NAMES = []
R_DRIVE_IDS = []
R_INDEX_URLS = []

if os.path.exists('drive_folderz'):
    with open('drive_folderz', 'r+') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.strip().split()
            R_DRIVE_NAMES.append(temp[0].replace("_", " "))
            R_DRIVE_IDS.append(temp[1])
            try:
                R_INDEX_URLS.append(temp[2])
            except IndexError as e:
                R_INDEX_URLS.append(None)

if R_DRIVE_IDS :
    pass

#### FOR RECURSIVE SEARCH

# Aiohttp Client
print("[INFO]: INITIALZING AIOHTTP SESSION")
session = aiohttp.ClientSession()

# ARQ client
print("[INFO]: INITIALIZING ARQ")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)

def getConfig(name: str):
    return os.environ[name]

def mktable():
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        sql = "CREATE TABLE users (uid bigint, sudo boolean DEFAULT FALSE);"
        cur.execute(sql)
        conn.commit()
        LOGGER.info("Table Created!")
    except Error as e:
        LOGGER.error(e)
        exit(1)


LOGGER = logging.getLogger(__name__)

try:
    if bool(getConfig('_____REMOVE_THIS_LINE_____')):
        logging.error('The README.md file there to be read! Exiting now!')
        exit()
except KeyError:
    pass

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret="",
    )
)

DOWNLOAD_DIR = None
BOT_TOKEN = None

download_dict_lock = threading.Lock()
status_reply_dict_lock = threading.Lock()
# Key: update.effective_chat.id
# Value: telegram.Message
status_reply_dict = {}
# Key: update.message.message_id
# Value: An object of Status
download_dict = {}
# Stores list of users and chats the bot is authorized to use in
AUTHORIZED_CHATS = set()
SUDO_USERS = set()
try:
    achats = getConfig('AUTHORIZED_CHATS')
    achats = achats.split(" ")
    for chats in achats:
        AUTHORIZED_CHATS.add(int(chats))
except:
    pass

try:
    BOT_TOKEN = getConfig('BOT_TOKEN')
    DB_URI = getConfig("DATABASE_URL")
    parent_id = getConfig('GDRIVE_FOLDER_ID')
    DOWNLOAD_DIR = getConfig('DOWNLOAD_DIR')
    if not DOWNLOAD_DIR.endswith("/"):
        DOWNLOAD_DIR = DOWNLOAD_DIR + '/'
    DOWNLOAD_STATUS_UPDATE_INTERVAL = int(getConfig('DOWNLOAD_STATUS_UPDATE_INTERVAL'))
    OWNER_ID = int(getConfig('OWNER_ID'))
    AUTO_DELETE_MESSAGE_DURATION = int(getConfig('AUTO_DELETE_MESSAGE_DURATION'))
    TELEGRAM_API = getConfig('TELEGRAM_API')
    TELEGRAM_HASH = getConfig('TELEGRAM_HASH')
    GROUP_ID = getConfig("GROUP_ID")
except KeyError as e:
    LOGGER.error("One or more env variables missing! Exiting now")
    exit(1)

try:
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    sql = "SELECT * from users;"
    cur.execute(sql)
    rows = cur.fetchall()  #returns a list ==> (uid, sudo)
    for row in rows:
        AUTHORIZED_CHATS.add(row[0])
        if row[1]:
            SUDO_USERS.add(row[0])
except Error as e:
    if 'relation "users" does not exist' in str(e):
        mktable()
    else:
        LOGGER.error(e)
        exit(1)
finally:
    cur.close()
    conn.close()

LOGGER.info("Generating USER_SESSION_STRING")
app = Client(':memory:', api_id=int(TELEGRAM_API), api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)

#Generate Telegraph Token
sname = ''.join(random.SystemRandom().choices(string.ascii_letters, k=8))
LOGGER.info("Generating Telegraph Token using '" + sname + "' name")
telegraph = Telegraph()
telegraph.create_account(short_name=sname)
telegraph_token = telegraph.get_access_token()
LOGGER.info("Telegraph Token Generated: '" + telegraph_token + "'")

try:
    MEGA_KEY = getConfig('MEGA_KEY')

except KeyError:
    MEGA_KEY = None
    LOGGER.info('MEGA API KEY NOT AVAILABLE')
if MEGA_KEY is not None:
    # Start megasdkrest binary
    subprocess.Popen(["megasdkrest", "--apikey", MEGA_KEY])
    time.sleep(3)  # Wait for the mega server to start listening
    mega_client = MegaSdkRestClient('http://localhost:6090')
    try:
        MEGA_USERNAME = getConfig('MEGA_USERNAME')
        MEGA_PASSWORD = getConfig('MEGA_PASSWORD')
        if len(MEGA_USERNAME) > 0 and len(MEGA_PASSWORD) > 0:
            try:
                mega_client.login(MEGA_USERNAME, MEGA_PASSWORD)
            except mega_err.MegaSdkRestClientException as e:
                logging.error(e.message['message'])
                exit(0)
        else:
            LOGGER.info("Mega API KEY provided but credentials not provided. Starting mega in anonymous mode!")
            MEGA_USERNAME = None
            MEGA_PASSWORD = None
    except KeyError:
        LOGGER.info("Mega API KEY provided but credentials not provided. Starting mega in anonymous mode!")
        MEGA_USERNAME = None
        MEGA_PASSWORD = None
else:
    MEGA_USERNAME = None
    MEGA_PASSWORD = None
try:
    HEROKU_API_KEY = getConfig('HEROKU_API_KEY')
except KeyError:
    logging.warning('HEROKU API KEY not provided!')
    HEROKU_API_KEY = None
try:
    HEROKU_APP_NAME = getConfig('HEROKU_APP_NAME')
except KeyError:
    logging.warning('HEROKU APP NAME not provided!')
    HEROKU_APP_NAME = None
try:
    MAX_TORRENT_SIZE = int(getConfig("MAX_TORRENT_SIZE"))
except KeyError:
    MAX_TORRENT_SIZE = None
try:
   ENABLE_FILESIZE_LIMIT = getConfig('ENABLE_FILESIZE_LIMIT')
   if ENABLE_FILESIZE_LIMIT.lower() == 'true':
       ENABLE_FILESIZE_LIMIT = True
   else:
       ENABLE_FILESIZE_LIMIT = False
except KeyError:
    ENABLE_FILESIZE_LIMIT = False
try:
    UPTOBOX_TOKEN = getConfig('UPTOBOX_TOKEN')
except KeyError:
    logging.info('UPTOBOX_TOKEN not provided!')
    UPTOBOX_TOKEN = None
try:
    INDEX_URL = getConfig('INDEX_URL')
    if len(INDEX_URL) == 0:
        INDEX_URL = None
except KeyError:
    INDEX_URL = None
try:
    BUTTON_THREE_NAME = getConfig('BUTTON_THREE_NAME')
    BUTTON_THREE_URL = getConfig('BUTTON_THREE_URL')
    if len(BUTTON_THREE_NAME) == 0 or len(BUTTON_THREE_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_THREE_NAME = None
    BUTTON_THREE_URL = None
try:
    BUTTON_FOUR_NAME = getConfig('BUTTON_FOUR_NAME')
    BUTTON_FOUR_URL = getConfig('BUTTON_FOUR_URL')
    if len(BUTTON_FOUR_NAME) == 0 or len(BUTTON_FOUR_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FOUR_NAME = None
    BUTTON_FOUR_URL = None
try:
    BUTTON_FIVE_NAME = getConfig('BUTTON_FIVE_NAME')
    BUTTON_FIVE_URL = getConfig('BUTTON_FIVE_URL')
    if len(BUTTON_FIVE_NAME) == 0 or len(BUTTON_FIVE_URL) == 0:
        raise KeyError
except KeyError:
    BUTTON_FIVE_NAME = None
    BUTTON_FIVE_URL = None
try:
    STOP_DUPLICATE_MIRROR = getConfig('STOP_DUPLICATE_MIRROR')
    if STOP_DUPLICATE_MIRROR.lower() == 'true':
        STOP_DUPLICATE_MIRROR = True
    else:
        STOP_DUPLICATE_MIRROR = False
except KeyError:
    STOP_DUPLICATE_MIRROR = False
try:
    IS_TEAM_DRIVE = getConfig('IS_TEAM_DRIVE')
    if IS_TEAM_DRIVE.lower() == 'true':
        IS_TEAM_DRIVE = True
    else:
        IS_TEAM_DRIVE = False
except KeyError:
    IS_TEAM_DRIVE = False
try:
    USE_SERVICE_ACCOUNTS = getConfig('USE_SERVICE_ACCOUNTS')
    if USE_SERVICE_ACCOUNTS.lower() == 'true':
        USE_SERVICE_ACCOUNTS = True
    else:
        USE_SERVICE_ACCOUNTS = False
except KeyError:
    USE_SERVICE_ACCOUNTS = False
try:
    BLOCK_MEGA_LINKS = getConfig('BLOCK_MEGA_LINKS')
    if BLOCK_MEGA_LINKS.lower() == 'true':
        BLOCK_MEGA_LINKS = True
    else:
        BLOCK_MEGA_LINKS = False
except KeyError:
    BLOCK_MEGA_LINKS = False
try:
    SHORTENER = getConfig('SHORTENER')
    SHORTENER_API = getConfig('SHORTENER_API')
    if len(SHORTENER) == 0 or len(SHORTENER_API) == 0:
        raise KeyError
except KeyError:
    SHORTENER = None
    SHORTENER_API = None
try:
    IMAGE_URL = getConfig('IMAGE_URL')
except KeyError:
    IMAGE_URL = 'https://telegra.ph/file/db03910496f06094f1f7a.jpg'

app = Client('slam', api_id=TELEGRAM_API, api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)
updater = tg.Updater(token=BOT_TOKEN,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
