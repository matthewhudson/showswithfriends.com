import os

class Config(object):
    SECRET_KEY = '!@#$%^&*(@IOMN)( ;oI*; "(@n!& )'
    SITE_NAME = 'nro'
    PORT = 5000
    RECON_SERVICE_URL = 'services-ec2-01.seatgeek.com:8400'

class ProductionConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = 'e34c6ffc7bf25aef4b8528a29f6d36d8da6da556'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql://delete_enabled:godlikepowers@db-ec2-02.seatgeek.com/scrapedb")
    SEATGEEK_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@db-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    PORT = 9600
    SG_CLIENT_KEY = 'NzYyNjd8MTM0NTIzOTk5MQ'
    SG_CLIENT_SEC = '4oQS3otqRbsvjZwMFAtDZXT-hybsKI7xVf5srOtE'
    SQLALCHEMY_BINDS = {
        'seatgeek': SEATGEEK_DATABASE_URI,
    }

class StagingConfig(Config):
    DEBUG = False
    EXCEPTIONAL_API_KEY = ''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql://root@localhost:3306/scrapedb")
    SEATGEEK_DATABASE_URI = os.environ.get("SG_DATABASE_URL", "mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay")
    PORT = 9600
    SG_CLIENT_KEY = 'NzYyNjd8MTM0NTU3NjQxMw'
    SG_CLIENT_SEC = 'MIxnAPtkRZUI_kAeAnMRSkKdnZCYjnlXbGcALcwg'
    SQLALCHEMY_BINDS = {
        'seatgeek': SEATGEEK_DATABASE_URI,
    }

class DevelopmentConfig(Config):
    '''Use "if app.debug" anywhere in your code, that code will run in development code.'''
    DEBUG = True
    EXCEPTIONAL_API_KEY = ''
    # EXCEPTIONAL_DEBUG_URL = 'http://requestb.in/1kmlz0e1'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:8889/scrapedb4?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
    SEATGEEK_DATABASE_URI = 'mysql://delete_enabled:godlikepowers@backup-ec2-02.seatgeek.com/tzanalytic_tixcast_ebay'
    SG_CLIENT_KEY = 'NzYyNjd8MTM0NTU2MzQyNQ'
    SG_CLIENT_SEC = 'x2st2rLD7jeD4h3dIAzQFF1Z8sYnTuYxibPcpG50'
    SQLALCHEMY_BINDS = {
        'seatgeek': SEATGEEK_DATABASE_URI,
    }
