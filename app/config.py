import os


class Config(object):
    SECRET_KEY = ''
    SITE_NAME = 'Showtunes'
    PORT = int(os.getenv('PORT', '5000'))


class ProductionConfig(Config):
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    EXCEPTIONAL_API_KEY = '' #'e34c6ffc7bf25aef4b8528a29f6d36d8da6da556'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/showtunes'
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkyNTM'
    SG_CLIENT_SEC = 'WWqj2_4lUDZ903aMXtd1IXFbu1RoivejRqI5B7wi'


class StagingConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = ''
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/showtunes'
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkzOTg'
    SG_CLIENT_SEC = '5tu1x0pYx8R_ouab_ZAeVJTUP-lzTelMJMP3qePi'
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", 'postgres://mlfaerdqmihwqt:5uioakbw8XgNzAR1pNA6NE4RAS@ec2-107-21-122-236.compute-1.amazonaws.com:5432/dfmmm3r5jodsua')
    # SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkyNTM'
    # SG_CLIENT_SEC = 'WWqj2_4lUDZ903aMXtd1IXFbu1RoivejRqI5B7wi'


class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    EXCEPTIONAL_API_KEY = ''
    # EXCEPTIONAL_DEBUG_URL = 'http://requestb.in/1kmlz0e1'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/showtunes'
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NzAyNzk'
    SG_CLIENT_SEC = 'qNW_5O2Wpd6J2p682lC1iwuNnoMv51dvQkb4gm1P'
