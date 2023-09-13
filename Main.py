# import Telegram

# import threading
# import time

# def get_current_datetime():
# 	from datetime import datetime
# 	pattern = "%H:%M:%S %d.%m.%Y"
# 	now = datetime.now()
# 	return now.strftime(pattern)

# def start():
# 	while True:
# 		print(f"-> {get_current_datetime()}")
# 		time.sleep(delay)

# def close():
# 	pass

# def set_time(time):
# 	global delay
# 	delay = time

# delay = 5 # секунды

# # в отдельном потоке запускаем Telegram.py 
# def TF():
# 	Telegram.main()

# telegram_flow = threading.Thread(target=TF)
# telegram_flow.start()

# start()
#  ####

# import asyncio
# import threading
# from Telegram import dp 
# import time

# def run_telegram():
# 	# await dp.start_polling()
# 	loop = asyncio.new_event_loop()
# 	loop.run_until_complete(dp.start_polling())
# 	loop.close()




# if __name__ == '__main__':
# 	telegram_thread = threading.Thread(target=run_telegram)
# 	telegram_thread.start()

# 	for i in range(20):
# 		print(i)
# 		time.sleep(1)

import threading
from Telegram import run_telegram
import time

if __name__ == '__main__':
	telegram_thread = threading.Thread(target=run_telegram)
	telegram_thread.start()
	for i in range(20):
		print(i)
		time.sleep(1)