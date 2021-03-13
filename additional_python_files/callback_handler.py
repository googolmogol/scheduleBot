from additional_python_files.reply_keyboard import *
import additional_python_files.variables as variables
import additional_python_files.parsing_sheet as ps


def callback_call(bot, call):
    user = call.from_user.id
    if call.data == 'ua':
        variables.get_language(user, 'UA')
        ps.update_language_user(user, 'UA')
        bot.send_message(user, 'Ви обрали українську мову',
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))
    elif call.data == 'ru':
        variables.get_language(user, 'RU')
        ps.update_language_user(user, 'RU')
        bot.send_message(user, 'Вы выбрали русский язык',
                         reply_markup=simple_keyboard(True, False, 0, 2, variables.main_menu_list(user)))
