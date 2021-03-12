import re

from functools import wraps
from flask import current_app, abort


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


def debug_only(f):
    @wraps(f)
    def wrapped(**kwargs):
        if not current_app.debug:
            abort(404)

        return f(**kwargs)

    return wrapped