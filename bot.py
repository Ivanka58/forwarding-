Вот обновлённый код с добавлением команды /stop и исправлением обработки альбомов фотографий:

Файл bot.py:
import os
from dotenv import load_dotenv
import telebot
import time

# Загрузка переменных среды из .env-файла
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PASSWORD = os.getenv('BOT_PASSWORD')
CHANNEL_ID = int(os.getenv('TELEGRAM_CHANNEL_ID'))

bot = telebot.TeleBot(TOKEN)

# Переменная для хранения объявления
announcement = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Введи пароль')

@bot.message_handler(commands=['stop'])
def stop_announcement(message):
    global announcement
    announcement = None
    bot.reply_to(message, 'Объявление отменено!\nОтправь новое сообщение которое я буду пересылать')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if not hasattr(bot, 'authorized'):
        if message.text == PASSWORD:
            bot.authorized = True
            bot.reply_to(message, 'Привет! Отправь мне объявление и я буду присылать его в твой канал каждые 7 объявлений')
        else:
            bot.reply_to(message, 'Пароль неверный, доступ закрыт.')
    elif getattr(bot, 'authorized', False):
        if message.content_type == 'text':
            global announcement
            announcement = message.text
            bot.reply_to(message, 'Спасибо! Это объявление будет публиковаться в канале с перерывом в 7 сообщений, если возникнут проблемы, пиши @Ivanka58')
        elif message.content_type == 'photo':
            global announcement
            announcement = message
            bot.reply_to(message, 'Спасибо! Это объявление будет публиковаться в канале с перерывом в 7 сообщений, если возникнут проблемы, пиши @Ivanka58')
        elif message.content_type == 'media_group':
            global announcement
            announcement = message
            bot.reply_to(message, 'Спасибо! Это объявление будет публиковаться в канале с перерывом в 7 сообщений, если возникнут проблемы, пиши @Ivanka58')

# Обработчик сообщений в канале
@bot.message_handler(chat_types=['channel'], content_types=['text', 'photo'])
def handle_channel_message(message):
    if message.chat.id == CHANNEL_ID:
        global announcement
        if announcement:
            if message.content_type == 'text':
                # Считаем сообщения в канале
                if hasattr(bot, 'message_count'):
                    bot.message_count += 1
                else:
                    bot.message_count = 1
                if bot.message_count % 7 == 0:
                    # Пересылаем объявление в канал
                    if announcement.content_type == 'text':
                        bot.send_message(CHANNEL_ID, announcement.text)
                    elif announcement.content_type == 'photo':
                        bot.send_photo(CHANNEL_ID, announcement.photo[-1].file_id, caption=announcement.caption)
                    elif announcement.content_type == 'media_group':
                        for photo in announcement.media_group:
                            bot.send_photo(CHANNEL_ID, photo.file_id, caption=announcement.caption)
                    bot.message_count = 0
            elif message.content_type == 'photo':
                # Считаем сообщения в канале
                if hasattr(bot, 'message_count'):
                    bot.message_count += 1
                else:
                    bot.message_count = 1
                if bot.message_count % 7 == 0:
                    # Пересылаем объявление в канал
                    if announcement.content_type == 'text':
                        bot.send_message(CHANNEL_ID, announcement.text)
                    elif announcement.content_type == 'photo':
                        bot.send_photo(CHANNEL_ID, announcement.photo[-1].file_id, caption=announcement.caption)
                    elif announcement.content_type == 'media_group':
                        for photo in announcement.media_group:
                            bot.send_photo(CHANNEL_ID, photo.file_id, caption=announcement.caption)
                    bot.message_count = 0

if __name__ == "__main__":
    bot.polling(none_stop=True)
