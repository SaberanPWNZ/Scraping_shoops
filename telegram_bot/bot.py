
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from telegram_bot.comands_handlers import command_router
from telegram_bot.handlers import user_router
from telegram_bot.midlleware import AdminOnlyMiddleware

load_dotenv()

token = os.getenv(key='BOT_TOKEN_TEST')
bot = Bot(token=token)
dp = Dispatcher(bot=bot)
dp.include_router(user_router)
dp.include_router(command_router)

#  204071671
dp.update.middleware(AdminOnlyMiddleware(admin_ids=[204071671]))
logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot, skip_updates=True)


