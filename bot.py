from threading import Thread

from additional_python_files.callback_handler import callback_call
from additional_python_files.send_messages import message_with_text
import additional_python_files.variables as v
from additional_python_files.reply_keyboard import *
from additional_python_files.message_handler import message_handler

import telebot
import schedule
import time


bot = telebot.TeleBot("1642275922:AAHxeYvKI821oXHIaD2D0XiSra9goFiqNQ4")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    language = inline_button_callback({"Українська": 'ua', "Русский": 'ru'})
    message_with_text(bot, message, "Для знаходження спільної мови давайте визначимо її.\nОберіть мову:", language)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    print(message.from_user.first_name, message.text)
    message_handler(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    callback_call(bot, call)


#  https://qna.habr.com/q/394496
def checker_schedule():
    #determine_week()
    #get_full_row()
    #schedule.every(2).minutes.do(get_full_row)

    while True:
        if len(v.chat_id_list) > 0:
            schedule.run_pending()
        time.sleep(2)


#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule


Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
