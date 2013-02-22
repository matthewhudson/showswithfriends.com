from sqlalchemy.orm import relation, backref
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
Base = declarative_base()

class User(Base):
    __tablename__   = 'users'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    sg_id       =   Column(u'sg_id', INTEGER(), primary_key=True)
    first_name  =   Column(u'first_name', VARCHAR(length=50))
    last_name   =   Column(u'last_name', VARCHAR(length=50))
    lat         =   Column(u'lat', Float(precision=None, asdecimal=False))
    lon         =   Column(u'lon', Float(precision=None, asdecimal=False))
    city        =   Column(u'city', VARCHAR(length=30))
    state       =   Column(u'state', VARCHAR(length=20))
    sg_access   =   Column(u'sg_access', INTEGER())
    created_at  =   Column(u'created_at', TIMESTAMP(timezone=False), default=datetime.now())
    updated_at  =   Column(u'updated_at', TIMESTAMP(timezone=False), default=datetime.now(), onupdate=datetime.now())

    def __init__(self, api_resp):
        self.sg_id = api_resp["user_id"]
        self.first_name = api_resp.get("first_name")
        self.last_name = api_resp.get("last_name")
        self.lat = api_resp.get('lat')
        self.lon = api_resp.get('lon')
        self.city = api_resp.get('city')
        self.state = api_resp.get('state')
        self.email = api_resp.get('email')
        self.sg_access = api_resp.get('sg_access')

class Friendship(Base):
    __tablename__   = 'friendships'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    friend_one  =   Column(u'friend_one', INTEGER(), ForeignKey('users.id'))
    friend_two  =   Column(u'friend_two', INTEGER(), ForeignKey('users.id'))
    status      =   Column(u'status', INTEGER(), default=0)
    created_at  =   Column(u'created_at', TIMESTAMP(timezone=False), default=datetime.now())
    updated_at  =   Column(u'updated_at', TIMESTAMP(timezone=False), default=datetime.now(), onupdate=datetime.now())

    user_one    =   relation(User, primaryjoin=friend_one == User.id)
    user_two    =   relation(User, primaryjoin=friend_two == User.id)

class UserPerformerPreference(Base):
    __tablename__   = 'user_performer_preferences'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    user_id     =   Column(u'user_id', INTEGER(), ForeignKey('users.id'))
    performer_id =  Column(u'performer_id', INTEGER())
    created_at  =   Column(u'created_at', TIMESTAMP(timezone=False), default=datetime.now())
    updated_at  =   Column(u'updated_at', TIMESTAMP(timezone=False), default=datetime.now(), onupdate=datetime.now())

    user        =   relation(User, primaryjoin=user_id == User.id)

class UserEventAffinity(Base):
    __tablename__   = 'user_event_affinity'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    user_id     =   Column(u'user_id', INTEGER(), ForeignKey('users.id'))
    event_id    =   Column(u'event_id', INTEGER())
    recommended =   Column(u'recommended', Float(precision=None, asdecimal=False))
    seen        =   Column(u'seen', INTEGER())
    shared_from =   Column(u'shared_from', INTEGER())
    shared_to   =   Column(u'shared_to', INTEGER())
    affinity    =   Column(u'affinity', Float(precision=None, asdecimal=False))

    user        =   relation(User, primaryjoin=user_id == User.id)

class EventShare(Base):
    __tablename__   = 'event_shares'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    user_from   =   Column(u'user_from', INTEGER(), ForeignKey('users.id'))
    user_to     =   Column(u'user_to', INTEGER(), ForeignKey('users.id'))
    event_id    =   Column(u'event_id', INTEGER())
