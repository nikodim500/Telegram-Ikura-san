# -*- coding: utf-8 -*-
#
import sys
print (sys.version)

import telebot
import os
import psycopg2
try:
    import urllib.parse
except:
    import urlparse

import talkzload

from flask import Flask, request

bot = telebot.TeleBot('225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A')

server = Flask(__name__)


#urllib.uses_netloc.append("postgres")
print(os.environ["DATABASE_URL"])
url = urlparse(os.environ["DATABASE_URL"])
print(url)

def db_init():
    # Создаём соединение
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    # Курсор - исполнитель команд на языке SQl для нашей бд
    cursor = connection.cursor()
    # Создаём табоицу, если её нет
    cursor.execute('''CREATE TABLE IF NOT EXISTS talkz
        (talk VARCHAR(250) PRIMARY KEY NOT NULL);''')
    # Сохраняем изменения и закрываем базу
    connection.commit()
    return connection


# Запись в базу данных
def writedb(talkz_collection):
    # Получаем соединение
    conn = db_init()
    # Курсор
    cursor = conn.cursor()

    for t in talkz_collection:
        # Пробуем обновить данные. Если ошибка, то создадим запись
        cursor.execute(
            '''INSERT INTO talkz (talk) VALUES (%s);'''
            % (t)
        )
        # Завершаем операцию, сохраняем
        conn.commit()
    # Сохраняем изменения
    conn.commit()
    conn.close()  # Закрываем соединение


# Чтение из базы
def readdb():
    # Получаем соединение
    conn = db_init()
    # Курсор
    cursor = conn.cursor()
    # Читаем базу
    response = cursor.execute('''SELECT talk FROM talkz;''')
    talkz_collection = cursor.fetchall()
    # Закрываем соединение
    conn.close()
    # Возвращаем данные
    return talkz_collection

#talkz = readdb()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['reload'])
def start(message):
    writedb(talkzload.talkz)
    bot.reply_to(message, 'Talkz reloaded')

@bot.message_handler(func=lambda message: message.text == u"икура")
def command_text_ikura(m):
    bot.send_message(m.chat.id, "Ну чево тебе? " + str(m.chat.id))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://ikurainline.herokuapp.com/bot")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

