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
sys.stderr.flush()

load_dotenv()
TOKEN = os.getenv("BASSLEAD_BOT_TOKEN")

bot = Bot(token=BASSLEAD_BOT_TOKEN)
dp=Dispatcher()

# обработка кнопки старт
@dp.message(Command("start"))
async def start_command(message:types.Message):
    logging.info("команда start от пользователя {message.from_user.id}")

    buttons = [
    [InlineKeyboardButton(text="🎸Bass",callback_data="mode:bass")] 
    [InlineKeyboardButton(text="🎹Lead",callback_data="mode:lead")] 
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Привет! Это генератор bass/lead партий для техно.\n"
    "Выбери режим:", 
    reply_markup=keyboard,)

#дальше идет обработка нажатия режима бас лид

@dp.callback_query(lambda c:)
