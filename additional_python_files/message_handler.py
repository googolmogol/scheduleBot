from additional_python_files.functions import *
from additional_python_files.reply_keyboard import *
from additional_python_files.send_messages import *
import additional_python_files.variables as variable
import additional_python_files.parsing_sheet as ps


def message_handler(bot, message):
    user = message.chat.id
    # Если язык не установлен, по умолчанию ставит украинский
    try:
        if len(variable.dictionary_bot[user]) < 1:
            variable.get_language(user, 'UA')
    except Exception as ex:
        print(ex)
        lang = ps.get_user_language(user)
        if lang != '' and lang is not None:
            variable.get_language(user, lang)
        else:
            variable.get_language(user, 'UA')

    if message.text == variable.dictionary_bot[user]["main_menu"]:
        clear_user_step(variable.user_step_edit_list[user], "action")
        clear_user_step(variable.user_step_add_list[user], "action")
        simple_message(bot, message, simple_keyboard(True, False, 0, 2, variable.main_menu_list(user)))
    #####################
    # back to edit menu #
    #####################
    elif message.text == variable.dictionary_bot[user]['back_to_edit_menu']:
        clear_user_step(variable.user_step_edit_list[user], "action")
        clear_user_step(variable.user_step_add_list[user], "action")

        simple_message(bot, message, simple_keyboard(True, False, 0, 2, variable.edit_schedule_list(user)))
    ########################
    # back to choosing day #
    ########################
    elif message.text == variable.dictionary_bot[user]['back_to_day_choosing']:
        clear_user_step(variable.user_step_edit_list[user], "day")
        message_with_text(bot, message, variable.dictionary_bot[user]["choose_day"],
                          simple_keyboard(True, True, 2, 3, variable.days_list(user)))
    #########################
    # back to choosing week #
    #########################
    elif message.text == variable.dictionary_bot[user]["back_to_choosing_week"]:
        clear_user_step(variable.user_step_edit_list[user], "week")
        simple_message(bot, message, simple_keyboard(True, False, 0, 3, variable.edit_lesson_list(user)))
    ###########################
    # back to lesson choosing #
    ###########################
    elif message.text == variable.dictionary_bot[user]['back_to_lesson_choosing']:
        try:
            clear_user_step(variable.user_step_edit_list[user], "lesson_num")
            message_with_text(bot, message, variable.text_list[user], simple_keyboard(True, False, 2, 3,
                                                                                      variable.button_list[user]))
        except Exception as e:
            print("back to lesson btn", e)
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))
    ###############
    # save button #
    ###############
    elif message.text == variable.dictionary_bot[user]['save']:
        if status_user(variable.user_step_edit_list[user], 'changed_value'):
            row = ps.row_index_to_change[user][int(variable.user_step_edit_list[user]["lesson_num"]) - 1]
            col = variable.items_change_dict(get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]
                                             ["item_to_change"]))
            if variable.user_step_edit_list[user]["item_to_change"] == variable.dictionary_bot[user]["week's"]:
                value = get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]["changed_value"])
            else:
                value = variable.user_step_edit_list[user]["changed_value"]
            print(ps.worksheet, row, col, value)
            ps.update_data(ps.worksheet, row, col, value)

            btn_list = [variable.dictionary_bot[user]['back_to_day_choosing'],
                        variable.dictionary_bot[user]["main_menu"]]
            text = variable.dictionary_bot[user]["save_action"]
            message_with_text(bot, message, text, simple_keyboard(True, False, 2, 2, btn_list))
            clear_user_step(variable.user_step_edit_list[user], "changed_value")
        elif status_user(variable.user_step_add_list[user], 'link'):
            btn_list = [variable.dictionary_bot[user]['back_to_edit_menu'], variable.dictionary_bot[user]["main_menu"]]
            text = variable.dictionary_bot[user]["save_action"]
            day = get_key(variable.dictionary_bot[user], variable.user_step_add_list[user]['day'])
            week = get_key(variable.dictionary_bot[user], variable.user_step_add_list[user]['week'])
            variable.user_step_add(user, "day", day)
            variable.user_step_add(user, "week", week)
            ps.add_new_lesson(list(variable.user_step_add_list[user].values())[1:])
            message_with_text(bot, message, text, simple_keyboard(True, False, 2, 2, btn_list))
    #################
    # delete button #
    #################
    elif message.text == variable.dictionary_bot[user]['delete_this_lesson']:
        text = variable.dictionary_bot[user]["are_you_sure_to_del_lesson"]
        text += ' "' + variable.lesson_to_change[user][int(variable.user_step_edit_list[user]["lesson_num"]) - 1][2] + \
                '"?'
        btn_list = list()
        btn_list.append(variable.dictionary_bot[user]['yes'])
        btn_list.append(variable.dictionary_bot[user]['no'])
        message_with_text(bot, message, text, simple_keyboard(True, True, 2, 2, btn_list))
    ##############
    # yes button #
    ##############
    elif message.text == variable.dictionary_bot[user]['yes']:
        if status_user(variable.user_step_edit_list[user], "lesson_num"):
            for i in range(1, 7):
                ps.update_data(ps.worksheet, ps.row_index_to_change[user][int(variable.user_step_edit_list[user]
                                                                              ["lesson_num"]) - 1], i, "")
            btn_list = list()
            btn_list.append(variable.dictionary_bot[user]["back_to_lesson_choosing"])
            btn_list.append(variable.dictionary_bot[user]["main_menu"])
            text = variable.dictionary_bot[user]["deleted"]
            message_with_text(bot, message, text, simple_keyboard(True, False, 0, 2, btn_list))
        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))
    #############
    # no button #
    #############
    elif message.text == variable.dictionary_bot[user]["no"]:
        btn_list = list()
        btn_list.append(variable.dictionary_bot[user]["back_to_lesson_choosing"])
        btn_list.append(variable.dictionary_bot[user]["main_menu"])
        simple_message(bot, message, simple_keyboard(True, False, 0, 2, btn_list))
    #######################
    # enter value to edit #
    #######################
    elif status_user(variable.user_step_edit_list[user], 'item_to_change'):
        btn_list = [variable.dictionary_bot[user]["save"], variable.dictionary_bot[user]['back_to_lesson_choosing'],
                    variable.dictionary_bot[user]["main_menu"]]
        item = get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]["item_to_change"])
        if item == 'time':
            if datetime_format(message.text)[1]:
                variable.user_step_edit(user, "changed_value", datetime_format(message.text)[0])
                message_with_text(bot, message, variable.dictionary_bot[user]["press_save_edit"],
                                  simple_keyboard(True, True, 0, 2, btn_list))
            else:
                message_with_text(bot, message, variable.dictionary_bot[user]["enter_correct_time"],
                                  simple_keyboard(True, True, 0, 0, ''))
        elif item == "link's":
            if checking_url(message.text):
                variable.user_step_edit(user, "changed_value", message.text)
                message_with_text(bot, message, variable.dictionary_bot[user]["press_save_edit"],
                                  simple_keyboard(True, True, 0, 2, btn_list))
            else:
                message_with_text(bot, message, variable.dictionary_bot[user]["enter_correct_link"],
                                  simple_keyboard(True, False, 0, 2, ''))
        else:
            variable.user_step_edit(user, "changed_value", message.text)

            message_with_text(bot, message, variable.dictionary_bot[user]["press_save_edit"],
                              simple_keyboard(True, True, 0, 2, btn_list))
    ######################
    # enter value to add #
    ######################
    elif status_user(variable.user_step_add_list[user], 'week'):

        if checking_url(message.text):
            variable.user_step_add(user, "link", message.text)
            text = variable.dictionary_bot[user]["day"] + ": " + variable.user_step_add_list[user]['day'].lower() + "\n"
            text += get_add_lesson(user)
            text += "\n\n" + variable.dictionary_bot[user]["save_add_lesson"]
            btn_list = list()
            btn_list.append(variable.dictionary_bot[user]["save"])
            btn_list.append(variable.dictionary_bot[user]["main_menu"])
            message_with_text(bot, message, text, simple_keyboard(True, False, 0, 2, btn_list))
        else:
            text = variable.dictionary_bot[user]["enter_correct_link"]
            message_with_text(bot, message, text, simple_keyboard(True, False, 0, 2, ''))
    elif status_user(variable.user_step_add_list[user], 'teacher'):
        variable.user_step_add(user, "week", message.text)
        text = variable.dictionary_bot[user]["enter"] + " " + variable.dictionary_bot[user]["link's"].lower()
        message_with_text(bot, message, text, "")
    elif status_user(variable.user_step_add_list[user], 'lesson_name'):
        variable.user_step_add(user, "teacher", message.text)
        text = variable.dictionary_bot[user]["enter"] + " " + variable.dictionary_bot[user]["week's"].lower()
        btn_list = variable.edit_lesson_list(user)[:-2]
        btn_list.append(variable.dictionary_bot[user]["back_to_lesson_choosing"])
        btn_list.append(variable.dictionary_bot[user]["main_menu"])
        message_with_text(bot, message, text, simple_keyboard(True, True, 0, 3, btn_list))
    elif status_user(variable.user_step_add_list[user], 'time'):
        variable.user_step_add(user, "lesson_name", message.text)
        text = variable.dictionary_bot[user]["enter"] + " " + variable.dictionary_bot[user]["teacher's"].lower()
        message_with_text(bot, message, text, "")
    elif status_user(variable.user_step_add_list[user], 'day'):
        if datetime_format(message.text)[1]:
            variable.user_step_add(user, "time", datetime_format(message.text)[0])
            text = variable.dictionary_bot[user]["enter"] + " " + variable.dictionary_bot[user]["lesson_name"].lower()
            message_with_text(bot, message, text, "")
        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["enter_correct_time"],
                              simple_keyboard(True, True, 0, 0, ''))
    ##################
    # main menu list #
    ##################
    elif message.text in variable.main_menu_list(user):
        if message.text == variable.dictionary_bot[user]['show_schedule']:
            show_schedule(bot, message)
            variable.user_show_schedule[user]["action"] = message.text
            message_with_text(bot, message, variable.dictionary_bot[user]['choose_week'],
                              simple_keyboard(True, False, 0, 2, variable.show_schedule_list(user)))

        elif message.text == variable.dictionary_bot[user]["edit_schedule"]:
            message_with_text(bot, message, variable.dictionary_bot[user]['choose_what_edit'],
                              simple_keyboard(True, False, 0, 2, variable.edit_schedule_list(user)))

        elif message.text == variable.dictionary_bot[user]["settings_bot"]:
            simple_message(bot, message, simple_keyboard(True, False, 0, 2, variable.bot_settings_list(user)))
    ##################
    # bot settings ###
    ##################
    elif message.text in variable.bot_settings_list(user):
        if message.text == variable.dictionary_bot[user]['change_language']:
            language = inline_button_callback({"Українська": 'ua', "Русский": 'ru'})
            message_with_text(bot, message, variable.dictionary_bot[user]["choose_lan"], language)
    ######################
    # edit schedule list #
    ######################
    elif message.text in variable.edit_schedule_list(user):
        clear_user_step(variable.user_step_edit_list[user], "action")
        clear_user_step(variable.user_step_add_list[user], "action")

        if message.text == variable.dictionary_bot[user]["edit_lesson"]:
            variable.user_step_edit(user, "action", message.text)
            message_with_text(bot, message, variable.dictionary_bot[user]['choose_week'],
                              simple_keyboard(True, False, 0, 3, variable.edit_lesson_list(user)))
        elif message.text == variable.dictionary_bot[user]["delete_lesson"]:
            variable.user_step_edit(user, "action", message.text)
            message_with_text(bot, message, variable.dictionary_bot[user]['choose_week'],
                              simple_keyboard(True, False, 0, 3, variable.edit_lesson_list(user)))
        elif message.text == variable.dictionary_bot[user]["add_lesson"]:
            variable.user_step_add(user, "action", message.text)
            message_with_text(bot, message, variable.dictionary_bot[user]['choose_day'],
                              simple_keyboard(True, True, 2, 3, variable.days_list(user)))
    ####################
    # edit lesson list #
    ####################
    elif message.text in variable.edit_lesson_list(user):
        if status_user(variable.user_step_edit_list[user], 'action'):
            if message.text == variable.dictionary_bot[user]["even"] or message.text == \
                    variable.dictionary_bot[user]["odd"] or message.text == variable.dictionary_bot[user]["both"]:
                variable.user_step_edit(user, "week", message.text)
                message_with_text(bot, message, variable.dictionary_bot[user]["choose_day"],
                                  simple_keyboard(True, True, 2, 3, variable.days_list(user)))
        elif status_user(variable.user_show_schedule[user], "action"):
            if message.text == variable.dictionary_bot[user]["even"] or message.text == \
                    variable.dictionary_bot[user]["odd"] or message.text == variable.dictionary_bot[user]["both"]:
                week = get_key(variable.dictionary_bot[user], message.text)
                message_with_text(bot, message, ps.get_all_lessons(user, week), simple_keyboard(True, True,
                                  0, 2, variable.show_schedule_list(user)))
        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))
    ###################
    # days list #######
    ###################
    elif message.text in variable.days_list(user):
        if status_user(variable.user_step_edit_list[user], 'week'):
            variable.user_step_edit(user, "day", message.text)
            message_with_text(bot, message, variable.dictionary_bot[user]["loading_wait.."],
                              simple_keyboard(True, False, 0, 0, ['']))
            week = get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]["week"])
            day = get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]["day"])
            variable.button_list[user], variable.text_list[user] = get_lessons_to_change(user, week, day)
            message_with_text(bot, message, variable.text_list[user], simple_keyboard(True, False, 2, 3,
                              variable.button_list[user]))
        elif status_user(variable.user_step_add_list[user], "action"):
            variable.user_step_add(user, "day", message.text)
            message_with_text(bot, message, variable.dictionary_bot[user]["enter_time_add"], '')
        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))
    ###################
    # choose lesson № #
    ###################
    elif len(variable.button_list) > 0 and message.text in variable.button_list[user]:
        if status_user(variable.user_step_edit_list[user], 'day'):
            if message.text.isdigit():
                variable.user_step_edit(user, "lesson_num", message.text)
                btn_list, text = get_text_choosing_lesson_num(user, message)
                if variable.user_step_edit_list[user]["action"] == variable.dictionary_bot[user]["edit_lesson"]:

                    i = variable.lesson_to_change[user][int(variable.user_step_edit_list[user]["lesson_num"]) - 1]
                    text = get_lesson(i, user)
                    text += "\n\n" + variable.dictionary_bot[user]["choose_what_edit"]

                    message_with_text(bot, message, text, simple_keyboard(True, True, 2, 3, btn_list))
                elif variable.user_step_edit_list[user]["action"] == variable.dictionary_bot[user]["delete_lesson"]:
                    btn_list.clear()
                    btn_list.append(variable.dictionary_bot[user]["delete_this_lesson"])
                    btn_list.append(variable.dictionary_bot[user]["back_to_day_choosing"])
                    btn_list.append(variable.dictionary_bot[user]["main_menu"])
                    text = variable.lesson_to_change[user][int(variable.user_step_edit_list[user]["lesson_num"]) - 1][2]
                    print(text)
                    message_with_text(bot, message, text, simple_keyboard(True, False, 2, 3, btn_list))

        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))

    #########################
    # choose item to change #
    #########################
    elif message.text in variable.edit_lesson_btn_list(user):
        if status_user(variable.user_step_edit_list[user], 'lesson_num'):
            variable.user_step_edit(user, "item_to_change", message.text)
            value = get_key(variable.dictionary_bot[user], variable.user_step_edit_list[user]["item_to_change"])
            text = variable.dictionary_bot[user]["enter"] + " " + variable.dictionary_bot[user][value].lower()
            if message.text == variable.dictionary_bot[user]["week's"]:
                btn_list = variable.edit_lesson_list(user)[:-2]
                print(btn_list)
                btn_list.append(variable.dictionary_bot[user]["back_to_lesson_choosing"])
                btn_list.append(variable.dictionary_bot[user]["main_menu"])
                message_with_text(bot, message, text, simple_keyboard(True, False, 0, 3, btn_list))
            else:
                message_with_text(bot, message, text, simple_keyboard(True, True, 0, 0, ""))
        else:
            message_with_text(bot, message, variable.dictionary_bot[user]["tech_changes"], simple_keyboard(True, True,
                              0, 2, [variable.dictionary_bot[user]["main_menu"]]))

    else:
        message_with_text(bot, message, 'Это собсна што', "")

    print("EDIT  :", message.from_user.first_name, variable.user_step_edit_list[user])
    print("ADD  :", message.from_user.first_name, variable.user_step_add_list[user])

    print('MESSAGE TEXT =', message.text)
