import os
import sys

from flask import Flask
from flask.ext.exceptional import Exceptional
from flask.ext.seasurf import SeaSurf
from flask.ext.oauth import OAuth

from app.models import db

flask_app = Flask(__name__)


# TODO clean up the rather nasty circular import issue that is causing
# this to need to be after the above definition.
import app.views

# Configuration
if os.getenv('SG_ENV', "dev") == 'dev':
    flask_app.config.from_object('app.config.DevelopmentConfig')
    flask_app.logger.info("Config: Development")
elif os.getenv('SG_ENV') == 'staging':
    flask_app.config.from_object('app.config.StagingConfig')
    flask_app.logger.info("Config: Staging")
else:
    flask_app.config.from_object('app.config.ProductionConfig')
    flask_app.logger.info("Config: Production")

db.init_app(flask_app)
exceptional = Exceptional(flask_app)
csrf = SeaSurf(flask_app)

oauth = OAuth()
sg_oauth = oauth.remote_app('seatgeek',
    base_url='https://seatgeek.com/',
    request_token_url=None,
    access_token_url='https://api.seatgeek.com/2/oauth/access_token',
    authorize_url='/oauth',
    consumer_key=flask_app.config['SG_CLIENT_KEY'],
    consumer_secret=flask_app.config['SG_CLIENT_SEC'],
    request_token_params={'scope': 'sg-recon-admin'}
)

@flask_app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    db.session.remove()
