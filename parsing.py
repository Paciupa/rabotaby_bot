from bs4 import BeautifulSoup
import requests

url = "https://rabota.by/search/vacancy?area=1002&enable_snippets=true&ored_clusters=true&text=инженер&search_period=1"
items_on_page = "&items_on_page=20"
pages = "&page="


# чтобы обойти ошибку 404, добавляю заголовок. Типо я реальный пользователь
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

number_vacancy = 0

for num_page in range(1000):
	url_ = f"{url}{items_on_page}{pages}{str(num_page)}"
	# print(url_)

	page = requests.get(url_, headers=headers)

	soup = BeautifulSoup(page.text, "html.parser")

	conteiners = soup.findAll('div', class_='serp-item')

	if conteiners != []:
		for conteiner in conteiners:
			strr = conteiner.find('a', class_='serp-item__title')
			# print(strr)
			href = strr['href']
			# Обрезаем всё с вопросительного знака и до конца
			url_vacancy = href.split("?")[0]
			name = strr.text

			number_vacancy += 1

			print(number_vacancy, name, "-->", url_vacancy)
	else:
		break
	

	# print(conteiners)