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
    logging.info(f"Команда /start от пользователя {message.from_user.id}")

    buttons = [
        [InlineKeyboardButton(text="🌆 Detroit", callback_data="style:detroit")],
        [InlineKeyboardButton(text="🏭 Industrial", callback_data="style:industrial")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    # button = InlineKeyboardButton(text="Сгенерировать паттерн", callback_data="generate") старый вариант с одной кнопкой
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer("👋Привет! Выбери стиль и после жми сгенерировать.", reply_markup=keyboard)

#обработка нажатия кнопки
@dp.callback_query(lambda c: c.data.startswitch("style:"))
async def process_style(callback_query: CallbackQuery):
    await callback_query.answer()
    style = callback_query.data.split(":")[1]

    logging.info(f"Пользователь {callback_query.from_user.id} выбрал стиль {style}")

    button = InlineKeyboardButton(text = "🎲 Сгенерировать паттерн", callback_data=f"generate{style}")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    await callback_query,message.answer(
        f"Стиль: {style}. Жми кнопку!",
        reply_markup=keyboard
    )

    # try:
    #     loop = generate_random_loop("detroit",steps=16)
    #     image_buffer = visualize_loop_image(loop)
    #     await callback_query.message.answer_photo(photo=BufferedInputFile(image_buffer.getvalue(), filename="pattern.png"),caption="Сгенерированный паттерн")
    # except Exception as e:
    #     logging.exception("Ошибка при генерации паттерна")
    #     await callback_query.message.answer("Произошла ошибка при генерации")

#запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception("Ошибка при запуске бота")
if __name__ == "__main__":
    print ("Бот запускается")
    asyncio.run(main())

