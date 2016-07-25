# -*- coding: utf-8 -*-

import telebot
#import os
#from flask import Flask

#app = Flask(__name__)
token = '225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A'

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def response_text(message):
    if (message.text == 'сдохни') or (message.text == 'die'):
        bot.send_message(message.chat.id, '[хокку и сеппуку')
        raise RuntimeError('User aborted operation')
    if (message.text == 'икура'):
        bot.send_message(message.chat.id, 'чо?')
    else:
        bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port)




