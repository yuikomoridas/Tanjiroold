import html
import random
from SaitamaRobot import dispatcher
from telegram import ParseMode, Update, Bot
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async

@run_async
def aq(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change🔁", callback_data="change_quote")]]
    )
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@run_async
def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change🔁", callback_data="quote_change")]]
    )
    message.edit_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)

__help__ = """
 • `/aq`*:* for random animequote
"""

AQ_HANDLER = DisableAbleCommandHandler("aq", aq)

dispatcher.add_handler(AQ_HANDLER)

__mod_name__ = "Animequote"
