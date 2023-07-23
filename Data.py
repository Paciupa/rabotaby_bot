# Просмотр базы на пк
# https://sqlitebrowser.org/dl/

import sqlite3

class Base:
	""" """
	def __init__(self, file):
		self.file = file
		self.__connect()
		self.__get_names_all_column()

	def __connect(self):
		self.conn = sqlite3.connect(self.file)
		self.cursor = self.conn.cursor()

	def __get_names_all_column(self):
		""" Если вдруг названия столбцов изменилось, то с помощью get_names_colomns(), можно будет получить этот список """
		self.cursor.execute("PRAGMA table_info(users)")
		# Если нету имён, то их создаём 
		self.names_columns = [column[1] for column in self.cursor.fetchall()]

	def get_names_colomns(self):
		return self.names_columns

	def get_string_by_id(self, user_id):
		self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
		return self.cursor.fetchone()

	def check_user_id(self, user_id):
		self.cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)", (user_id,))

		return bool(self.cursor.fetchone()[0])

	def close(self):
		self.cursor.close()
		self.conn.close()


class UserData(Base):
	def create_string(self, user_id = None, first_name = None, last_name = None, username = None, nickname = None, gender = None, age = None):
		# Создание новой строки
		self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)",
						(user_id, first_name, last_name, username, nickname, gender, age))
		# Сохранить новую строку
		self.conn.commit()

	def delete_string_by_id(self, user_id):
		self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
		# Сохранение изменений
		self.conn.commit()

	def get_cell(self, user_id, column_name):
		# Запрос данных из ячейки
		self.cursor.execute("SELECT {} FROM users WHERE user_id = ?".format(column_name), (user_id,))
		data = self.cursor.fetchone()

		if data:
			# Обрезаем лишнее, и возвращаем результат
			return data[0]
		else:
			return None

	def set_sell(self, user_id, column_name, new_value = None):
		self.cursor.execute("UPDATE users SET {} = ? WHERE user_id = ?".format(column_name), (new_value, user_id))
		# Сохранение изменений
		self.conn.commit()
