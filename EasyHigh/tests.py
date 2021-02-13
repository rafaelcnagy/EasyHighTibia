import json
from datetime import datetime

from flask import render_template

from models import Character, Frag
from utils import process_presences


def result():
    char_json = json.loads('{"name":"Lucca Redframe","title":"None (8 titles unlocked)","sex":"male","vocation":"Elite Knight","level":228,"achievement_points":151,"world":"Zenobra","residence":"Thais","house":{"name":"Treetop 13","town":"Ab\'Dendriel","paid":"2021-03-05","world":"Zenobra","houseid":0},"guild":{"name":"Zenobra Pune","rank":"One"},"last_login":[{"date":"2021-02-08 11:18:02.000000","timezone_type":2,"timezone":"CET"}],"account_status":"Premium Account","status":"offline"}')
    char = Character(name='Lucca Redframe', json=char_json)
    char.online_time = '154h 15min'
    char.kills.append(Frag(date=datetime(2020, 12, 12, 4, 52), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 12, 4, 24), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 12, 4, 7), target_name='Lius lambinha', target_level=19, frag_type='justified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 20)

    char.deaths.append(Frag(date=datetime(2020, 12, 12, 4, 58), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 12, 4, 42), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 12, 4, 33), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 12, 4, 15), target_name='Lucca Redframe', target_level=210, frag_type='justified', is_kill=False))
    char.deaths[-1].add_killer('Lambe lambe', 1000)

    char.kills.append(Frag(date=datetime(2020, 12, 11, 4, 51), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 11, 4, 22), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 11, 4, 4), target_name='Lius lambinha', target_level=19, frag_type='justified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 20)

    char.deaths.append(Frag(date=datetime(2020, 12, 11, 4, 57), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 11, 4, 44), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 11, 4, 33), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 11, 4, 11), target_name='Lucca Redframe', target_level=210, frag_type='justified', is_kill=False))
    char.deaths[-1].add_killer('Lambe lambe', 1000)

    char.kills.append(Frag(date=datetime(2020, 12, 10, 4, 57), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 10, 4, 29), target_name='Dell Brega', target_level=100, frag_type='injustified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 200)
    char.kills.append(Frag(date=datetime(2020, 12, 10, 4, 5), target_name='Lius lambinha', target_level=19, frag_type='justified', is_kill=True))
    char.kills[-1].add_killer('Lucca Redframe', 20)

    char.deaths.append(Frag(date=datetime(2020, 12, 10, 4, 59), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 10, 4, 49), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 10, 4, 30), target_name='Lucca Redframe', target_level=200, frag_type='injustified', is_kill=False))
    char.deaths[-1].add_killer('Lambinha delas', 800)
    char.deaths.append(Frag(date=datetime(2020, 12, 10, 4, 15), target_name='Lucca Redframe', target_level=210, frag_type='justified', is_kill=False))
    char.deaths[-1].add_killer('Lambe lambe', 1000)

    char.frags.extend(char.kills)
    char.frags.extend(char.deaths)
    char.frags.sort(key=lambda x: x.date, reverse=True)
    char = process_presences(char)

    return render_template('result.html', chars=[char])
