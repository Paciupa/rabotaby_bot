import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Файлик с API токеном и id пользователя
import config
bot = Bot(token=config.API_TOKEN)

# Извлекаем из виртуальной среды переменные окружения. API токен и id пользователя
from os import environ
telegram_key = environ.get('API_TELEGRAM_KEY')
user_id = environ.get('USER_ID')
# Подключаемся к боту
bot = Bot(token=telegram_key)

# MemoryStorage. Храним состояния в оператиной памяти. Заменить на другой тип хранения
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение класса состояний. 
class CS(StatesGroup):
	AVAILABLE = State()
	ADD_T1 = State()
	ADD_T2 = State()
	ADD_B1 = State()
	ADD_B2 = State()
	DEL_T = State()
	DEL_B = State()

async def is_user_ID(message):
	return message.from_user.id == int(user_id)

@dp.message_handler(commands=['start'])  
async def cmd_start(message: types.Message):
	await asyncio.sleep(0.5)
	if await is_user_ID(message):
		await bot.send_message(message.chat.id, "Привет!")
	else:
		await bot.send_message(message.chat.id, "Please leave this chat. You're an unregistered user\nПрошу покинуть этот чат. Вы незарегистрированный пользователь")


@dp.message_handler(commands=['help'], state=CS.AVAILABLE)
async def help(message: types.Message, state:FSMContext):
	await bot.send_message(message.chat.id, """
	Шаблоны поиска
	/add_T Добавить шаблон поиска
	/del_T Удалить шаблон поиска
	/print_T Вывести все шаблоны поиска

	Чёрный список
	/add_B Добавить адрес из чёрного списка
	/del_B Удалить адрес из чёрного списка
	/print_B Вывести все адреса чёрного списка
	""")

@dp.message_handler(commands=['add_T'], state=CS.AVAILABLE)
async def add_T(message: types.Message, state:FSMContext):
	await bot.send_message(message.chat.id, "1️⃣ Введите слово ключ шаблона")
	await state.set_state(CS.ADD_T1)

@dp.message_handler(state=CS.ADD_T1)
async def add_T_key(message: types.Message, state:FSMContext):
	wordkey = message.text
	# Проверка, на уникальность. Существует ли таке слово ключ в базе шаблонов
	if wordkey in st.get_col_by_name("key"):
		await bot.send_message(message.chat.id, "❌ Такое слово ключ уже существует. Введите другое слово ключ")
	else:
		# Сохраняем полученное значение
		await state.update_data(WORDKEY=wordkey)
		await state.set_state(CS.ADD_T2)
		await bot.send_message(message.chat.id, "✅ Слово ключ - сохранён!")
		await bot.send_message(message.chat.id, "2️⃣ Введите url для добавления в базу")

@dp.message_handler(state=CS.ADD_T2)
async def add_T_url(message: types.Message, state:FSMContext):
	# Извлекаем wordkey
	data = await state.get_data()
	wordkey = data.get("WORDKEY")
	# Получаем url
	url = message.text
	st.create_new_row(wordkey, url)
	await bot.send_message(message.chat.id, "✅ Новый шаблон добавлен в базу!")
	await state.set_state(CS.AVAILABLE)

@dp.message_handler(commands=['del_T'], state=CS.AVAILABLE)
async def del_T_msg(message: types.Message, state:FSMContext):
	await bot.send_message(message.chat.id, "Укажите номер шаблона.\nЧтобы узнать номер введите /print_T")
	await state.set_state(CS.DEL_T)

@dp.message_handler(state=CS.DEL_T)
async def del_T_input(message: types.Message, state:FSMContext):
	msg = message.text
	try:
		number_templece = int(msg)
		if number_templece > 0 and number_templece <= st.get_num_all_rows():
			st.delete_row_by_number(number_templece)
			await bot.send_message(message.chat.id, "✅ Номер шаблона успешно удалён!")
			await state.set_state(CS.AVAILABLE)
		else:
			await bot.send_message(message.chat.id, "❌ Такой номер в базе отсутсвует. Введите корректный!")
	except:
		if msg == "/print_T":
			await print_T(message, state)
		else:
			await bot.send_message(message.chat.id, "❌ Неверное значение! Укажите число из списка")
	
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
