import sqlite3

class Base:
	""" """
	def __init__(self, name_file):
		# Если файл базы существует, то
		if self.__check_file_db(name_file):
			# просто подключаемся к нему
			self.__connect(name_file)
		else:
			# иначе, создаём его с указанным именем
			self.__create_new_file_db(name_file)

	def __check_file_db(self, name_file):
		import os
		return os.path.isfile(name_file)

	def __connect(self, name_file):
		self.conn = sqlite3.connect(name_file)
		self.cursor = self.conn.cursor()

	def saving_changes(self):
		self.conn.commit()

	def __create_new_file_db(self, name_file):
		# Создаём новый файл с базой, и подключаемся к нему
		self.__connect(name_file)
			
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
			num INTEGER NOT NULL,
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
		self.cursor.execute(f"DELETE FROM {name_table} WHERE num=?", (number,))

		self.saving_changes()

		# обновляем нумерацию в столбце num. Так как при удалении появился разрыв в нумерации
		self.__update_col_num()

	def __update_col_num(self, name_table="urls"):
		""" Обновляем числа в столбце num """
		# Запрос выберет все данные из таблицы, отсортировав строки по значению столбца num.
		self.cursor.execute(f"SELECT * FROM {name_table} ORDER BY num")
		rows = self.cursor.fetchall()
		
		# Создаём список. От 1 до максимума. Где максимум, это количество строк в таблице
		# Предположу, что использование вот такого варианта list(range(1, len(self.get_num_all_rows())+1)), забирает чуть больше ресурсов.
		# Поэтому реализовал без обращения к методу
		list_new_numbers = list(range(1, len(rows)+1))
		# Обновите столбец 'number' с новыми значениями
		for new_number in list_new_numbers:
			# получаем старое значение num в строке, чтобы потом его заменить на новое
			old_number = rows[new_number-1][0]
			self.cursor.execute(f"UPDATE {name_table} SET num = ? WHERE num = ?", (new_number, old_number))

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
		from datetime import datetime
		pattern = "%H:%M:%S %d.%m.%Y"
		now = datetime.now()
		return now.strftime(pattern)

	def create_new_row(self, url, name_table="urls"):
		dateTime = self.get_current_datetime()
		# Создаём новую строку со необходимыми значениями
		# Так как это список посещений, то при создании новой строки, количество посещений = 1
		self.cursor.execute(f"INSERT INTO {name_table} VALUES (?, ?, ?)", (dateTime, 1, url))
		self.saving_changes()

	def get_visits(self, url, name_table="urls"):
		# Получаем количество посещений по адресу
		self.cursor.execute(f"SELECT visits FROM {name_table} WHERE url=?", (url,))
		return self.cursor.fetchone()[0]

	def update_visits(self, url, name_table="urls"):
		current_visits = self.get_visits(url)
		current_dateTime = self.get_current_datetime()
		self.cursor.execute(f"UPDATE {name_table} SET visits = ?, dateTime = ? WHERE url = ?",
			(current_visits + 1, current_dateTime, url))

		self.saving_changes()
