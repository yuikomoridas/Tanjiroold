# Simple dictionary module by @ABoyWhoWonders
import requests

from telegram import Bot, Message, Update, ParseMode
from telegram.ext import CallbackContext,CommandHandler, run_async

from SaitamaRobot import dispatcher

@run_async
def define(update: Update, context: CallbackContext):
    msg = update.effective_message
    word = " ".join(context.args)
    res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if res.status_code != 200:
        msg.reply_text("No results found!")
    info = res.json()[0]['meanings']
    phonetics = res.json()[0]['phonetics']
    query_word = res.json()[0]['word']
    pronunciation = []
    if phonetics:
        for phonetic in phonetics:
            pronunciation.append(phonetic.get('text'))
    if info:
        if len(pronunciation):
            meaning = f"<b>{query_word.capitalize()}</b> {' or '.join(pronunciation)}\n\n"
        else:
            meaning = f"<b>Word:</b>{query_word}\n\n"
        count = 1
        for partOfSpeech in info:
            meaning += f"<b>Category:</b> {partOfSpeech.get('partOfSpeech').capitalize()}\n"
            definitions = partOfSpeech.get("definitions")

            for definition in definitions:
                for cnt, (key, value) in enumerate(definition.items()):
                    if not cnt:
                        meaning += f"<b>{count}.</b> {value}\n"
                    elif key == 'synonyms':
                        meaning += f"<b>{key.capitalize()}:</b> <i>{', '.join(value)}</i>\n"
                    else:
                        meaning += f"<b>{key.capitalize()}:</b> <i>{value}</i>\n"
                count += 1
            meaning += "\n"
        msg.reply_text(meaning, parse_mode=ParseMode.HTML)
    else:
        return


__help__ = """
Ever stumbled upon a word that you didn't know of and wanted to look it up?
With this module, you can find the definitions of words without having to leave the app!
*Available commands:*
 - /define(df) <word>: returns the definition of the word.
 """


DEFINE_HANDLER = CommandHandler(["define", "df"], define, pass_args=True)

dispatcher.add_handler(DEFINE_HANDLER)

__mod_name__ = "Dictionary"
__command_list__ = ["define"]
__handlers__ = [DEFINE_HANDLER]
