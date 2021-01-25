from datetime import datetime


class Character:
    def __init__(self, name, json):
        self.name = name
        self.vocation = json['vocation']
        self.world = json['world']
        self.account_status = json['account_status']
        self.guild = json['guild']['name'] if 'guild' in json else None

        self.traded = False
        self.trade_info = None

        self.last_login = datetime.strptime(json['last_login'][0]['date'], '%Y-%m-%d %H:%M:%S.%f')
        self.online_time = None

        self.ranking_position = 0
        self.points = 0
        self.kills = list()
        self.deaths = list()


class Frag:
    def __init__(self, date, target_name, target_level, frag_type):
        self.date = date
        self.frag_type = frag_type
        self.target = SimpleCharacter(target_name, target_level)
        self.killers = list()

    def add_killer(self, killer_name, killer_level):
        self.killers.append(SimpleCharacter(killer_name, killer_level))


class SimpleCharacter:
    def __init__(self, name, level):
        self.name = name
        self.level = level
