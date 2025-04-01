import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


class VKAPIError(Exception):
    pass


def shorten_link(token, user_url):
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": user_url,
        "private": 0
    }

    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=payload)
    response.raise_for_status()
    data = response.json()

    if 'error' in data:
        raise VKAPIError(data['error']['error_msg'])

    return data['response']['short_url']


def count_clicks(token, key):
    payload = {
        "access_token": token,
        "v": "5.199",
        "key": key,
        "interval": "forever",
        "extended": 0
    }

    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=payload)
    response.raise_for_status()
    data = response.json()

    if 'error' in data:
        raise VKAPIError(data['error']['error_msg'])

    return data['response']['stats']


def is_shorten_link(token, user_url):
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": user_url
    }

    response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=payload)
    response.raise_for_status()
    data = response.json()

    return 'response' in data and 'object_id' in data['response']


def extract_key(user_url):
    return urlparse(user_url).path.strip('/')


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')

    user_url = input("Введите ссылку: ")

    try:
        if is_shorten_link(token, user_url):
            key = extract_key(user_url)
            clicks = count_clicks(token, key)
            print("Клики:", clicks)
        else:
            short_link = shorten_link(token, user_url)
            print("Сокращенная ссылка:", short_link)

    except requests.exceptions.HTTPError as error:
        print(f"Ошибка сети: {error}")
    except VKAPIError as error:
        print(f"Ошибка API: {error}")


if __name__ == '__main__':
    main()
