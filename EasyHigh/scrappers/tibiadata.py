import requests

from models import Character

from utils import CharacterNotExists


def search_char(name):
    r = requests.get(f'https://api.tibiadata.com/v2/characters/{name}.json')
    json = r.json()

    if 'error' in json['characters']:
        raise CharacterNotExists

    char = Character(json['characters']['data'])
    return char
