import sys, os

from app import app, db, sg_oauth
from flask import request, redirect, url_for, abort, render_template, flash, session, g
from models.user import User

import auth

import requests, json

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
sys.path.append(os.path.abspath(current_path + "/../../../utils/python"))

from app.plugs.index import IndexView

# Rules
app.add_url_rule('/', view_func=IndexView.as_view('index'))

@app.before_request
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

@app.route('/')
@auth.require_inspect
def index():
    return render_template('home.html')

@app.route('/oauth')
def oauth():
    return sg_oauth.authorize(callback='')

@app.route('/oauth/fin')
def sg_authorized():
    params = {
        'code': request.args.get('code'),
        'client_id': app.config['SG_CLIENT_KEY'],
        'client_secret': app.config['SG_CLIENT_SEC']
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
        db.session.add(user)
    else: # a little hack to avoid another query to get the id from a newly created user.
        user.access_token = token['access_token']
        db.session.merge(user)
    db.session.commit()

    flash('Sick, you are now logged in and can admin the recons', category="success")
    session['user_id'] = user.id
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 404
