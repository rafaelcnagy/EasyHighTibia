import requests

from EasyHigh.models import Character


def search_char(name):
    r = requests.get(f'https://api.tibiadata.com/v2/characters/{name}.json')
    json = r.json()

    char = Character(name, json['characters']['data'])
    return char
