import flask
import flask_session

from src.constants.environments import URL_FLASK_SESSION

app = flask.Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_FILE_DIR"] = URL_FLASK_SESSION

app.secret_key = """ZDFNqsovs1AL3n&:fd!!123dfq1nHcjAdfqçsdàçJCQFJs@"""

flask_session.Session(app)


@app.before_first_request
def session_configuration():
    # make cookies expires once the browser has been closed
    flask.session.permanent = False


import src.motor
