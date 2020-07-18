import os
import uuid
import datetime

import flask
from flask import Blueprint

from common.models import User
from common.database import DB
from common.config import CONFIG
from common.log.logger import logger

from akb.helpers.tools import render, redirect
from akb.helpers.checkers import validate_email, validate_password
from akb import constants
from akb.errors import errors
from akb.success import success
from akb.helpers.users import (
    get_user_from_username,
    verify_password,
    create_password_hash,
    create_new_user,
)
from akb.messaging.emails import send_reset_email
from akb.helpers.tools import login_required, anonymize_email


api = Blueprint("Users", __name__)


@api.route("/", methods=["GET"])
def home():
    user_id = flask.session.get("user_id")

    if user_id is None:
        return render("akingbee/login.html")

    return render("akingbee/index_akb.html")


@api.route("/_/status", methods=["GET"])
def healthcheck():
    try:
        DB.execute_sql("SELECT 1").fetchall()
    except Exception:
        logger.exception("Health check failed")
        return "DB Issue", 400

    return "OK", 200


@api.route("/images/<path:filename>", methods=["GET"])
def get_image(filename):
    filepath = os.path.join(CONFIG.PATH_IMAGES, filename)
    if os.path.exists(filepath):
        return flask.send_file(filepath, mimetype="image/svg+xml")
    return flask.abort(404)


@api.route("/favicon.ico", methods=["GET"])
def get_favicon():
    filepath = os.path.join(os.getcwd(), "favicon.ico")
    if os.path.exists(filepath):
        return flask.send_file(filepath, mimetype="image/x-con")
    return flask.abort(404)


@api.route("/login", methods=["POST"])
def login():
    # We remove the user id from the cookie (just in case)
    flask.session["user_id"] = None

    logger.info("Login attempt")

    username = flask.request.form.get("username")
    password = flask.request.form.get("password")

    user = get_user_from_username(username)

    # this variable should only be set to false in test
    if CONFIG.PASSWORD_REQUESTED:
        if not verify_password(user.pwd, password):
            raise errors.IncorrectPassword()

        # All good ! We can log in the user
        user.date_last_connection = datetime.datetime.now()
        user.save()

    flask.session["user_id"] = user.id

    logger.info(f"Login success for {username}")
    return success.LoginSuccess()


@api.route("/logout", methods=["GET"])
def logout():
    user_id = flask.session.pop("user_id", None)
    username = flask.session.pop("username", None)

    logger.info(f"Logout from {username}", user_id=user_id)
    return redirect("/")


@api.route("/language", methods=["POST"])
def updateLanguage():
    """Change the user language"""
    newLanguage = flask.request.form.get("language")

    if newLanguage not in constants.LANGUAGES:
        raise errors.UnknownLanguage(newLanguage)

    flask.session["language"] = newLanguage
    return success.LanguageChanged()


@api.route("/register", methods=["GET"])
def register():
    return render("akingbee/register.html")


@api.route("/registercheck", methods=["POST"])
def registerCheck():
    """
    Will check that we can correctly register a new user
    """
    logger.info("Registration attempt")

    data = {
        "pwd": flask.request.form.get("pwd"),
        "email": flask.request.form.get("email").lower(),
        "username": flask.request.form.get("username"),
    }

    if not validate_email(data["email"]):
        raise errors.IncorrectEmailFormat()

    if not validate_password(data["pwd"]):
        raise errors.IncorrectPasswordFormat()

    if not data["email"] or not data["username"]:
        raise errors.MissingInformation()

    user = User.select().where(User.username == data["username"]).count()
    if user:
        raise errors.UserAlreadyExists()

    email = User.select().where(User.email == data["email"]).count()
    if email:
        raise errors.UserAlreadyExists()

    create_new_user(data)

    logger.info("New user registered", user=user)
    return success.RegisterSuccess()


@api.route("/reset_password", methods=["GET", "POST"])
def reset_pwd_request():
    if flask.session.get("user_id") is not None:
        return redirect("/")

    if flask.request.method == "GET":
        return render("akingbee/reset_pwd_request.html")

    if flask.request.method == "POST":
        logger.info(flask.request.form)
        username = flask.request.form.get("username")

        user = tuple(
            User.select().where(
                (User.username == username) | (User.email == username)
            )
        )

        if not user:
            logger.exception(f"User doesn't exist: {username} - {user}")
            raise errors.UserNotFound()

        user = user[0]
        user.reset_pwd_id = uuid.uuid4()
        user.save()

        send_reset_email(user, flask.session.get("language", constants.FRENCH))

        return success.PasswordResetRequestSuccess(anonymize_email(user.email))


@api.route("/reset_password/<uuid:reset_id>", methods=["GET", "POST"])
def reset_pwd_action(reset_id):
    user = tuple(User.select().where(User.reset_pwd_id == reset_id))

    if not user:
        flask.abort(404)

    user = user[0]

    if flask.request.method == "GET":
        return render("akingbee/reset_pwd.html")

    if flask.request.method == "POST":
        password = flask.request.form.get("password")

        logger.info(password)
        if not validate_password(password):
            raise errors.IncorrectPasswordFormat()

        hashed_pwd = create_password_hash(password)

        user.pwd = hashed_pwd
        user.reset_pwd_id = None
        user.save()

        return success.PasswordResetSuccess()
