import json
import random
from aiogram import types, Dispatcher
from keyboards.game import answers_keyboard
from keyboards.menu import main_menu

QUESTIONS_FILE = "data/questions.json"
USERS_FILE = "data/users.json"

games = {}


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


async def start_game(message: types.Message):
    questions = load_questions()
    selected = random.sample(questions, 20)

    games[message.from_user.id] = {
        "questions": selected,
        "current": 0,
        "score": 0
    }

    await send_question(message.from_user.id, message)


async def send_question(user_id, message):
    game = games[user_id]
    q = game["questions"][game["current"]]

    await message.answer(
        f"Вопрос {game['current'] + 1}/20\n\n{q['question']}",
        reply_markup=answers_keyboard(q["options"])
    )


async def answer_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    game = games[user_id]
    q = game["questions"][game["current"]]

    if int(callback.data) == q["answer"]:
        game["score"] += 1

    game["current"] += 1

    if game["current"] < 20:
        await send_question(user_id, callback.message)
    else:
        await finish_game(callback.message, user_id)

    await callback.answer()


async def finish_game(message, user_id):
    users = load_users()
    user = users[str(user_id)]
    score = games[user_id]["score"]

    if score > user["best_score"]:
        user["best_score"] = score
        save_users(users)

    await message.answer(
        f"🎉 Игра окончена!\n"
        f"Ваш результат: {score}/20",
        reply_markup=main_menu()
    )

    del games[user_id]


def register(dp: Dispatcher):
    dp.register_message_handler(start_game, text="▶️ Начать игру")
    dp.register_callback_query_handler(answer_handler)
