import datetime
import os

import flask
from flask import Blueprint

from src.helpers.tools import render, redirect
from src.helpers.checkers import validate_email, validate_password
from src import constants
from src.errors import errors
from src.success import success
from src.config import CONFIG
from src.log.logger import logger
from src.helpers.users import (
    get_user_from_username,
    verify_password,
    create_password_hash,
    create_new_user,
)
from src.helpers.tools import login_required

from src.models import User

api = Blueprint("Users", __name__)


@api.route("/", methods=["GET"])
@login_required
def home():
    return render("akingbee/index_akb.html")


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


@api.route("/login", methods=["GET", "POST"])
def login():

    # We remove the user credentials if any in the cookie
    flask.session["user_id"] = None
    flask.session.pop("username", None)

    if flask.request.method == "GET":
        return render("akingbee/login.html")

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
    flask.session["username"] = user.username
    return success.LoginSuccess()


@api.route("/logout", methods=["GET"])
def logout():
    logger.info("Logout")
    flask.session["user_id"] = None
    flask.session.pop("username", None)
    return redirect("/")


@api.route("/language", methods=["POST"])
def updateLanguage():
    """Change the user language"""
    newLanguage = flask.request.form.get("language")

    if newLanguage not in constants.LANGUAGES:
        newLanguage = constants.ENGLISH

    flask.session["language"] = newLanguage
    return Success()


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

    return success.RegisterSuccess()


@api.route("/reset_password", methods=["GET", "POST"])
def reset_pwd():
    if flask.session.get("user_id") is not None:
        return redirect("/")

    if flask.request.method == "GET":
        return render("akingbee/reset_pwd.html")

    if flask.request.method == "POST":
        pwd = flask.request.form.get("pwd")
        username = flask.request.form.get("username")

        if not validate_password(pwd):
            raise errors.IncorrectPasswordFormat()

        hashed_pwd = create_password_hash(pwd)

        user = get_user_from_username(username)
        user.pwd = hashed_pwd
        user.save()

        return success.PasswordResetSuccess()
