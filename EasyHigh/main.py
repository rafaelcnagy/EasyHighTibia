from flask import Flask, render_template, request

from EasyHigh.scrappers import tibiadata, tibiaring, guildstats
from EasyHigh.scrappers.tibiaring import initialize_driver
from EasyHigh.utils import split_description, process_presences

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search_route():
    ts_description = request.args.get('description', '')
    if ts_description:
        chars = search(ts_description)
        return render_template('result.html', chars=chars)
    else:
        return render_template('search.html')


@app.route('/')
def home():
    return render_template('search.html')


def search(ts_description):
    char_list = list()
    char_name_list = split_description(ts_description)

    driver = initialize_driver()

    for char_name in char_name_list:
        char = tibiadata.search_char(char_name)
        char = guildstats.search_char(char)
        char = tibiaring.search_char(char, driver)
        char = process_presences(char)
        char_list.append(char)

    driver.close()
    return char_list
