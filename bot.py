import telebot
from pytube import YouTube
from moviepy.editor import *
import tempfile

API_KEY = 'your api key'

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_merge_videos = telebot.types.KeyboardButton('Merge Videos')
    markup.add(button_merge_videos)
    bot.reply_to(message, "Welcome to my bot!", reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text == 'Merge Videos':
        bot.send_message(message.chat.id, "Please enter the links of the videos you want to merge, separated by space")
    else:
        bot.send_message(message.chat.id, 'Invalid command')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def merge_videos(message):
    urls = message.text.split()
    if len(urls) == 0:
        bot.send_message(message.chat.id, "Please provide at least one URL")
        return
    if len(urls) > 10:
        bot.send_message(message.chat.id, "You can only merge up to 10 videos at a time")
        return
    files = []
    for url in urls:
        try:
            yt = YouTube(url)
            filename = f"{yt.title}.mp4"
            stream = yt.streams.filter(adaptive=True, file_extension="mp4").first()
            stream.download(output_path="./downloads", filename=filename)
            files.append(filename)
        except:
            bot.send_message(message.chat.id, f"Failed to download {url}")
    clips = [VideoFileClip(file) for file in files]
    final_clip = concatenate_videoclips(clips)
    with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
        final_clip.write_videofile(tmp.name, codec='libx264')
        tmp.seek(0)
        bot.send_video(message.chat.id, tmp, timeout=1000)
    for file in files:
        os.remove(file)


bot.polling()
