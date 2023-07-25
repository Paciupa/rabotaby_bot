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

	def __saving_changes(self):
		self.conn.commit()

	def __create_new_file_db(self, name_file):
		# Создаём новый файл с базой, и подключаемся к нему
		self.__connect(name_file)

		create_table_query = """
		CREATE TABLE IF NOT EXISTS urls (
			num INTEGER NOT NULL,
			key TEXT NOT NULL,
			url TEXT NOT NULL
			);
		"""
		# формируем специальную структуру базы
		self.cursor.execute(create_table_query)
		self.__saving_changes()

	def get_num_all_rows(self):
		# Получаем количество строк в таблице urls
		self.cursor.execute("SELECT COUNT(*) FROM urls")  
		return self.cursor.fetchone()[0]

	def create_new_row(self, new_key, new_url):
		number_rows = self.get_num_all_rows()
		# Создаём номер новой строки
		next_number = number_rows + 1
		# Создаём новую строку со необходимыми значениями
		self.cursor.execute("INSERT INTO urls VALUES (?, ?, ?)", (next_number, new_key, new_url))
		self.__saving_changes()

	def delete_line_by_number(self, number):
		""" Удаляем строку по номеру """
		self.cursor.execute("DELETE FROM urls WHERE num=?", (number,))

		self.__saving_changes()

		# обновляем нумерацию в столбце num. Так как при удалении появился разрыв в нумерации
		self.__update_col_num()

	def __update_col_num(self):
		""" Обновляем числа в столбце num """
		# Запрос выберет все данные из таблицы urls, отсортировав строки по значению столбца num.
		self.cursor.execute("SELECT * FROM urls ORDER BY num")
		rows = self.cursor.fetchall()
		
		# Создаём список. От 1 до максимума. Где максимум, это количество строк в таблице
		# Предположу, что использование вот такого варианта list(range(1, len(self.get_num_all_rows())+1)), забирает чуть больше ресурсов.
		# Поэтому реализовал без обращения к функции
		list_new_numbers = list(range(1, len(rows)+1))
		# Обновите столбец 'number' с новыми значениями
		for new_number in list_new_numbers:
			# получаем старое значение num в строке, чтобы потом его заменить на новое
			old_number = rows[new_number-1][0]
			self.cursor.execute("UPDATE urls SET num = ? WHERE num = ?", (new_number, old_number))

		self.__saving_changes()
		
	def get_all_table(self):
		self.cursor.execute("SELECT * FROM urls ORDER BY num")
		return self.cursor.fetchall()

	def close(self):
		self.__saving_changes()
		self.cursor.close()
		self.conn.close()
