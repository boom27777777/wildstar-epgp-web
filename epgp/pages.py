import flask
from epgp.guild import Guild


class Index:
    def __init__(self, guild):
        self.guild = guild
        self.add_player = self.guild.add_player

    def render(self):
        return flask.render_template('index.tpl.html', guild=self.guild)


class Raider:
    def __init__(self, raider):
        self.raider = raider

    def render(self):
        return flask.render_template('raider.tpl.html', raider=self.raider)


class Loot:
    def __init__(self, guild):
        self.guild = guild

    def render(self):
        return flask.render_template('loot.tpl.html', guild=self.guild)


class Import:
    def __init__(self, guild):
        self.guild = guild

    def render(self):
        return flask.render_template('import.tpl.html', guild=self.guild)


class Edit:
    def __init__(self, guild):
        self.guild = guild

    def render(self):
        return flask.render_template('edit.tpl.html', guild=self.guild)
