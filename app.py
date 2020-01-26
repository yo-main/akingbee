import flask
import flask_session

import yaml

from src import views
from src import database as db

from src.services.alerts import Error
from src.constants import alert_codes as alerts
from src.helpers.date import jinja_date_formatting
from src.config import CONFIG


def create_app():

    app = flask.Flask(__name__)

    app.config["TEMPLATE_AUTO_RELOAD"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = 60*60  # lifetime of a cookie -> 1 hour
    app.config["SESSION_TYPE"] = 'filesystem'
    app.config["SESSION_FILE_DIR"] = CONFIG.PATH_FLASK_SESSIONS
    app.config["SESSION_PERMANENT"] = False

    app.secret_key = CONFIG.SECRET_KEY

    app.debug = CONFIG.FLASK_DEBUG

    db.init()

    # JINJA
    app.jinja_env.filters['datetime'] = jinja_date_formatting

    # COOKIES
    flask_session.Session(app)

    register_blueprint(app)
    register_decorators(app)

    return app


def register_decorators(app):

    # @app.before_first_request
    # def session_configuration():
    #     # db.DB.init()
    #     # make cookies expires once the browser has been closed
    #     flask.session.permanent = False

    @app.after_request
    def after_request_func(f):
        # doing this in DEV will close the :memory: database - which we don't really want
        if not db.DB.is_closed() and not db.DB.database != ":memory":
            db.DB.close()
        return f

    @app.errorhandler(Error)
    def handle_error(error):
        response = flask.jsonify(error.to_dict())
        return response, 500


def register_blueprint(app):
    app.register_blueprint(views.ns_users)
    app.register_blueprint(views.ns_apiary)
    app.register_blueprint(views.ns_hive)
    app.register_blueprint(views.ns_swarm)
    app.register_blueprint(views.ns_setup)

