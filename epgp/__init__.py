from os.path import abspath, join, dirname


def get_resource(*path):
    return abspath(join(dirname(__file__), *path))


from epgp.routes import app, guild


def shutdown():
    import time

    guild.export(get_resource('data', 'guild-{}.json'.format(time.time())))
