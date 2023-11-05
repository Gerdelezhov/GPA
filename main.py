#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import script
import schedule


my_id = #ID

with open('token.txt') as f:
    token = f.readline()
f.close()

bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: message.chat.id != my_id)
def some(message):
    bot.send_message(message.chat.id, "Доступ для вас Закрыт")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Ты попал в основное меню.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Справка по МЛТА")
    markup.add(item1)

    bot.send_message(message.chat.id, "Выбери то, что тебя интересует".format(
        message.from_user), reply_markup=markup)


def mlta(message):
    text = script.mlta_script()
    bot.send_message(message.chat.id, text)

def rgr():
    new_m = script.new_mark()
    if(new_m != 35):
        rgr = new_m - 35
        if(rgr < 12):
            bot.send_message(my_id, "РГР проверено\nНе сдал: " + str(rgr))
        elif(rgr < 15):
            bot.send_message(my_id, "РГР проверено\nРГР сдано, но нехватило баллов на автомат: " + str(rgr))
        else:
            bot.send_message(my_id, "РГР проверено\nВсё в порядке: " + str(rgr))



schedule.every(10).seconds.do(rgr)

@bot.message_handler(content_types=['text'])
def check_command(message):
    if (message.text == "Справка по МЛТА"):
        mlta(message)

    if (message.text == "Старт парсинга"):
        bot.send_message(my_id, "Выполняю")
        while(1):
            schedule.run_pending()

bot.infinity_polling()
