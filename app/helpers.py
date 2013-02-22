import app

import requests, json

from app.models.tables import Friendship, User, UserEventAffinity, UserPerformerPreference
from itertools import permutations, groupby

def add_friendships(session, users):
    for user_one, user_two in permutations(users, 2):
        f = Friendship(user_one=user_one, user_two=user_two, status=1)
        session.merge(f)
    session.commit()

def add_affinity(session, user, resp):
    # load affinity
    recs = resp.get('recommendations')
    event_affinities = map(lambda x: UserEventAffinity(user=user,event_id=x['event']['id'],
                                                                    recommended=1, seen=0, shared_from=0, shared_to=0, affinity=x['score']),recs)
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

def get_event_friend_mapping(session, user, event_ids):
    event_friend_map = {}
    event_id_string = ','.join(map(str,event_ids))
    user_id = user.id
    query = """select event_id, ua.user_id friend_id, affinity friend_affinity  from friendships f, user_event_affinity ua  where f.friend_one = {0} and f.friend_two = ua.user_id and event_id in ({1}) order by affinity desc""".format(user_id, event_id_string)
    qs = session.execute(query)
    for key, q in groupby(qs, key=lambda e: e[0]):
        event_friend_map[key] = [(x[1], x[2]) for x in q]
        
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
    friendships = session.query(Friendship, User).filter(Friendship.friend_two == User.id).filter(Friendship.status == 1)
    friends = set()
    for friendship, friend in friendships:
        friends.add(friend)
    friend_list = map(user_to_dict, list(friends))
    return friend_list

def get_user_events(session, user):
    eq = session.query(UserEventAffinity).filter_by(user_id=user.id)
    ids = list(set([e.event_id for e in eq]))
    resp = requests.get('http://api.seatgeek.com/2/events', params={'id' : ids, 'per_page' : 50})
    resp = json.loads(resp.content)
    friend_map = get_event_friend_mapping(session, user, ids)
    events = resp['events']
    events = deduplicate(events)
    events = map(lambda x: {"friends" : friend_map.get(x['id'],[]),"event" : x},events)
    return events

def get_user_tracker(session, user):
    prefs =  session.query(UserPerformerPreference).filter_by(user_id=user.id)
    return [pref.performer_id for pref in prefs]