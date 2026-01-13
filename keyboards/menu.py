from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("▶️ Начать игру"),
        KeyboardButton("🏆 Рейтинг")
    )
    keyboard.add(
        KeyboardButton("ℹ️ О викторине")
    )
    return keyboard
