import os, sys

current_path = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
sys.path.append(os.path.abspath(current_path + "/../../../utils/python"))

from flask import Flask
from flask.ext.exceptional import Exceptional
from flask.ext.seasurf import SeaSurf
from flask.ext.oauth import OAuth

from app.models import db

app = Flask(__name__)

# Configuration
if os.getenv('SG_ENV') == 'dev':
    app.config.from_object('app.config.DevelopmentConfig')
    app.logger.info("Config: Development")
elif os.getenv('SG_ENV') == 'staging':
    app.config.from_object('app.config.StagingConfig')
    app.logger.info("Config: Staging")
else:
    app.config.from_object('app.config.ProductionConfig')
    app.logger.info("Config: Production")

db.init_app(app)
exceptional = Exceptional(app)
csrf = SeaSurf(app)

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

import app.views

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    db.session.remove()
