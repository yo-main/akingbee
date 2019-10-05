import flask
import flask_session

from src.constants import environments as env
from src.services.date_formatting import date_formatting
from src.data_access.connectors import DB

app = flask.Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_FILE_DIR"] = env.FLASK_URL_SESSION
app.config["DATABASE"] = DB

app.secret_key = env.FLASK_SECRET_KEY

# JINJA
app.jinja_env.filters['datetime'] = date_formatting

# COOKIES
flask_session.Session(app)

@app.before_first_request
def session_configuration():
    # make cookies expires once the browser has been closed
    flask.session.permanent = False


@app.after_request
def after_request_func(f):
    app.config["DATABASE"].close()
    return f


import src.motor
