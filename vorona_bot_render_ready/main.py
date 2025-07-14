
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = "7886670102:AAHyVJL0PDn0APmrpe8Lf1gwBTHwOlojm0U"
ADMIN_ID = 378871923

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Form(StatesGroup):
    car_exact = State()
    car_help = State()

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Кто я такой?")],
        [KeyboardButton(text="🛠 Как всё работает?")],
        [KeyboardButton(text="📄 Изучить договор и прочие документы")],
        [KeyboardButton(text="🇯🇵 Почему только Япония?")],
        [KeyboardButton(text="⚖️ Почему я делаю это честно?")],
        [KeyboardButton(text="🚗 Рассчитай мне авто")],
        [KeyboardButton(text="💬 Хочу поговорить с человеком")]
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

docs_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📃 Договор")],
        [KeyboardButton(text="📄 Пример инвойса")],
        [KeyboardButton(text="🧾 Данные об агентах")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Здравствуйте! Это бот-помощник компании https://instagram.com/vorona.car\nВыберите то, что вас интересует:", reply_markup=menu_kb)

@dp.message(F.text == "👤 Кто я такой?")
async def who_am_i(message: Message):
    photo = FSInputFile("me.jpg")
    await message.answer_photo(photo, caption=(
        "Меня зовут Илья. Я живу во Владивостоке, люблю машины и давно хотел сделать честный и прозрачный способ привозить авто из Японии.\n\n"
        "Этот бот — моя личная инициатива. Я не анонимная компания. Я тот, кто сам разбирается в этом процессе, и лично отвечает перед каждым клиентом.\n\n"
        "Telegram: @melehaha\n"
        "Instagram: https://instagram.com/vorona.car\n\n"
        "Я рядом, если что."
    ))

@dp.message(F.text == "🛠 Как всё работает?")
async def how_it_works(message: Message):
    await message.answer(
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
        "Instagram: https://instagram.com/vorona.car"
    )

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

@dp.message(F.text == "🇯🇵 Почему только Япония?")
async def why_only_japan(message: Message):
    await message.answer(
        "Я работаю только с Японией, потому что Япония — это честно.\n\n"
        "Там с 80-х годов существует система аукционов, где всё прозрачно и контролируется. Машину с залогом, криминальным прошлым или «кривыми» документами просто не пустят в торги. Всё проверяется автоматически и юридически. А ещё — я сам вижу подробные фото, схему повреждений, пробег, даже состояние днища, до того, как мы поставим ставку.\n\n"
        "В Корее такого контроля пока нет. Бывают случаи, когда авто оказывается после серьёзной аварии, а внешне выглядит почти новым. Это редкость, но всё же возможно. Я не могу за это отвечать, а значит — не хочу рисковать ни своей репутацией, ни чужими деньгами.\n\n"
        "Про Китай — там вообще сложнее. Машины часто приходят с более слабым качеством сборки, пробеги могут быть скручены, и главное — эксплуатация небрежная. В Японии — наоборот. Там обязателен shaken — государственный техосмотр. Первый проходит через 3 года, потом каждые 2 года. Если машина не в порядке — её просто не допустят на дорогу. А японцы к этому относятся серьёзно. У них культура ухода за автомобилем: ездят мало, моют часто, берегут.\n\n"
        "Почему только Япония? Потому что я хочу спать спокойно. Чтобы человек, которому я привёз машину, был доволен. Потому что я не перекуп, а человек, который поставил себе задачу делать это честно и на совесть.\n\n"
        "Если появится альтернатива с таким же уровнем доверия и прозрачности — я буду только рад. Но пока — Япония. Потому что это надёжно. Потому что я могу за это отвечать."
    )

@dp.message(F.text == "⚖️ Почему я делаю это честно?")
async def why_honest(message: Message):
    await message.answer(
        "1. Я сам боюсь быть обманутым — поэтому строю работу на прозрачности.\n"
        "2. Всё официально: договор, инвойс, документы.\n"
        "3. Деньги идут только после выигрыша авто на аукционе.\n"
        "4. Я лично показываю весь процесс — без менеджеров и фильтров.\n"
        "5. Моя репутация и доверие важнее любой быстрой прибыли.\n\n"
        "Если будет желание — можем пообщаться лично."
    )

@dp.message(F.text == "💬 Хочу поговорить с человеком")
async def talk_to_human(message: Message):
    await message.answer(
        "Я понимаю, что бот — это удобно, но не всегда достаточно. Иногда нужно просто поговорить с живым человеком.\n\n"
        "Вот мой Telegram: @melehaha\n\n"
        "Можем обсудить всё голосом или перепиской — как вам комфортнее."
    )


@dp.message(F.text == "🚗 Рассчитай мне авто")
async def choose_car_flow(message: Message):
    await message.answer("Выберите подходящий вариант:", reply_markup=car_choice_kb)

@dp.message(F.text == "✅ Я точно знаю, какой автомобиль хочу, рассчитайте мне среднюю стоимость")
async def car_exact(message: Message, state: FSMContext):
    await state.set_state(Form.car_exact)
    await message.answer("Напишите желаемую марку, модель, год, кузов, привод и цвет.\nЧем подробнее, тем точнее будет расчет.", reply_markup=ReplyKeyboardRemove())

@dp.message(Form.car_exact)
async def process_car_exact(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"[ТОЧНЫЙ ЗАПРОС ОТ {message.from_user.full_name} (@{message.from_user.username})]:\n{message.text}\n\nЧтобы ответить: /ответ {message.from_user.id} [ваш текст]")
    await message.answer("Спасибо за ваш запрос! Я рассмотрю его и обязательно отвечу в ближайшее время — прямо здесь, в этом боте.", reply_markup=menu_kb)
    await state.clear()

@dp.message(F.text == "🤔 Мне нужен совет, я знаю только бюджет и примерный запрос")
async def car_help(message: Message, state: FSMContext):
    await state.set_state(Form.car_help)
    await message.answer("Напишите примерный бюджет и какую машину вы хотите.\nНе стесняйтесь, даже если “красненькую” — это вся информация.", reply_markup=ReplyKeyboardRemove())

@dp.message(Form.car_help)
async def process_car_help(message: Message, state: FSMContext):
    await bot.send_message(ADMIN_ID, f"[ПОМОЩЬ С ВЫБОРОМ ОТ {message.from_user.full_name} (@{message.from_user.username})]:\n{message.text}\n\nЧтобы ответить: /ответ {message.from_user.id} [ваш текст]")
    await message.answer("Спасибо! Я изучу ваш запрос и отвечу вам прямо здесь в ближайшее время.", reply_markup=menu_kb)
    await state.clear()




@dp.message(Command("ответ"))
async def reply_command(message: Message):
    try:
        print(">> /ответ команда получена")
        parts = message.text.split(maxsplit=2)
        user_id = int(parts[1])
        text = parts[2]
        print(f">> Пытаюсь отправить сообщение user_id={user_id}, текст='{text}'")
        await bot.send_message(user_id, text)
        await message.answer("✅ Ответ отправлен пользователю.")
    except Exception as e:
        print(f">> Ошибка: {e}")
        await message.answer(f"❌ Ошибка при отправке: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


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
