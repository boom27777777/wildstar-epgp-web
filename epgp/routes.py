import time
import flask
from flask_login import login_user, login_required, logout_user

from epgp import get_resource
from epgp.database import db_session
from epgp.user import User
from epgp.application import app, login_manager, guild, build_pages
from epgp.pages import Raider


index_page, loot_page, import_page = build_pages(guild)


@app.route('/')
def index():
    return index_page.render()


@app.route('/raider/<name>')
def raider(name):
    player = index_page.guild.player_by_name(name.replace('_', ' '))
    if player:
        return Raider(player).render()
    else:
        flask.abort(404)


@app.route('/loot')
def loot():
    return loot_page.render()


@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if flask.request.method.lower() == 'post':
        data = flask.request.form
        user = User.query.filter_by(name=data['username']).first()
        if not user:
            return flask.abort(401)
        if user.validate(data['password']):
            login_user(user)
            next_url = flask.request.args.get('next')
            if next_url == 'login':
                return flask.abort(400)
            return flask.redirect('/')
    return flask.render_template('login.tpl.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User._id == user_id).first()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/epgp/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


@app.route('/import')
@login_required
def import_data():
    return import_page.render()


@app.route('/do-import', methods=['POST'])
@login_required
def do_import():
    data = flask.request.form['json-data']
    try:
        guild.from_json(data)
        guild.export(get_resource('data', 'guild-{}.json'.format(time.time())))
    except BaseException:
        return flask.abort(422)
    return flask.redirect('/')


@app.route('/rules')
def rules():
    return flask.render_template('rules.tpl.html')


@app.route('/api/export/all')
def api_export():
    return guild.export()


@app.route('/api/export/loot')
def api_export_loot():
    return guild.export_loot()


@app.route('/api/import', methods=['POST'])
def api_import():
    form = flask.request.form
    user = User.query.filter(
        User._api_key == bytes(form['api-key'].replace('\\n', '\n'), 'utf8')).first()
    if not user:
        return '{"status":"failed","reason":"Unauthorized"}', 401
    try:
        guild.from_json(form['json-data'])
        guild.export(get_resource('data', 'guild-{}.json'.format(time.time())))
    except BaseException:
        return flask.abort(422)
    return '{"status":"success"}', 200
