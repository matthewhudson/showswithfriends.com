import os


class Config(object):
    SECRET_KEY = 'REPLACE: SECRET KEY'
    SITE_NAME = 'REPLACE: PROJECT NAME'
    PORT = int(os.getenv('PORT', '5000'))


class ProductionConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = 'e34c6ffc7bf25aef4b8528a29f6d36d8da6da556'
    SQLALCHEMY_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@db-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    SG_CLIENT_KEY = ''  # REPLACE
    SG_CLIENT_SEC = ''  # REPLACE


class StagingConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = ''
    SQLALCHEMY_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    SG_CLIENT_KEY = ''  # REPLACE
    SG_CLIENT_SEC = ''  # REPLACE


class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    EXCEPTIONAL_API_KEY = ''
    # EXCEPTIONAL_DEBUG_URL = 'http://requestb.in/1kmlz0e1'
    SQLALCHEMY_DATABASE_URI = 'mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay'
    SG_CLIENT_KEY = ''  # REPLACE
    SG_CLIENT_SEC = ''  # REPLACE
