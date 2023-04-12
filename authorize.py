from decouple import config
import telebot

API_KEY = 'your api key'
PASSWORD = config('PASSWORD')

bot = telebot.TeleBot(API_KEY)


def is_authorized(chat_id, password):
    if password == PASSWORD:
        return True
    else:
        bot.send_message(chat_id, "Authentication failed. Please try again.")
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_authorized(message.chat.id, message.text.split()[1]):
        bot.reply_to(message, "Welcome!")


@bot.message_handler(commands=['merge_videos'])
def merge_videos(message):
    if not is_authorized(message.chat.id, message.text.split()[1]):
        return
    urls = message.text.split()[2:]
    if len(urls) == 0:
        bot.send_message(message.chat.id, "Please provide at least one URL")
        return
    if len(urls) > 10:
        bot.send_message(message.chat.id, "You can only merge up to 10 videos at a time")
        return
    # rest of the code...


bot.polling()
