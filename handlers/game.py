import json
import random
import time

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.game import question_keyboard

router = Router()

# Активные игры пользователей
user_games = {}


@router.message(F.text == "▶️ Начать игру")
async def start_game(message: Message):
    with open("data/questions.json", encoding="utf-8") as f:
        questions = json.load(f)

    random.shuffle(questions)

    user_games[message.from_user.id] = {
        "questions": questions[:20],   # 20 вопросов
        "current": 0,
        "score": 0,
        "start_time": time.time()
    }

    await send_question(message.from_user.id, message)


async def send_question(user_id: int, message: Message):
    game = user_games[user_id]
    q = game["questions"][game["current"]]

    await message.answer(
        f"❓ *Вопрос {game['current'] + 1}/20*\n\n"
        f"{q['question']}",
        reply_markup=question_keyboard(q),
        parse_mode="Markdown"
    )


@router.callback_query()
async def answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_games:
        await callback.answer("Игра не найдена", show_alert=True)
        return

    game = user_games[user_id]
    q = game["questions"][game["current"]]

    if int(callback.data) == q["answer"]:
        game["score"] += 1
        await callback.message.answer("✅ Верно!")
    else:
        await callback.message.answer("❌ Неверно!")

    game["current"] += 1

    if game["current"] >= len(game["questions"]):
        await finish_game(callback)
    else:
        await send_question(user_id, callback.message)

    await callback.answer()


async def finish_game(callback: CallbackQuery):
    user_id = callback.from_user.id
    game = user_games[user_id]

    score = game["score"]
    total = len(game["questions"])

    elapsed = int(time.time() - game["start_time"])
    minutes = elapsed // 60
    seconds = elapsed % 60

    with open("data/users.json", "r+", encoding="utf-8") as f:
        users = json.load(f)
        users[str(user_id)]["score"] += score
        f.seek(0)
        json.dump(users, f, ensure_ascii=False, indent=2)
        f.truncate()

    await callback.message.answer(
        "🏁 *Игра окончена!*\n\n"
        f"🎯 Результат: *{score} / {total}*\n"
        f"⏱ Время: *{minutes} мин {seconds} сек*",
        parse_mode="Markdown"
    )

    del user_games[user_id]
