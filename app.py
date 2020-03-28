import time

import flask
import flask_session

import yaml

from common import database as db
from common.config import CONFIG
from common.log.logger import logger, init_logging_filter

from webapp import views
from webapp.errors.base import BaseError
from webapp.helpers.date import jinja_date_formatting


def create_app():

    app = flask.Flask(__name__)

    app.config["TEMPLATE_AUTO_RELOAD"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = (
        60 * 60
    )  # lifetime of a cookie -> 1 hour
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = CONFIG.PATH_FLASK_SESSIONS
    app.config["SESSION_PERMANENT"] = False

    app.secret_key = CONFIG.SECRET_KEY

    app.debug = CONFIG.FLASK_DEBUG

    db.init()

    # JINJA
    app.jinja_env.filters["datetime"] = jinja_date_formatting

    # LOG SETUP
    init_logging_filter()
    app.before_request(do_stuff_before_request)
    app.after_request(do_stuff_after_request)

    # ERROR HANDLER
    app.errorhandler(BaseError)(handle_error)

    # COOKIES
    flask_session.Session(app)

    register_blueprint(app)

    return app


def do_stuff_before_request():
    log_before_request()


def do_stuff_after_request(response):
    log_after_request(response)
    close_database()
    return response


def can_log_request_info():
    url = flask.request.url
    return not url.endswith(
        (".svg", ".ico", ".js", ".css", ".json", ".html", "_/status")
    )


def log_before_request():
    flask.g.starting_time = time.time()


def log_after_request(response):
    if can_log_request_info():
        logger.info(
            "Response sent",
            status_code=response.status_code,
            duration=round(time.time() - flask.g.starting_time, 3),
        )


def close_database():
    # doing this in DEV will close the :memory: database - which we don't really want
    if not db.DB.is_closed() and not db.DB.database != ":memory":
        logger.info("Closing database connection")
        db.DB.close()


def handle_error(error):
    return error.to_dict(), error.code


def register_blueprint(app):
    app.register_blueprint(views.ns_users)
    app.register_blueprint(views.ns_apiary)
    app.register_blueprint(views.ns_hive)
    app.register_blueprint(views.ns_swarm)
    app.register_blueprint(views.ns_setup)
