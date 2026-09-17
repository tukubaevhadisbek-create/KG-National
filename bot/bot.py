import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Загружаем переменные из .env файла
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

# Проверка обязательных переменных окружения
if not BOT_TOKEN:
    raise ValueError("ОШИБКА: BOT_TOKEN не найден в файле .env")

if not WEB_APP_URL:
    raise ValueError("ОШИБКА: WEB_APP_URL не найден в файле .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 «Кыргыз Дүйнөсү» баштоо",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    await message.answer(
        "Саламатсызбы! «Кыргыз Дүйнөсү» тиркемесине кош келиңиз!",
        reply_markup=kb
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())