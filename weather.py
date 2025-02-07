import requests


url = 'https://wttr.in/Череповец?nTqMm&lang=ru'
response = requests.get(url)
response.raise_for_status()
print(response.text)