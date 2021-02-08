import requests
from parsel import Selector


def search_char(char):
    r = requests.get(f'https://guildstats.eu/character?nick={char.name}#tab2')
    sel = Selector(r.text)

    char.online_time = sel.xpath('//table[@id="myTable"]//td[2]/text()').extract_first()
    return char
