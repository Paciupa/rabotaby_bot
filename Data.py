import sqlite3
# import threading
import os
from datetime import datetime


# TODO
# Почитать ID в базах данных (уникальные значения)

class Settings:
	""" Example:
		print(Settings.get_query("BL"))
		print(Settings.get_table_name_by_code("gf"))
		print(Settings.get_name_database())
		Settings.set_name_database("database")
		print(Settings.get_name_database())
		print(Settings.is_column_present("BL"))
	"""

	__name_database = "base"

	# Тип хранения значений(кортеж), не изменять. По нему происходит поиск названия столбцов 
	__number = ("number", "INTEGER NOT NULL")
	__key = ("key", "TEXT NOT NULL")
	__url = ("url", "TEXT NOT NULL")
	__lastDateTime = ("lastDateTime", "DATETIME NOT NULL")
	__numberVisits = ("numberVisits", "INTEGER NOT NULL")

	__header = "CREATE TABLE IF NOT EXISTS "

	__database_structure = {
		"ST": {
			"name_table" : "SearchTemplates",
			"column_1" : __number,
			"column_2" : __key,
			"column_3" : __url
			},
		"BL": {
			"name_table" : "BlackList",
			"column_1" : __number,
			"column_2" : __key,
			"column_3" : __url
			},
		"VL": {
			"name_table" : "VisitsList",
			"column_1" : __lastDateTime,
			"column_2" : __numberVisits,
			"column_3" : __url
			}
	}

	@staticmethod
	def get_name_database():
		"""Получить имя файла базы данных"""
		return __class__.__name_database

	@staticmethod
	def set_name_database(new_name):
		"""Установть новое имя для файла базы данных"""
		__class__.__name_database = new_name

	@staticmethod
	def get_list_codes_tables():
		"""Получить список всех кодов для имён таблиц """
		return list(__class__.__database_structure.keys())

	@staticmethod
	def is_column_present(name_column):
		"""Проверяет, существует ли указанный столбец в таблицах"""
		# Извлекаем из текущего класса, все переменные (пары ключ-значения). И оставляем только кортежи
		tuple_used_names = tuple(value for key, value in vars(__class__).items() if isinstance(value, tuple))
		# Извлекаем из кортежей имена таблиц, и записываем в список
		list_all_names_collums = list([name for name, _ in tuple_used_names])
		
		# TODO исправить этот костыль
		if name_column in list_all_names_collums:
			# передаём дальше значение, если всё хорошо
			return name_column
		else:
			print(f"Некорретное имя стобца => {name_column}. Введите один из доступных => {list_all_names_collums}")

	@staticmethod
	def __check_table_code(func):
		def wrapper(table_code, *args):
			"""Проверяем, содержится ли введённый код в списке имён таблиц"""
			if table_code in __class__.get_list_codes_tables():
				return func(table_code, *args)
			else:
				print(f"Некорректный код => {table_code}. Введите один из доступных => {__class__.get_list_codes_tables()}")
		return wrapper

	@__check_table_code
	@staticmethod
	def __get_setting_for_parameter(code_table):
		# Так как "name_table" в списке ключей не нужен, используем срез [1::]
		list_keys_columns = list(__class__.__database_structure[code_table].keys())[1::]
		for key_column in list_keys_columns:
			# Получаем по ключу_столбца кортеж(имя и настройки). Потом собираем в строку с помощью " ".join
			# Пример вывода одной иттерации: "numberVisits INTEGER NOT NULL"
			yield " ".join(__class__.__database_structure[code_table][key_column])

	@__check_table_code
	@staticmethod
	def get_table_name_by_code(table_code):
		"""Получить имя таблицы по коду"""
		return __class__.__database_structure[table_code]['name_table']

	@__check_table_code
	@staticmethod
	def get_query(table_code):
		"""Получить запрос для создания таблицы"""
		# Формируем полную шапку запроса
		full_header = __class__.__header + __class__.get_table_name_by_code(table_code)
		
		## Получаем список всех параметров для запроса
		# Количество параметров для запроса = количество столбцов для каждой таблицы = количество запросов yield
		list_all_parameters = list(i for i in __class__.__get_setting_for_parameter(table_code))

		## Создаём запрос
		# Отделяем параметры запятыми и помещаем в скобки
		# Пример результата: 
		# "CREATE TABLE IF NOT EXISTS BlackList (number INTEGER NOT NULL, key TEXT NOT NULL, url TEXT NOT NULL)"
		query = f"{full_header} ({', '.join(list_all_parameters)})"

		return query

class Base():
	""" """
	def __init__(self):
		self.name_database = Settings.get_name_database()
		# Формируем полное имя с расширением
		self.full_name_database = f"{self.name_database}.db"

		# Если файл базы существует, то
		if self.__check_file_db():
			# просто подключаемся к нему
			self.__connect()
		else:
			# иначе, создаём его с указанным именем и базовыми таблицами
			self.__create_new_file_db()

		# Можно заметить что метод self.__connect вызвается вне зависимости от выполения условия.
		# Да, так и есть. Если разместить метод self.__connect пред условием self.__check_file_db, то выяснить, есть ли внутри файла необходимые таблицы, гораздо сложнее, чем при текущей проверке.
		# Поэтому оставляем такой вариант реализации

	def __check_file_db(self):
		return os.path.isfile(self.name_database)

	def __connect(self):
		self.conn = sqlite3.connect(self.full_name_database)
		self.cursor = self.conn.cursor()

	def saving_changes(self):
		self.conn.commit()

	def __create_new_file_db(self):
		# Создаём новый файл с базой, и подключаемся к нему
		self.__connect()

		# Для каждой таблицы, формируем персональный запрос
		for code_table in Settings.get_list_codes_tables():
			# Создаём таблицу
			self.cursor.execute(Settings.get_query(code_table))
			self.saving_changes()

	def get_num_all_rows(self, code_name_table: str):
		""" """
		name_table = Settings.get_table_name_by_code(code_name_table)
		# Получаем количество строк в таблице
		self.cursor.execute(f"SELECT COUNT(*) FROM {name_table}")
		return self.cursor.fetchone()[0]

	def get_all_from_table(self, code_name_table: str):
		"""Получить все данные таблицы"""
		name_table = Settings.get_table_name_by_code(code_name_table)
		self.cursor.execute(f"SELECT * FROM {name_table}")
		return self.cursor.fetchall()

	def get_col_by_name(self, col_name, code_name_table: str):
		"""Возвращает весь столбец по имени"""
		name_table = Settings.get_table_name_by_code(code_name_table)
		self.cursor.execute(f"SELECT {col_name} FROM {name_table}")
		raw_list_of_keys = self.cursor.fetchall()
		return [key[0] for key in raw_list_of_keys]

	def create_new_row(self, name_table, *args):
		"""Создаём новую строку со необходимыми значениями"""
		# Формируем параметры запроса. Пример результата -> (?, ?, ?)
		questions = "?" * len(args)
		query_parameters = f"({', '.join(questions)})"

		# Формируем сам запрос
		query = f"INSERT INTO {name_table} VALUES {query_parameters}"

		# Создаём новую строку
		self.cursor.execute(query, args)
		self.saving_changes()

	def close(self):
		self.saving_changes()
		self.cursor.close()
		self.conn.close()


class SearchTemplates(Base):
	""" """
	__name_table = Settings.get_table_name_by_code("ST")
	# Пред записью в переменную класса, проверяем существует ли такое имя
	__number = Settings.is_column_present("number")

	def create_new_row(self, new_key, new_url):
		number_rows = self.get_num_all_rows()
		# Создаём номер новой строки
		next_number = number_rows + 1
		# Создаём новую строку со необходимыми значениями
		super().create_new_row(__class__.__name_table, next_number, new_key, new_url)

	def delete_row_by_number(self, number):
		"""Удаляем строку по номеру"""
		self.cursor.execute(f"DELETE FROM {__class__.__name_table} WHERE {__class__.__number}=?", (number,))

		self.saving_changes()

		# обновляем нумерацию в столбце number. Так как при удалении появился разрыв в нумерации
		self.__update_col_number()

	def __update_col_number(self):
		"""Обновляем числа в столбце c числами"""
		# Запрос выберет все данные из таблицы, отсортировав строки по значению столбца number.
		self.cursor.execute(f"SELECT * FROM {__class__.__name_table} ORDER BY {__class__.__number}")
		rows = self.cursor.fetchall()

		# Создаём список. От 1 до максимума. Где максимум, это количество строк в таблице
		# Предположу, что использование вот такого варианта list(range(1, len(self.get_num_all_rows())+1)), забирает чуть больше ресурсов.
		# Поэтому реализовал без обращения к методу
		list_new_numbers = list(range(1, len(rows) + 1))
		# Обновите столбец 'number' с новыми значениями
		for new_number in list_new_numbers:
			# Получаем старое значение number в строке, чтобы потом его заменить на новое
			old_number = rows[new_number - 1][0]
			self.cursor.execute(
				f"UPDATE {__class__.__name_table} SET {__class__.__number} = ? WHERE {__class__.__number} = ?",
				(new_number, old_number),
			)

		self.saving_changes()


class BlackList(SearchTemplates):
	""" """
	__name_table = Settings.get_table_name_by_code("BL")


class VisitsList(Base):
	""" """
	__name_table = Settings.get_table_name_by_code("VL")
	# Пред записью в переменную класса, проверяем существует ли такое имя
	__url = Settings.is_column_present("url")
	__numberVisits = Settings.is_column_present("numberVisits")
	__lastDateTime = Settings.is_column_present("lastDateTime")

	def get_current_datetime(self):
		pattern = "%H:%M:%S %d.%m.%Y"
		now = datetime.now()
		return now.strftime(pattern)

	def create_new_row(self, url):
		current_datetime = self.get_current_datetime()
		# Создаём новую строку со необходимыми значениями
		# Так как это список посещений, то при создании новой строки, количество посещений = 1
		super().create_new_row(__class__.__name_table, current_datetime, 1, url)
	
	def get_visits(self, url):
		# Получаем количество посещений по адресу
		self.cursor.execute(
			f"SELECT {__class__.__numberVisits} FROM {__class__.__name_table} WHERE {__class__.__url}=?", (url,)
		)
		return self.cursor.fetchone()[0]

	def update_visits(self, url):
		current_visits = self.get_visits(url)
		current_datetime = self.get_current_datetime()
		
		# Сокращаем длинные имена, для более удобного восприятия строки
		name_table = __class__.name_table
		numberVisits = __class__.__numberVisits
		lastDateTime = __class__.__lastDateTime

		# КоличествоПосещений, Время/Дата последнего посещения, url
		self.cursor.execute(
			f"UPDATE {name_table} SET {numberVisits} = ?, {lastDateTime} = ? WHERE {__class__.__url} = ?",
			(current_visits + 1, current_datetime, url),
		)

		self.saving_changes()
