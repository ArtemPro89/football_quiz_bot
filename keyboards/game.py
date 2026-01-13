from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def answers_keyboard(options):
    keyboard = InlineKeyboardMarkup()
    for i, option in enumerate(options):
        keyboard.add(
            InlineKeyboardButton(
                text=option,
                callback_data=str(i)
            )
        )
    return keyboard
