# RabotaBy_bot

Telegram бот. Создан для ускорения поиска работы на сайте [rabota.by](https://rabota.by/), в режиме высокой конкуренции.
Он запускается локально на компьютере.

**❗❗❗ В проекте используется Python версии 3.12.3**

--- 
<details>
<summary><h3> 1. Работа с Telegram </h3></summary>

#### Создаём своего бота в Telegram
[Инструкция](https://core.telegram.org/bots/features#creating-a-new-bot)

#### Создание меню специальных команд для работы с ботом
- Введите команду `/setcommands` в [BotFather](https://t.me/BotFather)
- Выберете бота, которому нужно добавить команды
- Скопируйте все команды из файла `list_commands.md` в чат с BotFather и отправьте

#### Загрузка аватарки бота
- Введите команду `/setuserpic` в [BotFather](https://t.me/BotFather)
- Загрузите картинку `rabotaBY.jpg` без сжатия

</details>

--- 
<details>
<summary><h3> 2. Установка и запуск проекта </h3></summary>

```sh
# CodeBerg
git clone https://codeberg.org/femto/RabotaBy_bot.git
# или GitHub
git clone https://github.com/AnDsergey13/RabotaBy_bot.git
```

#### Откройте папку с проектом
```sh
cd RabotaBy_bot
```

#### Создание виртуальной среды (Linux)
```sh
python -m venv .venv
```

#### Откройте в удобном редакторе файл `.venv/bin/activate` (Linux)
Добавьте в конец файла следующие переменные окружения для `Bash` оболочки
```sh
## Telegram.py

# Пример: API_TELEGRAM_KEY="1111111111:AВKnNB61ehWUKnNBehWUIFXhWic_b8KnNBhW"
API_TELEGRAM_KEY="ваш ключ"
export API_TELEGRAM_KEY

# Пример: USER_ID="121212121"
USER_ID="ваш ID в Telegram"
export USER_ID

## Data.py
DB_HOST="localhost"
export DB_HOST

DB_PORT="5432"
export DB_PORT

# Пример: DB_NAME="db_rabota_by_bot"
DB_NAME="имя создаваемой базы данных"
export DB_NAME

# Пример: DB_USER="postgres"
DB_USER="имя пользователя для базы данных"
export DB_USER

# Пример: DB_PASSWORD="1111111"
DB_PASSWORD="ваш пароль от базы данных"
export DB_PASSWORD
```
для `Fish` оболочки открываем файл `.venv/bin/activate.fish` и добавляем следующие строки
```sh
## Telegram.py
# Пример: set -x API_TELEGRAM_KEY "1111111111:AВKnNB61ehWUKnNBehWUIFXhWic_b8KnNBhW"
set -x API_TELEGRAM_KEY "ваш ключ"
# Пример: set -x USER_ID "121212121"
set -x USER_ID "ваш ID в Telegram"

# Data.py
set -x DB_HOST "localhost"
set -x DB_PORT "5432"
# Пример: set -x DB_NAME "db_rabota_by_bot"
set -x DB_NAME "имя создаваемой базы данных"
# Пример: set -x DB_USER "postgres"
set -x DB_USER "имя пользователя для базы данных"
# Пример: set -x DB_PASSWORD "1111111"
set -x DB_PASSWORD "ваш пароль от базы данных"
```

#### Активация виртуальной среды (Linux)
```sh
# bash
source .venv/bin/activate
# или fish
source .venv/bin/activate.fish
```

#### Установка необходимых зависимостей
```sh
pip install -r requirements.txt 
```

### Запуск программы
```sh
python Telegram.py
```
</details>

--- 
<details open>
<summary><h3> 3. Взаимодействие с ботом </h3></summary>

--- 

<details open>
<summary><h4> 3.1 Базовые команды </h4></summary>

- `/start` - Запускает бота. 
	- ❗ Если серверная часть бота была перезагружена, то нужно заново зайти в бот и прописать эту команду
- `/help` - Выводит список и описание всех доступных команд

- `/update_time` - Устанавливает время обновления вакансий (в минутах). 
	- То есть, через сколько минут, бот заново будет парсить сайт [rabota.by](https://rabota.by/), для получения новых вакансий.
	- ❗ Перед первым запуском бота, если много включенных шаблонов (для проверки ввести `/print_t`), рекомендуется ставить время от 15 до 30 минут.
	- ❗ Так же, если вакансий приходит слишком много, то стоит увеличить время обновления.
- `/clear_visits` - Устанавливает время очистки списка посещений (в часах).
	- Чтобы вакансии не повторялись и выводились только новые, они записываются в таблицу visits_list в базе данных. Спустя установленное время они оттуда удаляются. Чем меньше установленное время, тем чаще будут попадаться повторы вакансий.
	- Рекомендуется ставить время от 2 недель
- `/print_s` - Выводит информацию о текущих настройках
</details>

--- 

<details>
<summary><h4> 3.2 Команды шаблонов поиска </h4></summary>

*Шаблон поиска*, это url по которому будут искаться вакансии
- Пример url: https://rabota.by/search/vacancy?search_period=1&area=1002&experience=noExperience&search_field=name&search_field=company_name&search_field=description&text=manager&enable_snippets=false
	- Расшифровка примера. Поиск по:
		- Cлову "manager"
		- Вакансии только "за сутки"
		- Вакансии только "без опыта работы"
- Шаблон поиска можно получить, просто скопировав адресную строку в браузере

- `/add_t`- Добавить шаблон поиска, по которому нужно искать вакансии.
	- У каждого шаблона нужно указать слово-ключ. Оно необходимо для понимания, какой шаблон за что отвечает
	- Так же, для удобства, указанное слово-ключ будет выводиться в виде тега в боте.
	- Пример вывода: #manager
- `/del_t` - Удалить шаблон поиска по указанному номеру
	- Номер шаблона можно узнать командой `/print_t`
- `/state_t` - Установить состояние для шаблона для парсинга сайта
	- Есть 2 состояния шаблона
		- 1(или 🟢) - это значит, что по данному шаблону парсится сайт.
		- 0(или 🔴) - это значит, что по данному шаблону сайт не парсится.
	- По умолчанию, при добавлении нового шаблона поиска `/add_t`, значение устанавливается в 1(или 🟢)
- `/print_t` - Вывести все шаблоны поиска
</details>

--- 

<details>
<summary><h4> 3.3 Команды шаблонов исключений </h4></summary>

*Шаблон исключения*, это url вакансии, которая нежелательна для появления в боте
- При добавлении url исключения, рекомендуется удалить лишнее
	- Правильно https://rabota.by/vacancy/89010007
	- Не правильно https://rabota.by/vacancy/89010007?query=manager&hhtmFrom=vacancy_search_list

- `/add_b` - Добавить исключение в чёрный список
	- У каждого исключения нужно указать слово-ключ. Для удобства, обычно, это название вакансии и компании
	- Пример слово-ключа: `Manager -> Lenta GOG`
- `/del_b` - Удалить исключение из чёрного списка
	- Номер исключения можно узнать командой `/print_b`
- `/state_b` - Установить состояние для исключения
	- Есть 2 состояния для исключения
		- 1(или 🟢) - это значит, что по данное исключение включено.
		- 0(или 🔴) - это значит, что по данное исключение отключено. И по нему вакансии не фильтруются
	- По умолчанию, при добавлении нового исключения `/add_b`, значение устанавливается в 1(или 🟢)
- `/print_b` - Вывести все исключения из чёрного списка

</details>