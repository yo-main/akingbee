
# pylint: disable=redefined-outer-name,unused-import
import base64
import jwt
import uuid

from fastapi.testclient import TestClient
import pytest

from meltingpot.database.utils.test import test_db_url

from cerbes.app import AppClient
from cerbes.helpers import generate_jwt

TEST_USER = {
    "username": "Maya",
    "password": "ILoveHoney",
    "email": "maya.labeille@akingbee.com"
}


@pytest.fixture(scope="module")
def test_app(test_db_url):
    client = AppClient()
    client.enable_db(test_db_url)
    return TestClient(client.get_app())


def test_user_post(test_app):
    response = test_app.post("/user", json=TEST_USER)
    assert response.status_code == 204

    response = test_app.post("/user", json=TEST_USER)
    assert response.status_code == 400
    assert response.json() == {"detail": "Registration failed"}


@pytest.mark.parametrize("creds,expected_code,expected_content", (
    (None, 401, "Missing authorization header"),
    ("testtest", 401, "Could not parse authorization header"),
    ("::testtest", 401, "Could not parse authorization header"),
    ("te:s:ttest", 401, "Could not parse authorization header"),
    (":testtest", 401, "Wrong credentials"),
    ("testtest:", 401, "Wrong credentials"),
    ("Maya:ILovehoney", 401, "Wrong credentials"),
    ("ILoveHoney:Maya", 401, "Wrong credentials"),
    ("maya:ilovehoney", 401, "Wrong credentials"),
    ("maya.labeille@akingbee.com:ILoveHoney", 401, "Wrong credentials"),
    ("Maya:ILoveHoney", 200, None),
))
def test_login(test_app, creds, expected_code, expected_content):
    headers = {}

    if creds is not None:
        creds = base64.b64encode(creds.encode()).decode()
        creds = f"Base {creds}"
        headers["authorization"] = creds

    response = test_app.post("/login", headers=headers)
    assert response.status_code == expected_code
    if expected_content:
        assert response.json() == {"detail": expected_content}
    else:
        data = response.json()
        assert jwt.decode(data["access_right"], verify=False, algorithm="HS256")
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(data["access_right"], algorithm="HS256")


def test_check_jwt(test_app):
    creds = base64.b64encode("Maya:ILoveHoney".encode()).decode()
    creds = f"Base {creds}"
    response = test_app.post("/login", headers={"authorization": creds})
    jwt = response.json()["access_right"]

    # response = test_app.get("/check")
    # assert response.status_code == 401

    # response = test_app.get("/check", headers={"authorization": jwt})
    # assert response.status_code == 401

    # response = test_app.get("/check", headers={"authorization": f"Base {jwt}"})
    # assert response.status_code == 401

    response = test_app.get("/check", headers={"authorization": f"Bearer {jwt}"})
    assert response.status_code == 204
