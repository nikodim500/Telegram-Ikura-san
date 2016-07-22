# -*- coding: utf-8 -*-

import telebot

token = '225635767:AAGEvQKd4Cj8wNN24wM5hpd8FlgiJPmky0A'

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def response_text(message):
    print(message)
    if (message.text == 'сдохни') or (message.text == 'die'):
        bot.send_message(message.chat.id, '[хокку и сеппуку')
        print('Aborted')
        raise RuntimeError('User aborted operation')
    if (message.text == 'икура'):
        bot.send_message(message.chat.id, 'чо?')
    else:
        bot.send_message(message.chat.id, message.text)

print('Starting')
if __name__ == '__main__':
     bot.polling(none_stop=True)