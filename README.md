# RabotaBy_bot

Telegram bot. Created to speed up job search on the site [rabota.by](https://rabota.by/) , in high competition mode.
It runs locally on the computer.

Для добавления в виртуальную среду переменных окружения, нужно
1) Открыть файл .venv/bin/activate
2) Добавить следующие строки в конец файла
	API_TELEGRAM_KEY="1212121212121212121212121212212"
	export API_TELEGRAM_KEY

	USER_ID="121212121"
	export USER_ID
где вместо 12121212... нужно вставить свои значения
3) Сохранить
4) Деактивировать среду
	deactivate
5) Подключится заново
	source .venv/bin/activate
6) Для получение значения из переменной окружения, нужно 
	from os import environ
	telegram_key = environ.get('API_TELEGRAM_KEY')
	print(telegram_key)