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
from app.models.tables import (
        User, 
        UserPerformerPreference, 
        UserEventAffinity, 
        Friendship)

# Rules
app.flask_app.add_url_rule('/', view_func=IndexView.as_view('index'))

def get_events():
    eq = db.session.query(UserEventAffinity).filter_by(user_id=g.user.id)
    return [e.event_id for e in eq]

def get_friends(event_id):
    users = db.session.query(User, Friendship).filter(Friendship.friend_one==g.user.id).filter(User.id == Friendship.friend_two)
    return [user[0].sg_id for user in users]

def get_with_authentication(url, *args, **kwargs):
    params = kwargs.get('params', {})
    params = {'access_token': session['access_token']}
    return requests.get(url, params=params)

def post_with_authentication(url, *args, **kwargs):
    params = kwargs.get('params', {})
    params['access_token'] = session['access_token']
    params['consumer_key'] = app.flask_app.config['SG_CLIENT_KEY']
    kwargs['params'] = params
    return requests.post(url, **kwargs)

@app.flask_app.before_request
def before_request():
    if app.flask_app.config['DEBUG']:
        g.user = db.session.query(User).first()

    access_token = session.get('access_token')

    if access_token:
        resp = get_with_authentication('https://api.seatgeek.com/2/oauth/token')

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
                try:
                    db.session.add(g.user)
                except:
                    pass
                
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
                    'performers.id' : performer_ids,
                    'per_page' : 50
                }

                resp = json.loads(requests.get('https://api.seatgeek.com/2/recommendations', params=params).content)

                recs = resp.get('recommendations')
                event_affinities = map(lambda x: UserEventAffinity(user=g.user,event_id=x['event']['id'],
                                                                    recommended=1, seen=0, shared_from=0, shared_to=0, affinity=x['score']),recs)

                db.session.add_all(event_affinities[:25])

                # make everybody my friend
                me = db.session.query(User).filter_by(sg_id=207935).first()
                if me is not None:
                    f = Friendship(user_one=me, user_two=g.user, status=1)
                    f2 = Friendship(user_two=me, user_one=g.user, status=1)
                    db.session.add_all([f,f2])

                db.session.commit()

            return
        else:
            return redirect(url_for('oauth'))

    if request.endpoint in ('oauth', 'sg_authorized'):
        return
    return redirect(url_for('oauth'))


@app.flask_app.route('/')
def index():
    event_ids = get_events()
    resp = requests.get('http://api.seatgeek.com/2/events', params={'id' : event_ids, 'per_page' : 50})
    resp = json.loads(resp.content)
    events = resp['events']

    return_objects = []

    for event in events:
        return_object = {}
        return_object["event"] = event
        return_object["friends"] = get_friends(event)
        return_objects.append(return_object)

    return json.dumps(return_objects)

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
    return redirect('/')


@app.flask_app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.flask_app.errorhandler(403)
def forbidden(error):
    return render_template('forbidden.html'), 404
