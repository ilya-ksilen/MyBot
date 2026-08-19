import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InLineKeyboardMarkup, InLineKeyboardButton
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

#обработка команды start
@dp.message(Command("start"))
async def start_command(message:types.Message):
    button = InLineKeyboardButton(text="Сгенерировать паттерн", callback_data="generate")
    keyboard = InLineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("Привет! Жми кнопку, сгенерируем драмку.", reply_markup=keyboard)

#обработка нажатия кнопки
@dp.callback_query(lambda c: c.data="generate"
async def process_generate(callback_query: CallbackQuery):
    await callback_query.answer()

    loop = generate_random_loop(steps=16)
    viz = visualize_loop(loop)

    await callback_query.message.answer("Сгенерированный паттерн:\n\n{viz}")

    #запуск бота
    async def main():
        await dp.start_polling(bot)
        if __name__ == "__name__":
            asyncio.run(main())
