import os, sys

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
sys.path.append(os.path.abspath(current_path + "/../../../utils/python"))

from flask import Flask
from flask.ext.exceptional import Exceptional
from flask.ext.seasurf import SeaSurf
from flask.ext.oauth import OAuth

from nro.models import db

from lib.defcon import retrieval
from lib.defcon.context import Context

app = Flask(__name__)

# Configuration
if os.getenv('SG_ENV') == 'dev':
    app.config.from_object('nro.config.DevelopmentConfig')
    app.logger.info("Config: Development")
elif os.getenv('SG_ENV') == 'staging':
    app.config.from_object('nro.config.StagingConfig')
    app.logger.info("Config: Staging")
else:
    app.config.from_object('nro.config.ProductionConfig')
    app.logger.info("Config: Production")

db.init_app(app)
exceptional = Exceptional(app)
csrf = SeaSurf(app)

# No Cache, Please.
mmc = retrieval.MergeMarketCache(no_cache=True)

# fake out indexes
ctx = Context()

from lib.defcon.DBIndex import DBIndex
fake_venue_index     = DBIndex("venue", db.session)
fake_performer_index = DBIndex("performer", db.session)

ctx._venue_index = fake_venue_index
ctx._performer_index = fake_performer_index

oauth = OAuth()
sg_oauth = oauth.remote_app('seatgeek',
    base_url='https://seatgeek.com/',
    request_token_url=None,
    access_token_url='https://api.seatgeek.com/2/oauth/access_token',
    authorize_url='/oauth',
    consumer_key=app.config['SG_CLIENT_KEY'],
    consumer_secret=app.config['SG_CLIENT_SEC'],
    request_token_params={'scope': 'sg-recon-admin'}
)

import nro.views

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    db.session.remove()
