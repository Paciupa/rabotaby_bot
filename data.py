# import threading  # noqa: ERA001, D100
from datetime import datetime, timedelta
from os import environ

import psycopg2


class Settings:
	"""
	A class for managing database connection settings and constructing SQL queries for table creation.
	It interacts with environment variables to retrieve connection parameters and provides methods for table and column management.

	Example Usage:
	print(Settings.get_query("BL"))
	print(Settings.get_table_name_by_code("gf"))
	print(Settings.get_name_database())
	Settings.set_name_database("database")
	print(Settings.get_name_database())
	print(Settings.is_column_present("BL"))

	print(Settings.get_db_connection_parameters())
	print(Settings.get_db_connection_parameters(True))
	print(Settings.get_db_connection_parameters())
	"""  # noqa: D400, D415

	# Подключение к базе данных

	# Достаём из переменных окружения все необходимые параметры для базы данных
	__db_host = environ.get("DB_HOST")
	__db_port = environ.get("DB_PORT")
	__db_name = environ.get("DB_NAME")
	__db_user = environ.get("DB_USER")
	__db_password = environ.get("DB_PASSWORD")

	__db_connection_parameters = {  # noqa: RUF012
		"host": __db_host,
		"port": __db_port,
		"database": __db_name,
		"user": __db_user,
		"password": __db_password,
	}

	# Формирование базы данных

	# Тип хранения значений(кортеж), не изменять. По нему происходит поиск названия столбцов # noqa: E501, ERA001
	__number = ("number", "INTEGER NOT NULL")
	__key = ("key", "TEXT NOT NULL")
	__url = ("url", "TEXT NOT NULL")
	__lastDateTime = ("last_date_time", "TIMESTAMP NOT NULL")
	__included = ("included", "BOOLEAN NOT NULL")

	__header = "CREATE TABLE IF NOT EXISTS "

	__database_structure = {  # noqa: RUF012
		"ST": {
			"name_table": "search_templates",
			"column_1": __number,
			"column_2": __key,
			"column_3": __url,
			"column_4": __included,
		},
		"BL": {
			"name_table": "black_list",
			"column_1": __number,
			"column_2": __key,
			"column_3": __url,
			"column_4": __included,
		},
		"VL": {
			"name_table": "visits_list",
			"column_1": __lastDateTime,
			"column_2": __key,
			"column_3": __url,
		},
	}

	@classmethod
	def get_name_database(cls):
		"""
		Returns the name of the database file.

		Example:
			print(Settings.get_name_database())

		Returns:
			str: The name of the database as set in the environment variable `DB_NAME`.
		"""
		return cls.__db_name

	@classmethod
	def get_db_connection_parameters(cls, without_database=False):  # noqa: FBT002
		"""
		Returns a dictionary of database connection parameters, optionally excluding the database name.

		Args:
			without_database (bool): If True, excludes the database name from the connection parameters.

		Example:
			print(Settings.get_db_connection_parameters())
			print(Settings.get_db_connection_parameters(True))

		Returns:
			dict: A dictionary of database connection parameters, possibly excluding the `database` key.
		"""
		if without_database:
			# Creates a copy to avoid modifying the original dictionary
			copy_db_conn_param = cls.__db_connection_parameters.copy()
			# Removes the 'database' parameter if requested
			del copy_db_conn_param["database"]
			return copy_db_conn_param

		return cls.__db_connection_parameters

	@classmethod
	def get_list_codes_tables(cls):
		"""
		Returns a list of all table codes.

		Example:
			print(Settings.get_list_codes_tables())

		Returns:
			list: A list of strings representing the table codes (e.g., ["ST", "BL", "VL"]).
		"""
		return list(cls.__database_structure.keys())

	@classmethod  # noqa: RET503
	def is_column_present(cls, name_column):
		"""
		Checks if the specified column name exists in any of the tables.

		Args:
			name_column (str): The column name to check.

		Example:
			print(Settings.is_column_present("BL"))

		Returns:
			str: The column name if it exists in any table, else prints an error message.
		"""
		# Extracting column names from all tables
		tuple_used_names = tuple(
			value for key, value in vars(cls).items() if isinstance(value, tuple)
		)
		# Извлекаем из кортежей имена таблиц, и записываем в список
		list_all_names_columns = list([name for name, _ in tuple_used_names])  # noqa: C411

		# TODO исправить этот костыль  # noqa: ERA001, FIX002, TD002, TD003, TD004
		if name_column in list_all_names_columns:
			# передаём дальше значение, если всё хорошо
			return name_column
		else:  # noqa: RET505
			print(
				f"Некорректное имя столбца => {name_column}. Введите один из доступных => {list_all_names_columns}"  # noqa: E501
			)

	@classmethod
	def __check_table_code(cls, table_code):
		"""
		Verifies if the given table code exists in the database structure.

		Args:
			table_code (str): The code for the table to check.

		Example:
			table_code = "BL"
			print(Settings.__check_table_code(table_code))

		Returns:
			str: The table code if valid, else prints an error message.
		"""
		try:
			# Делаем тестовый запрос
			_ = cls.__database_structure[table_code]
			# Если такой табличный код существует, то возвращаем его для дальнейших взаимодействий
			return table_code  # noqa: TRY300
		except KeyError:
			print(
				f"Некорректный код => {table_code}. Введите один из доступных => {cls.get_list_codes_tables()}"  # noqa: E501
			)

	@classmethod
	def __get_setting_for_parameter(cls, table_code):
		"""
		Yields the SQL column definition for each column in the specified table code.

		Args:
			table_code (str): The code for the table to get column settings.

		Yields:
			str: Each column definition as a string (e.g., "number INTEGER NOT NULL").
		"""
		table_code = cls.__check_table_code(table_code)
		# Так как "name_table" в списке ключей не нужен, используем срез [1::]  # noqa: ERA001
		list_keys_columns = list(cls.__database_structure[table_code].keys())[1::]
		for key_column in list_keys_columns:
			# Получаем по ключу_столбца кортеж(имя и настройки). Потом собираем в строку с помощью " ".join  # noqa: ERA001, E501
			# Пример вывода одной итерации: "numberVisits INTEGER NOT NULL"  # noqa: ERA001
			yield " ".join(cls.__database_structure[table_code][key_column])

	@classmethod
	def get_table_name_by_code(cls, table_code):
		"""
		Returns the name of the table corresponding to the given table code.

		Args:
			table_code (str): The code of the table to fetch the name for.

		Example:
			print(Settings.get_table_name_by_code("BL"))

		Returns:
			str: The name of the table (e.g., "black_list").
		"""
		table_code = cls.__check_table_code(table_code)
		return cls.__database_structure[table_code]["name_table"]

	@classmethod
	def get_query(cls, table_code):
		"""
		Constructs and returns a SQL query for creating a table based on the table code.

		Args:
			table_code (str): The code of the table to generate the SQL query for.

		Example:
			print(Settings.get_query("BL"))

		Returns:
			str: The SQL query for creating the table.
		"""
		table_code = cls.__check_table_code(table_code)
		# Формируем полную шапку запроса
		full_header = cls.__header + cls.get_table_name_by_code(table_code)

		# Получаем список всех параметров для запроса
		# Количество параметров для запроса = количество столбцов для каждой таблицы = количество запросов yield # noqa: ERA001, E501
		list_all_parameters = list(i for i in cls.__get_setting_for_parameter(table_code))  # noqa: C400

		# Создаём запрос
		# Отделяем параметры запятыми и помещаем в скобки
		# Пример результата:  # noqa: ERA001
		# "CREATE TABLE IF NOT EXISTS BlackList (number INTEGER NOT NULL, key TEXT NOT NULL, url TEXT NOT NULL)"  # noqa: ERA001, E501
		# Constructing the full SQL query
		query = f"{full_header} ({', '.join(list_all_parameters)})"

		return query  # noqa: RET504


class Base:
	""" """  # noqa: D419

	def __init__(self, table_code):  # noqa: D107
		self.all_parameters = Settings.get_db_connection_parameters()
		self.parameters_without_database = Settings.get_db_connection_parameters(
			without_database=True
		)
		self.db_name = Settings.get_name_database()

		self.table_code = table_code
		self.name_table = Settings.get_table_name_by_code(self.table_code)
		self.number = Settings.is_column_present("number")

		# Если базы данных не существует, то создаём её
		self.database_exists()

		# Если указанной таблицы не существует, то создаём её
		self.table_exists(self.table_code)

		self.connect_to_database(self.all_parameters)

	def saving_changes(self):  # noqa: D102
		self.connection.commit()

	# noinspection PyAttributeOutsideInit
	def connect_to_database(self, parameters_database):
		"""Подключаемся к базе данных."""
		self.connection = psycopg2.connect(**parameters_database)
		self.cursor = self.connection.cursor()

	def database_exists(self):
		"""Создание новой базы данных, если её не существует."""
		self.connect_to_database(self.parameters_without_database)
		try:
			self.connection.set_session(autocommit=True)
			# Создание пустой базы данных
			self.cursor.execute(f"CREATE DATABASE {self.db_name};")
			print(f"База данных '{self.db_name}' создана успешно.")

		except psycopg2.errors.DuplicateDatabase:
			# Если база данных уже создана, то ошибку не выводим,
			# а возвращаем базу данных к состоянию до выполнения запроса
			self.connection.rollback()
		except Exception as e:  # noqa: BLE001
			# Обработка остальных ошибок при создании базы данных
			print(f"Ошибка при создании базы данных: {e}")
			# Возвращаем базу данных к состоянию до выполнения запроса
			self.connection.rollback()
		finally:
			self.close()

	def table_exists(self, table_code):  # noqa: D102
		# Формируем таблицу по указанному коду
		self.connect_to_database(self.all_parameters)

		self.cursor.execute(Settings.get_query(table_code))
		self.saving_changes()

	def get_num_all_rows(self):
		""" """  # noqa: D419
		# Получаем количество строк в таблице
		self.cursor.execute(f"SELECT COUNT(*) FROM {self.name_table}")  # noqa: S608
		return self.cursor.fetchone()[0]

	def get_all_from_table(self):
		"""Получить все данные таблицы."""
		print(self.name_table)
		self.cursor.execute(f"SELECT * FROM {self.name_table}")  # noqa: S608
		return self.cursor.fetchall()

	def get_col_by_name(self, col_name):
		"""Возвращает весь столбец по имени."""
		self.cursor.execute(f"SELECT {col_name} FROM {self.name_table}")  # noqa: S608
		raw_list_of_keys = self.cursor.fetchall()
		return [key[0] for key in raw_list_of_keys]

	def create_new_row(self, name_table, *args):
		"""Создаём новую строку с необходимыми значениями."""
		# Формируем параметры запроса. Пример результата -> ('%s', '%s', '%s')  # noqa: ERA001
		placeholders = ["%s"] * len(args)
		query_parameters = f"({', '.join(placeholders)})"

		# Формируем сам запрос
		query = f"INSERT INTO {name_table} VALUES {query_parameters}"  # noqa: S608

		# Создаём новую строку
		self.cursor.execute(query, args)
		self.saving_changes()

	def delete_row_by_value(self, name_row, value):
		"""Удаляем строку/строки по значению в столбце."""
		self.cursor.execute(f"DELETE FROM {self.name_table} WHERE {name_row}=%s", (value,))  # noqa: S608

		self.saving_changes()

	def close(self):  # noqa: D102
		self.saving_changes()
		self.cursor.close()
		self.connection.close()


class SearchTemplates(Base):
	""" """  # noqa: D419

	def __init__(self):  # noqa: D107
		super().__init__(table_code="ST")
		self.key = Settings.is_column_present("key")
		self.included = Settings.is_column_present("included")

	# noinspection PyMethodOverriding
	def create_new_row(self, new_key, new_url, is_included=True):  # noqa: FBT002, D102
		number_rows = self.get_num_all_rows()
		# Создаём номер новой строки
		next_number = number_rows + 1
		# Создаём новую строку с необходимыми значениями
		super().create_new_row(self.name_table, next_number, new_key, new_url, is_included)
		self.__update_col_number()

	def delete_row_by_number(self, number):
		"""Удаляем строку по номеру."""
		super().delete_row_by_value(self.number, number)

		# Обновляем нумерацию в столбце number, так как при удалении появился разрыв в нумерации
		self.__update_col_number()

	def __update_col_number(self):
		"""Обновляем числа в столбце с числами."""
		# Запрос выберет все данные из таблицы, отсортировав строки по значению столбца number.
		self.cursor.execute(f"SELECT * FROM {self.name_table} ORDER BY {self.number}")  # noqa: S608
		rows = self.cursor.fetchall()

		# Создаём список. От 1 до максимума. Где максимум, это количество строк в таблице
		# Предположу, что использование вот такого варианта list(range(1, len(self.get_num_all_rows())+1)), забирает чуть больше ресурсов.  # noqa: ERA001, E501
		# Поэтому реализовал без обращения к методу
		list_new_numbers = list(range(1, len(rows) + 1))
		# Обновите столбец 'number' с новыми значениями
		for new_number in list_new_numbers:
			# Получаем старое значение number в строке, чтобы потом его заменить на новое
			old_number = rows[new_number - 1][0]
			self.cursor.execute(
				f"UPDATE {self.name_table} SET {self.number} = %s WHERE {self.number} = %s",  # noqa: S608
				(new_number, old_number),
			)

		self.saving_changes()

	def set_states_template(self, number, new_state):
		"""Перезаписываем текущее состояние шаблона/исключения на новое.

		Допускается лишь True/False.
		Если True - то шаблон/исключение используется в поиске
		Если False - то шаблон/исключение не используется в поиске
		"""
		self.cursor.execute(
			f"UPDATE {self.name_table} SET {self.included} = %s WHERE {self.number} = %s",  # noqa: S608
			(new_state, number),
		)
		# Сортируем строки по номеру, так как после изменения состояния, строка смещается(почему?) # noqa: E501, ERA001
		self.__update_col_number()

	def get_key_by_number(self, number_template):
		"""Получить ключ зная номер шаблона."""
		self.cursor.execute(
			f"SELECT {self.key} FROM {self.name_table} WHERE {self.number} = %s;",  # noqa: S608
			(number_template,),
		)
		return self.cursor.fetchone()[0]


class BlackList(SearchTemplates):
	""" """  # noqa: D419

	def __init__(self):  # noqa: D107
		Base.__init__(self, table_code="BL")
		self.included = Settings.is_column_present("included")


class VisitsList(Base):
	""" """  # noqa: D419

	pattern = "%Y-%m-%d %H:%M:%S"

	# Указываем время в часах
	# 1 день = 24  # noqa: ERA001
	# 1 неделя = 168  # noqa: ERA001
	# 1 месяц = 4 недели = 672  # noqa: ERA001
	time_clear = 1344

	def __init__(self):  # noqa: D107
		super().__init__(table_code="VL")
		self.key = Settings.is_column_present("key")
		self.lastDateTime = Settings.is_column_present("last_date_time")

	@classmethod
	def get_pattern(cls):  # noqa: D102
		return cls.pattern

	def get_current_datetime(self):  # noqa: D102
		now = datetime.now()  # noqa: DTZ005
		return now.strftime(self.get_pattern())

	# noinspection PyMethodOverriding
	def create_new_row(self, key, url):  # noqa: D102
		current_datetime = self.get_current_datetime()
		# Создаём новую строку с необходимыми значениями
		super().create_new_row(self.name_table, current_datetime, key, url)

	@classmethod
	def get_time_clear(cls):  # noqa: D102
		return cls.time_clear

	@classmethod
	def set_time_clear(cls, hours):  # noqa: D102
		cls.time_clear = hours

	def delete_rows_after_time(self, key):
		"""Удаляем строки по истечении времени с определённым ключом."""
		# Получаем текущую дату в удобном формате
		current_datetime = datetime.strptime(self.get_current_datetime(), self.get_pattern())  # noqa: DTZ007

		# Определяем временной интервал
		time_threshold = current_datetime - timedelta(hours=self.get_time_clear())

		self.cursor.execute(
			f"DELETE FROM {self.name_table} WHERE {self.key} = %s AND {self.lastDateTime} < %s",  # noqa: S608
			(key, time_threshold),
		)

		self.saving_changes()

	def delete_rows_by_key(self, key):
		"""Удаляем строки по ключу."""
		super().delete_row_by_value(self.key, key)
