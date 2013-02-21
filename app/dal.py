import app
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models import tables

DATABASE_URI = app.flask_app.config['SQLALCHEMY_DATABASE_URI']

def getSqlAlchemyConnection(database="showtunes", echo=False, scoped=False, pool_size=6):
    db = database
    engine = create_engine(DATABASE_URI, echo=echo, pool_size=pool_size, pool_recycle=3600)
    SessionMaker = sessionmaker(bind=engine)
    if scoped:
        session = scoped_session(SessionMaker)
    else:
        session = SessionMaker()
    return engine, SessionMaker, session

def _connect():
    return getSqlAlchemyConnection(pool_size=50)

def get_session():
    engine, maker, session = _connect()
    return session

def get_scoped_session():
    engine, maker, session = _connect()
    return scoped_session(maker)

def get_engine():
    engine, maker, session = _connect()
    return engine

def get_session_maker():
    _, maker, _ = _connect()
    return maker

def create_model_by_name(name):
    engine = get_engine()
    model = getattr(tables, name)
    model.__table__.create(engine)
