import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BufferedInputFile
from dotenv import load_dotenv
import os
from main_basslead import generate_bass, generate_lead
import random

logging.basicConfig(level=logging.DEBUG,
format="%(asctime)s - %(levelname)s - %(message)s")

print("DEBUG: bot_basslead.py начал выполняться", file=sys.stderr)
sys.stderr.flush()

load_dotenv()
TOKEN = os.getenv("BASSLEAD_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp=Dispatcher()

NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
SCALES = ["minor","major","frig","dor"]

user_state={}

# обработка кнопки старт
@dp.message(Command("start"))
async def start_command(message:types.Message):
    logging.info(f"команда start от пользователя {message.from_user.id}")

    buttons = [
        [
    InlineKeyboardButton(text="🎸Bass",callback_data="mode:bass"), 
    InlineKeyboardButton(text="🎹Lead",callback_data="mode:lead"), 
    ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Привет! Это генератор bass/lead партий для техно.\n"
    "Выбери режим:", 
    reply_markup=keyboard,)

#дальше идет обработка нажатия режима бас лид

@dp.callback_query(lambda c:c.data.startswith("mode:"))
async def process_mode(callback_query: CallbackQuery):
    await callback_query.answer()

    mode = callback_query.data.split(":")[1] 
    user_id = callback_query.from_user.id

    user_state[user_id] = {
        "mode":mode,
        "note_idx":0,
        "scale_idx":0
    }
    logging.info(f"Пользователь {user_id} выбрал режим {mode}")

    buttons = [
        [
        InlineKeyboardButton(text="Нота:{notes[0]}",callback_data="toggle_note"),
        InlineKeyboardButton(text="Лад^{scale[0]}",callback_data="toggle_scale"),
    ],
    [InlineKeyboardButton(text="🎲Сгенерировать паттерн",callback_data="generate")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = (
        f"Режим: {mode.capitalize()}\n"
        f"Нота: {NOTES[0]}\n"
        f"Лад: {SCALES[0]}"
    )

    await callback_query.message.answer(text, reply_markup=keyboard)


async def main():
    try:
        await dp.start_polling(bot)
    except Exception:
        logging.exception("Ошибка при запуске бота")


if __name__ == "__main__":
    print("Бот запускается")
    asyncio.run(main())
