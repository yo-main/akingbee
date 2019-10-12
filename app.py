import flask
import flask_session

from src import database
from src.motor import api
from src.services.alerts import Error
from src.constants import environments as env
from src.helpers.date import jinja_date_formatting


app = flask.Flask(__name__)
app.register_blueprint(api)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = 60*10  # lifetime of a cookie -> 10 minutes
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_FILE_DIR"] = env.FLASK_URL_SESSION

app.secret_key = env.FLASK_SECRET_KEY

# JINJA
app.jinja_env.filters['datetime'] = jinja_date_formatting

# COOKIES
flask_session.Session(app)
database.init()

@app.before_first_request
def session_configuration():
    # make cookies expires once the browser has been closed
    flask.session.permanent = False


@app.after_request
def after_request_func(f):
    # doing this in DEV will close the :memory: database - which we don't really want
    if not database.DB.is_closed() and not database.DB.database != ":memory":
        database.DB.close()
    return f

@app.errorhandler(Error)
def handle_error(error):
    response = flask.jsonify(error.to_dict())
    return response, 500