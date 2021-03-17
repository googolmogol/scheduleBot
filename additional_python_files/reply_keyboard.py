import telebot


def get_reply_markup(resize, onetime):
    return telebot.types.ReplyKeyboardMarkup(resize, onetime)


# creating inline buttons
def inline_button_url(text, url):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=text, url=url)
    markup.add(button)
    return markup


def inline_button_callback(list_btn, btn_count):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = []
    keys = list(list_btn.keys())
    for i in keys:
        btn.append(telebot.types.InlineKeyboardButton(text=i, callback_data=list_btn[i]))
    return few_btn_row(markup, btn, 0, btn_count)


def simple_keyboard(resize, hide, count_btn, count_btn_in_row, list_btns):
    return few_btn_row(get_reply_markup(resize, hide), list_btns, count_btn, count_btn_in_row)


# function which creates few reply buttons in the row (max - 3)
def few_btn_row(markup, btn_list, count_btns, count_btn_in_row):
    length = len(btn_list) - count_btns  # buttons that don't use this fun
    if count_btn_in_row == 3:
        if length >= 3:
            length2 = length % 3
            if length2 == 0:
                for i in range(0, length, 3):
                    markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
            elif length2 == 1:
                for i in range(0, length - 1, 3):
                    markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
                markup.add(btn_list[length - 1])
            elif length2 == 2:
                for i in range(0, length - 2, 3):
                    markup.add(btn_list[i], btn_list[i+1], btn_list[i+2])
                markup.add(btn_list[length-2], btn_list[length-1])
        elif length == 2:
            markup.add(btn_list[0], btn_list[1])
        elif length == 1:
            markup.add(btn_list[0])
    elif count_btn_in_row == 2:
        if length >= 2:
            length2 = length % 2
            if length2 == 0:
                for i in range(0, length, 2):
                    markup.add(btn_list[i], btn_list[i+1])
            elif length2 == 1:
                for i in range(0, length - 1, 2):
                    markup.add(btn_list[i], btn_list[i+1])
                markup.add(btn_list[length - 1])
        elif length == 1:
            markup.add(btn_list[0])
    if count_btns != 0:
        markup.add(btn_list[-2], btn_list[-1])
    return markup
