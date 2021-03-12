import datetime


class Character:
    def __init__(self, json):
        self.name = json['name'].split(' (')[0]
        self.level = json['level']
        self.vocation = json['vocation']
        self.world = json['world']
        self.account_status = json['account_status']
        self.guild = json['guild']['name'] if 'guild' in json else None

        self.traded = False
        self.trade_info = None

        self.last_login = datetime.datetime.strptime(json['last_login'][0]['date'], '%Y-%m-%d %H:%M:%S.%f')
        self.online_time = None

        self.ranking_position = 0
        self.points = 0
        self.kills = list()
        self.deaths = list()
        self.frags = list()
        self.presences = list()
        self.last_month_presences = list()

    def process_presences(self):
        if len(self.frags) > 0:
            this_participation = Presence(self.frags[0])
            for frag in self.frags[1:]:
                if this_participation.frags[-1].date - frag.date < datetime.timedelta(minutes=30):
                    this_participation.add_frag(frag)
                else:
                    self.presences.append(this_participation)
                    this_participation = Presence(frag)

            self.presences.append(this_participation)

        now = datetime.datetime.now()
        for presence in self.presences:
            if now - presence.frags[-1].date <= datetime.timedelta(days=30):
                self.last_month_presences.append(presence)
            else:
                break


class Frag:
    def __init__(self, date, target_name, target_level, frag_type, is_kill):
        self.date = date
        self.frag_type = frag_type
        self.target = SimpleCharacter(target_name, target_level)
        self.killers = list()
        self.is_kill = is_kill

    def add_killer(self, killer_name, killer_level):
        self.killers.append(SimpleCharacter(killer_name, killer_level))


class SimpleCharacter:
    def __init__(self, name, level):
        self.name = name
        self.level = level


class Presence:
    def __init__(self, first_frag=None):
        self.frags = list()
        self.qtd_deaths = 0
        self.qtd_kills = 0

        if first_frag:
            self.add_frag(first_frag)

    def add_frag(self, frag):
        self.frags.append(frag)
        if frag.is_kill:
            self.qtd_kills = self.qtd_kills + 1
        else:
            self.qtd_deaths = self.qtd_deaths + 1

    def get_duration(self):
        duration = self.frags[0].date - self.frags[-1].date
        return f'{str(duration.seconds//3600).zfill(2)}:{str((duration.seconds%3600)//60).zfill(2)}'
