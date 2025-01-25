import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher
from django.core.management import BaseCommand

from dotenv import load_dotenv

from scraper.celery_config import app
from telegram_bot.comands_handlers import command_router

load_dotenv()

if os.getenv('TELEGRAM_BOT_PRODUCTION') == 'prod':
    token = os.getenv('BOT_TOKEN')
else:
    token = os.getenv('BOT_TOKEN_TEST')

bot = Bot(token=token)
dp = Dispatcher(bot=bot)
dp.include_router(command_router)
logging.basicConfig(level=logging.INFO)
TELEGRAM_API_URL = f"https://api.telegram.org/bot{token}/sendMessage"

#  204071671


@app.task()
def send_telegram_message_task(message):
    #"204071671"
    try:
        payload = {
            'chat_id': '-1002325008174',
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(TELEGRAM_API_URL, data=payload)

        if response.status_code == 200:
            logging.info(f"message send: {message}")
        else:
            logging.error(f"Error message sending. Статус код: {response.status_code}")
    except Exception as e:
        logging.error(f"problem with message sending : {e}")


async def start_bot():
    logging.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(start_bot())
