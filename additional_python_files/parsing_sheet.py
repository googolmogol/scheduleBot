# https://www.youtube.com/watch?v=T1vqS1NL89E&ab_channel=PythonEngineer
# https://github.com/python-engineer/python-knowledge/blob/master/googlesheets.py
# https://www.youtube.com/watch?v=cnPlKLEGR7E&list=WL&index=17&ab_channel=TechWithTim
# https://www.techwithtim.net/tutorials/google-sheets-python-api-tutorial/

# open/create/delete new sheets tutorial
# https://github.com/burnash/gspread

from datetime import datetime
import gspread
import additional_python_files.variables as v

gc = gspread.service_account(filename='restfiles/cred.json')
sh = gc.open_by_key("19dLgpGsLAW4K4yiSdbpsA-njCGiDwhiYXa3uaWFJbsY")

worksheet2 = sh.worksheet("users")


def create_work(name):
    worksheet = sh.add_worksheet(title=name, rows="100", cols="20")
    worksheet.append_row(['day', 'time', 'lesson_name', 'teacher', 'week', 'link'])


# dictionary to recognize which day is today
days_dict = {"monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}
lesson_to_change = []  # list which will save the row of data from google sheet
row_index_to_change = {}


# function parsing lesson row
def get_lessons_row(user, week, day, row_index):
    worksheet = sh.worksheet(str(user))

    week_column = worksheet.col_values(5)  # list of weeks column

    row_index_to_change.clear()
    temp_list = []
    lesson_to_change.clear()  # clear previous data
    counter = 0  # counter for moving along rows
    for i in week_column:
        counter += 1
        if i == week or i == "both":
            if worksheet.cell(counter, 1).value == day:
                lesson_to_change.append(worksheet.row_values(counter))
                if row_index:
                    temp_list.append(counter)
    row_index_to_change[user] = temp_list
    print('USer', user, 'row_index_to_change:', row_index_to_change[user])
    return lesson_to_change


def get_all_lessons(user, week):
    worksheet = sh.worksheet(str(user))
    list_of_lists = worksheet.get_all_values()
    week_lessons = ''
    for k in days_dict.items():
        week_lessons += '\n<strong>'
        week_lessons += v.dictionary_bot[user][k[0]] + ", " + v.dictionary_bot[user][week].lower() + " "
        week_lessons += v.dictionary_bot[user]["week"].lower() + "</strong>\n\n"
        check = 0
        counter1 = 1
        for i in list_of_lists:
            if (i[4] == week or i[4] == 'both') and i[0] == k[0]:
                check += 1
                week_lessons += str(counter1) + ". "
                week_lessons += v.dictionary_bot[user]['lesson'] + ": " + i[2] + "\n"
                week_lessons += v.dictionary_bot[user]['teacher'] + ": " + i[3] + "\n"
                week_lessons += v.dictionary_bot[user]['time'] + ": " + i[1] + "\n"
                week_lessons += v.dictionary_bot[user]['link'] + ": " + i[5] + "\n\n"
                counter1 += 1
        if check == 0:
            week_lessons += v.dictionary_bot[user]["no_lessons_today"] + "\n\n"

    return week_lessons


def insert_users(user, language, name, surname, usr_id, notification, reminder, time_rem):
    users = worksheet2.col_values(1)[1:]
    if str(user) not in users:
        worksheet2.append_row([user, language, name, surname, usr_id, notification, reminder, time_rem])


def update_data(user, row, col, value):
    try:
        worksheet = sh.worksheet(str(user))
    except Exception as e:
        print(e)
        worksheet = user
    worksheet.update_cell(row, col, value)


def notif_update(user, col, value):
    row = 1
    users = worksheet2.col_values(1)[1:]
    for i in users:
        row += 1
        if i == str(user):
            break

    worksheet2.update_cell(row, col, value)


def get_notif(user, col):
    users = worksheet2.col_values(1)[1:]
    row = 1
    for i in users:
        row += 1
        if i == str(user):
            break
    return worksheet2.cell(row, col).value


def update_language_user(user, language):
    users_id = worksheet2.col_values(1)
    counter = 0

    for i in users_id:
        counter += 1
        if str(i) == str(user):
            update_data(worksheet2, counter, 2, language)


def get_user_language(user):
    user_id = worksheet2.col_values(1)
    counter = 0
    for i in user_id:
        counter += 1
        if str(i) == str(user):
            return worksheet2.cell(counter, 2).value


def add_new_lesson(user, user_step):
    worksheet = sh.worksheet(str(user))
    worksheet.append_row(user_step)


def get_users_id():
    return worksheet2.col_values(1)[1:]


def time_before_lesson(lesson_time, mytime):
    return str(datetime.strptime(lesson_time, "%H:%M") - datetime.strptime(mytime, "%H:%M"))[:-3]
