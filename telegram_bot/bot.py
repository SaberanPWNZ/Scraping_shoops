import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from django.core.management import BaseCommand

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot=bot)


#  204071671

class MessageSender:
    bot_token = token
    bot = Bot(token=bot_token)
    recipient_id = '2325008174'

    def get_token(self):
        return self.bot_token

    def get_recipient_id(self):
        return self.recipient_id

    @classmethod
    async def send_telegram_message(cls, message):
        try:
            await cls.bot.send_message(chat_id='2325008174', text=message)
            logging.info(f"Сообщение отправлено: {message}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
#

TOKEN = os.getenv("BOT_TOKEN_TEST")



# Создание объекта бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def start_bot():
    logging.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(start_bot())
