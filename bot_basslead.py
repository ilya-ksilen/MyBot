import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BufferedInputFile
from dotenv import load_dotenv
import os
from main_basslead import generate_bass, generate_lead, PATTERN_BASS, PATTERN_LEAD, generate_visual, midi_to_name, SCALES, NOTES, STEPS, GENRES, MODES, GENRE_EMOJI,MODES_EMOJI
import random
from markov import generate_markov
from audio import notes_to_wav

logging.basicConfig(level=logging.DEBUG,
format="%(asctime)s - %(levelname)s - %(message)s")

print("DEBUG: bot_basslead.py начал выполняться", file=sys.stderr)
sys.stderr.flush()

load_dotenv()
TOKEN = os.getenv("BASSLEAD_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp=Dispatcher()

user_state={}

STEPS = [16,32,64]

# главный экран-меню
def main_screen(state):
    genre = GENRES[state["genre_idx"]]
    mode = MODES[state["mode_idx"]]
    note = NOTES[state["note_idx"]]
    scale = SCALES[state["scale_idx"]]
    steps = STEPS[state["steps_idx"]]

    text = (
        "🎛ТЕХНО-ГЕНЕРАТОР🎛\n\n"
        "Привет! Я генерирую бас-линии и лид-партии в техно для твоего вдохновения!\n"
        "Генерация основана на глубоком анализе жанра и использует алгоритм цепей Маркова\n\n"
        "Режимы техно:\n"
        "☺Detroit - классический, фанковый, катящийся\n"
        "🏭Industrial - агрессивный, индустриальный, ломанный\n\n"
        "Тип партии:\n"
        "🎸Bass - генерация бас-линии\n"
        "🎹Lead - генерация лид-партии\n\n"
        "Выбирай настройки кнопками и жми 🎲 Сгенерировать"
    )

    buttons = [
        [
            InlineKeyboardButton(text=f"{GENRE_EMOJI[genre]} {genre.capitalize()}", callback_data="toggle_genre"),
            InlineKeyboardButton(text=f"{MODES_EMOJI[mode]} {mode.capitalize()}", callback_data="toggle_mode")
        ],

        [
            InlineKeyboardButton(text=f"{note}",callback_data="toggle_note"),
            InlineKeyboardButton(text=f"{scale}",callback_data="toggle_scale"),
            InlineKeyboardButton(text=f"⏱Шагов: {steps}",callback_data="toggle_steps")
        ],
        [
            InlineKeyboardButton(text=f"Сгенерировать", callback_data="generate")
            ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return text, keyboard

# обработка кнопки старт
@dp.message(Command("start"))
async def start_command(message:types.Message):
    logging.info(f"команда start от пользователя {message.from_user.id}")

    user_id = message.from_user.id
    user_state[user_id] = {
        "genre_idx": 0,
        "mode_idx": 0,
        "note_idx": 0,
        "scale_idx": 0,
        "steps_idx": 0
    }
    text, keyboard = main_screen(user_state[user_id])
    await message.answer(text, reply_markup=keyboard)

#дальше идет обработка нажатия всех кнопок на main_screen (с edit_text чтобы не множились сообщения от бота)

@dp.callback_query(lambda c:c.data == "toggle_genre")
async def toggle_genre(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    if user_id  not in user_state:
        await callback_query.answer("Сначала /start", show_alert = True)
        return

    state = user_state[user_id]
    state["genre_idx"]= (state["genre_idx"] + 1) % len(GENRES)
    text, keyboard = main_screen(state)
    
    genre = GENRES[state["genre_idx"]]
    logging.info(f"Пользователь {user_id} выбрал жанр {genre}")

    await callback_query.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query(lambda c:c.data == "toggle_mode")
async def toggle_mode(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    if user_id  not in user_state:
        await callback_query.answer("Сначала /start", show_alert = True)
        return

    state = user_state[user_id]
    state["mode_idx"]= (state["mode_idx"] + 1) % len(MODES)
    text, keyboard = main_screen(state)
    
    mode = MODES[state["mode_idx"]]
    logging.info(f"Пользователь {user_id} выбрал режим {mode}")

    await callback_query.message.edit_text(text, reply_markup=keyboard)

    
@dp.callback_query(lambda c:c.data == "toggle_note")
async def toggle_note(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    if user_id  not in user_state:
        await callback_query.answer("Сначала /start", show_alert = True)
        return

    state = user_state[user_id]
    state["note_idx"]= (state["note_idx"] + 1) % len(NOTES)
    text, keyboard = main_screen(state)
    
    note = NOTES[state["note_idx"]]
    logging.info(f"Пользователь {user_id} выбрал ноту {note}")

    await callback_query.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c:c.data == "toggle_scale")
async def toggle_scale(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    if user_id  not in user_state:
        await callback_query.answer("Сначала /start", show_alert = True)
        return

    state = user_state[user_id]
    state["scale_idx"]= (state["scale_idx"] + 1) % len(SCALES)
    text, keyboard = main_screen(state)
    
    scale = SCALES[state["scale_idx"]]
    logging.info(f"Пользователь {user_id} выбрал лад {scale}")

    await callback_query.message.edit_text(text, reply_markup=keyboard)

@dp.callback_query(lambda c:c.data == "toggle_steps")
async def toggle_steps(callback_query: CallbackQuery):
    await callback_query.answer()

    user_id = callback_query.from_user.id
    if user_id  not in user_state:
        await callback_query.answer("Сначала /start", show_alert = True)
        return

    state = user_state[user_id]
    state["steps_idx"]= (state["steps_idx"] + 1) % len(STEPS)
    text, keyboard = main_screen(state)
    
    steps = STEPS[state["steps_idx"]]
    logging.info(f"Пользователь {user_id} выбрал кол-во шагов {steps}")
    await callback_query.message.edit_text(text, reply_markup=keyboard)

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
        mode = MODES[state["mode_idx"]]
        genre = GENRES[state["genre_idx"]]

        steps = STEPS[state["steps_idx"]]
        scale = SCALES[state["scale_idx"]]
        note_idx = state["note_idx"]

        if mode == "bass":
            root_note = 36 + note_idx
        else:
            root_note = 60 + note_idx

        config = {
            "root_note":root_note,
            "scale":scale,
            "steps":steps,
            "oct_shift":0
        }

        logging.info(f"Генерация в режиме {mode} для пользователя {user_id}, config {config}")

        if mode == "bass":
            subgenre = f"{genre}_bass"
            note_color = "#ff8800"
        else:
            subgenre = f"{genre}_lead"
            note_color = "#00aaff"
        
        title = f"{genre.upper()} {mode.upper()} PATTERN"
        notes, count = generate_markov(subgenre, root_note, bars=steps//16,)
        image_buffer = generate_visual(notes, title, steps, note_color=note_color)
        await callback_query.message.answer_photo(
        photo=BufferedInputFile(image_buffer.getvalue(), filename="pattern.png"),
        caption=f"{mode.capitalize()}: {NOTES[note_idx]} {SCALES[state['scale_idx']]}"
        )
        audio_data = notes_to_wav(notes, bpm=130)
        await callback_query.message.answer_audio(
            audio = BufferedInputFile(audio_data, filename="pattern.wav")
            caption = f"Прослушать превью: {title}"
        )
    
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