import requests



payload = {"nTqMm": "", "lang=ru": ""}
url_template = 'https://wttr.in/{}'
cities = ['Лондон', 'Череповец', 'Шереметьево']

def main():
    for city in cities:
        url = url_template.format(city)
        response = requests.get(url, params=payload)
        response.raise_for_status()

if __name__ == "__main__":
    main()
    
