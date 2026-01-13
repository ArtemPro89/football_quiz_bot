import json
from aiogram import types, Dispatcher
from keyboards.menu import main_menu

USERS_FILE = "data/users.json"


def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


async def start_handler(message: types.Message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id in users:
        await message.answer(
            f"С возвращением, {users[user_id]['name']}!",
            reply_markup=main_menu()
        )
    else:
        await message.answer("Привет! Введи свой никнейм 👇")


async def name_handler(message: types.Message):
    users = load_users()
    user_id = str(message.from_user.id)

    if user_id in users:
        return

    users[user_id] = {
        "name": message.text,
        "best_score": 0
    }

    save_users(users)

    await message.answer(
        f"Отлично, {message.text}! Добро пожаловать в викторину ⚽",
        reply_markup=main_menu()
    )


def register(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(name_handler)
