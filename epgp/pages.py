import flask
from epgp.guild import Guild


class Index:
    def __init__(self, guild):
        self.guild = guild
        self.add_player = self.guild.add_player

    def render(self):
        return flask.render_template('index.tpl', guild=self.guild)


class Raider:
    def __init__(self, raider):
        self.raider = raider

    def render(self):
        return flask.render_template('raider.tpl', raider=self.raider)


class Loot:
    def __init__(self, guild):
        self.guild = guild

    def render(self):
        return flask.render_template('loot.tpl', guild=self.guild)


class Import:
    def __init__(self, guild):
        self.guild = guild

    def render(self):
        return flask.render_template('import.tpl', guild=self.guild)
