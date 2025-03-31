import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


load_dotenv('api_parol.env')
token = os.getenv('TOKEN')

user_url = input("Введите ссылку: ")

def shorten_link(token, user_url):
    parsed_url = urlparse(user_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return None, "Ошибка: Некорректная ссылка"

    payload = {
        "access_token": token,
        "v": "5.199",
        "url": user_url,
        "private": 0
    }

    try:
        response = requests.get('https://api.vk.com/method/utils.getShortLink', params=payload)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            return None, f"Ошибка: {data['error']['error_msg']}"

        if 'response' in data and 'short_url' in data['response']:
            return data['response']['short_url'], data['response']['key']

        return None, "Ошибка: Не удалось получить сокращённую ссылку"

    except requests.exceptions.HTTPError as error:
        return None, f"Ошибка сети: {error}"

def count_clicks(token, key): 
    payload = {
        "access_token": token,
        "v": "5.199",
        "key": key,
        "interval": "forever",
        "extended": 0
    }

    try:
        response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=payload)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            return f"Ошибка: {data['error']['error_msg']}"

        if 'response' in data and 'stats' in data['response']:
            return data['response']['stats']

        return "Ошибка: Не удалось получить статистику по кликам"

    except requests.exceptions.HTTPError as error:
        return f"Ошибка сети: {error}"

def is_shorten_link(user_url):
    parsed_url = urlparse(user_url)
    if parsed_url.netloc in ['vk.cc']:
        key = parsed_url.path.strip('/')
        return user_url, key  
    else:
        return shorten_link(token, user_url)

def main():
    short_link, key = is_shorten_link(user_url)
    clicks = count_clicks(token, key)

    if short_link is None:
        print("Ошибка:", key)
    else:
        clicks = count_clicks(token, key)
        if urlparse(user_url).netloc == 'vk.cc':
            print("Клики:", clicks)
        else:
            print("Сокращенная ссылка:", short_link)
    
if __name__ == '__main__':
    main()
