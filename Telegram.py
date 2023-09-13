import asyncio
from os import environ
# import threading

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Data import SearchTemplates, BlackList, VisitsList
import Main

# Извлекаем из виртуальной среды переменные окружения. API токен и id пользователя
telegram_key = environ.get('API_TELEGRAM_KEY')
user_id = environ.get('USER_ID')
# Подключаемся к боту
bot = Bot(token=telegram_key)

# global st, bl, vl, telegram_key, user_id, bot, storage, dp
st = SearchTemplates("SearchTemplates.db")
bl = BlackList("BlackList.db")
vl = VisitsList("SearchTemplates.db")

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
	SET_TIME = State()

# def run_telegram():
# 	executor.start_polling(dp, skip_updates=True)


async def is_user_ID(message):
	return message.from_user.id == int(user_id)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
	await asyncio.sleep(0.5)
	# Только пользователь с допустимым ID сможет получить доступ к боту
	if await is_user_ID(message):
		await bot.send_message(message.chat.id, "🖐 Hola! \nВведите /help для доступа к командам")
		await state.set_state(CS.AVAILABLE)
	else:
		await bot.send_message(message.chat.id, "❌  Please leave this chat. You're an unregistered user\nПрошу покинуть этот чат. Вы незарегистрированный пользователь")


@dp.message_handler(commands=['help'], state=CS.AVAILABLE)
async def command_help(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, """
	Шаблоны поиска
	/add_t Добавить шаблон поиска
	/del_t Удалить шаблон поиска
	/print_t Вывести все шаблоны поиска

	Чёрный список
	/add_b Добавить адрес из чёрного списка
	/del_b Удалить адрес из чёрного списка
	/print_b Вывести все адреса чёрного списка
	""")


@dp.message_handler(commands=['add_t'], state=CS.AVAILABLE)
async def add_t(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, "1️⃣ Введите слово ключ шаблона")
	await state.set_state(CS.ADD_T1)


@dp.message_handler(state=CS.ADD_T1)
async def add_t_key(message: types.Message, state: FSMContext):
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
async def add_t_url(message: types.Message, state: FSMContext):
	# Извлекаем wordkey
	data = await state.get_data()
	wordkey = data.get("WORDKEY")
	# Получаем url
	url = message.text
	st.create_new_row(wordkey, url)
	await bot.send_message(message.chat.id, "✅ Новый шаблон добавлен в базу!")
	await state.set_state(CS.AVAILABLE)


@dp.message_handler(commands=['del_t'], state=CS.AVAILABLE)
async def del_t_msg(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, "Укажите номер шаблона.\nЧтобы узнать номер введите /print_t")
	await state.set_state(CS.DEL_T)


@dp.message_handler(state=CS.DEL_T)
async def del_t_input(message: types.Message, state: FSMContext):
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
		if msg == "/print_t":
			await print_t(message, state)
		else:
			await bot.send_message(message.chat.id, "❌ Неверное значение! Укажите число из списка")


@dp.message_handler(commands=['print_t'], state=[
	CS.AVAILABLE, CS.ADD_T1, CS.ADD_T2,
	CS.ADD_B1, CS.ADD_B2, CS.DEL_T, CS.DEL_B])
async def print_t(message: types.Message, state: FSMContext):
	final_msg = "Список шаблонов\n\n"
	for line in st.get_all_table():
		final_msg += f"{line[0]}. {line[1]} - {line[2]}\n"

	await bot.send_message(message.chat.id, final_msg)


@dp.message_handler(commands=['add_b'], state=CS.AVAILABLE)
async def add_b(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, "1️⃣ Введите слово ключ для чёрного списка")
	await state.set_state(CS.ADD_B1)


@dp.message_handler(state=CS.ADD_B1)
async def add_b_key(message: types.Message, state: FSMContext):
	wordkey = message.text
	# Сохраняем полученное значение
	await state.update_data(WORDKEY=wordkey)
	await state.set_state(CS.ADD_B2)
	await bot.send_message(message.chat.id, "✅ Слово ключ - сохранён!")
	await bot.send_message(message.chat.id, "2️⃣ Введите url для добавления в чёрный список")


@dp.message_handler(state=CS.ADD_B2)
async def add_b_url(message: types.Message, state: FSMContext):
	# Извлекаем wordkey
	data = await state.get_data()
	wordkey = data.get("WORDKEY")
	# Получаем url
	url = message.text
	bl.create_new_row(wordkey, url)
	await bot.send_message(message.chat.id, "✅ Исключение добавлено в чёрный список!")
	await state.set_state(CS.AVAILABLE)


@dp.message_handler(commands=['del_b'], state=CS.AVAILABLE)
async def del_b_msg(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, "Укажите номер исключения для удаления.\nЧтобы узнать номер введите /print_b")
	await state.set_state(CS.DEL_B)


@dp.message_handler(state=CS.DEL_B)
async def del_b_input(message: types.Message, state: FSMContext):
	msg = message.text
	try:
		number_exception = int(msg)
		if number_exception > 0 and number_exception <= bl.get_num_all_rows():
			bl.delete_row_by_number(number_exception)
			await bot.send_message(message.chat.id, "✅ Номер исключения успешно удалён!")
			await state.set_state(CS.AVAILABLE)
		else:
			await bot.send_message(message.chat.id, "❌ Такой номер в чёрном списке отсутсвует. Введите корректный!")
	except:
		if msg == "/print_b":
			await print_b(message, state)
		else:
			await bot.send_message(message.chat.id, "❌ Неверное значение! Укажите число из чёрного списка")


@dp.message_handler(commands=['print_b'], state=[
	CS.AVAILABLE, CS.ADD_T1, CS.ADD_T2,
	CS.ADD_B1, CS.ADD_B2, CS.DEL_T, CS.DEL_B])
async def print_b(message: types.Message, state: FSMContext):
	final_msg = "Чёрный список\n\n"
	for line in bl.get_all_table():
		final_msg += f"{line[0]}. {line[1]} - {line[2]}\n"

	await bot.send_message(message.chat.id, final_msg)


@dp.message_handler(commands=['set_time'], state=CS.AVAILABLE)
async def set_request_interval(message: types.Message, state: FSMContext):
	await bot.send_message(message.chat.id, "Введите интервал запросов ")
	await state.set_state(CS.SET_TIME)


@dp.message_handler(state=CS.SET_TIME)
async def add_b_key(message: types.Message, state: FSMContext):
	delay = int(message.text)
	if delay > 0 and delay < 60:
		Main.set_time(delay)
		await bot.send_message(message.chat.id, """✅ Новый интервал установлен """)
		await state.set_state(CS.AVAILABLE)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)


# start - Запустить бота
# help - Помощь
# set_time - Установить задержку запросов
# add_t - Добавить шаблон поиска
# del_t - Удалить шаблон поиска
# print_t - Вывести все шаблоны поиска
# add_b - Добавить адрес из чёрного списка
# del_b - Удалить адрес из чёрного списка
# print_b - Вывести все адреса чёрного списка
