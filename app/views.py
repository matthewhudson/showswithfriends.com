import os
import sys
import json

from flask import (abort,
                   flash,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
import requests


import app
from app.plugs.index import IndexView


# Rules
app.flask_app.add_url_rule('/', view_func=IndexView.as_view('index'))


@app.flask_app.before_request
def before_request():
    if app.flask_app.config['DEBUG']:
        return

    access_token = session.get('access_token')
    if access_token:

        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': access_token})

        try:
            resp = json.loads(resp.content)
        except:
            abort(500)

        if resp['status'] == 200 and "email" in resp["scope"]:
            return
        del session["access_token"]
    if request.endpoint in ('oauth', 'sg_authorized'):
        return
    return redirect(url_for('oauth'))


@app.flask_app.route('/')
def index():
    return render_template('home.html')


@app.flask_app.route('/oauth')
def oauth():
    return app.sg_oauth.authorize(callback='')


@app.flask_app.route('/oauth/fin')
def sg_authorized():
    params = {
        'code': request.args.get('code'),
        'client_id': app.flask_app.config['SG_CLIENT_KEY'],
        'client_secret': app.flask_app.config['SG_CLIENT_SEC']
    }
    resp = requests.get("https://api.seatgeek.com/2/oauth/access_token", params=params)
    if resp is None:
        abort(403)

    try:
        resp = json.loads(resp.content)
    except:
        abort(500)

    try:
        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': resp['access_token']})
        token = json.loads(resp.content)
    except:
        abort(403)

    flash('Sick, you are now logged in', category="success")
    session["access_token"] = token['access_token']
    return redirect(url_for('index'))


@app.flask_app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.flask_app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 404
