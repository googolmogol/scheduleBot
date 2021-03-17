from datetime import datetime
from threading import Thread

from additional_python_files.callback_handler import callback_call
import additional_python_files.parsing_sheet as ps
from additional_python_files.send_messages import message_with_text
import additional_python_files.variables as v
from additional_python_files.reply_keyboard import *
from additional_python_files.message_handler import message_handler
from additional_python_files.functions import get_schedule, week_change

import telebot
import schedule
import time


bot = telebot.TeleBot("1642275922:AAHxeYvKI821oXHIaD2D0XiSra9goFiqNQ4")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        v.get_time_reminder(message.chat.id, '00:10')
        v.get_language(message.chat.id, 'UA')
        v.first_schedule = schedule.every().day.at("00:01").do(get_schedule, bot, message, message.chat.id, v.week)

        fname = str(message.from_user.first_name)
        surname = str(message.from_user.last_name)
        usr_id = str(message.from_user.username)

        ps.insert_users(message.chat.id, 'UA', fname, surname, usr_id, 'yes', 'yes', '00:10')
        ps.create_work(str(message.chat.id))

    except Exception as e:
        print(e)

    language = inline_button_callback({"Українська": 'ua', "Русский": 'ru'}, 2)
    message_with_text(bot, message, "Для знаходження спільної мови давайте визначимо її.\nОберіть мову:", language)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    # Если язык не установлен, по умолчанию ставит украинский
    try:
        if len(v.dictionary_bot[message.chat.id]) < 1:
            v.get_language(message.chat.id, 'UA')

    except Exception as ex:
        print(ex)
        lang = ps.get_user_language(message.chat.id)
        if lang != '' and lang is not None:
            v.get_language(message.chat.id, lang)
        else:
            v.get_language(message.chat.id, 'UA')
    message_handler(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # Если язык не установлен, по умолчанию ставит украинский
    try:
        if len(v.dictionary_bot[call.from_user.id]) < 1:
            v.get_language(call.from_user.id, 'UA')

    except Exception as ex:
        print(ex)
        lang = ps.get_user_language(call.from_user.id)
        if lang != '' and lang is not None:
            v.get_language(call.from_user.id, lang)
        else:
            v.get_language(call.from_user.id, 'UA')
    callback_call(bot, call)


#  https://qna.habr.com/q/394496
def checker_schedule():

    while True:
        if len(v.chat_id_list) > 0:
            schedule.run_pending()
            if datetime.today().isoweekday() == 7 and str(datetime.now().time())[:-7] == "21:59:59":
                week_change()

        time.sleep(1)


#  https://bit.ly/3dnzZbh
#  обязательно нужен новый поток, чтобы не было споров цикла бота и schedule


Thread(target=checker_schedule).start()


def start_bot():
    bot.polling(none_stop=True)


Thread(target=start_bot).start()
