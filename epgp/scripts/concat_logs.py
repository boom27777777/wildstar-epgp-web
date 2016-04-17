import os
import time
import json
from epgp import get_resource
from epgp.guild import Guild, Player


def add_logs(guild_1, file_name):
    guild_2 = Guild()
    guild_2.from_json(open(get_resource('data', file_name)))

    for mem_1, mem_2 in zip(guild_1._members, guild_2._members):
        if mem_1.name == mem_2.name:
            mem_1.raw_data['logs'] += mem_2.logs


def trim_logs(member: Player):
    json_set = set([json.dumps(i) for i in member.logs])
    clean = [json.loads(i) for i in json_set]
    member.raw_data['logs'] = clean


def fix():
    json_file = sorted(
        [f for f in os.listdir(get_resource('data')) if '.json' in f],
        reverse=True)
    log_1 = json_file[0]
    guild_1 = Guild()
    guild_1.from_json(open(get_resource('data', log_1)))

    for log_file in json_file:
        add_logs(guild_1, log_file)

    for member in guild_1._members:
        trim_logs(member)

    guild_1.export(get_resource('data', 'guild-{}.json.debug'.format(time.time())))


if __name__ == '__main__':
    fix()
