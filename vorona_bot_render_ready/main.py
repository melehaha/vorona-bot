
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = "7886670102:AAHyVJL0PDn0APmrpe8Lf1gwBTHwOlojm0U"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Рассчитай мне авто")],
        [KeyboardButton(text="📄 Изучить договор и прочие документы")],
        [KeyboardButton(text="🛠 Как всё работает?")],
        [KeyboardButton(text="💬 Оставить сообщение")],
        [KeyboardButton(text="👤 Кто я такой")],
        [KeyboardButton(text="⚖️ Почему мы делаем это честно")],
        [KeyboardButton(text="💬 Хочу поговорить с человеком")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуйте! Это бот-помощник компании vorona.car.\nВыберите то, что вас интересует:", reply_markup=menu_kb)

@dp.message(F.text == "👤 Кто я такой")
async def who_am_i(message: Message):
    photo = FSInputFile("me.jpg")
    await message.answer_photo(photo, caption=(
        "Меня зовут Илья. Я живу во Владивостоке, люблю машины и давно хотел сделать честный и прозрачный способ привозить авто из Японии.\n\n"
        "Этот бот — моя личная инициатива. Я не анонимная компания. Я тот, кто сам разбирается в этом процессе, и лично отвечает перед каждым клиентом.\n\n"
        "Вот мой Telegram: @melehaha\n"
        "Вот Instagram: @vorona.car\n\n"
        "Я рядом, если что."
    ))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
