import requests
import json

class AmbiguousCardError(Exception):
    pass

scryfall_named_endpoint_random = 'https://api.scryfall.com/cards/random'


def get_card_image_from_json(j, size='normal'):
    return j['image_uris'][size]


def get_card_image_by_query(q):
    query = q.replace(' ','+')
    resp = requests.get(f'https://api.scryfall.com/cards/named?fuzzy={query}')
    if resp.json().get('object') == 'error':
        raise AmbiguousCardError
    return get_card_image_from_json(resp.json()), resp.json()['name']

def get_card_image_random():
    resp = requests.get(f'https://api.scryfall.com/cards/random')
    return get_card_image_from_json(resp.json()), resp.json()['name']