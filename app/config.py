import os


class Config(object):
    SECRET_KEY = ''
    SITE_NAME = 'Showtunes'
    PORT = int(os.getenv('PORT', '5000'))


class ProductionConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = 'e34c6ffc7bf25aef4b8528a29f6d36d8da6da556'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@db-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkyNTM'
    SG_CLIENT_SEC = 'WWqj2_4lUDZ903aMXtd1IXFbu1RoivejRqI5B7wi'


class StagingConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = ''
    SQLALCHEMY_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkyNTM'
    SG_CLIENT_SEC = 'WWqj2_4lUDZ903aMXtd1IXFbu1RoivejRqI5B7wi'


class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    EXCEPTIONAL_API_KEY = ''
    # EXCEPTIONAL_DEBUG_URL = 'http://requestb.in/1kmlz0e1'
    SQLALCHEMY_DATABASE_URI = 'mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay'
    SG_CLIENT_KEY = 'MjA3OTM1fDEzNjE0NTkzOTg'
    SG_CLIENT_SEC = '5tu1x0pYx8R_ouab_ZAeVJTUP-lzTelMJMP3qePi'
