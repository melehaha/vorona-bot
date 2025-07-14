
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = "7886670102:AAHyVJL0PDn0APmrpe8Lf1gwBTHwOlojm0U"
ADMIN_ID = 378871923

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    car_exact = State()
    car_help = State()
    feedback = State()

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 Рассчитай мне авто")],
        [KeyboardButton(text="📄 Изучить договор и прочие документы")],
        [KeyboardButton(text="🛠 Как всё работает?")],
        [KeyboardButton(text="💬 Оставить сообщение")]
    ],
    resize_keyboard=True
)

docs_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📃 Договор")],
        [KeyboardButton(text="📄 Пример инвойса")],
        [KeyboardButton(text="🧾 Данные об агентах")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

car_choice_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Я точно знаю, какой автомобиль хочу, рассчитайте мне среднюю стоимость")],
        [KeyboardButton(text="🤔 Мне нужен совет, я знаю только бюджет и примерный запрос")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Здравствуйте! Это бот-помощник компании vorona.car.\nВыберите то, что вас интересует:",
        reply_markup=menu_kb
    )

@dp.message(F.text == "🚗 Рассчитай мне авто")
async def choose_car_flow(message: Message):
    await message.answer("Выберите подходящий вариант:", reply_markup=car_choice_kb)

@dp.message(F.text == "✅ Я точно знаю, какой автомобиль хочу, рассчитайте мне среднюю стоимость")
async def car_exact(message: Message, state: FSMContext):
    await state.set_state(Form.car_exact)
    await message.answer(
        "Напишите желаемую марку, модель, год, кузов, привод и цвет.\nЧем подробнее, тем точнее будет расчет.",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(F.text == "🤔 Мне нужен совет, я знаю только бюджет и примерный запрос")
async def car_help(message: Message, state: FSMContext):
    await state.set_state(Form.car_help)
    await message.answer(
        "Напишите примерный бюджет и какую машину вы хотите.\nНе стесняйтесь, даже если “красненькую” — это вся информация.",
        reply_markup=ReplyKeyboardRemove()
    )

@dp.message(Form.car_exact)
async def process_exact(message: Message, state: FSMContext):
    text = f"[ТОЧНЫЙ ЗАПРОС ОТ {message.from_user.full_name} (@{message.from_user.username})]:\n{message.text}\n\nЧтобы ответить: /ответ {message.from_user.id} [ваш текст]"
    await bot.send_message(ADMIN_ID, text)
    await message.answer("Спасибо за ваш запрос! Я рассмотрю его и обязательно отвечу в ближайшее время — прямо здесь, в этом боте.", reply_markup=menu_kb)
    await state.clear()

@dp.message(Form.car_help)
async def process_help(message: Message, state: FSMContext):
    text = f"[ПОМОЩЬ С ВЫБОРОМ ОТ {message.from_user.full_name} (@{message.from_user.username})]:\n{message.text}\n\nЧтобы ответить: /ответ {message.from_user.id} [ваш текст]"
    await bot.send_message(ADMIN_ID, text)
    await message.answer("Спасибо! Я изучу ваш запрос и отвечу вам прямо здесь в ближайшее время.", reply_markup=menu_kb)
    await state.clear()

@dp.message(F.text == "💬 Оставить сообщение")
async def ask_feedback(message: Message, state: FSMContext):
    await state.set_state(Form.feedback)
    await message.answer("Напишите ваше сообщение. Я обязательно его прочту и отвечу.")

@dp.message(Form.feedback)
async def handle_feedback(message: Message, state: FSMContext):
    text = f"[СООБЩЕНИЕ ОТ {message.from_user.full_name} (@{message.from_user.username})]:\n{message.text}\n\nЧтобы ответить: /ответ {message.from_user.id} [ваш текст]"
    await bot.send_message(ADMIN_ID, text)
    await message.answer("Спасибо! Ваше сообщение отправлено.", reply_markup=menu_kb)
    await state.clear()

@dp.message(Command("ответ"))
async def handle_admin_reply(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("❗ Формат команды: /ответ [user_id] [текст]")
        return

    try:
        target_user_id = int(parts[1])
        reply_text = parts[2]
        await bot.send_message(target_user_id, reply_text)
        await message.answer("✅ Ответ отправлен.")
    except Exception as e:
        await message.answer(f"Ошибка при отправке: {e}")

@dp.message(F.text == "📄 Изучить договор и прочие документы")
async def docs_menu(message: Message):
    await message.answer("Выберите документ:", reply_markup=docs_kb)

@dp.message(F.text == "📃 Договор")
async def send_dogovor(message: Message):
    await message.answer_document(FSInputFile("dogovor.pdf"))

@dp.message(F.text == "📄 Пример инвойса")
async def send_invoice(message: Message):
    await message.answer_document(FSInputFile("invoice.jpeg"))

@dp.message(F.text == "🧾 Данные об агентах")
async def send_agents(message: Message):
    await message.answer_document(FSInputFile("agency.png"))

@dp.message(F.text == "🔙 Назад")
async def go_back(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=menu_kb)

@dp.message(F.text == "🛠 Как всё работает?")
async def how_it_works(message: Message):
    steps = (
        "1. Мы заключаем договор\n"
        "2. Я нахожу интересующий вас авто на аукционах Японии\n"
        "3. Рассказываю максимально полную информацию о найденном авто\n"
        "4. Если вас всё устраивает - мы ставим ставку на аукционе\n"
        "5. Когда автомобиль куплен, я присылаю вам инвойс, вы оплачиваете его в банке\n"
        "6. После того, как оплата придет в Японию, начинается таможенная очистка и выдача экспортного сертификата\n"
        "7. Авто доставляют в порт и передают транспортной компании\n"
        "8. В порту проводят фотоопись и погрузку на корабль\n"
        "9. По приходу судна в порт Владивостока - погрузочно-разгрузочные работы, таможенное оформление, оформление СБКТС, ЭПТС, прохождение лаборатории\n"
        "10. Если вы во Владивостоке - вы забираете автомобиль. Если нет, я забираю авто и ставлю на автовоз, который отправит его в ваш город\n\n"
        "P.S.: Если честно, сухим текстом читать это скучно, поэтому переходите в инст: @vorona.car, там я рассказываю обо всём этом интересней!"
    )
    await message.answer(steps)


@dp.message(Command("ответ"))
async def reply_command(message: Message):
    try:
        parts = message.text.split(maxsplit=2)
        user_id = int(parts[1])
        text = parts[2]
        await bot.send_message(user_id, text)
        await message.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
