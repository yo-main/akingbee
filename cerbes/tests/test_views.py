
# pylint: disable=redefined-outer-name,unused-import
import base64
import jwt
import uuid

import pytest

from cerbes.helpers import generate_jwt

TEST_USER = {
    "username": "Maya",
    "password": "ILoveHoney",
    "email": "maya.labeille@akingbee.com"
}

def test_user_post(test_app):
    response = test_app.post("/user", json=TEST_USER)
    assert response.status_code == 204

    response = test_app.post("/user", json=TEST_USER)
    assert response.status_code == 400
    assert response.json() == {"detail": "Registration failed"}


@pytest.mark.parametrize("creds,expected_code,expected_content", (
    (None, 401, "Missing access_token cookie"),
    ("testtest", 401, "Could not parse access_token"),
    ("::testtest", 401, "Could not parse access_token"),
    ("te:s:ttest", 401, "Could not parse access_token"),
    (":testtest", 401, "Wrong credentials"),
    ("testtest:", 401, "Wrong credentials"),
    ("Maya:ILovehoney", 401, "Wrong credentials"),
    ("ILoveHoney:Maya", 401, "Wrong credentials"),
    ("maya:ilovehoney", 401, "Wrong credentials"),
    ("maya.labeille@akingbee.com:ILoveHoney", 401, "Wrong credentials"),
    ("Maya:ILoveHoney", 200, None),
))
def test_login(test_app, creds, expected_code, expected_content):
    cookies = {}

    if creds is not None:
        creds = base64.b64encode(creds.encode()).decode()
        cookies["access_token"] = creds

    response = test_app.post("/login", cookies=cookies)
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
    response = test_app.post("/login", cookies={"access_token": creds})
    jwt = response.json()["access_right"]

    response = test_app.get("/check")
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": ""})
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": f"Base {jwt}"})
    assert response.status_code == 401

    response = test_app.get("/check", cookies={"access_token": jwt})
    assert response.status_code == 204
