from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from flask_migrate import Migrate
from soccer.models import db as root_db, login_manager, ma

# CORS - cross origin resource sharing
from flask_cors import CORS

from soccer.helpers import JSONEncoder

app = Flask(__name__)

app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)


# Specifying a route for non authorized users
login_manager.login_view = 'auth.signin'

ma.init_app(app)
CORS(app)

app.json_encoder = JSONEncoder

from soccer import models