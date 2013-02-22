import app

import requests, json

from app.models.tables import Friendship, User, UserEventAffinity, UserPerformerPreference
from itertools import permutations, groupby

from random import random

def add_friendships(session, users):
    for user_one, user_two in permutations(users, 2):
        f = session.query(Friendship).filter_by(user_one=user_one, user_two=user_two)
        if f.count() == 0 and random() < .5:
            f = Friendship(user_one=user_one, user_two=user_two, status=1)
            f = Friendship(user_two=user_one, user_one=user_two, status=1)
            session.merge(f)
    session.commit()


def add_affinity(session, user):
    # load affinity

    affinity = session.query(UserEventAffinity).filter_by(user_id = user.id)
    if affinity.count() > 0:
        return

    preferences = session.query(UserPerformerPreference).filter_by(user_id = user.id)
    if not preferences.count():
        return

    performer_ids = [up.performer_id for up in preferences]

    params = {
                'client_id' : app.flask_app.config['SG_CLIENT_KEY'],
                'lat' : user.lat,
                'lon' : user.lon,
                'performers.id' : performer_ids,
                'per_page' : 100,
                'taxonomies.id' : 2000000
    }

    resp = json.loads(requests.get('https://api.seatgeek.com/2/recommendations', params=params).content)

    recs = resp.get('recommendations')
    try:
        max_aff = min(recs[0]['score'],.5)
    except:
        return
    event_affinities = map(lambda x: UserEventAffinity(user=user,event_id=x['event']['id'],
                                                                    recommended=1, seen=0, shared_from=0, shared_to=0, affinity=x['score'] / max_aff),recs)

    for ev in event_affinities:
        session.merge(ev)
    session.commit()

def add_preference(session, user, resp):
    performer_ids = [pref['performer']['id'] for pref in resp['preferences'] if pref['explicit']['preference'] is not None]
    performer_preferences = map(lambda x: UserPerformerPreference(user=user, performer_id=x), performer_ids)
    for pp in performer_preferences:
        session.merge(pp)

#### user methods

def user_to_dict(user):
    user_dict = {}
    user_dict["id"] = user.id

    if user.first_name:
        user_dict["name"] = user.first_name + ' ' + user.last_name
    if user.lat:
        user_dict["location"] = {
            "lat" : user.lat,
            "lon" : user.lon
        }
    if user.city:
        user_dict["location"]["city"] = user.city

    return user_dict

from collections import defaultdict

def get_event_friend_mapping(session, user, event_ids):
    user_id = user.id
    friend_query = "select friend_two from friendships, users where friendships.friend_one = users.id and friend_one = {0}".format(user.id)
    friend_ids = [x[0] for x in session.execute(friend_query)]
    friend_id_string = ','.join(map(str, friend_ids))
    event_friend_map = defaultdict(list)
    event_id_string = ','.join(map(str,event_ids))
    query = """select event_id, ua.user_id friend_id, affinity friend_affinity from user_event_affinity ua where ua.user_id in({0}) and event_id in({1})""".format(friend_id_string, event_id_string)
    qs = session.execute(query)

    tuples = [tuple(x) for x in qs]
    for key, q in groupby(tuples, key=lambda e: e[0]):
        new_list = event_friend_map[key] + map(lambda x: (x[1], x[2]), list(q))
        new_list.sort(key=lambda e: -e[1])
        event_friend_map[key] = new_list
    return event_friend_map

def deduplicate(events):
    perfs = set()
    ids = list()
    for event in events:
        perf = event['performers'][0]['id']
        if perf not in perfs:
            perfs.add(perf)
            ids.append(event['id'])
    events = filter(lambda x: x['id'] in ids, events)
    return events

def get_user_friends(session, user):
    friend_query = "select friend_two from friendships, users where friendships.friend_one = users.id and friend_one = {0}".format(user.id)
    friend_ids = [x[0] for x in session.execute(friend_query)]
    friends = session.query(User).filter(User.id.in_(friend_ids))
    friend_set = set()
    for friend in friends:
        friend_set.add(friend)
    friend_list = map(user_to_dict, list(friend_set))
    return friend_list

def get_venue_events(session, user, venue_id):
    params = {
        "venue.id" : venue_id,
        "taxonomies.id" : 2000000
    }
    resp = requests.get('http://api.seatgeek.com/2/events',params=params)
    return get_events_from_api_result(session, user, resp)

def score_event_for_user(event):
    n_friends = len(event["friends"])
    self_score = event["event"]["score"]
    friend_score = 0
    if n_friends > 0:
        friend_score = sum(map(lambda x: x[1], event["friends"]))
    if self_score is None:
        return 0
    return friend_score

def get_user_events(session, user):
    eq = session.query(UserEventAffinity).filter_by(user_id=user.id)
    ids = [e.event_id for e in eq]
    resp = requests.get('http://api.seatgeek.com/2/events', params={'id' : ids, 'per_page' : 50})
    content = json.loads(resp.content)
    return get_events_from_api_result(session, user, resp)
    friend_map = get_event_friend_mapping(session, user, ids)
    events = resp['events']
    events = deduplicate(events)
    events = map(lambda x: {"friends" : friend_map.get(x['id'],[]),"event" : x},events)

    return events

def get_events_from_api_result(session, user, resp):
    resp = json.loads(resp.content)
    events = resp['events']
    events = deduplicate(events)
    ids = [x['id'] for x in events]
    friend_map = get_event_friend_mapping(session, user, ids)
    events = map(lambda x: {"friends" : friend_map.get(x['id'],[]),"event" : x},events)
    scores = map(score_event_for_user, events)
    x = zip(events, scores)
    x.sort(key=lambda e: -e[1])
    events, scores = zip(*x)
    return events

def get_user_tracker(session, user):
    prefs =  session.query(UserPerformerPreference).filter_by(user_id=user.id)
    return [pref.performer_id for pref in prefs]