#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from bot.modules.others.gcloner.utils.callback import callback_delete_message
from bot.modules.others.gcloner.utils.config_loader import config
from bot.modules.others.gcloner.utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('gstart', start))


@restricted
def start(update, context):
    rsp = update.message.reply_text('🔺 First, send me a ZIP archive containing the SA files and add /sa to the subject.\n'
                                    '📂 After that, use /folders to set destination folders.\n'
                                    '🔗 You are now ready to go! Just forward or send a Google Drive link.')
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
