import re
import datetime

from functools import wraps
from flask import current_app, abort
from models import Presence


class InvalidDescription(Exception):
    pass


class CharacterNotExists(Exception):
    pass


def split_description(ts_description):
    if not re.match(
            ".+ \- Main: [A-Za-z \.']+ (?:[ \|]+[A-Za-z]+: (?:[A-Za-z \.']+(?:, [A-Za-z \.']+)*))+\| Reg: .+",
            ts_description, re.IGNORECASE | re.UNICODE):
        raise InvalidDescription()

    char_list = list()
    for char in re.findall("[A-Za-z]+: ([A-Za-z ,']+) \|", ts_description, re.IGNORECASE | re.UNICODE):
        chars = char.split(', ')
        char_list.extend(chars)

    return char_list


def process_presences(char):
    if len(char.frags) > 0:
        this_participation = Presence(char.frags[0])
        for frag in char.frags[1:]:
            if this_participation.frags[-1].date - frag.date < datetime.timedelta(minutes=30):
                this_participation.add_frag(frag)
            else:
                char.presences.append(this_participation)
                this_participation = Presence(frag)

        char.presences.append(this_participation)

    return char


def debug_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if not current_app.debug:
            abort(404)

        return f(**kwargs)

    return wrapped