import telebot
from pytube import YouTube
from moviepy.editor import *
import tempfile

API_KEY = 'your api key'

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome!")


@bot.message_handler(commands=['merge_videos'])
def merge_videos(message):
    urls = message.text.split()[1:]
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
