import re

def split_description(ts_description):
    if not re.match(
            ".+ \- Main: [A-Za-z \.']+ (?:[ \|]+[A-Za-z]+: (?:[A-Za-z \.']+(?:, [A-Za-z \.']+)*))+\| Reg: .+",
            ts_description, re.IGNORECASE | re.UNICODE):
        raise NotImplementedError()

    char_list = list()
    for char in re.findall("[A-Za-z]+: ([A-Za-z ,']+) \|", ts_description, re.IGNORECASE | re.UNICODE):
        chars = char.split(', ')
        char_list.extend(chars)

    return char_list


