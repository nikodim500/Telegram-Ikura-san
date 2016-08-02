# -*- coding: utf-8 -*-
#
# import telebot
# #import os
# #from flask import Flask
#
# #app = Flask(__name__)
# token = '225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A'
#
# bot = telebot.TeleBot(token)
#
# @bot.message_handler(content_types=["text"])
# def response_text(message):
#     if (message.text == 'сдохни') or (message.text == 'die'):
#         bot.send_message(message.chat.id, '[хокку и сеппуку')
#         raise RuntimeError('User aborted operation')
#     if (message.text == 'икура'):
#         bot.send_message(message.chat.id, 'чо?')
#     else:
#         bot.send_message(message.chat.id, message.text)
#
# if __name__ == '__main__':
#     bot.polling(none_stop=True)
# #    port = int(os.environ.get("PORT", 5000))
# #    app.run(host='0.0.0.0', port=port)


import telebot
import os
from flask import Flask, request

bot = telebot.TeleBot('225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A')

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

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
    bot.set_webhook(url="https://ikurabot.herokuapp.com")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

