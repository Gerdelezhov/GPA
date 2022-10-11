import telebot
from telebot import types
import time
import script

with open('token.txt') as f:
    token = f.readline()
f.close()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Справка по МЛТА")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привет! Ты попал в основное меню.")
    bot.send_message(message.chat.id, "Выбери то, что тебя интересует".format(
        message.from_user), reply_markup=markup)

@bot.message_handler(commands=['Справка по МЛТА'])
def mlta(message):
    script.mlta_script()
    f = open(r"message.txt", "r")
    for line in f:
        bot.send_message(message.chat.id, line)
        time.sleep(1)
    f.close()

@bot.message_handler(content_types=['text'])
def check_command(message):
    if (message.text == "Справка по МЛТА"):
        mlta(message)

bot.infinity_polling()
