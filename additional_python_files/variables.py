from additional_python_files.parsing_sheet import get_users_id


#######################################################
# DICTS ###############################################
#######################################################
# dict for user activity, to track his steps
user_step_edit_list = {}

user_step_add_list = {}

user_show_schedule = {}


def user_step_init(user):
    user_step_edit_list[user] = {"action": '', "week": '', "day": '', "lesson_num": '', "item_to_change": '',
                                 "changed_value": ''}
    user_step_add_list[user] = {"action": '', "day": '', "time": '', "lesson_name": '', "teacher": '', "week": '',
                                "link": ''}
    user_show_schedule[user] = {"action": '', "week": ''}


def user_step_edit(user, item, value):
    user_step_edit_list[user][item] = value


def user_step_add(user, item, value):
    user_step_add_list[user][item] = value


# dict with change items and their position on Google SH
def items_change_dict(val):
    try:
        k = {"lesson_name": 3, "teacher's": 4, "time": 2, "link's": 6, "week's": 5}
        return k[val]
    except Exception as e:
        print("Exception in items_change_dict", e)
        k = {"lesson_name": 3, "teacher's": 4, "time": 2, "link": 6, "week": 5}
        return k[val]


def days_dict(user):
    return {dictionary_bot[user]["monday"]: 1, dictionary_bot[user]["tuesday"]: 2, dictionary_bot[user]["wednesday"]: 3,
            dictionary_bot[user]["thursday"]: 4, dictionary_bot[user]["friday"]: 5, dictionary_bot[user]["saturday"]: 6,
            dictionary_bot[user]['sunday']: 7}


#######################################################
# LISTS ###############################################
#######################################################

def main_menu_list(user):
    return [dictionary_bot[user]["show_schedule"], dictionary_bot[user]["edit_schedule"],
            dictionary_bot[user]["settings_bot"]]


def bot_settings_list(user):
    return [dictionary_bot[user]['change_language'], dictionary_bot[user]["main_menu"]]


def edit_lesson_btn_list(user):
    return [dictionary_bot[user]["time"], dictionary_bot[user]["link's"], dictionary_bot[user]["week's"],
            dictionary_bot[user]["lesson_name"], dictionary_bot[user]["teacher's"],
            dictionary_bot[user]['back_to_lesson_choosing'], dictionary_bot[user]['main_menu']]


def edit_schedule_list(user):
    return [dictionary_bot[user]["add_lesson"], dictionary_bot[user]["edit_lesson"],
            dictionary_bot[user]["delete_lesson"], dictionary_bot[user]["main_menu"]]


def edit_lesson_list(user):
    return [dictionary_bot[user]["even"], dictionary_bot[user]["odd"], dictionary_bot[user]["both"],
            dictionary_bot[user]["back_to_edit_menu"], dictionary_bot[user]["main_menu"]]


def show_schedule_list(user):
    return [dictionary_bot[user]["even"], dictionary_bot[user]["odd"], dictionary_bot[user]["main_menu"]]


def days_list(user):
    temp_list = list(days_dict(user).keys())
    temp_list.append(dictionary_bot[user]["back_to_choosing_week"])
    temp_list.append(dictionary_bot[user]["main_menu"])
    return temp_list


def back_buttons_list():
    return ['Назад до вибору тижня', 'Назад до вибору дня']


button_list = {}  # list for creating dynamic buttons
text_list = {}
lesson_to_change = {}  # list to save nedeed rows
chat_id_list = get_users_id()  # list to determine user is new or no
week = False  # current week
lock_is = True  # var for week changing
global schedule_var, schedule_var2  # vars for schedules
lesson_today = []  # list for parsing today's lessons
dictionary_bot = {}


def get_language(user, language):
    global dictionary_bot
    if language == 'UA':
        dictionary_bot[user] = dictionary_UA
    elif language == 'RU':
        dictionary_bot[user] = dictionary_RU
    # init user_step dict
    user_step_init(user)


dictionary_UA = {
    "day": 'День',
    "enter": "Введіть",
    "save_action": 'Зберіг\nЩо далі, шеф?',
    "loading_wait..": 'Вантажу...почекайте, нічого не клацайте!!!',
    "choose_lan": 'Оберіть мову:',
    "main_menu": 'Головне меню',
    "choose_what_edit": 'Оберіть, що необхідно редагувати: ',
    "choose_week": 'Оберіть тиждень:',
    "choose_day": 'Оберіть день:',
    "lesson": 'Пара',
    "plural_lesson": 'Пари',
    "your_schedule": 'Ваш розклад',
    "show_schedule": 'Показати розклад',
    "edit_schedule": 'Редагувати розклад',
    "edit_lesson": 'Редагувати пару',
    "add_lesson": 'Додати пару',
    "delete_lesson": 'Видалити пару',
    "delete_this_lesson": 'Видалити цю пару',
    "settings_bot": 'Налаштування бота',
    "change_language": 'Змінити мову',
    "odd": 'Непарний',
    "even": 'Парний',
    "both": 'Обидва',
    "back_to_edit_menu": 'Назад в меню редагування',
    "lesson_name": 'Назву пари',
    "teacher": 'Викладач',
    "teacher's": 'Викладача',
    "time": 'Час',
    "link": 'Посилання',
    "link's": 'Посилання',
    "link_short": 'лінк',
    "week": 'Тиждень',
    "week's": 'Тиждень',
    'monday': 'Понеділок',
    "tuesday": 'Вівторок',
    "wednesday": 'Середа',
    "thursday": 'Четвер',
    "friday": "П'ятниця",
    "saturday": 'Субота',
    "sunday": 'Неділя',
    "back_to_choosing_week": 'Назад до вибору тижня',
    "choose_lesson_num_to_change": 'Оберіть номер пари, яку необхідно редагувати: ',
    "choose_lesson_num_to_delete": 'Оберіть номер пари, яку необхідно видалити: ',
    "no_lessons_today": 'В цей день немає пар',
    "back_to_day_choosing": 'Назад до вибору дня',
    "back_to_lesson_choosing": 'Назад до вибору пари',
    "save": 'Зберегти',
    "save_add_lesson": 'Натисніть кнопку "Зберегти" для збереження нової пари',
    "press_save_edit": 'Натисніть конпку "Зберегти" для збереження змін',
    "tech_changes": 'Сталися технічні зміни\nПоверніться до головного меню або перезапустіть бот',
    "yes": "Так",
    "no": "Ні",
    "are_you_sure_to_del_lesson": "Ви впевнені, що хочете видалити пару",
    "enter_time_add": 'Введіть час пари, наприклад: "13:15"',
    "enter_correct_time": 'Введіть час правильно! Наприклад, "14:10"',
    "enter_correct_link": 'Введіть коректне посилання!\nНаприклад, "https://google.com"'
}

dictionary_RU = {
    "day": 'День',
    "enter": "Введите",
    "save_action": 'Сохранил\nЧто дальше, шеф?',
    "loading_wait..": 'Загружаю...погодите, ничего не клацайте!!!',
    "choose_lan": 'Выберите язык:',
    "main_menu": 'Главное меню',
    "choose_what_edit": 'Выберите, что необходимо редактировать:',
    "choose_week": 'Выберите неделю:',
    "choose_day": 'Выберите день:',
    "lesson": 'Пара',
    "plural_lesson": 'Пары',
    "your_schedule": 'Ваше расписание',
    "show_schedule": 'Показать расписание',
    "edit_schedule": 'Редактировать расписание',
    "edit_lesson": 'Редактировать пару',
    "add_lesson": 'Добавить пару',
    "delete_lesson": 'Удалить пару',
    "delete_this_lesson": 'Удалить эту пару',
    "settings_bot": 'Настройки бота',
    "change_language": 'Изменить язык',
    "odd": 'Нечетная',
    "even": 'Четная',
    "both": 'Обе',
    "back_to_edit_menu": 'Назад в меню редактирования',
    "lesson_name": 'Название пары',
    "teacher": 'Преподаватель',
    "teacher's": 'Преподавателя',
    "time": 'Время',
    "link": 'Ссылка',
    "link's": 'Ссылку',
    "link_short": 'вжух',
    "week": 'Неделя',
    "week's": 'Неделю',
    'monday': 'Понедельник',
    "tuesday": 'Вторник',
    "wednesday": 'Среда',
    "thursday": 'Четверг',
    "friday": "Пятница",
    "saturday": 'Суббота',
    "sunday": 'Воскресенье',
    "back_to_choosing_week": 'Назад к выбору недели',
    "choose_lesson_num_to_change": 'Выберите номер пары, которую необходимо редактировать: ',
    "no_lessons_today": 'В этот день нет пар',
    "back_to_day_choosing": 'Назад к выбору дня',
    "back_to_lesson_choosing": 'Назад к выбору пары',
    "save": 'Сохранить',
    "save_add_lesson": 'Нажмите кнопку "Сохранить" для сохранения новой пары',
    "press_save_edit": 'Нажмите конпку "Сохранить" для сохранения изменений',
    "tech_changes": 'Произошли технические изменения\nВернитесь в главное меню или перезапустите бот',
    "yes": "Да",
    "no": "Нет",
    "are_you_sure_to_del_lesson": "Вы уверены, что хотите удалить пару",
    "enter_time_add": 'Введите время пары, например: "13:15"',
    "enter_correct_time": 'Введите время правильно! Например, "14:10"',
    "enter_correct_link": 'Введите корректную ссылку!\nНапример, "https://google.com"'
}
