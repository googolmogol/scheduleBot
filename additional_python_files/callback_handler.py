from additional_python_files.functions import call_back_flag
from additional_python_files.reply_keyboard import *
import additional_python_files.variables as variables
import additional_python_files.parsing_sheet as ps


def callback_call(bot, call):
    user = call.from_user.id
    if call.data == 'ua':
        variables.get_language(user, 'UA')
        ps.update_language_user(user, 'UA')

        btn_list = call_back_flag('ua')
        text = variables.dictionary_bot[user]["choose_lan"] + '\n'
        text += variables.dictionary_bot[user]["curr_lan"]

        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=text,
                              reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, 'Ви обрали українську мову', reply_markup=simple_keyboard(True, False, 0, 2,
                                                                                    variables.main_menu_list(user)))
    elif call.data == 'ru':
        variables.get_language(user, 'RU')
        ps.update_language_user(user, 'RU')
        btn_list = call_back_flag('ru')
        text = variables.dictionary_bot[user]["choose_lan"] + '\n'
        text += variables.dictionary_bot[user]["curr_lan"]
        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=text,
                              reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, 'Вы выбрали русский язык',
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))

    # как отправлять смайлы
    # https://qna.habr.com/q/238682
    elif call.data == "get":

        btn_list = {'\U00002705' + variables.dictionary_bot[user]["get"]: "get", '\U0000274C' +
                    variables.dictionary_bot[user]["don't_get"]: "don't_get"}
        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=variables.dictionary_bot[user]
        ['choose_become_notification_text'], reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, variables.dictionary_bot[user]["you_will_become_notifications"],
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))

        ps.notif_update(user, 6, 'yes')

    elif call.data == "don't_get":

        btn_list = {'\U0000274C' + variables.dictionary_bot[user]["get"]: "get", '\U00002705' +
                    variables.dictionary_bot[user]["don't_get"]: "don't_get"}
        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=variables.dictionary_bot[user]
        ['choose_become_notification_text'], reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, variables.dictionary_bot[user]["you_won't_become_notifications"],
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))

        ps.notif_update(user, 6, 'no')

    elif call.data == "get_rem":

        btn_list = {'\U00002705' + variables.dictionary_bot[user]["get"]: "get_rem", '\U0000274C' +
                    variables.dictionary_bot[user]["don't_get"]: "don't_get_rem", variables.dictionary_bot[user]
        ["change_time"]: 'ch_time'}
        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=variables.dictionary_bot[user]
        ['choose_become_reminder_text'], reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, variables.dictionary_bot[user]["you_will_become_reminder"],
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))

        ps.notif_update(user, 7, 'yes')

    elif call.data == "don't_get_rem":

        btn_list = {'\U0000274C' + variables.dictionary_bot[user]["get"]: "get_rem", '\U00002705' +
                    variables.dictionary_bot[user]["don't_get"]: "don't_get_rem"}
        bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text=variables.dictionary_bot[user]
        ['choose_become_reminder_text'], reply_markup=inline_button_callback(btn_list, 2))
        bot.send_message(user, variables.dictionary_bot[user]["you_won't_become_reminder"],
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))

        ps.notif_update(user, 7, 'no')

    elif call.data == "ch_time":
        variables.get_change_rem_time(user, True)
        bot.send_message(user, variables.dictionary_bot[user]["enter_time_rem"], reply_markup="")
