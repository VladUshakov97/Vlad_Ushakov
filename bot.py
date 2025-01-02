import os
from dotenv import load_dotenv
from pytimeparse import parse
import ptbot

TG_ENV_FILE = 'tg.env'

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    progress_bar = fill * filled_length + zfill * (length - filled_length)
    return f'{prefix} |{progress_bar}| {percent}% {suffix}'


def reply(chat_id, text):
    delay = parse(text)
    message_id = bot.send_message(chat_id, "Запускаю таймер.")
    bot.create_countdown(delay, notify, chat_id=chat_id, message_id=message_id, delay=delay)
    bot.create_timer(delay, time_up, chat_id=chat_id, message_id=message_id)


def notify(seconds_left, chat_id, message_id, delay):
    progress = render_progressbar(delay, delay - seconds_left)
    message = f"Осталось {seconds_left} секунд.\n{progress}"
    bot.update_message(chat_id, message_id, message)


def time_up(chat_id, message_id):
    bot.update_message(chat_id, message_id, "Время пришло!")


def main():
    load_dotenv(TG_ENV_FILE)
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    global bot
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply)
    bot.run_bot()


if __name__ == '__main__':
    main()
