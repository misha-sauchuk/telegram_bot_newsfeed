#!/usr/bin/env python

import requests
import telebot
from telebot.types import Message
import vk_api
import configparser


# Read the settings data from settings.ini
config = configparser.ConfigParser()
config.read('settings.ini')
LOGIN = config.get('VK', 'login')
PASSWORD = config.get('VK', 'password')
VK_GR_ID = config.get('VK', 'group_id')
COUNT = config.get('VK', 'count')
TOKEN = config.get('Telegram', 'token')

# Bot initial
bot = telebot.TeleBot(TOKEN)


# Get the data from vk.com
def get_data(vk_id, count):
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth()
    vk = vk_session.get_api()
    response = vk.newsfeed.get(source_ids=vk_id, count=count)
    return response


# Create a commands to control the bot
@bot.message_handler(commands=['start', 'feed'])
def command_holder(message: Message):

    if message.text == '/start':
        text_start = 'Привет. Я новостной бот портала tut.by'
        bot.reply_to(message, text_start)

    if message.text == '/feed':
        response = get_data(VK_GR_ID, COUNT)
        response = reversed(response['items'])

        count = 11 # will shaw the news number: 1 - is the last one news
        for post in response:
            count -=1
            # use block Try/Except if there is a picture or video
            try:
                text = 'NEWS #{}\n{}'.format(count, post['text'])
            except:
                text = 'NEWS #{} is missing'.format(count)
            bot.reply_to(message, text)


# Bot can answer for if some one will say hello to him
@bot.message_handler(content_types=['text'])
def echo_digits(message: Message):
    if 'Привет' in message.text:
        bot.reply_to(message, 'Добрый день! Командуйте мной!')
        return


bot.polling(timeout=60)
