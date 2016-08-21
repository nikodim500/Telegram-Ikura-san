# -*- coding: utf-8 -*-
#
from random import random

import telebot
import os
import psycopg2
from telebot import types

try:
    import urllib.parse
except:
    import urlparse

import talkzload

from flask import Flask, request

bot = telebot.TeleBot('225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A')

server = Flask(__name__)


#urllib.uses_netloc.append("postgres")
# print(os.environ["DATABASE_URL"])
# url = urlparse(os.environ["DATABASE_URL"])
# print(url)
#
# def db_init():
#     # Создаём соединение
#     connection = psycopg2.connect(
#         database=url.path[1:],
#         user=url.username,
#         password=url.password,
#         host=url.hostname,
#         port=url.port
#     )
#     # Курсор - исполнитель команд на языке SQl для нашей бд
#     cursor = connection.cursor()
#     # Создаём табоицу, если её нет
#     cursor.execute('''CREATE TABLE IF NOT EXISTS talkz
#         (talk VARCHAR(250) PRIMARY KEY NOT NULL);''')
#     # Сохраняем изменения и закрываем базу
#     connection.commit()
#     return connection
#
#
# # Запись в базу данных
# def writedb(talkz_collection):
#     # Получаем соединение
#     conn = db_init()
#     # Курсор
#     cursor = conn.cursor()
#
#     for t in talkz_collection:
#         # Пробуем обновить данные. Если ошибка, то создадим запись
#         cursor.execute(
#             '''INSERT INTO talkz (talk) VALUES (%s);'''
#             % (t)
#         )
#         # Завершаем операцию, сохраняем
#         conn.commit()
#     # Сохраняем изменения
#     conn.commit()
#     conn.close()  # Закрываем соединение
#
#
# # Чтение из базы
# def readdb():
#     # Получаем соединение
#     conn = db_init()
#     # Курсор
#     cursor = conn.cursor()
#     # Читаем базу
#     response = cursor.execute('''SELECT talk FROM talkz;''')
#     talkz_collection = cursor.fetchall()
#     # Закрываем соединение
#     conn.close()
#     # Возвращаем данные
#     return talkz_collection

#talkz = readdb()

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    print("inline")
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['reload'])
def start(message):
#    writedb(talkzload.talkz)
    bot.reply_to(message, 'Talkz reloaded')

@bot.message_handler(func=lambda message: message.text == u"икура")
def command_text_ikura(message):
    #bot.send_message(m.chat.id, talkzload.talkz[random.randrange(len(talkzload.talkz))])
    print("икура")
    bot.send_message(message.chat.id, "Ну чево тебе?")
    l = len(talkzload.talkz)
    print("l = " + str(l))
    #i = random.randint(0, l)
    #print(i)
    r = random.choice(talkzload.talkz)#talkzload.talkz[i]
    print(r)
    bot.send_message(message.chat.id, r)

@bot.message_handler(func=lambda message: message.text == "ikura")
def command_text_ikuraeng(m):
    #bot.send_message(m.chat.id, talkzload.talkz[random.randrange(len(talkzload.talkz))])
    print("ikura")
    try:
        bot.send_message(m.chat.id, talkzload.talkz[random.randint(1, len(talkzload.talkz))])
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    for s in talkzload.talkz:
        if message.text in s:
            print(s)
    bot.send_message(message.chat.id, "\n".join(s for s in talkzload.talkz if message.text in s))
    #bot.reply_to(message, message.text)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://ikurabot.herokuapp.com/bot")
    return "Hooked!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

