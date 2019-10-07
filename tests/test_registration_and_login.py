import flask

import pytest
from mock import MagicMock

from src.constants.environments import PLATFORM_ENVIRONMENT

# don't go further if the below assertion fails
assert PLATFORM_ENVIRONMENT == "DEV"

from tests.helpers import client, fake_database

from src.helpers import helpers
from src.constants import alert_codes
from src.data_access.pw_objects import MODELS





def test_index_page_logged_out(client):
    answer = client.get("/", follow_redirects=True)
    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Login\n</title>" in answer.data


@pytest.mark.parametrize("email", [
    "emailgmailcom",
    "emailgmail.com",
    "email@gmailcom",
    "@emailgmail.com",
    "email!@gmail.com",
    "email@gmail.1com",
    "email@gmai.lcom",
])
def test_register_user_wrong_email(email, client):
    form = {
        "username": "Hello",
        "email": email,
        "pwd": "c123aze123"
    }

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCORRECT_EMAIL_FORMAT
    assert answer.json["status"] == "error"


@pytest.mark.parametrize("password", [
    "c1",
    "123457123",
    "azebazeae",
    "AZEbazeabAZE",
    "AZEAZ123123",
]) 
def test_register_user_wrong_password(password, client):
    form = {
        "username": "Yo",
        "email": "test@gmail.com",
        "pwd": password
    }

    answer = client.post("/registercheck",
                            data=form,
                            follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCORRECT_PASSWORD_FORMAT
    assert answer.json["status"] == "error"


def test_register_user_success(client):
    form = {
        "username": "user_test",
        "email": "test@test.com",
        "pwd": "azeAZE123!!"
    }

    answer = client.post("/registercheck",
                            data=form,
                            follow_redirects=True)

    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.REGISTER_SUCCESS
    assert answer.json["status"] == "success"


def test_register_user_username_taken(client):
    form = {
        "username": "user_test",
        "email": "testing@test.com",
        "pwd": "azeAZE123!!"
    }

    answer = client.post("/registercheck",
                            data=form,
                            follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.USER_ALREADY_EXISTS_ERROR
    assert answer.json["status"] == "error"


def test_register_user_email_taken(client):
    form = {
        "username": "user_testing",
        "email": "test@test.com",
        "pwd": "azeAZE123!!"
    }

    answer = client.post("/registercheck",
                            data=form,
                            follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.EMAIL_ALREADY_EXISTS_ERROR
    assert answer.json["status"] == "error"


def test_user_login_wrong_password(client):
    form = {
        "username": "user_test",
        "password": "1234",
    }
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCORRECT_PASSWORD_ERROR
    assert answer.json["status"] == "error"


def test_login_unknown_username(client):
    form = {
        "username": "user_testing",
        "password": "azeAZE123!!",
    }
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.USER_NOT_FOUND_ERROR
    assert answer.json["status"] == "error"


def test_user_login_success(client):
    form = {
        "username": "user_test",
        "password": "azeAZE123!!",
    }
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.LOGIN_SUCCESS
    assert answer.json["status"] == "success"


def test_index_page_logged_in(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
    answer = client.get("/", follow_redirects=True)
    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Index\n</title>" in answer.data
    

@pytest.mark.parametrize("password", [
    "c1",
    "123457123",
    "azebazeae",
    "AZEbazeabAZE",
    "AZEAZ123123",
]) 
def test_reset_password_fail(password, client):
    form = {
        "username": "user_test",
        "pwd": password
    }

    answer = client.post("/reset_password",
                            data=form,
                            follow_redirects=True)

    assert answer.status_code == 500
    assert answer.json["code"] == alert_codes.INCORRECT_PASSWORD_FORMAT
    assert answer.json["status"] == "error"


def test_reset_password_success(client):
    form = {
        "username": "user_test",
        "pwd": "123azeAZE!",
    }
    
    answer = client.post("/reset_password", data=form, follow_redirects=True)

    assert answer.status_code == 200
    assert answer.json["code"] == alert_codes.PASSWORD_RESET_SUCCESS
    assert answer.json["status"] == "success"




