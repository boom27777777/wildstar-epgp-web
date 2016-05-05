import json
import time
from os.path import getatime
from datetime import datetime


class Guild:
    def __init__(self):
        self._members = []
        self.data = None

    def from_json(self, blob, append=False, _fix=False):
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

        if not _fix:
            self.fix_dict_logs()

    def export(self, path=None):
        if path is None:
            return json.dumps(self.data)

        with open(path, 'w') as export_file:
            json.dump(self.data, export_file)

    def export_loot(self):
        logs = {'logs': self.logs}
        return json.dumps(logs)

    def refresh(self, _fix=False):
        self.from_json(self.export(), _fix=_fix)

    def add_player(self, name, _class=None, _roll=None):
        player = {'strName': name, 'class': _class, 'role': _roll}
        self._members.append(Player(player))

    def player_by_name(self, player):
        for player_obj in self._members:
            if player_obj.name == player:
                return player_obj

    def decay(self, percent: float = 0.1):
        log_time = round(time.time(), 0)
        for player in self._members:
            d_gp = round(player.gp * percent, 0)
            if player.gp - d_gp < 2000:
                d_gp = 2000 - player.gp

            player.raw_data['GP'] -= d_gp
            player.gp = player.raw_data['GP']
            player.raw_data['logs'].insert(
                0,
                {
                    'nAfter': player.gp,
                    'strModifier': '{}'.format(-d_gp),
                    'strComment': '10% GP Decay',
                    'nDate': log_time,
                    'strType': '{Decay}',
                    'strGroup': 'Def'
                })

            d_ep = round(player.ep * percent, 0)
            if player.ep - d_ep < 750:
                d_ep = 750 - player.e

            player.raw_data['EP'] -= d_ep
            player.ep = player.raw_data['EP']
            player.raw_data['logs'].insert(
                0,
                {
                    'nAfter': player.ep,
                    'strModifier': '{}'.format(-d_ep),
                    'strComment': '10% EP Decay',
                    'nDate': round(time.time(), 0),
                    'strType': '{Decay}',
                    'strGroup': 'Def'
                })

        self.refresh()

    def fix_dict_logs(self):
        for raider in self._members:
            if type(raider.logs) is dict:
                raider.raw_data['logs'] = [v for v in raider.logs.values()]

        self.refresh(_fix=True)

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
            Must contain keys: strName
        """
        self.raw_data = player_dict
        self.name = self.raw_data['strName']

        # Ain't nobody got space for all this
        get = lambda key, default: self.raw_data.setdefault(key, default)

        self.class_name = get('class', 'N/A')
        self.gp = int(get('GP', 0))
        self.ep = int(get('EP', 0))
        self.base_gp = get('nBaseGP', 1000)
        self.role = get('role', 'DPS')
        self.off_role = get('offrole', 'N/A')
        self._logs = get('logs', {})
        self.l_logs = get('tLLogs', [])
        self.tot = get('tot', 0)
        self.net = get('net', 0)
        self.data_sets = get('tDataSets', [])
        self.alts = get('alts', [])
        self.armory = get('tArmoryEntry', [])

        try:
            self.fix_dates()
        except:
            a = 1

    def fix_dates(self):
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

    @property
    def logs(self):
        if self._logs:
            return sorted(
                self._logs,
                key=lambda x: x['nDate'] if type(x) is dict else 0,
                reverse=True
            )
        else:
            return []

    def __repr__(self):
        return self.name
