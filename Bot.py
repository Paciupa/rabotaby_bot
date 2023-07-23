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



# async def start_keyboard_and_message(message, state):
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button = types.KeyboardButton("Начать 🪐")
# 	keyboard.add(button)
# 	# reply_markup=keyboard - это отрисовка клавиатуры. Этот тип клавиатуры нельзя отдельно, без привязки к сообщению, Отправить 🦋 в чат. 
# 	await bot.send_message(message.chat.id, "Поделись с нами моментом из твоей жизни.", reply_markup=keyboard)

# # Так как отрисовка Опубликовать анонимно? используется несколько раз, выносим в отдельную функцию
# async def publish_anonymously(message, state):
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button_yes = types.KeyboardButton("✅ Да")
# 	button_no = types.KeyboardButton("❌ Нет")
# 	button_back = types.KeyboardButton("🔙 Назад")
# 	# Кнопки отрисовываются слева направо в порядке добавления. 
# 	keyboard.add(button_yes, button_no, button_back)
# 	await message.answer("Опубликовать анонимно? (твой никнейм, возраст и пол останутся тайной)", reply_markup=keyboard)
# 	# Устанавливаем состояние в ANONYMOUS, чтобы случано не запускались другие функции
# 	await state.set_state(ClientState.ANONYMOUS)

# @dp.message_handler(text="Начать 🪐")
# async def begin(message: types.Message, state:FSMContext):
# 	await publish_anonymously(message, state)

# # Если state=ClientState. равен другому состоянию, то функция anonymous_answer_yes, не запустится
# # Так же и с остальными функциями
# @dp.message_handler(text=["✅ Да"], state=ClientState.ANONYMOUS)
# async def anonymous_answer_yes(message: types.Message, state:FSMContext):
# 	# Создаём спец переменную ANON=True для пользователя, чтобы потом можно было определить какой заголовок для текстового сообщения отправлять #анонимно или #Киборг-Убийца #мужской #31
# 	await state.update_data(ANON=True)
# 	# Устанавливаем состояние в ANONYMOUS_YES, чтобы при нажатии кнопки "🔙 Назад" мы вернулись не в регистрацию, а к вопросу "Опубликовать анонимно?..."
# 	await state.set_state(ClientState.ANONYMOUS_YES)
# 	# переходим на этап, когда пользователь пишет свою историю
# 	await recording_history(message, state)

# @dp.message_handler(text="🔙 Назад", state=ClientState.ANONYMOUS)
# async def back_to_start(message: types.Message, state:FSMContext):
# 	# Отрисовываем стартовое сообщение, без приветствия
# 	await start_keyboard_and_message(message, state)
# 	# Сбрасываем все состояния. Тут надо это????
# 	await state.finish()

# @dp.message_handler(text=["❌ Нет"], state=ClientState.ANONYMOUS)
# async def anonymous_answer_no(message: types.Message, state:FSMContext):

# 	await state.update_data(ANON=False)

# 	user_id = int(message.from_user.id)
# 	if db.check_user_id(user_id):
# 		# если есть пользователь в локальной базе, то извлекаем его данные и сохраняем во временное хранилище, чтобы не делать лишние запросы в базу
# 		nickname = db.get_cell(user_id, "nickname")
# 		await state.update_data(NICKNAME=nickname)

# 		gender = db.get_cell(user_id, "gender")
# 		await state.update_data(GENDER=gender)

# 		age = db.get_cell(user_id, "age")
# 		await state.update_data(AGE=age)

# 		await state.set_state(ClientState.USER_FOUND)
# 		await message.answer(f"Добро пожаловать, {nickname}! Давно не виделись.")
# 		# переходим на этап, когда пользователь пишет свою историю
# 		await recording_history(message, state)
# 	else:
# 		await registration_keyboard_and_messages(message, state)

# async def registration_keyboard_and_messages(message, state, аdditional_text="❗️ Регистрация"):
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button = types.KeyboardButton("🔙 Назад")
# 	keyboard.add(button)
# 	await message.answer(аdditional_text)
# 	await message.answer("1️⃣  Твой никнейм (создаётся один раз, больше 2 и меньше 16 символов):",  reply_markup=keyboard)
# 	await state.set_state(ClientState.USER_NOT_FOUND)

# @dp.message_handler(text="🔙 Назад", state=ClientState.USER_NOT_FOUND)
# async def back_to_publish_anonymously(message: types.Message, state:FSMContext):
# 	await publish_anonymously(message, state)

# async def gender_keyboard_and_messages(message, state):
# 	await state.set_state(ClientState.SET_NICKNAME)
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button_male = types.KeyboardButton("♂ Мужской")
# 	button_female = types.KeyboardButton("♀ Женский")
# 	# button_another = types.KeyboardButton("⚥,⚧,⚦,NB,∅ Другой")
# 	button_back = types.KeyboardButton("🔙 Назад")
# 	keyboard.add(button_male, button_female, button_back) # убрал кнопку button_another
# 	await message.answer("2️⃣ Твой пол:",  reply_markup=keyboard)

# @dp.message_handler(state=ClientState.USER_NOT_FOUND)
# async def nickname_processing(message: types.Message, state:FSMContext):
# 	nickname = message.text
# 	# проверка никнейма на длину
# 	if len(nickname) > 2 and len(nickname) < 16:
# 		# Записываем во временное хранилище никнейм
# 		await state.update_data(NICKNAME=nickname)
# 		# parse_mode="HTML" позволяет дополнительно форматировать текст
# 		# <i></i> - это надпись курсивом
# 		# <b></b> - это жирная надпись
# 		await message.answer(f"✅ Установлен никнейм <i>{nickname}</i>!", parse_mode="HTML")
# 		# переходим к выбору пола(гендера)
# 		await gender_keyboard_and_messages(message, state)
# 	else:
# 		# Так как код для регистрации и для некорректного ввода, практически идентичен, поэтому используем функцию регистрации, чтобы отрисовать всё необходимое. 
# 		# Но вместо сообщения "Регистрация", вставляем "Некорректный никнейм!"
# 		await registration_keyboard_and_messages(message, state, "❌ Некорректный никнейм!")

# @dp.message_handler(text="🔙 Назад", state=ClientState.SET_NICKNAME)
# async def back_to_registration(message: types.Message, state:FSMContext):
# 	await registration_keyboard_and_messages(message, state)

# # Объеденённая функция для всех (гендер)кнопок
# @dp.message_handler(text=["♂ Мужской", "♀ Женский"], state=ClientState.SET_NICKNAME)
# async def change_gender(message: types.Message, state: FSMContext):
# 	gender_text = message.text

# 	# Чтобы в локальную базу не отправлять лишние символы, обрежем с помощью регулярных выражений
# 	import re
# 	clear_gender_text = re.sub('[^а-яА-Я\s]', '', gender_text)
# 	# А после удалим лишние пробелы(strip) и сделаем все буквы маленькими(lower)
# 	gender_text = clear_gender_text.strip().lower()

# 	await state.update_data(GENDER=message.text[2])
# 	await message.answer(f"✅ Установлен <i>{gender_text}</i> пол!", parse_mode="HTML")

# 	await age_keyboard_and_message(message, state)

# async def age_keyboard_and_message(message, state):
# 	await state.set_state(ClientState.SET_GENDER)
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	button_back = types.KeyboardButton("🔙 Назад")
# 	keyboard.add(button_back)
# 	await message.answer("3️⃣ Твой возраст (2-99):",  reply_markup=keyboard)

# async def get_string_age(age):
# 	# Так как из-за числа изменяется произношение, поэтому обрабатываем все варианты
# 	# пример1: Установлен двадцать один год
# 	# пример2: Установлено сорок четыре года
# 	# пример3: Установлено тридцать девять лет
# 	basic_text = "✅ Установлен"
# 	if age in range(11, 15):
# 		# 11 - 14 лет, это исключения из правил, поэтому пишем перед всеми условиями
# 		return f"{basic_text}о <i>{age}</i> лет!"
# 	elif age % 10 == 1:
# 		# остаток от деления на 10 равно 1
# 		return f"{basic_text} <i>{age}</i> год!"
# 	elif age % 10 in range(2, 5):
# 		# остаток от деления на 10 от 2 до 4
# 		return f"{basic_text}о <i>{age}</i> года!"
# 	else:
# 		return f"{basic_text}о <i>{age}</i> лет!"

# async def save_user_data(message, state):
# 	user_id = str(message.from_user.id)
# 	first_name = str(message.from_user.first_name)
# 	last_name = str(message.from_user.last_name)
# 	username = str(message.from_user.username)

# 	# извлекаем необходимые данные из временного хранилища
# 	data = await state.get_data()
# 	nickname = data.get("NICKNAME")
# 	gender = data.get("GENDER")
# 	age = data.get("AGE")

# 	# проверка. есть ли пользователь в локальной базе. Если есть, то данные перезапишутся
# 	if not db.check_user_id(user_id):
# 		# создаём новую строку в локальной базе. И записываем туда все значения
# 		db.create_string(user_id, first_name, last_name, username, nickname, gender, age)
# 	else:
# 		db.set_sell(user_id, "first_name", first_name)
# 		db.set_sell(user_id, "last_name", last_name)
# 		db.set_sell(user_id, "username", username)
# 		db.set_sell(user_id, "nickname", nickname)
# 		db.set_sell(user_id, "gender", gender)
# 		db.set_sell(user_id, "age", age)

# @dp.message_handler(state=ClientState.SET_GENDER)
# async def age_processing(message: types.Message, state:FSMContext):
# 	msg = message.text
# 	if msg != "🔙 Назад":
# 		try:
# 			# преобразуем запись в число
# 			age = int(msg)
# 			if age > 1 and age < 100:
# 				await state.update_data(AGE=age)

# 				# Формируем строку подтверждения
# 				# пример3: Установлено 35 лет
# 				string = await get_string_age(age)
# 				# так как в сформированной строке есть <i></i>, поэтому указываем parse_mode="HTML"
# 				await message.answer(string, parse_mode="HTML")

# 				# Окончание регистрации. Все данные пользователя сохраняются в локальную базу
# 				await save_user_data(message, state)

# 				await state.set_state(ClientState.SET_AGE)
# 				# переходим на этап, когда пользователь пишет свою историю
# 				await recording_history(message, state)
# 			else:
# 				await message.answer("❌ Некорректный возраст!")
# 				await age_keyboard_and_message(message, state)
# 		except:
# 			await message.answer("❌ Некорректный возраст!")
# 			await age_keyboard_and_message(message, state)
# 	else:
# 		await gender_keyboard_and_messages(message, state)

# @dp.message_handler(text="🔙 Назад", state=[ClientState.SET_AGE, ClientState.ANONYMOUS_YES, ClientState.USER_FOUND])
# async def back_to_different_directions(message: types.Message, state:FSMContext):
# 	# Удаляем пользователя из быстрой базы, если он возвращается 🔙 Назад
# 	user_id = str(message.from_user.id)
# 	await fs.del_user(user_id)

# 	# в зависимости от текущего статуса, кнопка 🔙 Назад ведёт ...
# 	current_status = await state.get_state()
# 	if current_status == "ClientState:SET_AGE":
# 		# ... или в вопросу о возрасте(этап регистрации),
# 		await age_keyboard_and_message(message, state)
# 	elif current_status == "ClientState:ANONYMOUS_YES" or current_status == "ClientState:USER_FOUND":
# 		# ... или к вопросу "Опубликовать анонимно?...",
# 		await publish_anonymously(message, state)

# ################################

# async def recording_history(message: types.Message, state:FSMContext):
# 	# создаём нового пользователя в быстрой базе
# 	await fs.create_new_user(str(message.from_user.id))
# 	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 	send_moderator = types.KeyboardButton("Поделиться 🦋")
# 	button_back = types.KeyboardButton("🔙 Назад")
# 	keyboard.add(send_moderator, button_back)
# 	# await message.answer("❗️ Просьба. Файлы, фотографии, аудиозаписи, и др. отправляй ОТДЕЛЬНО от текста истории ❗️ ")1️⃣
# 	# await message.answer("Удалённые сообщения, всё-равно отправляются на модерацию ")
# 	await message.answer("1️⃣ Отправь сообщение с текстом.\n\n2️⃣ Отправь аудиозапись, по желанию.\n\n3️⃣ Нажми на кнопку 'Поделиться' после завершения.\n\nКнопки автоматически скрываются в меню кнопок при наборе текста.")
# 	# await message.answer("Нажми кнопку 'Отправить запись на модерацию' после завершения.\n Кнопка автоматически скрывается в меню кнопок при наборе текста.", reply_markup=keyboard)
# 	await message.answer("Твой момент:", reply_markup=keyboard) 

# # Обновление данных. Если пользователь отправил сообщение, а потом изменил, то данная функция перезапишет зачения в быстрой базе 
# @dp.edited_message_handler(content_types=["text", "photo", "document"], state=[ClientState.SET_AGE, ClientState.ANONYMOUS_YES, ClientState.USER_FOUND])
# async def update_text(message: types.Message, state: FSMContext):
# 	user_id = str(message.from_user.id)
# 	msg_id = str(message.message_id)
# 	type_msg = message.content_type
# 	await fs.update_obj_from_id(user_id, type_msg, msg_id, message)

# @dp.message_handler(content_types=["text"], state=[ClientState.SET_AGE, ClientState.ANONYMOUS_YES, ClientState.USER_FOUND])
# async def save_text(message: types.Message, state: FSMContext):
# 	user_id = str(message.from_user.id)
# 	msg_id = str(message.message_id)
# 	type_msg = message.content_type
# 	text = message.text
# 	if text != "Поделиться 🦋":
# 		await fs.add_obj_to(user_id, type_msg, msg_id, message)
# 	else:
# 		await state.set_state(ClientState.SEND_MODERATOR)
# 		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# 		button = types.KeyboardButton("Вернуться в начало 🏕")
# 		keyboard.add(button)
# 		await message.answer("Спасибо! Запись будет опубликована после модерации в порядке очереди.",reply_markup=keyboard)
# 		await send_to_moderator(message, state)

# @dp.message_handler(text="Вернуться в начало 🏕", state=ClientState.SEND_MODERATOR)
# async def new_story(message: types.Message, state:FSMContext):
# 	await starting_message(message, state)

# async def get_header_for_msg(message, state):
# 	# получаем из временного хранилища переменную ANON, и проверяем на истинность
# 	data = await state.get_data()
# 	anon = data.get("ANON")
# 	if anon:
# 		return "#moment\n#анонимно\n"
# 	else:
# 		user_id = str(message.from_user.id)
# 		# получаем по id пользователя, данные о регистрации
# 		nickname = db.get_cell(user_id, "nickname")
# 		gender = db.get_cell(user_id, "gender")
# 		age = db.get_cell(user_id, "age")

# 		# Формируем порядок данных в заголовке
# 		string = f"#moment\n#{nickname} #{gender} #{age}\n"
# 		return string
		
# async def send_to_moderator(message, state):
# 	user_id = str(message.from_user.id)
# 	moderator_id = config.ID_MODERATOR
# 	# список из типов, которые поддерживаются этим ботом
# 	list_types_messages = ["text", "photo", "audio", "voice", "video_note", "document", "location"]
# 	for type_message in list_types_messages:
# 		# Получаем список объектов, по id и по типу
# 		# Если тип это "photo", то извлекаем из быстрой базы(FastStorage)
# 		list_obj = await fs.get_list_objs(user_id, type_message)

# 		# Например: пользователь отправил в бота только фото и голосовые. Значит в остальных пункты, будут пустые. И чтобы лишний раз не проходить все проверки, создано такое условие
# 		if list_obj != []:
# 			if type_message == "text" and block_text == False:
# 				# получаем заголовок, и вставлеяем в первое текстовое сообщение
# 				# Пример заголовка 1: #анонимно
# 				# Пример заголовка 2: #ТонниСтарк #мужской #73
# 				header_msg = await get_header_for_msg(message, state)
# 				# await bot.send_message(chat_id=moderator_id, text=header_msg)

# 				# enumerate - это счётчик сообщений
# 				for num_msg, obj in enumerate(list_obj):
# 					# Так как заголовок должен быть только в первом сообщении(индекс 0), делаем проверку
# 					if num_msg == 0:
# 						# Вставляем заголовок внутрь первого сообщения
# 						obj.text = f"{header_msg}\n{obj.text}"
# 					# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 					# Костыль из try/except(это не толко для "text", но и далее по коду) нужен для частичной обработки удалённых сообщений.
# 					# если пользователь удалил сообщение, то в боте всёравно оно остаётся. И быстрой базе тоже. Обработка удаленого сообщения, пока невозможна.
# 					# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 					try:
# 						# Остальные сообщения отправляются без заголовка
# 						await bot.send_message(chat_id=moderator_id, text=obj.text)
# 					except:
# 						# pass это код-заглушка. Ничего не выполняет. Просто её иногда ставят при псевдокоде
# 						pass

# 			if type_message == "photo" and block_photo == False:
# 				for obj in list_obj:
# 					try:
# 						# так как телеграмм сжимает изображения, он предоставляет 3 типа качества. 
# 						# Выбираем самый лучший
# 						photo_ = obj.photo[-1]
# 						media = [types.InputMediaPhoto(media=photo_.file_id, caption=obj.caption)]
# 						await bot.send_media_group(chat_id=moderator_id, media=media)
# 					except:
# 						pass

# 			if type_message == "audio" and block_audio == False:
# 				for obj in list_obj:
# 					try:
# 						await bot.send_audio(chat_id=moderator_id, audio=obj.audio.file_id)
# 					except:
# 						pass

# 			if type_message == "voice" and block_voice == False:
# 				for obj in list_obj:
# 					try:
# 						await bot.send_voice(chat_id=moderator_id, voice=obj.voice.file_id)
# 					except:
# 						pass

# 			if type_message == "video_note" and block_video_note == False:
# 				for obj in list_obj:
# 					try:
# 						await bot.send_video_note(chat_id=moderator_id, video_note=obj.video_note.file_id)
# 					except:
# 						pass

# 			if type_message == "document" and block_document == False:
# 				for obj in list_obj:
# 					try:
# 						await bot.send_document(chat_id=moderator_id, document=obj.document.file_id, caption=obj.caption)
# 					except:
# 						pass

# 			if type_message == "location" and block_location == False:
# 				for obj in list_obj:
# 					try:
# 						latitude = obj.location.latitude
# 						longitude = obj.location.longitude
# 						await bot.send_location(chat_id=moderator_id, latitude=latitude, longitude=longitude)
# 					except:
# 						pass

# 	# удаляем пользователя и все его данные из быстрой базы
# 	await fs.del_user(user_id)

# ## Cохранение сообщения в быструю базу данных
# @dp.message_handler(content_types=["photo", "audio", "voice", "video_note", "document", "location"], state=[ClientState.SET_AGE, ClientState.ANONYMOUS_YES, ClientState.USER_FOUND])
# async def save_all(message: types.Message, state: FSMContext):
# 	user_id = str(message.from_user.id)
# 	msg_id = str(message.message_id)
# 	type_msg = message.content_type
# 	await fs.add_obj_to(user_id, type_msg, msg_id, message)

# if __name__ == "__main__":
# 	# запуск скрипта
# 	executor.start_polling(dp, skip_updates=True)