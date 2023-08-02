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
	return message.from_user.id == config.USER_ID

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
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
