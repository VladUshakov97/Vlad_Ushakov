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
    response_json = response.json()

    return response_json['response']['short_url']


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
    stats_json = response.json()

    return stats_json['response']['stats']


def is_shorten_link(token, user_url):
    payload = {
        "access_token": token,
        "v": "5.199",
        "url": user_url
    }

    response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=payload)
    response.raise_for_status()
    screen_name_json = response.json()

    return 'response' in screen_name_json and 'object_id' in screen_name_json['response']


def main():
    load_dotenv()
    token = os.environ['VK_TOKEN']

    user_url = input("Введите ссылку: ")

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
