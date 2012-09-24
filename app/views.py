import os
import sys
import json

from flask import (abort,
                   flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
import requests


import app
from app.plugs.index import IndexView
import auth
import models
from models.user import User


# Rules
app.flask_app.add_url_rule('/', view_func=IndexView.as_view('index'))

@app.flask_app.before_request
def before_request():
    if session.get('user_id'):
        g.user = User.query.get(session.get('user_id'))
        if g.user is None:
            session['user_id'] = None
            return redirect(url_for('oauth'))
        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': g.user.access_token})

        try:
            resp = json.loads(resp.content)
        except:
            abort(500)

        if resp['status'] != 200:
            redirect(url_for('oauth'))
    elif request.endpoint != 'oauth' and request.endpoint != 'sg_authorized':
        return redirect(url_for('oauth'))

@app.flask_app.route('/')
@auth.require_inspect
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

    # Check the TS
    try:
        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': resp['access_token']})
        token = json.loads(resp.content)
    except:
        abort(403)

    user = User.query.filter_by(sg_id=token['user_id']).first()
    if user is None:
        user = User(token['user_id'])
        user.access_token = token['access_token']
        models.db.session.add(user)
    else: # a little hack to avoid another query to get the id from a newly created user.
        user.access_token = token['access_token']
        models.db.session.merge(user)
    models.db.session.commit()

    flash('Sick, you are now logged in and can admin the recons', category="success")
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.flask_app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.flask_app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 404
