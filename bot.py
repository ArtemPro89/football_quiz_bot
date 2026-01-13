from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN

from handlers import start, menu, game

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

start.register(dp)
menu.register(dp)
game.register(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
