import time
import os
import re

import flask
from flask_login import login_user, login_required, logout_user

from epgp import get_resource
from epgp.application import app, login_manager, guild, index_page, \
    import_page, loot_page, edit_page
from epgp.database import db_session
from epgp.db_objects.user import User, user_by_api
from epgp.db_objects.suggestion import Suggestion
from epgp.pages import Raider
import epgp.scripts.concat_logs as concat_script


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


@app.route('/edit')
def edit():
    return edit_page.render()


@app.route('/suggest')
def suggest():
    return flask.render_template('suggest.tpl.html')


@app.route('/suggestions')
@login_required
def suggestions():
    return flask.render_template(
        'suggestions.tpl.html',
        suggestions=Suggestion.query.all()
    )


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User._id == user_id).first()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect('/')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/epgp/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)


@app.route('/api/import', methods=['POST'])
def api_import():
    form = flask.request.form
    user = user_by_api(form['api-key'])
    if not user:
        return '{"status":"failed","reason":"Unauthorized"}', 401
    try:
        guild.from_json(form['json-data'])
        guild.export(get_resource('data', 'guild-{}.json'.format(time.time())))
        concat_script.fix(3)
        json_file = sorted(
            [f for f in os.listdir(get_resource('data')) if '.json' in f], reverse=True)

        guild.from_json(open(get_resource('data', json_file[0])))
    except BaseException:
        return flask.abort(422)
    return '{"status":"success"}', 200


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


@app.route('/api/decay/all', methods=['POST'])
def api_decay():
    form = flask.request.form
    user = user_by_api(form['api-key'])
    if not user:
        return '{"status":"failed","reason":"Unauthorized"}', 401
    try:
        guild.decay()
        guild.from_json(guild.export())
        guild.export(get_resource('data', 'guild-{}.json'.format(time.time())))
    except BaseException as e:
        return flask.abort(422)
    return '{"status":"success"}', 200


@app.route('/api/suggest', methods=['POST'])
def api_suggest():
    form = flask.request.form
    tmp_suggest = re.sub(r'[^a-zA-z0-9 .,;\-\/_\'"]*', '', form['suggestion'])
    suggestion = Suggestion(tmp_suggest)
    db_session.add(suggestion)
    db_session.commit()

    return flask.redirect('/')


@app.route('/api/suggest/delete', methods=['POST'])
def api_delete_suggestion():
    form = flask.request.form
    sug_id = int(form['suggestion-id'])
    suggestion = Suggestion.query.filter(Suggestion._id == sug_id).first()
    db_session.delete(suggestion)
    db_session.commit()

    return flask.redirect('/suggestions')
