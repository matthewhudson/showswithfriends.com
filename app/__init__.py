import os

from flask import Flask
from flask.ext.exceptional import Exceptional
from flask.ext.seasurf import SeaSurf
from flask.ext.oauth import OAuth

from app.models import db

flask_app = Flask(__name__)

# Configuration
if os.getenv('SG_ENV') == 'dev':
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
    request_token_params={'scope': 'name,email,location,preferences,sg-access_level'}
)


@flask_app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    db.session.remove()


try:
    import newrelic.agent
    new_relic_app = newrelic.agent.wsgi_application()(flask_app)
except ImportError:
    print "Could not import New Relic"

# NOTE this is below the above due to a circular import issue documented here:
# http://flask.pocoo.org/docs/patterns/packages/
import app.views