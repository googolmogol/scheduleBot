import additional_python_files.variables as v
from additional_python_files.reply_keyboard import inline_button_url


def simple_message(bot, message, markup):
    bot.send_message(message.chat.id, message.text, parse_mode="HTML", reply_markup=markup,
                     disable_web_page_preview=True)


def message_with_text(bot, message, text, markup):
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)




def send_schedule_msg(bot, message, text, url):
    markup = inline_button_url(v.dictionary_bot[message.chat.id]["link"], url)
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
