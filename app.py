import flask
import flask_session

app = flask.Flask(__name__)
app.config["TEMPLATE_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SESSION_FILE_DIR"] = "flask_session"

app.secret_key = """ZDFNqsovs1AL3n&:fd!!123dfq1nHcjAdfqçsdàçJCQFJs@"""

flask_session.Session(app)

import src.motor
