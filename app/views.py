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


from models import db
import app.dal as dal
from app.models.tables import User, UserPerformerPreference, UserEventAffinity

# Rules
#app.flask_app.add_url_rule('/', view_func=IndexView.as_view('index'))


@app.flask_app.before_request
def before_request():
    if app.flask_app.config['DEBUG']:
        g.user = db.session.query(User).first()

    access_token = session.get('access_token')

    if access_token:
        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': access_token})

        try:
            resp = json.loads(resp.content)
        except:
            abort(500)

        if resp['status'] == 200 and "preferences" in resp["scope"]:
            try:
                g.user = db.session.query(User).filter_by(sg_id=resp["user_id"]).first()
            except:
                g.user = None

            if g.user is None:
                # create user
                resp = requests.get('http://api.seatgeek.com/2/me', params = {'access_token' : access_token})

                sg_user = json.loads(resp.content)
                g.user = User(sg_user)
                
                db.session.merge(g.user)
                
                # load preferences
                resp = requests.get("https://api.seatgeek.com/2/preferences", params={'access_token': access_token})
                resp = json.loads(resp.content)
                performer_ids = [pref['performer']['id'] for pref in resp['preferences'] if pref['explicit']['preference'] is not None]
                performer_preferences = map(lambda x: UserPerformerPreference(user=g.user, performer_id=x), performer_ids)
                db.session.add_all(performer_preferences)

                # load affinity
                params = {
                    'client_id' : app.flask_app.config['SG_CLIENT_KEY'],
                    'lat' : g.user.lat,
                    'lon' : g.user.lon,
                    'performers.id' : performer_ids
                }

                resp = json.loads(requests.get('https://api.seatgeek.com/2/recommendations', params=params).content)

                recs = resp.get('recommendations')
                event_affinities = map(lambda x: UserEventAffinity(user=g.user,event_id=x['event']['id'],
                                                                    recommended=1, seen=0, shared_from=0, shared_to=0, affinity=x['score']),recs)
                db.session.add_all(event_affinities[:25])

                db.session.commit()

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
