from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def question_keyboard(question: dict):
    buttons = []

    for i, option in enumerate(question["options"]):
        buttons.append([
            InlineKeyboardButton(
                text=option,
                callback_data=str(i)
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
