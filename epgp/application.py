import os
from flask import Flask
from flask_login import LoginManager

from epgp import get_resource
from epgp.pages import Index, Loot, Import
from epgp.guild import Guild


app = Flask(__name__)

app.secret_key = 'TITS'

login_manager = LoginManager()
login_manager.init_app(app)

guild = Guild()
json_file = sorted(
    [f for f in os.listdir(get_resource('data')) if '.json' in f], reverse=True)

if json_file:
    guild.from_json(open(get_resource('data', json_file[0])))
else:
    app.logger.error('Failed to load json')


def build_pages(gld):
    index_page = Index(gld)
    loot_page = Loot(gld)
    import_page = Import(gld)

    return index_page, loot_page, import_page
