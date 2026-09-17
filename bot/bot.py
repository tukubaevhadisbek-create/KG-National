import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8845602104:AAF-xL54YP5OvUIIJShmrqDQ30Zq_TE1Woc"
# Обновили адрес на текущий из localtunnel:
WEB_APP_URL = "https://65736cca73a1a.lhr.life"

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