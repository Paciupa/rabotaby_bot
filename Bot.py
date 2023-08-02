import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Файлик с API токеном и id пользователя
import config
bot = Bot(token=config.API_TOKEN)

# MemoryStorage. Храним состояния в оператиной памяти. Заменить на другой тип хранения
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# Определение класса состояний. Состояния нужны для того, чтобы кнопки с одинаковыми названиями, не смогли с друг другом конфликтовать.
# class ClientState(StatesGroup):
# 	ANONYMOUS = State()

# from FastStorage import FstSrg
# fs = FstSrg()

async def is_user_ID(message):
	return message.from_user.id == config.USER_ID

@dp.message_handler(commands=['start'])  
async def cmd_start(message: types.Message):
	await asyncio.sleep(0.5)
	if await is_user_ID(message):
		await bot.send_message(message.chat.id, "Привет!")
	else:
		await bot.send_message(message.chat.id, "Please leave this chat. You're an unregistered user\nПрошу покинуть этот чат. Вы незарегистрированный пользователь")


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
