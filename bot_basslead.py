import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BufferedInputFile
from dotenv import load_dotenv
import os
from main_basslead import generate_bass, generate_lead, PATTERN_BASS, PATTERN_LEAD, NOTES, SCALES,STEPS
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
STEPS = [16,32,64]

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
        "steps_idx": 0,
        "mode":mode,
        "note_idx":0,
        "scale_idx":0
    }
    logging.info(f"Пользователь {user_id} выбрал режим {mode}")

    buttons = [
        [
        InlineKeyboardButton(text=f"Нота:{NOTES[0]}",callback_data="toggle_note"),
        InlineKeyboardButton(text=f"Лад:{SCALES[0]}",callback_data="toggle_scale"),
        InlineKeyboardButton(text=f"Шаги:{STEPS[0]}",callback_data="toggle_steps"),
    ],
    [InlineKeyboardButton(text="🎲Сгенерировать паттерн",callback_data="generate")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    text = (
        f"Режим: {mode.capitalize()}\n"
        f"Нота: {NOTES[0]}\n"
        f"Лад: {SCALES[0]}\n"
        f"Шаги: {STEPS[0]}"
    )

    await callback_query.message.answer(text, reply_markup=keyboard)

#дальше идет обработчки кнопки нота и далее обработчик кнопки лад и далее еще steps(с edit.text обязательно)

@dp.callback_query(lambda c: c.data =="toggle_note")
async def toggle_note(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    state = user_state[user_id]

    state["note_idx"] = (state["note_idx"] + 1) % len(NOTES)

    text = (
        f"Режим: {state["mode"].capitalize()}\n"
        f"Нота: {NOTES[state["note_idx"]]}\n"
        f"Лад: {SCALES[state["scale_idx"]]}\n"
        f"Шаги: {STEPS[state["steps_idx"]]}"
    )
    buttons = [
        [InlineKeyboardButton(text=f"Нота: {NOTES[state["note_idx"]]}",callback_data="toggle_note"),
        InlineKeyboardButton(text=f"Лад: {SCALES[state["scale_idx"]]}", callback_data="toggle_scale"),
        InlineKeyboardButton(text=f"Шаги: {STEPS[state["steps_idx"]]}", callback_data="toggle_steps")],
        [InlineKeyboardButton(text="🎲Сгенерировать паттерн",callback_data="generate")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "toggle_scale")
async def toggle_scale(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    state = user_state[user_id]

    state["scale_idx"] = (state["scale_idx"] + 1) % len(SCALES)

    text = (
        f"Режим: {state["mode"].capitalize()}\n"
        f"Нота: {NOTES[state["note_idx"]]}\n"
        f"Лад: {SCALES[state["scale_idx"]]}\n"
        f"Шаги: {STEPS[state["steps_idx"]]}"
    )

    buttons = [
        [InlineKeyboardButton(text=f"Нота: {NOTES[state["note_idx"]]}",callback_data="toggle_note"),
        InlineKeyboardButton(text=f"Лад: {SCALES[state["scale_idx"]]}", callback_data="toggle_scale"),
        InlineKeyboardButton(text=f"Шаги: {STEPS[state["steps_idx"]]}", callback_data="toggle_steps")],
        [InlineKeyboardButton(text="🎲Сгенерировать паттерн",callback_data="generate")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "toggle_steps")
async def toggle_steps(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    state = user_state[user_id]

    state["steps_idx"] = (state["steps_idx"] + 1) % len(STEPS)

    text = (
        f"Режим: {state["mode"].capitalize()}\n"
        f"Нота: {NOTES[state["note_idx"]]}\n"
        f"Лад: {SCALES[state["scale_idx"]]}\n"
        f"Шаги: {STEPS[state["steps_idx"]]}"
    )

    buttons = [
        [InlineKeyboardButton(text=f"Нота: {NOTES[state["note_idx"]]}",callback_data="toggle_note"),
        InlineKeyboardButton(text=f"Лад: {SCALES[state["scale_idx"]]}", callback_data="toggle_scale"),
        InlineKeyboardButton(text=f"Шаги: {STEPS[state["steps_idx"]]}", callback_data="toggle_steps")],
        [InlineKeyboardButton(text="🎲Сгенерировать паттерн",callback_data="generate")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback_query.message.edit_text(text, reply_markup=keyboard)

def midi_to_name(midi):
    note = NOTES[midi % 12]
    octave = midi // 12 - 1
    return f"{note}{octave}"

#далее идет обработчик генерации 

@dp.callback_query(lambda c: c.data=="generate")
async def process_generate(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id

    if user_id not in user_state:
        await callback_query.answer("Сначала выбери режим через /start", show_alert=True)
        return
    
    try:
        state = user_state[user_id]
        mode = state["mode"]

        steps = STEPS[state["steps_idx"]]
        scale = SCALES[state["scale_idx"]]
        note_idx = state["note_idx"]

        if mode == "bass":
            root_note = 36 + note_idx
            mask_name = random.choice(PATTERN_BASS)
        else:
            root_note = 60 + note_idx
            mask_name = random.choice(PATTERN_LEAD)

        config = {
            "root_note":root_note,
            "scale":scale,
            "mask":mask_name,
            "steps":steps,
            "oct_shift":0
        }

        logging.info(f"Генерация в режиме {mode} для пользователя {user_id}, config {config}")

        if mode == "bass":
            notes, count = generate_bass(config)
        else:
            notes, count = generate_lead(config)

        names = [midi_to_name(n) if n is not None else "-" for n in notes]
        text = (
            f"Режим: {mode.capitalize()}\n"
            f"Нота: {NOTES[note_idx]}\n"
            f"Лад: {SCALES[state["scale_idx"]]}\n"
            f"Шаги: {steps}\n"
            f"Маска: {mask_name}\n"
            f"Всего нот: {count}\n\n"
            + " ".join(names)
        )

        await callback_query.message.answwr(text)
    
    except Exception:
        logging.exception("Ошибка при генерации паттерна")
        await callback_query.message.answer("Произошла ошибка при генерации. Попробуй ещё раз.")


async def main():
    try:
        await dp.start_polling(bot)
    except Exception:
        logging.exception("Ошибка при запуске бота")


if __name__ == "__main__":
    print("Бот запускается")
    asyncio.run(main())