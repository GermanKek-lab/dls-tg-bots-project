import telebot
import os
import logging
import warnings
from config import TOKEN
warnings.filterwarnings("ignore")


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to("Привет!")


@bot.message_handler(commands=['convert'])
def send_convert(message):
    bot.reply_to(message, 'This is my convert function')
    bot.register_next_step_handler(message, get_photo)

def get_photo(message):
    if message.photo is None:
        return
    if not os.path.isdir("user_files"):
        os.mkdir("photo")
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = f"photo/photo_{str(message.chat.id)}.jpg"
    with open(path, 'wb') as file:
        file.write(downloaded_file)
    bot.reply_to(message, "Отправьте стиль")
    bot.register_next_step_handler(message, get_style)

def get_style(message):
    if message.phot is None:
        return
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = f"photo/style_{str(message.chat.id)}.jpg"
    with open(path, 'wb') as file:
        file.write(downloaded_file)

    bot.send_message(message.chat.id, "Начинается обработка...")



if __name__ == '__main__':
    try:
        bot.polling(non_stop=True)
    except Exception as ex:
        if not isinstance(ex, telebot.apihelper.ApiTelegramException):
            logging.error(ex, exc_info=True)