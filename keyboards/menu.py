from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="▶️ Начать игру"),
                KeyboardButton(text="⚔️ Игра 1 на 1")
            ],
            [
                KeyboardButton(text="🏆 Рейтинг"),
                KeyboardButton(text="ℹ️ О викторине")
            ]
        ],
        resize_keyboard=True
    )
