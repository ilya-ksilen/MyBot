import sys
print('DEBUG: bot_drum начал выполняться', file=sys.stderr)
sys.stderr.flush()
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.types import BufferedInputFile
from dotenv import load_dotenv
import os
from main_drum import generate_random_loop, visualize_loop_image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s- %(levelname)s - %(message)s')

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

#обработка команды start
@dp.message(Command("start"))
async def start_command(message:types.Message):
    button = InlineKeyboardButton(text="Сгенерировать паттерн", callback_data="generate")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Привет! Жми кнопку, сгенерируем драмку.", reply_markup=keyboard)

#обработка нажатия кнопки
@dp.callback_query(lambda c: c.data =="generate")
async def process_generate(callback_query: CallbackQuery):
    await callback_query.answer()
    try:
        loop = generate_random_loop(steps=16)
        image_buffer = visualize_loop_image(loop)
        await callback_query.message.answer_photo(photo=BufferedInputFile(image_buffer.getvalue(), filename="pattern.png"),caption="Сгенерированный паттерн")
    except Exception as e:
        logging.exception("Ошибка при генерации паттерна")
        await callback_query.message.answer("Произошла ошибка при генерации")

#запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception("Ошибка при запуске бота")
if __name__ == "__main__":
    print ("Бот запускается")
    asyncio.run(main())

