import json
import time
from os.path import getatime
from datetime import datetime


class Guild:
    def __init__(self):
        self._members = []
        self.data = None

    def from_json(self, blob, append=False):
        if type(blob) is str:
            self.data = json.loads(blob)
            self.last_update = datetime.fromtimestamp(
                time.time()).strftime('%d/%m/%Y')
        else:
            self.data = json.load(blob)
            self.last_update = datetime.fromtimestamp(
                getatime(blob.name)).strftime('%d/%m/%Y')

        if not append:
            self._members = []

        for member in self.data['tMembers']:
            player = Player(member)
            self._members.append(player)

    def export(self, path=None):
        if path is None:
            return json.dumps(self.data)

        with open(path, 'w') as export_file:
            json.dump(self.data, export_file)

    def export_loot(self):
        logs = {'logs': self.logs}
        return json.dumps(logs)

    def add_player(self, name, _class=None, _roll=None):
        player = {'strName': name, 'class': _class, 'role': _roll}
        self._members.append(Player(player))

    def player_by_name(self, player):
        for player_obj in self._members:
            if player_obj.name == player:
                return player_obj

    @property
    def _public_members(self):
        return [m for m in self._members if m.name != 'Guild Bank']

    def _sorted(self, key):
        return sorted(self._public_members, key=key)

    @property
    def by_role(self):
        return self._sorted(lambda x: x.role)

    @property
    def by_name(self):
        return self._sorted(lambda x: x.name.lower())

    @property
    def by_class(self):
        return self._sorted(lambda x: x.class_name.lower())

    @property
    def by_pr(self):
        return self._sorted(lambda x: x.pr)

    @property
    def by_ep(self):
        return self._sorted(lambda x: x.ep)

    @property
    def by_gp(self):
        return self._sorted(lambda x: x.gp)

    @property
    def logs(self):
        logs = []
        for raider in self.by_name:
            for entry in raider.logs:
                if not entry:
                    continue

                is_type = entry['strType'] == '{GP}'
                is_gear = entry['strComment'] not in [
                    'Set GP',
                    'Subtract GP',
                    'Add GP',
                    'Reset  to Base GP',
                    'Reset to Base GP'
                ]

                if is_type and is_gear:
                    logs.append((raider.name, entry))

        return sorted(logs, key=lambda x: x[1]['nDate'], reverse=True)


class Player:
    def __init__(self, player_dict):
        """Initializes a new player from a dictionary

        :param player_dict:
/            Must contain keys: strName
        """

        self.name = player_dict['strName']

        # Ain't nobody got space for all this
        get = lambda key, default: player_dict.setdefault(key, default)

        self.class_name = get('class', 'N/A')
        self.gp = get('GP', 0)
        self.ep = get('EP', 0)
        self.base_gp = get('nBaseGP', 1000)
        self.role = get('role', 'DPS')
        self.off_role = get('offrole', 'N/A')
        self.logs = get('logs', [])
        self.l_logs = get('tLLogs', [])
        self.tot = get('tot', 0)
        self.net = get('net', 0)
        self.data_sets = get('tDataSets', [])
        self.alts = get('alts', [])
        self.armory = get('tArmoryEntry', [])

        try:
            self._fix_dates()
        except:
            a = 1

    def _fix_dates(self):
        for line in self.logs:
            try:
                line['strDate'] = datetime.fromtimestamp(
                    line['nDate']).strftime('%d/%m/%Y')
                line['strTime'] = datetime.fromtimestamp(
                    line['nDate']).strftime('%H:%M:%S')
                line['Type'] = line['strType'].strip('{').strip('}')
            except:
                continue

    @property
    def pr(self):
        if self.gp > 0:
            return self.ep / self.gp
        else:
            return 0

    @property
    def gear(self):
        gear = []
        for item in self.armory.values():
            if 'id' in item:
                gear.append(item)
        return gear


    def __repr__(self):
        return self.name
