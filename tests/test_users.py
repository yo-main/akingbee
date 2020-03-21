import flask

import pytest

from webapp.constants import alert_codes
from common.models import User

from tests.fixtures import client, fake_database


def test_index_page_logged_out(client):
    answer = client.get("/", follow_redirects=True)

    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Login\n</title>" in answer.data


@pytest.mark.parametrize(
    "email",
    [
        "emailgmailcom",
        "emailgmail.com",
        "email@gmailcom",
        "@emailgmail.com",
        "email!@gmail.com",
        "email@gmail.1com",
        "email@gmai.lcom",
    ],
)
def test_register_user_wrong_email(email, client):
    form = {"username": "Hello", "email": email, "pwd": "c123aze123"}

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 400


@pytest.mark.parametrize(
    "password", ["c1", "123457123", "azebazeae", "AZEbazeabAZE", "AZEAZ123123"]
)
def test_register_user_wrong_password(password, client):
    form = {"username": "Yo", "email": "test@gmail.com", "pwd": password}

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_register_user_success(client):
    form = {
        "username": "user_test",
        "email": "test@test.com",
        "pwd": "azeAZE123!!",
    }

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 200


def test_register_user_username_taken(client):
    form = {
        "username": "user_test",
        "email": "testing@test.com",
        "pwd": "azeAZE123!!",
    }

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_register_user_email_taken(client):
    form = {
        "username": "user_testing",
        "email": "test@test.com",
        "pwd": "azeAZE123!!",
    }

    answer = client.post("/registercheck", data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_user_login_wrong_password(client):
    form = {"username": "user_test", "password": "1234"}
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_login_unknown_username(client):
    form = {"username": "user_testing", "password": "azeAZE123!!"}
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_user_login_success(client):
    form = {"username": "user_test", "password": "azeAZE123!!"}
    answer = client.post("/login", data=form, follow_redirects=True)

    assert answer.status_code == 200


def test_index_page_logged_in(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
    answer = client.get("/", follow_redirects=True)
    assert answer.status_code == 200
    assert b"<title>aKingBee - \n    Index\n</title>" in answer.data


@pytest.mark.parametrize("language", ("en", "fr"))
def test_change_language_success(language, client):
    form = {"language": language}

    answer = client.post("/language", data=form, follow_redirects=True)

    assert answer.status_code == 200


@pytest.mark.parametrize("language", ("gr", "us"))
def test_change_language_fail(language, client):
    form = {"language": language}

    answer = client.post("/language", data=form, follow_redirects=True)

    assert answer.status_code == 400


@pytest.mark.parametrize("username", ("Bob", "user_test@", ""))
def test_password_reset_request_fail(username, client, mocked_redis_client):
    form = {"username": username}
    answer = client.post("/reset_password", data=form, follow_redirects=True)
    assert answer.status_code == 400
    assert mocked_redis_client.not_called


@pytest.mark.parametrize("username", ("user_test", "test@test.com"))
def test_password_reset_request_success(username, client, mocked_redis_client):
    form = {"username": username}
    answer = client.post("/reset_password", data=form, follow_redirects=True)
    assert answer.status_code == 200
    assert mocked_redis_client.called


@pytest.mark.parametrize(
    "password", ["c1", "123457123", "azebazeae", "AZEbazeabAZE", "AZEAZ123123"]
)
def test_reset_password_fail(password, client):
    user = User.get(User.username == "user_test")
    form = {"password": password}
    url = f"/reset_password/{user.reset_pwd_id}"

    answer = client.post(url, data=form, follow_redirects=True)

    assert answer.status_code == 400


def test_reset_password_success(client):
    user = User.get(User.username == "user_test")
    form = {"password": "123azeAZE!"}
    url = f"/reset_password/{user.reset_pwd_id}"

    answer = client.post(url, data=form, follow_redirects=True)

    assert answer.status_code == 200
