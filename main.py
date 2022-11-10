#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import script

my_id = 667772448

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


@bot.message_handler(content_types=['text'])
def check_command(message):
    if (message.text == "Справка по МЛТА"):
        mlta(message)


bot.infinity_polling()
