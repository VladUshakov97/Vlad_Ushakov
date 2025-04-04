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
    response = response.json()

    return response['response']['short_url']


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
    stats = response.json()

    return stats['response']['stats']


def is_shorten_link(token, user_url):
    parsed_url = urlparse(user_url)
    key = parsed_url.path.strip('/')

    payload = {
        "access_token": token,
        "v": "5.199",
        "key": key,
        "interval": "forever"
    }

    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=payload)
    response.raise_for_status()
    link_info = response.json()

    return 'error' not in link_info 


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']

    user_url = input("Введите ссылку: ")
    parsed_url = urlparse(user_url)
    key = parsed_url.path.strip('/')

    try:
        if is_shorten_link(token, user_url):
            clicks = count_clicks(token, key)
            print("Клики:", clicks)
        else:
            short_link = shorten_link(token, user_url)
            print("Сокращенная ссылка:", short_link)

    except (requests.exceptions.HTTPError, KeyError) as error:
        print(f"Ошибка сети или API: {error}")


if __name__ == '__main__':
    main()
