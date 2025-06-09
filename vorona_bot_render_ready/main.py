from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

bot = Bot(token='7886670102:AAHyVJL0PDn0APmrpe8Lf1gwBTHwOlojm0U')
dp = Dispatcher(storage=MemoryStorage())

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton('👤 Кто я такой'))

@dp.message(F.text == '👤 Кто я такой')
async def who(message: Message):
    await message.answer_photo(FSInputFile('me.jpg'), caption='Меня зовут Илья. Я живу во Владивостоке, люблю машины и сделал этот бот для честной и прозрачной помощи людям в автоимпорте.\n\nTelegram: @melehaha\nInstagram: @vorona.car')

@dp.message(commands='start')
async def start(message: Message):
    await message.answer('Привет! Выбери, что тебя интересует:', reply_markup=menu)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
