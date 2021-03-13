import telebot
from telebot import types

bot = telebot.TeleBot('1642275922:AAHxeYvKI821oXHIaD2D0XiSra9goFiqNQ4')

@bot.message_handler(commands=["start"])
def inline(massege):
  mainmenu = types.InlineKeyboardMarkup()
  catalog = types.InlineKeyboardButton(text="Каталог", callback_data="Catalog")
  help = types.InlineKeyboardButton(text="Поддержка", callback_data="help")
  mainmenu.add(catalog, help,)
  bot.send_message(massege.chat.id, "ВЫБЕРИТЕ КНОПКУ", reply_markup=mainmenu)


@bot.callback_query_handler(func=lambda a:True)
def inline_a(a):
    if a.data == 'Catalog':
        bot.send_message(a.message.chat.id, 'Это кнопка 1')
    elif a.data == 'help':
        menuhelp = types.InlineKeyboardMarkup()
        helper = types.InlineKeyboardButton(text="Связь с нами", callback_data="helper")
        backinmainmenu = types.InlineKeyboardButton(text="Назад", callback_data="backinmainmenu")
        menuhelp.add(helper, backinmainmenu)
        bot.send_message(a.message.chat.id, 'Выбирите действие', reply_markup=menuhelp)
    elif a.data == "helper":
        bot.send_message(a.message.chat.id, 'Это кнопка 2')
    elif a.data == 'backinmainmenu':
        return inline(a.message)

bot.polling()