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

from app.helpers import (
        get_user_tracker,
        get_user_friends,
        get_user_events,
        add_affinity,
        get_venue_events,
        add_friendships
    )

# Rules
app.flask_app.add_url_rule('/', view_func=IndexView.as_view('index'))

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

def get_events(args):
    if args:
        venue_id = args.get('venue')
        if venue_id:
            return get_venue_events(db.session, g.user, venue_id)
        user_id = args.get('user_id')
        if user_id:
            user = db.session.query(User).filter(User.id==user_id).first()
            return get_user_events(db.session, user)
    return get_user_events(db.session, g.user)
    
def set_user(resp):
    try:
        g.user = db.session.query(User).filter_by(sg_id=resp["user_id"]).first()
    except:
        g.user = None

    if g.user is None:
        # create user
        resp = requests.get('http://api.seatgeek.com/2/me', params = {'access_token' : session['access_token']})

        sg_user = json.loads(resp.content)
        g.user = User(sg_user)
        try:
            db.session.add(g.user)
            db.session.commit()
            return True
        except:
            pass
    else:
        return False


@app.flask_app.before_request
def before_request():
    access_token = session.get('access_token')

    if app.flask_app.debug:
        g.user = db.session.query(User).filter_by(sg_id=36197).first()

    if access_token:
        resp = get_with_authentication('https://api.seatgeek.com/2/oauth/token')

        try:
            resp = json.loads(resp.content)
        except:
            abort(500)

        if resp['status'] == 200 and "preferences" in resp["scope"]:
            new_user = set_user(resp)
            if not new_user:
                return

            # store preferences
            resp = requests.get("https://api.seatgeek.com/2/preferences", params={'access_token': access_token})
            resp = json.loads(resp.content)
            performer_ids = [pref['performer']['id'] for pref in resp['preferences'] if pref['explicit']['preference'] is not None]
            performer_preferences = map(lambda x: UserPerformerPreference(user=g.user, performer_id=x), performer_ids)
            for pp in performer_preferences:
                db.session.merge(pp)

            # load affinity
            params = {
                'client_id' : app.flask_app.config['SG_CLIENT_KEY'],
                'lat' : g.user.lat,
                'lon' : g.user.lon,
                'performers.id' : performer_ids,
                'per_page' : 50
            }

            resp = json.loads(requests.get('https://api.seatgeek.com/2/recommendations', params=params).content)

            add_affinity(db.session, g.user, resp)

            db.session.commit()
            return
        else:
            del session['access_token']        
            return redirect(url_for('oauth'))

    if request.endpoint in ('oauth', 'sg_authorized') or 'favicon' in request.url:
        return

    return redirect(url_for('oauth'))

@app.flask_app.route('/add_friend', methods=['GET'])
def add_friend():
    if g.user is None:
        g.user = db.session.query(User).filter(User.id == 202).first()
    user_id = request.args.get('user_id')
    user = db.session.query(User).filter(User.id == user_id).first()
    add_friendships(db.session, [g.user, user])
    flash('friend added')
    print 'friend added'
    return redirect(url_for('index'))


@app.flask_app.route('/')
def index():
    if g.user is None:
        return render_template('home.html')
    args = request.args
    events = get_events(args)
    return_response = {
        "tracker" : get_user_tracker(db.session, g.user),
        "friends" : get_user_friends(db.session, g.user),
        "events" : events[0]
    }

    return json.dumps(return_response)

    #return render_template('home.html', res = return_response)


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
        raise
        abort(403)

    try:
        resp = json.loads(resp.content)
    except:
        raise
        abort(500)

    try:
        resp = requests.get('https://api.seatgeek.com/2/oauth/token', params={'access_token': resp['access_token']})
        token = json.loads(resp.content)
    except:
        raise
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
