import sqlite3
# import threading
import os
from datetime import datetime


# TODO
# Почитать ID в базах данных (уникальные значения)

class Base:
class Settings:
	""" Example:
		print(Settings.get_query("BL"))
		print(Settings.get_table_name_by_code("gf"))
		print(Settings.get_name_database())
		Settings.set_name_database("database")
		print(Settings.get_name_database())
	"""

	__name_database = "base"

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
		""" """
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


	""" """
	def __init__(self, name_file):
		# !!!!!!!!!!!!!!!!
		# функция __connect вызывается всегда(и при создании нового файла, и при его наличии)
		# написать проверку структуры. Если структуры нет(т.е. файл был только что создан), то нужно создать необходимую. А если есть структура, то пропускаем
		# !!!!!!!!!!!!!!!!
		# Если файл базы существует, то
		if self.__check_file_db(name_file):
			pass
			# просто подключаемся к нему
			# self.__connect(name_file)
		else:
			# иначе, создаём его с указанным именем
			self.__create_new_file_db(name_file)

	def __check_file_db(self, name_file):
		return os.path.isfile(name_file)

	def __connect(self, name_file):
		self.conn = sqlite3.connect(name_file)
		self.cursor = self.conn.cursor()

	def saving_changes(self):
		self.conn.commit()

	def __create_new_file_db(self, name_file):
		# Создаём новый файл с базой, и подключаемся к нему
		# self.__connect(name_file)

		# формируем специальную структуру базы
		self.cursor.execute(self.create_table_query)
		self.saving_changes()

	def get_num_all_rows(self, name_table="urls"):
		# Получаем количество строк в таблице
		self.cursor.execute(f"SELECT COUNT(*) FROM {name_table}")
		return self.cursor.fetchone()[0]

	# Пока не используется
	def get_num_all_cols(self, name_table="urls"):
		# Получаем количество столбцов в таблице
		self.cursor.execute(f"PRAGMA table_info('{name_table}')")
		return len(self.cursor.fetchall())

	def get_all_table(self, name_table="urls"):
		self.cursor.execute(f"SELECT * FROM {name_table}")
		return self.cursor.fetchall()

	def get_col_by_name(self, col_name, name_table="urls"):
		""" Возвращает весь столбец по имени """
		self.cursor.execute(f"SELECT {col_name} FROM {name_table}")
		raw_list_of_keys = self.cursor.fetchall()
		return [key[0] for key in raw_list_of_keys]

	def close(self):
		self.saving_changes()
		self.cursor.close()
		self.conn.close()


class SearchTemplates(Base):
	""" """
	create_table_query = """
		CREATE TABLE IF NOT EXISTS urls (
			number INTEGER NOT NULL,
			key TEXT NOT NULL,
			url TEXT NOT NULL);
		"""

	def create_new_row(self, new_key, new_url, name_table="urls"):
		number_rows = self.get_num_all_rows()
		# Создаём номер новой строки
		next_number = number_rows + 1
		# Создаём новую строку со необходимыми значениями
		self.cursor.execute(f"INSERT INTO {name_table} VALUES (?, ?, ?)", (next_number, new_key, new_url))
		self.saving_changes()

	def delete_row_by_number(self, number, name_table="urls"):
		""" Удаляем строку по номеру """
		self.cursor.execute(f"DELETE FROM {name_table} WHERE number=?", (number,))

		self.saving_changes()

		# обновляем нумерацию в столбце num. Так как при удалении появился разрыв в нумерации
		self.__update_col_num()

	def __update_col_num(self, name_table="urls"):
		""" Обновляем числа в столбце num """
		# Запрос выберет все данные из таблицы, отсортировав строки по значению столбца num.
		self.cursor.execute(f"SELECT * FROM {name_table} ORDER BY number")
		rows = self.cursor.fetchall()

		# Создаём список. От 1 до максимума. Где максимум, это количество строк в таблице
		# Предположу, что использование вот такого варианта list(range(1, len(self.get_num_all_rows())+1)), забирает чуть больше ресурсов.
		# Поэтому реализовал без обращения к методу
		list_new_numbers = list(range(1, len(rows) + 1))
		# Обновите столбец 'number' с новыми значениями
		for new_number in list_new_numbers:
			# получаем старое значение num в строке, чтобы потом его заменить на новое
			old_number = rows[new_number - 1][0]
			self.cursor.execute(f"UPDATE {name_table} SET number = ? WHERE number = ?", (new_number, old_number))

		self.saving_changes()


class BlackList(SearchTemplates):
	""" """
	pass


class VisitsList(Base):
	""" """
	create_table_query = """
		CREATE TABLE IF NOT EXISTS urls (
			dateTime TEXT NOT NULL,
			visits INTEGER NOT NULL,
			url TEXT NOT NULL);
		"""

	def get_current_datetime(self):
		pattern = "%H:%M:%S %d.%m.%Y"
		now = datetime.now()
		return now.strftime(pattern)

	def create_new_row(self, url, name_table="urls"):
		current_datetime = self.get_current_datetime()
		# Создаём новую строку со необходимыми значениями
		# Так как это список посещений, то при создании новой строки, количество посещений = 1
		self.cursor.execute(f"INSERT INTO {name_table} VALUES (?, ?, ?)", (current_datetime, 1, url))
		self.saving_changes()

	def get_visits(self, url, name_table="urls"):
		# Получаем количество посещений по адресу
		self.cursor.execute(f"SELECT visits FROM {name_table} WHERE url=?", (url,))
		return self.cursor.fetchone()[0]

	def update_visits(self, url, name_table="urls"):
		current_visits = self.get_visits(url)
		current_datetime = self.get_current_datetime()
		# Переделать названия для столбцов
		# КоличествоПосещений, Время/Дата последнего посещения, url
		self.cursor.execute(f"UPDATE {name_table} SET visits = ?, dateTime = ? WHERE url = ?",
			(current_visits + 1, current_datetime, url))

		self.saving_changes()


