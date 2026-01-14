from aiogram import Router, F
from aiogram.types import Message
import json

router = Router()


@router.message(F.text == "🏆 Рейтинг")
async def rating(message: Message):
    with open("data/users.json", encoding="utf-8") as f:
        users = json.load(f)

    top = sorted(users.values(), key=lambda x: x["score"], reverse=True)[:10]

    text = "🏆 ТОП-10 игроков:\n\n"
    for i, user in enumerate(top, start=1):
        text += f"{i}. {user['name']} — {user['score']}\n"

    await message.answer(text)


@router.message(F.text == "ℹ️ О викторине")
async def about_quiz(message: Message):
    await message.answer(
        "⚽ *Футбольная викторина*\n\n"
        "• 10 случайных вопросов\n"
        "• 1 балл за каждый правильный ответ\n"
        "• Попади в ТОП-10 рейтинга\n\n"
        "Удачи! 🍀",
        parse_mode="Markdown"
    )


@router.message(F.text == "⚔️ Игра 1 на 1")
async def duel(message: Message):
    await message.answer(
        "⚔️ Режим *1 на 1* скоро будет доступен!\n\n"
        "Мы уже работаем над ним 👨‍💻",
        parse_mode="Markdown"
    )
