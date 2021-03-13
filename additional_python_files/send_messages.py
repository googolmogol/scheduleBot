import additional_python_files.variables as v


def simple_message(bot, message, markup):
    bot.send_message(message.chat.id, message.text, parse_mode="HTML", reply_markup=markup)


def message_with_text(bot, message, text, markup):
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)


def show_schedule(bot, message):
    user = message.chat.id
    img = open('restfiles/schedule.jpg', 'rb')
    bot.send_photo(message.chat.id, img, "<strong>" + v.dictionary_bot[user]['your_schedule'] + "</strong>",
                   parse_mode="HTML")


