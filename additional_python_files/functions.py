from datetime import datetime

import schedule
import validators

import additional_python_files.variables as v
import additional_python_files.parsing_sheet as ps
from additional_python_files.send_messages import send_schedule_msg, message_with_text


def get_key(d, value):
    for k, val in d.items():
        if val == value:
            return k


# verifies compliance with the sequence of user steps
def status_user(user_step, value):
    keys = list(user_step.keys())
    first_elements = keys.index(value) + 1
    keys = keys[:first_elements]
    for i in keys:
        if user_step[i] == '':
            return False
    return True


# clear user status
def clear_user_step(user_step, current):
    keys = list(user_step.keys())[::-1]  # reverse list
    for i in keys:
        user_step[i] = ''
        if i == current:
            break


def get_lessons_to_change(user, ch_week, day):
    button_list = []
    text = "<strong>" + v.dictionary_bot[user][day] + ", " + v.dictionary_bot[user]["plural_lesson"].lower() + ", " + \
           v.dictionary_bot[user][ch_week].lower() + " " + v.dictionary_bot[user]["week"].lower() + ":</strong>\n\n"
    v.lesson_to_change[user] = ps.get_lessons_row(user, ch_week.lower(), day, True)
    counter = 1
    for i in v.lesson_to_change[user]:
        text += str(counter) + ". "
        counter += 1
        button_list.append(str(counter - 1))

        text += get_lesson(i, user)

        text += '\n\n'
    if len(v.lesson_to_change[user]) > 0:
        text += v.dictionary_bot[user]['choose_lesson_num_to_change']
    else:
        text = v.dictionary_bot[user]['no_lessons_today']
    button_list.append(v.dictionary_bot[user]['back_to_day_choosing'])
    button_list.append(v.dictionary_bot[user]['main_menu'])
    v.button_list[user] = button_list
    return v.button_list[user], text


def get_lesson(i, user):
    text = v.dictionary_bot[user]['lesson'] + ": " + i[2] + "\n" + v.dictionary_bot[user]['teacher'] + ": " + i[3] + \
           "\n" + v.dictionary_bot[user]['time'] + ": " + i[1] + "\n" + v.dictionary_bot[user]['link'] + ": " + \
           '<a href="' + i[5] + '">' + v.dictionary_bot[user]['link_short'] + "</a>\n" + \
           v.dictionary_bot[user]["week"] + ": " + v.dictionary_bot[user][i[4]].lower()
    return text


def get_add_lesson(user):
    text = v.dictionary_bot[user]['lesson'] + ": " + v.user_step_add_list[user]["lesson_name"] + "\n" + \
           v.dictionary_bot[user]['teacher'] + ": " + v.user_step_add_list[user]["teacher"] + "\n" + \
           v.dictionary_bot[user]['time'] + ": " + v.user_step_add_list[user]["time"] + "\n" + \
           v.dictionary_bot[user]['link'] + ": " + '<a href="' + v.user_step_add_list[user]['link'] + '">' + \
           v.dictionary_bot[user]['link_short'] + "</a>\n" + \
           v.dictionary_bot[user]["week"] + ": " + v.user_step_add_list[user]['week'].lower()
    return text


# chosing needed lesson
def get_text_choosing_lesson_num(user, message):
    index = int(message.text)
    text = '\n'
    text += v.dictionary_bot[user]['lesson'] + ": " + v.lesson_to_change[user][index - 1][2] + "\n" + \
        v.dictionary_bot[user]['teacher'] + ": " + v.lesson_to_change[user][index - 1][
                3] + "\n" + v.dictionary_bot[user]['time'] + ": " + v.lesson_to_change[user][index - 1][1] + "\n" + \
        v.dictionary_bot[user]['link'] + ": " + '<a href="' + v.lesson_to_change[user][index - 1][5] + '">' + \
        v.dictionary_bot[user]['link_short'] + '</a>\n' + v.dictionary_bot[user]["week"] + ': ' + \
        v.dictionary_bot[user][v.lesson_to_change[user][index - 1][4]].lower()
    text += '\n\n'
    btn_list = v.edit_lesson_btn_list(user)
    return btn_list, text


def datetime_format(user, time):
    try:
        return str(datetime.strptime(time, "%H:%M"))[11:-3], True
    except Exception as e:
        print(e)
        return v.dictionary_bot[user]["enter_correct_time"], False


def checking_url(url):
    if not validators.url(url):
        return False
    else:
        return True


def get_schedule(bot, message, user, week):
    try:
        if ps.get_notif(user, 6) == "yes":
            day = get_key(ps.days_dict, datetime.today().isoweekday())
            v.schedule_lesson[user] = ps.get_lessons_row(user, week, day, False)
            if len(v.schedule_lesson[user]) > 0:
                get_reminder(bot, message, user)
                for i in v.schedule_lesson[user]:
                    text = v.dictionary_bot[user]["lesson"] + ": " + i[2] + "\n" + v.dictionary_bot[user]["teacher"] + \
                           ": " + i[3]
                    url = i[5]
                    time = i[1]
                    v.schedule_list[user] = schedule.every().day.at(time).do(send_schedule_msg, bot, message, text, url)
    except Exception as e:
        print(e)


def get_reminder(bot, message, user):
    try:
        if ps.get_notif(user, 7) == "yes":
            rem_time = ps.get_notif(user, 8)
            for i in v.schedule_lesson[user]:
                text = v.dictionary_bot[user]["reminder"] + "!\n"
                text += v.dictionary_bot[user]["lesson"] + ' "' + i[2] + v.dictionary_bot[user]["reminder_txt"] + i[1]
                time = ps.time_before_lesson(i[1], rem_time)
                v.schedule_list[user] = schedule.every().day.at(time).do(message_with_text, bot, message, text, "")
    except Exception as e:
        print(e)


def week_change():
    if v.week == "odd":
        v.week = "even"
    else:
        v.week = "odd"
    print("week has changed")


def call_back_flag(lan):
    flag = '\ud83c\uddfa\ud83c\udde6'.encode("utf-16", "surrogatepass").decode("utf-16", "surrogatepass")
    if lan == 'ua':
        btn_list = {flag + "Українська": 'ua', "Русский": 'ru'}
    else:
        btn_list = {"Українська": 'ua', flag + "Русский": 'ru'}
    return btn_list
