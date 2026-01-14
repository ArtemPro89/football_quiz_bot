from aiogram import Router, F
from aiogram.types import Message
from keyboards.menu import main_menu
import json

router = Router()

waiting_for_name = set()

MENU_BUTTONS = {
    "▶️ Начать игру",
    "⚔️ Игра 1 на 1",
    "🏆 Рейтинг",
    "ℹ️ О викторине",
}


@router.message(F.text == "/start")
async def start_cmd(message: Message):
    waiting_for_name.add(message.from_user.id)
    await message.answer("👋 Привет! Введи своё имя:")


@router.message(
    F.text
    & ~F.text.in_(MENU_BUTTONS)   # ❗ НЕ кнопки меню
)
async def get_name(message: Message):
    user_id = message.from_user.id

    # если имя не ждём — игнор
    if user_id not in waiting_for_name:
        return

    name = message.text.strip()

    with open("data/users.json", "r+", encoding="utf-8") as f:
        users = json.load(f)
        users[str(user_id)] = {
            "name": name,
            "score": 0
        }
        f.seek(0)
        json.dump(users, f, ensure_ascii=False, indent=2)
        f.truncate()

    waiting_for_name.remove(user_id)

    await message.answer(
        f"✅ Отлично, {name}!",
        reply_markup=main_menu()
    )
