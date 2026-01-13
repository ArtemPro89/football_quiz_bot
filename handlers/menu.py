import json
from aiogram import types, Dispatcher
from keyboards.menu import main_menu

USERS_FILE = "data/users.json"


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


async def rating_handler(message: types.Message):
    users = load_users()

    sorted_users = sorted(
        users.values(),
        key=lambda x: x["best_score"],
        reverse=True
    )[:10]

    text = "🏆 ТОП-10 Рейтинг:\n\n"
    for i, user in enumerate(sorted_users, 1):
        text += f"{i}. {user['name']} — {user['best_score']} очков\n"

    await message.answer(text, reply_markup=main_menu())


async def about_handler(message: types.Message):
    await message.answer(
        "⚽ Футбольная викторина\n"
        "20 вопросов — 1 попытка\n"
        "В рейтинг попадает лучший результат",
        reply_markup=main_menu()
    )


def register(dp: Dispatcher):
    dp.register_message_handler(rating_handler, text="🏆 Рейтинг")
    dp.register_message_handler(about_handler, text="ℹ️ О викторине")
