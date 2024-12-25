import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse

load_dotenv('tg.env')

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = ptbot.Bot(TG_TOKEN)

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{pbar}| {percent}% {suffix}'

def reply(chat_id, text):
    delay = parse(text)
    if delay is None:
        bot.send_message(chat_id, "Неверный формат времени. Пожалуйста, используйте формат, например, '5m' или '1h 30m'.")
        return

    msg_id = bot.send_message(chat_id, "Запускаю таймер.")
    bot.create_countdown(delay, notify, chat_id=chat_id, msg_id=msg_id, delay=delay)
    bot.create_timer(delay, time_up, chat_id=chat_id, msg_id=msg_id)

def notify(secs_left, chat_id, msg_id, delay):
    progress = render_progressbar(delay, delay - secs_left)
    message = f"Осталось {secs_left} секунд.\n{progress}"
    bot.update_message(chat_id, msg_id, message)

def time_up(chat_id, msg_id):
    bot.update_message(chat_id, msg_id, "Время пришло!")

def main():
    bot.reply_on_message(reply)
    bot.run_bot()

if __name__ == '__main__':
    main()
