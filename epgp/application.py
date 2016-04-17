import os
from flask import Flask
from flask_login import LoginManager

from epgp import get_resource
from epgp.pages import Index, Loot, Import, Edit
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

index_page = Index(guild)
loot_page = Loot(guild)
import_page = Import(guild)
edit_page = Edit(guild)
