import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BufferedInputFile
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.DEBUG,
format="%(asctime)s - %(levelname)s - %(message)s")

print("DEBUG: bot_basslead.py начал выполняться", file=sys.stderr)

load_dotenv()
TOKEN = os.getenv("BASSLEAD_BOT_TOKEN")
bot = Bot(token=BASSLEAD_BOT_TOKEN)
dp=Dispatcher()

# обработка кнопки старт
@dp.message(Command("start"))
async def start_command(message:types.Message):
    logging.info("команда start от пользователя {message.from_user.id}")

    buttons = [
        # здесь кнопки режимов надо выбрать Бас, Лид
    ]
    