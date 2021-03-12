from flask import Flask, render_template, request, flash

import tests
from scrappers import tibiadata, tibiaring, guildstats
from utils import split_description, debug_only, CharacterNotExists, InvalidDescription

app = Flask(__name__)
app.secret_key = b'^H\xec\xe3\x0b?\x8d\x934\x17\xca\xd0Z\xf0a\xc9'


@app.route('/search', methods=['GET'])
def search_route():
    ts_description = request.args.get('description', '')
    if ts_description:
        return search(ts_description)
    else:
        return render_template('search.html')


@app.route('/')
def home():
    return render_template('search.html')


def search(ts_description):
    try:
        char_name_list = split_description(ts_description)
    except InvalidDescription:
        flash(u'Descrição inválida', 'error')
        return render_template('search.html')

        # errors = "Descrição inválida, verifique se a descrição está correta e que você copiou a descrição inteira."
        # return render_template('search.html', error=errors)

    char_list = list()

    try:
        driver = tibiaring.initialize_driver()
    except Exception as e:
        flash(f'Erro ao executar a busca, por favor, tente novamente ou entre em contato com um administrador.\nError: {e}', 'error')
        return render_template('search.html')

    for char_name in char_name_list:
        try:
            char = tibiadata.search_char(char_name)
            char = guildstats.search_char(char)
            char = tibiaring.search_char(char, driver)
            char.process_presences()
            char_list.append(char)
        except CharacterNotExists:
            flash(f'O character {char_name} não existe!', 'warning')
        except Exception as e:
            flash(f'Aconteceu um erro na busca do char {char_name}, por favor, tente novamente ou entre em contato com um administrador.\nError: {e}', 'error')
    driver.close()

    return render_template('result.html', chars=char_list)


@app.route('/test', methods=['GET'])
def test():
    return tests.result()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
