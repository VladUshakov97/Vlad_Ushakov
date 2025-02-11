import requests



PAYLOAD = {"nTqMm": ""}
url_template = 'https://ru.wttr.in/{}'
cities = ['Лондон', 'Череповец', 'Шереметьево']

def main():
	for city in cities:
		url = url_template.format(city)
		response = requests.get(url, params=PAYLOAD)
		response.raise_for_status()

if __name__ == '__main__':
    main()


		
