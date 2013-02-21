from sqlalchemy.orm import relation, backref
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__   = 'users'

    id          =   Column(u'id', INTEGER(), primary_key=True)
    sg_id       =   Column(u'sg_id', INTEGER())
    first_name  =   Column(u'first_name', VARCHAR(length=50))
    last_name   =   Column(u'last_name', VARCHAR(length=50))
    lat         =   Column(u'lat', Float(precision=None, asdecimal=False))
    lon         =   Column(u'lon', Float(precision=None, asdecimal=False))
    city        =   Column(u'city', VARCHAR(length=30))
    state       =   Column(u'state', VARCHAR(length=20))

    def __init__(self, api_resp):
        self.sg_id = api_resp["user_id"]
        self.first_name = api_resp["first_name"]
        self.last_name = api_resp["last_name"]
        self.lat = api_resp.get('lat')
        self.lon = api_resp.get('lon')
        self.city = api_resp.get('city')
        self.state = api_resp.get('state')
        self.email = api_resp.get('email')
